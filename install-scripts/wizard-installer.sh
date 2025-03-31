#!/bin/bash

whiptail --title "HomeNetMonitor Setup Wizard" --msgbox "Welcome to the HomeNetMonitor Installer Wizard!" 10 60

INSTALL_TYPE=$(whiptail --title "Installation Type" --radiolist \
"Choose your setup type:" 15 60 2 \
"default" "Recommended settings (auto)" ON \
"custom" "Customize settings (advanced)" OFF 3>&1 1>&2 2>&3)

USE_AUTOBLOCK="yes"
SCAN_INTERVAL="60"
AUTOSTART_FRONTEND="yes"

if [ "$INSTALL_TYPE" = "custom" ]; then
  if (whiptail --title "Auto-Block Devices" --yesno "Enable auto-blocking of unknown devices?" 10 60); then
    USE_AUTOBLOCK="yes"
  else
    USE_AUTOBLOCK="no"
  fi

  SCAN_INTERVAL=$(whiptail --title "Scan Interval" --inputbox "Enter scan interval in seconds:" 10 60 "$SCAN_INTERVAL" 3>&1 1>&2 2>&3)

  if (whiptail --title "Frontend Autostart" --yesno "Run frontend automatically on boot?" 10 60); then
    AUTOSTART_FRONTEND="yes"
  else
    AUTOSTART_FRONTEND="no"
  fi
fi

# Save config
CONFIG_PATH="/usr/local/home-net-monitor/config.json"
echo "{
  \"auto_block\": \"$USE_AUTOBLOCK\",
  \"scan_interval\": $SCAN_INTERVAL,
  \"frontend_autostart\": \"$AUTOSTART_FRONTEND\"
}" > "$CONFIG_PATH"

# Enable services
systemctl enable homenet-backend
systemctl enable homenet-agent

whiptail --title "Installation Complete" --msgbox "✅ HomeNetMonitor has been configured and is ready to use!" 10 60
