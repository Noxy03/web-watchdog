# 🕵️‍♂️ WebWatchdog
A lightweight Python script to monitor website changes and receive detailed "diff" notifications via Discord. Optimized for running 24/7 on old Android devices via Termux.

## ✨ Features
* **Text-only Monitoring**: Ignores headers, footers, and scripts to reduce false alarms.
* **Smart Diffs**: Sends exactly what changed (added/removed lines) to Discord.
* **Persistent**: Built-in support for autostarting on Android/Termux.
* **Low Resource**: Extremely light on CPU and battery.

## 🛠 Installation (Android/Termux)
Follow these steps to turn your old phone into a monitoring server:

### 1. Setup Environment
```bash
pkg update && pkg upgrade
pkg install python openssh nano screen
pip install requests beautifulsoup4
```

### 2. Configure SSH (Optional but Recommended)
To manage the script from your PC:
```bash
passwd
sshd
```
Connect via: ssh <user>@<ip> -p 8022.

### 3. Deploy the Script
Clone this repo or create the file: nano monitor.py
Add your URLs: nano urls.txt 
Add your Discord Webhook URL inside monitor.py.

### 4. Run in Background
```bash
nohup python monitor.py > watchdog.log 2>&1 &
```

## 🔄 Autostart on Boot
To ensure the script starts when the phone reboots:

1. Install Termux:Boot app.
2. Create the boot directory: mkdir -p ~/.termux/boot
3. Create the start script: nano ~/.termux/boot/start-watchdog.sh
4. Add the following:
```bash
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
sshd
nohup python ~/monitor.py > ~/log.txt 2>&1 &
```
5. Make it executable: chmod +x ~/.termux/boot/start-watchdog.sh

## 🛑 Stopping the Script
To stop the monitor:
```bash
pkill python
```

## 📜 License
MIT License - Feel free to use and modify!
