import json
import logging
import xml.etree.ElementTree as ET
from decimal import Decimal
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DataExporter:
    def export_results(self, format: str, data: Dict[str, Any], filename: str) -> None:

        logger.info(f"Export results to {format}")
        if format == "json":
            self.export_json(data, filename)
        elif format == "xml":
            self.export_xml(data, filename)
        else:
            logger.error("Failed to export")

    def export_json(self, data: Dict[str, Any], filename: str) -> None:
        with open(f"{filename}.json", "w") as f:
            json.dump(data, f, default=self._decimal_default, indent=2)

    def export_xml(self, data: Dict[str, Any], filename: str) -> None:
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

    def _decimal_default(self, obj) -> float:
        if isinstance(obj, Decimal):
            return float(obj)
