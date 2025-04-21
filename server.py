from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import socket
import json
import os

app = Flask(__name__)
app.secret_key = 'secret123'

BLOCKED_FILE = 'blocked_domains.json'

# Load blocked domains from file
def load_blocked_domains():
    if not os.path.exists(BLOCKED_FILE):
        return {}
    with open(BLOCKED_FILE, 'r') as f:
        return json.load(f)

# Save blocked domains to file
def save_blocked_domains(data):
    with open(BLOCKED_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Resolve domain to IPs
def resolve_domain(domain):
    try:
        _, _, ip_list = socket.gethostbyname_ex(domain)
        return ip_list
    except Exception as e:
        print(f"Error resolving {domain}: {e}")
        return []

# Block using netsh
def block_ip_windows(ip_address):
    try:
        for direction in ['in', 'out']:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name=Block_{ip_address}_{direction}',
                f'dir={direction}',
                'action=block',
                f'remoteip={ip_address}',
                'protocol=ANY'
            ], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Unblock using netsh
def unblock_ip_windows(ip_address):
    try:
        for direction in ['in', 'out']:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name=Block_{ip_address}_{direction}'
            ], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    blocked_domains = load_blocked_domains()

    if request.method == 'POST':
        domain = request.form.get('block_domain')
        if domain:
            resolved_ips = resolve_domain(domain)
            if resolved_ips:
                blocked_domains[domain] = resolved_ips
                for ip in resolved_ips:
                    block_ip_windows(ip)
                save_blocked_domains(blocked_domains)
                flash(f"{domain} blocked successfully!", "success")
            else:
                flash("Failed to resolve domain.", "danger")
        return redirect(url_for('index'))

    return render_template('index.html', blocked=blocked_domains)

@app.route('/unblock', methods=['POST'])
def unblock():
    blocked_domains = load_blocked_domains()
    domain = request.form.get('unblock_domain')

    if domain in blocked_domains:
        for ip in blocked_domains[domain]:
            unblock_ip_windows(ip)
        del blocked_domains[domain]
        save_blocked_domains(blocked_domains)
        flash(f"{domain} unblocked successfully!", "success")
    else:
        flash(f"{domain} not found in blocked list.", "danger")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
