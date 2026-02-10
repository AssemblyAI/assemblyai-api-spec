def format_timestamp(seconds):
    """
    Convert seconds to a formatted timestamp string (HH:MM:SS).

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted timestamp string.
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
