# Modernization and validation status

Validated 2026-09-22 on macOS with Python 3.13.13. The original teaching inventory is **30 Python files: 28 Streamlit apps/pages (19 entrypoints and nine child pages in three multipage apps), one ML training script and one SQL helper**. Test files added during modernization are not new teaching apps.

All 28 apps/pages received initial execution and rerun checks. All 19 entrypoints passed actual local server startup/health checks. These are separate kinds of evidence: an HTTP health response alone does not execute an app or prove that it works.

## Canonical app matrix

**Fully tested** means the main teaching path was exercised with assertions or browser interaction; it is not exhaustive testing of every possible input. **Smoke tested** means initial/rerun execution plus the listed checks, with broader interaction or visual coverage incomplete. **Limited** identifies a known unverified part. **Requires credentials** means only the no-secret path was tested.

Totals: **10 fully tested, 14 smoke tested, two limited, two requiring credentials**. One limited app (NLP) also contains an untested credential-dependent OpenAI section. No unexpected Python exception remains in the tested paths. The intentional error-display sampler is not counted as a failing app.

Commands below run from the repository root. For each `pages/` row, use its parent's command and navigate in the sidebar.

| File | Lesson / environment | Status | Evidence and limitation |
|---|---|---|---|
| `clt_app/hello_world.py` | First rendering / core | Fully tested | AppTest initial/rerun and browser greeting. |
| `clt_app/clt_demo.py` | Simulation and widgets / core | Fully tested | Probability 0 and 1, histogram output and rerun. Random draws intentionally vary. |
| `clt_app/example.py` | Forms / core | Fully tested | Submitted probability/title reach the rendered figure. |
| `components_example/streamlit_app.py` | Component gallery landing / core | Smoke tested | Landing and navigation to all five pages; run with components extra for children. |
| `components_example/pages/aggrid.py` | Editable component / components | Fully tested | Browser cell edit 39.1→40.2 appeared in Python-returned dataframe; rerun. No CSV write. |
| `components_example/pages/folium_map.py` | Map components / components | Limited | Tiles and vector markers render. Marker-to-Python return remains unconfirmed (null in browser check). |
| `components_example/pages/plotly_events.py` | Click-to-filter / components | Fully tested | Real browser clicks returned selected rows, including Chinstrap; all three species/colors rendered. All-trace JSON-array regression test. |
| `components_example/pages/penguin_animated.py` | Lottie + selection + gated profiling / profiling | Smoke tested | Initial/rerun, offline animation fallback, mocked selected-point branch; shared report generation tested on profiled page. Click a point before profile controls appear. |
| `components_example/pages/penguin_profiled.py` | Cached exploratory report / profiling | Smoke tested | Full HTML generated and checkbox/report iframe browser-verified; not every report control tested. Optional mode explains separate setup. |
| `database_examples/bigquery_app.py` | SQL→dataframe→chart / cloud | Requires credentials | Graceful missing-secret startup/rerun only; no live BigQuery query. |
| `database_examples/streamlit_app.py` | Connection/query cache / snowflake | Requires credentials | Graceful missing-secret startup/rerun only; no live Snowflake query. |
| `huggingface_demo/streamlit_app.py` | Local vs hosted NLP / nlp | Limited | Pinned CPU model downloaded and local sentiment inference passed; missing-key path passed. OpenAI service not called. |
| `job_application_example/job_streamlit.py` | Control flow, airport math / core | Smoke tested | Gate, all eight origins, seven sorted positive distances each, offline animation. Representation exercise remains explanatory. |
| `mpa_example/streamlit_app.py` | Multipage parent / core | Fully tested | Parent title plus navigation to both children and reruns. |
| `mpa_example/pages/app1.py` | First page / core | Fully tested | Parent-based navigation, rendered page text and rerun. |
| `mpa_example/pages/app2.py` | Second page / core | Fully tested | Parent-based navigation, rendered page text and rerun. |
| `penguin_app/penguins.py` | Upload, widgets, Altair / core | Smoke tested | Valid/empty/wrong-column parsing and axis change via file-like inputs; browser upload transport not tested. |
| `penguin_app/session_state_examples.py` | Session state / core | Fully tested | Add item; subsequent rerun does not append it again. |
| `penguin_ml/penguins_streamlit.py` | Cached model + prediction form / core | Smoke tested | Gate, real training, Torgersen inference, histograms; training called once across form reruns. Arbitrary training uploads not certified. |
| `plotting_app/plot_demo.py` | Finite streaming loop / core | Smoke tested | All 100 updates execute, initial/rerun; no exhaustive browser timing check. |
| `plotting_app/tmp.py` | API/media sampler / core | Smoke tested | Initial/rerun permits only intentional `example of error` exception. Audio/video controls not exhaustively tested. |
| `pretty_trees/pretty_trees.py` | Layout and filtering / core | Smoke tested | Private owner/color changes, browser histograms. |
| `pretty_trees/pages/data_quality.py` | Safe editing/download / core | Smoke tested | Disposable-copy edit/export preserves 10,000 rows and 125 missing-coordinate rows; all unedited rows/source bytes unchanged. Browser download transport not tested. |
| `pretty_trees/pages/map.py` | Coordinates/map / core | Smoke tested | Parent navigation, local data and rerun; basemap availability remains external. |
| `random_survey_app/app.py` | Simulation/budget widgets / core | Fully tested | Sample-size and budget changes, both charts and rerun. Original statistical assumptions retained. |
| `streamlit_goodreads_book/goodreads_app.py` | Analytical dashboard / core | Smoke tested | Bundled history, valid/empty/wrong-column uploads, charts, offline Lottie, reruns; file picker not tested. |
| `trees_app/all_code.py` | Chart-library comparison / components | Smoke tested | Full execution including raw 10k-row Altair, browser Bokeh/Vega and map containers; not all toolbar actions. |
| `trees_app/trees.py` | Pandas grouping/native charts / core | Smoke tested | Source-relative CSV and all three native chart outputs, reruns. |

