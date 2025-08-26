# Portfolio Backend API

A complete FastAPI backend for a personal portfolio website with SQLite database, authentication, and file upload capabilities.

## Features

- **Complete CRUD Operations** for all portfolio sections
- **SQLite Database** with SQLAlchemy ORM
- **API Key Authentication** for secure endpoints
- **Image Upload & Management** with local storage
- **Contact Form** with email notifications
- **Soft Delete** functionality for all records
- **Pydantic Validation** for all data models
- **Auto-generated API Documentation** with Swagger UI

## Database Tables

- **Home**: Personal information and hero section
- **Certifications**: Professional certifications
- **Honors & Awards**: Recognition and achievements
- **Experience**: Work history and roles
- **Projects**: Portfolio projects with tech stack
- **Services**: Freelance services offered
- **Blogs**: Blog posts with slug-based routing
- **Contact**: Contact form submissions

## Quick Start

### 1. Installation

\`\`\`bash
# Clone the repository
git clone <your-repo-url>
cd portfolio-backend

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 2. Environment Setup

\`\`\`bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
\`\`\`

### 3. Run the Application

\`\`\`bash
# Start the development server
uvicorn app.main:app --reload
\`\`\`

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Public Endpoints
- `GET /api/home/` - Get home/personal info
- `GET /api/certifications/` - Get all certifications
- `GET /api/honors-awards/` - Get all honors & awards
- `GET /api/experience/` - Get work experience
- `GET /api/projects/` - Get all projects
- `GET /api/services/` - Get all services
- `GET /api/blogs/` - Get all blog posts
- `GET /api/blogs/slug/{slug}` - Get blog by slug
- `POST /api/contact/` - Submit contact form
- `GET /media/{filename}` - Serve uploaded files

### Protected Endpoints (Require X-API-KEY header)
- `POST /api/{resource}/` - Create new record
- `PUT /api/{resource}/{id}` - Update existing record
- `DELETE /api/{resource}/{id}` - Soft delete record
- `POST /api/upload/image` - Upload image file
- `DELETE /api/upload/media/{filename}` - Delete uploaded file

## Authentication

All write operations require the `X-API-KEY` header:

\`\`\`bash
curl -X POST "http://localhost:8000/api/home/" \
  -H "X-API-KEY: your_secret_api_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "headline": "Software Engineer", "about": "..."}'
\`\`\`

## File Upload

Upload images and files:

\`\`\`bash
curl -X POST "http://localhost:8000/api/upload/image" \
  -H "X-API-KEY: your_secret_api_key" \
  -F "file=@image.jpg"
\`\`\`

Response:
\`\`\`json
{
  "filename": "uuid-generated-name.jpg",
  "url": "/media/uuid-generated-name.jpg",
  "original_filename": "image.jpg"
}
\`\`\`

## Contact Form Email

Contact form submissions are automatically emailed to `aryankhatri.forwork@gmail.com`. Configure SMTP settings in `.env`:

\`\`\`env
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_FROM=your_email@gmail.com
\`\`\`

## Database Schema

The application uses SQLite with the following key features:
- **Auto-incrementing IDs** for all tables
- **Timestamps** (created_at, updated_at) for all records
- **Soft delete** via `is_active` boolean field
- **Unique constraints** where appropriate (e.g., blog slugs)

## Development

### Database Migrations

\`\`\`bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
\`\`\`

### Project Structure

\`\`\`
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and settings
├── database.py          # Database connection and session
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── routes/              # API route handlers
├── auth/                # Authentication dependencies
└── uploads/             # File upload directory
\`\`\`

## Production Deployment

1. **Environment Variables**: Update `.env` with production values
2. **Database**: Consider PostgreSQL for production
3. **File Storage**: Consider cloud storage (AWS S3, etc.)
4. **Security**: Use strong API keys and HTTPS
5. **CORS**: Configure allowed origins properly

## API Documentation

Visit `/docs` for interactive Swagger UI documentation with all endpoints, schemas, and examples.

## License

This project is licensed under the MIT License.
