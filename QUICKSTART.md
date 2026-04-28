# 🚀 Quick Start Guide

Get the NGO website running in 5 minutes!

## ⚡ Express Setup

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create & Configure .env
```bash
cp .env.example .env
# Edit .env with a text editor and set:
# - SESSION_SECRET_KEY (any random string)
# - ENVIRONMENT=development
# - ADMIN_USERNAME=admin
# - ADMIN_PASSWORD=password123
```

### 4. Start Server
```bash
python -m uvicorn main:app --reload
```

### 5. Login
- Open: http://localhost:8000/admin/login
- Username: `admin`
- Password: (from ADMIN_PASSWORD in .env)

---

## 🎯 Key Features

✅ **Admin Dashboard**: Manage donations, events, volunteers, contacts  
✅ **Payment Gateway**: Razorpay integration with 80G receipts  
✅ **Email Notifications**: Confirmations and receipts  
✅ **Security**: Rate limiting, password reset, audit logs  
✅ **Database**: SQLite (includes sample data)  

---

## 📝 First Steps

1. **Donations Page**: http://localhost:8000/donate
2. **Contact Form**: http://localhost:8000/contact
3. **Admin Dashboard**: http://localhost:8000/admin/dashboard
4. **Volunteer Management**: http://localhost:8000/admin/volunteers
5. **Event Management**: http://localhost:8000/admin/events

---

## 🔧 Testing Payment (No Card Required)

```bash
GET http://localhost:8000/api/donation/test-success
```

This creates a test donation with receipt PDF.

---

## 📧 Email Setup (Optional)

To receive email confirmations:

1. **Gmail**: Use app password (Settings > Security > App passwords)
2. Add to .env:
```bash
EMAIL_PROVIDER=smtp
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=16-char-app-password
```

---

## 📚 Full Documentation

- **SETUP.md**: Complete setup & deployment guide
- **FIXES_SUMMARY.md**: All improvements & fixes applied
- **API Docs**: http://localhost:8000/docs

---

## 🆘 Common Issues

| Issue | Fix |
|-------|-----|
| Port 8000 in use | `python -m uvicorn main:app --reload --port 8001` |
| SESSION_SECRET_KEY error | Add SESSION_SECRET_KEY to .env |
| Database locked | `pkill -9 python` then restart |
| Emails not sending | Check SMTP settings in .env |

---

## 📞 Next Steps

1. ✅ Try the donation flow
2. ✅ Test admin dashboard
3. ✅ Review audit logs
4. ✅ Configure email (optional)
5. ✅ Read SETUP.md for production deployment

---

**Need help?** Check SETUP.md troubleshooting section or review logs in terminal.

Enjoy! 🎉
