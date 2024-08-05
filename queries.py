import json
import xml.etree.ElementTree as ET
from decimal import Decimal


class Queries:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def list_students_in_rooms(self):
        query = """
                 SELECT r.name AS room_name, COUNT(s.id) AS student_count
                 FROM rooms r 
                 LEFT JOIN students s ON r.id = s.room
                 GROUP BY r.id, r.name;
                 """

        return self.db_manager.execute_query(query)
    
    def smallest_average_age(self):
        query = """
                SELECT r.name AS room_name, AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
                FROM rooms r 
                JOIN students s ON r.id = s.room
                GROUP BY r.id, r.name
                ORDER BY avg_age
                LIMIT 5;
                """
        
        return self.db_manager.execute_query(query)
    
    def biggest_gap_age(self):
        query = """
                SELECT r.name AS room_name, MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS age_gap
                FROM rooms r 
                JOIN students s ON r.id = s.room
                GROUP BY r.id, r.name
                ORDER BY age_gap DESC
                LIMIT 5;
                """
        
        return self.db_manager.execute_query(query)
    
    def rooms_different_sex(self):
        query = """
                SELECT r.name AS room_name
                FROM rooms r
                JOIN students s ON r.id = s.room
                GROUP BY r.id, r.name
                HAVING COUNT(DISTINCT s.sex) > 1;
                 """
        
        return self.db_manager.execute_query(query)

    def export_results(self, format, data, filename):
        if format == 'json':
            self.export_json(data, filename)
        elif format == 'xml':
            self.export_xml(data, filename)

    def export_json(self, data, filename):
        with open(f"{filename}.json", 'w') as f:
            json.dump(data, f, default= self._decimal_default, indent = 2)

    def export_xml(self, data, filename):
        root = ET.Element("results")
        
        for query, items in data.items():
            query_element = ET.SubElement(root, query)
            for item in items:
                item_element = ET.SubElement(query_element, "item")
                for key, value in item.items():
                    sub_element = ET.SubElement(item_element, key)
                    sub_element.text = str(value)
        
        tree = ET.ElementTree(root)
        tree.write(f"{filename}.xml", encoding="utf-8", xml_declaration=True)
    
    def _decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
 