"""
Unit tests for the retry_with_backoff decorator.

Tests successful attempts, retry logic, exponential backoff, and exception handling.
"""

import pytest
import time
from unittest.mock import Mock, patch, call

from catholic_liturgy_tools.utils.retry import retry_with_backoff


class CustomError(Exception):
    """Custom exception for testing."""
    pass


class AnotherError(Exception):
    """Another custom exception for testing."""
    pass


class TestRetryWithBackoff:
    """Tests for the retry_with_backoff decorator."""
    
    def test_successful_first_attempt(self):
        """Test that successful function on first attempt returns immediately."""
        mock_func = Mock(return_value="success")
        
        @retry_with_backoff(max_attempts=3)
        def test_func():
            return mock_func()
        
        result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 1
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    def test_successful_after_retry(self, mock_sleep):
        """Test that function succeeds after retrying once."""
        mock_func = Mock(side_effect=[CustomError("fail"), "success"])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 2
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    def test_max_attempts_reached(self, mock_sleep):
        """Test that exception is raised after max attempts."""
        mock_func = Mock(side_effect=CustomError("persistent failure"))
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        with pytest.raises(CustomError) as exc_info:
            test_func()
        
        assert str(exc_info.value) == "persistent failure"
        assert mock_func.call_count == 3
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    def test_exponential_backoff_delays(self, mock_sleep):
        """Test that delays follow exponential backoff pattern."""
        mock_func = Mock(side_effect=[CustomError("1"), CustomError("2"), "success"])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=2.0, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        result = test_func()
        
        # Verify exponential backoff: 2^0 = 1s, 2^1 = 2s
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1.0)  # 2^0
        mock_sleep.assert_any_call(2.0)  # 2^1
        assert result == "success"
        assert mock_func.call_count == 3
    
    @patch('time.sleep')
    def test_backoff_calculation(self, mock_sleep):
        """Test that backoff delays are calculated correctly."""
        mock_func = Mock(side_effect=[CustomError("1"), CustomError("2"), CustomError("3")])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=2.0, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        with pytest.raises(CustomError):
            test_func()
        
        # Verify sleep was called with correct delays
        # attempt 1 fails -> sleep(2^0) = 1
        # attempt 2 fails -> sleep(2^1) = 2
        # attempt 3 fails -> no sleep
        assert mock_sleep.call_count == 2
        mock_sleep.assert_has_calls([call(1.0), call(2.0)])
    
    @patch('time.sleep')
    def test_custom_backoff_factor(self, mock_sleep):
        """Test custom backoff factor."""
        mock_func = Mock(side_effect=[CustomError("1"), CustomError("2"), "success"])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=3.0, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        result = test_func()
        
        # Verify sleep was called with custom backoff factor
        # attempt 1 fails -> sleep(3^0) = 1
        # attempt 2 fails -> sleep(3^1) = 3
        assert mock_sleep.call_count == 2
        mock_sleep.assert_has_calls([call(1.0), call(3.0)])
        assert result == "success"
    
    def test_specific_exceptions_only(self):
        """Test that only specified exceptions are retried."""
        mock_func = Mock(side_effect=AnotherError("wrong exception"))
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        # AnotherError should not be caught since we only specified CustomError
        with pytest.raises(AnotherError):
            test_func()
        
        # Should fail immediately without retry
        assert mock_func.call_count == 1
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    def test_multiple_exception_types(self, mock_sleep):
        """Test that multiple exception types can be caught."""
        mock_func = Mock(side_effect=[CustomError("1"), AnotherError("2"), "success"])
        
        @retry_with_backoff(
            max_attempts=3,
            backoff_factor=0.01,
            exceptions=(CustomError, AnotherError)
        )
        def test_func():
            return mock_func()
        
        result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    def test_default_exception_catches_all(self, mock_sleep):
        """Test that default exception tuple catches all exceptions."""
        mock_func = Mock(side_effect=[ValueError("value error"), KeyError("key error"), "success"])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01)
        def test_func():
            return mock_func()
        
        result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    def test_function_with_arguments(self):
        """Test that decorated function preserves arguments."""
        mock_func = Mock(return_value="result")
        
        @retry_with_backoff(max_attempts=3)
        def test_func(x, y, z=None):
            return mock_func(x, y, z)
        
        result = test_func(1, 2, z=3)
        
        assert result == "result"
        mock_func.assert_called_once_with(1, 2, 3)
    
    def test_function_metadata_preserved(self):
        """Test that functools.wraps preserves function metadata."""
        @retry_with_backoff(max_attempts=3)
        def test_func():
            """Test function docstring."""
            return "result"
        
        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "Test function docstring."
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    @patch('catholic_liturgy_tools.utils.retry.logger')
    def test_logging_on_retry(self, mock_logger, mock_sleep):
        """Test that retry attempts are logged."""
        mock_func = Mock(side_effect=[CustomError("fail"), "success"])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        test_func()
        
        # Should log warning on first failure
        assert mock_logger.warning.called
        warning_message = mock_logger.warning.call_args[0][0]
        assert "failed on attempt 1/3" in warning_message.lower()
        assert "retrying" in warning_message.lower()
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    @patch('catholic_liturgy_tools.utils.retry.logger')
    def test_logging_on_success_after_retry(self, mock_logger, mock_sleep):
        """Test that success after retry is logged."""
        mock_func = Mock(side_effect=[CustomError("fail"), "success"])
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        test_func()
        
        # Should log info on success after retry
        assert mock_logger.info.called
        info_message = mock_logger.info.call_args[0][0]
        assert "succeeded on attempt 2/3" in info_message.lower()
    
    @patch('catholic_liturgy_tools.utils.retry.time.sleep')
    @patch('catholic_liturgy_tools.utils.retry.logger')
    def test_logging_on_final_failure(self, mock_logger, mock_sleep):
        """Test that final failure is logged as error."""
        mock_func = Mock(side_effect=CustomError("persistent"))
        
        @retry_with_backoff(max_attempts=3, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        with pytest.raises(CustomError):
            test_func()
        
        # Should log error on final failure
        assert mock_logger.error.called
        error_message = mock_logger.error.call_args[0][0]
        assert "failed after 3 attempts" in error_message.lower()
    
    @patch('catholic_liturgy_tools.utils.retry.logger')
    def test_no_logging_on_first_success(self, mock_logger):
        """Test that successful first attempt doesn't log info."""
        mock_func = Mock(return_value="success")
        
        @retry_with_backoff(max_attempts=3)
        def test_func():
            return mock_func()
        
        test_func()
        
        # Should not log info for first attempt success
        assert not mock_logger.info.called
    
    @patch('logging.getLogger')
    def test_custom_logger_name(self, mock_get_logger):
        """Test that custom logger name is used."""
        custom_logger = Mock()
        mock_get_logger.return_value = custom_logger
        
        @retry_with_backoff(max_attempts=2, backoff_factor=0.01, logger_name="custom.logger")
        def test_func():
            return "success"
        
        test_func()
        
        # Should get logger with custom name
        mock_get_logger.assert_called_with("custom.logger")
    
    def test_single_attempt(self):
        """Test with max_attempts=1 (no retry)."""
        mock_func = Mock(side_effect=CustomError("fail"))
        
        @retry_with_backoff(max_attempts=1, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        with pytest.raises(CustomError):
            test_func()
        
        assert mock_func.call_count == 1
    
    def test_many_attempts(self):
        """Test with many retry attempts."""
        # Fail 4 times, succeed on 5th
        mock_func = Mock(side_effect=[
            CustomError("1"),
            CustomError("2"),
            CustomError("3"),
            CustomError("4"),
            "success"
        ])
        
        @retry_with_backoff(max_attempts=5, backoff_factor=0.01, exceptions=(CustomError,))
        def test_func():
            return mock_func()
        
        result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 5
