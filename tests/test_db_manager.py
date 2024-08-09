import pytest
from unittest.mock import Mock, patch
from src.db_manager import DBManager
import mysql.connector

@pytest.fixture
def db_manager_mock():
    with patch('src.db_manager.mysql.connector.connect') as connect_mock:
        db_mock = Mock()
        connect_mock.return_value = db_mock
        yield DBManager("host", "user", "password", "database")

    connect_mock.stop()

@pytest.fixture
def mock_logger():
    with patch('src.db_manager.logger') as mock_logger:
        yield mock_logger

def test_db_connection_success(db_manager_mock, mock_logger):
        db_manager = DBManager("host", "user", "password", "database")
        mock_logger.info.assert_called_with("Db connected")
        assert db_manager.mydb == db_manager_mock.mydb

def test_db_connection_failed(mock_logger):
    with patch('src.db_manager.mysql.connector.connect', side_effect=mysql.connector.Error("Connection error")) as connect_mock:
        db_manager = DBManager("host", "user", "password", "database")
        mock_logger.error.assert_called_with("Failed to connect: Connection error")


def test_execute_quary_success(db_manager_mock, mock_logger):
    cursor_mock = Mock()
    cursor_mock.execute = Mock()
    cursor_mock.fetchall.return_value = [("Room #3"), 10]
    
    db_manager_mock.mydb.cursor.return_value = cursor_mock

    result = db_manager_mock.execute_query("Select * from rooms")

    assert result == [("Room #3"), 10]

    mock_logger.info.assert_called_with("Query executed successfully: Select * from rooms")

def test_execute_quary_failed(db_manager_mock, mock_logger):
    db_manager_mock.mydb.cursor.side_effect = mysql.connector.Error("Execute quary failed")

    result = db_manager_mock.execute_query("Select * from rooms")

    assert result == None

    mock_logger.error.assert_called_with("Error: Execute quary failed")


def test_execute_many_query_success(db_manager_mock, mock_logger):
    cursor_mock = Mock()
    cursor_mock.executemany = Mock()

    db_manager_mock.mydb.cursor.return_value = cursor_mock

    db_manager_mock.execute_many_query("INSERT INTO rooms(id, name) VALUES (%s, %s)", [(5, "Room #1"), (6, "Room #2")])

    mock_logger.info.assert_called_with("Many queries executed successfully: INSERT INTO rooms(id, name) VALUES (%s, %s)")
    
def test_execute_many_query_failed(db_manager_mock, mock_logger):

    db_manager_mock.mydb.cursor.side_effect = mysql.connector.Error("Execute quaries failed")

    db_manager_mock.execute_many_query("INSERT INTO rooms(id, name) VALUES (%s, %s)", [(5, "Room #1"), (6, "Room #2")])

    mock_logger.error.assert_called_with("Error: Execute quaries failed")


def test_fetch_all_success(db_manager_mock, mock_logger):
    cursor_mock = Mock()
    cursor_mock.fetchall.return_value = [("Room #1", 2)]

    result = db_manager_mock.fetch_all(cursor_mock)

    assert result == [("Room #1", 2)]
    mock_logger.debug.assert_called_with("Fetched all records")

def test_fetch_all_error(db_manager_mock, mock_logger):
    cursor_mock = Mock()
    cursor_mock.fetchall.side_effect = mysql.connector.Error("Fetch error")

    result = db_manager_mock.fetch_all(cursor_mock)

    assert result is None
    mock_logger.error.assert_called_with("Error: Fetch error")


def test_commit_success(db_manager_mock, mock_logger):
    db_manager_mock.commit()
    mock_logger.info.assert_called_with("Database commit successful")

def test_commit_error(db_manager_mock, mock_logger):
    db_manager_mock.mydb.commit.side_effect = mysql.connector.Error("Commit error")
    db_manager_mock.commit()

    mock_logger.error.assert_called_with("Error: Commit error")


def test_close_success(db_manager_mock, mock_logger):
    cursor_mock = Mock()
    db_manager_mock.close(cursor_mock)
    mock_logger.info.assert_called_with("Database connection closed")

def test_close_error(db_manager_mock, mock_logger):
    cursor_mock = Mock()
    db_manager_mock.mydb.close.side_effect = mysql.connector.Error("Close error")
    db_manager_mock.close(cursor_mock)
    mock_logger.error.assert_called_with("Err: Close error")
