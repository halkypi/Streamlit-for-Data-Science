# A cumulative Streamlit learning lab

These examples accompany Tyler Richards's *Streamlit for Data Science*. This tour connects the original chapters into a learning sequence; keep the book alongside the code. See [MODERNIZATION.md](MODERNIZATION.md) for what has actually been validated.

Run every command below from the repository root after `uv sync`. Stop a server with Ctrl-C before starting another on the same port. The core environment needs no account. Optional extras and isolated environments are introduced only when their lessons need them.

The execution model to keep tracing is:

**script → render → user interaction → rerun → state/data changes → render again**

A widget usually reruns the script from the top. A form batches edits until submit. Ordinary Python variables are recreated; session state survives within a browser session. Cached results survive reruns according to their arguments and expiry. None of these mechanisms automatically saves a file.

## 1. The smallest app

**File:** [clt_app/hello_world.py](clt_app/hello_world.py)

```bash
uv run streamlit run clt_app/hello_world.py
```

**Concept and source:** Follow `import streamlit` to the rendering call. Python runs on the server and sends UI elements to the browser.

**UI:** Open the local URL and read the greeting. **Experiment:** Change the greeting in source and save; compare a source-triggered rerun with refreshing the browser. **Why first:** There is no data or widget behavior to distract from script-to-render. **Prerequisite/caveat:** Core environment only; the development server must stay running.

## 2. Widgets change a computation

**File:** [clt_app/clt_demo.py](clt_app/clt_demo.py)

```bash
uv run streamlit run clt_app/clt_demo.py
```

**Concept and source:** `number_input` supplies the probability to NumPy's binomial simulation. The list of sample means becomes a Matplotlib histogram; the figure is closed after rendering.

**UI:** Change the probability from 0.5 to 0.8 and follow the histogram's center. **Experiments:** Try 0 and 1; rerun at the same probability and explain the random variation. **Why here:** It makes the rerun model visible before introducing persistent state. **Caveat:** The simulation is stochastic, so exact bars are not expected to repeat.

## 3. Batch changes with a form

**File:** [clt_app/example.py](clt_app/example.py)

```bash
uv run streamlit run clt_app/example.py
```

**Concept and source:** Compare the preceding example with `st.form` and `form_submit_button`. The graph is outside the form and receives the last submitted values.

**UI:** Change the probability and graph title, then submit together. **Experiment:** Edit the title without submitting and observe that the plot does not immediately update. **Why here:** Same statistical idea, one new interaction rule. **Caveat:** A form delays reruns; it does not cache the simulation.

## 4. A rerun is not a timer

**File:** [plotting_app/plot_demo.py](plotting_app/plot_demo.py)

```bash
uv run streamlit run plotting_app/plot_demo.py
```

**Concept and source:** `st.empty` replaces one chart during a finite Python loop. Progress and status update as arrays accumulate; the final button triggers a fresh script run.

**UI:** Watch progress finish, then press Re-run. **Experiment:** In a local edit, shorten the loop or change its sleep and compare responsiveness. **Why here:** Distinguishes repeated rendering within one run from a widget-triggered rerun. **Caveat:** This intentionally takes about five seconds; it is not an unbounded background worker.

## 5. Retain state between runs

**File:** [penguin_app/session_state_examples.py](penguin_app/session_state_examples.py)

```bash
uv run streamlit run penguin_app/session_state_examples.py
```

**Concept and source:** Inspect the conditional initialization of `my_todo_list` and the button-only append. Text input changes alone do not append.

**UI:** Add a task, then change the input without pressing Add. **Experiments:** Add a second item; open a new browser session and compare the initial list. **Why here:** You can now explain why a local list would reset on every run. **Caveat:** This is per-session memory, not a database; empty or duplicate tasks are allowed by the original simple lesson.

## 6. Connect Pandas aggregation to charts

**File:** [trees_app/trees.py](trees_app/trees.py)

```bash
uv run streamlit run trees_app/trees.py
```

**Concept and source:** The CSV path is relative to the source file. `groupby('dbh').count()['tree_id']` produces one count per diameter; its index becomes the chart's x-axis.

**UI:** Compare the same counts as a line, bar and area chart. **Experiment:** Change the grouping to a sensible categorical column in a working copy and consider which chart remains appropriate. **Why here:** Introduces a data transformation before chart-library syntax. **Caveat:** Counts exclude missing identifiers; diameter units and missing values deserve scrutiny before drawing conclusions.

