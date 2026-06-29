from django.urls import path
from .views import *

urlpatterns = [
    path("cl_home/",cl_home),
    path("cl_login_reg/",cl_login_reg),
    path("cl_reg/",cl_reg),
    path("cl_validate_login/",cl_validate_login),
    path("cl_logout/",cl_logout),
    path("cl_req/",cl_req),
    path("cl_req_sym/",cl_req_sym),
    path("cl_req_kp_up/<str:rh_id>/",cl_req_kp_up),
    path("cl_req_bp_up/<str:rh_id>/",cl_req_bp_up),
    path("cl_bp_status/",cl_bp_status),
    path("cl_kp_status/",cl_kp_status),
    path("cl_bp_pte/",cl_bp_pte),
    path("cl_kp_pte/",cl_kp_pte),
    path("cl_bp_pte_up/<str:rh_id>/",cl_bp_pte_up),
    path("cl_kp_pte_up/<str:rh_id>/",cl_kp_pte_up),
]
