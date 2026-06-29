from django.urls import path
from .views import *

urlpatterns = [
    path("rt_home/", rt_home),
    path("rt_login_reg/",rt_login_reg),
    path("rt_reg/",rt_reg),
    path("rt_validate_login/",rt_validate_login),
    path("rt_logout/",rt_logout),
    path("rt_bp_req/",rt_bp_req),
    path("rt_kp_req/",rt_kp_req),
    path("rt_bp_analyze/",rt_bp_analyze),
    path("rt_kp_analyze/",rt_kp_analyze),
    path("rt_bp_analyze_process/<str:cl_rh_id>/",rt_bp_analyze_process),
    path("rt_kp_analyze_process/<str:cl_rh_id>/",rt_kp_analyze_process),
    path("rt_bp_report/",rt_bp_report),
    path("rt_kp_report/",rt_kp_report),
]