# Installation & Setup Steps

## Student 1 — Infrastructure Setup

### Environment
- **Host Machine:** Apple MacBook (Apple M4 chip)
- **RAM:** 32GB
- **VM Software:** UTM (VirtualBox not supported on Apple Silicon)
- **Guest OS:** Kali Linux 2025.4 ARM64

---

## Step 1 — Install UTM

1. Download UTM from: https://mac.getutm.app
2. Open the `.dmg` file
3. Drag UTM to Applications folder
4. Open UTM from Applications

**Why UTM instead of VirtualBox?**
VirtualBox does not support Apple Silicon (M1/M2/M3/M4) chips. UTM is the recommended free alternative for Apple Silicon Macs.

---

## Step 2 — Download Kali Linux ARM64

1. Go to: https://www.kali.org/get-kali/
2. Click **"Installer"** tab
3. Select **"Apple Silicon (ARM64)"** toggle
4. Download the **Installer** (recommended) option
5. File downloaded: `kali-linux-2025.4-installer-arm64.iso`

**Important:** Must select ARM64 version — the x86_64/amd64 version will not work on Apple Silicon and will result in a black screen.

---

## Step 3 — Create Kali Linux VM in UTM

1. Open UTM
2. Click **"Create a New Virtual Machine"**
3. Select **"Virtualize"**
4. Select **"Linux"**
5. Boot Image: Browse and select `kali-linux-2025.4-installer-arm64.iso`
6. Hardware settings:
   - Memory: 4096 MiB (4GB)
   - CPU Cores: 4
   - OpenGL Acceleration: OFF
7. Storage: 64 GB
8. Shared Directory: Skip
9. Name: `Kali-Linux`
10. Click **Save**

---

## Step 4 — Install Kali Linux

1. Start the VM in UTM
2. Select **"Graphical Install"** from GRUB menu
3. Follow the installer:
   - Language: English
   - Location: Your country
   - Keyboard: Your layout
   - Hostname: `kali`
   - Username: `kali`
   - Password: `kali`
   - Partitioning: Guided - use entire disk
4. Wait for installation to complete (~15 minutes)
5. Reboot when prompted

---

## Step 5 — Configure Network Settings

1. Boot into Kali Linux
2. Open terminal
3. Check network connectivity:
```bash
ping google.com
```
4. UTM default network (NAT) provides internet access automatically

---

## Step 6 — Install Seed Internet Emulator

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip docker.io docker-compose git

# Enable Docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Log out and back in, then clone the repo
git clone https://github.com/seed-labs/seed-emulator.git
cd seed-emulator

# Install Python dependencies
pip3 install seedemu --break-system-packages
```

---

## Step 7 — Run Example Topology

```bash
cd seed-emulator/examples/basic/A00-simple-peering
python3 simple-peering.py
cd output
docker-compose up
```

Open browser and go to: `http://localhost:8080` to view the network map.

---

## What Went Well
- UTM installation was straightforward
- Kali Linux ARM64 downloaded and configured correctly
- Network (NAT) works automatically in UTM
- Seed Emulator cloned successfully

## Issues Encountered
- VirtualBox not compatible with Apple Silicon — switched to UTM
- Initial download was wrong architecture (amd64 instead of arm64)
- Graphical installer had display issues — used text installer instead

## Skills Developed
- Virtual machine configuration on Apple Silicon
- Linux environment setup
- Network configuration basics
- GitHub repository management
- Troubleshooting architecture compatibility issues
