
def convert_to_minutes(time: list[int]):
    # [9,20] => 560
    minutes = time[0] * 60 + time[1]
    return minutes


def convert_to_readable_time(time_in_munutes):
    # не доработано
    time(time_in_munutes).strftime(time_format)