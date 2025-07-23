from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)


def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect('database/tickets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            tickets INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tickets = request.form['tickets']

        conn = sqlite3.connect('database/tickets.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, tickets) VALUES (?, ?, ?)",
                  (name, email, tickets))
        booking_id = c.lastrowid 
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation', booking_id=booking_id))
    return render_template('book.html')


@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    conn = sqlite3.connect('database/tickets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    booking = c.fetchone()
    conn.close()

    if booking:
        return render_template('confirmation.html', booking=booking)
    else:
        return "<h3>Booking not found.</h3>"


@app.route('/bookings')
def bookings():
    conn = sqlite3.connect('database/tickets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    all_bookings = c.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=all_bookings)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
