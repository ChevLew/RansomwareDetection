import json

INPUT_FILE = "data/MarcusCarpenterDataset/benign.json"
LOOKUP_FILE = "data/MarcusCarpenterDataset/lookup_table.json"
OUTPUT_FILE = "data/processed/Sequence/MCBenign.json"

# Load dataset
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Load lookup table
with open(LOOKUP_FILE, "r", encoding="utf-8") as f:
    lookup_data = json.load(f)

lookup = lookup_data

# Find label indexe
benign_index = lookup.index("benign")
ransomware_index = lookup.index("ransomware")

output = []

# Extract API sequence
for api_sequence, label_vector in zip(data["apis"], data["labels"]):

    if (
        label_vector[benign_index] == 1
        or label_vector[ransomware_index] == 1
    ):
        output.append(api_sequence)

# Out file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print(f"Extracted {len(output)} API sequences")
print(f"Saved to {OUTPUT_FILE}")