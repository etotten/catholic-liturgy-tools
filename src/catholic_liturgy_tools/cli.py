"""Command-line interface for Catholic Liturgy Tools."""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# Skip loading if SKIP_DOTENV_LOAD is set (for testing)
if not os.environ.get('SKIP_DOTENV_LOAD'):
    load_dotenv()


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


def generate_readings_command(args):
    """Execute the generate-readings command."""
    from datetime import datetime
    from catholic_liturgy_tools.scraper.usccb import USCCBReadingsScraper
    from catholic_liturgy_tools.scraper.exceptions import NetworkError, ParseError, ValidationError, DateError
    from catholic_liturgy_tools.generator.readings import generate_readings_page
    from catholic_liturgy_tools.utils.date_utils import get_today
    
    # Determine date to fetch
    if args.date:
        date_str = args.date
        
        # Validate date format
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            # Format display date
            date_display = date_obj.strftime("%B %d, %Y")
        except ValueError:
            print(f"Error: Invalid date format: {date_str}", file=sys.stderr)
            print("Expected format: YYYY-MM-DD", file=sys.stderr)
            print("Example: 2025-12-25", file=sys.stderr)
            return 2
    else:
        date_str = get_today()
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        date_display = date_obj.strftime("%B %d, %Y")
    
    # Display progress
    print(f"Fetching readings for {date_display}...")
    
    try:
        # Initialize scraper and fetch readings
        scraper = USCCBReadingsScraper()
        reading = scraper.get_readings_for_date(date_obj)
        
        print(f'Successfully fetched readings for "{reading.liturgical_day}"')
        
        # Generate HTML page
        output_path = generate_readings_page(reading, args.output_dir)
        
        print(f"Generated HTML page: {output_path}")
        return 0
        
    except NetworkError as e:
        print("Error: Failed to fetch readings from USCCB.org", file=sys.stderr)
        print(f"Network error: {e}", file=sys.stderr)
        print("Please check your internet connection and try again.", file=sys.stderr)
        return 1
        
    except DateError as e:
        print(f"Error: Invalid date: {e}", file=sys.stderr)
        return 2
        
    except ParseError as e:
        print("Error: Failed to parse readings from USCCB page", file=sys.stderr)
        print("The USCCB website structure may have changed.", file=sys.stderr)
        print("Please report this issue at: https://github.com/etotten/catholic-liturgy-tools/issues", file=sys.stderr)
        return 3
        
    except ValidationError as e:
        print(f"Error: Data validation failed: {e}", file=sys.stderr)
        print("The USCCB website structure may have changed.", file=sys.stderr)
        print("Please report this issue at: https://github.com/etotten/catholic-liturgy-tools/issues", file=sys.stderr)
        return 3
        
    except OSError as e:
        print(f"Error: Failed to create output file: {args.output_dir}/{date_str}.html", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        print("Please check directory permissions.", file=sys.stderr)
        return 4
        
    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        return 5


def generate_index_command(args):
    """Execute the generate-index command."""
    from catholic_liturgy_tools.generator.index import generate_index, scan_message_files, scan_readings_files
    
    try:
        # Display progress
        print(f"Scanning daily messages in {args.posts_dir}...")
        message_count = len(scan_message_files(args.posts_dir))
        print(f"Found {message_count} message(s)")
        
        # Scan readings if directory provided
        readings_count = 0
        if args.readings_dir:
            print(f"\nScanning daily readings in {args.readings_dir}...")
            readings_count = len(scan_readings_files(args.readings_dir))
            print(f"Found {readings_count} reading(s)")
        
        # Generate index
        result_path = generate_index(
            posts_dir=args.posts_dir, 
            output_file=args.output_file,
            readings_dir=args.readings_dir
        )
        
        # Display summary
        print(f"\nGenerated index page with {message_count} messages and {readings_count} readings")
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


def check_pages_command(args):
    """Execute the check-pages command."""
    from catholic_liturgy_tools.github.actions import check_pages_status, REPO_OWNER, REPO_NAME
    from datetime import datetime
    
    try:
        status = check_pages_status()
        
        # Check for errors
        if 'error' in status:
            print(f"Error: {status['error']}", file=sys.stderr)
            return 1
        
        # Display Pages configuration
        print("GitHub Pages Status")
        print("=" * 50)
        print(f"Site URL:       {status.get('html_url', 'N/A')}")
        print(f"Build Type:     {status.get('build_type', 'N/A')}")
        print(f"Source Branch:  {status.get('source_branch', 'N/A')}")
        print(f"HTTPS Enforced: {status.get('https_enforced', 'N/A')}")
        
        # Display build status
        build_status = status.get('status')
        if build_status is None:
            print(f"Build Status:   No build in progress")
        else:
            print(f"Build Status:   {build_status}")
        
        # Display recent workflows
        recent_workflows = status.get('recent_workflows', [])
        if recent_workflows:
            print(f"\nRecent Workflow Runs:")
            print("-" * 50)
            for workflow in recent_workflows[:5]:
                name = workflow['name']
                wf_status = workflow['status']
                conclusion = workflow['conclusion'] or 'in_progress'
                created = workflow['created_at']
                
                # Parse and format timestamp
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    time_str = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                except:
                    time_str = created
                
                # Use emoji for status
                if conclusion == 'success':
                    icon = '✅'
                elif conclusion == 'failure':
                    icon = '❌'
                elif conclusion == 'in_progress' or wf_status == 'in_progress':
                    icon = '🔄'
                else:
                    icon = '⚠️'
                
                print(f"{icon} {name}")
                print(f"   Status: {wf_status} / {conclusion}")
                print(f"   Time:   {time_str}")
                print(f"   URL:    {workflow['html_url']}")
                print()
        
        print(f"View all runs: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
        return 0
    
    except ValueError as e:
        # Missing token error
        print(f"Error: {e}", file=sys.stderr)
        print("\nTo set your GitHub Personal Access Token:", file=sys.stderr)
        print("  export GITHUB_TOKEN=ghp_your_token_here", file=sys.stderr)
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
    
    # generate-readings subcommand
    readings_parser = subparsers.add_parser(
        "generate-readings",
        help="Generate HTML page with daily Catholic liturgical readings from USCCB.org",
    )
    readings_parser.add_argument(
        "--date",
        "-d",
        default=None,
        help="Date to generate readings for in YYYY-MM-DD format (default: today)",
    )
    readings_parser.add_argument(
        "--output-dir",
        "-o",
        default="readings",
        help="Output directory for HTML files (default: readings)",
    )
    readings_parser.set_defaults(func=generate_readings_command)
    
    # generate-index subcommand
    index_parser = subparsers.add_parser(
        "generate-index",
        help="Generate an index page with links to all daily messages and readings",
    )
    index_parser.add_argument(
        "--posts-dir",
        "-p",
        default="_posts",
        help="Directory containing message files (default: _posts)",
    )
    index_parser.add_argument(
        "--readings-dir",
        "-r",
        default="readings",
        help="Directory containing readings HTML files (default: readings)",
    )
    index_parser.add_argument(
        "--output-file",
        "-o",
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
    
    # check-pages subcommand
    check_pages_parser = subparsers.add_parser(
        "check-pages",
        help="Check GitHub Pages deployment status",
    )
    check_pages_parser.set_defaults(func=check_pages_command)
    
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
