"""
JSON Payload Sanitizer converting NumPy types (np.int64, np.float64, np.ndarray) to native Python types
"""

import numpy as np

def sanitize_json_payload(obj):
    """
    Recursively converts NumPy data types into standard Python types for JSON serialization.
    Checks boolean types FIRST to prevent bool subclass of int conversion.
    """
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return [sanitize_json_payload(x) for x in obj.tolist()]
    elif isinstance(obj, dict):
        return {str(k): sanitize_json_payload(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_json_payload(x) for x in obj]
    return obj
