import re
from datetime import date, datetime, timedelta


def _parse_explicit_date(text: str) -> str | None:
    iso_match = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", text)
    if iso_match:
        try:
            return date.fromisoformat(iso_match.group(0)).isoformat()
        except ValueError:
            return None

    br_match = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b", text)
    if br_match:
        day, month, year = br_match.groups()
        if len(year) == 2:
            year = f"20{year}"

        try:
            return datetime(int(year), int(month), int(day)).date().isoformat()
        except ValueError:
            return None

    return None


def parse_date(message: str) -> str:
    text = message.lower()

    today = date.today()

    explicit_date = _parse_explicit_date(text)
    if explicit_date:
        return explicit_date

    if "anteontem" in text:
        return (today - timedelta(days=2)).isoformat()

    if "ontem" in text:
        return (today - timedelta(days=1)).isoformat()

    if "hoje" in text:
        return today.isoformat()

    return today.isoformat()
