# 🔐 MQL BackEnd — Django REST API for Authentication

Welcome to the official **MQL BackEnd** repository — a secure, scalable, and lightweight authentication system built using **Django** and **Django REST Framework (DRF)**. This project provides clean and modular endpoints for registering, logging in, and managing user sessions via token-based authentication.

---

## 🚀 Key Features

- ✅ **User Registration & Login APIs**
- 🔐 **Token-based Authentication System**
- 📦 **RESTful API built with Django REST Framework**
- ⚡ **Frontend Integration via `fetch()` (JavaScript)**
- 🧱 **SQLite Database for lightweight development**
- 🔧 **Modular, Scalable Django Architecture**
- 📁 **Frontend-friendly API handler (`apiHandeler.js`)**

---

## 📂 Project Structure

MQL-BackEnd/
├── MQL/ # Main Django settings & root config
│ ├── settings.py
│ └── urls.py
├── AuthenticationSystem/ # Authentication app (core logic)
│ ├── models.py # User model(s) and logic
│ ├── views.py # API endpoints
│ ├── serializers.py # DRF serializers
│ └── admin.py
├── apiHandeler.js # JS utility for API requests
├── manage.py # Django management script
├── db.sqlite3 # Development SQLite DB
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## 🧠 Technologies Used

| Area        | Technology                     |
|-------------|---------------------------------|
| Backend     | Django, Django REST Framework   |
| Auth        | Token Authentication (DRF Token)|
| Database    | SQLite                          |
| Frontend    | Vanilla JavaScript (`fetch`)    |
| API Format  | REST / JSON                     |

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/EstarioRios/MQL-BackEnd.git
cd MQL-BackEnd
```
### 2. Create a Virtual Environment
```bash
Copy
Edit
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```
### 4. Install Dependencies
```bash
Copy
Edit
pip install -r requirements.txt
```
### 5. Run Migrations
```bash
Copy
Edit
python manage.py migrate
```
### 6. Start the Development Server
```bash
Copy
Edit
python manage.py runserver
The backend will be available at: http://127.0.0.1:8000/
```

## 🔌 API Endpoints
Endpoint	Method	Description
```txt
 ✅ Signup normal user (user_type="normal")
     POST /api/signup/
     Required fields: email, phone_number, password, first_name, last_name

 ✅ Login (JWT-based, fallback to manual login if token not valid)
     POST /api/login/
     Required fields: email, password
     Optional field: remember (boolean)

 ✅ Manually login if JWT not present or failed
    POST /api/manual-login/
    Required fields: email, password

 ✅ Create new admin user (Requires JWT and must be admin)
     POST /api/create-admin/
     Required fields: first_name, last_name, email, password, phone_number

 ✅ Submit a new order (Authenticated users only)
    POST /api/sub-order /
    Required fields: title, description, tools_description
```
These endpoints are implemented inside the AuthenticationSystem app using Django REST views and serializers.

## 🧪 Frontend Integration
The file apiHandeler.js contains utility methods to:

Call /register and /login endpoints using fetch()

Store and reuse the token for authenticated requests

Add Authorization headers automatically

Ideal for static sites, SPAs, or mobile hybrid apps.

### ✅ Use Cases
Full-stack starter authentication for Django projects

Backend for React/Vue frontend with token-based login

Educational use for learning DRF + Auth patterns

### 👨‍💻 Maintainer
Built with ❤️ by Abolfazl Khezri
GitHub: @EstarioRios

### 📃 License
This project is licensed under the MIT License.

✨ Future Enhancements (Optional Ideas)

✅ Add JWT support with refresh tokens

✅ Email confirmation during registration

✅ Rate limiting and login throttling

✅ Admin dashboard or user management panel

✅ Docker support for production deployment

