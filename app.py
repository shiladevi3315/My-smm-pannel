from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'boostsmm_final_mega_secret_key'

# Default Admin Credentials
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

# Global Data Storage (Temporary until Database is added)
prices = {
    "child_panel_monthly": 749,
    "child_panel_yearly": 7639  # 15% Discount on 12 * 749
}

services = [
    {"id": 1, "name": "Instagram Followers [Non-Drop] [Best]", "rate": 80},
    {"id": 2, "name": "Instagram Likes [Instant/Real]", "rate": 20},
    {"id": 3, "name": "YouTube Views [High Quality]", "rate": 150},
    {"id": 4, "name": "Telegram Members [Speedy]", "rate": 60}
]

orders = []
tickets = []
used_utrs = set()  # Duplicity check for UTR
user_wallet = 0.0
affiliate_balance = 0.0
total_referred_spend = 0.0

BASE_CSS = """
<style>
    body { font-family: 'Poppins', sans-serif; background-color: #0d0e15; margin: 0; padding: 0; color: #ffffff; }
    .navbar { background-color: #1f2029; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #343746; }
    .navbar .logo { font-size: 20px; font-weight: bold; color: #00f2fe; text-decoration: none; }
    .navbar .links a { color: #8a99ad; text-decoration: none; margin-left: 20px; font-weight: 500; font-size: 14px; transition: 0.3s; }
    .navbar .links a:hover, .navbar .links a.active { color: #00f2fe; }
    .container { max-width: 750px; margin: 40px auto; background: #1f2029; padding: 30px; border-radius: 12px; border: 1px solid #343746; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
    h2, h3 { color: #00f2fe; margin-top: 0; font-weight: 600; }
    label { font-weight: bold; display: block; margin: 15px 0 5px; color: #8a99ad; font-size: 14px; }
    select, input, textarea { width: 100%; padding: 12px; background: #13141c; border: 1px solid #343746; border-radius: 6px; color: white; box-sizing: border-box; font-size: 14px; }
    select:focus, input:focus, textarea:focus { border-color: #00f2fe; outline: none; }
    .btn { background: linear-gradient(45deg, #0072ff, #00f2fe); color: white; border: none; padding: 14px; width: 100%; border-radius: 6px; font-size: 16px; cursor: pointer; margin-top: 20px; font-weight: bold; text-align: center; text-decoration: none; display: block; box-sizing: border-box; transition: 0.3s; }
    .btn:hover { opacity: 0.9; transform: translateY(-1px); }
    .btn-whatsapp { background: linear-gradient(45deg, #11998e, #38ef7d); }
    .card { background: #13141c; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #00f2fe; }
    .alert { background-color: #155724; color: #d4edda; padding: 12px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; border: 1px solid #c3e6cb; }
    .alert-danger { background-color: #721c24; color: #f8d7da; border-color: #f5c6cb; }
    .wallet-box { background: #13141c; padding: 12px 20px; border-radius: 6px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #343746; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #13141c; border-radius: 8px; overflow: hidden; }
    th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #343746; font-size: 14px; }
    th { background-color: #1a1b23; color: #8a99ad; font-weight: 600; }
    .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #343746; color: #fff; }
    .badge-pending { background: #ff9800; }
    .badge-success { background: #4caf50; }
</style>
"""

