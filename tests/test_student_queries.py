import pytest
from src.student_queries import Queries
from unittest.mock import MagicMock

def test_list_students_in_rooms():
    db_manager_mock = MagicMock()
    db_manager_mock.execute_query.return_value = [("Room #1", 2), ("Room #5", 10)]

    query = Queries(db_manager_mock)
    result = query.list_students_in_rooms()

    excepted_result = [("Room #1", 2), ("Room #5", 10)]

    assert result == excepted_result

    db_manager_mock.execute_query.assert_called_once_with("""
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r
                 LEFT JOIN students s ON r.id = s.room
                 GROUP BY r.name;
                 """)

def test_smallest_average_age():
    db_manager_mock = MagicMock()
    db_manager_mock.execute_query.return_value = [("Room #1", 3.5), ("Room #5", 11.2)]

    query = Queries(db_manager_mock)
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
    
def test_biggest_gap_age():
    db_manager_mock = MagicMock()
    db_manager_mock.execute_query.return_value = [("Room #1", 2), ("Room #5", 10)]

    query = Queries(db_manager_mock)
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
    
def test_rooms_different_sex():
    db_manager_mock = MagicMock()
    db_manager_mock.execute_query.return_value = [("Room #1"), ("Room #5")]

    query = Queries(db_manager_mock)
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
    
