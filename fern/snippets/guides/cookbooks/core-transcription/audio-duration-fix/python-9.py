def durations_are_consistent(durations, tolerance=0.01):
    #Check if durations are consistent within a given tolerance of 0.01 seconds.
    if None in durations:
        return False
    min_duration = min(durations)
    max_duration = max(durations)
    return (max_duration - min_duration) <= tolerance
