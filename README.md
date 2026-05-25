<p align="center">https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=OverDrive%20API&textBg=false</p>

<h3 align="center">AI-Powered Used Vehicle Valuation System</h3>

<p align="center">
  A robust Flask backend that powers intelligent vehicle valuation using AI image analysis and real Kenyan market data.
</p>

---

## Tech Stack

- **Python 3.10+**
- **Flask** + **Flask-SQLAlchemy** + **Flask-Migrate**
- **PostgreSQL** (Supabase)
- **JWT Authentication**
- **Claude AI Vision**
- **Kenyan Market Pricing Engine**

---

## Project Structure

```bash
over-drive-backend/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── services/        # Business logic (AI + Valuation)
│   ├── ai/              # Claude prompts & services
│   ├── utils/           # Helpers
│   └── __init__.py
├── migrations/
├── main.py
├── start_app.py
├── requirements.txt
└── .env
```

---

## Setup Instructions

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/over-drive-backend.git
cd over-drive-backend

python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables (`.env`)
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:5173,https://yourfrontend.com
CLAUDE_API_KEY=sk-ant-...
```

### 4. Database Migrations
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run Server
```bash
python main.py
# OR
python start_app.py
```

Server runs at: `http://127.0.0.1:5000`

---

## API Documentation

### Authentication
- **JWT Bearer Token**
- Header: `Authorization: Bearer <your-token>`
- Store token in frontend: `localStorage.setItem('overdrive_token', token)`

### Main Endpoints

| Method | Endpoint                                   | Description                        |
|--------|--------------------------------------------|------------------------------------|
| POST   | `/api/auth/register`                       | User registration                  |
| POST   | `/api/auth/login`                          | User login                         |
| GET    | `/api/vehicle/<int:vehicle_id>`            | Get vehicle details                |
| POST   | `/api/vehicle/<int:vehicle_id>/analyze`    | Trigger AI Analysis & Valuation    |
| GET    | `/api/vehicle/<int:vehicle_id>/valuation`  | Get complete valuation report      |
| POST   | `/api/vehicle/<int:vehicle_id>/upload_image` | Upload vehicle image            |
| GET    | `/media/vehicles/<int:vehicle_id>/images`  | Get all images for a vehicle       |
| GET    | `/health`                                  | Health check                       |


---

## AI Vehicle Analysis Flow

1. User uploads vehicle images
2. System sends images to Claude Vision
3. AI returns condition score, issues, positives, and **buyer recommendation**
4. Market valuation is calculated using Kenyan data
5. Full report is saved and returned

---

## Deployment Instructions

### Option 1: Railway / Render (Recommended)

1. Push code to GitHub
2. Connect repository to Railway or Render
3. Add environment variables in dashboard
4. Set start command:
   ```bash
   gunicorn main:app
   ```
5. Add PostgreSQL database (Railway/Supabase)

### Option 2: Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Option 3: Manual VPS
```bash
sudo apt update && sudo apt install nginx supervisor
# Configure gunicorn + nginx
```

---

## Environment Variables Reference

| Variable            | Purpose                            |
|---------------------|------------------------------------|
| `DATABASE_URL`      | PostgreSQL connection              |
| `SECRET_KEY`        | Flask session security             |
| `JWT_SECRET_KEY`    | JWT token signing                  |
| `CORS_ORIGINS`      | Allowed frontend domains           |
| `CLAUDE_API_KEY`    | Anthropic API key                  |

---

## Contributing

1. Fork the repo
2. Create feature branch
3. Make changes + tests
4. Submit Pull Request

---

**Built for the Kenyan used car market with Determination**

---
