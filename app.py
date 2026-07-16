from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'boostsmm_final_mega_secret_key'

# Default Admin Credentials
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

# Global Data Storage (Temporary until Database integration)
prices = {
    "child_panel_monthly": 749,
    "child_panel_yearly": 7639
}

services = [
    {"id": 1, "name": "Instagram Followers [ALL Flags Work] [365 Days Refill]", "rate": 80},
    {"id": 2, "name": "Instagram Video/Reel Views [1m/Day] [Cheapest]", "rate": 20},
    {"id": 3, "name": "Facebook Video/Reel Views [0-30 Min] [30 Days Refill]", "rate": 150},
    {"id": 4, "name": "Telegram Members [Speedy] [Non-Drop]", "rate": 60}
]

orders = []
tickets = []
used_utrs = set()
user_wallet = 0.0
affiliate_balance = 0.0
total_referred_spend = 0.0

# Premium Modern SMM Layout with Floating Elements & Bottom Navigation Bar
BASE_LAYOUT_START = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BoostSMM - SMM Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; background-color: #0b0c10; margin: 0; padding-bottom: 80px; color: #ffffff; }
        
        /* Premium Floating Top Navbar */
        .top-navbar { background: linear-gradient(135deg, #1f2029 0%, #13141c 100%); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #282a36; box-shadow: 0 4px 15px rgba(0,0,0,0.4); position: sticky; top: 0; z-index: 100; }
        .top-navbar .logo { font-size: 20px; font-weight: 700; color: #00f2fe; text-decoration: none; display: flex; align-items: center; gap: 8px; }
        .top-navbar .user-profile { background: rgba(0, 242, 254, 0.1); padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3); font-size: 13px; font-weight: 500; color: #00f2fe; }

        .container { max-width: 600px; margin: 25px auto; padding: 0 15px; box-sizing: border-box; }
        
        /* Premium Dashboard Widgets */
        .info-card { background: #1a1b24; padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid #282a36; box-shadow: 0 8px 20px rgba(0,0,0,0.2); position: relative; overflow: hidden; }
        .info-card::before { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px; background: linear-gradient(to bottom, #0072ff, #00f2fe); }
        .info-card h3 { margin: 0 0 5px 0; font-size: 14px; color: #8a99ad; font-weight: 500; text-transform: uppercase; }
        .info-card .value { font-size: 28px; font-weight: 700; color: #38ef7d; }

        h2, h4 { color: #ffffff; font-weight: 600; margin-top: 0; margin-bottom: 15px; }
        .accent-color { color: #00f2fe; }

        /* Form Components */
        label { font-weight: 500; display: block; margin: 15px 0 6px; color: #8a99ad; font-size: 13px; }
        select, input, textarea { width: 100%; padding: 14px; background: #13141c; border: 1px solid #282a36; border-radius: 10px; color: white; box-sizing: border-box; font-size: 14px; font-family: inherit; transition: all 0.3s; }
        select:focus, input:focus, textarea:focus { border-color: #00f2fe; outline: none; box-shadow: 0 0 10px rgba(0,242,254,0.2); }
        
        .btn { background: linear-gradient(45deg, #0072ff, #00f2fe); color: white; border: none; padding: 14px; width: 100%; border-radius: 10px; font-size: 15px; cursor: pointer; margin-top: 20px; font-weight: 600; text-align: center; text-decoration: none; display: block; box-sizing: border-box; transition: 0.3s; box-shadow: 0 4px 15px rgba(0,114,255,0.3); }
        .btn:hover { opacity: 0.95; transform: translateY(-1px); box-shadow: 0 6px 20px rgba(0,114,255,0.4); }
        .btn-whatsapp { background: linear-gradient(45deg, #11998e, #38ef7d); box-shadow: 0 4px 15px rgba(56,239,125,0.3); }

        .alert { background-color: rgba(56, 239, 125, 0.15); color: #38ef7d; padding: 14px; border-radius: 10px; margin-bottom: 20px; text-align: center; font-weight: 500; border: 1px solid rgba(56, 239, 125, 0.3); font-size: 14px; }
        .alert-danger { background-color: rgba(244, 67, 54, 0.15); color: #f44336; border-color: rgba(244, 67, 54, 0.3); }

        /* Modern Table Styling */
        .table-wrapper { background: #1a1b24; border-radius: 14px; border: 1px solid #282a36; overflow: hidden; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; box-sizing: border-box; }
        th, td { padding: 14px 16px; text-align: left; border-bottom: 1px solid #282a36; font-size: 13px; }
        th { background-color: #13141c; color: #8a99ad; font-weight: 500; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }
        .badge { padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; background: #282a36; color: #fff; text-transform: uppercase; }
        .badge-pending { background: rgba(255, 152, 0, 0.2); color: #ff9800; border: 1px solid rgba(255, 152, 0, 0.3); }
        .badge-success { background: rgba(56, 239, 125, 0.2); color: #38ef7d; border: 1px solid rgba(56, 239, 125, 0.3); }

        /* Fixed Premium Bottom Navigation Bar */
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: #13141c; height: 65px; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #282a36; box-shadow: 0 -4px 20px rgba(0,0,0,0.5); z-index: 1000; }
        .bottom-nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8a99ad; text-decoration: none; font-size: 11px; font-weight: 500; transition: 0.3s; flex: 1; height: 100%; gap: 4px; }
        .bottom-nav-item.active { color: #00f2fe; }
        .bottom-nav-item svg { width: 22px; height: 22px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="top-navbar">
        <a href="/" class="logo">⚡ BoostSMM</a>
        <div class="user-profile">👤 abhiahek3376</div>
    </div>
    <div class="container">
"""

BASE_LAYOUT_END = """
    </div>
    <div class="bottom-nav">
        <a href="/" class="bottom-nav-item {{ 'active' if active_page == 'order' else '' }}">
            <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
            New Order
        </a>
        <a href="/add-funds" class="bottom-nav-item {{ 'active' if active_page == 'funds' else '' }}">
            <svg viewBox="0 0 24 24"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
            Top Up
        </a>
        <a href="/child-panel" class="bottom-nav-item {{ 'active' if active_page == 'child' else '' }}">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.04-.42 1.99-1.07 2.75z"/></svg>
            Child Panel
        </a>
        <a href="/affiliate" class="bottom-nav-item {{ 'active' if active_page == 'affiliate' else '' }}">
            <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 1.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
            Affiliate
        </a>
        <a href="/tickets" class="bottom-nav-item {{ 'active' if active_page == 'tickets' else '' }}">
            <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>
            Support
        </a>
    </div>
</body>
</html>
"""

@app.route('/')
def user_dashboard():
    msg = request.args.get('msg', '')
    msg_type = request.args.get('type', 'success')
    alert_html = ""
    if msg:
        css_class = "alert alert-danger" if msg_type == "danger" else "alert"
        alert_html = f"<div class='{css_class}'>{msg}</div>"

    content = f"""
    {alert_html}
    <div class="info-card">
        <h3>⚡ Wallet Balance</h3>
        <div class="value">₹{user_wallet:.2f}</div>
    </div>
    
    <h2>📦 Place New Order</h2>
    <form action="/place-order" method="POST">
        <label>Category Services:</label>
        <select name="service_id">
            {"".join([f"<option value='{s['id']}'>{s['name']} - ₹{s['rate']}/k</option>" for s in services])}
        </select>
        
        <label>Link / Target URL:</label>
        <input type="text" name="link" placeholder="e.g. https://instagram.com/profile" required>
        
        <label>Quantity:</label>
        <input type="number" name="quantity" min="100" placeholder="Min: 100" required>
        
        <button type="submit" class="btn">New Order</button>
    </form>
    
    <h2 style="margin-top: 35px;">📋 Recent Transaction Logs</h2>
    <div class="table-wrapper">
        <table>
            <thead>
                <tr><th>ID</th><th>Target URL</th><th>Qty</th><th>Status</th></tr>
            </thead>
            <tbody>
                {"".join([f"<tr><td>#{o['id']}</td><td>{o['link']}</td><td>{o['quantity']}</td><td><span class='badge badge-pending'>{o['status']}</span></td></tr>" for o in orders[::-1]]) if orders else "<tr><td colspan='4' style='text-align:center; color:#8a99ad; padding:20px;'>No orders recorded yet.</td></tr>"}
            </tbody>
        </table>
    </div>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='order')

@app.route('/place-order', methods=['POST'])
def place_order():
    global user_wallet, total_referred_spend, affiliate_balance
    service_id = int(request.form.get('service_id'))
    qty = int(request.form.get('quantity', 0))
    link = request.form.get('link')
    
    rate = 80
    for s in services:
        if s['id'] == service_id:
            rate = s['rate']
            break
            
    cost = (qty / 1000) * rate
    
    if user_wallet < cost:
        return redirect(url_for('user_dashboard', msg="Insufficient Wallet Funds! Please add money.", type="danger"))
        
    user_wallet -= cost
    total_referred_spend += cost
    if total_referred_spend >= 500:
        affiliate_balance = total_referred_spend * 0.02

    order_id = len(orders) + 1001
    orders.append({
        "id": order_id,
        "link": link,
        "quantity": qty,
        "status": "Pending"
    })
    return redirect(url_for('user_dashboard', msg=f"🎉 Order #{order_id} successfully queued!"))

@app.route('/add-funds', methods=['GET', 'POST'])
def add_funds():
    global user_wallet
    msg_html = ""
    if request.method == 'POST':
        method = request.form.get('method')
        amount_str = request.form.get('amount', '0')
        ref_id = request.form.get('ref_id', '').strip()
        
        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0

        if amount <= 0:
            msg_html = "<div class='alert alert-danger'>❌ Please input a valid deposit amount.</div>"
        elif not ref_id:
            msg_html = "<div class='alert alert-danger'>❌ Transaction ID reference hash required.</div>"
        elif ref_id in used_utrs:
            msg_html = "<div class='alert alert-danger'>❌ Error: Duplicate Transaction ID detected!</div>"
        else:
            if method == "upi" and (len(ref_id) != 12 or not ref_id.isdigit()):
                msg_html = "<div class='alert alert-danger'>❌ Invalid UTR structural signature. Must be 12 digits.</div>"
            else:
                used_utrs.add(ref_id)
                user_wallet += amount
                msg_html = f"<div class='alert'>🎉 Payment verified! Instantly credited ₹{amount:.2f} via {method.upper()}.</div>"

    upi_id = "shiladevi0445@nyes"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa={upi_id}%26pn=Boost%20SMM%20Panel"

    content = f"""
    <h2>💳 Automatic Fund Injection</h2>
    {msg_html}
    
    <div style="background: #1a1b24; padding: 15px; border-radius: 12px; border: 1px solid #282a36; text-align: left; margin-bottom: 20px;">
        <h4 style="margin: 0 0 10px 0; color: #00f2fe;">🪙 Multi-Currency Vault Gateways:</h4>
        <p style="margin: 4px 0; font-size: 13px;"><strong>🇮🇳 Fast UPI Address:</strong> {upi_id}</p>
        <p style="margin: 4px 0; font-size: 13px;"><strong>🟢 USDT (TRC-20 Network):</strong> TX7xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p>
        <p style="margin: 4px 0; font-size: 13px;"><strong>🔵 USDT (BEP-20 / Smart Chain):</strong> 0x7xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p>
    </div>

    <div style="background: white; padding: 15px; display: inline-block; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.4); margin-bottom: 25px;">
        <img src="{qr_url}" alt="Gateway QR Code" style="display:block;">
    </div>
    
    <form method="POST" style="text-align: left;">
        <label>Deposit Network Engine:</label>
        <select name="method">
            <option value="upi">PhonePe-Paytm (India Only) - Instant</option>
            <option value="paypal">PayPal Gateway / International Card</option>
            <option value="crypto">Crypto Network Cascade (USDT / BTC)</option>
        </select>
        
        <label>Exact Transaction Amount:</label>
        <input type="number" step="any" name="amount" placeholder="e.g. 500" required>
        
        <label>UTR Reference ID / TxID String:</label>
        <input type="text" name="ref_id" placeholder="Enter 12-digit UTR or Payment ID" required>
        
        <button type="submit" class="btn">Verify & Load Wallet</button>
    </form>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='funds')

@app.route('/child-panel')
def child_panel():
    whatsapp_url = "https://wa.me/918376820445?text=I%20need%20child%20pannel"
    content = f"""
    <h2>🛠️ White-Label Reseller Platform (Child Panel)</h2>
    <p style="color: #8a99ad; margin-bottom: 25px; font-size: 14px;">Establish your independent customized SMM identity linked directly to our automated pipeline.</p>
    
    <div class="info-card" style="margin-bottom: 15px;">
        <h3 style="color: #38ef7d;">📅 Regular Rolling Plan</h3>
        <div class="value" style="color: #ffffff; font-size: 24px;">₹{prices['child_panel_monthly']}<span style="font-size:14px; color:#8a99ad; font-weight:normal;"> / Month</span></div>
    </div>
    
    <div class="info-card" style="background: linear-gradient(135deg, #1a1b24 0%, #152722 100%); border-color: #38ef7d;">
        <h3 style="color: #00f2fe;">🌟 Infinite Annual Engine</h3>
        <div class="value" style="color: #38ef7d; font-size: 24px;">₹{prices['child_panel_yearly']}<span style="font-size:14px; color:#8a99ad; font-weight:normal;"> / Year</span></div>
        <p style="color: #38ef7d; font-size: 12px; font-weight: 600; margin: 8px 0 0 0;">🔥 Flat 15% System Discount Built-in!</p>
    </div>
    
    <a href="{whatsapp_url}" target="_blank" class="btn btn-whatsapp">💬 Synchronize via WhatsApp</a>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='child')

@app.route('/affiliate')
def affiliate():
    status_msg = "🔒 Locked (Minimum referral trigger set at ₹500 spend threshold)"
    status_color = "#ff9800"
    if total_referred_spend >= 500:
        status_msg = "🔓 Unlocked & Processing (2% Pipelined Commission Active)"
        status_color = "#38ef7d"
        
    content = f"""
    <h2>👥 Performance Affiliate Node</h2>
    <p style="color: #8a99ad; font-size: 14px;">Distribute your dedicated referral token and absorb a rolling 2% processing revenue cut on global client spending.</p>
    
    <div class="info-card">
        <h3>🔗 Cryptographic Token Link</h3>
        <input type="text" value="https://boostsmm.onrender.com/?ref=abhiahek3376" readonly style="color:#00f2fe; font-weight:600; cursor:pointer; background:#13141c; text-align:center;">
    </div>
    
    <div class="info-card" style="border-left-color: {status_color};">
        <h3>💰 Vault Ledger Revenue</h3>
        <div class="value" style="color: #38ef7d; margin-bottom: 10px;">₹{affiliate_balance:.2f}</div>
        <p style="margin: 5px 0; font-size:13px;">Pipelined Spend Volume: <strong>₹{total_referred_spend:.2f} / ₹500.00</strong></p>
        <p style="margin: 0; font-size:12px; color: {status_color}; font-weight:600;">System Check: {status_msg}</p>
    </div>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='affiliate')

@app.route('/tickets', methods=['GET', 'POST'])
def tickets_page():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        tickets.append({
            "id": len(tickets) + 1,
            "subject": subject,
            "msg": message,
            "reply": "System Route: Forwarded to Admin Cluster Review."
        })
    tickets_html = "".join([f"<div class='info-card'><h4>📌 Ticket #{t['id']}: {t['subject']}</h4><p style='color:#ccc; font-size:13px; margin:5px 0;'>{t['msg']}</p><p style='color: #00f2fe; margin:5px 0 0; font-size:12px; font-weight:600;'>💬 Node Reply: {t['reply']}</p></div>" for t in tickets[::-1]])
    
    content = f"""
    <h2>📩 Encrypted Support Desk</h2>
    <form method="POST">
        <label>Node Issue Context:</label>
        <input type="text" name="subject" placeholder="e.g. Transaction Routing Delay" required>
        
        <label>Extended Transmission Core:</label>
        <textarea name="message" rows="4" placeholder="Describe the structural error or deployment context..." required></textarea>
        
        <button type="submit" class="btn">Transmit Core Ticket</button>
    </form>
    <hr style='margin: 30px 0; border: none; border-top: 1px solid #282a36;'>
    <h2>📜 Historical Logs</h2>
    {tickets_html if tickets else "<p style='color:#8a99ad; font-size:13px;'>No communications records registered.</p>"}
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='tickets')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template_string(f"""
    <!DOCTYPE html>
    <html><head><title>Secure Login</title>{BASE_LAYOUT_START}</head><body><div class="container" style="max-width:400px; margin-top:80px;">
        <h2>🔐 Control Module</h2>
        <form method="POST">
            <label>Master Username:</label><input type="text" name="username" required>
            <label>Master Password:</label><input type="password" name="password" required>
            <button type="submit" class="btn">Initialize Node</button>
        </form>
    </div></body></html>
    """)

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    if request.method == 'POST':
        prices['child_panel_monthly'] = int(request.form.get('monthly', prices['child_panel_monthly']))
        prices['child_panel_yearly'] = int(request.form.get('yearly', prices['child_panel_yearly']))
        
    orders_html = "".join([f"<tr><td>#{o['id']
