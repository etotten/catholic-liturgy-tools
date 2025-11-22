"""Unit tests for GitHub Actions trigger module."""

import pytest
import os
from unittest.mock import Mock, patch
from catholic_liturgy_tools.github.actions import trigger_workflow


class TestTriggerWorkflow:
    """Tests for trigger_workflow function."""
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_success(self, mock_post):
        """Test successful workflow trigger."""
        # Mock successful response (204 No Content)
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        result = trigger_workflow()
        
        assert result is True
        mock_post.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    def test_trigger_workflow_missing_token(self):
        """Test that missing GITHUB_TOKEN raises ValueError."""
        with pytest.raises(ValueError, match="GITHUB_TOKEN environment variable not set"):
            trigger_workflow()
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'invalid_token'})
    def test_trigger_workflow_auth_error(self, mock_post):
        """Test handling of authentication errors (401/403)."""
        # Mock 401 Unauthorized response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response
        
        result = trigger_workflow()
        
        assert result is False
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_not_found(self, mock_post):
        """Test handling of workflow not found error (404)."""
        # Mock 404 Not Found response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post.return_value = mock_response
        
        result = trigger_workflow()
        
        assert result is False
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_with_custom_params(self, mock_post):
        """Test trigger with custom workflow file and branch."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        result = trigger_workflow(workflow_file="custom-workflow.yml", branch="develop")
        
        assert result is True
        # Verify the URL includes the custom workflow file
        call_args = mock_post.call_args
        assert "custom-workflow.yml" in call_args[0][0]
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_uses_correct_api_endpoint(self, mock_post):
        """Test that correct GitHub API endpoint is used."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        trigger_workflow()
        
        # Verify API URL format
        call_args = mock_post.call_args
        url = call_args[0][0]
        assert "api.github.com" in url
        assert "/repos/" in url
        assert "/actions/workflows/" in url
        assert "/dispatches" in url
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_sends_correct_headers(self, mock_post):
        """Test that correct authorization headers are sent."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        trigger_workflow()
        
        # Verify headers
        call_kwargs = mock_post.call_args[1]
        headers = call_kwargs.get('headers', {})
        assert 'Authorization' in headers
        assert headers['Authorization'] == 'Bearer test_token'
        assert headers['Accept'] == 'application/vnd.github+json'
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_sends_correct_payload(self, mock_post):
        """Test that correct JSON payload is sent."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        trigger_workflow(branch="main")
        
        # Verify payload
        call_kwargs = mock_post.call_args[1]
        json_data = call_kwargs.get('json', {})
        assert 'ref' in json_data
        assert json_data['ref'] == 'main'
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_handles_request_exception(self, mock_post):
        """Test handling of network/request exceptions."""
        import requests
        mock_post.side_effect = requests.RequestException("Network error")
        
        result = trigger_workflow()
        
        assert result is False
    
    @patch('catholic_liturgy_tools.github.actions.requests.post')
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'})
    def test_trigger_workflow_handles_unexpected_status_code(self, mock_post):
        """Test handling of unexpected HTTP status codes."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        result = trigger_workflow()
        
        assert result is False
