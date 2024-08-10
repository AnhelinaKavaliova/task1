import sys
from unittest.mock import patch, Mock
from src.main import main

@patch('src.main.DBManager')
@patch('src.main.LoadData')
@patch('src.main.Queries')
@patch('src.main.DataExporter')
@patch('src.main.logger')
def test_main_logging_success(mock_logger, mock_data_exporter, mock_queries, mock_load_data, mock_db_manager):
    test_args = ["src/main.py", "data/students.json", "data/rooms.json", "--format", "xml", "--output_name", "output_file"]

    with patch.object(sys, 'argv', test_args):
        mock_queries.return_value.list_students_in_rooms = Mock(return_value=[(1, "Room A", 30)])
        mock_queries.return_value.smallest_average_age = Mock(return_value=[("Room A", 20.5)])
        mock_queries.return_value.biggest_gap_age = Mock(return_value=[("Room B", 15)])
        mock_queries.return_value.rooms_different_sex = Mock(return_value=[("Room C",)])

        main()

        mock_logger.info.assert_any_call("Program started")
        mock_logger.info.assert_any_call("Configuration loaded successfully")
        mock_logger.info.assert_any_call("Db connected")
        mock_logger.info.assert_any_call("Loading data from rooms file")
        mock_logger.info.assert_any_call("Loading data from students file")
        mock_logger.info.assert_any_call("Execute queries")
        mock_logger.info.assert_any_call("Export results to xml")
        mock_logger.info.assert_any_call("Connection closed")
        mock_logger.info.assert_any_call("Program completed")

        mock_logger.error.assert_not_called()



