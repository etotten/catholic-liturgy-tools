"""GitHub Actions workflow trigger module."""

import os
import requests
from typing import Optional

from ..constants import DEFAULT_WORKFLOW_FILE


# Repository configuration
REPO_OWNER = "etotten"
REPO_NAME = "catholic-liturgy-tools"


def trigger_workflow(  # pragma: no cover
    workflow_file: str = DEFAULT_WORKFLOW_FILE,
    branch: str = "main",
    inputs: Optional[dict] = None
) -> bool:
    """
    Trigger a GitHub Actions workflow remotely.
    
    Args:
        workflow_file: Name of the workflow file (default: publish-content.yml)
        branch: Branch to run the workflow on (default: main)
        inputs: Optional dictionary of workflow inputs (e.g., {'date': '2025-12-25'})
        
    Returns:
        bool: True if workflow was triggered successfully, False otherwise
        
    Raises:
        ValueError: If GITHUB_TOKEN environment variable is not set
        
    Example:
        >>> import os
        >>> os.environ['GITHUB_TOKEN'] = 'ghp_xxxxx'
        >>> trigger_workflow()
        True
        >>> trigger_workflow(inputs={'date': '2025-12-25'})
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
    
    # Add inputs if provided
    if inputs:
        payload['inputs'] = inputs
    
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


def check_pages_status() -> dict:  # pragma: no cover
    """
    Check the GitHub Pages deployment status.
    
    Returns:
        dict: Pages status information including:
            - html_url: The public URL of the site
            - status: Current build status (null if no build in progress)
            - build_type: How pages is configured (workflow or legacy)
            - recent_workflows: List of recent workflow runs
        
    Raises:
        ValueError: If GITHUB_TOKEN environment variable is not set
        
    Example:
        >>> import os
        >>> os.environ['GITHUB_TOKEN'] = 'ghp_xxxxx'
        >>> status = check_pages_status()
        >>> print(status['html_url'])
        https://etotten.github.io/catholic-liturgy-tools/
    """
    # Get GitHub token from environment
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError(
            "GITHUB_TOKEN environment variable not set. "
            "Please set your GitHub Personal Access Token."
        )
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    
    result = {}
    
    try:
        # Get Pages configuration
        pages_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pages"
        pages_response = requests.get(pages_url, headers=headers)
        
        if pages_response.status_code == 200:
            pages_data = pages_response.json()
            result['html_url'] = pages_data.get('html_url')
            result['status'] = pages_data.get('status')
            result['build_type'] = pages_data.get('build_type')
            result['source_branch'] = pages_data.get('source', {}).get('branch')
            result['https_enforced'] = pages_data.get('https_enforced')
        elif pages_response.status_code == 404:
            result['error'] = "GitHub Pages is not enabled for this repository"
            return result
        else:
            result['error'] = f"Failed to get Pages info: {pages_response.status_code}"
            return result
        
        # Get recent workflow runs
        runs_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
        runs_response = requests.get(runs_url, headers=headers, params={'per_page': 5})
        
        if runs_response.status_code == 200:
            runs_data = runs_response.json()
            result['recent_workflows'] = [
                {
                    'name': run['name'],
                    'status': run['status'],
                    'conclusion': run['conclusion'],
                    'created_at': run['created_at'],
                    'html_url': run['html_url']
                }
                for run in runs_data.get('workflow_runs', [])
            ]
        
        return result
        
    except requests.RequestException as e:
        return {'error': f"Request failed: {e}"}