## 7. Upload data and choose Altair encodings

**File:** [penguin_app/penguins.py](penguin_app/penguins.py)

```bash
uv run streamlit run penguin_app/penguins.py
```

**Concept and source:** Follow uploader → CSV/schema checks → numeric conversion → `alt.Chart(...).mark_circle().encode(...)`. Widget values select the x/y columns; species supplies color.

**UI:** Upload the bundled `penguin_app/penguins.csv`, then change x to body mass and y to flipper length. **Experiments:** Swap axes; upload a disposable CSV with the species column missing and inspect the explanation. **Why here:** Builds on a dataframe while introducing user-controlled schema and declarative charts. **Caveat:** Missing/non-numeric measurements become missing points; upload parsing was tested with file-like inputs, not every browser's file picker.

## 8. Compare chart libraries

**File:** [trees_app/all_code.py](trees_app/all_code.py)

```bash
uv run --extra components streamlit run trees_app/all_code.py
```

**Concept and source:** Read the chapter's successive blocks: native charts, Plotly, Seaborn, Matplotlib, Bokeh, Altair and PyDeck. Compare pre-aggregated caretaker counts with Altair's `count():Q` over the raw 10,000 rows. Both should tell the same count story. Bokeh uses `streamlit_bokeh`.

**UI:** Scroll through each chart, compare caretaker counts, and explore the map. **Experiments:** Change an Altair mark; adjust a PyDeck view parameter. **Why here:** You already understand data-to-encoding, so library differences become meaningful. **Caveat:** This intentionally repetitive chapter script is preserved. Components are optional; map tiles require network access. A rendered chart does not validate every toolbar action.

## 9. Explore the UI vocabulary

**File:** [plotting_app/tmp.py](plotting_app/tmp.py)

```bash
uv run streamlit run plotting_app/tmp.py
```

**Concept and source:** Trace text, math, tables, charts, audio, optional video upload, status messages and controls. Look at each rendering call before its output.

**UI:** Inspect the examples, play the generated audio, and optionally upload an MP4 you own. **Experiments:** Change the audio frequency; compare a status message with a raised Python exception. **Why here:** This reference-style sampler is easier after understanding reruns and charts. **Caveat:** The displayed error and `RuntimeError('example of error')` are intentional teaching output. Video playback and all media controls were not exhaustively browser-tested.

## 10. Make a simulation useful to a decision

**File:** [random_survey_app/app.py](random_survey_app/app.py)

```bash
uv run streamlit run random_survey_app/app.py
```

**Concept and source:** Follow sample size into random sampling, expected cost and simulated budget exceedance. Notice the fixed random seed.

**UI:** Compare small and large sample histograms and change the budget. **Experiments:** Keep sample size fixed while increasing budget; explain the difference between expected cost and risk of exceeding it. **Why here:** Combines widgets, simulation, text and plots into one question. **Caveat:** The cost model and synthetic population are teaching assumptions, not survey-design advice.

## 11. Widget-driven control flow and calculations

**File:** [job_application_example/job_streamlit.py](job_application_example/job_streamlit.py); exercise brief: [job_problems.md](job_application_example/job_problems.md).

```bash
uv run streamlit run job_application_example/job_streamlit.py
```

**Concept and source:** Follow the teaching password gate, scalar coordinate extraction, distance computation, dataframe construction and sorting. Read the second representation exercise separately.

**UI:** Use the displayed teaching password `example_password`, then choose airport origins and inspect seven destinations in increasing distance. **Experiments:** Compare opposite routes for symmetry; disconnect the network and observe the optional animation fallback. **Why here:** Adds gating and a nontrivial transformation to familiar widgets. **Caveat:** The hardcoded password illustrates control flow, not secure authentication; animation availability is independent of the calculation.

## 12. Train and serve a reproducible model

**Files:** [penguin_ml/penguins_ml.py](penguin_ml/penguins_ml.py) and [penguin_ml/penguins_streamlit.py](penguin_ml/penguins_streamlit.py).

```bash
uv run python penguin_ml/penguins_ml.py
uv run streamlit run penguin_ml/penguins_streamlit.py
```

**Concept and source:** Start with `encode_features`: fixed island/sex categories guarantee nine columns even for a single row. Follow the stratified split and seeded random forest into `train_model`. In the app, cached training depends on the data; the prediction form reuses the result.

