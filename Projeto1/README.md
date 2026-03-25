# Online Retail Database (BD Project - Part 1)

This project was developed for the **Databases** (Bases de Dados) course at LEIC, Instituto Superior Técnico (2022/2023). It focuses on the conceptual design of a relational database for an e-commerce platform.

## Project Overview

The objective is to design a robust information system to manage customers, orders, products, and payments for an online retail company. The design emphasizes data integrity, privacy requirements, and the accurate mapping of business rules.

### Core Entities
* **Customers**: Identified by unique emails and immutable customer numbers.
* **Orders**: Unique transactions linked to a single customer, tracking dates and product quantities.
* **Products**: Items with specific descriptions and pricing.
* **Payments**: Management of various payment methods and gateway tokens.
* **Suppliers**: Entities providing products to the system.

## Design Components

The project consists of two primary architectural artifacts:

1.  **Entity-Relationship (ER) Model**:
    * A high-level conceptual data model using graphical notation.
    * Defines entities, attributes (primary keys, multi-valued, etc.), and relationships (cardinality and participation).

2.  **Integrity Constraints**:
    * Specification of business rules that cannot be captured by the ER diagram alone.
    * Includes domain constraints, key constraints, and referential integrity.
