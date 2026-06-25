# Overloaded

## The purpose of this project is to allow users to log workouts consistently and quickly without disrupting the workout itself

## https://overloaded-two.vercel.app/

## Screenshots

![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

## Tech stack

- **Backend:** Flask, SQLAlchemy, Flask-Migrate, JWT auth (Flask-JWT-Extended)
- **Frontend:** React, TypeScript, Vite, Bootstrap
- **Database:** PostgreSQL
- **Deployment:** Render (backend + database), Vercel (frontend)

## Features

- User registration and login with hashed passwords and JWT-based auth
- Log a full workout — multiple exercises, each with sets/reps/weight/RPE — in
  a single action
- Workout history with per-exercise detail
- Dashboard with quick stats (total workouts, exercises logged, last workout)

## Installation

Steps to install

## Local setup

You'll need Python, Node.js, and a running PostgreSQL instance.

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with:

```
DATABASE_URL=postgresql://user:password@localhost:5432/your_db
JWT_SECRET_KEY=your_secret_key
```

Then run the migrations, seed the standard exercises, and start the server:

```bash
flask db upgrade
python seed.py
flask run
```

### Frontend

```bash
cd frontend/react-app
npm install
```

Create a `.env` file in `frontend/react-app/` with:

```
VITE_API_URL=http://localhost:5000
```

Then start the dev server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.
