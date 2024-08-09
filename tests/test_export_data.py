import pytest
from src.export_data import DataExporter
from unittest.mock import *
from decimal import Decimal

@pytest.fixture
def mock_logger():
    with patch("src.export_data.logger") as mock_logger:
        yield mock_logger

@pytest.fixture
def data_exporter():
    yield DataExporter()

def test_export_results_invalid_format(data_exporter, mock_logger):
    format = "txt"
    data = {"key": "value"}
    filename = "file"

    data_exporter.export_results(format, data, filename)
    mock_logger.error.asserd_called_with("Failed to export")

def test_export_json_success(data_exporter, mock_logger):
    data = {"key": "value"}
    filename = "file"

    with patch('builtins.open', mock_open()) as file_mock:
        data_exporter.export_results("json", data, filename)

        file_mock.assert_called_once_with(f"{filename}.json", "w")
        file_mock().write.assert_called() 

        mock_logger.info.assert_called_with("Successfully exported data")

def test_export_json_file_not_found(data_exporter, mock_logger):
    data = {"key": "value"}
    filename = "file"

    with patch('json.dump', side_effect=FileNotFoundError("File not found")):
        data_exporter.export_json(data, filename)
    
    mock_logger.error.assert_called_with("Error: File not found")

def test_export_json_failed(data_exporter, mock_logger):
    data = {"key": "value"}
    filename = "file"

    with patch('json.dump', side_effect=Exception("Test exception")):
        data_exporter.export_json(data, filename)

    mock_logger.error.assert_called_with("Error: Test exception")

def test_export_xml_success(data_exporter, mock_logger):
    data = {"key": [{"subkey": "value"}]} 
    filename = "file"

    with patch('src.export_data.ET.ElementTree') as MockElementTree:
        mock_tree = Mock()
        MockElementTree.return_value = mock_tree

        data_exporter.export_results("xml", data, filename)
        mock_tree.write.assert_called_once_with(f"{filename}.xml", encoding="utf-8", xml_declaration=True)

        mock_logger.info.assert_called_with("Successfully exported data")

def test_export_xml_file_not_found(data_exporter, mock_logger):
    data = {"key": [{"subkey": "value"}]} 
    filename = "file"

    with patch('src.export_data.ET.ElementTree') as MockElementTree:
        MockElementTree.side_effect = FileNotFoundError("File not found")
        
        data_exporter.export_results("xml", data, filename)
        
        mock_logger.error.assert_called_once_with("Error: File not found")


def test_export_xml_general_exception(data_exporter, mock_logger):
    data = {"key": [{"subkey": "value"}]} 
    filename = "file"

    with patch('src.export_data.ET.ElementTree') as MockElementTree:
        MockElementTree.side_effect = Exception("Test exception")
        
        data_exporter.export_results("xml", data, filename)
        
        mock_logger.error.assert_called_once_with("Error: Test exception")

def test_decimal_default(data_exporter):
    decimal_value = Decimal("10.5")
    result = data_exporter._decimal_default(decimal_value)
    assert result == 10.5

def test_decimal_default_error(data_exporter, mock_logger):
    data_exporter._decimal_default("non-decimal")
    mock_logger.error.assert_called_once_with("Object is not serializable")


