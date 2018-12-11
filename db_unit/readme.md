This package contains experiments in developing unit tests for database code.
In this case we define database unit tests as tests of single functions that
interface with a database that always starts empty. If tests need to run against
a version of a production database then they are integration tests.