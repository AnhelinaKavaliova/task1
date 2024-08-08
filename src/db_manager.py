import logging
from typing import Any, List, Tuple

import mysql.connector

logger = logging.getLogger("db_manager")


class DBManager:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        try:
            self.mydb = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            logger.info("Db connected")
        except mysql.connector.Error as err:
            logger.info(f"Failed to connect: {err}")

    def execute_query(self, query: str) -> List[Tuple[Any, ...]]:
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(query)
            result = mycursor.fetchall()
            mycursor.close()
            logger.info(f"Query executed successfully: {query}")
            return result
        except mysql.connector.Error as err:
            logger.info(f"Error: {err}")

    def execute_many_query(self, query: str, data: List[Tuple[Any, ...]]) -> None:
        try:
            mycursor = self.mydb.cursor()
            mycursor.executemany(query, data)
            self.mydb.commit()
            mycursor.close()
            logger.info(f"Query executed successfully: {query}")
        except mysql.connector.Error as err:
            logger.info(f"Error: {err}")

    def fetch_all(self) -> List[Tuple[Any, ...]]:
        try:
            result = self.mycursor.fetchall()
            logger.info("Fetched all records.")
            return result
        except mysql.connector.Error as err:
            logger.error(f"Error f: {err}")

    def commit(self) -> None:
        try:
            self.mydb.commit()
            logger.info("Database commit successful.")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")

    def close(self) -> None:
        try:
            self.mycursor.close()
            self.mydb.close()
            logger.info("Database connection closed.")
        except mysql.connector.Error as err:
            logger.error(f"Err: {err}")
