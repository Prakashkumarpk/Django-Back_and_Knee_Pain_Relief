from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from admins.models import *

# Create your views here.

def home(request):
    return render(request,'home/home.html')

def admins(request):
    return render(request,"admins/admins_login.html")

def admins_home(request):
    return render(request,"admins/admins_home.html")


def admins_login(request):
    if request.method == "POST":
        try:
            email=request.POST['email']
            password=request.POST['password']
            if email=="admin@gmail.com" and password=="admin":
                messages.info(request,"Admin Login Successful")
                return redirect("/admins_home/")
            elif email !="admin@gmail.com" and password=="admin":
                messages.error(request, "Incorrect email!")
                return render(request,"admins/admins_login.html")
            elif email =="admin@gmail.com" and password!="admin":
                messages.error(request, "Incorrect Password!")
                return render(request,"admins/admins_login.html")
            elif email !="admin@gmail.com" and password!="admin":
                messages.error(request, "Incorrect email and Password!")
                return render(request,"admins/admins_login.html")
            else:
                return render(request,"admins/admins_login.html")
        except:
            messages.error(request, "Incorrect Credentials!")
    return render(request,"admins/admins_login.html")

def admins_logout(request):
    messages.info(request,"Admins Logout Successfull")
    return redirect("/")

import random
def accept(request,id):
    data=registration.objects.get(id=id)
    password=random.randint(1000,9999)
    print(password)
    data.password=password
    data.rh_id=f"SG:{password}"
    data.save()

    send_mail(
        '{0}:Username and Password'.format(data.department),
        'Hello {0},\n Your {1} profile has been Approved.\n Your Username is "{2}" and Password is "{3}".\n Make sure you use this Username and Password while your logging in to the "{4}" Portal.\n Thank You '.format(
            data.name,data.department, data.email,data.password,data.department.capitalize()),
        'demosample47@gmail.com',
        [data.email],
        fail_silently=False,
    )

    data.accept=True
    data.reject=False
    data.save()
    messages.info(request,f"{data.rh_id} : {data.department} Approval Successful")
    return redirect("/admins_home/")


def reject(request,id):
    data = registration.objects.get(id=id)
    data.accept=False
    data.reject=True
    data.save()

    subject = 'Client Rejection'
    plain_message = f"Hi {data.name},\nYour registration was rejected due to some reasons.try this later!"
    send_mail(subject, plain_message, 'prakashkumar03.surya@gmail.com', [data.email], fail_silently=False)

    # data.delete()
    messages.info(request, "Rejection Mail Sent to Client")
    return redirect("/admins_home/")

def cl_approve(request):
    data=registration.objects.filter(department="CLIENT")
    return render(request,'admins/cl_approve.html', {'data':data})

def pm_approve(request):
    data=registration.objects.filter(department="PAINMETRICS")
    return render(request,'admins/pm_approve.html', {'data':data})

def rt_approve(request):
    data=registration.objects.filter(department="RELIEFTHERAPY")
    return render(request,'admins/rt_approve.html', {'data':data})

def ef_approve(request):
    data=registration.objects.filter(department="EFFECTIVENESS")
    return render(request,'admins/ef_approve.html', {'data':data})

def bp_admins_status(request):
    # data=registration.objects.all()
    obj=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,'admins/bp_admins_status.html', {'obj':obj})

def kp_admins_status(request):
    # data=registration.objects.all()
    obj=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,'admins/kp_admins_status.html', {'obj':obj})

def ad_cl_bp_report(request):
    data=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,'admins/ad_cl_bp_report.html', {'data':data})

def ad_cl_kp_report(request):
    data=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,'admins/ad_cl_kp_report.html', {'data':data})

def ad_pm_bp_report(request):
    data=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,'admins/ad_pm_bp_report.html', {'data':data})

def ad_pm_kp_report(request):
    data=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,'admins/ad_pm_kp_report.html', {'data':data})

def ad_rt_bp_report(request):
    data=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,'admins/ad_rt_bp_report.html', {'data':data})

