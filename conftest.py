import logging
import os
import glob
import pytest
from datetime import datetime

# Dictionary to store test outcomes
test_results = {"passed": 0, "failed": 0, "skipped": 0}

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

# Hook to execute before each test
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    print(f"\n[Before Test] Starting test: {item.name}")

# Hook to execute after each test
@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    print(f"\n[After Test] Finished test: {item.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    """Hook to execute before each step."""
    # Print step details
    print(f"\n[Before Step] Starting step:")
    print(f" - Keyword: {step.keyword}")
    print(f" - Name: {step.name}")
    print(f" - Line Number: {step.line_number}")
    print(f" - Step Type: {step.type}")
    if step.params:
        print(f" - Parameters: {step.params}")

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """Hook to execute after each step."""
    # Print step details
    print(f"\n[After Step] Finished step:")
    print(f" - Keyword: {step.keyword}")
    print(f" - Name: {step.name}")
    print(f" - Line Number: {step.line_number}")
    print(f" - Step Type: {step.type}")
    if step.params:
        print(f" - Parameters: {step.params}")
    
    # Print result of step
    if step_func_args is not None:
        if step_func_args.get('exception') is None:
            print(f" - Step Status: PASSED")
        else:
            print(f" - Step Status: FAILED")
            print(f" - Error: {step_func_args.get('exception')}")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Check if the pytest-html plugin is active
    if hasattr(config, '_metadata'):
        # Add custom metadata to the HTML report
        config._metadata["Project Name"] = "Dynamic Pytest Report"
        config._metadata["Execution Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config._metadata["Test Environment"] = "Staging"
        config._metadata["Platform"] = "Windows 10"
    else:
        print("pytest-html plugin not found; skipping metadata configuration.")

# Hook to log the result of each test
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    # Check if this is the final call phase of the test
    if result.when == "call":
        if result.passed:
            test_results["passed"] += 1
        elif result.failed:
            test_results["failed"] += 1
        elif result.skipped:
            test_results["skipped"] += 1

# Hook to summarize results after all tests have finished
def pytest_sessionfinish(session, exitstatus):
    total_tests = session.testscollected
    print(f"\nTotal tests: {total_tests}")
    print(f"Passed tests: {test_results['passed']}")
    print(f"Failed tests: {test_results['failed']}")
    print(f"Skipped tests: {test_results['skipped']}")
    print(f"Exit status: {exitstatus}")

# Hook for dynamically adding information after tests complete
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([f"Dynamic Pytest Report Summary at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    postfix.extend([f"Generated by Pytest with dynamic hooks"])

# Optionally customize environment metadata
def pytest_html_report_title(report):
    report.title = "Dynamic Pytest Report"  # Custom title for the HTML report

# To remove any files
# def pytest_sessionfinish(session, exitstatus):
#     try:
#         os.remove('test_log.log')  # Adjust the name if needed
#     except FileNotFoundError:
#         pass  # Log file doesn't exist, ignore