Non-app examples: `penguin_ml/penguins_ml.py` has deterministic-training/schema and safe-export tests. `database_examples/queries.py` is parsed and imported by the BigQuery app; its live SQL execution remains unvalidated.

## Run commands

| Entry point | Command |
|---|---|
| Hello | `uv run streamlit run clt_app/hello_world.py` |
| CLT | `uv run streamlit run clt_app/clt_demo.py` |
| Form | `uv run streamlit run clt_app/example.py` |
| Gallery | `uv run --extra components streamlit run components_example/streamlit_app.py` |
| Profiling gallery | `uv run --project environments/profiling streamlit run components_example/streamlit_app.py` |
| BigQuery | `uv run --extra cloud streamlit run database_examples/bigquery_app.py` |
| Snowflake | `uv run --project environments/snowflake streamlit run database_examples/streamlit_app.py` |
| NLP | `uv run --extra nlp streamlit run huggingface_demo/streamlit_app.py` |
| Airport exercise | `uv run streamlit run job_application_example/job_streamlit.py` |
| Multipage basics | `uv run streamlit run mpa_example/streamlit_app.py` |
| Penguin upload | `uv run streamlit run penguin_app/penguins.py` |
| Todo | `uv run streamlit run penguin_app/session_state_examples.py` |
| Penguin ML | `uv run streamlit run penguin_ml/penguins_streamlit.py` |
| Streaming plot | `uv run streamlit run plotting_app/plot_demo.py` |
| Sampler | `uv run streamlit run plotting_app/tmp.py` |
| Pretty trees | `uv run streamlit run pretty_trees/pretty_trees.py` |
| Survey | `uv run streamlit run random_survey_app/app.py` |
| Goodreads | `uv run streamlit run streamlit_goodreads_book/goodreads_app.py` |
| Chart gallery | `uv run --extra components streamlit run trees_app/all_code.py` |
| Trees | `uv run streamlit run trees_app/trees.py` |

## Dependency and API decisions