**UI:** Use the displayed teaching password `streamlit_is_great`, keep the bundled training data, then submit plausible measurements. **Experiments:** Change island without changing measurements; compare two training exports' metadata and predictions. **Why here:** Brings together forms, validated data and expensive-work caching. **Caveat:** The initial model fits on first entry. Accuracy is for one small held-out teaching split, not a general performance guarantee. New exports go to ignored `penguin_ml/generated/`; historical sklearn-1.1.3 pickles are retained but never loaded. Load only trusted pickles with matching library versions. The demonstration gate is not authentication.

## 13. Build a richer analytical page

**File:** [streamlit_goodreads_book/goodreads_app.py](streamlit_goodreads_book/goodreads_app.py)

```bash
uv run streamlit run streamlit_goodreads_book/goodreads_app.py
```

**Concept and source:** Follow date parsing, `Year Finished`, groupby counts, `days_to_finish`, rating filters and two-column layouts. The cached Lottie request has a timeout and a fallback; uploaded reading data is not saved to disk by this app.

**UI:** Inspect the bundled history first, then optionally upload your Goodreads export. **Experiments:** Compare the year chart with its grouped dataframe in source; test a disposable export with no completed books. **Why here:** A capstone analytical page combines most preceding concepts. **Caveat:** “Date Added” is not necessarily the reading start date. Some charts describe the whole export, not only completed books. Personal uploads stay in the running app's memory; deploy only where you trust the host.

## 14. Understand multipage navigation

**Files:** [mpa_example/streamlit_app.py](mpa_example/streamlit_app.py), [pages/app1.py](mpa_example/pages/app1.py), [pages/app2.py](mpa_example/pages/app2.py).

```bash
uv run streamlit run mpa_example/streamlit_app.py
```

**Concept and source:** The sibling `pages/` folder creates sidebar navigation. Each page is a simple script.

**UI:** Visit home, app1 and app2, then return home. **Experiment:** Change one page's title and observe that the other page's content is independent. **Why here:** Separates navigation from analytics before combining them. **Caveat:** Start the parent command, not an individual page. The original supported folder-based navigation is deliberately retained.

## 15. Combine layout, filtering, maps and safe editing

**Files:** [pretty_trees/pretty_trees.py](pretty_trees/pretty_trees.py), [pages/map.py](pretty_trees/pages/map.py), [pages/data_quality.py](pretty_trees/pages/data_quality.py).

```bash
uv run streamlit run pretty_trees/pretty_trees.py
```

**Concept and source:** Home filters the dataframe using sidebar owners and colors both Plotly histograms. Map filters missing coordinates for display. Data quality keeps the original full dataframe and merges edits by index into a copy before exporting.

**UI:** Select Private on home; visit map; on data quality edit one diameter and download the complete CSV. **Experiments:** Compare download row count to the original 10,000; verify that the 125 missing-coordinate rows remain. **Why here:** Connects page navigation with a concrete distinction between display filtering and data loss. **Caveat:** The editor includes only privately maintained trees with coordinates. Downloading does not replace the bundled file or persist changes to other pages. Safety tests use a disposable copy; browser download transport is not part of the pytest suite.

## 16. Add external components

**Files:** [components_example/streamlit_app.py](components_example/streamlit_app.py), [pages/aggrid.py](components_example/pages/aggrid.py), [pages/folium_map.py](components_example/pages/folium_map.py), [pages/plotly_events.py](components_example/pages/plotly_events.py).

```bash
uv run --extra components streamlit run components_example/streamlit_app.py
```

**Concept and source:** A component renders JavaScript UI and returns values to Python, potentially triggering a rerun. Inspect AgGrid's cell-change event, Folium's returned objects and Plotly's selected-point filter. Plotly axes are serialized as JSON lists because the component bundles older JavaScript.

**UI:** Visit each named page. Edit an AgGrid number and see the returned dataframe change; explore the Folium map; click a Plotly point and inspect matching rows. **Experiments:** Click another species; compare page-local edits with the unmodified CSV. **Why here:** You can now recognize the same rerun cycle across a frontend/Python boundary. **Caveat:** AgGrid and Plotly events were browser-verified. Folium tiles/vector points rendered, but marker event return is not yet confirmed. Components remain a maintenance boundary and need browser checks after upgrades.

