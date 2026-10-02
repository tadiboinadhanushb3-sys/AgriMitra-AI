# AgriMitra AI

AgriMitra AI is a demo-first smart farming web application that brings sample farm, crop, weather, crop-health, market, planning, assistant, and reporting workflows into one interface. Most values and recommendations are predefined demonstration content; this project is not a production agronomic advisory service.

## Features

- Dashboard with sample farm metrics, alerts, tasks, and trend charts
- Read-only farm profile
- Crop recommendation form with optional soil-report flow (NPK/pH are not required)
- Weather impacts and forecast demonstration
- Crop Doctor image-upload interface (fixed demo diagnosis)
- Market comparison, crop calendar, keyword-based assistant, and knowledge hub
- Printable farm report using the browser print dialog
- Demo login, registration, and onboarding flow

The soil flow accepts PDF/image/TXT/CSV file selections. Current extraction only reads simple TXT/CSV text; PDF/image OCR and report storage are not implemented. Crop and disease results are predefined demo responses. See [DOCUMENTATION.md](DOCUMENTATION.md) for implementation details and limitations.

## Screenshots

Add screenshots of the running application here before publication.

<!-- Example: ![Dashboard](docs/screenshots/dashboard.png) -->

## Tech Stack

- Frontend: React 18, TypeScript, Vite, React Router, Framer Motion, custom CSS
- Backend: Python, FastAPI, Pydantic, Uvicorn
- Database configuration: SQLAlchemy with SQLite default; no application tables or persistence are currently implemented
- Local containers: Docker and Docker Compose

## Installation

Prerequisites: Python 3.12 recommended, Node.js 20 recommended, npm.

### Backend

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
Set-Location backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

In a second terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Frontend: http://localhost:5173  
Backend health: http://localhost:8000/health

The frontend currently calls `http://localhost:8000` directly. `.env.example` is a template, and its values are not all consumed by the application. See the environment-variable notes in [DOCUMENTATION.md](DOCUMENTATION.md).

## Usage

1. Start backend and frontend using the commands above.
2. Open http://localhost:5173 and choose Login.
3. Use the demo credentials prefilled by the login screen: `demo@agrimitra.ai` / `demo123`.
4. Continue through the sample onboarding screen and explore the dashboard/sidebar modules.
5. For local container demonstration, run `docker compose up --build` from the repository root.

Authentication and all major data/AI outputs are demo-only. Do not use the displayed recommendations or scores as verified farm advice.

## Project Structure

```text
.
├── backend/       # FastAPI application and SQLAlchemy setup
├── frontend/      # React pages, layout, styles, and Vite configuration
├── ml/            # Notes for future model integration; no trained model
├── .env.example
├── docker-compose.yml
├── DOCUMENTATION.md
└── README.md
```

## Demo

- Frontend: http://localhost:5173
- Backend health: http://localhost:8000/health
- Demo login shown by the login form: `demo@agrimitra.ai` / `demo123`
- Demo mode uses sample data and does not persist user or farm records.

## Future Enhancements

- Persistent users, farms, crop cycles, tasks, and notifications
- Secure authentication and role-based API authorization
- PDF/image soil-report OCR with validation and value provenance
- Evaluated crop recommendation and disease-detection models
- Live weather/market integrations and measured farm data
- Automated tests and production deployment configuration

## Team / Contributors

Contributor names are not specified in the current repository. Add the project team's names and roles here before submission.
