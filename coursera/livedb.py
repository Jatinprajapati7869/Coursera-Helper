"""
This module previously handled Firebase tracking and telemetry.
All tracking functionality has been removed for privacy.
The functions are kept as stubs to prevent crashes in code that calls them.
"""

# === Authentication ===
def authenticate_anonymously():
    """Stub: Authentication disabled. Returns None."""
    return None

# === check for update ===
def get_latest_version(id_token):
    """Stub: Update checking disabled. Returns None."""
    return None, None, None

def check_for_update(id_token):
    """Stub: Update checking disabled. Returns current version info."""
    from maingui import __version__
    return False, __version__, None, None

# === get notification ===
def get_notification(id_token):
    """Stub: Push notifications disabled. Returns None."""
    return None

# === log_usage_info ===
def log_usage_info(id_token):
    """Stub: Usage logging disabled. Does nothing."""
    pass

def get_set_user_id():
    """Stub: User ID generation disabled. Returns empty string."""
    return ""

def get_country():
    """Stub: Geolocation tracking disabled. Returns 'Unknown'."""
    return "Unknown"

def make_doc_id():
    """Stub: Document ID generation disabled. Returns empty string."""
    return ""

# === Main ===
if __name__ == "__main__":
    print("All tracking and telemetry has been disabled.")
    print("This module now contains only stub functions.")