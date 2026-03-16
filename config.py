"""Configuration constants for the cargo hold system."""

# Bay kinds
STANDARD_BAY = "standard"
OVERFLOW_BAY = "overflow"
REFRIGERATED_BAY = "refrigerated"
HAZMAT_BAY = "hazmat"

VALID_BAY_KINDS = {STANDARD_BAY, OVERFLOW_BAY, REFRIGERATED_BAY, HAZMAT_BAY}

# Weight limits (metric tons)
MAX_BAY_LOAD = 10000
MIN_STOW_WEIGHT = 1
MAX_STOW_WEIGHT = 5000

# Formatting
WEIGHT_PRECISION = 2
DEFAULT_SEPARATOR = " | "
HEADER_WIDTH = 60

# Bay naming conventions
BAY_NAME_MAX_LENGTH = 32
BAY_NAME_PATTERN = r"^[A-Z][A-Z0-9\-]*$"

# Log settings
MAX_LOG_DISPLAY = 100
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Export formats
EXPORT_CSV = "csv"
EXPORT_JSON = "json"
EXPORT_TEXT = "text"
VALID_EXPORT_FORMATS = {EXPORT_CSV, EXPORT_JSON, EXPORT_TEXT}

# Analysis thresholds
BALANCE_TOLERANCE = 0.05
OVERLOAD_WARNING_RATIO = 0.85
CRITICAL_LOAD_RATIO = 0.95
