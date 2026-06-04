from palisade.gui.widgets import app_picker
from palisade.gui.widgets.app_picker import (
    _discover_installed_apps,
    _exec_basename,
    _parse_desktop_file,
)


def test_exec_basename_strips_path_and_field_codes():
    assert _exec_basename("/usr/bin/firefox %u") == "firefox"
    assert _exec_basename("code --new-window %F") == "code"
    assert _exec_basename("/opt/app/bin/foo") == "foo"
    assert _exec_basename("") == ""


def _write_desktop(path, **entries):
    body = "[Desktop Entry]\n" + "".join(f"{k}={v}\n" for k, v in entries.items())
    path.write_text(body, encoding="utf-8")
    return path


def test_parse_desktop_file_application(tmp_path):
    fp = _write_desktop(
        tmp_path / "discord.desktop",
        Type="Application",
        Name="Discord",
        Exec="/usr/bin/discord %U",
        Icon="discord",
    )
    app = _parse_desktop_file(fp)
    assert app is not None
    assert app.name == "Discord"
    assert app.exec_name == "discord"


def test_parse_desktop_file_skips_nodisplay_hidden_and_non_app(tmp_path):
    nodisplay = _write_desktop(
        tmp_path / "a.desktop", Type="Application", Name="A", NoDisplay="true"
    )
    hidden = _write_desktop(
        tmp_path / "b.desktop", Type="Application", Name="B", Hidden="true"
    )
    link = _write_desktop(tmp_path / "c.desktop", Type="Link", Name="C")
    noname = _write_desktop(tmp_path / "d.desktop", Type="Application")
    assert _parse_desktop_file(nodisplay) is None
    assert _parse_desktop_file(hidden) is None
    assert _parse_desktop_file(link) is None
    assert _parse_desktop_file(noname) is None


def test_discover_dedupes_by_exec_name(tmp_path, monkeypatch):
    _write_desktop(
        tmp_path / "x1.desktop", Type="Application", Name="X One", Exec="/usr/bin/x"
    )
    _write_desktop(
        tmp_path / "x2.desktop", Type="Application", Name="X Two", Exec="/usr/bin/x"
    )
    monkeypatch.setattr(app_picker, "XDG_APP_DIRS", [tmp_path])
    apps = _discover_installed_apps()
    assert [a.exec_name for a in apps] == ["x"]
