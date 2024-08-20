
def ConvertSeconds(value):
    """
    Function convert seconds into days, hours, minutes and seconds 

    Args:
        seconds (float): time in seconds with type float

    Returns:
        string: time in days, hours, minutes and seconds 
    """

    days = value // (24 * 3600)

    value = value % (24 * 3600)
    hours = value // 3600

    value %= 3600
    minutes = value // 60

    value %= 60
    seconds = value

    time_in_text = f"{int(round(days))} days {int(round(hours))} hours {int(round(minutes))} minutes {int(round(seconds))} seconds"

    if days <= 1:
        time_in_text = time_in_text.replace("days", "day")
        if hours <= 1:
            time_in_text = time_in_text.replace("hours", "hour")
            if minutes <= 1:
                time_in_text = time_in_text.replace("minutes", "minute")
                if seconds <= 1:
                    time_in_text = time_in_text.replace("seconds", "second")

    return time_in_text

def main():
    ConvertSeconds()

if __name__ == "__main__":
    main()
