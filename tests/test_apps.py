import ast
import importlib
from importlib.metadata import PackageNotFoundError, version
import io
import json
from pathlib import Path

import pandas as pd
import pytest

from conftest import ROOT

ENTRYPOINTS = sorted(
    p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/*.py")
    if p.name not in {"queries.py", "penguins_ml.py"} and p.parent.name != "tests"
)
PAGES = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/pages/*.py"))
OPTIONAL = {
    "trees_app/all_code.py": "streamlit_bokeh",
    "aggrid.py": "st_aggrid", "folium_map.py": "streamlit_folium",
    "penguin_animated.py": "streamlit_plotly_events",
    "penguin_profiled.py": "streamlit_plotly_events",
    "plotly_events.py": "streamlit_plotly_events",
}


def optional_module(name):
    distribution = "streamlit-aggrid" if name == "st_aggrid" else name.replace("_", "-")
    try:
        version(distribution)
    except PackageNotFoundError:
        pytest.skip("Install the components extra for this check")
    # An installed but broken component must fail, not silently skip.
    return importlib.import_module(name)


def healthy(at):
    assert not at.exception, [e.message for e in at.exception]


@pytest.mark.parametrize("path", ENTRYPOINTS + PAGES)
def test_initial_and_rerun(app, path):
    optional = OPTIONAL.get(path, OPTIONAL.get(Path(path).name))
    if optional:
        optional_module(optional)
    if "/pages/" in path:
        chapter = path.split("/")[0]
        parent = "pretty_trees.py" if chapter == "pretty_trees" else "streamlit_app.py"
        at = app(f"{chapter}/{parent}")
        at.switch_page("pages/" + Path(path).name).run()
    else:
        at = app(path)
    for _ in range(2):
        if path == "plotting_app/tmp.py":
            assert [e.message for e in at.exception] == ["example of error"]
        else:
            healthy(at)
        at.run()


def test_all_teaching_python_parses():
    for path in ENTRYPOINTS + PAGES + ["penguin_ml/penguins_ml.py", "database_examples/queries.py"]:
        ast.parse((ROOT / path).read_text(), filename=path)
    assert len(ENTRYPOINTS) == 19
    assert len(PAGES) == 9


def test_todo_add_does_not_repeat_on_rerun(app):
    at = app("penguin_app/session_state_examples.py")
    at.text_input[0].set_value("Study reruns").run()
    at.button[0].click().run()
    at.run()
    healthy(at)
    assert at.session_state["my_todo_list"].count("Study reruns") == 1


def test_clt_bounds_and_form(app, monkeypatch):
    at = app("clt_app/clt_demo.py")
    for value in [0.0, 1.0]:
        at.number_input[0].set_value(value).run()
        healthy(at)
        assert at.get("image")
    titles = []
    monkeypatch.setattr("matplotlib.pyplot.title", lambda title: titles.append(title))
    at = app("clt_app/example.py")
    at.text_input[0].set_value("Submitted title")
    at.number_input[0].set_value(0.7)
    at.button[0].click().run()
    healthy(at)
    assert titles[-1] == "Submitted title"


def test_airport_distances_and_offline_animation(app):
    at = app("job_application_example/job_streamlit.py")
    at.text_input[0].set_value("example_password").run()
    assert any("unavailable" in c.value for c in at.caption)
    for origin in at.selectbox[0].options:
        at.selectbox[0].set_value(origin).run()
        healthy(at)
        frame = next(x.value for x in at.dataframe if "Distance" in x.value.columns)
        assert len(frame) == 7
        assert origin not in frame["Airport Code"].tolist()
        assert frame["Distance"].is_monotonic_increasing
        assert frame["Distance"].gt(0).all()


@pytest.mark.parametrize("path", ["database_examples/bigquery_app.py", "database_examples/streamlit_app.py"])
def test_missing_secrets_stop_before_service_use(app, path):
    at = app(path)
    healthy(at)
    assert at.info
    assert not at.dataframe


@pytest.mark.parametrize("path,data", [
    ("penguin_app/penguins.py", "penguin_app/penguins.csv"),
    ("streamlit_goodreads_book/goodreads_app.py", "streamlit_goodreads_book/goodreads_history.csv"),
])
@pytest.mark.parametrize("input_kind", ["valid", "empty", "wrong_columns"])
def test_upload_parsing(app, monkeypatch, path, data, input_kind):
    payload = {"valid": (ROOT / data).read_bytes(), "empty": b"", "wrong_columns": b"wrong\n1\n"}[input_kind]
    # A fresh stream on each rerun reproduces an uploaded file's reusable contents.
    monkeypatch.setattr("streamlit.file_uploader", lambda *a, **kw: io.BytesIO(payload))
    at = app(path)
    at.run()
    healthy(at)
    if input_kind == "valid":
        assert not at.error
        assert at.get("plotly_chart") or at.get("image") or at.get("vega_lite_chart")
    else:
        assert at.error


@pytest.mark.parametrize("page", ["plotly_events.py", "penguin_animated.py", "penguin_profiled.py"])
def test_component_selection_and_legacy_js_serialization(app, monkeypatch, page):
    component = optional_module("streamlit_plotly_events")
    figures = []
    def click(fig, **kwargs):
        figures.append(json.loads(fig.to_json()))
        return [{"x": 39.1, "y": 18.7}]
    monkeypatch.setattr(component, "plotly_events", click)
    at = app("components_example/streamlit_app.py")
    at.switch_page("pages/" + page).run()
    healthy(at)
    selected = at.dataframe[0].value
    assert len(selected) > 0
    assert selected["bill_length_mm"].eq(39.1).all()
    assert selected["bill_depth_mm"].eq(18.7).all()
    for trace in figures[-1]["data"]:
        assert isinstance(trace["x"], list) and isinstance(trace["y"], list)
        assert trace["marker"]["color"].startswith("#")
