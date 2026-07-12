from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

@app.route('/')
def home():
    return "<h1>Welcome to Boost SMM Panel!</h1><p>Website is working perfectly.</p><a href='/admin'>Go to Admin Panel</a>"

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Credentials! <a href='/admin'>Try Again</a>"
    return '''
        <h2>Admin Login</h2>
        <form method="POST">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return "<h2>Welcome to Admin Dashboard</h2><p>Here you can manage your SMM services and orders soon!</p><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
  
