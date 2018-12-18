import subprocess
from typing import List


def postgres_running_container_id_cmd() -> List[str]:
    return f'docker ps -f name={CONTAINER_NAME} -q'.split(' ')

def postgres_stopped_container_id_cmd() -> List[str]:
    return f'docker ps -f name={CONTAINER_NAME} -f status=exited -q'.split(' ')


def postgres_container_running() -> bool:
    return len(subprocess.check_output(postgres_running_container_id_cmd())) > 0

def postgres_container_stopped_exists() -> bool:
    return len(subprocess.check_output(postgres_stopped_container_id_cmd())) > 0


def postgres_image_id_cmd() -> List[str]:
    return 'docker images postgres -q'.split(' ')


def postgres_image_is_pulled() -> bool:
    return len(subprocess.check_output(postgres_image_id_cmd())) > 0


def start_postgres_cmd() -> List[str]:
    return (
        f'docker run '
        f'--name {CONTAINER_NAME} '
        f'-e POSTGRES_PASSWORD=test '
        f'-p {POSTGRES_PORT}:{POSTGRES_PORT} '
        f'-d postgres '
        # Following options are good for unit testing as they avoid writes
        # to disk. These are bad settings to use if you like your data to
        # be persistent across time, so don't cut and paste these options
        # into arbitrary use cases.
        f'-c fsync=off '
        f'-c full_page_writes=false'
    ).split(' ')


def pull_postgres_cmd() -> List[str]:
    return 'docker pull postgres'.split(' ')


def ensure_posgres_container_is_up() -> None:
    if postgres_container_running():
        print('Postgres is running in docker. Ready to test.')
        return

    if postgres_container_stopped_exists():
        print('Removing old stopped container')
        subprocess.check_call(
            f'docker rm {CONTAINER_NAME}'.split(' ')
        )

    if not postgres_image_is_pulled():
        print('Pulling postgres.')
        subprocess.check_call(pull_postgres_cmd())

    print('Start postgres in docker.')
    subprocess.check_call(start_postgres_cmd())


TEST_DB_NAME = 'test'
CONTAINER_NAME = 'test-postgres'
POSTGRES_PORT = 5432