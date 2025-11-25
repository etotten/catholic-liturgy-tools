"""Unit tests for the CLI module.

Tests the CLI command functions directly without subprocess execution.
"""
import os
from unittest.mock import patch, Mock
from pathlib import Path
from catholic_liturgy_tools import cli


class TestGenerateMessageCommand:
    """Test suite for generate_message_command function."""
    
    @patch('catholic_liturgy_tools.generator.message.generate_message')
    def test_generate_message_command_calls_generator(self, mock_generate):
        """Test that command calls the generate_message function."""
        mock_args = Mock(output_dir='_site/messages', date=None)
        mock_generate.return_value = Path('_site/messages/2025-01-15-daily-message.md')
        
        result = cli.generate_message_command(mock_args)
        
        mock_generate.assert_called_once_with(output_dir='_site/messages', date=None)
        assert result == 0
    
    @patch('catholic_liturgy_tools.generator.message.generate_message')
    def test_generate_message_command_with_custom_output_dir(self, mock_generate):
        """Test command with custom output directory."""
        mock_args = Mock(output_dir='custom/dir', date=None)
        mock_generate.return_value = Path('custom/dir/2025-01-15-daily-message.md')
        
        result = cli.generate_message_command(mock_args)
        
        mock_generate.assert_called_once_with(output_dir='custom/dir', date=None)
        assert result == 0
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.generator.message.generate_message')
    def test_generate_message_command_prints_success_message(self, mock_generate, mock_print):
        """Test that command prints success message."""
        mock_args = Mock(output_dir='_site/messages', date=None)
        output_path = Path('_site/messages/2025-01-15-daily-message.md')
        mock_generate.return_value = output_path
        
        cli.generate_message_command(mock_args)
        
        # Verify print was called with success messages
        assert mock_print.call_count == 2
        first_call = str(mock_print.call_args_list[0][0][0])
        assert 'Generated daily message' in first_call
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.generator.message.generate_message')
    def test_generate_message_command_handles_exception(self, mock_generate, mock_print):
        """Test command handles exceptions and returns error code."""
        mock_args = Mock(output_dir='_site/messages')
        mock_generate.side_effect = Exception("Test error")
        
        result = cli.generate_message_command(mock_args)
        
        assert result == 1
        # Verify error was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args[0][0])
        assert 'Error' in call_args
        assert 'Test error' in call_args


