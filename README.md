---

# 📌 Client Query Management System

## 🚀 About the Project

The **Client Query Management System** is a **Streamlit web application** that enables organizations to **collect, track, and resolve client queries** efficiently.

It features:

* A **Client Interface** → for submitting and tracking queries.
* A **Support Dashboard** → for managing and resolving queries.

The system is powered by:

* **PostgreSQL** (database)
* **Streamlit** (frontend UI)
* **Pandas** (data manipulation)
* **Plotly** (visualizations)
* **SQLAlchemy & psycopg2** (database connection)

---

## 🛠️ Features

### 👨‍💻 Client Side

* Register/Login securely (SHA-256 hashed passwords).
* Submit new queries with **email, phone, heading, description, and priority**.
* Track all submitted queries with **status updates** (Open, In Progress, Resolved).
* View query distribution with **interactive charts**.

### 🎧 Support Team Side

* Role-based dashboard with metrics:

  * 📌 Total Queries
  * 🟠 In Progress
  * ✅ Resolved
* Filter and manage queries by status.
* Assign queries to support agents.
* Update query progress and resolution.
* Visualize query trends over time.

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/client-query-management.git
cd client-query-management
```

### 2️⃣ Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
# Activate virtual environment
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install requirements
pip install -r requirements.txt
```

**requirements.txt**

```
streamlit
pandas
sqlalchemy
psycopg2
plotly
```

### 3️⃣ Setup PostgreSQL Database

* Create a new database:

```sql
CREATE DATABASE Client_query;
```

* Update credentials in `app.py`:

```python
DB_URL = "postgresql+psycopg2://<username>:<password>@localhost:5432/Client_query"
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🔑 Default Users

The system initializes with two default accounts:

| Username        | Password     | Role    |
| --------------- | ------------ | ------- |
| `support_admin` | `support123` | Support |
| `client_user`   | `client123`  | Client  |

---

## 📊 Dataset

* Sample queries are loaded from a **CSV file** (Google Drive link inside code).
* Columns include:

  * `client_name`, `email_id`, `mobile_number`
  * `query_heading`, `query_text`
  * `status`, `priority`
  * `submitted_on`, `resolved_on`, `assigned_to`

---

## 📈 How It Works

1. **Clients** log in, submit queries, and track them.
2. **Support Team** logs in, views all queries, and updates progress.
3. **Visualizations** show query status breakdown and trends.
4. Data is stored in **PostgreSQL** and updated in real-time.

---

## 📌 Example Use Cases

* 🏢 Companies → Handle customer support tickets.
* 🎓 Universities → Manage student issues and feedback.
* 🛠️ Service Providers → Track client requests.
* 👨‍💻 Teams → Organize and assign project queries.

---

## 📌 Future Enhancements

* 🔐 JWT / OAuth authentication.
* 📷 File/Image upload support.
* 📧 Email alerts on query updates.
* 📊 SLA (Service Level Agreement) monitoring.
* 🌐 Cloud deployment (Heroku, AWS, Streamlit Cloud).

---

## 👨‍🏫 Author

Developed as part of a **Data Engineering / Python capstone project**.
📧 For queries: *(mailto:rajfreelancer1993@gmail.com)*

---
