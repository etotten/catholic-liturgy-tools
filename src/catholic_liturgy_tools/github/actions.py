"""GitHub Actions workflow trigger module."""

import os
import requests
from typing import Optional


# Repository configuration
REPO_OWNER = "etotten"
REPO_NAME = "catholic-liturgy-tools"


def trigger_workflow(
    workflow_file: str = "publish-daily-message.yml",
    branch: str = "main"
) -> bool:
    """
    Trigger a GitHub Actions workflow remotely.
    
    Args:
        workflow_file: Name of the workflow file (default: publish-daily-message.yml)
        branch: Branch to run the workflow on (default: main)
        
    Returns:
        bool: True if workflow was triggered successfully, False otherwise
        
    Raises:
        ValueError: If GITHUB_TOKEN environment variable is not set
        
    Example:
        >>> import os
        >>> os.environ['GITHUB_TOKEN'] = 'ghp_xxxxx'
        >>> trigger_workflow()
        True
    """
    # Get GitHub token from environment
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError(
            "GITHUB_TOKEN environment variable not set. "
            "Please set your GitHub Personal Access Token with 'workflow' scope."
        )
    
    # Construct API URL
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{workflow_file}/dispatches"
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    
    # Prepare payload
    payload = {
        'ref': branch,
    }
    
    # Make API request
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 204:
            # Success (No Content response)
            return True
        elif response.status_code in (401, 403):
            # Authentication/authorization error
            print(f"Authentication error: {response.text}")
            return False
        elif response.status_code == 404:
            # Workflow not found
            print(f"Workflow not found: {response.text}")
            return False
        else:
            # Other error
            print(f"Unexpected error ({response.status_code}): {response.text}")
            return False
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
