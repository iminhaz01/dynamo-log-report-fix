import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _load_report():
    """Shared helper: loads report.json, failing with a clear message if missing or invalid."""
    if not REPORT_PATH.exists():
        raise AssertionError("no report.json found at /app/report.json")
    try:
        return json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def _expected():
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_total_requests():
    """Verifies instruction.md criterion 1: total_requests is an integer count of all non-empty log lines."""
    actual = _load_report()
    expected = _expected()
    assert actual.get("total_requests") == expected["total_requests"], (
        f"total_requests: expected {expected['total_requests']}, got {actual.get('total_requests')}"
    )


def test_unique_ips():
    """Verifies instruction.md criterion 2: unique_ips is an integer count of distinct client IP addresses."""
    actual = _load_report()
    expected = _expected()
    assert actual.get("unique_ips") == expected["unique_ips"], (
        f"unique_ips: expected {expected['unique_ips']}, got {actual.get('unique_ips')}"
    )


def test_top_path():
    """Verifies instruction.md criterion 3: top_path is the most frequently requested path."""
    actual = _load_report()
    expected = _expected()
    assert actual.get("top_path") == expected["top_path"], (
        f"top_path: expected {expected['top_path']}, got {actual.get('top_path')}"
    )