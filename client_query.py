import streamlit as st
import pandas as pd
import hashlib
from sqlalchemy import create_engine, text
from datetime import datetime
import plotly.express as px

# Database Configuration
# -------------------------
DB_URL = "postgresql+psycopg2://postgres:8098086631@localhost:5432/client_support_query"
engine = create_engine(DB_URL)

# Password Hashing
# -------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Database Setup
# -------------------------
def setup_database():
# tables and default users
    with engine.begin() as conn:
    # queries table
        conn.execute(text("""CREATE TABLE IF NOT EXISTS queries (
                query_id SERIAL PRIMARY KEY,
                client_name TEXT NOT NULL,
                email_id VARCHAR(255),
                mobile_number VARCHAR(20),
                query_heading TEXT,
                query_text TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                submitted_on DATE NOT NULL,
                submitted_time TIME NOT NULL,
                resolved_on DATE,
                resolved_time TIME,
                assigned_to TEXT);"""))
    # users table
        conn.execute(text("""CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'client');"""))
    # Inserted default users
        default_users = {"support_admin": ("support123", "support"),"client_user": ("client123", "client")}
        for username, (password, role) in default_users.items():
            hashed_pw = hash_password(password)
            conn.execute(text("""
                INSERT INTO users (username, password, role)
                VALUES (:username, :password, :role)
                ON CONFLICT (username) DO NOTHING;
            """), {
                "username": username,
                "password": hash_password(password),
                "role": role,})

    # Loaded queries from CSV
    try:
        import numpy as np
        csv_url = "https://drive.google.com/uc?id=1x6IiZYzi25-57a_pqG-ngQZWryuocqKT&export=download"
        df_csv = pd.read_csv(csv_url)

        # Replace NaN with None
        df_csv = df_csv.replace({np.nan: None})

        # Insert rows into queries
        with engine.begin() as conn:
            for _, row in df_csv.iterrows():
                conn.execute(text('''
                    INSERT INTO queries (
                        client_name, email_id, mobile_number, query_heading, query_text, status, priority, submitted_on, submitted_time, resolved_on, resolved_time, assigned_to)
                    VALUES (:client_name, :email_id, :mobile_number, :query_heading, :query_text,:status, :priority, :submitted_on, :submitted_time, :resolved_on, :resolved_time, :assigned_to)
                    ON CONFLICT (query_id) DO NOTHING;'''), {
                    "client_name": row['client_name'], "email_id": row['email_id'], "mobile_number": row['mobile_number'],
                    "query_heading": row['query_heading'], "query_text": row['query_text'], "status": row['status'], "priority": row['priority'],
                    "submitted_on": row['submitted_on'], "submitted_time": row['submitted_time'],
                    "resolved_on": row['resolved_on'], "resolved_time": row['resolved_time'], "assigned_to": row['assigned_to']})
    except Exception as e:
        st.warning(f"⚠️ Could not load CSV: {e}")
    conn.commit()

# Query Functions
# -------------------------
def get_queries_from_db():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM queries", conn, parse_dates=['submitted_on', 'resolved_on'])
        df['submitted_on'] = pd.to_datetime(df['submitted_on']).dt.date
        df['resolved_on'] = pd.to_datetime(df['resolved_on']).dt.date
        return df

def add_new_query(client_name, email_id, mobile_number, query_heading, query_text, priority):
    with engine.connect() as conn:
        now = datetime.now()
        submitted_on = now.date()   # date
        submitted_time = now.time() # time
        status = "Open"
        conn.execute(text('''
            INSERT INTO queries (client_name, email_id, mobile_number, query_heading, query_text, status, priority, submitted_on, submitted_time)
            VALUES (:client_name, :email_id, :mobile_number, :query_heading, :query_text,:status, :priority, :submitted_on, :submitted_time);'''), {
            "client_name": client_name, "email_id": email_id, "mobile_number": mobile_number, "query_heading": query_heading, "query_text": query_text,
            "status": status, "priority": priority, "submitted_on": submitted_on, "submitted_time": submitted_time})
        conn.commit()

def update_query_status(query_id, new_status, assigned_to):
    with engine.connect() as conn:
        now = datetime.now()
        resolved_on = now.date() if new_status == "Resolved" else None
        resolved_time = now.time() if new_status == "Resolved" else None
        conn.execute(text('''UPDATE queries 
            SET status = :status, resolved_on = :resolved_on, resolved_time = :resolved_time, assigned_to = :assigned_to 
            WHERE query_id = :query_id;'''), {"status": new_status, "resolved_on": resolved_on, "resolved_time": resolved_time, "assigned_to": assigned_to, "query_id": query_id})
        conn.commit()

# User Authentication
# -------------------------
def register_user(username, password, role="client"):
    with engine.connect() as conn:
        check_user = conn.execute(text("SELECT 1 FROM users WHERE username = :username;"), {"username": username}).scalar()     # Check if user already exists
        if check_user:
            return False, "⚠️ Username already exists!"
        hashed_pw = hash_password(password)
        conn.execute(text('''INSERT INTO users (username, password, role) VALUES (:username, :password, :role);'''), {"username": username, "password": hashed_pw, "role": role})   # Insert new user
        conn.commit()
        return True, "✅ Registration successful! Please log in."
    