@app.route('/')
def user_dashboard():
    msg = request.args.get('msg', '')
    msg_type = request.args.get('type', 'success')
    alert_html = ""
    if msg:
        css_class = "alert alert-danger" if msg_type == "danger" else "alert"
        alert_html = f"<div class='{css_class}'>{msg}</div>"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Boost SMM Panel - Dashboard</title>{BASE_CSS}</head>
    <body>
        <div class="navbar">
            <a href="/" class="logo">🚀 Boost SMM</a>
            <div class="links">
                <a href="/" class="active">New Order</a>
                <a href="/add-funds">Add Funds</a>
                <a href="/child-panel">Child Panel</a>
                <a href="/affiliate">Affiliate</a>
                <a href="/tickets">Tickets</a>
                <a href="/admin">Admin Area</a>
            </div>
        </div>
        <div class="container">
            {alert_html}
            <div class="wallet-box">
                <span style="color: #8a99ad; font-weight: 500;">👋 Welcome User</span>
                <span>Wallet Balance: <strong style="color: #38ef7d; font-size: 18px;">₹{user_wallet:.2f}</strong></span>
            </div>
            <h2>🔥 Place New Order</h2>
            <form action="/place-order" method="POST">
                <label>Select Service:</label>
                <select name="service_id">
                    {"".join([f"<option value='{s['id']}'>{s['name']} - ₹{s['rate']}/k</option>" for s in services])}
                </select>
                <label>Target Link:</label>
                <input type="text" name="link" placeholder="https://instagram.com/username..." required>
                <label>Quantity:</label>
                <input type="number" name="quantity" min="100" placeholder="Min: 100" required>
                <button type="submit" class="btn">Submit Order</button>
            </form>
            
            <h3 style="margin-top: 40px;">📦 Recent Orders</h3>
            <table>
                <thead>
                    <tr><th>Order ID</th><th>Link</th><th>Quantity</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {"".join([f"<tr><td>#{o['id']}</td><td>{o['link']}</td><td>{o['quantity']}</td><td><span class='badge badge-pending'>{o['status']}</span></td></tr>" for o in orders[::-1]]) if orders else "<tr><td colspan='4' style='text-align:center; color:#8a99ad;'>No orders placed yet.</td></tr>"}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """)

@app.route('/place-order', methods=['POST'])
def place_order():
    global user_wallet, total_referred_spend, affiliate_balance
    service_id = int(request.form.get('service_id'))
    qty = int(request.form.get('quantity', 0))
    link = request.form.get('link')
    
    # Find service rate
    rate = 80
    for s in services:
        if s['id'] == service_id:
            rate = s['rate']
            break
            
    cost = (qty / 1000) * rate
    
    if user_wallet < cost:
        return redirect(url_for('user_dashboard', msg="Insufficient Funds! Please add money to your wallet.", type="danger"))
        
    user_wallet -= cost
    
    # Track Affiliate Spend simulation
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
    return redirect(url_for('user_dashboard', msg=f"🎉 Order #{order_id} placed successfully!"))

@app.route('/add-funds', methods=['GET', 'POST'])
def add_funds():
    global user_wallet
    msg_html = ""
    if request.method == 'POST':
        utr = request.form.get('utr').strip()
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            amount = 0.0
        
        if utr in used_utrs:
            msg_html = "<div class='alert alert-danger'>❌ Error: This UTR has already been used for adding funds!</div>"
        elif len(utr) != 12 or not utr.isdigit():
            msg_html = "<div class='alert alert-danger'>❌ Invalid UTR! Transaction ID must be exactly 12 digits.</div>"
        elif amount <= 0:
            msg_html = "<div class='alert alert-danger'>❌ Please enter a valid payment amount.</div>"
        else:
            used_utrs.add(utr)
            user_wallet += amount
            msg_html = f"<div class='alert'>🎉 Success! ₹{amount:.2f} has been instantly added to your wallet.</div>"

    upi_id = "shiladevi0445@nyes"
    # Standard dynamic UPI QR generation via public API
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa={upi_id}%26pn=Boost%20SMM%20Panel"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Add Funds - Instant Payment</title>{BASE_CSS}</head>
    <body>
        <div class="navbar">
            <a href="/" class="logo">🚀 Boost SMM</a>
            <div class="links"><a href="/">New Order</a><a href="/add-funds" class="active">Add Funds</a><a href="/child-panel">Child Panel</a></div>
        </div>
        <div class="container" style="text-align: center;">
            <h2>💳 Add Funds (Instant Automation)</h2>
            {msg_html}
            <p style="color: #8a99ad; margin-bottom: 20px;">Scan QR code using Paytm, PhonePe, or Google Pay to complete payment.</p>
            
            <div style="background: white; padding: 15px; display: inline-block; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
                <img src="{qr_url}" alt="Payment QR Code" style="display:block;">
            </div>
            
            <p style="font-size: 16px; font-weight: bold; color: #38ef7d; margin-top: 15px;">Official Merchant UPI ID: <span style="color:#fff;">{upi_id}</span></p>
            
            <hr style="border-color: #343746; margin: 30px 0;">
            
            <form method="POST" style="text-align: left; max-width: 420px; margin: 0 auto;">
                <label>Exact Amount Paid (₹):</label>
                <input type="number" step="any" name="amount" placeholder="e.g. 500" required>
                
                <label>12-Digit UTR / Transaction Number:</label>
                <input type="text" name="utr" maxlength="12" placeholder="Enter 12 digit payment reference" required>
                
                <button type="submit" class="btn">Verify & Credit Instantly</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/child-panel')
def child_panel():
    whatsapp_url = "https://wa.me/918376820445?text=I%20need%20child%20pannel"
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Make Your Child Panel</title>{BASE_CSS}</head>
    <body>
        <div class="navbar">
            <a href="/" class="logo">🚀 Boost SMM</a>
            <div class="links"><a href="/">New Order</a><a href="/child-panel" class="active">Child Panel</a><a href="/tickets">Tickets</a></div>
        </div>
        <div class="container">
            <h2>🛠️ Make Your Own SMM Panel (Child Panel)</h2>
            <p style="color: #8a99ad; margin-bottom: 25px;">Apna logo laga kar apna khud ka brand aur automated business shuru karein.</p>
            
            <div class="card">
                <h3 style="margin-bottom:5px;">📅 Monthly Plan</h3>
                <p style="font-size: 26px; font-weight: bold; margin: 5px 0; color:#38ef7d;">₹{prices['child_panel_monthly']} <span style="font-size: 14px; color:#8a99ad; font-weight:normal;">/ Month</span></p>
                <p style="color:#8a99ad; font-size:13px; margin:0;">Best for absolute beginners looking to try out.</p>
            </div>
            
            <div class="card" style="border-left-color: #38ef7d; background: linear-gradient(135deg, #13141c 0%, #1a2721 100%);">
                <h3 style="margin-bottom:5px; color:#38ef7d;">🌟 Yearly Plan (Best Savings!)</h3>
                <p style="font-size: 26px; font-weight: bold; margin: 5px 0; color:#00f2fe;">₹{prices['child_panel_yearly']} <span style="font-size: 14px; color:#8a99ad; font-weight:normal;">/ Year</span></p>
                <p style="color: #38ef7d; font-size: 13px; font-weight: bold; margin:0;">🔥 Flat 15% Off Included! Saves huge money over monthly payments.</p>
            </div>
            
            <a href="{whatsapp_url}" target="_blank" class="btn btn-whatsapp">💬 Order via WhatsApp</a>
        </div>
    </body>
    </html>
    """)

