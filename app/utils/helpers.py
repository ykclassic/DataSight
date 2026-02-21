def calculate_overlap(series1, series2):
    set1 = set(series1.dropna())
    set2 = set(series2.dropna())

    if not set1 or not set2:
        return 0

    return len(set1 & set2) / min(len(set1), len(set2))
