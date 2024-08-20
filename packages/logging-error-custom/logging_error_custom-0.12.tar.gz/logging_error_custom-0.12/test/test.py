from logging_error_custom import ExceptionLogger  # Import your custom library
from dotenv import load_dotenv

load_dotenv()

def test_logging():
    try:
        # Initialize the ExceptionLogger
        logger = ExceptionLogger()

        # Sample data
        application_name = "TestApp"
        application_type = "Backend"
        exception_category = "SystemException"
        error_message = "Test error message"
        stack_trace = "Traceback (most recent call last): ..."
        exception_object = "SampleObject"
        exception_process = "SampleProcess"
        inner_exception = "SampleInnerException"

        # Log an exception
        logger.log_exception(
            application_name,
            application_type,
            exception_category,
            error_message,
            stack_trace,
            exception_object,
            exception_process,
            inner_exception
        )

        # Verify log entry (Optional step, you might need to manually verify it in the database)
        print("Exception logged successfully.")
        
    except Exception as e:
        print(f"Test failed with exception: {e}")
    finally:
        # Ensure resources are cleaned up
        if 'logger' in locals():
            logger.close()

if __name__ == "__main__":
    test_logging()