def authenticate_user(username, password, role):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT password FROM users WHERE username = :username AND role = :role;"), {"username": username, "role": role}).scalar()
        if result and result == hash_password(password):
            return True, role
    return False, None

# Streamlit Config
# -------------------------
st.set_page_config(page_title="Client Query Management", layout="wide")
if "logged_in" not in st.session_state:   # ------------------------------> Initialize session state for login tracking
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# Login & Register UI
# -------------------------
def login_and_register_ui():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 Login or Register")
        st.markdown("""<style>div.stForm{background-color:#F9FAFB;padding:40px;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,0.05);} .stTextInput>div>div>input,.stSelectbox>div>div>div{border:1px solid #E0E3E8;border-radius:8px;padding:10px;background-color:#FFFFFF;box-shadow:inset 0 1px 2px rgba(0,0,0,0.03);} .stTextInput>div>div>input:focus,.stSelectbox>div>div>div:focus{border-color:#008080;box-shadow:0 0 0 3px rgba(0,128,128,0.2);outline:none;} .stTextInput>div>label,.stSelectbox>label{color:#555555;font-weight:500;}</style>""", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            choice = st.radio("Choose an option:", ["Login", "Register"])
# ---Login---           
            if choice == "Login":    
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    role = st.selectbox("Role", ["client", "support"])
                    submitted = st.form_submit_button("Log In")
                    if submitted:
                        success, user_role = authenticate_user(username, password, role)
                        if success:
                            st.session_state.logged_in = True          # Store session data on success
                            st.session_state.user_role = user_role
                            st.session_state.username = username
                            st.success(f"✅ Welcome {username}! Role: {user_role}")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username, password, or role.")
# ---REGISTER---            
            else:
                with st.form("register_form"):
                    new_username = st.text_input("New Username", key="reg_user")
                    new_password = st.text_input("New Password", type="password", key="reg_pass")
                    confirm_pw = st.text_input("Confirm Password", type="password", key="reg_conf")
                    submitted = st.form_submit_button("Register")
                    if submitted:
                        if new_password != confirm_pw:
                            st.error("⚠️ Passwords do not match!")
                        else:
                            success, msg = register_user(new_username, new_password)
                        if success:
                            st.success(msg)                        
def logout_button():
    if st.sidebar.button("Log Out"):
        st.session_state.update({"logged_in": False, "user_role": None, "username": None})
        st.rerun()

# Client View
# -------------------------
def client_view():
    st.title("🙋 Client Query Submission")
    st.subheader(f"Welcome, {st.session_state.username}!")
    st.markdown("""<style>div.stForm{background-color:#F9FAFB;padding:40px;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,0.05);} .stTextInput>div>div>input,.stSelectbox>div>div>div{border:1px solid #E0E3E8;border-radius:8px;padding:10px;background-color:#FFFFFF;box-shadow:inset 0 1px 2px rgba(0,0,0,0.03);} .stTextInput>div>div>input:focus,.stSelectbox>div>div>div:focus{border-color:#008080;box-shadow:0 0 0 3px rgba(0,128,128,0.2);outline:none;} .stTextInput>div>label,.stSelectbox>label{color:#555555;font-weight:500;}</style>""", unsafe_allow_html=True)
 # New query form ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
    with st.form("new_query_form"):
        email_id = st.text_input("Your Email ID")
        mobile_number = st.text_input("Your Mobile Number")
        query_heading = st.text_input("Query Heading")
        query_text = st.text_area("Query Description", placeholder="Describe your issue in detail...", height=150)
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        submitted = st.form_submit_button("Submit Query")
        if submitted:
            if email_id and query_heading and query_text:
                add_new_query(st.session_state.username, email_id, mobile_number, query_heading, query_text, priority)
                st.success("✅ Your query has been submitted successfully!")
                st.balloons()
            else:
                st.error("⚠️ Please fill out all required fields.")
    st.markdown("---")
    st.subheader("📂 Your Submitted Queries")

# Fetch and display client-specific queries --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
    all_queries = get_queries_from_db()
    client_queries = all_queries[all_queries['client_name'] == st.session_state.username]
    if not client_queries.empty:
    # Status distribution pie chart
        st.plotly_chart(px.pie(client_queries['status'].value_counts().reset_index().set_axis(['Status','Count'], axis=1), values='Count', names='Status', title="📌 Your Queries by Status", color='Status', color_discrete_map={"Open":"red","In Progress":"orange","Resolved":"green"}).update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True)
    # Styled DataFrame of queries
        st.dataframe(client_queries.style.applymap(lambda v: f"background-color: { {'Open':'lightcoral','In Progress':'khaki','Resolved':'lightgreen'}.get(v,'white')}; font-weight:bold;", subset=["status"]).applymap(lambda v: f"background-color: { {'Low':'lightgreen','Medium':'orange','High':'tomato'}.get(v,'white')}; font-weight:bold;", subset=["priority"]), use_container_width=True, height=400)
    else:
        st.info("📭 You have not submitted any queries yet.")

# Support Dashboard
# -------------------------
def support_dashboard():
    st.title("🎧 Support Team Dashboard")
    queries_df = get_queries_from_db()
    if queries_df.empty: return st.info("📭 No queries found in the system.")
# Metrics summary --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    st.subheader("📊 System Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("🧾 Total Queries", len(queries_df)); c2.metric("⏳ In Progress", len(queries_df[queries_df['status']=="In Progress"])); c3.metric("✅ Resolved", len(queries_df[queries_df['status']=="Resolved"]))
    st.markdown("---")
# Data Visualizations --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    st.subheader("📈 Query Trends & Breakdown")
    colA, colB = st.columns(2)
# Pie chart by status ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    with colA:
        st.plotly_chart(px.pie(queries_df['status'].value_counts().reset_index().set_axis(['Status','Count'], axis=1), values='Count', names='Status', title="📌 Queries by Status", color='Status', color_discrete_map={"Open":"red","In Progress":"orange","Resolved":"green"}).update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True)
    # Line chart of queries over time ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
        with colB:
            st.plotly_chart(px.line(queries_df.assign(submitted_on=pd.to_datetime(queries_df["submitted_on"],errors="coerce").dt.date,resolved_on=pd.to_datetime(queries_df["resolved_on"],errors="coerce").dt.date).groupby("submitted_on").size().reset_index(name="Count").rename(columns={"submitted_on":"Date"}), x="Date", y="Count", title="🗓 Queries Submitted Over Time", markers=True).update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"), use_container_width=True)

    st.markdown("---")
# Query management table
    st.subheader("📂 Manage Queries")
    status_filter = st.radio("🔍 Filter by Status", ["All", "Open", "In Progress", "Resolved"], horizontal=True)
    if status_filter == "All":
        filtered_df = queries_df
    else:
        filtered_df = queries_df[queries_df['status'] == status_filter]
# Display filtered queries with emojis for status/priority ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    st.dataframe(filtered_df.copy().assign(status=lambda x: x["status"].map({"Open": "📌 Open","In Progress": "⏳ In Progress","Resolved": "✅ Resolved"}), priority=lambda x: x["priority"].map({"Low": "🔻 Low","Medium": "💡 Medium","High": "🚀 High"})), use_container_width=True, height=400)
    
# Query update form
    if not filtered_df.empty:
        st.markdown("### 🛠 Update Query")
    query_id_to_update_str = st.text_input("Enter Query ID to Update", value="")
    try:
        query_id_to_update = int(query_id_to_update_str)
        if query_id_to_update in filtered_df['query_id'].values:
            current_query = queries_df[queries_df['query_id'] == query_id_to_update].iloc[0]
            
            st.markdown(f"**Current Status:** <span style='color:blue'>{current_query['status']}</span> "f"| **Priority:** <span style='color:darkred'>{current_query['priority']}</span>", unsafe_allow_html=True)
            st.markdown("""<style>div.stForm{background-color:#F9FAFB;padding:40px;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,0.05);} .stTextInput>div>div>input,.stSelectbox>div>div>div{border:1px solid #E0E3E8;border-radius:8px;padding:10px;background-color:#FFFFFF;box-shadow:inset 0 1px 2px rgba(0,0,0,0.03);} .stTextInput>div>div>input:focus,.stSelectbox>div>div>div:focus{border-color:#008080;box-shadow:0 0 0 3px rgba(0,128,128,0.2);outline:none;} .stTextInput>div>label,.stSelectbox>label{color:#555555;font-weight:500;}</style>""", unsafe_allow_html=True)
            
            with st.form("update_query_form"):
                new_status = st.selectbox("Change Status", ["Open", "In Progress", "Resolved"], index=["Open", "In Progress", "Resolved"].index(current_query['status']))
                assigned_to = st.text_input("Assign to Agent", value=current_query['assigned_to'] if pd.notna(current_query['assigned_to']) else "Default Agent")
                resolved_on_input = st.date_input("Resolved On (optional)", value=current_query['resolved_on'] if pd.notna(current_query['resolved_on']) else datetime.now().date())
                update_button = st.form_submit_button("🚀 Update Query") 
                if update_button:
                    update_query_status(query_id_to_update, new_status, assigned_to)
                    st.success(f"✅ Query ID {query_id_to_update} updated successfully!")
                    st.balloons()
                    st.rerun()
        else:
            if query_id_to_update_str:
                st.warning("⚠️ Query ID not found.")
    except ValueError:
        if query_id_to_update_str:
            st.warning("⚠️ Please enter a valid number for the Query ID.")

# Main App
# -------------------------
def main():
    st.title("📌 Client Query Management System")
    st.markdown("""<style>.stApp {background: linear-gradient(to bottom, #EAECEE, #FFFFFF);}</style>""", unsafe_allow_html=True)
# Setup database on app start    
    setup_database()
# Role-based routing    
    if st.session_state.logged_in:
        st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
        logout_button()
        if st.session_state.user_role == "client":client_view()
        elif st.session_state.user_role == "support":support_dashboard()
    else:
        login_and_register_ui()

if __name__ == "__main__":
    main()