def ad_rt_kp_report(request):
    data=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,'admins/ad_rt_kp_report.html', {'data':data})

def ad_ef_bp_report(request):
    data=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,'admins/ad_ef_bp_report.html', {'data':data})

def ad_ef_kp_report(request):
    data=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,'admins/ad_ef_kp_report.html', {'data':data})


from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.core.mail import EmailMessage
from django.http import JsonResponse
import os

def bp_generate_pdf(request, cl_rh_id):
    # Retrieve ResidentialDetails object or return 404 if not found
    user = pain_relief.objects.get(cl_rh_id=cl_rh_id, type_of_pain="back_pain")

    title = "BACK PAIN RELIEF REPORT"

    # Client Info Table - no headers, just data
    client_info = [
        ["CLIENT ID", user.cl_rh_id],
        ["TYPE OF PAIN", "BACK PAIN"],
    ]

    # Data grouped into sections
    sections = {
        "SYMPTOMS (%) BEFORE THERAPY:": [  # Changed heading here
            ["DULL ACHING PAIN(%)", user.dull_aching_pain],
            ["SHARP STABBING PAIN(%)", user.sharp_stabbing_pain],
            ["MUSCLE SPASMS(%)", user.muscle_spasms],
            ["RADIATING PAIN(%)", user.radiating_pain],
            ["NUMBNESS OR TINGLING(%)", user.numbness_or_tingling],
            ["WEAKNESS(%)", user.weakness],
            ["STIFFNESS(%)", user.b_stiffness],
            ["PAIN WITH MOVEMENT(%)", user.pain_with_movement],
            ["PAIN THAT WORSENS AT NIGHT(%)", user.pain_that_worsens_at_night],
            ["FATIGUE(%)", user.fatigue],
            ["LOSS OF RANGE OF MOTION(%)", user.loss_of_range_of_motion],
            ["FEVER OR CHILLS(%)", user.fever_or_chills],
        ],
        "PAINETRICS ANALYZE:": [
            ["SEVERITY(%)", user.severity],
            ["TYPE OF BACKPAIN", user.type_of_backpain],
        ],
        "RELIEFTHERAPY ANALYZE:": [
            ["THERAPY", user.therapy],
            ["DURATION", user.duration],
        ],
        "SYMPTOMS (%) AFTER THERAPY:": [  # Changed heading here
            ["PAIN BEFORE THERAPY (REDUCED %)", user.r_pain_intensity_before_therapy],
            ["PAIN AFTER THERAPY (REDUCED %)", user.r_pain_intensity_after_therapy],
            ["MUSCLE SPASMS (REDUCED %)", user.r_muscle_spams],
            ["RADIATING PAIN (REDUCED %)", user.r_radiating_pain],
            ["NUMBNESS OR TINGLING (REDUCED %)", user.r_numbness_or_tingling],
            ["STIFFNESS (REDUCED %)", user.r_b_stiffness],
            ["PAIN WITH MOVEMENT (REDUCED %)", user.r_pain_with_movement],
            ["PAIN THAT WORSENS AT NIGHT (REDUCED %)", user.r_pain_that_worsens_at_night],
            ["FATIGUE (REDUCED %)", user.r_fatigue],
            ["LOSS OF RANGE OF MOTION (REDUCED %)", user.r_loss_of_range_of_motion],
            ["FEVER OR CHILLS (REDUCED %)", user.r_fever_or_chills],
            ["OVERALL RELIEF PERCEPTION (%)", user.r_overall_relief_preception],
            
        ],
        "EFFECTIVENESS ANALYZE:": [
            ["EFFECTIVENESS (%)", user.effectiveness],
        ],
    }

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    # Title
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_para = Paragraph(title, title_style)
    story.append(title_para)
    story.append(Spacer(1, 12))

    # Add Heading for Client Info
    client_info_heading = Paragraph("CLIENT DETAILS", styles["Heading2"])  # Added client details heading
    story.append(client_info_heading)
    story.append(Spacer(1, 6))

    # Add Client Info Table - no headers, just data
    client_info_table = Table(client_info, colWidths=[200, 150])
    client_info_table.setStyle(
        TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ]))
    story.append(client_info_table)
    story.append(Spacer(1, 20))  # Add space after client info

    # Iterate through sections and create tables
    for section, data in sections.items():
        # Add section title
        section_title = Paragraph(section, styles["Heading2"])
        story.append(section_title)
        story.append(Spacer(1, 6))

        # Adjust column widths and table data
        if section == "SYMPTOMS (%) AFTER THERAPY:" or section == "SYMPTOMS (%) BEFORE THERAPY:":
            col_widths = [250, 150]  # Wider column for symptoms
        else:
            col_widths = [200, 150]

        table_data = [["Title", "Value"]] + data  # Add headers Title and Value

        # Create table for the section
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(
            TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.green),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]))
        story.append(table)
        story.append(Spacer(1, 20))  # Add space after each table

    # Build PDF
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()

    # Prepare HTTP response with PDF data
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{title}_{user.cl_rh_id}.pdf"'
    response.write(pdf_data)

    # Save PDF file to the model field
    user.bp_f_report.save(f"{title}_{user.cl_rh_id}.pdf", ContentFile(pdf_data))
    user.bp_f_rep_view = True
    user.save()

    # Redirect after generating PDF
    messages.info(request, f"Backpain Report for {user.cl_rh_id} Generated Successfully")

    # #sending the report to the client
    # data = registration.objects.get(rh_id=cl_rh_id)

    # subject = 'BackPain Report'
    # plain_message = f"Hi {data.name},\nWe hope this email finds you in good health. Below is a summary of your personalized pain management report:\n\n{user.bp_f_report}\n\nWe are here to support you every step of the way toward recovery. If you have any questions or need further assistance, feel free to contact us"
    # send_mail(subject, plain_message, 'prakashkumar03.surya@gmail.com', [data.email], fail_silently=False)

     # Email the PDF
    try:
        client = registration.objects.get(rh_id=cl_rh_id)
        email_subject = "Your Back Pain Relief Report"
        email_body = f"Dear {client.name},\n\nPlease find your report attached.\n\nBest Regards,\nYour Team"

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email='your_email@example.com',
            to=[client.email]
        )

        # Attach the PDF directly
        email.attach(f"{title}_{user.cl_rh_id}.pdf", pdf_data, "application/pdf")
        email.send()

        messages.info(request, f"Back Pain Report for {user.cl_rh_id} sent to {client.email}.")
    except registration.DoesNotExist:
        messages.error(request, f"Client with ID {cl_rh_id} does not exist.")
    except Exception as e:
        messages.error(request, f"Error sending email: {str(e)}")
    
    return redirect("/bp_admins_status/")





