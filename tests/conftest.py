import pytest



@pytest.fixture
def sample_projects_yaml_with_resource():
    return """
projects:
  - name: numpy
    github_id: numpy/numpy
    pypi_id: numpy
    category: math
  - name: resource-ref
    github_id: owner/resource-ref
    resource: true
    category: math
categories:
  - category: math
    title: Math & Statistics
"""


@pytest.fixture
def sample_github_repo_response():
    return {
        "id": 12345,
        "name": "numpy",
        "full_name": "numpy/numpy",
        "stargazers_count": 27000,
        "forks_count": 8000,
    }


@pytest.fixture
def sample_pypi_stats_response():
    return {
        "data": [
            {"category": "without_mirrors", "date": "2024-01-10", "downloads": 5000000},
            {"category": "without_mirrors", "date": "2024-01-09", "downloads": 4800000},
            {"category": "with_mirrors", "date": "2024-01-10", "downloads": 6000000},
        ],
        "package": "numpy",
        "type": "overall",
    }
