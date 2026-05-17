import os
import sys

# Ensure the parent directory is in the Python path so we can import our backend logic
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import csv, io
from database import get_connection, init_db, get_next_available_id
from auth import verify_login

# Initialize the Flask app
app = Flask(__name__)
# Secret key is required for securely signing the session cookies
app.secret_key = "clinic_sys_secure_secret_key_123"

# Inject the translation function into Jinja globally
@app.context_processor
def inject_i18n():
    def translate_jinja(key):
        import i18n
        i18n._current_lang = session.get('lang', 'en')
        return i18n.t(key)
    return dict(t=translate_jinja)

# Initialize the main DB just in case it hasn't been created
init_db()

# -----------------------------------------------------------------------------
# Dependency Rules
# -----------------------------------------------------------------------------
def login_required(role_needed=None):
    """Decorator logic for enforcing login status manually inside routes."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for('login'))
            if role_needed and session.get("role") != role_needed:
                flash("You do not have permission to access that area.", "danger")
                return redirect(url_for('dashboard'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.route('/')
def dashboard():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return redirect(url_for('patients'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'warning')
            return redirect(url_for('login'))
            
        success, role = verify_login(username, password)
        if success:
            session['user_id'] = username
            session['role'] = role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/set_lang/<lang>')
def set_lang(lang):
    if lang in ['en', 'ar']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/toggle_theme')
def toggle_theme():
    current = session.get('theme', 'light')
    session['theme'] = 'dark' if current == 'light' else 'light'
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/export/<table_name>')
@login_required()
def export_csv(table_name):
    allowed_tables = ['Patients', 'Doctors', 'Inventory', 'Billing', 'Admin_Users']
    if table_name not in allowed_tables:
        flash("Invalid table export requested.", "danger")
        return redirect(url_for('dashboard'))
    
    if table_name == 'Admin_Users' and session.get('role') != 'admin':
        flash("Unauthorized export.", "danger")
        return redirect(url_for('dashboard'))

    conn = get_connection()
    try:
        rows = conn.execute(f"SELECT * FROM {table_name} ORDER BY ID").fetchall()
    finally:
        conn.close()

    if not rows:
        flash("No data available to export.", "warning")
        return redirect(request.referrer or url_for('dashboard'))

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(rows[0].keys())  # Columns header
    for r in rows:
        cw.writerow(list(r))
    
    return Response(
        si.getvalue().encode('utf-8-sig'),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={table_name.lower()}_data.csv"}
    )


@app.route('/patients', methods=['GET', 'POST'])
@login_required()
def patients():
    conn = get_connection()
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                name = request.form.get('full_name', '').strip()
                dob = request.form.get('dob', '').strip()
                phone = request.form.get('phone', '').strip()
                history = request.form.get('history', '').strip()
                allergies = request.form.get('allergies', '').strip()
                if allergies == 'Other...':
                    allergies = request.form.get('allergies_other', '').strip()
                next_appt = request.form.get('next_appt', '').strip()

                age = None
                if dob:
                    try:
                        from datetime import datetime
                        d = datetime.strptime(dob, '%Y-%m-%d')
                        today = datetime.today()
                        age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
                    except ValueError:
                        pass
                
                if phone and (not phone.isdigit() or len(phone) != 11):
                    flash('Phone number must be exactly 11 digits.', 'danger')
                    return redirect(url_for('patients'))
                
                if name:
                    next_id = get_next_available_id(conn, "Patients")
                    conn.execute(
                        "INSERT INTO Patients (ID, FullName, Age, PhoneNumber, MedicalHistory, Allergies, NextAppointment, DOB) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (next_id, name, age, phone, history, allergies, next_appt, dob)
                    )
                    conn.commit()
                    flash('Patient added successfully!', 'success')
                else:
                    flash('Full name is required!', 'danger')
                    
            elif action == 'edit':
                pid = request.form.get('id')
                name = request.form.get('full_name', '').strip()
                dob = request.form.get('dob', '').strip()
                phone = request.form.get('phone', '').strip()
                history = request.form.get('history', '').strip()
                allergies = request.form.get('allergies', '').strip()
                if allergies == 'Other...':
                    allergies = request.form.get('allergies_other', '').strip()
                next_appt = request.form.get('next_appt', '').strip()
                
                age = None
                if dob:
                    try:
                        from datetime import datetime
                        d = datetime.strptime(dob, '%Y-%m-%d')
                        today = datetime.today()
                        age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
                    except ValueError:
                        pass

                if phone and (not phone.isdigit() or len(phone) != 11):
                    flash('Phone number must be exactly 11 digits.', 'danger')
                    return redirect(url_for('patients'))
                
                if name and pid:
                    conn.execute(
                        "UPDATE Patients SET FullName=?, Age=?, PhoneNumber=?, MedicalHistory=?, Allergies=?, NextAppointment=?, DOB=? WHERE ID=?",
                        (name, age, phone, history, allergies, next_appt, dob, pid)
                    )
                    conn.commit()
                    flash('Patient updated successfully!', 'success')
                    
            elif action == 'delete':
                pid = request.form.get('id')
                if pid:
                    import sqlite3
                    try:
                        conn.execute("DELETE FROM Patients WHERE ID = ?", (pid,))
                        conn.commit()
                        flash('Patient deleted successfully!', 'success')
                    except sqlite3.IntegrityError:
                        flash('Cannot delete patient: Linked billing records exist. Please delete them first.', 'danger')
            
            return redirect(url_for('patients'))
            
        q = request.args.get('q', '').strip()
        if q:
            rows = conn.execute("SELECT * FROM Patients WHERE FullName LIKE ? ORDER BY ID ASC", (f"%{q}%",)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM Patients ORDER BY ID ASC").fetchall()
    finally:
        conn.close()
        
    return render_template('patients.html', patients=rows)


@app.route('/doctors', methods=['GET', 'POST'])
@login_required()
def doctors():
    conn = get_connection()
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                name = request.form.get('name', '').strip()
                specialty = request.form.get('specialty', '').strip()
                if specialty == 'Other...':
                    specialty = request.form.get('specialty_other', '').strip()
                phone = request.form.get('phone', '').strip()
                
                if phone and (not phone.isdigit() or len(phone) != 11):
                    flash('Phone number must be exactly 11 digits.', 'danger')
                    return redirect(url_for('doctors'))

                if name:
                    next_id = get_next_available_id(conn, "Doctors")
                    conn.execute(
                        "INSERT INTO Doctors (ID, Name, Specialty, PhoneNumber) VALUES (?, ?, ?, ?)",
                        (next_id, name, specialty, phone)
                    )
                    conn.commit()
                    flash('Doctor added successfully!', 'success')
                else:
                    flash('Doctor name is required!', 'danger')
                    
            elif action == 'edit':
                did = request.form.get('id')
                name = request.form.get('name', '').strip()
                specialty = request.form.get('specialty', '').strip()
                if specialty == 'Other...':
                    specialty = request.form.get('specialty_other', '').strip()
                phone = request.form.get('phone', '').strip()
                
                if phone and (not phone.isdigit() or len(phone) != 11):
                    flash('Phone number must be exactly 11 digits.', 'danger')
                    return redirect(url_for('doctors'))

                if name and did:
                    conn.execute(
                        "UPDATE Doctors SET Name=?, Specialty=?, PhoneNumber=? WHERE ID=?",
                        (name, specialty, phone, did)
                    )
                    conn.commit()
                    flash('Doctor updated successfully!', 'success')
                    
            elif action == 'delete':
                did = request.form.get('id')
                if did:
                    conn.execute("DELETE FROM Doctors WHERE ID = ?", (did,))
                    conn.commit()
                    flash('Doctor deleted successfully!', 'success')
                    
            return redirect(url_for('doctors'))
            
        q = request.args.get('q', '').strip()
        if q:
            rows = conn.execute("SELECT * FROM Doctors WHERE Name LIKE ? ORDER BY ID ASC", (f"%{q}%",)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM Doctors ORDER BY ID ASC").fetchall()
    finally:
        conn.close()
        
    return render_template('doctors.html', doctors=rows)


@app.route('/inventory', methods=['GET', 'POST'])
@login_required()
def inventory():
    conn = get_connection()
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                item_name_select = request.form.get('item_name_select', '').strip()
                item_name = item_name_select if item_name_select != 'Other' else request.form.get('item_name_other', '').strip()
                price_str = request.form.get('price', '0').strip()
                
                try: price = float(price_str)
                except ValueError: price = 0.0
                
                quantity = request.form.get('quantity', '0').strip()
                expiry = request.form.get('expiry_date', '').strip()
                
                if item_name and quantity.isdigit():
                    next_id = get_next_available_id(conn, "Inventory")
                    conn.execute("INSERT INTO Inventory (ID, ItemName, Quantity, Price, ExpiryDate) VALUES (?, ?, ?, ?, ?)",
                                 (next_id, item_name, int(quantity), price, expiry))
                    conn.commit()
                    flash('Item added successfully!', 'success')
                else:
                    flash('Invalid item name or quantity!', 'danger')
                    
            elif action == 'edit':
                iid = request.form.get('id')
                item_name_select = request.form.get('item_name_select', '').strip()
                item_name = item_name_select if item_name_select != 'Other' else request.form.get('item_name_other', '').strip()
                price_str = request.form.get('price', '0').strip()
                
                try: price = float(price_str)
                except ValueError: price = 0.0
                
                quantity = request.form.get('quantity', '0').strip()
                expiry = request.form.get('expiry_date', '').strip()
                
                if item_name and quantity.isdigit() and iid:
                    conn.execute("UPDATE Inventory SET ItemName=?, Quantity=?, Price=?, ExpiryDate=? WHERE ID=?",
                                 (item_name, int(quantity), price, expiry, iid))
                    conn.commit()
                    flash('Item updated!', 'success')
                    
            elif action == 'delete':
                iid = request.form.get('id')
                if iid:
                    conn.execute("DELETE FROM Inventory WHERE ID=?", (iid,))
                    conn.commit()
                    flash('Item removed!', 'success')
                    
            return redirect(url_for('inventory'))
            
        q = request.args.get('q', '').strip()
        if q:
            rows = conn.execute("SELECT * FROM Inventory WHERE ItemName LIKE ? ORDER BY ID ASC", (f"%{q}%",)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM Inventory ORDER BY ID ASC").fetchall()
    finally:
        conn.close()
    return render_template('inventory.html', inventory=rows)


@app.route('/billing', methods=['GET', 'POST'])
@login_required()
def billing():
    conn = get_connection()
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                pid = request.form.get('patient_id')
                amount_str = request.form.get('amount', '').strip()
                date = request.form.get('date', '').strip()
                status = request.form.get('status', 'Pending').strip()
                item_id_str = request.form.get('item_id', '')
                item_qty_str = request.form.get('item_qty', '0').strip()
                
                try:
                    amount = float(amount_str)
                except ValueError:
                    flash('Invalid amount format! Bill not accepted.', 'danger')
                    return redirect(url_for('billing'))
                    
                item_qty = int(item_qty_str) if item_qty_str.isdigit() else 0
                item_id = int(item_id_str) if item_id_str.isdigit() else None
                
                if pid and date:
                    next_id = get_next_available_id(conn, "Billing")
                    conn.execute("INSERT INTO Billing (ID, Patient_ID, Amount, Date, Status, Item_ID, Item_Qty) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (next_id, pid, amount, date, status, item_id, item_qty))
                    if item_id and item_qty > 0:
                        conn.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE ID = ?", (item_qty, item_id))
                    conn.commit()
                    flash('Bill created!', 'success')
                else:
                    flash('Missing required fields!', 'danger')
                    
            elif action == 'edit':
                bid = request.form.get('id')
                pid = request.form.get('patient_id')
                amount_str = request.form.get('amount', '').strip()
                date = request.form.get('date', '').strip()
                status = request.form.get('status', 'Pending').strip()
                item_id_str = request.form.get('item_id', '')
                item_qty_str = request.form.get('item_qty', '0').strip()
                
                try:
                    amount = float(amount_str)
                except ValueError:
                    flash('Invalid amount format! Update aborted.', 'danger')
                    return redirect(url_for('billing'))
                    
                item_qty = int(item_qty_str) if item_qty_str.isdigit() else 0
                item_id = int(item_id_str) if item_id_str.isdigit() else None
                
                if bid and pid and date:
                    # Reverse previous inventory deduction
                    r = conn.execute("SELECT Item_ID, Item_Qty FROM Billing WHERE ID=?", (bid,)).fetchone()
                    if r and r['Item_ID'] is not None and r['Item_Qty']:
                        conn.execute("UPDATE Inventory SET Quantity = Quantity + ? WHERE ID = ?", (r['Item_Qty'], r['Item_ID']))
                        
                    # Apply new billing entry and new deduction
                    conn.execute("UPDATE Billing SET Patient_ID=?, Amount=?, Date=?, Status=?, Item_ID=?, Item_Qty=? WHERE ID=?",
                                 (pid, amount, date, status, item_id, item_qty, bid))
                    if item_id and item_qty > 0:
                        conn.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE ID = ?", (item_qty, item_id))
                    conn.commit()
                    flash('Bill updated!', 'success')
                    
            elif action == 'delete':
                bid = request.form.get('id')
                if bid:
                    # Restore inventory before wiping out the bill
                    r = conn.execute("SELECT Item_ID, Item_Qty FROM Billing WHERE ID=?", (bid,)).fetchone()
                    if r and r['Item_ID'] is not None and r['Item_Qty']:
                        conn.execute("UPDATE Inventory SET Quantity = Quantity + ? WHERE ID = ?", (r['Item_Qty'], r['Item_ID']))
                        
                    conn.execute("DELETE FROM Billing WHERE ID=?", (bid,))
                    conn.commit()
                    flash('Bill removed!', 'success')
            
            elif action == 'update_status':
                bid = request.form.get('id')
                status = request.form.get('status')
                if bid and status in ('Paid', 'Pending'):
                    conn.execute("UPDATE Billing SET Status=? WHERE ID=?", (status, bid))
                    conn.commit()
                    flash('Bill status updated!', 'success')

            return redirect(url_for('billing'))
            
        # For the dropdown and bills
        patients = conn.execute("SELECT ID, FullName FROM Patients ORDER BY FullName").fetchall()
        inventory_items = conn.execute("SELECT ID, ItemName, Quantity FROM Inventory ORDER BY ItemName").fetchall()
        
        q = request.args.get('q', '').strip()
        if q:
            bills = conn.execute('''
                SELECT b.ID, p.FullName, b.Amount, b.Date, b.Status, b.Patient_ID, b.Item_ID, b.Item_Qty, i.ItemName, i.Price
                FROM Billing b JOIN Patients p ON b.Patient_ID = p.ID 
                LEFT JOIN Inventory i ON b.Item_ID = i.ID
                WHERE p.FullName LIKE ?
                ORDER BY b.ID ASC
            ''', (f"%{q}%",)).fetchall()
        else:
            bills = conn.execute('''
                SELECT b.ID, p.FullName, b.Amount, b.Date, b.Status, b.Patient_ID, b.Item_ID, b.Item_Qty, i.ItemName, i.Price
                FROM Billing b JOIN Patients p ON b.Patient_ID = p.ID 
                LEFT JOIN Inventory i ON b.Item_ID = i.ID
                ORDER BY b.ID ASC
            ''').fetchall()
    finally:
        conn.close()
        
    from datetime import datetime
    now_dt = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('billing.html', bills=bills, patients=patients, inventory_items=inventory_items, now_dt=now_dt)


@app.route('/users', methods=['GET', 'POST'])
@login_required(role_needed='admin')
def users():
    import bcrypt
    conn = get_connection()
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()
                role = request.form.get('role', 'staff').strip()
                
                if username and password:
                    try:
                        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        conn.execute("INSERT INTO Admin_Users (Username, PasswordHash, Role) VALUES (?, ?, ?)",
                                     (username, hashed, role))
                        conn.commit()
                        flash('User added!', 'success')
                    except Exception:
                        flash('Username exists!', 'danger')
                else:
                    flash('Username and Password required!', 'danger')
                    
            elif action == 'edit':
                uid = request.form.get('id')
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()
                role = request.form.get('role', 'staff').strip()
                
                if uid and username:
                    if password:
                        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        conn.execute("UPDATE Admin_Users SET Username=?, PasswordHash=?, Role=? WHERE ID=?",
                                     (username, hashed, role, uid))
                    else:
                        conn.execute("UPDATE Admin_Users SET Username=?, Role=? WHERE ID=?",
                                     (username, role, uid))
                    conn.commit()
                    flash('User updated!', 'success')
                    
            elif action == 'delete':
                uid = request.form.get('id')
                count = conn.execute("SELECT COUNT(*) FROM Admin_Users").fetchone()[0]
                if count <= 1:
                    flash('Cannot delete last admin!', 'danger')
                elif uid:
                    conn.execute("DELETE FROM Admin_Users WHERE ID=?", (uid,))
                    conn.commit()
                    flash('User deleted!', 'success')
                    
            return redirect(url_for('users'))
            
        q = request.args.get('q', '').strip()
        if q:
            rows = conn.execute("SELECT ID, Username, Role FROM Admin_Users WHERE Username LIKE ? ORDER BY ID ASC", (f"%{q}%",)).fetchall()
        else:
            rows = conn.execute("SELECT ID, Username, Role FROM Admin_Users ORDER BY ID ASC").fetchall()
    finally:
        conn.close()
    return render_template('users.html', users=rows)

@app.route('/api/sync_state')
@login_required()
def sync_state():
    conn = get_connection()
    try:
        # Generate a checksum mapping for total DB changes (inserts/deletes/updates across models)
        c = conn.execute('''
            SELECT 
                (SELECT COUNT(*) FROM Patients) +
                (SELECT COUNT(*) FROM Doctors) +
                (SELECT COUNT(*) FROM Inventory) +
                (SELECT COUNT(*) FROM Billing) as cnt,
                IFNULL((SELECT SUM(Age) FROM Patients), 0) +
                IFNULL((SELECT SUM(Quantity) FROM Inventory), 0) +
                IFNULL((SELECT SUM(Amount) FROM Billing), 0) +
                IFNULL((SELECT SUM(LENGTH(Status)) FROM Billing), 0) +
                IFNULL((SELECT SUM(LENGTH(FullName)) FROM Patients), 0) as stats
        ''').fetchone()
        state_hash = f"{c['cnt']}-{c['stats']}"
        return jsonify({"version": state_hash})
    finally:
        conn.close()

if __name__ == '__main__':
    # Run server locally on 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