class TestGenerateIndexCommand:
    """Test suite for generate_index_command function."""
    
    @patch('catholic_liturgy_tools.generator.index.scan_readings_files')
    @patch('catholic_liturgy_tools.generator.index.scan_message_files')
    @patch('catholic_liturgy_tools.generator.index.generate_index')
    def test_generate_index_command_calls_generator(self, mock_generate, mock_scan_messages, mock_scan_readings):
        """Test that command calls the generate_index function."""
        mock_args = Mock(posts_dir='_site/messages', output_file='_site/index.html', readings_dir='_site/readings')
        mock_generate.return_value = Path('_site/index.html')
        mock_scan_messages.return_value = [Path('_site/messages/2025-11-22-daily-message.md')]
        mock_scan_readings.return_value = []
        
        result = cli.generate_index_command(mock_args)
        
        mock_generate.assert_called_once_with(posts_dir='_site/messages', output_file='_site/index.html', readings_dir='_site/readings')
        assert result == 0
    
    @patch('catholic_liturgy_tools.generator.index.scan_readings_files')
    @patch('catholic_liturgy_tools.generator.index.scan_message_files')
    @patch('catholic_liturgy_tools.generator.index.generate_index')
    def test_generate_index_command_with_custom_posts_dir(self, mock_generate, mock_scan_messages, mock_scan_readings):
        """Test command with custom posts directory."""
        mock_args = Mock(posts_dir='custom/_posts', output_file='custom/index.html', readings_dir='custom/readings')
        mock_generate.return_value = Path('custom/index.html')
        mock_scan_messages.return_value = []
        mock_scan_readings.return_value = []
        
        result = cli.generate_index_command(mock_args)
        
        mock_generate.assert_called_once_with(posts_dir='custom/_posts', output_file='custom/index.html', readings_dir='custom/readings')
        assert result == 0
    
    @patch('catholic_liturgy_tools.generator.index.scan_readings_files')
    @patch('catholic_liturgy_tools.generator.index.scan_message_files')
    @patch('catholic_liturgy_tools.generator.index.generate_index')
    def test_generate_index_command_with_custom_output_file(self, mock_generate, mock_scan_messages, mock_scan_readings):
        """Test command with custom output file."""
        mock_args = Mock(posts_dir='_posts', output_file='custom-index.md', readings_dir='readings')
        mock_generate.return_value = Path('custom-index.md')
        mock_scan_messages.return_value = []
        mock_scan_readings.return_value = []
        
        result = cli.generate_index_command(mock_args)
        
        mock_generate.assert_called_once_with(posts_dir='_posts', output_file='custom-index.md', readings_dir='readings')
        assert result == 0
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.generator.index.scan_readings_files')
    @patch('catholic_liturgy_tools.generator.index.scan_message_files')
    @patch('catholic_liturgy_tools.generator.index.generate_index')
    def test_generate_index_command_prints_success_message(self, mock_generate, mock_scan_messages, mock_scan_readings, mock_print):
        """Test that command prints success message."""
        mock_args = Mock(posts_dir='_posts', output_file='index.md', readings_dir='readings')
        output_path = Path('index.md')
        mock_generate.return_value = output_path
        mock_scan_messages.return_value = [Path('_posts/2025-11-22-daily-message.md')]
        mock_scan_readings.return_value = []
        
        cli.generate_index_command(mock_args)
        
        # Verify print was called (should be 6: scanning messages, found X, scanning readings, found Y, generated, file)
        assert mock_print.call_count == 6
        # Check that success message contains both counts
        success_calls = [str(call[0][0]) for call in mock_print.call_args_list if 'Generated index page' in str(call[0][0])]
        assert len(success_calls) == 1
        assert 'messages and' in success_calls[0]
        assert 'readings' in success_calls[0]
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.generator.index.scan_readings_files')
    @patch('catholic_liturgy_tools.generator.index.scan_message_files')
    @patch('catholic_liturgy_tools.generator.index.generate_index')
    def test_generate_index_command_handles_exception(self, mock_generate, mock_scan_messages, mock_scan_readings, mock_print):
        """Test command handles exceptions and returns error code."""
        mock_args = Mock(posts_dir='_posts', output_file='index.md', readings_dir='readings')
        mock_scan_messages.return_value = []
        mock_scan_readings.return_value = []
        mock_generate.side_effect = Exception("Test error")
        
        result = cli.generate_index_command(mock_args)
        
        assert result == 1
        # Verify error was printed (should be in stderr)
        error_calls = [call for call in mock_print.call_args_list if 'Error' in str(call[0][0])]
        assert len(error_calls) > 0
        assert 'Test error' in str(error_calls[0][0][0])


