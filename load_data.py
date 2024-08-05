import json

class LoadData:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def load_data(self, rooms_path, students_pass):
        with open(rooms_path) as f:
            rooms = json.load(f)
        with open(students_pass) as f:
            students = json.load(f)

        for room in rooms:
            self.db_manager.execute_query("INSERT INTO rooms(id, name) VALUES (%s, %s)", (room['id'], room['name']))

        for student in students:
            self.db_manager.execute_query("""INSERT INTO students(id, name, birthday, id_room, sex) 
                     VALUES (%s, %s, %s, %s, %s)""", (student['id'], student['name'], student['birthday'], student['id_room'], student['sex']))
