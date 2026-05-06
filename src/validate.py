"""Validate extracted financial data against accounting identities."""
from dataclasses import dataclass


@dataclass
class ValidationResult:
    check_name: str
    expected: int
    actual: int

    @property
    def passed(self) -> bool:
        return self.expected == self.actual

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (
            f"[{status}] {self.check_name}: "
            f"expected {self.expected:,}, got {self.actual:,}"
        )


def check_subtotal(name: str, components: list[int], stated_total: int) -> ValidationResult:
    """Check that a list of values sums to a stated subtotal."""
    return ValidationResult(
        check_name=name,
        expected=stated_total,
        actual=sum(components),
    )