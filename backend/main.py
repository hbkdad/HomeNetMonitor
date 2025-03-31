from fastapi import FastAPI
import subprocess, json, os

app = FastAPI()

@app.get("/devices")
def get_devices():
    with open("/usr/local/home-net-monitor/agent/scan_output.json") as f:
        data = json.load(f)
    return {"devices": data.get("devices", [])}

@app.get("/bandwidth")
def get_bandwidth():
    with open("/usr/local/home-net-monitor/agent/scan_output.json") as f:
        data = json.load(f)
    return {"bandwidth": data.get("bandwidth", {})}

@app.get("/traffic")
def get_traffic():
    with open("/usr/local/home-net-monitor/agent/live_traffic.json") as f:
        return json.load(f)

@app.get("/ping")
def ping_host(host: str):
    try:
        output = subprocess.check_output(["ping", "-c", "4", host], stderr=subprocess.STDOUT)
        return {"result": output.decode("utf-8")}
    except subprocess.CalledProcessError as e:
        return {"error": e.output.decode("utf-8")}

