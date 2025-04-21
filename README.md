

```markdown
# 🔒 BlockMate — Website Firewall Controller

BlockMate is a simple yet effective parental control and firewall management web app built with Flask (Python) and basic HTML. It allows users to **block or unblock websites** at the IP level by dynamically modifying Windows firewall rules.

---

## ⚙️ Features

- 🌐 Block any website by domain name (resolved to IP addresses).
- 🧹 Unblock previously blocked websites.
- 💾 Persistent storage of blocked websites in a JSON file.
- 🛡️ Uses Windows built-in firewall (`netsh`) commands.
- 🧠 Simple web interface with forms to manage the firewall.

---

## 🚀 Getting Started

### ⚠️ Requirements

- **Windows OS**
- **Python 3.8+**
- **Administrator privileges** (required for modifying firewall rules)

---

### 🖥️ Setup Instructions

1. **Clone the repository** (or copy your project folder):

```bash
cd path\to\your\project\BlockMate
```

2. **Create and activate virtual environment:**

```bash
python -m venv firewall-env
.\firewall-env\Scripts\activate
```

> ✅ You can rename the environment to `blockmate-env` or anything else, just adjust the path accordingly.

3. **Install dependencies:**

```bash
pip install flask
```

---

### ▶️ Run the Application

```bash
python server.py
```

Visit the app in your browser:

```
http://127.0.0.1:5000/
```

---

## 📂 Project Structure

```
BlockMate/
│
├── server.py                  # Flask backend server
├── blocked_domains.json       # Stores blocked domain-IP mappings
├── templates/
│   └── index.html             # Main HTML interface (Jinja2 template)
├── static/
│   └── style.css              # Custom styles
├── firewall-env/              # Virtual environment folder
└── README.md                  # You're reading it!
```

---

## 🧠 How It Works (Network & CN Focus)

- Uses **DNS resolution** (`socket.gethostbyname_ex`) to fetch IPs of domains.
- Applies **firewall rules** using `netsh advfirewall`, a key **CN concept** for managing network-level traffic.
- Simulates **packet filtering firewall behavior** directly from a user interface.
- Demonstrates **client-server communication** in a controlled network environment.

---

## ❗ Admin Privileges Note

To allow the app to modify Windows firewall rules:

- Run your terminal as **Administrator** before launching the server.
- If not, firewall changes will fail silently or throw permission errors.

---

## ✨ Future Improvements

- Logging blocked attempts.
- Role-based access (e.g., parental lock).
- Platform-independent support (Linux/macOS).

