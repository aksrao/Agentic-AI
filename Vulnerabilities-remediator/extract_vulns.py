import json
import argparse
import os
import sys

parser = argparse.ArgumentParser(
    description="Extract vulnerabilities from Trivy report by severity"
)


parser.add_argument(
    "--severity",
    required=True,
    choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
    help="Severity level to extract"
)
parser.add_argument(
    "--input",
    default="./data/fullstack-report.json",
    help="Path to Trivy report JSON"
)
args = parser.parse_args()

severity_filter = args.severity.upper()
input_file = args.input

with open("./data/fullstack-report.json") as f:
    report = json.load(f)


filtered_vulns = []

for result in report.get("Results", []):
    vulns = result.get("Vulnerabilities")
    if not vulns:
        continue

    for v in vulns:
        if v.get("Severity") == severity_filter:
            filtered_vulns.append({
                "title": v.get("Title"),
                "cve": v.get("VulnerabilityID"),
                "package": v.get("PkgName"),
                "severity": v.get("Severity"),
                "installed_version": v.get("InstalledVersion"),
                "fixed_version": v.get("FixedVersion"),
                "description": v.get("Description"),
                "dataSource": v.get("DataSource")
            })

output_filename = f"{severity_filter.lower()}_vulns.json"
with open(output_filename, "w") as f:
    json.dump(filtered_vulns, f, indent=2)

print(f"✅ Extracted {len(filtered_vulns)} {severity_filter} vulnerabilities")
print(f"📄 Output written to: {output_filename}")