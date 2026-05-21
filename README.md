<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=Over-Drive%20&descAlign=53&descAlignY=53&animation=fadeIn&fontSize=30&textBg=false"/>
</p>

AI Vehicle Valuation API built with Flask.

This backend powers the Over-Drive platform, handling authentication, vehicle uploads, and AI-based vehicle image analysis.

---

##  Tech Stack

- Python 3
- Flask
- Flask SQLAlchemy
- Flask Migrate
- PostgreSQL (Supabase / hosted DB)
- JWT Authentication
- Flask-CORS
- AI Vision Service (Claude / external AI model)

---

##  Project Structure
over-drive-backend/
│
├── app/
│ ├── models/
│ ├── routes/
│ ├── services/
│ ├── utils/
│ └── __init__.py
│
├── migrations/
├── main.py
├── requirements.txt
└── .env


---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/over-drive-backend.git
cd over-drive-backend

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pipenv install
pipenv shell
```
### Create .env file

DATABASE_URL=your_postgres_connection_string
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
CORS_ORIGINS=http://localhost:5173

### Run database migrations
flask db init
flask db migrate -m "init"
flask db upgrade head

### Start Server
cd start_app.py
flask run

### Server runs at
http://127.0.0.1:5000

### Authentication
JWT authentication is used.

### Header format
Authorization: Bearer <token>

### Frontend token storage
localStorage key: overdrive_token

### AI Vehicle Analysis Flow
1.User uploads vehicle images
2.Backend validates request
3.Images sent to AI service
4.AI returns:
----Condition score
----Detected issues
----Summary report
5.API returns structured JSON response

### API Endpoints
AUTH
```bash
POST /api/auth/register
POST /apia/auth/login
```
VEHICLES
Get Vehicle Details
```bash
GET /api/vehicle/<vehicle_id>
```

Analyze Vehicle(AI)
```bash
POST /api/vehicle/<vehicle_id>/analyze
```

Get Vehicle Valuation
```bash
GET /api/vehicle/vehicle<vehicle_id>/valuation
```

IMAGES
Upload Vehicle Image
```bash
POST /api/vehicle/<vehicle_id>/upload_image
```

Get Vehicle Images
```bash
GET /media/vehicles/<vehicle_id>/images
```

Serve Uploaded Vehicle File
```bash
GET /api/vehicle/uploads/<filename>
```

Delete Image
```bash
DELETE /media/images/<image_id>
```

GENERAL MEDIA ACCESS
Serve File
```bash
GET /uploads/<filename>
```

Upload Vehicle Image
```bash
POST /media/vehicles/<vehicle_id>/upload
```

System Routes
Root
```bash
GET /
```

Health Check
```bash
GET /health
```



