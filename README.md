🌐 Remote Job Notifier
A full-stack web application for discovering, filtering, and analyzing remote job listings — with user subscriptions, salary insights, and API-driven job ingestion.

🔧 Tech Stack
Frontend: Angular · TailwindCSS · Chart.js
Backend: Flask · PostgreSQL · JWT Authentication
APIs: Adzuna · USAJobs

🚀 Features
Search & Filter Jobs: Easily browse remote jobs using keyword, category, and location filters.

Analytics Dashboard: Visualize top job categories, locations, and salary coverage with interactive charts.

User Authentication: Secure sign-up, login, and session handling with JWT-based auth.

Email Alerts: Subscribe to job alerts and receive email updates when new matches are posted.

Data Normalization: Unified job format from multiple APIs for consistent display and analysis.

Modern UI: Responsive design built with TailwindCSS and Angular components.

📊 Screenshot Preview
TBD

⚙️ How It Works
Job Fetching
Python scripts connect to Adzuna and USAJobs APIs to fetch remote jobs, normalize the data, and store them in PostgreSQL.

Backend API (Flask)

Handles user registration/login (JWT-based)

Exposes endpoints for jobs, categories, subscriptions, and dashboard analytics

Protects routes with authentication

Frontend (Angular)

Displays job listings and analytics

Manages user sessions and subscriptions

Uses Angular route guards and form validation

🛠️ Installation
Backend (Flask API)
bash
Copy
Edit
cd backend
pip install -r requirements.txt
flask run
Frontend (Angular)
bash
Copy
Edit
cd frontend
npm install
ng serve
📬 Deployment
Deployed with Render (Flask) and Vercel/Netlify (Angular)

Environment variables for API keys and database connections

📈 Future Improvements
Resume upload + matching jobs

Pagination and advanced search

User profile management

OAuth login (Google/GitHub)

📚 Learnings
This project was built to:

Practice full-stack development from scratch

Integrate multiple job APIs with different schemas

Build meaningful dashboards from real-world data

Deploy production-ready apps with auth and subscriptions

🧑‍💻 Author
Aaron Casas
GitHub: @sasac27
