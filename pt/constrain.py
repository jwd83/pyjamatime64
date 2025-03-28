def constrain(value, min_value, max_value):
    """
    Constrain a value to be within the specified range.

    Args:
        value (float): The value to constrain.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.

    Returns:
        float: The constrained value.
    """
    return max(min(value, max_value), min_value)
