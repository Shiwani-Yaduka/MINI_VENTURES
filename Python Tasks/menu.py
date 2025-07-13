import os
import gradio as gr
import secrets
import cv2
import numpy as np
import pywhatkit as pwk
import urllib.request
import subprocess
from twilio.rest import Client

# ===== API Key Setup =====
API_KEY = secrets.token_hex(8)
print(f"\n🔑 Your session API key is: {API_KEY}")
print("Use this API key in the input field to access app features.\n")

# ===== Twilio Config =====
TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH = "YOUR_TWILIO_AUTH"
TWILIO_PHONE = "+160868941"
client = Client(TWILIO_SID, TWILIO_AUTH)

# ===== Haarcascade Download =====
HAAR_PATH = "haarcascade_frontalface_default.xml"
if not os.path.exists(HAAR_PATH):
    url = "https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, HAAR_PATH)

# ===== Command Maps =====
command_map = {
    "🖥 Linux: Show Date": "date",
    "🖥 Linux: Show Calendar": "cal",
    "🖥 Linux: List Files": "ls -lh",
    "🖥 Linux: Current Directory": "pwd",
    "🖥 Linux: Disk Usage": "df -h",
    "🖥 Linux: Check Memory Usage": "free -m",
    "🖥 Linux: CPU Info": "lscpu",
    "🖥 Linux: Memory Info": "cat /proc/meminfo",
    "🖥 Linux: Uptime": "uptime",
    "🖥 Linux: List Users": "cut -d: -f1 /etc/passwd",
    "🖥 Linux: Show IP Address": "ip a",
    "🖥 Linux: Show Hostname": "hostname",
    "🖥 Linux: Running Processes": "ps aux",
    "🖥 Linux: Environment Variables": "printenv",
    "🖥 Linux: System Architecture": "uname -m",
    "🖥 Linux: Kernel Version": "uname -r",
    "🖥 Linux: Operating System Info": "uname -a",
    "🖥 Linux: List Logged In Users": "who",
    "🖥 Linux: Show Last 5 Logins": "command -v last >/dev/null && last -n 5 || echo '❌ last not installed'",
    "🖥 Linux: List Open Ports": "ss -tuln",
    "🖥 Linux: Top Running Processes": "top -bn1 | head -20",
    "🖥 Linux: Find OS Type": "cat /etc/os-release",
    "🖥 Linux: Network Interfaces": "ip link show",
    "🖥 Linux: Ping Google": "ping -c 4 google.com",
    "🖥 Linux: Mounted Filesystems": "mount | column -t",
    "🖥 Linux: Show Crontab": "crontab -l",
    "🖥 Linux: List Hidden Files": "ls -la",
    "🖥 Linux: Active Network Connections": "netstat -tulnp || ss -tulnp",
    "🖥 Linux: List USB Devices": "lsusb",
    "🖥 Linux: List PCI Devices": "lspci",
    "🖥 Linux: Show Disk Partitions": "lsblk",
    "🖥 Linux: Disk Space (ncdu)": "command -v ncdu >/dev/null && ncdu / || echo '❌ ncdu not installed'",
    "🖥 Linux: Check File Descriptors": "ulimit -n",
    "🖥 Linux: Check Open Files": "lsof | head -20",
    "🖥 Linux: Show System Logs": "journalctl -n 20",
    "🖥 Linux: Check SSH Status": "systemctl status ssh || service ssh status",
    "🖥 Linux: Current User": "whoami",
    "🖥 Linux: File Type of bash": "file /bin/bash",
    "🖥 Linux: Check SELinux Status": "sestatus || echo 'sestatus not found'",
    "🖥 Linux: View dmesg logs": "dmesg | tail -20",
    "🖥 Linux: Count Logged Users": "who | wc -l",
    "🖥 Linux: List Active Services": "systemctl list-units --type=service --state=running",
    "🖥 Linux: View Aliases": "alias",
    "🖥 Linux: Find a File": "find /etc -name 'hosts' 2>/dev/null",
    "🖥 Linux: Show PATH": "echo $PATH",
    "🖥 Linux: Reboot System": "echo 'Run: sudo reboot (permission required)'",
    "🖥 Linux: Shutdown System": "echo 'Run: sudo shutdown now (permission required)'",
    "🖥 Linux: Update Packages (Debian)": "sudo apt update && echo '✅ Updated (Debian)' || echo '❌ apt not found'",
    "🖥 Linux: Update Packages (RHEL)": "sudo yum update -y && echo '✅ Updated (RHEL)' || echo '❌ yum not found'",
    "🖥 Linux: Docker Version": "docker version || echo '❌ Docker not installed'",
    "🖥 Linux: Docker Containers": "docker ps -a || echo '❌ Docker not installed'",
    "🐳 Docker: List Running Containers": "docker ps",
    "🐳 Docker: List All Containers": "docker ps -a",
    "🐳 Docker: List Images": "docker images",
    "🐳 Docker: System Info": "docker info",
    "🐳 Docker: Disk Usage": "docker system df",
    "🐳 Docker: Container Stats": "docker stats --no-stream",
    "🐳 Docker: Docker Version": "docker version"
}

