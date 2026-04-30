from datetime import date, timedelta


def parse_date(message: str) -> str:
    text = message.lower()

    today = date.today()

    if "ontem" in text:
        return (today - timedelta(days=1)).isoformat()

    if "hoje" in text:
        return today.isoformat()

    return today.isoformat()