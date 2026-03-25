# Online Retail Information System (BD Projects 2022/2023)

This repository contains the full three-phase development of a relational database system for an online retail company, developed for the **Databases** (Bases de Dados) course at Instituto Superior Técnico.

---

## Phase 1: Conceptual Design
**Goal:** Translate business requirements into a formal data architecture.
* **ER Model**: A high-level diagram capturing entities like Customers, Orders, Products, and Suppliers, along with their relationships and cardinalities.
* **Integrity Constraints**: Defining domain and business rules (e.g., privacy restrictions on customer names).

---

## Phase 2: Relational Implementation & SQL
**Goal:** Transform the conceptual model into a functional PostgreSQL database.
* **Relational Mapping**: Conversion of the ER diagram into a set of normalized tables with Primary and Foreign Keys.
* **Relational Algebra**: Formal query expressions to solve complex data retrieval problems.
* **SQL Development**: 
    * `schema.sql`: DDL for table creation.
    * `populate.sql`: Script to seed the database with consistent test data.
    * `queries.sql`: Implementation of multi-table joins and aggregations.

---

## Phase 3: Advanced Features & Analytics
**Goal:** Implement complex business logic, a user interface, and Business Intelligence (BI) capabilities.
* **Triggers & Stored Procedures**: Automated enforcement of complex rules (e.g., age verification and disjoint entity constraints).
* **Web Prototype**: A functional interface built with **Python (Flask)** and **Psycopg2** to interact with the database in real-time.
* **OLAP (On-Line Analytical Processing)**: 
    * Design of a **Star Schema** for data warehousing.
    * Analytical queries using `ROLLUP` and `CUBE` for multidimensional sales analysis.