## 17. Make expensive reports explicit

**Files:** [pages/penguin_profiled.py](components_example/pages/penguin_profiled.py) and [pages/penguin_animated.py](components_example/pages/penguin_animated.py).

```bash
uv sync --project environments/profiling
uv run --project environments/profiling streamlit run components_example/streamlit_app.py
```

**Concept and source:** The maintained `fg-data-profiling` distribution imports as `data_profiling`. Read the checkbox before report generation, cache bounds, and `st.iframe` embedding. Compare placement of `st.stop()` in the two pages.

**UI:** On penguin profiled, check Generate profiling report and explore the report. On penguin animated, click a scatter point first to reach profiling. **Experiments:** Uncheck/recheck the report and compare latency; inspect missingness against the raw penguin CSV. **Why here:** Builds on components and teaches caching expensive derived output. **Caveat:** Its Pandas-below-3 constraint is isolated from the core. Only bundled trusted data is embedded. Without this environment the pages explain how to enable profiling; optional Lottie animation can be unavailable.

## 18. Local NLP before a hosted model

**File:** [huggingface_demo/streamlit_app.py](huggingface_demo/streamlit_app.py)

```bash
uv run --extra nlp streamlit run huggingface_demo/streamlit_app.py
```

**Concept and source:** Model ID and revision are explicit; `cache_resource` retains the CPU pipeline. The button delays downloading/loading until requested. The OpenAI section separately uses a secret, user-chosen model and `client.responses.create`.

**UI:** Enter an English movie-review sentence and Analyze locally. **Experiments:** Compare a positive and negative review; consider why sarcasm is harder. **Why here:** Reuses caching and explicit-submit concepts with external model assets. **Caveat:** First use downloads model weights; the score is not calibrated certainty. Local inference was tested. OpenAI was not called: that section requires your own `OPENAI_API_KEY`, account access, model choice and possible paid usage. No key is needed for the local lesson.

## 19. Query services with explicit secrets

**Files:** [database_examples/bigquery_app.py](database_examples/bigquery_app.py), [queries.py](database_examples/queries.py), [streamlit_app.py](database_examples/streamlit_app.py).

```bash
uv run --extra cloud streamlit run database_examples/bigquery_app.py
uv run --project environments/snowflake streamlit run database_examples/streamlit_app.py
```

Run those commands separately. **Concept and source:** BigQuery uses session-scoped cached credentials/client and query results. Snowflake uses the connection cache plus a query TTL. Inspect the SQL and the dataframe columns passed to charts.

**UI:** Without credentials, read the setup message. With your own authorized credentials, query the public dataset and change the lookback (BigQuery), or select the aggregate (Snowflake). **Experiments:** Explain when a cached query can be stale; estimate query cost before increasing scope. **Why here:** Extends familiar dataframe/chart code across an authentication and network boundary. **Caveat:** Neither live query was validated. Keep `[bigquery_service_account]` and `[snowflake]` in untracked `.streamlit/secrets.toml` in the launch directory; obtain actual values from your provider. BigQuery needs a billing/project context and dataset access; Snowflake needs a warehouse and access to `snowflake_sample_data.tpch_sf1.lineitem`. Snowflake's separate environment preserves core Pandas 3. Never publish secrets.

## 20. Reproduce and prepare to teach

**Files:** [pyproject.toml](pyproject.toml), [uv.lock](uv.lock), [.python-version](.python-version), [tests](tests), [MODERNIZATION.md](MODERNIZATION.md).

```bash
uv sync --locked
uv run pytest
uv run streamlit run clt_app/hello_world.py
```

**Concept and source:** A lockfile fixes the environment; tests protect Python behavior; a browser is still needed for component/media behavior. Review chapter `.streamlit/config.toml` files where present: Streamlit reads configuration relative to the launch directory, unlike the source-relative dataset paths.

**UI:** Start Hello World again from the root. **Experiments:** Run `uv run --extra components pytest` to include optional component checks; explain why a green missing-secret test cannot certify a cloud query. **Why last:** Turns individual examples into a repeatable lab. **Caveat:** No deployment was performed. Before deployment, select one entrypoint/environment, configure secrets on the trusted host, check its uv support, resource limits, networking and session behavior, and verify with real service access. Do not combine all optional environments or restore old pins merely to make one deployment install.