# ===== API Key Decorator =====
def require_key(func):
    def wrapper(*args):
        entered_key = args[-1]
        if entered_key != API_KEY:
            return "❌ Invalid API Key"
        return func(*args[:-1])
    return wrapper

# ===== Combined SSH Handler with Port and Error Output =====
@require_key
def run_ssh_combined(command_choice, username, ip, port):
    command = command_map.get(command_choice)
    if not command:
        return "❌ Invalid command selected."
    
    ssh_cmd = f"ssh {username}@{ip} {command}"
    # subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=20)
    
    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            return f"❌ SSH Failed:\n{result.stderr.strip() or 'No error message'}\n\n⚠ Please check:\n- SSH service running\n- IP/username/port correct\n- SSH key setup (no password prompts)"
        output = result.stdout.strip()
        return output if output else "✅ Command executed successfully (no output)"
    except subprocess.TimeoutExpired:
        return "⏰ SSH connection timed out. Is the server up and reachable?"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# ===== Twilio Tasks =====
@require_key
def send_sms(phone):
    msg = client.messages.create(to=phone, from_=TWILIO_PHONE, body="Hello from your app!")
    return f"✅ SMS sent to {phone}: {msg.sid}"

@require_key
def make_call(phone):
    call = client.calls.create(to=phone, from_=TWILIO_PHONE, url="http://demo.twilio.com/docs/voice.xml")
    return f"📞 Call initiated to {phone}: {call.sid}"

# ===== WhatsApp Message =====
@require_key
def send_whatsapp(phone, message):
    try:
        pwk.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
        return "✅ WhatsApp message sent using pywhatkit"
    except Exception as e:
        return f"❌ WhatsApp error: {str(e)}"

# ===== Face Swap =====
@require_key
def face_swap(img1, img2):
    try:
        face_cascade = cv2.CascadeClassifier(HAAR_PATH)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
        faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)
        if len(faces1) == 0 or len(faces2) == 0:
            return "❌ Face not detected in one or both images."
        x1, y1, w1, h1 = faces1[0]
        x2, y2, w2, h2 = faces2[0]
        face1 = img1[y1:y1+h1, x1:x1+w1]
        face1_resized = cv2.resize(face1, (w2, h2))
        swapped = img2.copy()
        swapped[y2:y2+h2, x2:x2+w2] = face1_resized
        path = "face_swapped.jpg"
        cv2.imwrite(path, swapped)
        return path
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ===== Sketch Image =====
@require_key
def sketch_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    path = "sketch.png"
    cv2.imwrite(path, sketch)
    return path

# ===== Gradio Interfaces =====
ssh_ui = gr.Interface(
    fn=run_ssh_combined,
    inputs=[
        gr.Dropdown(choices=list(command_map.keys()), label="📋 Choose a Task"),
        gr.Text(label="👤 Remote Username", placeholder="e.g., ubuntu"),
        gr.Text(label="🌐 Remote Server IP", placeholder="e.g., 192.168.1.10"),
        gr.Text(label="🔌 SSH Port", value="22"),
        gr.Text(label="🔑 Enter API Key", type="password")
    ],
    outputs="text",
    title="🔧 Remote System Assistant",
    description="Run Linux or Docker commands remotely. Make sure SSH works without asking for password."
)

sms_ui = gr.Interface(fn=send_sms, inputs=[
    gr.Text(label="📱 Phone Number (+CountryCode)"),
    gr.Text(label="🔑 API Key", type="password")
], outputs="text", title="📨 Send SMS")

call_ui = gr.Interface(fn=make_call, inputs=[
    gr.Text(label="📞 Phone Number (+CountryCode)"),
    gr.Text(label="🔑 API Key", type="password")
], outputs="text", title="📞 Make a Call")

wa_ui = gr.Interface(fn=send_whatsapp, inputs=[
    gr.Text(label="📱 WhatsApp Number with Country Code"),
    gr.Text(label="💬 Message Text"),
    gr.Text(label="🔑 API Key", type="password")
], outputs="text", title="💬 Send WhatsApp Message")

face_ui = gr.Interface(fn=face_swap, inputs=[
    gr.Image(label="🖼 Upload Image 1 (with Face)"),
    gr.Image(label="🖼 Upload Image 2 (to Replace Face)"),
    gr.Text(label="🔑 API Key", type="password")
], outputs="image", title="🔀 Face Swap")

sketch_ui = gr.Interface(fn=sketch_image, inputs=[
    gr.Image(label="🖼 Upload Image"),
    gr.Text(label="🔑 API Key", type="password")
], outputs="image", title="🎨 Convert Image to Sketch")

# ===== Final Launch =====
gr.TabbedInterface(
    [ssh_ui, sms_ui, call_ui, wa_ui, face_ui, sketch_ui],
    ["🧠 Remote Tasks", "📨 SMS", "📞 Call", "💬 WhatsApp", "🔀 Face Swap", "🎨 Sketch"]
).launch()