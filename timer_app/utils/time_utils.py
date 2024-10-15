def format_time(seconds):
    """Format time as HH:MM if more than 1 hour, else MM:SS or SS."""
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}min"
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)}min {int(seconds):02}sec"

def format_time_compact(seconds):
    """Format time in compact style: '1h45'."""
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h{int(minutes):02}"
    minutes = seconds // 60
    return f"{int(minutes)}min"