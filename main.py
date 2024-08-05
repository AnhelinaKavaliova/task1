from db_manager import DBManager
from load_data import LoadData
from queries import Queries
import argparse

def main():
    parser = argparse.ArgumentParser(description="Task1 Database Managment")
    parser.add_argument('students', help = "Path to the students file")
    parser.add_argument("rooms", help = "Path to the rooms file")
    parser.add_argument("--format", choices=['json', 'xml'], help = "Output", default="json")
    parser.add_argument("--output_name", help = "Output file name", default="Output")
    args = parser.parse_args()

    db_manager = DBManager(host='127.0.0.1', user='root', password='mkmkuop', database='task1')
    data_loader = LoadData(db_manager)
    query_executor = Queries(db_manager)

    #data_loader.load_data(args.students, args.rooms)

    results = {}

    rooms = query_executor.list_students_in_rooms()
    results["students_in_rooms"] = [{"room_name": room[0], "students_count": room[1]} for room in rooms]
    for room in rooms:
        print(room)

    query_executor.export_results(args.format, results, args.output_name)

    db_manager.close()

if __name__ == "__main__":
    main()


