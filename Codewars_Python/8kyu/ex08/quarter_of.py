def quarter_of(month):
    if month < 1 or month > 12:
        raise ValueError("Invalid month")
    elif month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4