# 🎬 Film Data Quality & Cleansing Pipeline

This project is a complete **data validation and cleansing pipeline** built with Python and Pandas. It connects to a **PostgreSQL** database, extracts multiple related tables, validates the schema and data quality against a defined requirements schema, cleans the data, and finally writes a refined dataset back to the database.

---

## 🧩 Project Overview

This pipeline covers:

- Extracting raw data from PostgreSQL and external sources (CSV, JSON)
- Validating:
  - Table existence
  - Data shape
  - Column presence
  - Data types
  - Missing values
  - Duplicates
- Data cleansing:
  - Resolving column mismatches
  - Fixing data type mismatches
  - Removing missing or duplicate values
- Building a clean, enriched film dataset
- Loading the final dataset back to PostgreSQL

---

## 📦 Architecture

![ETL Architecture](https://cdn.discordapp.com/attachments/1400160453740462170/1400163705852788868/Dataset_1.jpg?ex=688ba391&is=688a5211&hm=69cac23d596a72e46112bd5468671e2a4fb19dc4b54ac62777dbda855d734a17&)