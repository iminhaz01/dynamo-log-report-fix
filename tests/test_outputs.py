import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


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


def test_report_exists():
    """The agent produced a report file."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"


def test_report_is_valid_json():
    """The report file contains valid JSON."""
    try:
        json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        assert False, f"report.json is not valid JSON: {e}"


def test_report_values_correct():
    """The report's computed values match the actual log contents."""
    actual = json.loads(REPORT_PATH.read_text())
    expected = _expected()
    assert actual.get("total_requests") == expected["total_requests"], (
        f"total_requests: expected {expected['total_requests']}, got {actual.get('total_requests')}"
    )
    assert actual.get("unique_ips") == expected["unique_ips"], (
        f"unique_ips: expected {expected['unique_ips']}, got {actual.get('unique_ips')}"
    )
    assert actual.get("top_path") == expected["top_path"], (
        f"top_path: expected {expected['top_path']}, got {actual.get('top_path')}"
    )