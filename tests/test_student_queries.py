from src.student_queries import Queries
from unittest.mock import Mock, patch
import pytest
import logging

@pytest.fixture
def db_manager_mock():
    yield Mock()

@pytest.fixture
def query(db_manager_mock):
    yield Queries(db_manager_mock)

def test_list_students_in_rooms(query, db_manager_mock):
    db_manager_mock.execute_query.return_value = [("Room #1", 2), ("Room #5", 10)]

    result = query.list_students_in_rooms()

    excepted_result = [("Room #1", 2), ("Room #5", 10)]

    assert result == excepted_result

    db_manager_mock.execute_query.assert_called_once_with("""
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r
                 LEFT JOIN students s ON r.id = s.room
                 GROUP BY r.name;
                 """)

def test_smallest_average_age(query, db_manager_mock):
    db_manager_mock.execute_query.return_value = [("Room #1", 3.5), ("Room #5", 11.2)]

    result = query.smallest_average_age()

    excepted_result = [("Room #1", 3.5), ("Room #5", 11.2)]

    assert result == excepted_result

    db_manager_mock.execute_query.assert_called_once_with("""
                SELECT r.name AS room_name,
                AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.name
                ORDER BY avg_age
                LIMIT 5;
                """)
    
def test_biggest_gap_age(query, db_manager_mock):
    db_manager_mock.execute_query.return_value = [("Room #1", 2), ("Room #5", 10)]

    result = query.biggest_gap_age()

    excepted_result = [("Room #1", 2), ("Room #5", 10)]

    assert result == excepted_result

    db_manager_mock.execute_query.assert_called_once_with("""
                SELECT r.name AS room_name,
                MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday,
                CURDATE())) AS age_gap
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.name
                ORDER BY age_gap DESC
                LIMIT 5;
                """)
    
def test_rooms_different_sex(query, db_manager_mock):
    db_manager_mock.execute_query.return_value = [("Room #1"), ("Room #5")]

    result = query.rooms_different_sex()

    excepted_result = [("Room #1"), ("Room #5")]

    assert result == excepted_result

    db_manager_mock.execute_query.assert_called_once_with("""
                SELECT r.name AS room_name
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.name
                HAVING COUNT(DISTINCT s.sex) > 1;
                 """)

def test_execute_query_successfully(query, db_manager_mock):
    with patch('src.student_queries.logger') as mock_logger:
        db_manager_mock.execute_query.return_value = [("Room #1", 2)]

        result = query.list_students_in_rooms()

        assert result == [("Room #1", 2)]
        mock_logger.info.assert_called_with("Query executed successfully")

def test_execute_query_failed(query, db_manager_mock):
    with patch('src.student_queries.logger') as mock_logger:
        db_manager_mock.execute_query.side_effect = Exception("Test exeption")

        result = query.list_students_in_rooms()

        assert result == None
        mock_logger.error.assert_called_with("Error: Test exeption")