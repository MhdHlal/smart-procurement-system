````markdown
# 🚀 Smart Procurement System (SPS)

**Bridging Production Engineering and Supply Chain Execution with Digital Intelligence.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Executive Overview

The **Smart Procurement System (SPS)** is a professional-grade MVP designed to transform fragmented, manual procurement workflows into a centralized digital engine. By integrating **Bill of Materials (BOM)** logic with automated **RFQ dispatching**, SPS eliminates operational silos, minimizes human error, and ensures 100% data integrity from the factory floor to the awarding terminal.

---

## 🏗️ Engineering & Strategic Documentation

To provide a comprehensive understanding of the system, the project is documented across four strategic pillars:

1.  **[Strategic Project Summary](./PROJECT_SUMMARY.md):** The business case, current challenges, and the future state of the procurement process.
2.  **[Solution Architecture](./Solution_architecture.md):** A deep dive into the N-Tier architecture, including component interactions and logic flow.
3.  **[Database Design](./Database_design.md):** Detailed ERD and entity relationships based on the SQLAlchemy implementation.
4.  **[Technology Rationale](./Technology_rationale.md):** The "Why" behind our choice of tools (Python, Streamlit, SQLAlchemy, etc.).

---

## ✨ Key Features

- **BOM-Driven Procurement:** Automatically calculate material requirements based on production planning.
- **Automated RFQ Dispatch:** Generate professional PDF RFQs and dispatch them to vendors via SMTP in one click.
- **Awarding Terminal:** Side-by-side bid comparison matrix for data-driven decision making.
- **Immutable Audit Trail:** Every action (Create, Send, Award) is logged for full transparency and GRC compliance.
- **Vendor Management:** Targeted vendor selection based on material specialty.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/smart-procurement-system.git](https://github.com/your-username/smart-procurement-system.git)
cd smart-procurement-system
```
````

### 2. Environment Configuration

SPS uses a decoupled configuration model for security and flexibility.

1. Copy the template: `cp .env.example .env`
2. Update the `.env` file with your SMTP credentials and database path.

### 3. Install Dependencies

```bash
pip install -r requirements.json
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## 📊 System Flow at a Glance

```mermaid
graph LR
    A[BOM Requirements] --> B[Purchase Request]
    B --> C[Automated RFQ]
    C --> D[Vendor Bidding]
    D --> E[Comparison Matrix]
    E --> F[Awarding Decision]
    F --> G[Audit Log]
```

---

## 🚀 Future Roadmap

- **Phase 2:** Secure User Authentication (RBAC).
- **Phase 3:** AI-Driven Price Trend Analytics.
- **Phase 4:** Supplier Self-Service Portal.

---

## 🤝 Contact & Collaboration

**Digital Consultant:** Mohammed Hlal
**LinkedIn:** https://www.linkedin.com/in/mohamed-hlal-288206334/

_Designed and engineered with a focus on operational excellence and digital scalability._

```

```
