"""Train the chapter's classifier reproducibly; run this file to export new artifacts."""
from pathlib import Path
import argparse
import json
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

NUMERIC = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
ISLANDS = ["Biscoe", "Dream", "Torgersen"]
SEXES = ["female", "male"]


def encode_features(data):
    """Use the same category order even when an uploaded sample lacks a category."""
    required = NUMERIC + ["island", "sex"]
    missing = set(required) - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    features = data[required].copy()
    features["sex"] = features["sex"].astype("string").str.lower()
    for column, values in [("island", ISLANDS), ("sex", SEXES)]:
        if not features[column].isin(values).all():
            raise ValueError(f"{column} must contain only {values}")
        features[column] = pd.Categorical(features[column], categories=values)
    for column in NUMERIC:
        features[column] = pd.to_numeric(features[column], errors="raise")
    if not np.isfinite(features[NUMERIC].to_numpy(dtype=float)).all():
        raise ValueError("Measurements must be finite numbers.")
    if (features[NUMERIC] <= 0).any().any():
        raise ValueError("Measurements must be greater than zero.")
    return pd.get_dummies(features, dtype=int)


def train_model(data):
    required = NUMERIC + ["island", "sex", "species"]
    missing = set(required) - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    clean = data.dropna(subset=required)
    counts = clean["species"].value_counts()
    if len(counts) < 2 or counts.min() < 5:
        raise ValueError("Provide at least two species with five complete rows each.")
    features = encode_features(clean)
    output, species = pd.factorize(clean["species"], sort=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features, output, test_size=0.2, random_state=15, stratify=output
    )
    model = RandomForestClassifier(random_state=15)
    model.fit(x_train, y_train)
    score = accuracy_score(y_test, model.predict(x_test))
    return model, species, score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "generated")
    args = parser.parse_args()
    data = pd.read_csv(Path(__file__).resolve().parent / "penguins.csv")
    model, species, score = train_model(data)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Only load artifacts you trust, with the same library versions used to train them.
    with (args.output_dir / "random_forest_penguin.pickle").open("wb") as output:
        pickle.dump(model, output)
    with (args.output_dir / "output_penguin.pickle").open("wb") as output:
        pickle.dump(species, output)
    (args.output_dir / "metadata.json").write_text(json.dumps({
        "sklearn": sklearn.__version__, "pandas": pd.__version__,
        "features": model.feature_names_in_.tolist(), "accuracy": score,
    }, indent=2))
    fig, ax = plt.subplots()
    sns.barplot(x=model.feature_importances_, y=model.feature_names_in_, ax=ax)
    ax.set(title="Which features predict species?", xlabel="Importance")
    fig.tight_layout()
    fig.savefig(args.output_dir / "feature_importance.png")
    plt.close(fig)
    print(f"Held-out accuracy: {score:.3f}; artifacts written to {args.output_dir}")
