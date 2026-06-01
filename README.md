# Real Estate Property Management System

ITAP3010 Group Project

## Tech Stack
- Python 3.10
- Tkinter (GUI)
- MySQL (Database)
- matplotlib (Charts)

## Setup Instructions

### Step 1: Install Python packages
```
pip install mysql-connector-python matplotlib
```

### Step 2: Create the database
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Open the file `database/real_estate_db.sql`
4. Click the lightning bolt to execute the entire script
5. You should see `real_estate_pms` database in your SCHEMAS panel

### Step 3: Update database password
Open `database/db_connection.py` and change `your_password_here` to your MySQL root password.

### Step 4: Setup admin users
```
python setup_admin.py
```

### Step 5: Run the application
```
python main.py
```

## Default Login
- Username: `admin`     Password: `admin123`
- Username: `manager1`  Password: `manager123`

## Project Structure
```
real_estate_pms/
├── main.py
├── setup_admin.py
├── README.md
├── database/
│   ├── db_connection.py
│   └── real_estate_db.sql
├── modules/
│   ├── controller/
│   │   ├── auth_controller.py
│   │   ├── business_logic.py
│   │   ├── landlord_controller.py
│   │   ├── property_controller.py
│   │   ├── tenant_controller.py
│   │   ├── lease_controller.py
│   │   ├── payment_controller.py
│   │   └── maintenance_controller.py
        └── user_controller.py
│   └── views/
│       ├── login_view.py
│       ├── landlord_view.py
│       ├── property_view.py
│       ├── tenant_view.py
│       ├── lease_view.py
│       ├── payment_view.py
│       ├── maintenance_view.py
│       └── reports_view.py
        └── user_view.py
├── reports/
├── tests/
└── screenshots/
```
