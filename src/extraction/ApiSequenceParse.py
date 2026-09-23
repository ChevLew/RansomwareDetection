import json
import glob
import os, re


def get_api_sequence(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    api_sequence = data.get("api_sequence", [])

    sequence = []

    for entry in api_sequence:
        if "->" in entry:
            api = entry.split("->", 1)[1].strip()
            sequence.append(api)

    return sequence


# Process all reports
all_sequences = []

for json_file in glob.glob("data/RansomwareReports/*.json"):

    filename = os.path.basename(json_file)
    report_id = re.match(r"(\d+)report\.json", filename).group(1)

    sequence = get_api_sequence(json_file)
    sequence = ["1", report_id] + sequence

    all_sequences.append(sequence)


with open("sequences.json", "w", encoding="utf-8") as f:
    json.dump(all_sequences, f, indent=2)