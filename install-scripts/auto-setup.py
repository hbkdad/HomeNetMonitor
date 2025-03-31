#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

def run(command, cwd=None):
    print(f"▶️ {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Failed: {command}")
        sys.exit(1)

def check_and_install_package(pkg):
    print(f"📦 Ensuring {pkg} is installed...")
    subprocess.run(f"sudo apt-get install -y {pkg}", shell=True)

def main():
    print("🚀 Starting Auto Setup for Home Network Monitor (Kali Linux)")

    # Install system dependencies
    check_and_install_package("python3-venv")
    check_and_install_package("nmap")
    check_and_install_package("nodejs")
    check_and_install_package("npm")

    # Create virtual environment
    if not os.path.exists("venv"):
        print("🛠 Creating Python virtual environment...")
        run("python3 -m venv venv")

    # Activate virtualenv & install Python packages
    pip = "./venv/bin/pip"
    run(f"{pip} install --upgrade pip")
    run(f"{pip} install fastapi uvicorn psutil python-nmap netifaces")

    # Setup React frontend
    frontend_dir = "frontend"
    if os.path.exists(frontend_dir):
        print("🧼 Removing old frontend folder...")
        shutil.rmtree(frontend_dir)

    print("⚛️ Creating new React frontend...")
    run("npx create-react-app frontend")

    # Replace App.js with custom dashboard
    app_js_path = os.path.join(frontend_dir, "src", "App.js")
    dashboard_code = """import React, { useEffect, useState } from 'react';

function App() {
  const [devices, setDevices] = useState([]);
  const [bandwidth, setBandwidth] = useState({});

  useEffect(() => {
    const host = window.location.hostname;
    fetch(`http://${host}:8000/devices`)
      .then(res => res.json())
      .then(data => setDevices(data.devices));

    fetch(`http://${host}:8000/bandwidth`)
      .then(res => res.json())
      .then(data => setBandwidth(data.bandwidth));

    const interval = setInterval(() => {
      fetch(`http://${host}:8000/devices`)
        .then(res => res.json())
        .then(data => setDevices(data.devices));

      fetch(`http://${host}:8000/bandwidth`)
        .then(res => res.json())
        .then(data => setBandwidth(data.bandwidth));
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className='p-4 max-w-3xl mx-auto'>
      <h1 className='text-3xl font-bold mb-4'>📡 Home Network Dashboard</h1>

      <div className='bg-white shadow p-4 rounded-2xl mb-4'>
        <h2 className='text-xl font-semibold mb-2'>📶 Bandwidth</h2>
        <p><strong>Download:</strong> {bandwidth.download_kbps || 0} kbps</p>
        <p><strong>Upload:</strong> {bandwidth.upload_kbps || 0} kbps</p>
        <p className='text-xs text-gray-500 mt-2'>Updated: {bandwidth.timestamp || "N/A"}</p>
      </div>

      <div className='bg-white shadow p-4 rounded-2xl'>
        <h2 className='text-xl font-semibold mb-2'>🔍 Devices on Network</h2>
        <ul className='divide-y divide-gray-200'>
          {devices.map((device, index) => (
            <li key={index} className='py-2'>
              <p><strong>IP:</strong> {device.ip}</p>
              <p><strong>MAC:</strong> {device.mac}</p>
            </li>
          ))}
        </ul>
        {devices.length === 0 && <p className='text-gray-500'>No devices found.</p>}
      </div>
    </div>
  );
}

export default App;"""
    os.makedirs(os.path.dirname(app_js_path), exist_ok=True)
    with open(app_js_path, "w") as f:
        f.write(dashboard_code)

    print("✅ Setup complete.")
    print("👉 Now run the following in 3 terminals:")
    print("  1. source venv/bin/activate && cd backend && uvicorn main:app --host 0.0.0.0 --port 8000")
    print("  2. source venv/bin/activate && cd agent && python3 scanner.py")
    print("  3. cd frontend && npm start")

if __name__ == "__main__":
    main()
