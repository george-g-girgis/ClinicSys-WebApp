# ClinicSys — Web App

A full-featured **Clinic Management System** web application built with **Flask** and **SQLite**.

## Features
- **Patient Management** — Register, search, edit, delete patients with medical history tracking
- **Doctor Management** — Manage doctor profiles with specialty dropdowns
- **Inventory Management** — Track medical supplies with pricing, quantity, expiry dates, and predefined item dropdowns
- **Billing & Payments** — Create bills linked to inventory items with automatic stock deduction/restoration
- **User Authentication** — Login system with bcrypt-hashed passwords and role-based access
- **CSV Export** — Export any table to CSV
- **Real-time Sync** — Auto-polling state hash for multi-client synchronization
- **Smart ID Recycling** — Deleted IDs are automatically reused by new entries

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/george-g-girgis/ClinicSys-WebApp.git
cd ClinicSys-WebApp

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Default Login
On first run, the database is initialized with a default admin account:
- **Username:** `admin`
- **Password:** `admin123`

## Tech Stack
- **Backend:** Python 3.11+, Flask
- **Database:** SQLite3
- **Frontend:** Bootstrap 5, Jinja2 templates
- **Auth:** bcrypt password hashing

## Project Structure
```
├── app.py              # Flask application (routes, logic)
├── database.py         # SQLite schema, migrations, helpers
├── auth.py             # Authentication utilities
├── i18n.py             # Internationalization / translations
├── requirements.txt
├── .gitignore
└── templates/
    ├── base.html       # Layout template
    ├── login.html
    ├── patients.html
    ├── doctors.html
    ├── inventory.html
    ├── billing.html
    └── users.html
```
