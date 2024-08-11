import argparse
import logging
import os
from typing import Dict, List, Tuple, Union

from dotenv import load_dotenv

from db_manager import DBManager
from export_data import DataExporter
from load_data import LoadData
from student_queries import Queries

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main function for the Task1 Database Management program.
    This function performs the following steps:
    1. Sets up logging to a file named "py_log.log" 
    2. Parses command-line arguments for input files and output format
    3. Loads environment variables from a .env file
    4. Establishes a connection to the database
    5. Loads data from the specified input files into the db
    6. Executes queries 
    7. Exports the results of the queries to the specified format 
    8. Closes the database connection 
    """

    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logger.info("Program started")

    parser = argparse.ArgumentParser(description="Task1 Database Managment")
    parser.add_argument("students", help="Path to the students file")
    parser.add_argument("rooms", help="Path to the rooms file")
    parser.add_argument(
        "--format", choices=["json", "xml"], help="Output", default="json"
    )
    parser.add_argument("--output_name", help="Output file name", default="Output")
    args = parser.parse_args()

    try:
        load_dotenv(dotenv_path="../.env")
        logger.info("Configuration loaded successfully")
    except Exception as err:
        logger.error(f"Error: {err}")
        return

    db_config: Dict[str, str] = {
        "host": os.getenv("HOST"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE"),
    }


    try:
        db_manager = DBManager(**db_config)
        logger.info("Db connected")
    except Exception as err:
        logger.error(f"Failed to connect: {err}")
        return
    data_loader = LoadData(db_manager)
    query_executor = Queries(db_manager)
    data_exporter = DataExporter()

    db_manager.execute_query("DELETE FROM students")  # clearing tables for testing
    db_manager.execute_query("DELETE FROM rooms")

    try:
        logger.info("Loading data from rooms file")
        data_loader.load_data_rooms(args.rooms)
        logger.info("Loading data from students file")
        data_loader.load_data_students(args.students)
    except Exception as err:
        logger.error(f"Failed to load data: {err}")
        return

    try:
        logger.info("Execute queries")
        results: Dict[str, List[Dict[str, Union[str, int, float]]]] = {}

        rooms: List[Tuple[int, str]] = query_executor.list_students_in_rooms()
        results["students_in_rooms"] = [
            {"room_name": room[0], "students_count": room[1]} for room in rooms
        ]

        smallest_age_rooms: List[Tuple[str, float]] = (
            query_executor.smallest_average_age()
        )
        results["smallest_age_rooms"] = [
            {"room_name": room[0], "avg_age": room[1]} for room in smallest_age_rooms
        ]

        biggest_age_gap_rooms: List[Tuple[str, int]] = query_executor.biggest_gap_age()
        results["biggest_age_gap_rooms"] = [
            {"room_name": room[0], "age_gap": room[1]} for room in biggest_age_gap_rooms
        ]

        different_sex_rooms: List[Tuple[str]] = query_executor.rooms_different_sex()
        results["different_sex_rooms"] = [
            {"room_name": room[0]} for room in different_sex_rooms
        ]
    except Exception as err:
        logger.error(f"Failed to execute: {err}")
        return

    try:
        logger.info(f"Export results to {args.format}")
        data_exporter.export_results(args.format, results, args.output_name)
    except Exception as err:
        logger.error(f"Failed to export: {err}")
        return

    db_manager.close_db_connection()
    logger.info("Connection closed")
    logger.info("Program completed")


if __name__ == "__main__":
    main()
