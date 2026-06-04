from pathlib import Path

from palisade import config


def test_configure_dev(monkeypatch):
    monkeypatch.setattr(config, "_dev", False)
    monkeypatch.setattr(config, "_paths", config._PROD_PATHS)
    config.configure(dev=True)
    assert config.is_dev() is True
    assert config.db_path() == Path("/tmp/palisade_dev.db")
    assert config.socket_path() == Path("/tmp/palisade_dev.sock")


def test_configure_prod(monkeypatch):
    monkeypatch.setattr(config, "_dev", True)
    monkeypatch.setattr(config, "_paths", config._DEV_PATHS)
    config.configure(dev=False)
    assert config.is_dev() is False
    assert config.db_path() == Path("/var/lib/palisade/palisade.db")
    assert config.hosts_path() == Path("/etc/hosts")
