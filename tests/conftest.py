from pathlib import Path
import sys

import pytest
import requests
import streamlit as st
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def offline_and_isolated(monkeypatch, tmp_path):
    # Running elsewhere catches accidental working-directory-relative data access.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    def offline(*args, **kwargs):
        raise requests.ConnectionError("Offline regression test")
    monkeypatch.setattr(requests.sessions.Session, "request", offline)
    st.cache_data.clear()
    st.cache_resource.clear()
    yield
    st.cache_data.clear()
    st.cache_resource.clear()


@pytest.fixture
def app():
    def load(path):
        at = AppTest.from_file(str(ROOT / path), default_timeout=30)
        # An empty mapping would fall back to the user's real global secrets.
        at.secrets = {"TEST_WITHOUT_CREDENTIALS": True}
        return at.run()
    return load
