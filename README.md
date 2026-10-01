# Simple Web-Based CRM (Flask)

A small Flask web application for managing customer records: add, update,
delete, and view customers in a formatted table.

## Features

- Add new customers (name, email, phone, company, notes)
- Edit/update existing customer records
- Delete customer records (with confirmation)
- View all customers in a clean, formatted table
- Data persisted locally in a SQLite database (`crm.db`), created
  automatically on first run

## Project Structure

```
flask_crm/
├── app.py                 # Main Flask application (routes + DB logic)
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── templates/
    ├── base.html           # Shared layout and styling
    ├── index.html          # Customer list page
    └── form.html           # Add/Edit customer form
```

## Requirements

- Python 3.8+
- Flask (see `requirements.txt`)

## Setup & Installation

1. **Clone or copy the project files** into a folder, e.g. `flask_crm/`.

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

From inside the `flask_crm/` folder, run:

```bash
python app.py
```

The app will:
- Automatically create `crm.db` and the `customers` table if they don't exist.
- Start a local development server, by default at:

  ```
  http://127.0.0.1:5000/
  ```

Open that URL in your browser to use the CRM.

## Usage

- **View customers:** The home page (`/`) lists all customers in a table.
- **Add a customer:** Click "+ Add New Customer", fill in the form
  (Name and Email are required), and submit.
- **Edit a customer:** Click "Edit" next to a customer's row.
- **Delete a customer:** Click "Delete" next to a customer's row and confirm.

## Notes

- This app uses Flask's built-in development server (`debug=True`), which is
  suitable for learning/demo purposes but **not** for production use.
- The database file `crm.db` will be created in the same directory as `app.py`.
- To reset all data, simply delete `crm.db` and restart the app — it will be
  recreated automatically.
- The `secret_key` in `app.py` is used only for flash messages; change it if
  you plan to deploy this beyond local use.
