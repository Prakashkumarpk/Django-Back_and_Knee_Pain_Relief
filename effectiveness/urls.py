from django.urls import path
from .views import *

urlpatterns = [
    path("ef_home/",ef_home),
    path("ef_login_reg/",ef_login_reg),
    path("ef_reg/",ef_reg),
    path("ef_validate_login/",ef_validate_login),
    path("ef_logout/",ef_logout),
    path("ef_bp_req/",ef_bp_req),
    path("ef_kp_req/",ef_kp_req),
    path("ef_bp_analyze/",ef_bp_analyze),
    path("ef_kp_analyze/",ef_kp_analyze),
    path("ef_bp_analyze_process/<str:cl_rh_id>/",ef_bp_analyze_process),
    path("ef_kp_analyze_process/<str:cl_rh_id>/",ef_kp_analyze_process),
    path("ef_bp_report/",ef_bp_report),
    path("ef_kp_report/",ef_kp_report),
]