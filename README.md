# Real Estate Property Management System

## Tech Stack
- Python 3.10+
- Tkinter (GUI)
- MySQL 8.0+ (Database)
- matplotlib (Charts)
- mysql-connector-python

## Setup Instructions

### 1. Install Python dependencies
```bash
pip install mysql-connector-python matplotlib
```

### 2. Set up MySQL database
1. Install MySQL Workbench and MySQL Server
2. Open MySQL Workbench
3. Open and run `database/real_estate_db.sql`
4. This creates the `real_estate_pms` database with all tables and sample data

### 3. Configure database connection
1. Open `database/db_connection.py`
2. Update the `DB_CONFIG` dictionary with your local MySQL password

### 4. Create admin account
Run this once to set up your first admin user (do this after running the SQL script):
```bash
python setup_admin.py
```

### 5. Run the application
```bash
python main.py
```

Default login (after setup_admin.py runs):
- Username: `admin`
- Password: `admin123`

## Project Structure
```
real_estate_pms/
├── main.py                 # App entry point
├── setup_admin.py          # One-time admin setup
├── README.md
├── database/
│   ├── real_estate_db.sql  # Schema + sample data
│   └── db_connection.py    # Connection module
├── modules/
│   ├── auth.py             # Login system
│   ├── crud_template.py    # Generic CRUD base
│   ├── properties.py
│   ├── landlords.py
│   ├── tenants.py
│   ├── lease_agreements.py
│   ├── rental_payments.py
│   └── maintenance_requests.py
├── reports/
│   └── reports.py          # Reports + matplotlib charts
├── tests/
│   └── test_cases.py
└── screenshots/            # For the Word report
```
