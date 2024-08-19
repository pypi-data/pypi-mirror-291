import pytest
from clipboard_processor.plugins.oui import OuiPlugin


@pytest.mark.full_installation
@pytest.mark.parametrize('input_data, expected_output', [
    ('c0:3c:59:12:34:56', ['Intel Corporate (C0-3C-59)']),
    ('c0-3c-59-12-34-56', ['Intel Corporate (C0-3C-59)']),
    ('c03c59123456', ['Intel Corporate (C0-3C-59)']),
    ('c0-3c-59', ['Intel Corporate (C0-3C-59)']),
    ('c03c59', ['Intel Corporate (C0-3C-59)']),
    ('c0:3c:59', ['Intel Corporate (C0-3C-59)']),
    ('01:23:45', []),  # not registered
    ('c0/3c/59', []),  # invalid format
    ('c03c', []),  # invalid format
    ('c03c5912345', []),  # invalid format
    ('c03c591234567', []),  # invalid format
    ('c03c5912345600', []),  # invalid format
    ('c03c59_', []),  # invalid format
    ('0c03c59', []),  # invalid format
])
def test_oui(input_data, expected_output):
    assert OuiPlugin().process(input_data) == expected_output


@pytest.mark.full_installation
def test_is_available():
    assert OuiPlugin.is_available() is True


@pytest.mark.minimal_installation
def test_is_not_available():
    assert OuiPlugin.is_available() is False
