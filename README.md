### Streamlit for Data Science

## Lab setup (uv)

The environment is being modernized; most teaching apps still need compatibility
updates. Environment installation does not imply that every app works yet.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run from
the repository root:

```bash
uv sync
uv run streamlit run clt_app/hello_world.py
```

uv installs the Python patch version in `.python-version` and creates `.venv`.
`pyproject.toml` is the dependency source of truth; `uv.lock` records exact
versions. The four former requirements.txt files have been retired. Use
`uv sync --locked` when you want setup to fail rather than change the lockfile.
Python 3.13 is the supported lab minor version for now.

The default environment includes Streamlit, Pandas, NumPy, Altair, Matplotlib,
Seaborn, Plotly, PyDeck, scikit-learn, Requests, Lottie, and the `dev` group
(pytest). Use `uv sync --no-dev` for runtime dependencies only.

Optional examples have separate extras:

| Extra | Install from repo root | Scope |
|---|---|---|
| Components | `uv sync --extra components` | AgGrid, Folium, Plotly events, modern Bokeh integration |
| Cloud | `uv sync --extra cloud` | BigQuery with DataFrame support and Google authentication |
| NLP | `uv sync --extra nlp` | Transformers, Torch and OpenAI; large download |

Repeat extras when running commands, for example
`uv run --extra components streamlit run streamlit_app.py` from `components_example`.
Extras can be combined by repeating `--extra`; plain `uv sync` restores the
default dependency set. Installing an extra does not provide credentials or
validate its service, browser component, or application behavior. Torch's Linux
distribution may also download large GPU runtime packages; GPU setup is not
required for the introductory lab.

Snowflake's current connector DataFrame extra requires Pandas below 3.0. That
lesson has a separate lockfile so its constraint does not downgrade the core:

```bash
uv sync --project environments/snowflake
uv run --project environments/snowflake streamlit run database_examples/streamlit_app.py
```

This uses Pandas 2.3 and the current connector. Its service still needs credentials
and app-level validation. Keep both lockfiles when updating the project.

Many existing apps still use working-directory-relative data paths. Until those
are modernized, run them from their chapter directory. For example:

```bash
cd components_example
uv run --extra components streamlit run streamlit_app.py
```

Known migration boundaries:

- Profiling pages are preserved but not runnable in this environment yet.
  `pandas-profiling` and `streamlit-pandas-profiling` are excluded. The current
  replacement, `ydata-profiling`, constrains Pandas below 3.0, NumPy below 2.4 and
  Matplotlib at most 3.10. Profiling needs a deliberate separate environment or
  compatible replacement in Phase 3; it must not downgrade the whole lab.
- Modern Bokeh and `streamlit-bokeh` are in the components extra. The old
  `st.bokeh_chart` call still needs migration; Bokeh 2.4.3 is not retained.
- `streamlit-plotly-events` remains available for the original lesson, but its
  browser behavior with the modern stack still needs validation. Native Plotly
  selection is a possible later migration, not a completed change.
- The bundled random forest was saved with scikit-learn 1.1.3. It needs
  reproducible retraining and feature-schema validation; installing an old
  scikit-learn is not the solution. The original artifacts are untouched.
- Cloud apps need configured `snowflake` or `bigquery_service_account` secrets.
  The NLP app needs model downloads and `OPENAI_API_KEY`, and its old OpenAI call
  still needs migration. Keep credentials in untracked `.streamlit/secrets.toml`
  for the working directory from which the app is launched.

## Original introduction

Welcome to [Streamlit for Data Science!](https://www.amazon.com/Streamlit-Data-Science-Create-interactive/dp/180324822X) I'm the author, [Tyler Richards](www.tylerjrichards.com), and I wrote this book when I was at Facebook, and have since moved to work for Streamlit, which is now owned by Snowflake. 
If you're coming here from the book, go ahead and take a peak inside each one of the sub-folders in this main repo. You can feel free to [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository), and if anything doesn't work you can always [open an issue or pull request](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/working-with-your-remote-repository-on-github-or-github-enterprise/creating-an-issue-or-pull-request) or just find me on [Twitter](https://www.twitter.com/tylerjrichards) and DM me until I figure it out.
If you're coming here from another place on the internet, feel free to use these respositories and examples however you would like! They are more useful in context, and so I would obviously recommend [giving the book a shot](https://www.amazon.com/Streamlit-Data-Science-Create-interactive/dp/180324822X). If you're a new data scientist who can't afford the book, please reach out to me and I'd be happy to provide a copy no questions asked.
The first chapter starts in the folder 'clt_app', head over there with the book in hand and enjoy! As a note: since I moved to working at Streamlit, I donate all proceeds for this book to [PyLadies](https://pyladies.com/). 

#### Book Edits
Streamlit is an ever-changing library, and by the time this book was written it was already slightly behind compared to newer versions of the library. If you notice error messages, please message me about them so I can get them all fixed or note them below!
