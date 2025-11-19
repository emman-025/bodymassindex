def pounds_to_kg(pounds):
    return round(pounds * 0.453592, 2)

def feet_inches_to_meters(feet, inches):
    total_inches = feet * 12 + inches
    return round(total_inches * 0.0254, 2)

def cm_to_meters(cm):
    return round(cm / 100, 2)

def ideal_weight_range(height_m):
    min_wt = 18.5 * (height_m ** 2)
    max_wt = 24.9 * (height_m ** 2)
    return (round(min_wt, 1), round(max_wt, 1))