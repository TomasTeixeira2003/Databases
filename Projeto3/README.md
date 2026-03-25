# Online Retail System - Advanced SQL, Triggers & Analytics (BD Project - Part 3)

This is the third and final phase of the **Databases** (Bases de Dados) project for LEIC, Instituto Superior Técnico (2022/2023). This stage focuses on advanced database features, including procedural SQL (Triggers/Stored Procedures), web application prototyping, and OLAP (On-Line Analytical Processing).

## Project Overview

The final phase elevates the "Online Retail" database into a functional system with complex business logic, a Python-based web interface, and analytical capabilities for business intelligence.

### Key Components
* **Database Integrity**: Implementation of complex business rules using **Triggers** and **Stored Procedures**.
* **SQL Programming**: Development of advanced queries involving aggregation, window functions, and subqueries.
* **Web Prototype**: A basic interface developed in **Python (Flask/Psycopg2)** to interact with the PostgreSQL database.
* **Data Analytics (OLAP)**: Design of a Star Schema for a Data Warehouse and execution of multidimensional queries (Roll-up, Drill-down) using SQL `GROUP BY ROLLUP` or `CUBE`.

## Advanced Features

### 1. Integrity Constraints (RI)
Specific business logic implemented via Triggers:
* **RI-1**: Ensures no employee is under 18 years of age.
* **RI-2**: Enforces the disjoint constraint for `Workplace` (must be an `Office` or `Warehouse`, but not both).
* **RI-3**: Ensures every `Order` is linked to at least one product in the `Contains` table.

### 2. Web Application
A Python-based prototype providing:
* **Product Management**: CRUD operations for product listings and prices.
* **Supplier Management**: Viewing and editing supplier details.
* **Order Tracking**: Listing all orders and their current status.

### 3. OLAP & Data Warehousing
Multidimensional analysis focusing on:
* Sales trends over time (daily, monthly, yearly).
* Product performance across different categories and suppliers.
* Geographical distribution of orders.
