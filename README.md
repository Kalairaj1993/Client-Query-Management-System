---

# 📌 Client Query Management System

## 🚀 About the Project

The **Client Query Management System** is a **Streamlit web application** that enables organizations to **collect, track, and resolve client queries** efficiently.

* Used **PostgreSQL** to create the database.
* Connected via **VS Code** using `DB_URL` with PostgreSQL credentials.
* First tested the connection in a **Jupyter Notebook (`.ipynb`)**.
* Then converted it into a **Python script (`.py`)**.
* Finally built the **Streamlit dashboard**.

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

## 🛠️ Development Workflow

1. **Database Setup (PostgreSQL)**

   * Created a PostgreSQL database named `Client_query`.
   * Connected using **VS Code** with a `DB_URL` string:

     ```python
     DB_URL = "postgresql+psycopg2://<username>:<password>@localhost:5432/Client_query"
     ```
   * Replaced `<username>` and `<password>` with PostgreSQL credentials.

2. **Initial Testing**

   * Used a **Jupyter Notebook (`.ipynb`)** to test PostgreSQL connection.
   * Verified query execution and database CRUD operations.

3. **Python Script (`.py`)**

   * Migrated connection code into a Python script.
   * Created **tables** (`users`, `queries`) directly in the database.
   * Added helper functions for insert, update, and fetch operations.

4. **Streamlit Dashboard**

   * Built a **UI for Clients** to submit and track queries.
   * Built a **Support Dashboard** to manage queries, visualize metrics, and update statuses.

---

## 🛠️ Features

### 👨‍💻 Client Side

* Secure **Login & Registration**.
* Submit queries with **email, phone, heading, description, and priority**.
* Track submitted queries with **status updates**.
* Query distribution displayed via **charts and styled tables**.

### 🎧 Support Team Side

* Dashboard with metrics:

  * 📌 Total Queries
  * 🟠 In Progress
  * ✅ Resolved
* Filter queries by status.
* Assign queries to support agents.
* Update query status and resolution date.
* Query insights with pie and line charts.

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/client-query-management.git
cd client-query-management
```

### 2️⃣ Create Virtual Environment & Install Dependencies

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

### 3️⃣ Setup PostgreSQL

* Create a database:

```sql
CREATE DATABASE Client_query;
```

* Update DB credentials in `app.py`:

```python
DB_URL = "postgresql+psycopg2://<username>:<password>@localhost:5432/Client_query"
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🔑 Default Users

| Username        | Password     | Role    |
| --------------- | ------------ | ------- |
| `support_admin` | `support123` | Support |
| `client_user`   | `client123`  | Client  |

---

## 📊 Dataset

* Loads sample queries from a CSV (Google Drive link inside code).
* Includes columns:

  * `client_name`, `email_id`, `mobile_number`,
  * `query_heading`, `query_text`, `status`, `priority`,
  * `submitted_on`, `resolved_on`, `assigned_to`.

---

## 📈 How It Works

1. **Clients** log in, submit queries, and track progress.
2. **Support team** views all queries and updates status.
3. **Charts** show workload distribution and trends.
4. **PostgreSQL** stores and updates data in real-time.

---

## 📌 Use Cases

* 🏢 Companies → Handle customer support tickets.
* 🎓 Universities → Manage student requests.
* 🛠️ Service Providers → Track client complaints.
* 👨‍💻 Teams → Organize project-related queries.

---

## 📌 Future Enhancements

* JWT / OAuth-based authentication.
* File/image upload with BLOB storage.
* Email notifications for query updates.
* SLA tracking and overdue alerts.
* Cloud deployment (Heroku, AWS, Streamlit Cloud).

---

## 👨‍🏫 Author

Developed as part of a **Data Engineering / Python capstone project**.
📧 For queries: *(mailto:rajfreelancer1993@gmail.com)*

---
