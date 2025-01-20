from flask import Flask, render_template, request, redirect, url_for, session, flash
from mysql import connector

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Fungsi koneksi ke database
def get_db_connection():
    return connector.connect(
        host="i-n-w.h.filess.io",  # Ganti hostname menjadi host
        database="absensi_creamfatus",
        port="3307",
        user="absensi_creamfatus",  # Ganti username menjadi user
        password="7094460c9c6779113753116a9e12b6b3f2f6d3b3"
    )



# Home page or student absens route
@app.route('/')
def student_absens():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM web')
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('student_absens.html', hasil=result)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        cursor.close()
        db.close()
        
        if admin:
            session['admin'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# Admin dashboard route
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM web')
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('dashboard.html', hasil=result)

# Add user route
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']
        
        db = get_db_connection()
        cursor = db.cursor()
        query = "INSERT INTO web (nama, nim, jurusan) VALUES (%s, %s, %s)"
        values = (nama, nim, jurusan)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        db.close()
        
        return redirect(url_for('dashboard'))

# Update user route
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        # Get form data
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']

        # Update the user in the database
        query = "UPDATE web SET nama = %s, nim = %s, jurusan = %s WHERE id = %s"
        values = (nama, nim, jurusan, user_id)
        cursor.execute(query, values)
        db.commit()

        flash('User information updated successfully!', 'success')
        cursor.close()
        db.close()

        # Redirect back to the dashboard after successful update
        return redirect(url_for('dashboard'))

    # If GET request, fetch the student data to pre-fill the form
    cursor.execute('SELECT * FROM web WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        return render_template('update_user.html', user=user)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

# Delete user route
@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('DELETE FROM web WHERE id = %s', (user_id,))
    db.commit()
    cursor.close()
    db.close()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('student_absens'))

# Route for calendar (placeholder example)
@app.route('/student-calendar')
def student_calendar():
    return render_template('student-calendar.html')

if __name__ == '__main__':
    app.run(debug=True)
