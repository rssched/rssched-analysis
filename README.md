# RSSched Output Analysis and Visualization

Analysis and visualization of results from the scheduler service. Part of the Innosuisse project
Rolling Stock Scheduling (RSSched) by SBB and ETH Zurich.

To get started with the whole RSSched project, have a look at this [step-by-step instruction](https://github.com/rolling-stock-scheduling/.github/blob/main/getting_started.md).

## Setup

1. install poetry a package manager for python: https://python-poetry.org/docs/

2. install the dependencies for this project via:

   ```sh
   poetry install
   ```

## Usage

Visualize a rolling stock scheduling response from the solver:

```sh
poetry run rssched-plot rssched/data/small_test_response.json
```

To start a streamlit dashboard run
```sh
poetry run streamlit run rssched/app/Instance.py
```

## Development

Before committing, run the following commands from the project root directory:

```sh
poetry run isort .
poetry run black .
poetry run pytest
```

Note: If working with jupyter notebooks, also delete the cell outputs before committing.

---

© 2024 SBB CFF FFS. Licensed under MIT.
