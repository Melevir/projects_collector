import argparse
import logging
import math
import os
import sys
from typing import List

import requests

from common_types import GithubSort, GithubOrder, GithubProjectInfo
from config import MAX_GITHUB_API_PAGE_SIZE, GITHUB_API_TOKEN, DEFAULT_PROJECTS_DIRECTORY
from git import Repo


log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('git').setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('search_query', help='Github search query')
    parser.add_argument(
        '--projects_path',
        default=DEFAULT_PROJECTS_DIRECTORY,
        help='path to directory where new projects will be cloned',
    )
    parser.add_argument('--projects_amount', type=int, default=10, help='amount of projects to clone')
    parser.add_argument(
        '--sort_by',
        default='stars',
        choices=['stars', 'forks', 'help-wanted-issues', 'updated'],
        help='field to search projects with',
    )
    parser.add_argument('--order', default='desc', choices=['desc', 'asc'], help='order of sorting')

    return parser.parse_args()


def fetch_projects(
    search_query: str,
    projects_path: str,
    projects_amount: int = 100,
    sort: GithubSort = 'stars',
    order: GithubOrder = 'desc',
) -> None:
    if projects_amount <= MAX_GITHUB_API_PAGE_SIZE:
        per_page = projects_amount
        pages_amount = 1
    else:
        per_page = MAX_GITHUB_API_PAGE_SIZE
        pages_amount = math.ceil(projects_amount / per_page)

    for project_info in make_github_search_query(search_query, sort, order, pages_amount, per_page):
        clone_project(project_info, projects_path)


def make_github_search_query(
    search_query: str,
    sort: GithubSort,
    order: GithubOrder,
    pages_amount: int,
    per_page: int,
) -> List[GithubProjectInfo]:
    projects_info: List[GithubProjectInfo] = []
    for page_num in range(1, pages_amount + 1):
        current_page_data = requests.get(  # type: ignore  # seems like typeshed can't work with Literal
            'https://api.github.com/search/repositories',
            params={
                'q': search_query,
                'sort': sort,
                'order': order,
                'page': page_num,
                'per_page': per_page,
            },
            headers={
                'Authorization': f'token {GITHUB_API_TOKEN}',
            },
        ).json()
        projects_info += current_page_data['items']
    return projects_info


def clone_project(project_info: GithubProjectInfo, projects_path: str) -> None:
    log.debug(f'Cloning {project_info["full_name"]}...')
    repo_path = os.path.join(projects_path, project_info['full_name'].replace('/', '_'))
    if os.path.exists(repo_path):
        return
    git_url = f'https://github.com/{project_info["full_name"]}.git'
    Repo.clone_from(git_url, repo_path)


if __name__ == '__main__':
    args = parse_args()
    fetch_projects(
        search_query=args.search_query,
        projects_path=args.projects_path,
        projects_amount=args.projects_amount,
        sort=args.sort_by,
        order=args.order,
    )
