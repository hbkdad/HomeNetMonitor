import json
from datetime import datetime

# Simulated scan output
scan_output = {
    "devices": [
        {"ip": "192.168.2.1", "mac": "AA:BB:CC:DD:EE:FF", "hostname": "Router"},
        {"ip": "192.168.2.10", "mac": "11:22:33:44:55:66", "hostname": "Laptop"}
    ],
    "bandwidth": {
        "upload_kbps": 42.5,
        "download_kbps": 84.3,
        "timestamp": str(datetime.now())
    }
}

with open("scan_output.json", "w") as f:
    json.dump(scan_output, f, indent=2)

print("✅ Scan complete: scan_output.json updated")
