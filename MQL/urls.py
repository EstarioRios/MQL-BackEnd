from django.urls import path
from AuthenticationSystem import views

urlpatterns = [
    # ✅ Signup normal user (user_type="normal")
    # POST /api/signup/
    # Required fields: email, phone_number, password, first_name, last_name
    path("signup/", views.signup, name="signup"),
    # ✅ Login (JWT-based, fallback to manual login if token not valid)
    # POST /api/login/
    # Required fields: email, password
    # Optional field: remember (boolean)
    path("login/", views.login, name="login"),
    # ✅ Manually login if JWT not present or failed
    # POST /api/manual-login/
    # Required fields: email, password
    path("manual-login/", views.manual_login, name="manual_login"),
    # ✅ Create new admin user (Requires JWT and must be admin)
    # POST /api/create-admin/
    # Required fields: first_name, last_name, email, password, phone_number
    path("create-admin/", views.create_admin, name="create_admin"),
    # ✅ Submit a new order (Authenticated users only)
    # POST /api/sub-order /
    # Required fields: title, description, tools_description
    path("sub-order/", views.sub_order, name="sub_order"),
]
