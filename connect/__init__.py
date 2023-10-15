from cs50 import SQL

import check50
import re
import sqlparse


@check50.check()
def exists():
    """schema.sql exists"""
    check50.exists("schema.sql")


@check50.check(exists)
def test_execution():
    """schema.sql runs without error"""
    db = create_database("connect.db")
    run_statements(db, "schema.sql")


@check50.check(test_execution)
def test_create_tables():
    """schema.sql contains at least 1 CREATE TABLE statement"""
    test_contents("CREATE TABLE", "schema.sql")


@check50.check(test_execution)
def test_primary_keys():
    """schema.sql contains at least 1 PRIMARY KEY constraint"""
    test_contents("PRIMARY KEY", "schema.sql")


@check50.check(test_execution)
def test_foreign_keys():
    """schema.sql contains at least 1 FOREIGN KEY constraint"""
    test_contents("FOREIGN KEY", "schema.sql")


def create_database(filename: str) -> SQL:
    """
    Creates a database with the specified filename and returns a connection to it.

    positional arguments:
        filename (str)      name of database to create

    returns:
        SQL object from the cs50 library
    """
    open(filename, "w").close()
    return SQL(f"sqlite:///{filename}")


def run_statements(db: SQL, filename: str) -> None:
    """
    Runs the SQL queries contained in 'filename' and checks for errors

    positional arguments:
        filename (str)      file containing SQL query

    returns:
        None
    """

    with open(filename) as f:

        # Read contents and strip comments
        contents = sqlparse.format(f.read().strip(), strip_comments=True)

        # Parse contents into list of SQL statements
        statements = sqlparse.split(contents)
        if not statements:
            raise check50.Failure(
                f"Could not find SQL statements in {filename}"
            )
        
        # Execute each statement starting from top of file
        try:
            for statement in statements:
                db.execute(statement.strip())
        except Exception as e:
            raise check50.Failure(f"Error when executing statements: {str(e)}")


def test_contents(pattern: str, filename: str, quantity: int = 1) -> None:
    """
    Tests if the given pattern is in the filename quantity number of times

    positional arguments:
        pattern (str)       regex pattern to check for
        filename (str)      the file in which to look for the pattern
        quantity (int)      the number of times the pattern should appear
    
    raises:
        check50.Failure if the pattern is not found quantity number of times
    """
    with open(filename, "r") as f:
        contents = f.read()

    if not len(re.findall(pattern, contents, re.IGNORECASE)) >= quantity:
        if quantity == 1:
            message = f"Expected to find at least {quantity} {pattern} statement"
        else:
            message = f"Expected to find at least {quantity} {pattern} statements"
        raise check50.Failure(message)
