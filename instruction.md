There is an Apache-style access log at /app/access.log. Analyze it and write a JSON summary report to /app/report.json.

Your report must satisfy the following criteria:

1. total_requests - an integer count of all non-empty log lines.
2. unique_ips - an integer count of distinct client IP addresses.
3. top_path - a string with the most frequently requested path (as it appears after the HTTP method in the request line).

Example output:
{"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}