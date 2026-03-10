# DevWars: Multiplayer Coding Arena

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-22+-green)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7+-brightgreen)](https://www.mongodb.com/)
[![Fastify](https://img.shields.io/badge/Fastify-4.26-000000)](https://www.fastify.io/)
[![Docker](https://img.shields.io/badge/Docker-v24+-blue)](https://www.docker.com/)


**DevWars** is a real-time multiplayer competitive coding platform where developers compete head-to-head in coding battles. From algorithm races to debugging challenges, DevWars provides a secure, scalable, and engaging environment for coders to showcase their skills.


---


## Table of Contents


- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Game Modes](#game-modes)
- [Core Features](#core-features)
- [Sandbox Service](#sandbox-service)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Socket Events](#socket-events)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)


---


## Key Features


- **Real-Time Multiplayer**: Compete against other developers in live coding battles with WebSocket-powered real-time updates
- **Secure Code Execution**: Fully isolated Docker-based sandbox environment for safe code execution
- **Multi-Language Support**: Python, JavaScript, C++, Java, Go, and more
- **High Performance**: Built with Fastify and BullMQ for sub-second execution latency
- **Advanced Code Editor**: Monaco Editor with syntax highlighting, auto-completion, and multi-theme support
- **Match History and Analytics**: Track your progress with detailed match history and performance analytics
- **Leaderboard System**: Global and mode-specific leaderboards with ELO-based rating system
- **Tournament Support**: Participate in scheduled tournaments with brackets and prizes
- **Code Quality Analysis**: Get insights on code complexity, security issues, and best practices


---


## Tech Stack


### Frontend (code-arena)
- **React 18** with TypeScript
- **Vite** for lightning-fast build tooling
- **Tailwind CSS** for modern, responsive design
- **Monaco Editor** for code editing
- **Socket.io Client** for real-time communication
- **React Query** for server state management
- **Radix UI** for accessible component primitives
- **Framer Motion** for animations


### Backend API
- **Node.js 22** with Express 5
- **MongoDB** with Mongoose ODM
- **Socket.io** with Redis adapter for horizontal scaling
- **JWT** for authentication with refresh tokens
- **Winston** for structured logging


### Sandbox Microservice (compilers/sandbox-service)
- **Fastify** for high-performance HTTP server
- **BullMQ** with Redis for job queue management
- **Dockerode** for Docker container management
- **Pino** for fast structured logging


### Infrastructure
- **Redis** for session storage, caching, and job queues
- **Docker** for containerized code execution
- **MongoDB** for persistent data storage


---


## System Architecture


```
+------------------+     WebSocket      +------------------+
|                  |<------------------>|                  |
|   React Client   |                    |   Main Backend   |
|   (code-arena)   |     HTTP API       |    (Express)     |
|                  |<------------------>|                  |
+------------------+                    +--------+---------+
                                                 |
                                                 | Submit Code
                                                 v
                                        +--------+---------+
                                        |                  |
                                        |   Redis Queue    |
                                        |    (BullMQ)      |
                                        |                  |
                                        +--------+---------+
                                                 |
                                                 | Process Job
                                                 v
                                        +--------+---------+
                                        |                  |
                                        | Sandbox Worker   |
                                        |   (Fastify)      |
                                        |                  |
                                        +--------+---------+
                                                 |
                                                 | Execute
                                                 v
                                        +--------+---------+
                                        |                  |
                                        | Docker Container |
                                        | (Isolated)       |
                                        |                  |
                                        +------------------+
```


---


## Project Structure


```
DevWars/
+-- code-arena/                    # Frontend React application
|   +-- src/
|   |   +-- components/            # Reusable UI components
|   |   |   +-- ui/               # Shadcn/ui components
|   |   |   +-- room/             # Room-specific components
|   |   |   +-- history/          # Match history components
|   |   +-- contexts/             # React contexts (Auth, Socket)
|   |   +-- hooks/                # Custom React hooks
|   |   +-- layouts/              # Page layouts
|   |   +-- lib/                  # Utilities and API client
|   |   +-- pages/                # Page components
|   |   |   +-- app/              # Authenticated app pages
|   |   |   |   +-- Dashboard.tsx
|   |   |   |   +-- Lobby.tsx
|   |   |   |   +-- Room.tsx      # Main game room
|   |   |   |   +-- History.tsx
|   |   |   |   +-- Leaderboard.tsx
|   |   |   |   +-- Profile.tsx
|   |   |   |   +-- Settings.tsx
|   |   +-- styles/               # Global styles
|   +-- package.json
|
+-- backend/                       # Main API server
|   +-- src/
|   |   +-- modules/
|   |   |   +-- auth/             # Authentication module
|   |   |   +-- users/            # User management
|   |   |   +-- rooms/            # Room/lobby management
|   |   |   +-- matches/          # Match lifecycle
|   |   |   +-- questions/        # Question bank
|   |   |   +-- evaluation/       # Code evaluation
|   |   |   +-- competition/      # Competition history
|   |   |   +-- stats/            # Statistics
|   |   +-- services/             # Business logic services
|   |   |   +-- execution.service.js
|   |   +-- socket/               # Socket.io handlers
|   |   +-- utils/                # Utilities
|   |   +-- cron/                 # Scheduled jobs
|   |   +-- config/               # Configuration
|   |   +-- server.js             # Entry point
|   +-- package.json
|
+-- compilers/                     # Sandbox microservice
|   +-- sandbox-service/
|   |   +-- src/
|   |   |   +-- api/              # API routes
|   |   |   +-- workers/          # Job workers
|   |   |   +-- executors/        # Language executors
|   |   |   +-- config/           # Configuration
|   |   +-- server.js             # Entry point
|   |   +-- Dockerfile            # Sandbox Docker image
|   |   +-- docker-compose.yml
|
+-- ml-service/                    # ML prediction service (optional)
```


---


## Game Modes


### Debug Battle
The classic mode where players race to find and fix bugs in code snippets. Each question comes with:
- Buggy starter code
- Hidden test cases
- Time limit for solving


Scoring is based on test cases passed, time to solve, and code quality.


### Bug Hunt
Hunt down specific bugs in larger codebases. Players must:
- Identify the exact line causing the issue
- Provide a minimal fix
- Pass all test cases


### Code Golf
Solve problems with the shortest possible code. Scoring criteria:
- Number of characters
- Code correctness
- Execution efficiency


---


## Core Features


### Authentication System
- Email/password registration with bcrypt hashing
- JWT-based access tokens (15-minute expiry)
- Refresh tokens with HTTP-only cookies (7-day expiry)
- "Remember Me" functionality
- Session management with MongoDB store


### Room System
- Create public or private rooms
- Invite codes for private rooms
- Host controls (start match, kick players)
- Player ready status
- Real-time player presence


### Match System
- Automatic question selection by difficulty
- Configurable time limits (10-30 minutes)
- Live code sharing between players
- Real-time test results
- First-blood bonuses for fastest correct solutions


### Code Execution
- Direct VM execution for JavaScript (instant results)
- Docker sandbox for other languages
- Timeout protection (5 seconds max)
- Memory limits (128MB default)
- Security sandboxing (no file system, network access)


### Rating System
- ELO-based rating calculation
- Separate ratings for each game mode
- Rank tiers: Bronze, Silver, Gold, Platinum, Diamond, Master, Grandmaster
- Win/loss streak bonuses


---


## Sandbox Service


The heart of DevWars is the **Sandbox Service**, a secure microservice that executes untrusted code in hardened Docker containers.


### Security Features
- **Network Isolation**: All containers have networking disabled
- **Resource Limits**: CPU (0.5 core) and Memory (128MB) caps per execution
- **Read-Only Filesystem**: Container filesystem is read-only
- **Auto-Cleanup**: Containers destroyed immediately after execution
- **Seccomp Profiles**: Advanced security profiles to block dangerous syscalls
- **User Namespacing**: Code runs as non-root user inside containers


### Supported Languages
| Language | Version | Timeout | Memory |
|----------|---------|---------|--------|
| JavaScript | Node 22 | 5s | 128MB |
| Python | 3.12 | 5s | 128MB |
| Java | 21 | 5s | 256MB |
| C++ | GCC 13 | 5s | 256MB |
| Go | 1.22 | 5s | 128MB |


---


## Setup and Installation


### Prerequisites
- Node.js 20+ 
- MongoDB 7+
- Redis 7+
- Docker (for sandbox)


### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/devwars.git
cd devwars
```


### 2. Install Dependencies
```bash
# Frontend
cd code-arena
npm install


# Backend
cd ../backend
npm install


# Sandbox Service
cd ../compilers/sandbox-service
npm install
```


### 3. Configure Environment


**Backend (.env)**
```bash
cd backend
cp .env.example .env
```


**Sandbox Service (.env)**
```bash
cd compilers/sandbox-service
cp .env.example .env
```


### 4. Start Services
```bash
# Start MongoDB and Redis (using Docker)
docker run -d -p 27017:27017 --name mongodb mongo:7
docker run -d -p 6379:6379 --name redis redis:7


# Start Backend
cd backend
npm run dev


# Start Sandbox Service (in new terminal)
cd compilers/sandbox-service
npm run start:all


# Start Frontend (in new terminal)
cd code-arena
npm run dev
```


### 5. Seed Questions
```bash
cd backend
node src/modules/questions/question.seed.js
```


### 6. Access the Application
- Frontend: http://localhost:8080
- Backend API: http://localhost:3000
- Sandbox API: http://localhost:3001


---


## Environment Variables


### Backend Environment
```bash
# Server
PORT=3000
NODE_ENV=development


# Sandbox Service
SANDBOX_SERVICE_URL=http://localhost:3001


# Frontend CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8080


# Database
MONGODB_URI=mongodb://localhost:27017/devwars
REDIS_URL=redis://localhost:6379


# Authentication
JWT_SECRET=your-jwt-secret
JWT_REFRESH_SECRET=your-refresh-secret
JWT_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
SESSION_SECRET=your-session-secret


# Security
BCRYPT_ROUNDS=10
```


### Sandbox Service Environment
```bash
PORT=3001
NODE_ENV=development
REDIS_HOST=localhost
REDIS_PORT=6379
```


---


## API Reference


### Authentication


#### Register User
```
POST /api/v1/auth/register
Body: { username, email, password }
```


#### Login
```
POST /api/v1/auth/login
Body: { email, password, rememberMe }
Response: { user, accessToken }
```


#### Get Current User
```
GET /api/v1/auth/me
Headers: Authorization: Bearer <accessToken>
```


#### Refresh Token
```
POST /api/v1/auth/refresh
Cookies: refreshToken
```


#### Logout
```
POST /api/v1/auth/logout
Headers: Authorization: Bearer <accessToken>
```


### Rooms


#### Get All Rooms
```
GET /api/v1/lobby/rooms?mode=debug&status=waiting
```


#### Create Room
```
POST /api/v1/lobby/rooms
Body: { name, mode, maxPlayers, isPrivate, difficulty, timer }
```


#### Join Room
```
POST /api/v1/lobby/rooms/:id/join
Body: { inviteCode? }
```


#### Start Match
```
POST /api/v1/lobby/rooms/:id/start-match
```


### Evaluation


#### Evaluate Code
```
POST /api/v1/evaluation/evaluate
Body: { questionId, code, language }
Response: {
  score,
  passedTests,
  totalTests,
  results: [{ passed, input, expectedOutput, actualOutput, error }],
  codeQuality: { overall, maintainability, security, performance },
  complexity: { time, space }
}
```


### Questions


#### Get Questions
```
GET /api/v1/questions?mode=debug&difficulty=medium
```


#### Get Question by ID
```
GET /api/v1/questions/:id
```


### Sandbox Service


#### Execute Code
```
POST /api/execute
Body: { language, code, input, timeout }
Response: { status, jobId }
```


#### Get Job Result
```
GET /api/job/:jobId
Response: { status, stdout, stderr, runtime, memory }
```


---


## Socket Events


### Client to Server
| Event | Payload | Description |
|-------|---------|-------------|
| `lobby:join` | `{}` | Join lobby to receive room updates |
| `lobby:leave` | `{}` | Leave lobby |
| `room:join` | `{ roomId }` | Join a specific room |
| `room:leave` | `{ roomId }` | Leave a room |
| `room:create` | `{ name, mode, ... }` | Create a new room |
| `room:ready` | `{ roomId, ready }` | Toggle ready status |
| `match:code-update` | `{ roomId, code }` | Share code with opponent |


### Server to Client
| Event | Payload | Description |
|-------|---------|-------------|
| `lobby:rooms` | `{ rooms, stats }` | List of available rooms |
| `room:created` | `{ room }` | New room created |
| `room:updated` | `{ room }` | Room state updated |
| `room:deleted` | `{ roomId }` | Room deleted |
| `match:started` | `{ matchId, question, timerDuration }` | Match started |
| `match:code-update` | `{ code }` | Opponent code update |
| `match:end` | `{ results }` | Match ended |


---


## Database Schema


### User
```javascript
{
  username: String,          // Unique
  email: String,             // Unique
  password: String,          // Bcrypt hashed
  stats: {
    rating: Number,          // Default: 1000
    wins: Number,
    losses: Number,
    matchesPlayed: Number
  },
  createdAt: Date,
  updatedAt: Date
}
```


### Room
```javascript
{
  name: String,
  mode: String,              // debug, bug-hunt, code-golf
  status: String,            // waiting, playing, finished
  difficulty: String,        // easy, medium, hard, extreme
  inviteCode: String,        // 8-character code
  isPrivate: Boolean,
  maxPlayers: Number,
  timer: Number,             // Minutes
  players: [{
    userId: ObjectId,
    username: String,
    joinedAt: Date,
    isReady: Boolean
  }],
  createdBy: ObjectId,
  createdAt: Date
}
```


### Question
```javascript
{
  id: String,                // Custom ID (q-xxxxx)
  mode: String,
  title: String,
  description: String,
  language: String,
  difficulty: String,
  starterCode: String,       // Buggy code for debug mode
  solution: String,          // Correct solution
  testcases: [{
    input: String,
    output: String,
    isHidden: Boolean,
    description: String
  }],
  hints: [String],
  tags: [String],
  timeLimit: Number,
  memoryLimit: Number,
  isActive: Boolean
}
```


### Match
```javascript
{
  roomId: ObjectId,
  questionId: ObjectId,
  status: String,            // waiting, active, finished
  players: [{
    playerId: ObjectId,
    username: String,
    score: Number,
    solvedAt: Date
  }],
  submissions: [{
    playerId: ObjectId,
    code: String,
    score: Number,
    testResults: Array,
    submittedAt: Date
  }],
  winner: {
    playerId: ObjectId,
    username: String
  },
  startTime: Date,
  endTime: Date,
  duration: Number,
  timerDuration: Number
}
```


---


## Contributing


1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


### Development Guidelines
- Follow the existing code style
- Write tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR


---


## License


This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---


## Acknowledgments


- Monaco Editor by Microsoft
- Shadcn/ui for beautiful React components
- Fastify team for the high-performance web framework
- BullMQ for reliable job processing


---


Built for the developer community
