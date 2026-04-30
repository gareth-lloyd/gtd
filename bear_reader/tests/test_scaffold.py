"""Smoke test: app is installable and importable."""

from django.apps import apps


def test_app_is_installed():
    assert apps.is_installed("bear_reader")


def test_package_imports():
    import bear_reader  # noqa: F401
