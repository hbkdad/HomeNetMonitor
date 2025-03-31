#!/bin/bash

echo "📦 Installing backend + agent + frontend dependencies..."

sudo apt update && sudo apt install -y python3 python3-pip nmap net-tools nodejs npm

pip3 install fastapi uvicorn psutil python-nmap

cd frontend
npm install
cd ..

echo "🚀 Starting backend..."
gnome-terminal -- bash -c "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000"

sleep 2
echo "🔍 Starting network scanner..."
gnome-terminal -- bash -c "cd agent && python3 scanner.py"

sleep 2
echo "🌐 Starting frontend..."
gnome-terminal -- bash -c "cd frontend && npm start"