from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.core.files.base import ContentFile
import os
from .models import pain_relief, registration  # Adjust your imports as per your app structure


def kp_generate_pdf(request, cl_rh_id):
    # Retrieve ResidentialDetails object or return 404 if not found
    user = pain_relief.objects.get(cl_rh_id=cl_rh_id, type_of_pain="knee_pain")
    title = "KNEE PAIN RELIEF REPORT"

    # Client Info Table - no headers, just data
    client_info = [
        ["CLIENT ID", user.cl_rh_id],
        ["TYPE OF PAIN", "KNEE PAIN"],
    ]

    # Data grouped into sections
    sections = {
        "SYMPTOMS (%) BEFORE THERAPY:": [
            ["PAIN(%)", user.pain],
            ["SWELLING(%)", user.swelling],
            ["STIFFNESS(%)", user.stiffness],
            ["WARMTH AND REDNESS(%)", user.warmth_and_redness],
            ["WEAKNESS OR INSTABILITY(%)", user.weakness_or_instability],
            ["POPPING OR GRINDING SENSATION(%)", user.popping_or_grinding_sensation],
            ["LIMITED RANGE OF MOTION(%)", user.limites_range_of_motion],
            ["PAIN WITH CERTAIN MOVEMENT(%)", user.pain_with_certain_movements],
            ["TENDERNESS(%)", user.tenderness],
            ["BEARING WEIGHT(%)", user.bearing_weight],
        ],
        "PAINETRICS ANALYZE:": [
            ["SEVERITY(%)", user.severity],
            ["TYPE OF BACKPAIN", user.type_of_backpain],
        ],
        "RELIEFTHERAPY ANALYZE:": [
            ["THERAPY", user.therapy],
            ["DURATION", user.duration],
        ],
        "SYMPTOMS (%) AFTER THERAPY:": [
            ["PAIN BEFORE THERAPY (REDUCED %)", user.r_pain_intensity_before_therapy],
            ["PAIN AFTER THERAPY (REDUCED %)", user.r_pain_intensity_after_therapy],
            ["SWELLING (REDUCED %)", user.r_swelling],
            ["STIFFNESS (REDUCED %)", user.r_stiffness],
            ["WARMTH AND REDNESS (REDUCED %)", user.r_warmth_and_redness],
            ["WEAKNESS OR INSTABILITY (REDUCED %)", user.r_weakness_or_instability],
            ["POPPING OR GRINDING SENSATION (REDUCED %)", user.r_popping_or_grinding_sensation],
            ["LIMITED RANGE OF MOTION (REDUCED %)", user.r_limited_range_of_motion],
            ["PAIN WITH CERTAIN MOVEMENT (REDUCED %)", user.r_pain_with_certain_movements],
            ["TENDERNESS (REDUCED %)", user.r_tenderness],
            ["BEARING WEIGHT (REDUCED %)", user.r_bearing_weight],
            ["OVERALL RELIEF PERCEPTION (%)", user.r_overall_relief_preception],
        ],
        "EFFECTIVENESS ANALYZE:": [
            ["EFFECTIVENESS (%)", user.effectiveness],
        ],
    }

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    # Title
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_para = Paragraph(title, title_style)
    story.append(title_para)
    story.append(Spacer(1, 12))

    # Add Heading for Client Info
    client_info_heading = Paragraph("CLIENT DETAILS", styles["Heading2"])
    story.append(client_info_heading)
    story.append(Spacer(1, 6))

    # Add Client Info Table - no headers, just data
    client_info_table = Table(client_info, colWidths=[200, 150])
    client_info_table.setStyle(
        TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ])
    )
    story.append(client_info_table)
    story.append(Spacer(1, 20))

    # Iterate through sections and create tables
    for section, data in sections.items():
        section_title = Paragraph(section, styles["Heading2"])
        story.append(section_title)
        story.append(Spacer(1, 6))

        col_widths = [250, 150]
        table_data = [["Title", "Value"]] + data

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.green),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ])
        )
        story.append(table)
        story.append(Spacer(1, 20))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()

    # Save PDF to the model field
    user.kp_f_report.save(f"{title}_{user.cl_rh_id}.pdf", ContentFile(pdf_data))
    user.kp_f_rep_view = True
    user.save()

    # Email the PDF
    try:
        client = registration.objects.get(rh_id=cl_rh_id)
        email_subject = "Your Knee Pain Relief Report"
        email_body = f"Dear {client.name},\n\nPlease find your report attached.\n\nBest Regards,\nYour Team"

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email='your_email@example.com',
            to=[client.email]
        )

        # Attach the PDF directly
        email.attach(f"{title}_{user.cl_rh_id}.pdf", pdf_data, "application/pdf")
        email.send()

        messages.info(request, f"Knee Pain Report for {user.cl_rh_id} sent to {client.email}.")
    except registration.DoesNotExist:
        messages.error(request, f"Client with ID {cl_rh_id} does not exist.")
    except Exception as e:
        messages.error(request, f"Error sending email: {str(e)}")

    # Redirect after generating PDF
    messages.info(request, f"Knee Pain Report for {user.cl_rh_id} generated successfully.")
    return redirect("/kp_admins_status/")










