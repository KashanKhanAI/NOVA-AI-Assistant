from .license import is_pro


FREE_FEATURES = {
    "chat",
    "basic_memory",
    "basic_commands",
}

PRO_FEATURES = {
    "voice",
    "computer_control",
    "file_automation",
    "advanced_memory",
    "custom_commands",
}


def has_feature(feature_name):
    """Check whether the current NOVA plan can use a feature."""
    if feature_name in FREE_FEATURES:
        return True

    if feature_name in PRO_FEATURES:
        return is_pro()

    return False