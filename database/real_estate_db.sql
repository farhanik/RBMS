-- Real Estate Property Management System Database

DROP DATABASE IF EXISTS real_estate_pms;
CREATE DATABASE real_estate_pms;
USE real_estate_pms;

-- Users table for login
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Manager') NOT NULL DEFAULT 'Manager',
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Landlords table
CREATE TABLE Landlords (
    landlord_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Properties table
CREATE TABLE Properties (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    landlord_id INT NOT NULL,
    address VARCHAR(255) NOT NULL,
    suburb VARCHAR(100) NOT NULL,
    property_type ENUM('Apartment', 'House', 'Townhouse', 'Studio', 'Unit') NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    monthly_rent DECIMAL(10, 2) NOT NULL,
    status ENUM('Available', 'Leased', 'Maintenance') NOT NULL DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (landlord_id) REFERENCES Landlords(landlord_id) ON DELETE RESTRICT,
    INDEX idx_property_status (status),
    INDEX idx_property_suburb (suburb)
);

-- Tenants table
CREATE TABLE Tenants (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    emergency_contact_name VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lease Agreements table
CREATE TABLE Lease_Agreements (
    lease_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    tenant_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthly_rent DECIMAL(10, 2) NOT NULL,
    bond_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Active', 'Expired', 'Terminated') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE RESTRICT,
    FOREIGN KEY (tenant_id) REFERENCES Tenants(tenant_id) ON DELETE RESTRICT,
    INDEX idx_lease_status (status)
);

-- Rental Payments table
CREATE TABLE Rental_Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    lease_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('Bank Transfer', 'Cash', 'Card', 'Cheque') NOT NULL,
    status ENUM('Paid', 'Pending', 'Overdue') NOT NULL DEFAULT 'Paid',
    notes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lease_id) REFERENCES Lease_Agreements(lease_id) ON DELETE RESTRICT,
    INDEX idx_payment_status (status)
);

-- Maintenance Requests table
CREATE TABLE Maintenance_Requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    tenant_id INT NOT NULL,
    description TEXT NOT NULL,
    priority ENUM('Low', 'Medium', 'High', 'Urgent') NOT NULL DEFAULT 'Medium',
    status ENUM('Open', 'In Progress', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Open',
    request_date DATE NOT NULL,
    completion_date DATE,
    cost DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE RESTRICT,
    FOREIGN KEY (tenant_id) REFERENCES Tenants(tenant_id) ON DELETE RESTRICT,
    INDEX idx_request_status (status)
);

-- Sample data
INSERT INTO Users (username, password_hash, role, email, full_name) VALUES
('admin', 'REPLACE_ME', 'Admin', 'admin@realestate.com', 'System Administrator'),
('manager1', 'REPLACE_ME', 'Manager', 'manager@realestate.com', 'Property Manager');

INSERT INTO Landlords (full_name, phone, email, address) VALUES
('John Smith', '0412345678', 'john.smith@email.com', '12 Collins St Melbourne VIC 3000'),
('Sarah Johnson', '0423456789', 'sarah.j@email.com', '45 Bourke St Melbourne VIC 3000'),
('Michael Chen', '0434567890', 'm.chen@email.com', '78 Flinders St Melbourne VIC 3000');

INSERT INTO Properties (landlord_id, address, suburb, property_type, bedrooms, bathrooms, monthly_rent, status) VALUES
(1, '101/200 Spencer St', 'Melbourne', 'Apartment', 2, 1, 2200.00, 'Leased'),
(1, '15 Park Ave', 'Carlton', 'House', 3, 2, 3500.00, 'Available'),
(2, '8/55 King St', 'Melbourne', 'Studio', 1, 1, 1500.00, 'Leased'),
(2, '22 Smith St', 'Fitzroy', 'Townhouse', 3, 2, 2800.00, 'Available'),
(3, '5/100 Chapel St', 'Prahran', 'Apartment', 2, 2, 2400.00, 'Maintenance');

INSERT INTO Tenants (full_name, phone, email, emergency_contact_name, emergency_contact_phone, date_of_birth) VALUES
('Emma Wilson', '0445678901', 'emma.w@email.com', 'David Wilson', '0456789012', '1995-03-15'),
('James Brown', '0467890123', 'james.b@email.com', 'Mary Brown', '0478901234', '1990-07-22');

INSERT INTO Lease_Agreements (property_id, tenant_id, start_date, end_date, monthly_rent, bond_amount, status) VALUES
(1, 1, '2025-01-01', '2025-12-31', 2200.00, 4400.00, 'Active'),
(3, 2, '2025-02-01', '2026-01-31', 1500.00, 3000.00, 'Active');

INSERT INTO Rental_Payments (lease_id, amount, payment_date, payment_method, status, notes) VALUES
(1, 2200.00, '2025-01-01', 'Bank Transfer', 'Paid', 'January rent'),
(1, 2200.00, '2025-02-01', 'Bank Transfer', 'Paid', 'February rent'),
(1, 2200.00, '2025-03-01', 'Bank Transfer', 'Paid', 'March rent'),
(2, 1500.00, '2025-02-01', 'Card', 'Paid', 'February rent'),
(2, 1500.00, '2025-03-01', 'Card', 'Overdue', 'Awaiting payment');

INSERT INTO Maintenance_Requests (property_id, tenant_id, description, priority, status, request_date, completion_date, cost) VALUES
(1, 1, 'Leaking kitchen tap', 'Medium', 'Completed', '2025-02-15', '2025-02-18', 150.00),
(3, 2, 'Broken air conditioner', 'High', 'In Progress', '2025-03-10', NULL, NULL),
(5, 1, 'Repaint living room walls', 'Low', 'Open', '2025-03-20', NULL, NULL);
