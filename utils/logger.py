import logging
import os
import glob
from datetime import datetime

def setup_logger():
    # Create a logger
    logger = logging.getLogger('pytest_logger')
    logger.setLevel(logging.INFO)

    # Define the log directory and ensure it exists
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create a log file with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = os.path.join(log_dir, f'pytest_{timestamp}.log')
    
    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Manage log file copies, keep the latest 5 logs
    manage_log_files(log_dir)

    return logger

def manage_log_files(log_dir):
    # Get a list of all log files in the directory, sorted by creation time
    log_files = sorted(glob.glob(os.path.join(log_dir, 'pytest_*.log')), key=os.path.getmtime)

    # Check if there are more than 5 log files
    if len(log_files) > 5:
        # Remove the oldest log file
        os.remove(log_files[0])  # The oldest file is at index 0

# Initialize the logger when this module is imported
logger = setup_logger()
