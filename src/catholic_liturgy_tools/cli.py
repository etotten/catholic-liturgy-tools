"""Command-line interface for Catholic Liturgy Tools."""

import argparse
import sys
from pathlib import Path


def generate_message_command(args):
    """Execute the generate-message command."""
    from catholic_liturgy_tools.generator.message import generate_message
    
    try:
        result_path = generate_message(output_dir=args.output_dir)
        print(f"Generated daily message for {result_path.stem.split('-daily-message')[0]}")
        print(f"File: {result_path}")
        return 0
    except OSError as e:
        print(f"Error: Failed to create message file: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def generate_index_command(args):
    """Execute the generate-index command."""
    from catholic_liturgy_tools.generator.index import generate_index
    
    try:
        result_path = generate_index(posts_dir=args.posts_dir, output_file=args.output_file)
        
        # Count message files to report
        from catholic_liturgy_tools.generator.index import scan_message_files
        message_count = len(scan_message_files(args.posts_dir))
        
        print(f"Generated index page with {message_count} messages")
        print(f"File: {result_path}")
        return 0
    except OSError as e:
        print(f"Error: Failed to create index file: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def trigger_publish_command(args):
    """Execute the trigger-publish command."""
    from catholic_liturgy_tools.github.actions import trigger_workflow, REPO_OWNER, REPO_NAME
    
    try:
        success = trigger_workflow(
            workflow_file=args.workflow_file,
            branch=args.branch,
        )
        
        if success:
            print("Successfully triggered GitHub Actions workflow")
            print(f"Workflow: {args.workflow_file}")
            print(f"Check status at: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
            return 0
        else:
            print("Error: Failed to trigger workflow", file=sys.stderr)
            print("Please check your GITHUB_TOKEN and try again", file=sys.stderr)
            return 1
    
    except ValueError as e:
        # Missing token error
        print(f"Error: {e}", file=sys.stderr)
        print("\nTo set your GitHub Personal Access Token:", file=sys.stderr)
        print("  export GITHUB_TOKEN=ghp_your_token_here", file=sys.stderr)
        print("\nSee: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="catholic-liturgy",
        description="Tools for Catholic liturgy and daily message generation",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # generate-message subcommand
    generate_parser = subparsers.add_parser(
        "generate-message",
        help="Generate a daily message for today's date",
    )
    generate_parser.add_argument(
        "--output-dir",
        default="_posts",
        help="Output directory for message files (default: _posts)",
    )
    generate_parser.set_defaults(func=generate_message_command)
    
    # generate-index subcommand
    index_parser = subparsers.add_parser(
        "generate-index",
        help="Generate an index page with links to all daily messages",
    )
    index_parser.add_argument(
        "--posts-dir",
        default="_posts",
        help="Directory containing message files (default: _posts)",
    )
    index_parser.add_argument(
        "--output-file",
        default="index.md",
        help="Output file for index (default: index.md)",
    )
    index_parser.set_defaults(func=generate_index_command)
    
    # trigger-publish subcommand
    trigger_parser = subparsers.add_parser(
        "trigger-publish",
        help="Trigger GitHub Actions workflow to publish messages",
    )
    trigger_parser.add_argument(
        "--workflow-file",
        default="publish-daily-message.yml",
        help="Workflow file to trigger (default: publish-daily-message.yml)",
    )
    trigger_parser.add_argument(
        "--branch",
        default="main",
        help="Branch to run workflow on (default: main)",
    )
    trigger_parser.set_defaults(func=trigger_publish_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