@app.route('/affiliate')
def affiliate():
    status_msg = "🔴 Locked (Aapke referral ne abhi tak total ₹500 spend nahi kiya hai)"
    status_color = "#ff9800"
    if total_referred_spend >= 500:
        status_msg = "🟢 Active & Unlocked (2% Commission Available!)"
        status_color = "#38ef7d"
        
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Affiliate & Earn</title>{BASE_CSS}</head>
    <body>
        <div class="navbar">
            <a href="/" class="logo">🚀 Boost SMM</a>
            <div class="links"><a href="/">New Order</a><a href="/affiliate" class="active">Affiliate</a></div>
        </div>
        <div class="container">
            <h2>🔗 Affiliate & Referral Program</h2>
            <p style="color: #8a99ad;">Dosto ko refer karein aur unke har order spend par **2% commission** direct kamaayein.</p>
            
            <div class="card">
                <label>Your Unique Referral Link:</label>
                <input type="text" value="https://boost-smm.onrender.com/?ref=user8376" readonly style="color:#00f2fe; font-weight:bold; cursor:pointer;">
            </div>

            <div class="card" style="border-left-color: {status_color};">
                <h3>💰 Affiliate Wallet Balance: <span style="color:#38ef7d;">₹{affiliate_balance:.2f}</span></h3>
                <p style="margin: 10px 0 5px;">Referral Total Spend Progress: <strong>₹{total_referred_spend:.2f} / ₹500.00</strong></p>
                <p style="margin: 0; font-size:14px;">Program Status: <span style="font-weight:bold; color: {status_color};">{status_msg}</span></p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/tickets', methods=['GET', 'POST'])
