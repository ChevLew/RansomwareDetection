import json
import csv
from collections import Counter

files = {
    "data/processed/Sequence/MCBenign.json": 0,
    "data/processed/Sequence/MCransomware368.json": 1,
    "data/processed/Sequence/MCransomware389.json": 1
}

samples = []
all_apis = set()

for filename, label in files.items():
    with open(filename, "r") as f:
        data = json.load(f)

    for api_list in data:
        counts = Counter(api_list)
        samples.append((label, counts))
        all_apis.update(counts.keys())

all_apis = sorted(all_apis)

with open("MC_api_counts.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["label", "report_id"] + all_apis)

    for label, counts in samples:
        writer.writerow(
            [label, "MC"] + [counts.get(api, 0) for api in all_apis]
        )

print(f"Created MC_api_counts.csv with {len(samples)} samples.")