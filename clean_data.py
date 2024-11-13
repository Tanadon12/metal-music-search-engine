# import json

# # Convert a JSON array to NDJSON
# def convert_to_ndjson(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as infile:
#         data = json.load(infile)  # Load as a list of JSON objects

#     with open(output_file, 'w', encoding='utf-8') as outfile:
#         for item in data:
#             json.dump(item, outfile)
#             outfile.write('\n')  # Write each JSON object in a new line

# # Convert songs.json to NDJSON
# convert_to_ndjson('songs.json', 'songs.ndjson')

# print("Converted songs.json to NDJSON format as songs.ndjson")

import ndjson
from collections import OrderedDict

def update_ndjson(input_file, output_file):
    # Open and read the input NDJSON file
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = ndjson.load(infile)  # Load as a list of JSON objects

    # Update each record
    updated_data = []
    for record in data:
        # Remove "Song Query"
        record.pop("Song Query", None)

        # Rename "Track Name" to "Song Name"
        if "Track Name" in record:
            record["Song Name"] = record.pop("Track Name")

        # Reorder keys: Place "Song Name" at the front
        ordered_record = OrderedDict()
        ordered_record["Song Name"] = record.get("Song Name", "Unknown Song")
        for key, value in record.items():
            if key != "Song Name":  # Skip since it's already added at the front
                ordered_record[key] = value

        updated_data.append(ordered_record)

    # Write updated data to a new NDJSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        ndjson.dump(updated_data, outfile)

    print(f"Updated NDJSON saved to {output_file}")

# Input and output file paths
input_file = 'songs-bulk.ndjson'    # Replace with your actual file path
output_file = 'updated_songs.ndjson'

# Run the function
update_ndjson(input_file, output_file)
