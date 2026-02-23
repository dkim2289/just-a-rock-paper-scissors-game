import json
import os
import hashlib
import base64

HALL_OF_FAME_FILE = "hall_of_fame.json"
SECRET_KEY = 42

# encode the data using XOR and base64
def encode_data(data):
    # keep the data in json_str as dumping the original data
    json_str = json.dumps(data)
    # jumble it - XOR each character with the secret key
    encoded = ''.join(chr(ord(c) ^ SECRET_KEY) for c in json_str)
    # use base64 to convert the scrambled bytes to safe text and then decode it back to a string
    return base64.b64encode(encoded.encode()).decode()

# decode the data using XOR and base64
def decode_data(encoded_data):
    # decode the base64 encoded string
    decoded = base64.b64decode(encoded_data).decode()
    return json.loads(''.join(chr(ord(c) ^ SECRET_KEY) for c in decoded))

# takes the record, calculatres its checksum, bundles both into a dictionary,
# then passes to encode_data() to scramble it before writing to file.
def save_record(record):
    record_str = json.dumps(record)
    checksum = hashlib.sha256(record_str.encode()).hexdigest()

    data = {
        "record": record,
        "checksum": checksum
    }

    with open(HALL_OF_FAME_FILE, 'w') as f:
        f.write(encode_data(data))

# Reads the scrambled file, passes to decode_data() to unscramble, extracts the record
# and its checksum, verifies the checksum matches, and returns the record
# or default if tampering detected
def load_record():
    default_record = {
        "name": "No Champions Yet",
        "streak": 0
    }

    if not os.path.exists(HALL_OF_FAME_FILE):
        return default_record

    try:
        with open(HALL_OF_FAME_FILE, "r") as f:
            encoded = f.read()
            if not encoded:
                return default_record

            data = decode_data(encoded)

            record_str = json.dumps(data["record"])
            expected = hashlib.sha256(record_str.encode()).hexdigest()

            if expected == data["checksum"]:
                return data["record"]
            else:
                return default_record

    except:
        return default_record
