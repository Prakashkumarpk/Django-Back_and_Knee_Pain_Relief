from django.urls import path
from .views import *

urlpatterns = [
    path("pm_home/",pm_home),
    path("pm_login_reg/",pm_login_reg),
    path("pm_reg/",pm_reg),
    path("pm_validate_login/",pm_validate_login),
    path("pm_logout/",pm_logout),
    path("pm_kp_req/",pm_kp_req),
    path("pm_bp_req/",pm_bp_req),
    path("pm_bp_analyze/",pm_bp_analyze),
    path("pm_kp_analyze/",pm_kp_analyze),
    path("pm_bp_analyze_process/<str:cl_rh_id>/",pm_bp_analyze_process),
    path("pm_kp_analyze_process/<str:cl_rh_id>/",pm_kp_analyze_process),
    path("pm_bp_report/",pm_bp_report),
    path("pm_kp_report/",pm_kp_report),
]