### Welcome to Chapter 4: Using Machine Learning with Streamlit

This folder contains the machine learning app created to predict the species of penguin from Palmer's Penguins, and uses some of the libraries declared in the [project environment](../pyproject.toml). Follow the [root README setup](../README.md#lab-setup-uv) and run `uv sync` from the repository root before starting this chapter.
Run `uv run streamlit run penguin_ml/penguins_streamlit.py` from the repository root.
The app displays its teaching password; no secret is required for local prediction.
This gate illustrates control flow and is not secure authentication. Training uses
current scikit-learn with fixed features and seeds, and is cached across reruns.
Run `uv run python penguin_ml/penguins_ml.py` to export new artifacts under
`penguin_ml/generated/`; the original historical pickles are preserved but unused.
For real service-secret handling, see the database/NLP stops in the
[walkthrough](../walkthrough.md).
If you think there is a problem with this code, please [open an issue or pull request](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/working-with-your-remote-repository-on-github-or-github-enterprise/creating-an-issue-or-pull-request) or just find me on [Twitter](https://www.twitter.com/tylerjrichards) and DM me! 
