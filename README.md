# 🚀 Smart Procurement System (SPS) v1.0

An industrial-grade MVP designed to bridge the gap between production engineering and supply chain execution through automated intelligence and BOM-driven workflows.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Executive Overview

The **Smart Procurement System (SPS)** is a professional digital engine tailored for manufacturing environments. It transforms manual, error-prone procurement into a centralized, data-driven process. By integrating **Bill of Materials (BOM)** requirements directly with automated **RFQ dispatching**, SPS ensures that every component needed on the production floor is sourced with 100% traceability, optimized pricing, and minimal operational lag.

---

## 🏗️ Engineering & Strategic Documentation

To provide a 360-degree view of the system's architecture and business value, the project is documented across four strategic pillars:

1. **[Strategic Project Summary](./PROJECT_SUMMARY.md)**: Business case, ROI analysis, and current-state vs. future-state gap analysis.
2. **[Solution Architecture](./Solution_architecture.md)**: Deep dive into the N-Tier architecture, logic handlers, and component interactions.
3. **[Database Design](./Database_design.md)**: ERD schemas and relational integrity constraints using SQLAlchemy ORM.
4. **[Technology Rationale](./Technology_rationale.md)**: Technical justification for the chosen stack (Streamlit, SQLite, SMTP Gateway).

---

## 📁 Project Structure

```text
.
├── database/           # DB connection & Session management (SQLAlchemy)
├── models/             # Data entities (BOM, RFQ, Vendor, User)
├── services/           # Business logic: RFQ Generation & SMTP Mailer
├── utils/              # PDF Generators & Data formatting helpers
├── views/              # Streamlit UI Components & Pages
├── rfq_archive/        # Local storage for generated PDF audit trails
├── .env.example        # Environment configuration template
├── app.py              # Application entry point
└── requirements.txt    # Production dependencies
```

---

## ✨ Key Features

- **BOM-Driven Intelligence:** Automated derivation of procurement needs from complex production Bill of Materials.
- **Automated RFQ Engine:** Dynamic PDF generation and direct dispatch to vendors via secure SMTP protocols.
- **Strategic Awarding Terminal:** Multi-vendor bid comparison matrix for data-backed awarding decisions.
- **Immutable Audit Trail:** Full transparency and GRC compliance for every system action.
- **Vendor Specialization:** Intelligent vendor-to-material mapping to optimize sourcing quality.

---

## 📊 System Flow at a Glance

```mermaid
graph TD
    %% Input Layer
    subgraph Input [Engineering Input]
        BOM[Import BOM Data] --> PR[Generate Purchase Request]
    end

    %% Processing Layer
    subgraph Core [SPS Core Engine]
        RFQ[RFQ Logic Handler] --> PDF[PDF Export Service]
        PDF --> SMTP[SMTP Dispatch Gateway]
    end

    %% Strategic Layer
    subgraph Strategic [Awarding & Analysis]
        Bids[Vendor Bid Collection] --> Matrix[Comparison Matrix]
        Matrix --> Decision[Awarding Decision]
    end

    %% Connections
    PR --> RFQ
    RFQ --> PDF
    PDF --> SMTP
    SMTP --> Bids
    Bids --> Matrix
    Matrix --> Decision
    Decision --> Audit([System Audit Log])

    %% Styling
    style Core fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Strategic fill:#e1f5fe,stroke:#01579b
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites

To ensure a seamless deployment, please verify that your environment meets the following requirements:

- **Python 3.9+**: The recommended stable version for library compatibility.
- **Git**: Required for version control and repository management.

### 2. Environment Setup

1. **Clone the Repository:**

   ```bash
   git clone [https://github.com/your-username/smart-procurement-system.git](https://github.com/your-username/smart-procurement-system.git)
   cd smart-procurement-system
   ```

2. **Initialize Virtual Environment:**
   _It is highly recommended to use a virtual environment to isolate project dependencies._
   ```bash
   python -m venv venv
   # Activation for Windows:
   .\venv\Scripts\activate
   # Activation for Mac/Linux:
   source venv/bin/activate
   ```

### 3. Configuration

1. **Initialize Environment Variables:** Create your local configuration file from the provided template.
   ```bash
   cp .env.example .env
   ```
2. **SMTP Integration:** Open the `.env` file and update your email credentials.
   - **Note:** If using **Gmail**, you must generate and use an **"App Password"** instead of your primary account password to bypass security blocks and ensure successful RFQ dispatch.

### 4. Deployment

```bash
# Upgrade package manager and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Launch the Streamlit User Interface
streamlit run app.py
```

---

## 🔍 Troubleshooting

If you encounter issues during setup or execution, please refer to the following solutions:

- **Dependency Installation Failure:** Ensure your virtual environment (`venv`) is active and that `pip` is updated to the latest version.
- **SMTP/Email Authentication Error:** Verify your `SENDER_EMAIL` and `SENDER_PASSWORD` in the `.env` file. Double-check that "App Passwords" are enabled for your mail provider.
- **Database File Not Found:** The system automatically initializes the `procurement.db` file upon the first successful transaction; ensure the application has write permissions for the project directory.

---

## 🚀 Future Roadmap

- **Phase 2 (Security):** Role-Based Access Control (RBAC) & OAuth2 Integration.
- **Phase 3 (Intelligence):** Predictive Lead-Time Analytics using historical vendor performance.
- **Phase 4 (Integration):** Supplier Self-Service Portal for direct bid entry.

---

## 🤝 Contact & Collaboration

**Digital Consultant:** Mohammed Hlal
**LinkedIn:** [Mohammed Hlal Profile](https://www.linkedin.com/in/mohamed-hlal-288206334/)

_This project is engineered to meet the highest standards of operational excellence and digital scalability in the procurement domain._

```

```
