from typing import List, Tuple
from db_manager import DBManager


class Queries:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def list_students_in_rooms(self) -> List[Tuple[str, int]]:
        query = """
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r
                 LEFT JOIN students s ON r.id = s.room
                 GROUP BY r.name;
                 """

        return self.db_manager.execute_query(query)

    def smallest_average_age(self) -> List[Tuple[str, float]]:
        query = """
                SELECT r.name AS room_name,
                AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.name
                ORDER BY avg_age
                LIMIT 5;
                """

        return self.db_manager.execute_query(query)

    def biggest_gap_age(self) -> List[Tuple[str, int]]:
        query = """
                SELECT r.name AS room_name,
                MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday,
                CURDATE())) AS age_gap
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.name
                ORDER BY age_gap DESC
                LIMIT 5;
                """

        return self.db_manager.execute_query(query)

    def rooms_different_sex(self) -> List[Tuple[str]]:
        query = """
                SELECT r.name AS room_name
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.name
                HAVING COUNT(DISTINCT s.sex) > 1;
                 """

        return self.db_manager.execute_query(query)
