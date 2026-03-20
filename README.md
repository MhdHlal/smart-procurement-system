🚀 Smart Procurement System (SPS)

Bridging Production Engineering and Supply Chain Execution with Digital Intelligence.

📌 Executive Overview

The Smart Procurement System (SPS) is a professional-grade MVP designed to transform fragmented, manual procurement workflows into a centralized digital engine. By integrating Bill of Materials (BOM) logic with automated RFQ dispatching, SPS eliminates operational silos, minimizes human error, and ensures 100% data integrity from the factory floor to the awarding terminal.

🏗️ Engineering & Strategic Documentation

To provide a comprehensive understanding of the system, the project is documented across four strategic pillars:

Strategic Project Summary

Solution Architecture

Database Design

Technology Rationale

✨ Key Features

BOM-Driven Procurement: Automatically calculate material requirements based on production planning.

Automated RFQ Dispatch: Generate professional PDF RFQs and dispatch them via SMTP.

Awarding Terminal: Side-by-side bid comparison matrix for data-driven decisions.

Immutable Audit Trail: Full transparency and GRC compliance for every system action.

Vendor Management: Targeted vendor selection based on material specialty.

🛠️ Installation & Setup

1. Clone the Repository

git clone [https://github.com/your-username/smart-procurement-system.git](https://github.com/your-username/smart-procurement-system.git)
cd smart-procurement-system

2. Environment Configuration

SPS uses a decoupled configuration model for security and flexibility.

Copy the template: cp .env.example .env

Update the .env file with your SMTP credentials and database path.

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

streamlit run app.py

📊 System Flow at a Glance

graph LR
A[BOM Requirements] --> B[Purchase Request]
B --> C[Automated RFQ]
C --> D[Vendor Bidding]
D --> E[Comparison Matrix]
E --> F[Awarding Decision]
F --> G[Audit Log]

🚀 Future Roadmap

Phase 2: Secure User Authentication (RBAC).

Phase 3: AI-Driven Price Trend Analytics.

Phase 4: Supplier Self-Service Portal.

🤝 Contact & Collaboration

Digital Consultant: Mohammed Hlal

LinkedIn: https://www.linkedin.com/in/mohamed-hlal-288206334/

Designed and engineered with a focus on operational excellence and digital scalability.