def tickets_page():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        tickets.append({
            "id": len(tickets) + 1,
            "subject": subject,
            "msg": message,
            "reply": "Waiting for admin review..."
        })
    tickets_html = "".join([f"<div class='card'><h4>📌 Ticket #{t['id']}: {t['subject']}</h4><p style='color:#ccc; font-size:14px;'>{t['msg']}</p><p style='color: #00f2fe; margin:5px 0 0; font-size:13px; font-weight:bold;'>💬 Admin Response: {t['reply']}</p></div>" for t in tickets[::-1]])
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Support Tickets</title>{BASE_CSS}</head>
    <body>
        <div class="navbar">
            <a href="/" class="logo">🚀 Boost SMM</a>
            <div class="links"><a href="/">New Order</a><a href="/tickets" class="active">Tickets</a></div>
        </div>
        <div class="container">
            <h2>📩 Support Helpdesk</h2>
            <form method="POST">
                <label>Issue Subject:</label>
                <input type="text" name="subject" placeholder="e.g. Order Pending, Fund not added" required>
                <label>Detailed Message:</label>
                <textarea name="message" rows="4" placeholder="Explain your query clearly..." required></textarea>
                <button type="submit" class="btn">Open Ticket</button>
            </form>
            <hr style='margin-top:40px; border-color:#343746;'>
            <h3>My Open Tickets</h3>
            {tickets_html if tickets else "<p style='color:#8a99ad;'>No support tickets found.</p>"}
        </div>
    </body>
    </html>
    """)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template_string(f"""
    <!DOCTYPE html>
    <html><head><title>Admin Login</title>{BASE_CSS}</head><body><div class="container" style="max-width:400px; margin-top:100px;">
        <h2>🔐 Admin Control Sign-In</h2>
        <form method="POST">
            <label>Admin Username:</label><input type="text" name="username" required>
            <label>Admin Password:</label><input type="password" name="password" required>
            <button type="submit" class="btn">Login</button>
        </form>
    </div></body></html>
    """)

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        prices['child_panel_monthly'] = int(request.form.get('monthly', prices['child_panel_monthly']))
        prices['child_panel_yearly'] = int(request.form.get('yearly', prices['child_panel_yearly']))
        
    orders_html = "".join([f"<tr><td>#{o['id']}</td><td>{o['link']}</td><td>{o['quantity']}</td><td><span class='badge badge-success'>{o['status']}</span></td></tr>" for o in orders])
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Admin Dashboard</title>{BASE_CSS}</head>
    <body>
        <div class="navbar" style="background:#13141c;">
            <span style="color:#38ef7d; font-weight:bold;">👑 Master Admin Panel</span>
            <div class="links"><a href="/admin/logout">Logout</a></div>
        </div>
        <div class="container">
            <h2>⚙️ Dynamic Child Panel Pricing Management</h2>
            <form method="POST">
                <label>Set Monthly Price (₹):</label>
                <input type="number" name="monthly" value="{prices['child_panel_monthly']}">
                <label>Set Yearly Price (₹):</label>
                <input type="number" name="yearly" value="{prices['child_panel_yearly']}">
                <button type="submit" class="btn" style="background:#38ef7d;">Save & Update Rates</button>
            </form>
            
            <h2 style='margin-top:45px;'>📦 Live Customer Orders Logs</h2>
            <table>
                <thead><tr><th>ID</th><th>Target URL</th><th>Qty</th><th>Status</th></tr></thead>
                <tbody>
                    {orders_html if orders else "<tr><td colspan='4' style='text-align:center; color:#8a99ad;'>No user orders recorded yet.</td></tr>"}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
    
