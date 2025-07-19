# Auto-PFT Docker Setup

This repository contains a full-stack application with both client and backend components, organized using Docker and Docker Compose for streamlined development and deployment.

## Architecture Overview

The application consists of three main components:

- **Backend**: FastAPI-based Python server located in the `server/` directory
- **Frontend**: React/Vite-based client application located in the `client/` directory  
- **Redis**: In-memory data store for caching and session management

## Prerequisites

Before running the application, ensure you have the following installed:

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Git (for cloning the repository)

## Development Setup

For development, use the `docker-compose.dev.yml` configuration which includes hot-reloading and volume mounting for live code changes.

### Starting Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd auto-pft

# Start all services in development mode
docker-compose -f docker-compose.dev.yml up --build

# Or run in detached mode
docker-compose -f docker-compose.dev.yml up -d --build
```

### Development Services

- **Frontend**: Available at http://localhost:3000
- **Backend**: Available at http://localhost:8000
- **API Documentation**: Available at http://localhost:8000/docs

### Development Features

- **Hot Reloading**: Both frontend and backend automatically reload when code changes
- **Volume Mounting**: Local code changes are immediately reflected in containers
- **Debug Mode**: Backend runs with `--reload` flag for development

## Production Deployment

For production deployment, use the main `docker-compose.yml` configuration which includes optimized builds and production settings.

### Starting Production Environment

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Services

- **Frontend**: Available at http://localhost:80
- **Backend**: Available at http://localhost:8000
- **Redis**: Available at http://localhost:6379

## Service Configuration

### Backend Service

The backend service is built from the `server/` directory and includes:

- **Base Image**: Python 3.11 slim
- **Dependencies**: Installed from `requirements.txt`
- **Port**: Exposes port 8000
- **Command**: Runs with Uvicorn ASGI server

### Frontend Service

The frontend service uses a multi-stage build:

- **Build Stage**: Node.js 20 Alpine for building the React application
- **Runtime Stage**: Nginx Alpine for serving static files
- **Port**: Exposes port 80 (production) or 3000 (development)
- **Proxy**: Nginx configured to proxy API requests to backend

### Redis Service

- **Image**: Redis 7 Alpine
- **Port**: Exposes port 6379
- **Persistence**: Data stored in Docker volume

## Environment Variables

Create a `.env` file in the root directory to configure environment-specific variables:

```env
# Backend Configuration
PYTHONPATH=/app
PYTHONUNBUFFERED=1

# Frontend Configuration
VITE_API_URL=http://localhost:8000

# Redis Configuration
REDIS_URL=redis://redis:6379
```

## Docker Commands Reference

### Building Services

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build without cache
docker-compose build --no-cache
```

### Managing Services

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View service status
docker-compose ps
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

### Executing Commands

```bash
# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh

# Run one-time command
docker-compose run backend python manage.py migrate
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 3000, 8000, and 6379 are not in use by other applications
2. **Permission Issues**: On Linux, you may need to run Docker commands with `sudo`
3. **Build Failures**: Clear Docker cache with `docker system prune -a`

### Debugging

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs [service-name]

# Access container shell
docker-compose exec [service-name] bash

# Inspect container
docker inspect [container-name]
```

## File Structure

```
auto-pft/
├── client/                 # Frontend React application
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   ├── Dockerfile         # Production build
│   ├── Dockerfile.dev     # Development build
│   ├── nginx.conf         # Nginx configuration
│   └── .dockerignore      # Docker ignore rules
├── server/                # Backend FastAPI application
│   ├── agent/             # AI agent modules
│   ├── models/            # Data models
│   ├── utils/             # Utility functions
│   ├── main.py            # Application entry point
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Docker build configuration
│   └── .dockerignore      # Docker ignore rules
├── docker-compose.yml     # Production configuration
├── docker-compose.dev.yml # Development configuration
└── README.md              # This documentation
```

## Contributing

When contributing to this project:

1. Use the development environment for testing changes
2. Ensure all services start successfully with `docker-compose -f docker-compose.dev.yml up`
3. Test the production build before submitting changes
4. Update documentation as needed

## License



