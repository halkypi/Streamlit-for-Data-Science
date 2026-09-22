import io
import json
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from conftest import ROOT
from penguin_ml.penguins_ml import encode_features, train_model


def test_editor_exports_all_rows_without_overwriting_source(tmp_path, monkeypatch):
    chapter = tmp_path / "pretty_trees"
    (chapter / "pages").mkdir(parents=True)
    for name in ["trees.csv", "pretty_trees.py", "pages/data_quality.py"]:
        shutil.copy(ROOT / "pretty_trees" / name, chapter / name)
    source_bytes = (chapter / "trees.csv").read_bytes()
    source = pd.read_csv(io.BytesIO(source_bytes))
    exports, edited_indices = [], []
    def edit(frame, **kwargs):
        frame = frame.copy()
        edited_indices.append(frame.index[0])
        frame.loc[frame.index[0], "dbh"] = 42
        return frame
    monkeypatch.setattr("streamlit.data_editor", edit)
    monkeypatch.setattr("streamlit.download_button", lambda label, data, **kw: exports.append(data))
    at = AppTest.from_file(str(chapter / "pretty_trees.py"), default_timeout=30).run()
    at.switch_page("pages/data_quality.py").run()
    assert not at.exception
    exported = pd.read_csv(io.BytesIO(exports[-1]))
    assert len(exported) == len(source) == 10000
    assert exported.loc[edited_indices[-1], "dbh"] == 42
    unchanged = source.index != edited_indices[-1]
    pd.testing.assert_frame_equal(source.loc[unchanged], exported.loc[unchanged])
    assert source[["latitude", "longitude"]].isna().any(axis=1).sum() == 125
    assert (chapter / "trees.csv").read_bytes() == source_bytes


def test_model_schema_and_reproducible_predictions():
    data = pd.read_csv(ROOT / "penguin_ml/penguins.csv").dropna()
    model, species, score = train_model(data)
    other, other_species, other_score = train_model(data)
    features = encode_features(data)
    assert list(features.columns) == list(model.feature_names_in_)
    assert list(encode_features(data.iloc[:1]).columns) == list(features.columns)
    assert len(features.columns) == 9
    np.testing.assert_array_equal(model.predict(features), other.predict(features))
    assert list(species) == list(other_species)
    assert score == other_score and 0 <= score <= 1
    uppercase = data.iloc[:1].copy()
    uppercase["sex"] = uppercase["sex"].str.upper()
    pd.testing.assert_frame_equal(encode_features(uppercase), encode_features(data.iloc[:1]))


@pytest.mark.parametrize("column,value", [("island", "Unknown"), ("sex", "unknown"), ("sex", 1), ("body_mass_g", -1), ("bill_depth_mm", float("inf"))])
def test_model_rejects_invalid_measurements(column, value):
    data = pd.read_csv(ROOT / "penguin_ml/penguins.csv").dropna().iloc[:1].copy()
    data[column] = value
    with pytest.raises(ValueError):
        encode_features(data)


def test_training_export_is_separate_from_original_artifacts(tmp_path):
    originals = list((ROOT / "penguin_ml").glob("*.pickle"))
    before = {p: p.read_bytes() for p in originals}
    output = tmp_path / "model"
    subprocess.run([sys.executable, str(ROOT / "penguin_ml/penguins_ml.py"), "--output-dir", str(output)], check=True, capture_output=True)
    metadata = json.loads((output / "metadata.json").read_text())
    assert len(metadata["features"]) == 9
    assert (output / "feature_importance.png").stat().st_size > 0
    assert len(list(output.glob("*.pickle"))) == 2
    assert all(p.read_bytes() == content for p, content in before.items())


def test_ml_form_uses_cached_training(app, monkeypatch):
    # The app imports this chapter-local name; count real training calls.
    monkeypatch.syspath_prepend(str(ROOT / "penguin_ml"))
    import penguins_ml
    original = penguins_ml.train_model
    calls = []
    def train(data):
        calls.append(1)
        return original(data)
    monkeypatch.setattr(penguins_ml, "train_model", train)
    at = app("penguin_ml/penguins_streamlit.py")
    at.text_input[0].set_value("streamlit_is_great").run()
    at.selectbox[0].set_value("Torgersen")
    at.button[0].click().run()
    assert not at.exception
    assert len(calls) == 1
    assert at.success or any("predict" in m.value.lower() for m in at.markdown)
