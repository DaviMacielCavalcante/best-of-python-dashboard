import pytest
from requests.exceptions import ConnectionError, HTTPError
from src.data.loader import load


PROJECTS_URL = "https://raw.githubusercontent.com/lukasmasuch/best-of-python/main/projects.yaml"


class TestLoad:
    """Tests for the load() function."""

    def test_returns_dict_on_success(self, requests_mock, sample_projects_yaml_with_resource):
        """load() should return a dict with 'projects' and 'categories' keys on success."""
        requests_mock.get(PROJECTS_URL, text=sample_projects_yaml_with_resource)

        result = load()

        assert isinstance(result, dict)
        assert "projects" in result
        assert "categories" in result

    def test_filters_out_resource_entries(self, requests_mock, sample_projects_yaml_with_resource):
        """load() should exclude projects where resource=true."""
        requests_mock.get(PROJECTS_URL, text=sample_projects_yaml_with_resource)

        result = load()

        names = [p["name"] for p in result["projects"]]
        assert "numpy" in names
        assert "resource-ref" not in names

    def test_keeps_non_resource_entries(self, requests_mock, sample_projects_yaml_with_resource):
        """load() should preserve all projects that do not have the resource field."""
        requests_mock.get(PROJECTS_URL, text=sample_projects_yaml_with_resource)

        result = load()

        assert len(result["projects"]) == 1

    def test_returns_none_on_http_error(self, requests_mock):
        """load() should return None when the server responds with an error status."""
        requests_mock.get(PROJECTS_URL, status_code=404)

        result = load()

        assert result is None

    def test_returns_none_on_connection_error(self, requests_mock):
        """load() should return None when a network error occurs."""
        requests_mock.get(PROJECTS_URL, exc=ConnectionError)

        result = load()

        assert result is None

    def test_categories_are_preserved(self, requests_mock, sample_projects_yaml_with_resource):
        """load() should return categories unchanged."""
        requests_mock.get(PROJECTS_URL, text=sample_projects_yaml_with_resource)

        result = load()

        assert len(result["categories"]) == 1
        assert result["categories"][0]["category"] == "math"

    def test_returns_none_on_invalid_yaml(self, requests_mock):
        """load() should return None when the response body is not valid YAML."""
        requests_mock.get(PROJECTS_URL, text=": invalid: yaml: ][")

        result = load()

        assert result is None
