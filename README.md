# best-of-python-dashboard 🐍

A Streamlit dashboard for exploring and visualizing Python libraries from the [best-of-python](https://github.com/lukasmasuch/best-of-python) curated list.

## Overview

The Python ecosystem has hundreds of great libraries scattered across GitHub and PyPI, making it hard to compare them at a glance. This dashboard fetches real-time data from the GitHub and PyPI Stats APIs to let you rank libraries by stars, forks, or downloads — and track their download growth over time.

Data is cached locally for 24 hours to avoid hammering the APIs on every page load.

## Tech Stack

Streamlit, Polars, Plotly, Requests, diskcache, Loguru, PyYAML, python-dotenv

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
git clone https://github.com/davicc/best-of-python-dashboard
cd best-of-python-dashboard

# with uv
uv sync

# or with pip
pip install .
```

### Configuration

Copy `.env.example` to `.env` and set your GitHub token (optional, but recommended to avoid rate limits):

```bash
GITHUB_TOKEN=ghp_your_token_here
```

Without a token, the GitHub API allows 60 requests/hour. With one, it's 5,000/hour.

### Usage

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Architecture

```
app.py              ← Home page (overview metrics)
pages/
  1_Ranking.py      ← Rank libraries by stars, forks, or downloads
  2_Growth.py       ← Compare download trends over time
src/
  data/
    loader.py       ← Fetches projects.yaml from best-of-python repo
    github_client.py← GitHub API calls (concurrent via ThreadPoolExecutor)
    pypi_client.py  ← PyPI Stats API calls (concurrent, rate-limited)
  cache/
    manager.py      ← Disk-based cache (24h TTL, stored in .temp/cache)
  utils/
    logger.py       ← Loguru setup (rotating logs in .temp/logs)
```

Data flows from the public YAML → GitHub/PyPI APIs → disk cache → Streamlit pages.

## Running Tests

```bash
pytest -v
```

## Contributing

Open an issue or pull request — all feedback welcome.

## License

Creative Commons Attribution-ShareAlike 4.0 International — see [LICENCE.MD](LICENCE.MD) for details.

---

**Author:** Davi Cavalcante — [davicc@outlook.com.br](mailto:davicc@outlook.com.br)

*"Your focus determines your reality." — Qui-Gon Jinn (also applies to picking the right library)*
