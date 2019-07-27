from typing_extensions import Literal, TypedDict

GithubSort = Literal['stars', 'forks', 'help-wanted-issues', 'updated']
GithubOrder = Literal['desc', 'asc']


class GithubProjectInfo(TypedDict):
    id: int
    full_name: str
    description: str
    homepage: str
    language: str
