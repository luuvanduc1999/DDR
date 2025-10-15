# Docker-Django-React Project

## First Time Docker Setup

### Prerequisites
- Docker Desktop installed on your machine
- Git installed on your machine

### Development Environment Setup

1. Clone the repository (if you haven't already):
```bash
git clone <your-repository-url>
cd Django-CFS
```

2. Build and start the development environment:
```bash
cd docker/dev
docker-compose up --build
```

3. Run database migrations:
```bash
# In a new terminal window
docker-compose exec web python manage.py migrate
```

4. Create a superuser for admin access:
```bash
# Create superuser for Django admin
docker-compose exec web python manage.py createsuperuser
# Follow the prompts to create your admin user:
# - Enter username
# - Enter email (optional)
# - Enter and confirm password
```

This will:
- Build the frontend React application
- Build the Django backend
- Set up the development database
- Configure Nginx as a reverse proxy
- Set up the database schema
- Create an admin user for accessing the Django admin interface

The services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin interface: http://localhost:8000/admin

### Production Environment Setup

1. Navigate to the production docker compose directory:
```bash
cd docker/prod
```

2. Build and start the production environment:
```bash
docker-compose up --build
```

3. Run database migrations in production:
```bash
# In a new terminal window
docker-compose exec web python manage.py migrate
```

4. Create a superuser for production admin access:
```bash
# Create superuser for Django admin
docker-compose exec web python manage.py createsuperuser
# Follow the prompts to create your admin user:
# - Enter username
# - Enter email (optional)
# - Enter and confirm password
```

The production environment will be available at:
- Application: http://localhost:80 (or just http://localhost)
- Backend API: http://localhost/api
- Admin interface: http://localhost/admin

### Docker Commands Reference

- Start the services:
```bash
docker-compose up
```

- Start services in detached mode (background):
```bash
docker-compose up -d
```

- Stop the services:
```bash
docker-compose down
```

- View logs:
```bash
docker-compose logs
```

- View logs for a specific service:
```bash
docker-compose logs [service_name]  # e.g., docker-compose logs web
```

- Rebuild the services:
```bash
docker-compose up --build
```

### Project Structure

```
backend/           # Django backend
├── Dockerfile.dev  # Development Dockerfile
├── Dockerfile.prod # Production Dockerfile
└── ...

frontend/          # React frontend
├── Dockerfile.dev
├── Dockerfile.prod
└── ...

docker/
├── dev/           # Development Docker configuration
│   └── docker-compose.yml
└── prod/          # Production Docker configuration
    ├── docker-compose.yml
    └── nginx/     # Nginx configuration for production
```

### Database Management Commands

- Create new migrations after model changes:
```bash
docker-compose exec web python manage.py makemigrations
```

- Apply migrations:
```bash
docker-compose exec web python manage.py migrate
```

- Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

- Open Django shell:
```bash
docker-compose exec web python manage.py shell
```

### Troubleshooting

1. If containers fail to start:
   - Check if all required ports (80, 3000, 8000) are available
   - Ensure Docker Desktop is running
   - Try stopping any existing containers: `docker-compose down`

2. If you can't access the services:
   - Verify all containers are running: `docker-compose ps`
   - Check container logs: `docker-compose logs`
   - Ensure no other services are using the required ports

3. For permission issues:
   - On Linux/Mac, you might need to use `sudo` with Docker commands
   - Check file permissions in mounted volumes

### Development Notes

- The development environment uses hot-reloading for both frontend and backend
- Changes to the React code will automatically rebuild in development mode
- Django development server will reload on Python file changes
- Database data persists in Docker volumes

For additional configuration options or environment-specific settings, refer to the docker-compose files in the respective directories.