The root `uv.lock` keeps Python 3.13.13, Streamlit 1.64.0, Pandas 3.0.6, Altair 6.3.0, NumPy 2.5.3, Matplotlib 3.11.2, Plotly 7.1.0 and scikit-learn 1.9.1. `dev` supplies pytest; components, BigQuery and NLP are optional extras. The four legacy requirements files were retired in Phase 2. Python minor is constrained to 3.13 for this tested lab, not claimed as the only upstream-supported version.

Snowflake connector DataFrame support and profiling require Pandas below 3, so each has a separate project/lockfile. Profiling uses [fg-data-profiling 4.20.0](https://pypi.org/project/fg-data-profiling/4.20.0/) (`data_profiling` import). Neither legacy `pandas_profiling`, its Streamlit wrapper, nor deprecated `ydata_profiling` is installed. The modern HTML report is embedded with `st.iframe` and generated on demand. No legacy setuptools workaround remains.

Removed/replaced calls include `experimental_data_editor` → `data_editor`, `st.bokeh_chart` → `streamlit_bokeh`, `use_container_width` → `width`, removed chart `add_rows` → explicit `st.empty` updates, Pandas `append` → dataframe construction, Series-to-scalar coordinate arithmetic, and old OpenAI completions → the current [Responses API](https://developers.openai.com/api/docs/quickstart). Generated audio supplies its sample rate; video uses actual uploaded MP4 bytes.

Plotly-events 0.0.6 remains intentionally for the original component lesson. Its bundled older Plotly.js cannot consume modern typed-array JSON or Streamlit CSS color variables. The three pages clear/reassign axes as Python lists and set literal species colors. Tests check every trace: simple reassignment of an equal array was insufficient. This small documented compatibility boundary preserves the lesson without downgrading Plotly.

Local CSV/image paths are source-relative. Remote Lottie requests have timeouts, bounded caches and explicit fallback. ML training uses fixed feature categories, a seeded stratified split/forest, and cached data-dependent results. BigQuery clients/results are session-scoped; Snowflake uses `st.connection` and a query TTL. No broad exception handler was added.

## Data safety and external requirements

The editor exports a complete copy; filtering never deletes source rows. No original CSV, image or pickle was modified. Training exports new artifacts to ignored `penguin_ml/generated/` (or a supplied output directory). Old sklearn-1.1.3 pickles are historical artifacts, not portable current models.

Cloud apps need real provider configuration in ignored `.streamlit/secrets.toml`: `[snowflake]` or `[bigquery_service_account]`. OpenAI uses `OPENAI_API_KEY` and an explicitly entered model available to that account. No credentials were invented, read from personal global secrets, or used to run paid service calls. Local model assets come from the pinned Hugging Face revision in source. Map tiles and Lottie assets remain remote dependencies; a network failure can affect visuals without invalidating local analysis.

The empty `basic-sentiment-classifier` gitlink lacks a `.gitmodules` URL and cannot be restored from current repo metadata. It is not required by the updated pinned-model demo. Upstream license provenance is unresolved: no license text was found and none was invented. Tyler Richards's original introduction and attribution remain intact. The public demonstration passwords and intentionally repetitive chapter structure are preserved and explained, not presented as production security or architecture.

## Regression and release checks

```bash
uv sync --locked
uv run pytest
uv run --extra components pytest
uv sync --project environments/profiling --locked
uv sync --project environments/snowflake --locked
```

Final results: **43 passed, 9 skipped** with the core environment; **52 passed** with `--extra components`.

Tests run from a temporary working directory, force HTTP offline, and provide a nonempty credential-free secrets mapping. Optional component checks skip only when their distributions are absent; broken installed packages fail. Python tests cannot certify browser component events, playback, deployment, or real services. Recheck those explicitly when upgrading dependencies.

Start at [walkthrough stop 1](walkthrough.md#1-the-smallest-app). The next unresolved validation target is Folium marker event return, followed by authorized live cloud/OpenAI checks and browser upload/download/media checks. No deployment, commit or push was performed during phases 3–7.
