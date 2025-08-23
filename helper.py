def to_hours_minutes(minutes):
    hours = 0
    minutes = minutes

    while (minutes >= 60):
        hours += 1
        minutes -= 60

    if hours == 0:
        return f"{minutes}m"
    else:
        return f"{hours}h {minutes}m"