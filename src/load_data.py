import json
from typing import List, Tuple
import logging
from db_manager import DBManager

logger = logging.getLogger("load_data")

class LoadData:
    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def load_data_rooms(self, rooms_path: str) -> None:
        try:
            with open(rooms_path) as f:
                rooms: List[dict] = json.load(f)

            data: List[Tuple[int, str]] = [(room["id"], room["name"]) for room in rooms]

            query = "INSERT INTO rooms(id, name) VALUES (%s, %s)"

            self.db_manager.execute_many_query(query, data)
            logger.info("Successfully loaded rooms into the database")
        except FileNotFoundError as err:
            logger.error(f"Error: {err}")
        except Exception as err:
            logger.error(f"Error: {err}")

    def load_data_students(self, students_path: str) -> None:
        try:
            with open(students_path) as f:
                students: List[dict] = json.load(f)

            data: List[Tuple[int, str, str, int, str]] = [
                (
                    student["id"],
                    student["name"],
                    student["birthday"],
                    student["room"],
                    student["sex"],
                )
                for student in students
            ]
            query = (
                """
                INSERT INTO students(id, name, birthday, room, sex)
                VALUES (%s, %s, %s, %s, %s)
                """
            )

            self.db_manager.execute_many_query(query, data)
            logger.info("Successfully loaded students into the database")
        except FileNotFoundError as err:
            logger.error(f"Error: {err}")
        except Exception as err:
            logger.error(f"Error: {err}")