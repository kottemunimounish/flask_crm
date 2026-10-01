"""
Simple Web-Based CRM System
----------------------------
A Flask application that lets users add, update, delete, and view
customer records stored in a local SQLite database.
"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # needed for flash messages

DATABASE = "crm.db"


def get_db_connection():
    """Create a connection to the SQLite database with row access by name."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the customers table if it doesn't already exist."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            company TEXT,
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Display all customer records in a formatted table."""
    conn = get_db_connection()
    customers = conn.execute("SELECT * FROM customers ORDER BY name ASC").fetchall()
    conn.close()
    return render_template("index.html", customers=customers)


@app.route("/add", methods=["GET", "POST"])
def add_customer():
    """Add a new customer record."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        company = request.form.get("company", "").strip()
        notes = request.form.get("notes", "").strip()

        if not name or not email:
            flash("Name and Email are required fields.", "error")
            return redirect(url_for("add_customer"))

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO customers (name, email, phone, company, notes) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, company, notes),
        )
        conn.commit()
        conn.close()
        flash(f"Customer '{name}' added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", customer=None, action="Add")


@app.route("/edit/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    """Update an existing customer record."""
    conn = get_db_connection()
    customer = conn.execute(
        "SELECT * FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()

    if customer is None:
        conn.close()
        flash("Customer not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        company = request.form.get("company", "").strip()
        notes = request.form.get("notes", "").strip()

        if not name or not email:
            flash("Name and Email are required fields.", "error")
            conn.close()
            return redirect(url_for("edit_customer", customer_id=customer_id))

        conn.execute(
            """UPDATE customers
               SET name = ?, email = ?, phone = ?, company = ?, notes = ?
               WHERE id = ?""",
            (name, email, phone, company, notes, customer_id),
        )
        conn.commit()
        conn.close()
        flash(f"Customer '{name}' updated successfully.", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("form.html", customer=customer, action="Edit")


@app.route("/delete/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    """Delete a customer record."""
    conn = get_db_connection()
    customer = conn.execute(
        "SELECT * FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()

    if customer is None:
        flash("Customer not found.", "error")
    else:
        conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        flash(f"Customer '{customer['name']}' deleted.", "success")

    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
