import glob
import os
import re
import json
import csv
from collections import Counter

reports = []

for json_file in glob.glob("data/RansomwareReports/*.json"):
    filename = os.path.basename(json_file)
    report_id = re.match(r"(\d+)report\.json", filename).group(1)

    with open(json_file) as f:
        sequence = json.load(f)["api_sequence"]

    sequence = [api.split(" -> ")[-1] for api in sequence]

    reports.append((report_id, sequence))

all_api_calls = sorted(set(api for _, sequence in reports for api in sequence))

with open("ransomware_api_counts.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["label", "report_id"] + all_api_calls)

    for report_id, sequence in reports:
        counts = Counter(sequence)
        writer.writerow(
            ["1", report_id] + [counts.get(api, 0) for api in all_api_calls]
        )