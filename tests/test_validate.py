"""Tests for validation logic."""
from src.validate import check_subtotal


def test_subtotal_passes_when_sum_matches():
    result = check_subtotal(
        name="Test",
        components=[100, 200, 300],
        stated_total=600,
    )
    assert result.passed
    assert result.actual == 600


def test_subtotal_fails_when_sum_mismatches():
    result = check_subtotal(
        name="Test",
        components=[100, 200, 300],
        stated_total=999,
    )
    assert not result.passed


def test_real_balance_sheet_consistency():
    """Coca-Cola 1975 current liabilities should sum to stated total."""
    result = check_subtotal(
        name="Current liabilities 1975",
        components=[21909567, 1723791, 266539348, 149777010],
        stated_total=439949716,
    )
    assert result.passed