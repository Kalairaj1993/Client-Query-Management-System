---

# 📌 Client Query Management System

## 🚀 About the Project

The **Client Query Management System** is a **Streamlit web application** that enables organizations to **collect, track, and resolve client queries** efficiently.

**Development Process:**

* Used **PostgreSQL** to create the database.
* Connected via **VS Code** using `DB_URL` with PostgreSQL credentials.
* First tested the connection in a **Jupyter Notebook (`.ipynb`)**.
* Then converted it into a **Python script (`.py`)**.
* Finally built the **Streamlit dashboard**.

**Key Features:**

* A **Client Interface** → for submitting and tracking queries.
* A **Support Dashboard** → for managing and resolving queries.

**Tech Stack:**

* **PostgreSQL** (database)
* **Streamlit** (frontend UI)
* **Pandas** (data manipulation)
* **Plotly** (visualizations)
* **SQLAlchemy & psycopg2** (database connection)

---

## 🛠️ Features

### 👨‍💻 Client Side

* Secure login & registration.
* Submit queries with **email, phone, heading, description, and priority**.
* Track all submitted queries with status updates (Open, In Progress, Resolved).
* Visualize query distribution with charts.

### 🎧 Support Team Side

* Dashboard with metrics:

  * 📌 Total Queries
  * 🟠 In Progress
  * ✅ Resolved
* Filter queries by status.
* Assign queries to support agents.
* Update query status & resolution date.
* Insights via pie chart & line chart.

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
# Activate environment
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install packages
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

* Create database:

```sql
CREATE DATABASE Client_query;
```

* Update DB credentials in `app.py`:

```python
DB_URL = "postgresql+psycopg2://<username>:<password>@localhost:5432/Client_query"
```

### 4️⃣ Run the Application

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

* Loads sample queries from a **CSV file** (Google Drive link inside the code).
* Columns include:

  * `client_name`, `email_id`, `mobile_number`
  * `query_heading`, `query_text`
  * `status`, `priority`
  * `submitted_on`, `resolved_on`, `assigned_to`

---

## 📈 How It Works

1. **Clients** → log in, submit queries, track status.
2. **Support Team** → views all queries, updates progress.
3. **Charts** → show workload distribution & query trends.
4. **PostgreSQL** → ensures real-time updates.

---

## 📌 Use Cases

* 🏢 Companies → Customer support ticketing system.
* 🎓 Universities → Manage student requests.
* 🛠️ Service Providers → Track customer complaints.
* 👨‍💻 Teams → Organize project-related queries.

---

## 📌 Future Enhancements

* 🔐 JWT / OAuth authentication.
* 📷 File/image uploads with BLOB storage.
* 📧 Email notifications.
* 📊 SLA tracking.
* 🌐 Cloud deployment (Heroku, AWS, Streamlit Cloud).

---

## 👨‍🏫 Author

Developed as part of a **Data Science / Python capstone project**.
📧 For queries: *(mailto:rajfreelancer1993@gmail.com)*

---
