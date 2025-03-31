import React, { useState, useEffect } from "react";

function App() {
  const [devices, setDevices] = useState([]);
  const [bandwidth, setBandwidth] = useState({});
  const [history, setHistory] = useState([]);
  const [traffic, setTraffic] = useState({});
  const [pingHost, setPingHost] = useState("");
  const [pingResult, setPingResult] = useState("");

  const API = `http://${window.location.hostname}:8000`;

  const fetchData = async () => {
    try {
      const resDevices = await fetch(`${API}/devices`);
      const resBandwidth = await fetch(`${API}/bandwidth`);
      const resHistory = await fetch(`${API}/history`);
      const resTraffic = await fetch(`${API}/traffic`);

      const dataDevices = await resDevices.json();
      const dataBandwidth = await resBandwidth.json();
      const dataHistory = await resHistory.json();
      const dataTraffic = await resTraffic.json();

      setDevices(dataDevices.devices || []);
      setBandwidth(dataBandwidth.bandwidth || {});
      setHistory(dataHistory || []);
      setTraffic(dataTraffic || {});
    } catch (err) {
      console.error("Error fetching data", err);
    }
  };

  const handlePing = async () => {
    try {
      const res = await fetch(`${API}/ping?host=${pingHost}`);
      const data = await res.json();
      setPingResult(data.result || data.error || "No response");
    } catch (err) {
      setPingResult("Ping failed");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">📡 HomeNetMonitor Dashboard</h1>

      {/* 📶 Bandwidth */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">📶 Bandwidth</h2>
        <p>Download: {bandwidth.download_kbps || 0} kbps</p>
        <p>Upload: {bandwidth.upload_kbps || 0} kbps</p>
        <p>Updated: {bandwidth.timestamp || "N/A"}</p>
      </div>

      {/* 🌐 Live Traffic */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">🌐 Live Network Traffic</h2>
        <p>Bytes Sent: {traffic.bytes_sent || 0}</p>
        <p>Bytes Received: {traffic.bytes_recv || 0}</p>
        <p>Updated: {traffic.timestamp || "N/A"}</p>
      </div>

      {/* 🧪 Ping Test */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">🧪 Ping Test</h2>
        <input
          type="text"
          className="text-black p-2 mr-2 rounded"
          placeholder="Enter host (e.g., google.com)"
          value={pingHost}
          onChange={(e) => setPingHost(e.target.value)}
        />
        <button
          onClick={handlePing}
          className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-700"
        >
          Ping
        </button>
        <pre className="bg-gray-800 p-4 mt-2 rounded text-sm whitespace-pre-wrap">
          {pingResult}
        </pre>
      </div>

      {/* 🔍 Devices */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">🔍 Devices on Network</h2>
        {devices.length > 0 ? (
          <ul className="divide-y divide-gray-200 text-sm">
            {devices.map((device, index) => (
              <li key={index} className="py-2">
                <strong>{device.hostname}</strong> - {device.ip} - {device.mac}
              </li>
            ))}
          </ul>
        ) : (
          <p>No devices found.</p>
        )}
      </div>

      {/* 🗂 History */}
      <div>
        <h2 className="text-xl font-semibold mb-2">🗂 Scan History</h2>
        {history.length > 0 ? (
          <ul className="text-sm space-y-2">
            {history.map((entry, index) => (
              <li key={index}>
                🕒 {entry.timestamp} | Devices: {entry.devices?.length || 0} | ↓{" "}
                {entry.download_kbps} kbps | ↑ {entry.upload_kbps} kbps
              </li>
            ))}
          </ul>
        ) : (
          <p>No history available.</p>
        )}
      </div>
    </div>
  );
}

export default App;
