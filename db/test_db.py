"""
This is an experiment for writing tests against an empty postgres database
that is instantiated with docker. This test has docker as an implicit external
dependency and will pull postgres in as a part of its setup. It will destroy
all data created as part of the testing process.
"""
