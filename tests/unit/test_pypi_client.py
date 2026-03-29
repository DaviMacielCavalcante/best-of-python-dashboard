import pytest
from requests.exceptions import ConnectionError
from src.data.pypi_client import get_lib, get_libs


class TestGetLib:
    """Tests for the get_lib() function."""

    def test_returns_dict_on_success(self, requests_mock, sample_pypi_stats_response):
        """get_lib() should return the JSON response as a dict on success."""
        requests_mock.get(
            "https://pypistats.org/api/packages/numpy/overall",
            json=sample_pypi_stats_response,
        )

        result = get_lib("numpy")

        assert isinstance(result, dict)
        assert result["package"] == "numpy"

    def test_lowercases_package_name_in_url(self, requests_mock, sample_pypi_stats_response):
        """get_lib() should lowercase the package name when building the request URL."""
        adapter = requests_mock.get(
            "https://pypistats.org/api/packages/numpy/overall",
            json=sample_pypi_stats_response,
        )

        get_lib("NumPy")

        assert adapter.called

    def test_returns_none_on_http_error(self, requests_mock):
        """get_lib() should return None when the API responds with an error status."""
        requests_mock.get(
            "https://pypistats.org/api/packages/unknown-pkg/overall",
            status_code=404,
        )

        result = get_lib("unknown-pkg")

        assert result is None

    def test_returns_none_on_connection_error(self, requests_mock):
        """get_lib() should return None on network failure."""
        requests_mock.get(
            "https://pypistats.org/api/packages/numpy/overall",
            exc=ConnectionError,
        )

        result = get_lib("numpy")

        assert result is None

    def test_response_contains_data_list(self, requests_mock, sample_pypi_stats_response):
        """get_lib() response should include a 'data' list."""
        requests_mock.get(
            "https://pypistats.org/api/packages/numpy/overall",
            json=sample_pypi_stats_response,
        )

        result = get_lib("numpy")

        assert "data" in result
        assert isinstance(result["data"], list)


class TestGetLibs:
    """Tests for the get_libs() function."""

    def test_returns_list_of_same_length(
        self, requests_mock, sample_pypi_stats_response, monkeypatch
    ):
        """get_libs() should return one entry per input package."""
        monkeypatch.setattr("src.data.pypi_client.time.sleep", lambda _: None)
        requests_mock.get(
            "https://pypistats.org/api/packages/numpy/overall",
            json=sample_pypi_stats_response,
        )
        requests_mock.get(
            "https://pypistats.org/api/packages/pandas/overall",
            json=sample_pypi_stats_response,
        )

        result = get_libs(["numpy", "pandas"])

        assert len(result) == 2

    def test_returns_none_for_failed_packages(
        self, requests_mock, sample_pypi_stats_response, monkeypatch
    ):
        """get_libs() should include None for packages that fail."""
        monkeypatch.setattr("src.data.pypi_client.time.sleep", lambda _: None)
        requests_mock.get(
            "https://pypistats.org/api/packages/numpy/overall",
            json=sample_pypi_stats_response,
        )
        requests_mock.get(
            "https://pypistats.org/api/packages/bad-pkg/overall",
            status_code=404,
        )

        result = get_libs(["numpy", "bad-pkg"])

        assert result[0] is not None
        assert result[1] is None

    def test_returns_empty_list_for_empty_input(self, requests_mock, monkeypatch):
        """get_libs() should return an empty list when given no packages."""
        monkeypatch.setattr("src.data.pypi_client.time.sleep", lambda _: None)

        result = get_libs([])

        assert result == []
