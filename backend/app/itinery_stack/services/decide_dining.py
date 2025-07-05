# decide_dining.py
def choose_dining(weather):
    # Heuristic
    if weather["rain"] or weather["temp"] > 35:
        return "indoor"
    return "outdoor"