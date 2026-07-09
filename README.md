# Visit Counter Web System

A four-service web system built with Docker and Docker Compose for tracking website visits.

## System Architecture

This system consists of 4 separate containers running in a shared network:
```
User Browser
     ↓
[Frontend - Nginx] (Port 80)
     ↓
[Backend - Flask] (Port 5000)
     ↓        ↓
[Redis]   [PostgreSQL]
```

### Workflow:
1. User opens the webpage
2. Frontend serves HTML/CSS/JS files
3. JavaScript sends request to Backend API
4. Backend increments counter in Redis
5. Backend stores visit info in PostgreSQL
6. Result is displayed to user

## Components

### 1. Frontend (Nginx)
- **Technology**: Nginx Alpine
- **Port**: 80
- **Role**: Serves UI and acts as reverse proxy to Backend
- **Files**: index.html, style.css, script.js, nginx.conf

### 2. Backend (Flask)
- **Technology**: Python 3.11 + Flask
- **Port**: 5000
- **Role**: Handles business logic, connects to Redis and PostgreSQL
- **Libraries**: flask, redis, psycopg2

### 3. PostgreSQL Database
- **Technology**: PostgreSQL 15 Alpine
- **Port**: 5432
- **Role**: Persistent storage of visit data
- **Volume**: db-data for data persistence

### 4. Redis Cache
- **Technology**: Redis 7 Alpine
- **Port**: 6379
- **Role**: Fast in-memory counter for visits

## Service Communication

All services communicate via **Service Names** (not IPs):

- Frontend → Backend: `http://backend:5000`
- Backend → Database: `host='database'`
- Backend → Redis: `host='redis'`

All containers are in the `visit-network` bridge network.

**Benefits:**
- Flexibility (IP changes don't break connections)
- Better readability
- Enhanced security
- Automatic DNS resolution by Docker

## Why This Architecture?

1. **Separation of Concerns**: Each container has a single responsibility
2. **Scalability**: Services can be scaled independently
3. **Maintainability**: Easy to update individual components
4. **Data Persistence**: Volume ensures data survives container removal
5. **Performance**: Redis for fast operations, PostgreSQL for reliability

## Project Structure
```
visit-counter/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── .env
├── .env.example
└── README.md
```

## How to Run

### Prerequisites
- Docker (v20+)
- Docker Compose (v2+)
- Linux OS (tested on Kali Linux)

### Steps

1. **Navigate to project directory:**
```bash
cd visit-counter
```

2. **Run the system:**
```bash
docker compose up --build
```

For background execution:
```bash
docker compose up -d --build
```

3. **Check container status:**
```bash
docker ps
```

You should see 4 containers with status "Up".

4. **Access the application:**

Open browser and go to:
```
http://localhost
```

### Useful Commands

**View logs:**
```bash
docker logs visit-counter-backend
docker logs visit-counter-frontend
```

**Stop system:**
```bash
docker compose down
```

**Stop and remove volumes:**
```bash
docker compose down -v
```

**Restart a container:**
```bash
docker restart visit-counter-backend
```

## Data Persistence Test

To verify Volume functionality:

1. Visit the page several times (counter reaches e.g., 25)
2. Remove database container:
```bash
docker rm -f visit-counter-database
```
3. Restart system:
```bash
docker compose up -d
docker restart visit-counter-backend
```
4. Refresh page - counter should continue from 25, not start from 1

This proves data is stored in the Volume and survives container deletion.

## Environment Variables

Configuration is managed via `.env` file:

- `DB_HOST`: Database hostname
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `REDIS_HOST`: Redis hostname

See `.env.example` for template.

## Key Features

- ✅ Containerization with Docker
- ✅ Multi-service orchestration with Docker Compose
- ✅ Service Name based networking (no hardcoded IPs)
- ✅ Data persistence with Docker Volume
- ✅ Environment variable management
- ✅ Lightweight Alpine-based images
- ✅ Dependency management with depends_on

## Technologies Used

- **Docker & Docker Compose**: Containerization
- **Nginx**: Web server and reverse proxy
- **Flask**: Python web framework for API
- **PostgreSQL**: Relational database
- **Redis**: In-memory data store for caching

## Notes

- All inter-container communication uses Service Names
- Database and Redis are not exposed externally (security)
- Alpine images reduce container size
- Volume ensures data persists across container lifecycles

---

**Developed as part of Software Engineering course project**
