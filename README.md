# Streamlit for Data Science

A modern, reproducible teaching lab for Tyler Richards's book. Start with the
[cumulative walkthrough](walkthrough.md), and consult the
[app-by-app validation matrix](MODERNIZATION.md) for tested behavior and limits.
The lab contains 28 Streamlit apps/pages; cloud services and some browser paths
still have explicit validation limits.

## Lab setup (uv)

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
from the repository root:

```bash
uv sync
uv run streamlit run clt_app/hello_world.py
uv run pytest
```

uv installs Python 3.13.13 from `.python-version` and creates `.venv`.
`pyproject.toml` declares dependencies; `uv.lock` records resolved versions.
Use `uv sync --locked` to reject an out-of-date lockfile. The four former
requirements files are retired. Local teaching datasets resolve relative to
source files, so the walkthrough's root-based commands work consistently.

The default environment includes Streamlit, Pandas, NumPy, Altair, Matplotlib,
Seaborn, Plotly, PyDeck, scikit-learn, Requests, Lottie, and the `dev` group
(pytest). Use `uv sync --no-dev` for runtime dependencies only.

| Optional extra | Example command from root | Scope |
|---|---|---|
| Components | `uv run --extra components streamlit run components_example/streamlit_app.py` | AgGrid, Folium, Plotly events, Bokeh |
| Cloud | `uv run --extra cloud streamlit run database_examples/bigquery_app.py` | BigQuery and Google authentication |
| NLP | `uv run --extra nlp streamlit run huggingface_demo/streamlit_app.py` | Transformers, Torch, OpenAI |

For an explicit installation use `uv sync --extra components` (or `cloud` or
`nlp`). Repeat the extra on `uv run`; extras can be combined. Plain `uv sync`
restores the default dependency set. `uv run --extra components pytest` includes
the nine optional component tests skipped by the default suite. NLP installs
and the first model download can be large; this lesson uses CPU inference.
Installing a dependency does not provide credentials or validate a live service.

## Isolated lessons

Snowflake's connector DataFrame support and profiling require Pandas below 3.
Separate projects keep those constraints out of the core environment:

```bash
uv sync --project environments/snowflake
uv run --project environments/snowflake streamlit run database_examples/streamlit_app.py
```

```bash
uv sync --project environments/profiling
uv run --project environments/profiling streamlit run components_example/streamlit_app.py
```

Run each server separately. Profiling uses maintained `fg-data-profiling`, imported
as `data_profiling`, and embeds its generated HTML without the obsolete Streamlit
profiling wrapper. Select **penguin profiled** and check **Generate profiling
report**. On **penguin animated**, click a point first. Keep all three lockfiles
when updating dependencies.

## Data, secrets and validation

- The tree editor downloads a complete edited copy; it never overwrites the
  bundled CSV or drops rows outside its editing view.
- ML trains reproducibly with the current stack and caches training across
  reruns. `uv run python penguin_ml/penguins_ml.py` writes new artifacts under
  ignored `penguin_ml/generated/`. Historical pickles are preserved and unused.
- BigQuery needs `[bigquery_service_account]` and Snowflake needs `[snowflake]`
  in ignored `.streamlit/secrets.toml` in the launch directory. Use actual
  provider-issued values. Both apps explain missing configuration; neither live
  service was validated during modernization.
- Local sentiment analysis uses a pinned Hugging Face model and needs no API
  key. The separate OpenAI section needs `OPENAI_API_KEY` and an account-accessible
  model name. No OpenAI request was made during validation.
- Job/ML demonstration passwords are shown in the apps. These teach conditional
  UI flow, not secure authentication. `plotting_app/tmp.py` deliberately displays
  an error and example exception.
- AppTest covers Python execution and selected interactions, not every browser
  feature. See [MODERNIZATION.md](MODERNIZATION.md) before treating an example as
  fully validated. Folium event return and browser upload/download/media paths
  remain partly unverified; remote maps/animations require network access.

Chapter-local Streamlit config files are retained. Streamlit reads config from
the launch working directory, so root-based runs need not use a chapter's theme.
No deployment was performed. The empty `basic-sentiment-classifier` gitlink has
no recoverable remote URL in the repository metadata. Original attribution is
preserved below; no license text was present and no license has been invented.

## Original introduction

Welcome to [Streamlit for Data Science!](https://www.amazon.com/Streamlit-Data-Science-Create-interactive/dp/180324822X) I'm the author, [Tyler Richards](https://www.tylerjrichards.com), and I wrote this book when I was at Facebook, and have since moved to work for Streamlit, which is now owned by Snowflake.
If you're coming here from the book, go ahead and take a peak inside each one of the sub-folders in this main repo. You can feel free to [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository), and if anything doesn't work you can always [open an issue or pull request](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/working-with-your-remote-repository-on-github-or-github-enterprise/creating-an-issue-or-pull-request) or just find me on [Twitter](https://www.twitter.com/tylerjrichards) and DM me until I figure it out.
If you're coming here from another place on the internet, feel free to use these respositories and examples however you would like! They are more useful in context, and so I would obviously recommend [giving the book a shot](https://www.amazon.com/Streamlit-Data-Science-Create-interactive/dp/180324822X). If you're a new data scientist who can't afford the book, please reach out to me and I'd be happy to provide a copy no questions asked.
The first chapter starts in the folder 'clt_app', head over there with the book in hand and enjoy! As a note: since I moved to working at Streamlit, I donate all proceeds for this book to [PyLadies](https://pyladies.com/).

#### Book Edits
Streamlit is an ever-changing library, and by the time this book was written it was already slightly behind compared to newer versions of the library. If you notice error messages, please message me about them so I can get them all fixed or note them below!
