import json
#import

class Queries:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def list_students_in_rooms(self):
        query = """
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r 
                 LEFT JOIN students s ON r.id = s.id_room
                 GROUP BY r.id, r.name;
                 """

        return self.db_manager.execute_query(query)
    
    def smallest_average_age(self):
        query = """
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r 
                 LEFT JOIN students s ON r.id = s.id_room
                 GROUP BY r.id, r.name;
                 """
        
        return self.db_manager.execute_query(query)
    
    def biggest_gap_age(self):
        query = """
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r 
                 LEFT JOIN students s ON r.id = s.id_room
                 GROUP BY r.id, r.name;
                 """
        
        return self.db_manager.execute_query(query)
    
    def rooms_different_sex(self):
        query = """
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r 
                 LEFT JOIN students s ON r.id = s.id_room
                 GROUP BY r.id, r.name;
                 """
        
        return self.db_manager.execute_query(query)

    def export_results(self, format, data, filename):
        if format == 'json':
            self.export_json(data, filename)

    def export_json(self, data, filename):
        with open(f"{filename}.json", 'w') as f:
            json.dump(data, f, indent = 2)

    def export_xml(self, data, filename):
        return