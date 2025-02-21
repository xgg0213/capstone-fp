import pytest
import sys

if __name__ == "__main__":
    # Run the tests
    result = pytest.main(["-v", "test_websocket.py"])
    
    # Exit with the test result
    sys.exit(result) 