class TestTriggerPublishCommand:
    """Test suite for trigger_publish_command function."""
    
    @patch('catholic_liturgy_tools.github.actions.trigger_workflow')
    def test_trigger_publish_command_calls_trigger(self, mock_trigger):
        """Test that command calls the trigger_workflow function."""
        mock_args = Mock(workflow_file='publish-content.yml', branch='main', date=None)
        mock_trigger.return_value = True
        
        result = cli.trigger_publish_command(mock_args)
        
        mock_trigger.assert_called_once_with(
            workflow_file='publish-content.yml',
            branch='main',
            inputs=None
        )
        assert result == 0
    
    @patch('catholic_liturgy_tools.github.actions.trigger_workflow')
    def test_trigger_publish_command_with_custom_workflow(self, mock_trigger):
        """Test command with custom workflow file."""
        mock_args = Mock(workflow_file='custom-workflow.yml', branch='main', date=None)
        mock_trigger.return_value = True
        
        result = cli.trigger_publish_command(mock_args)
        
        mock_trigger.assert_called_once_with(
            workflow_file='custom-workflow.yml',
            branch='main',
            inputs=None
        )
        assert result == 0
    
    @patch('catholic_liturgy_tools.github.actions.trigger_workflow')
    def test_trigger_publish_command_with_custom_branch(self, mock_trigger):
        """Test command with custom branch."""
        mock_args = Mock(workflow_file='publish-content.yml', branch='develop', date=None)
        mock_trigger.return_value = True
        
        result = cli.trigger_publish_command(mock_args)
        
        mock_trigger.assert_called_once_with(
            workflow_file='publish-content.yml',
            branch='develop',
            inputs=None
        )
        assert result == 0
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.github.actions.trigger_workflow')
    def test_trigger_publish_command_prints_success_message(self, mock_trigger, mock_print):
        """Test that command prints success message."""
        mock_args = Mock(workflow_file='publish-content.yml', branch='main', date=None)
        mock_trigger.return_value = True
        
        cli.trigger_publish_command(mock_args)
        
        # Verify print was called with success message
        assert mock_print.call_count >= 1
        # Check first call contains success message
        first_call = str(mock_print.call_args_list[0][0][0])
        assert 'Successfully triggered' in first_call
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.github.actions.trigger_workflow')
    def test_trigger_publish_command_handles_failure(self, mock_trigger, mock_print):
        """Test command handles trigger failure."""
        mock_args = Mock(workflow_file='publish-content.yml', branch='main')
        mock_trigger.return_value = False
        
        result = cli.trigger_publish_command(mock_args)
        
        assert result == 1
        # Verify error message was printed (first call should have the error)
        assert mock_print.call_count >= 1
        first_call = str(mock_print.call_args_list[0][0][0])
        assert 'Failed to trigger workflow' in first_call
    
    @patch('builtins.print')
    @patch('catholic_liturgy_tools.github.actions.trigger_workflow')
    def test_trigger_publish_command_handles_exception(self, mock_trigger, mock_print):
        """Test command handles exceptions."""
        mock_args = Mock(workflow_file='publish-content.yml', branch='main')
        mock_trigger.side_effect = Exception("Test error")
        
        result = cli.trigger_publish_command(mock_args)
        
        assert result == 1
        # Verify error was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args[0][0])
        assert 'Error' in call_args
        assert 'Test error' in call_args


class TestMainFunction:
    """Test suite for main CLI function."""
    
    @patch('catholic_liturgy_tools.cli.sys.argv', ['catholic-liturgy', 'generate-message'])
    @patch('catholic_liturgy_tools.cli.generate_message_command')
    def test_main_calls_generate_message_command(self, mock_command):
        """Test main function routes to generate-message command."""
        mock_command.return_value = 0
        
        result = cli.main()
        
        assert result == 0
        mock_command.assert_called_once()
    
    @patch('catholic_liturgy_tools.cli.sys.argv', ['catholic-liturgy', 'generate-index'])
    @patch('catholic_liturgy_tools.cli.generate_index_command')
    def test_main_calls_generate_index_command(self, mock_command):
        """Test main function routes to generate-index command."""
        mock_command.return_value = 0
        
        result = cli.main()
        
        assert result == 0
        mock_command.assert_called_once()
    
    @patch('catholic_liturgy_tools.cli.sys.argv', ['catholic-liturgy', 'trigger-publish'])
    @patch('catholic_liturgy_tools.cli.trigger_publish_command')
    def test_main_calls_trigger_publish_command(self, mock_command):
        """Test main function routes to trigger-publish command."""
        mock_command.return_value = 0
        
        result = cli.main()
        
        assert result == 0
        mock_command.assert_called_once()
    
    @patch('catholic_liturgy_tools.cli.sys.argv', ['catholic-liturgy', '--help'])
    def test_main_handles_help_flag(self):
        """Test main function handles help flag."""
        # argparse will exit with code 0 for help
        try:
            cli.main()
        except SystemExit as e:
            assert e.code == 0
    
    @patch('catholic_liturgy_tools.cli.sys.argv', ['catholic-liturgy'])
    def test_main_without_subcommand_shows_help(self):
        """Test main function without subcommand shows help."""
        # argparse will exit with code 2 for missing required subcommand
        try:
            cli.main()
        except SystemExit as e:
            assert e.code in (0, 2)  # Different versions of argparse may vary
