# Shri Krishna Udhav Memorial Trust - Dynamic Backend

This is the FastAPI backend for the Shri Krishna Udhav Memorial Trust NGO website. It provides a fully dynamic website with database-driven content management for events, projects, gallery, news, team members, and more.

## Features

- **Dynamic Content Management**: Events, Projects, Gallery, News, Team Members
- **Form Submissions**: Contact forms and donation tracking
- **RESTful API**: Complete API endpoints for all entities
- **Database**: SQLite for local development, easily upgradeable to PostgreSQL
- **Template Engine**: Jinja2 for dynamic HTML rendering
- **File Upload**: Support for gallery image uploads
- **Image Storage**: Uploaded files stored in /uploads directory

## Project Structure

\\\
backend/
├── main.py              # FastAPI application
├── database.py          # Database configuration
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic validation schemas
├── requirements.txt     # Python dependencies
├── templates/           # Jinja2 HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   ├── about.html      # About page
│   ├── mission.html    # Mission & Vision
│   ├── objective.html  # Objectives
│   ├── events.html     # Events listing
│   ├── team.html       # Team members
│   ├── gallery.html    # Gallery
│   ├── project.html    # Projects
│   ├── donate.html     # Donation page
│   ├── contact.html    # Contact page
│   ├── privacy.html    # Privacy policy
│   ├── disclaimer.html # Disclaimer
│   ├── terms.html      # Terms & conditions
│   └── refund.html     # Refund policy
├── static/              # CSS, JS, Images
│   ├── style.css       # Main stylesheet
│   ├── script.js       # Frontend scripts
│   ├── main.js         # Additional JS
│   └── Images/         # Logo, banner, etc.
├── uploads/             # User uploaded files
└── shree_krishna.db    # SQLite database (auto-created)
\\\

## Setup Instructions

### 1. Install Python Dependencies

\\\ash
pip install -r requirements.txt
\\\

### 2. Database Setup

The database will be automatically created when you run the application for the first time. SQLite database file will be created as shree_krishna.db.

### 3. Run the FastAPI Server

\\\ash
python main.py
\\\

Or using uvicorn directly:

\\\ash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\\\

### 4. Access the Application

- **Website**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Events
- GET /api/events - Get all events
- GET /api/events/{id} - Get single event
- POST /api/events - Create event
- PUT /api/events/{id} - Update event
- DELETE /api/events/{id} - Delete event

### Projects
- GET /api/projects - Get all projects
- GET /api/projects/{id} - Get single project
- POST /api/projects - Create project
- PUT /api/projects/{id} - Update project
- DELETE /api/projects/{id} - Delete project

### Gallery
- GET /api/gallery - Get all gallery images
- POST /api/gallery/upload - Upload gallery image
- DELETE /api/gallery/{id} - Delete gallery image

### News
- GET /api/news - Get all news
- GET /api/news/{id} - Get single news
- POST /api/news - Create news
- PUT /api/news/{id} - Update news
- DELETE /api/news/{id} - Delete news

### Team
- GET /api/team - Get all team members
- GET /api/team/{id} - Get single team member
- POST /api/team - Create team member
- PUT /api/team/{id} - Update team member
- DELETE /api/team/{id} - Delete team member

### Contact & Donations
- POST /api/contact - Submit contact form
- GET /api/contact - Get all contact submissions
- POST /api/donate - Record donation
- GET /api/donations - Get all donations

### Health Check
- GET /api/health - Check server status

## Example API Requests

### Create an Event
\\\ash
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Health Camp 2025",
    "description": "Free health checkups for senior citizens",
    "location": "Khukhundoo",
    "image_url": "https://example.com/image.jpg"
  }'
\\\

### Upload Gallery Image
\\\ash
curl -X POST http://localhost:8000/api/gallery/upload \
  -F "title=Event Photo" \
  -F "description=Photo from health camp" \
  -F "file=@/path/to/image.jpg"
\\\

### Submit Contact Form
\\\ash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210",
    "subject": "Support Inquiry",
    "message": "I want to know more about your programs"
  }'
\\\

## Database Models

### Event
- id, title, description, image_url, date, location, created_at, updated_at

### Project
- id, title, description, image_url, category, created_at, updated_at

### GalleryImage
- id, title, description, image_url, uploaded_at

### News
- id, title, content, image_url, published, published_date, created_at, updated_at

### Contact
- id, name, email, phone, subject, message, read, submitted_at

### Donation
- id, donor_name, donor_email, amount, transaction_id, status, message, donation_date

### TeamMember
- id, name, position, bio, photo_url, email, phone, created_at

## Configuration

### Database URL
To use PostgreSQL instead of SQLite, modify the DATABASE_URL in \database.py\:

\\\python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
\\\

### Server Configuration
To change host/port, modify the \main.py\ at the bottom:

\\\python
uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)
\\\

## File Upload Configuration

Uploaded files are stored in the \/uploads\ directory. Ensure this directory exists and is writable by the application.

## Development

The server runs in reload mode for development. Any changes to Python files will automatically reload the server.

## Production Deployment

For production:

1. Set \eload=False\ in main.py
2. Use a production ASGI server like Gunicorn with Uvicorn:
   \\\ash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   \\\
3. Use PostgreSQL instead of SQLite
4. Set up HTTPS/SSL
5. Configure proper security headers

## Troubleshooting

### Port already in use
Change port in main.py to an available port (default: 8000)

### Database lock error
Ensure only one instance of the application is running

### Static files not loading
Verify static files are copied to \ackend/static\ directory

### Image upload fails
Check /uploads directory permissions and available disk space

## License

This project is developed for Shri Krishna Udhav Memorial Trust.

## Support

For issues or feature requests, contact: krishnaudhavtrust@gmail.com
