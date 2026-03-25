import pytest
from src.converter import *

# ── Basic tests using fixtures ──────────────────────────────────



def test_freezing_c_to_f(freezing_point):
    # freezing_point is injected from conftest.py
    assert celsius_to_fahrenheit(freezing_point["C"]) == freezing_point["F"]


def test_boiling_c_to_f(boiling_point):
    assert celsius_to_fahrenheit(boiling_point["C"]) == boiling_point["F"]


# ── Parametrize for multiple conversion cases ───────────────────


@pytest.mark.parametrize(
    "c, expected_f",
    [
        (0, 32.0),  # freezing
        (100, 212.0),  # boiling
        (-40, -40.0),  # where C and F are equal
        (37, 98.6),  # body temperature
    ],
)
def test_c_to_f_cases(c, expected_f):
    assert celsius_to_fahrenheit(c) == pytest.approx(expected_f, rel=1e-3)


@pytest.mark.parametrize(
    "f, expected_c",
    [
        (32.0, 0.0),
        (212.0, 100.0),
        (-40.0, -40.0),
        (98.6, 37.0),
    ],
)
def test_f_to_c_cases(f, expected_c):
    assert fahrenheit_to_celsius(f) == pytest.approx(expected_c, rel=1e-3)


@pytest.mark.parametrize(
    "c, expected_k",
    [
        (-273.15, 0),
        (-263.15, 10),
        (3524.85, 3798),
        (-51.15, 222),
    ],
)
def test_c_to_k_cases(c, expected_k):
    assert celsius_to_kelvin(c) == pytest.approx(expected_k, rel=1e-3)


@pytest.mark.parametrize(
    "k, expected_c",
    [
        (0, -273.15),
        (10, -263.15),
        (3798, 3524.85),
        (222, -51.15),
    ],
)
def test_k_to_c_cases(k, expected_c):
    assert kelvin_to_celsius(k) == pytest.approx(expected_c, rel=1e-3)


@pytest.mark.parametrize(
    "value, from_u, to_u, expected_v",
    [
        (100, "C", "F", 212.0),
        (32, "F", "C", 0.0),
        (0, "C", "K", 273.15),
        (0, "K", "K", 0),
        (0, "K", "", -273.15),
    ],
)
def test_conversion_cases(value, from_u, to_u, expected_v):
    assert convert(value, from_u, to_u) == pytest.approx(expected_v, rel=1e-3)


def test_unknown_to_unit():
    # The match argument takes a regular expression
    with pytest.raises(ValueError):
        convert(0, "C", "X")


def test_unknown_from_unit():
    # The match argument takes a regular expression
    with pytest.raises(ValueError):
        convert(0, "X", "C")


# ── Edge cases ──────────────────────────────────────────────────


@pytest.mark.edge
def test_absolute_zero_kelvin():
    assert celsius_to_kelvin(-273.15) == pytest.approx(0.0)


@pytest.mark.edge
def test_below_absolute_zero_raises():
    with pytest.raises(ValueError):
        celsius_to_kelvin(-300)
