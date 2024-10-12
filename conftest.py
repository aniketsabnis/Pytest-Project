import logging
import os
import glob
import pytest
from datetime import datetime

class LoggerInstance():
    _logger_instance = None

def get_logger():

    if LoggerInstance._logger_instance is None:
        # Create a logger
        logger = logging.getLogger('pytest_logger')
        # logger.setLevel(logging.INFO)

        # Remove any existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Define the log directory and ensure it exists
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # Create a log file with a timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file_path = os.path.join(log_dir, f'pytest_{timestamp}.log')
        
        # Create a file handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)

        # Create console handler and set level to debug
        # stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        # stream_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Manage log file copies, keep the latest 5 logs
        manage_log_files(log_dir)
    
        LoggerInstance._logger_instance = logger

    return LoggerInstance._logger_instance

def manage_log_files(log_dir):
    # Get a list of all log files in the directory, sorted by creation time
    log_files = sorted(glob.glob(os.path.join(log_dir, 'pytest_*.log')), key=os.path.getmtime)

    # Check if there are more than 5 log files
    if len(log_files) > 5:
        # Remove the oldest log file
        os.remove(log_files[0])  # The oldest file is at index 0

@pytest.fixture(scope='session')
def logger():
    """Fixture that provides a singleton logger instance."""
    return get_logger()

# def pytest_sessionfinish(session, exitstatus):
#     try:
#         os.remove('test_log.log')  # Adjust the name if needed
#     except FileNotFoundError:
#         pass  # Log file doesn't exist, ignore