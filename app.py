from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'boostsmm_final_mega_secret_key'

# Default Admin Credentials
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

# Global Data Storage
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
        .top-navbar { background: linear-gradient(135deg, #1f2029 0%, #13141c 100%); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #282a36; box-shadow: 0 4px 15px rgba(0,0,0,0.4); position: sticky; top: 0; z-index: 100; }
        .top-navbar .logo { font-size: 20px; font-weight: 700; color: #00f2fe; text-decoration: none; display: flex; align-items: center; gap: 8px; }
        .top-navbar .user-profile { background: rgba(0, 242, 254, 0.1); padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3); font-size: 13px; font-weight: 500; color: #00f2fe; }
        .container { max-width: 600px; margin: 25px auto; padding: 0 15px; box-sizing: border-box; }
        .info-card { background: #1a1b24; padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid #282a36; box-shadow: 0 8px 20px rgba(0,0,0,0.2); position: relative; overflow: hidden; }
        .info-card::before { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px; background: linear-gradient(to bottom, #0072ff, #00f2fe); }
        .info-card h3 { margin: 0 0 5px 0; font-size: 14px; color: #8a99ad; font-weight: 500; text-transform: uppercase; }
        .info-card .value { font-size: 28px; font-weight: 700; color: #38ef7d; }
        h2, h4 { color: #ffffff; font-weight: 600; margin-top: 0; margin-bottom: 15px; }
        label { font-weight: 500; display: block; margin: 15px 0 6px; color: #8a99ad; font-size: 13px; }
        select, input, textarea { width: 100%; padding: 14px; background: #13141c; border: 1px solid #282a36; border-radius: 10px; color: white; box-sizing: border-box; font-size: 14px; font-family: inherit; }
        .btn { background: linear-gradient(45deg, #0072ff, #00f2fe); color: white; border: none; padding: 14px; width: 100%; border-radius: 10px; font-size: 15px; cursor: pointer; margin-top: 20px; font-weight: 600; text-align: center; text-decoration: none; display: block; box-sizing: border-box; }
        .btn-whatsapp { background: linear-gradient(45deg, #11998e, #38ef7d); }
        .alert { background-color: rgba(56, 239, 125, 0.15); color: #38ef7d; padding: 14px; border-radius: 10px; margin-bottom: 20px; text-align: center; font-weight: 500; border: 1px solid rgba(56, 239, 125, 0.3); font-size: 14px; }
        .alert-danger { background-color: rgba(244, 67, 54, 0.15); color: #f44336; border-color: rgba(244, 67, 54, 0.3); }
        .table-wrapper { background: #1a1b24; border-radius: 14px; border: 1px solid #282a36; overflow: hidden; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 14px 16px; text-align: left; border-bottom: 1px solid #282a36; font-size: 13px; }
        th { background-color: #13141c; color: #8a99ad; font-weight: 500; text-transform: uppercase; font-size: 11px; }
        .badge { padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; background: #282a36; color: #fff; text-transform: uppercase; }
        .badge-pending { background: rgba(255, 152, 0, 0.2); color: #ff9800; }
        .badge-success { background: rgba(56, 239, 125, 0.2); color: #38ef7d; }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: #13141c; height: 65px; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #282a36; box-shadow: 0 -4px 20px rgba(0,0,0,0.5); z-index: 1000; }
        .bottom-nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8a99ad; text-decoration: none; font-size: 11px; font-weight: 500; flex: 1; height: 100%; gap: 4px; }
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
        <a href="/" class="bottom-nav-item {% if active_page == 'order' %}active{% endif %}">
            <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
            New Order
        </a>
        <a href="/add-funds" class="bottom-nav-item {% if active_page == 'funds' %}active{% endif %}">
            <svg viewBox="0 0 24 24"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
            Top Up
        </a>
        <a href="/child-panel" class="bottom-nav-item {% if active_page == 'child' %}active{% endif %}">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.04-.42 1.99-1.07 2.75z"/></svg>
            Child Panel
        </a>
        <a href="/affiliate" class="bottom-nav-item {% if active_page == 'affiliate' %}active{% endif %}">
            <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 1.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
            Affiliate
        </a>
        <a href="/tickets" class="bottom-nav-item {% if active_page == 'tickets' %}active{% endif %}">
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

    options = "".join([f"<option value='{s['id']}'>{s['name']} - ₹{s['rate']}/k</option>" for s in services])
    
    rows = ""
    if orders:
        for o in orders[::-1]:
            rows += f"<tr><td>#{o['id']}</td><td>{o['link']}</td><td>{o['quantity']}</td><td><span class='badge badge-pending'>{o['status']}</span></td></tr>"
    else:
        rows = "<tr><td colspan='4' style='text-align:center; color:#8a99ad; padding:20px;'>No orders recorded yet.</td></tr>"

    content = f"""
    {alert_html}
    <div class="info-card">
        <h3>⚡ Wallet Balance</h3>
        <div class="value">₹{user_wallet:.2f}</div>
    </div>
    <h2>📦 Place New Order</h2>
    <form action="/place-order" method="POST">
        <label>Category Services:</label>
        <select name="service_id">{options}</select>
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
            <tbody>{rows}</tbody>
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
        return redirect(url_for('user_dashboard', msg="Insufficient Wallet Funds!", type="danger"))
        
    user_wallet -= cost
    total_referred_spend += cost
    if total_referred_spend >= 500:
        affiliate_balance = total_referred_spend * 0.02

    order_id = len(orders) + 1001
    orders.append({"id": order_id, "link": link, "quantity": qty, "status": "Pending"})
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
            msg_html = "<div class='alert alert-danger'>❌ Transaction ID hash required.</div>"
        elif ref_id in used_utrs:
            msg_html = "<div class='alert alert-danger'>❌ Error: Duplicate ID detected!</div>"
        else:
            used_utrs.add(ref_id)
            user_wallet += amount
            msg_html = f"<div class='alert'>🎉 Verified! Credited ₹{amount:.2f} via {method.upper()}.</div>"

    upi_id = "shiladevi0445@nyes"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa={upi_id}%26pn=BoostSMM"

    content = f"""
    <h2>💳 Fund Injection</h2>
    {msg_html}
    <div style="background: #1a1b24; padding: 15px; border-radius: 12px; border: 1px solid #282a36; margin-bottom: 20px;">
        <p><strong>🇮🇳 UPI Address:</strong> {upi_id}</p>
    </div>
    <div style="background: white; padding: 15px; display: inline-block; border-radius: 12px; margin-bottom: 25px;">
        <img src="{qr_url}" alt="QR">
    </div>
    <form method="POST">
        <label>Engine:</label>
        <select name="method"><option value="upi">UPI - Instant</option></select>
        <label>Amount:</label>
        <input type="number" step="any" name="amount" required>
        <label>UTR ID:</label>
        <input type="text" name="ref_id" required>
        <button type="submit" class="btn">Verify & Load</button>
    </form>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='funds')

@app.route('/child-panel')
def child_panel():
    whatsapp_url = "https://wa.me/918376820445?text=I%20need%20child%20pannel"
    content = f"""
    <h2>🛠️ Child Panel</h2>
    <div class="info-card"><h3>📅 Monthly</h3><div class="value">₹{prices['child_panel_monthly']}</div></div>
    <div class="info-card"><h3>🌟 Annual</h3><div class="value">₹{prices['child_panel_yearly']}</div></div>
    <a href="{whatsapp_url}" target="_blank" class="btn btn-whatsapp">💬 Sync via WhatsApp</a>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='child')

@app.route('/affiliate')
def affiliate():
    status_msg = "🔒 Locked" if total_referred_spend < 500 else "🔓 Unlocked"
    content = f"""
    <h2>👥 Affiliate System</h2>
    <div class="info-card"><h3>💰 Earnings</h3><div class="value">₹{affiliate_balance:.2f}</div><p>{status_msg}</p></div>
    """
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='affiliate')

@app.route('/tickets', methods=['GET', 'POST'])
def tickets_page():
    if request.method == 'POST':
        tickets.append({"id": len(tickets) + 1, "subject": request.form.get('subject'), "msg": request.form.get('message'), "reply": "Forwarded to Admin cluster."})
    t_html = "".join([f"<div class='info-card'><h4>📌 #{t['id']} {t['subject']}</h4><p>{t['msg']}</p></div>" for t in tickets[::-1]])
    content = f"<h2>📩 Support</h2><form method='POST'><label>Context:</label><input type='text' name='subject' required><label>Core:</label><textarea name='message' required></textarea><button type='submit' class='btn'>Submit</button></form><hr>{t_html}"
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='tickets')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST' and request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
        session['admin_logged'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template_string(BASE_LAYOUT_START + "<h2>🔐 Control Module</h2><form method='POST'><label>User:</label><input type='text' name='username'><label>Pass:</label><input type='password' name='password'><button type='submit' class='btn'>Login</button></form>" + BASE_LAYOUT_END, active_page='admin')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged'): 
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        prices['child_panel_monthly'] = int(request.form.get('monthly', prices['child_panel_monthly']))
        prices['child_panel_yearly'] = int(request.form.get('yearly', prices['child_panel_yearly']))
    
    orders_html = "".join([f"<tr><td>#{o['id']}</td><td>{o['link']}</td><td>{o['quantity']}</td><td>{o['status']}</td></tr>" for o in orders])
    content = f"<h2>⚙️ Admin Control Panel</h2><form method='POST'><input type='number' name='monthly' value='{prices['child_panel_monthly']}'><input type='number' name='yearly' value='{prices['child_panel_yearly']}'><button type='submit' class='btn'>Update Matrix</button></form><table>{orders_html}</table>"
    return render_template_string(BASE_LAYOUT_START + content + BASE_LAYOUT_END, active_page='admin')

if __name__ == '__main__':
    app.run(debug=True)
