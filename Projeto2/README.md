# Online Retail System - Relational Design & SQL (BD Project - Part 2)

This project is the second phase of the **Databases** (Bases de Dados) project for LEIC, Instituto Superior Técnico (2022/2023). This stage focuses on translating a conceptual Entity-Relationship (ER) model into a formal **Relational Model** and implementing it using **PostgreSQL**.


## Project Overview

The project manages an e-commerce ecosystem including customers, orders, products, suppliers, and workplace logistics (warehouses and offices). It bridges the gap between high-level design and a functional, queried database.

### Key Components
* **Relational Schema**: Translation of the ER diagram into tables, identifying primary keys, foreign keys, and specific integrity constraints.
* **Relational Algebra**: Formal queries to retrieve specific data sets (e.g., identifying customers who bought products from all suppliers).
* **SQL Implementation**:
    * `schema.sql`: Data Definition Language (DDL) to create the table structure.
    * `populate.sql`: Data Manipulation Language (DML) to seed the database with test data.
    * `queries.sql`: Complex analytical queries (aggregations, joins, and subqueries).

## Database Structure

The schema covers several interconnected domains:
* **Users & Logistics**: Management of Employees, Departments, and Workplaces (Offices/Warehouses).
* **Commercial Flow**: Tracking Products (SKUs/EANs), Suppliers, and Supply Contracts.
* **Sales Cycle**: Customer profiles, Orders, and the final Sales transactions.
