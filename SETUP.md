# 🚀 NGO Website - Complete Setup & Deployment Guide

## Overview

This is a production-ready FastAPI-based NGO website with:
- **Admin Dashboard**: Event, donation, volunteer, and contact management
- **Payment Integration**: Razorpay for secure donations with 80G receipts
- **Email Notifications**: Contact confirmations, donation receipts, volunteer updates
- **Security**: Rate limiting, password reset, session management, audit logging
- **Database**: SQLite for development, easily upgradeable to PostgreSQL

---

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip / conda
- Git

### Step 1: Clone & Setup Project

```bash
# Navigate to project directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your values
nano .env  # or use your editor
```

**Required fields in .env:**
```bash
SESSION_SECRET_KEY=your_random_secure_key_here
ENVIRONMENT=development
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password_123

# For testing payments (get from Razorpay dashboard)
RAZORPAY_KEY_ID=rzp_test_XXXXXXX
RAZORPAY_KEY_SECRET=your_secret_key

# For email (optional - skip to test without emails)
EMAIL_PROVIDER=smtp
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your_app_password  # Gmail: Settings > Security > App passwords
```

### Step 3: Run Development Server

```bash
# Start FastAPI server
python -m uvicorn main:app --reload

# Server will be available at: http://localhost:8000
# Admin dashboard: http://localhost:8000/admin/login
# API docs: http://localhost:8000/docs
```

### Step 4: Test Login

- **URL**: http://localhost:8000/admin/login
- **Username**: admin (or value from ADMIN_PASSWORD env)
- **Password**: (value from ADMIN_PASSWORD env)

---

## 📧 Email Configuration

### Option 1: Gmail SMTP (Recommended for Testing)

1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account > Security > App passwords
3. Generate an app password for "Mail" and "Windows"
4. Copy the password (16 characters, no spaces)
5. Add to .env:
```bash
EMAIL_PROVIDER=smtp
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
```

### Option 2: SendGrid (Production)

1. Create SendGrid account at sendgrid.com
2. Create API key
3. Add to .env:
```bash
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxx
SENDER_EMAIL=noreply@yourdomain.com
```

### Option 3: Skip Email (Testing Only)

Leave EMAIL variables blank. The app will log but not send emails.

---

## 🔐 Security Setup

### Generate Secure Session Key

```python
import secrets
key = secrets.token_urlsafe(32)
print(key)
# Add the output to SESSION_SECRET_KEY in .env
```

### Admin Password Requirements

- Minimum 8 characters
- Must contain uppercase AND lowercase letters
- Must contain at least one number
- Cannot contain special characters in Bcrypt

**Example**: `Admin@2024`

---

## 💳 Razorpay Integration

### Test Mode Setup

1. Go to Razorpay Dashboard: https://dashboard.razorpay.com
2. Navigate to: Account & Settings > API Keys
3. Copy:
   - Key ID (starts with `rzp_test_`)
   - Key Secret
4. Add to .env:
```bash
RAZORPAY_KEY_ID=rzp_test_XXXXXXX
RAZORPAY_KEY_SECRET=your_secret_key
```

### Test Payment Flow

1. Go to http://localhost:8000/donate
2. Fill donation form (any amount)
3. Click "Donate Securely"
4. Use Razorpay test card:
   - Card: 4111 1111 1111 1111
   - Expiry: Any future date
   - CVV: Any 3 digits

---

## 🗄️ Database Management

### View/Modify Database

```bash
# Using SQLite CLI
sqlite3 SKUMT_NGO.db

# Useful queries:
sqlite> .tables  # List all tables
sqlite> SELECT * FROM admin_users;  # View admins
sqlite> SELECT * FROM donations;  # View donations
sqlite> .quit  # Exit
```

### Backup Database

```bash
# Create backup
cp SKUMT_NGO.db SKUMT_NGO.db.backup

# Schedule regular backups (cron job):
0 2 * * * cp /path/to/SKUMT_NGO.db /path/to/backups/SKUMT_NGO_$(date +\%Y\%m\%d).db
```

### Upgrade to PostgreSQL (Production)

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update database.py:
# Old: DATABASE_URL = "sqlite:///./SKUMT_NGO.db"
# New: DATABASE_URL = "postgresql://user:password@localhost:5432/skumt_db"

# Create PostgreSQL database:
createdb skumt_db

# Run migrations if using Alembic
# (Optional: set up Alembic for version control)
```

---

## 🧪 Testing Features

### 1. Test Payment Without Razorpay
```
GET /api/donation/test-success
```

### 2. Test Email Service
```bash
# Check if emails are configured
curl http://localhost:8000/api/health
```

### 3. Test Rate Limiting
Try logging in 6 times with wrong password - should be blocked on 6th attempt

### 4. Test Password Reset
1. Go to /admin/login
2. Click "Forgot Password?"
3. Enter email
4. Check email (if configured) for reset link

### 5. View Audit Logs
- URL: http://localhost:8000/admin/audit
- Filter by action, user, or date range

---

## 📦 Production Deployment

### Pre-Deployment Checklist

```bash
# Update environment to production
ENVIRONMENT=production

# Generate strong session key (see Security Setup above)

