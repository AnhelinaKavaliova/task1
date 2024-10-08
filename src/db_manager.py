import logging
from typing import Any, List, Tuple

import mysql.connector

logger = logging.getLogger("db_manager")


class DBManager:
    """
    Manages the connection to a MySQL database and provides methods for executing queries
    """

    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        try:
            self.mydb = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            logger.info("Db connected")
        except mysql.connector.Error as err:
            logger.error(f"Failed to connect: {err}")
            raise

    def execute_query(self, query: str) -> List[Tuple[Any, ...]]:
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(query)
            result = self.fetch_all(mycursor)
            self.close_cursor(mycursor)
            logger.info(f"Query executed successfully: {query}")
            return result
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            raise

    def execute_many_query(self, query: str, data: List[Tuple[Any, ...]]) -> None:
        try:
            mycursor = self.mydb.cursor()
            mycursor.executemany(query, data)
            self.mydb.commit()
            self.close_cursor(mycursor)
            logger.info(f"Many queries executed successfully: {query}")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            raise

    def fetch_all(self, cursor) -> List[Tuple[Any, ...]]:
        try:
            result = cursor.fetchall()
            logger.debug("Fetched all records")
            return result
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            return None

    def commit(self) -> None:
        try:
            self.mydb.commit()
            logger.info("Database commit successful")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            raise

    def close_cursor(self, cursor) -> None:
        try:
            cursor.close()
            logger.info("Cursor connection closed")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            raise

    def close_db_connection(self) -> None:
        try:
            self.mydb.close()
            logger.info("Database connection closed")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            raise
