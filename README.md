# 🌍 Remote Jobs V2

A full-stack remote job board powered by **Angular** and **Flask**, with user authentication, job analytics, email subscriptions, and real-time job data from external APIs like Remotive.

> ✅ Live on [Render](https://remote-jobs-v2.onrender.com) — full SSR support, JWT-based auth, and a dashboard for job insights.

---

## 🔧 Features

### 👤 User Features
- Register / Login with JWT
- Protected Dashboard
- Saved job subscriptions (category, location, keyword)
- Email alerts for matching jobs

### 🗺️ Job Browser
- Browse and filter by location, category, tags, salary, and more
- Keyword + tag search
- Pagination and sorting

### 📊 Dashboard & Analytics
- Salary distribution histogram
- Job posting trends (daily)
- Top companies, categories, sources, and tags
- Monthly/weekly posting activity

---

## ⚙️ Tech Stack

| Layer        | Tech                                               |
|--------------|----------------------------------------------------|
| Frontend     | Angular 16+, Tailwind CSS, Functional Interceptors |
| Backend      | Flask, SQLAlchemy, Flask-JWT-Extended, APScheduler |
| Database     | SQLite (dev), PostgreSQL-ready                     |
| Auth         | JWT, localStorage (SSR-safe)                       |
| Emails       | Gmail SMTP (via environment vars)                  |
| Hosting      | Render.com                                         |

---

## 📦 Project Structure

remote-jobs-v2/
├── frontend/              # Angular app
│   └── src/
│       ├── app/           # Pages, services, routes
│       ├── environments/  # Dev/prod API configs
│       └── interceptors/  # SSR-safe JWT interceptor
├── backend/               # Flask API
│   ├── routes/            # jobs, auth, analytics, dashboard
│   ├── api/jobs/          # Remotive integration
│   ├── models.py
│   └── app.py             # Flask entrypoint


---

## 🚀 Getting Started

### 🔹 Backend (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start the Flask server
python app.py

cd frontend
npm install
npm run dev   # For local dev
npm run build -- --configuration production  # For production

JWT_SECRET_KEY=your-secret
EMAIL_USER=you@gmail.com
EMAIL_PASS=yourpassword
CORS_ORIGIN=https://remote-jobs-v2.onrender.com

