"""Validation utilities for cargo hold operations."""

import re
from config import (
    BAY_NAME_MAX_LENGTH,
    BAY_NAME_PATTERN,
    MIN_STOW_WEIGHT,
    MAX_STOW_WEIGHT,
    VALID_BAY_KINDS,
)


def validate_bay_name(name):
    """Validate a bay name.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not isinstance(name, str):
        return False, "bay name must be a string"
    if not name:
        return False, "bay name must not be empty"
    if len(name) > BAY_NAME_MAX_LENGTH:
        return False, f"bay name too long (max {BAY_NAME_MAX_LENGTH})"
    if not re.match(BAY_NAME_PATTERN, name):
        return False, "bay name must match pattern: uppercase letters, digits, hyphens"
    return True, ""


def validate_weight(weight):
    """Validate a stow weight.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not isinstance(weight, (int, float)):
        return False, "weight must be a number"
    if weight <= 0:
        return False, "weight must be positive"
    if weight < MIN_STOW_WEIGHT:
        return False, f"weight below minimum ({MIN_STOW_WEIGHT})"
    if weight > MAX_STOW_WEIGHT:
        return False, f"weight exceeds maximum ({MAX_STOW_WEIGHT})"
    return True, ""


def validate_bay_kind(kind):
    """Validate a bay kind value.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if kind not in VALID_BAY_KINDS:
        valid = ", ".join(sorted(VALID_BAY_KINDS))
        return False, f"invalid bay kind {kind!r}; valid: {valid}"
    return True, ""


def validate_stow_data(dest_name, source_name, weight):
    """Validate complete stow data.

    Returns:
        Tuple of (is_valid, errors list).
    """
    errors = []
    valid, msg = validate_bay_name(dest_name)
    if not valid:
        errors.append(f"dest: {msg}")
    valid, msg = validate_bay_name(source_name)
    if not valid:
        errors.append(f"source: {msg}")
    valid, msg = validate_weight(weight)
    if not valid:
        errors.append(f"weight: {msg}")
    if dest_name == source_name:
        errors.append("dest and source must be different")
    return len(errors) == 0, errors


def validate_steps(steps):
    """Validate a list of stow steps.

    Returns:
        Tuple of (is_valid, errors list).
    """
    errors = []
    if not steps:
        errors.append("steps must not be empty")
        return False, errors
    for i, step in enumerate(steps):
        if len(step) != 3:
            errors.append(f"step {i}: must have 3 elements (source, dest, weight)")
            continue
        source_name, dest_name, weight = step
        valid, step_errors = validate_stow_data(dest_name, source_name, weight)
        if not valid:
            for err in step_errors:
                errors.append(f"step {i}: {err}")
    return len(errors) == 0, errors
