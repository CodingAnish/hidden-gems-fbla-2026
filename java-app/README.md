# Hidden Gems — Java Enterprise Stack

Enterprise-grade, cross-platform application built with **Java 17**, **Spring Boot 3.2**, and a **React** frontend. Designed for scalability, RESTful APIs, JWT authentication, and deployment via Docker.

## Architecture

- **Backend**: Spring Boot (Web, Data JPA, Security, Validation), SQLite (or switch to PostgreSQL via config), JWT auth, layered design (Controller → Service → Repository).
- **Frontend**: React 18 + TypeScript + Vite + **Tailwind CSS**. Modern, responsive UI; API client with JWT auth. **PWA-ready** (installable, offline-capable).
- **Mobile**: Same React app can be wrapped with **Capacitor** or **Ionic** for native iOS/Android; or use as a **PWA** in the browser.
- **Deployment**: Docker Compose for API + static frontend; cloud-ready (env-based config).

## Requirements

- **Backend**: Java 17+, Maven 3.8+
- **Frontend**: Node.js 18+, npm or yarn
- **Optional**: Docker & Docker Compose

## Quick Start

### 1. Run the backend (API)

```bash
cd java-app/backend
mvn spring-boot:run
```

API base: `http://localhost:8080/api`  
Endpoints: `GET /api/health`, `POST /api/auth/login`, `POST /api/auth/register`, `GET /api/businesses`, etc.

### 2. Run the frontend (dev)

```bash
cd java-app/frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to the backend.

### 3. Build frontend for production

```bash
cd java-app/frontend
npm run build
```

Serve the `dist/` folder with any static host or use the Docker setup below.

## Docker

Build and run API + pre-built frontend:

```bash
cd java-app/frontend && npm run build && cd ..
docker-compose up --build
```

- API: `http://localhost:8080`
- Frontend (via nginx): `http://localhost:3000` (proxies `/api` to the API container)

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_PATH` | SQLite database path | `./data/hiddengems.db` |
| `PORT` | Server port | `8080` |
| `JWT_SECRET` | Secret for JWT (min 32 chars) | (dev default in application.yml) |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:5173,http://localhost:3000` |

## Project Structure

```
java-app/
├── backend/                    # Spring Boot API
│   ├── src/main/java/com/hiddengems/
│   │   ├── config/             # Security, Web, Beans, DataSeeder
│   │   ├── controller/         # Auth, Business, Health
│   │   ├── dto/                # Request/Response DTOs
│   │   ├── entity/             # User, Business, Favorite (JPA)
│   │   ├── exception/          # GlobalExceptionHandler
│   │   ├── repository/         # JPA repositories
│   │   ├── security/           # JWT filter & service
│   │   └── service/            # AuthService, BusinessService
│   ├── src/main/resources/
│   │   └── application.yml
│   ├── pom.xml
│   └── Dockerfile
├── frontend/                   # React + Vite + Tailwind + PWA
│   ├── src/
│   │   ├── api/                # API client, auth helpers
│   │   ├── context/            # AuthContext
│   │   ├── pages/              # Home, Login, Register, BusinessDetail
│   │   └── theme/              # design-system.css (Tailwind + components)
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── vite.config.ts          # VitePWA plugin for PWA
│   └── nginx.conf              # For Docker serve
├── docker-compose.yml
└── README.md
```

## API Overview

- **POST /api/auth/login** — `{ "emailOrUsername", "password" }` → JWT + user info
- **POST /api/auth/register** — `{ "username", "email", "password" }` → JWT + user info
- **GET /api/health** — Health check (no auth)
- **GET /api/businesses** — Paginated list (optional auth for `favorited`)
- **GET /api/businesses/{id}** — Single business
- **GET /api/businesses/search?q=** — Search by name
- **GET /api/businesses/city/{city}** — By city

Protected endpoints (future): pass `Authorization: Bearer <token>`.

## Frontend stack (modern web UI)

The app uses **React + Tailwind CSS** so the UI stays clean and modern with minimal custom CSS. This matches how most production apps are built; Java UI frameworks (e.g. JavaFX) are not used for the web/mobile client.

- **Tailwind CSS**: Utility-first styling, responsive layout (`sm:`, `md:`), design tokens in `tailwind.config.js` (primary, surface, content width).
- **PWA**: `vite-plugin-pwa` adds a web app manifest and service worker. Users can “Add to Home Screen” on mobile; the app works offline for cached routes. Add `icon-192.png` and `icon-512.png` to `frontend/public/` for better install experience.
- **Mobile (native-style)**:
  - **Capacitor**: Run `npm run build`, then add the web app to a Capacitor project and build iOS/Android. Same React app, same API.
  - **Ionic**: Use the Ionic CLI with React and point it at this app, or use Ionic components inside the existing React app.
  - **PWA**: Deploy the built site to HTTPS; mobile browsers can install it as an app. No app store required.

## Extending

- **Database**: To use PostgreSQL, add the driver and set `spring.datasource.url` (and remove SQLite dialect).
- **CI/CD**: Add a pipeline that runs `mvn test`, `npm run build`, and builds Docker images.
