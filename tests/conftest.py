import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest


@pytest.fixture(scope="session")
def qapp():
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication([])


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    from palisade import config

    db = tmp_path / "test.db"
    monkeypatch.setattr(config, "db_path", lambda: db)
    monkeypatch.setattr(config, "is_dev", lambda: True)

    from palisade.db.database import init_db

    init_db()
    return db
