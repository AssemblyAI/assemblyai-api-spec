def sliding_window(elements, distance, stride):
    """Create sliding windows of elements"""
    idx = 0
    results = []
    while idx + distance < len(elements):
        results.append(elements[idx:idx + distance])
        idx += (distance - stride)
    return results
