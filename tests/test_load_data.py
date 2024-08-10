import json
from unittest.mock import Mock, mock_open, patch

import pytest

from src.db_manager import DBManager
from src.load_data import LoadData


@pytest.fixture
def db_manager_mock():
    yield Mock(DBManager)


@pytest.fixture
def load_data(db_manager_mock):
    yield LoadData(db_manager_mock)


@pytest.fixture
def mock_logger():
    with patch("src.load_data.logger") as mock_logger:
        yield mock_logger


def test_load_data_rooms_success(db_manager_mock, load_data, mock_logger):
    data = mock_open(
        read_data=json.dumps(
            [{"id": 1, "name": "Room #1"}, {"id": 2, "name": "Room #2"}]
        )
    )
    with patch("builtins.open", data):
        load_data.load_data_rooms("path.json")

    expected_query = "INSERT INTO rooms(id, name) VALUES (%s, %s)"
    expected_data = [(1, "Room #1"), (2, "Room #2")]
    db_manager_mock.execute_many_query.assert_called_once_with(
        expected_query, expected_data
    )

    mock_logger.info.assert_called_with("Successfully loaded rooms into the database")


def test_load_data_rooms_file_not_found(db_manager_mock, load_data, mock_logger):
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        with pytest.raises(FileNotFoundError):
            load_data.load_data_rooms("path.json")
    mock_logger.error.assert_called_with("Error: File not found")


def test_load_data_rooms_failed(db_manager_mock, load_data, mock_logger):
    with patch("builtins.open", side_effect=Exception("Test exception")):
        with pytest.raises(Exception):
            load_data.load_data_rooms("path.json")
    mock_logger.error.assert_called_with("Error: Test exception")


def test_load_data_students_success(db_manager_mock, load_data, mock_logger):
    data = mock_open(
        read_data=json.dumps(
            [
                {
                    "id": 1,
                    "name": "Luke",
                    "birthday": "2001-09-13",
                    "room": 101,
                    "sex": "M",
                },
                {
                    "id": 2,
                    "name": "Xto",
                    "birthday": "1999-05-15",
                    "room": 102,
                    "sex": "F",
                },
            ]
        )
    )

    with patch("builtins.open", data):
        load_data.load_data_students("path.json")

    expected_query = """
                INSERT INTO students(id, name, birthday, room, sex)
                VALUES (%s, %s, %s, %s, %s)
                """

    expected_data = [
        (1, "Luke", "2001-09-13", 101, "M"),
        (2, "Xto", "1999-05-15", 102, "F"),
    ]
    db_manager_mock.execute_many_query.assert_called_once_with(
        expected_query, expected_data
    )

    mock_logger.info.assert_called_with(
        "Successfully loaded students into the database"
    )


def test_load_data_students_file_not_found(db_manager_mock, load_data, mock_logger):
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        with pytest.raises(FileNotFoundError):
            load_data.load_data_students("path.json")
    mock_logger.error.assert_called_with("Error: File not found")


def test_load_data_students_failed(db_manager_mock, load_data, mock_logger):
    with patch("builtins.open", side_effect=Exception("Test exception")):
        with pytest.raises(Exception):
            load_data.load_data_students("path.json")
    mock_logger.error.assert_called_with("Error: Test exception")
