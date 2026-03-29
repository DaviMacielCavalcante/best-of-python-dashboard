import pytest
from requests.exceptions import ConnectionError
from src.data.github_client import get_repo, get_repos


class TestGetRepo:
    """Tests for the get_repo() function."""

    def test_returns_dict_on_success(self, requests_mock, sample_github_repo_response):
        """get_repo() should return the JSON response as a dict on success."""
        requests_mock.get(
            "https://api.github.com/repos/numpy/numpy",
            json=sample_github_repo_response,
        )

        result = get_repo("numpy/numpy")

        assert isinstance(result, dict)
        assert result["name"] == "numpy"
        assert result["stargazers_count"] == 27000

    def test_returns_none_on_http_error(self, requests_mock):
        """get_repo() should return None when the API responds with an error status."""
        requests_mock.get("https://api.github.com/repos/owner/repo", status_code=404)

        result = get_repo("owner/repo")

        assert result is None

    def test_returns_none_on_connection_error(self, requests_mock):
        """get_repo() should return None on network failure."""
        requests_mock.get(
            "https://api.github.com/repos/owner/repo", exc=ConnectionError
        )

        result = get_repo("owner/repo")

        assert result is None

    def test_sends_auth_header_when_token_is_set(
        self, requests_mock, sample_github_repo_response, monkeypatch
    ):
        """get_repo() should include an Authorization header when GITHUB_TOKEN is set."""
        monkeypatch.setenv("GITHUB_TOKEN", "test-token-123")
        adapter = requests_mock.get(
            "https://api.github.com/repos/numpy/numpy",
            json=sample_github_repo_response,
        )

        get_repo("numpy/numpy")

        assert adapter.last_request.headers.get("Authorization") == "Bearer test-token-123"

    def test_sends_no_auth_header_when_token_is_absent(
        self, requests_mock, sample_github_repo_response, monkeypatch
    ):
        """get_repo() should not include an Authorization header when GITHUB_TOKEN is unset."""
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        adapter = requests_mock.get(
            "https://api.github.com/repos/numpy/numpy",
            json=sample_github_repo_response,
        )

        get_repo("numpy/numpy")

        assert "Authorization" not in adapter.last_request.headers

    def test_constructs_correct_url_from_github_id(
        self, requests_mock, sample_github_repo_response
    ):
        """get_repo() should build the URL using owner and repo from the github_id."""
        adapter = requests_mock.get(
            "https://api.github.com/repos/pandas-dev/pandas",
            json=sample_github_repo_response,
        )

        get_repo("pandas-dev/pandas")

        assert adapter.called


class TestGetRepos:
    """Tests for the get_repos() function."""

    def test_returns_list_of_same_length(self, requests_mock, sample_github_repo_response):
        """get_repos() should return a list with one entry per input id."""
        requests_mock.get(
            "https://api.github.com/repos/numpy/numpy", json=sample_github_repo_response
        )
        requests_mock.get(
            "https://api.github.com/repos/pandas-dev/pandas", json=sample_github_repo_response
        )

        result = get_repos(["numpy/numpy", "pandas-dev/pandas"])

        assert len(result) == 2

    def test_returns_none_for_failed_repos(self, requests_mock, sample_github_repo_response):
        """get_repos() should include None for repos that fail."""
        requests_mock.get(
            "https://api.github.com/repos/numpy/numpy", json=sample_github_repo_response
        )
        requests_mock.get(
            "https://api.github.com/repos/bad/repo", status_code=404
        )

        result = get_repos(["numpy/numpy", "bad/repo"])

        assert result[0] is not None
        assert result[1] is None

    def test_returns_empty_list_for_empty_input(self, requests_mock):
        """get_repos() should return an empty list when given no ids."""
        result = get_repos([])

        assert result == []