# Use production Razorpay keys

# Set strong admin password

# Configure email provider (SMTP or SendGrid)

# Update ALLOWED_ORIGINS for CORS

# Set up HTTPS/SSL certificate

# Configure backup strategy
```

### Deployment Options

#### Option 1: Heroku
```bash
# Install Heroku CLI
# Create Procfile:
# web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Deploy
git push heroku main
```

#### Option 2: AWS EC2
```bash
# Install on Ubuntu
sudo apt update
sudo apt install python3-pip python3-venv

# Clone, setup, and run with Gunicorn:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

#### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Setup SSL/HTTPS

```bash
# Using Let's Encrypt (free)
sudo certbot certonly --standalone -d yourdomain.com

# Configure FastAPI to use HTTPS
# (Use Nginx reverse proxy or Uvicorn SSL parameters)
```

### Environment Variables in Production

Store sensitive data in environment variables, never in code:
- Use AWS Systems Manager Parameter Store
- Use Heroku Config Vars
- Use Docker secrets
- Use .env.production (NOT in git)

```bash
# Don't commit .env to git
echo ".env" >> .gitignore
echo ".env.production" >> .gitignore
```

---

## 🛠️ API Endpoints Reference

### Public Endpoints
```
GET  /                           # Homepage
GET  /about, /mission, /events   # Static pages
GET  /donate                     # Donation page
POST /contact                    # Submit contact form
POST /submit-volunteer           # Submit volunteer application
POST /api/donation/verify-payment # Process payment
GET  /api/config/razorpay        # Get payment key
GET  /api/csrf-token             # Get CSRF token
GET  /api/health                 # Health check
```

### Admin Endpoints (Requires Login)
```
GET  /admin/login                # Login page
POST /admin/login                # Submit login
GET  /admin/dashboard            # Dashboard
GET  /admin/donations            # View donations
GET  /admin/contacts             # View contacts (paginated)
GET  /admin/volunteers           # View volunteers
GET  /admin/volunteer/approve/{id}  # Approve volunteer
GET  /admin/volunteer/reject/{id}   # Reject volunteer
GET  /admin/events               # Manage events
POST /admin/events/add           # Create event
GET  /admin/team_members         # Manage team
POST /admin/team/add             # Add team member
GET  /admin/documents            # Manage documents
POST /admin/documents/upload     # Upload document
GET  /admin/audit                # View audit logs
GET  /admin/forgot-password      # Reset password
```

---

## 🐛 Troubleshooting

### Issue: "SESSION_SECRET_KEY not set"
**Solution**: Add SESSION_SECRET_KEY to .env file

### Issue: Emails not sending
**Solution**: 
1. Check SMTP credentials in .env
2. Verify Gmail app password (not regular password)
3. Check firewall allows port 587
4. Enable "Less secure app" if not using app password

### Issue: Razorpay payment fails
**Solution**:
1. Verify RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET
2. Ensure keys are for TEST environment
3. Use test card: 4111 1111 1111 1111

### Issue: Database locked error
**Solution**:
```bash
# Close any open connections
killall -9 python  # Or specific process

# Restart server
python -m uvicorn main:app --reload
```

### Issue: CORS errors in frontend
**Solution**: Update ALLOWED_ORIGINS in main.py or .env

---

## 📊 Performance Optimization

### Database Indexing
```sql
CREATE INDEX idx_donor_email ON donations(donor_email);
CREATE INDEX idx_volunteer_status ON volunteers(status);
CREATE INDEX idx_contact_date ON contacts(submitted_at);
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_events():
    # Cache events for 1 hour
    pass
```

### Pagination
All list endpoints support pagination (10-20 items per page)

---

## 📝 Logging

### View Application Logs

```bash
# Development (console)
# Logs appear in terminal where server is running

# Production (file)
# Configure in main.py:
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Debug Mode

```bash
# Enable detailed logging
LOG_LEVEL=DEBUG python -m uvicorn main:app --reload
```

---

## 🔄 Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/ngo"
mkdir -p $BACKUP_DIR
cp SKUMT_NGO.db "$BACKUP_DIR/SKUMT_NGO_$(date +%Y%m%d_%H%M%S).db"

# Add to crontab:
# 0 */6 * * * /path/to/backup.sh
```

### Restore from Backup

```bash
# Stop server
# Replace database file
cp /backups/SKUMT_NGO_backup.db SKUMT_NGO.db
# Start server
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

1. **Weekly**: Check audit logs for suspicious activity
2. **Monthly**: Review and clean old temporary files
3. **Quarterly**: Update dependencies (`pip list --outdated`)
4. **Annually**: Security audit and penetration testing

### Update Dependencies Safely

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all packages (careful!)
pip install -U -r requirements.txt
```

### Monitor Performance

```python
# Add to main.py for request timing
@app.middleware("http")
async def add_process_time_header(request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Razorpay Integration](https://razorpay.com/docs/)
- [SendGrid Email](https://docs.sendgrid.com/)
- [OWASP Security Guidelines](https://owasp.org/)

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Last Updated**: April 26, 2026
**Version**: 2.0 - Production Ready
**Status**: ✅ All Features Implemented

For issues or feature requests, contact the development team.
