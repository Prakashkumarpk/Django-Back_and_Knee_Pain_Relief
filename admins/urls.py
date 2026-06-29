from django.urls import path
from .views import *

urlpatterns = [
    path("",home),
    path("admins/",admins),
    path("admins_home/",admins_home),
    path("admins_login/",admins_login),
    path("admins_logout/",admins_logout),
    path("accept/<int:id>/",accept),
    path("reject/<int:id>/",reject),
    path("cl_approve/",cl_approve),
    path("pm_approve/",pm_approve),
    path("rt_approve/",rt_approve),
    path("ef_approve/",ef_approve),
    path("bp_admins_status/",bp_admins_status),
    path("kp_admins_status/",kp_admins_status),
    path("ad_cl_bp_report/",ad_cl_bp_report),
    path("ad_cl_kp_report/",ad_cl_kp_report),
    path("ad_pm_bp_report/",ad_pm_bp_report),
    path("ad_pm_kp_report/",ad_pm_kp_report),
    path("ad_rt_bp_report/",ad_rt_bp_report),
    path("ad_rt_kp_report/",ad_rt_kp_report),
    path("ad_ef_bp_report/",ad_ef_bp_report),
    path("ad_ef_kp_report/",ad_ef_kp_report),
    path("bp_generate_pdf/<str:cl_rh_id>/",bp_generate_pdf),
    path("kp_generate_pdf/<str:cl_rh_id>/",kp_generate_pdf),

]
