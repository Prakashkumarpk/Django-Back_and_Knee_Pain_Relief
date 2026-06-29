from django.shortcuts import render,redirect
from django.contrib import messages
from admins.models import *

# Create your views here.
def cl_home(request):
    return render(request,"client/cl_home.html")

def cl_login_reg(request):
    return render(request,"client/cl_login_reg.html")

def cl_reg(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        mobile_no=request.POST['mobile_no']
        department=request.POST['department']
        registration(name=name,email=email,mobile_no=mobile_no,department=department).save()
        messages.info(request," Client Registration successful")
        return redirect('/cl_login_reg/')
    else:
        return render(request,'client/cl_login_reg.html')
    

def cl_validate_login(request):
    if request.method=='POST':
        
        email = request.POST['email']
        password = request.POST['password']
        try:        
            data = registration.objects.get(email=email, password=password)
            if data.accept:   
                messages.info(request, "Client Login Successful")
                data.cl_login=True
                data.cl_logout=False
                data.save()       
                return redirect("/cl_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, "client/cl_login_reg.html")
        except:
            messages.info(request, "Wrong Credentials")
            return render(request, "client/cl_login_reg.html")
    return render(request, "client/cl_login_reg.html")


def cl_logout(request):
    data = registration.objects.get(cl_login=True)
    data.cl_logout=True
    data.cl_login=False
    data.save()
    messages.info(request,"Client Logout Successful")
    return redirect("/")

import random
def cl_req(request):
    obj=registration.objects.filter(cl_login=True)
    return render(request,"client/cl_req.html",{"obj":obj})


def cl_req_sym(request):
    obj=registration.objects.filter(cl_login=True)
    obj1=registration.objects.get(cl_login=True)
    if request.method=="POST":
        type_of_pain=request.POST["paintype"]
        if type_of_pain =="knee_pain" and obj1.knee_pain is False: 
            # if registration.knee_pain is False:
            #     obj1=registration.objects.get(cl_login=True,rh_id=rh_id)
            #     obj1.knee_pain = True
            #     obj1.save()
                return render(request,"client/cl_req_ks.html",{"obj":obj})
        # else:
                # messages.info(request,"Requirements Already uploaded")
                # return redirect("/cl_req/")  
        elif type_of_pain=="back_pain" and obj1.back_pain is False:
            # if registration.back_pain is False:
            #     obj2=registration.objects.get(cl_login=True,rh_id=rh_id)
            #     obj2.back_pain=True
            #     obj2.save()
                return render(request,"client/cl_req_bs.html",{"obj":obj})
        else:
            messages.info(request,"Symptoms Already uploaded")
            return redirect("/cl_req/")

    else:
        return redirect("/cl_req/")
    


from django.shortcuts import redirect
from django.contrib import messages
from admins.models import pain_relief

def cl_req_kp_up(request,rh_id):
    data = registration.objects.get(cl_login=True,rh_id=rh_id)
    if data.cl_login and rh_id==data.rh_id:
        if request.method == "POST" and data.knee_pain is False:
            # Create a new instance of pain_relief or retrieve an existing one
            obj = pain_relief(
                cl_rh_id=data.rh_id,
                pain=request.POST.get("pain"),
                swelling=request.POST.get("swelling"),
                stiffness=request.POST.get("stiffness"),
                warmth_and_redness=request.POST.get("warmth_and_redness"),
                weakness_or_instability=request.POST.get("weakness_or_instability"),
                popping_or_grinding_sensation=request.POST.get("popping_or_grinding_sensation"),
                limites_range_of_motion=request.POST.get("limited_range_of_motion"),
                pain_with_certain_movements=request.POST.get("pain_with_certain_movements"),
                tenderness=request.POST.get("tenderness"),
                bearing_weight=request.POST.get("bearing_weight"),
                type_of_pain="knee_pain"
            )

            # Save the new or updated instance
            data.knee_pain = True
            data.save()
            obj.save()
            
            messages.info(request, "KneePain Symptoms Submitted Successfully")
            return redirect("/cl_home/")
        else:
            messages.info(request, "Symptoms Already Uploaded")
            return redirect("/cl_req/")

        

def cl_req_bp_up(request,rh_id):

    data = registration.objects.get(cl_login=True,rh_id=rh_id)

    if data.cl_login is True and data.back_pain is False:
        if request.method == "POST" and rh_id==data.rh_id :
            # Create a new instance of pain_relief or retrieve an existing one
            obj = pain_relief(
                cl_rh_id=data.rh_id,
                dull_aching_pain=request.POST.get("dull_aching_pain"),
                sharp_stabbing_pain=request.POST.get("sharp_stabbing_pain"),
                muscle_spasms=request.POST.get("muscle_spams"),
                radiating_pain=request.POST.get("radiating_pain"),
                numbness_or_tingling=request.POST.get("numbness_or_tingling"),
                weakness=request.POST.get("weakness"),
                b_stiffness=request.POST.get("b_stiffness"),
                pain_with_movement=request.POST.get("pain_with_movement"),
                pain_that_worsens_at_night=request.POST.get("pain_that_worsens_at_night"),
                fatigue=request.POST.get("fatigue"),
                loss_of_range_of_motion=request.POST.get("loss_of_range_of_motion"),
                fever_or_chills=request.POST.get("fever_or_chills"),
                type_of_pain="back_pain"
            )

            # Save the new or updated instance
            data.back_pain = True
            data.save()
            obj.save()
            
            messages.info(request, "BackPain Symptoms Submitted Successfully")
            return redirect("/cl_home/")
        else:
            messages.info(request, "Symptoms Already Uploaded")
            return redirect("/cl_req/")

def cl_bp_status(request):
    data = registration.objects.get(cl_login=True)
    id=data.rh_id
    obj=pain_relief.objects.filter(cl_rh_id=id, type_of_pain ="back_pain")
    return render(request,"client/cl_bp_status.html",{"obj":obj})

def cl_kp_status(request):
    data = registration.objects.get(cl_login=True)
    id=data.rh_id
    obj=pain_relief.objects.filter(cl_rh_id=id, type_of_pain ="knee_pain")
    return render(request,"client/cl_kp_status.html",{"obj":obj})
   

def cl_bp_pte(request):
    obj = registration.objects.get(cl_login=True)
    id = obj.rh_id
    try:
        data = pain_relief.objects.get(cl_rh_id=id, type_of_pain="back_pain")
        obj1 = pain_relief.objects.filter(cl_rh_id=id, type_of_pain="back_pain")
        
        # Check if both conditions for `data` are True
        if data.pm_bp_scan is True and data.rt_bp_scan is True:
            
            if data.r_back_pain is False:
                return render(request, "client/cl_bp_pte.html", {"obj1": obj1})
            else:
                messages.info(request,"Back Pain Post Therapy Details Already Uploaded")
                return redirect("/cl_home/")
        else:
            messages.info(request, "Therapy Not Suggested Yet")
            return redirect("/cl_home/")
        
    except pain_relief.DoesNotExist:
        # Handle the case where no data is found for back pain
        messages.error(request, "Back Pain data not uploaded yet.")
        return redirect("/cl_home/")

def cl_kp_pte(request):
    obj=registration.objects.get(cl_login=True)
    id=obj.rh_id
    try:
        data=pain_relief.objects.get(cl_rh_id=id,type_of_pain="knee_pain")
        obj1=pain_relief.objects.filter(cl_rh_id=id,type_of_pain="knee_pain")
        if data.pm_kp_scan is True and data.rt_kp_scan is True:
            if data.r_knee_pain is False:
                return render(request,"client/cl_kp_pte.html",{"obj1":obj1})
            else:
                messages.info(request,"knee Pain Post Therapy Details Already Uploaded")
                return redirect("/cl_home/")
        else:
            messages.info(request,"Therapy Not Suggested Yet")
            return redirect("/cl_home/")
    except pain_relief.DoesNotExist:
        # Handle the case where no data is found for knee pain
        messages.error(request, "knee Pain data not uploaded yet.")
        return redirect("/cl_home/")
    


from django.shortcuts import render, redirect
from django.contrib import messages

def cl_bp_pte_up(request, rh_id):
    data = pain_relief.objects.get(type_of_pain="back_pain", cl_rh_id=rh_id)

    if data.type_of_pain == "back_pain" and data.cl_rh_id == rh_id:
        if request.method == "POST" and data.r_back_pain is False:
            try:
                # Convert the input to the correct types
                data.r_pain_intensity_before_therapy = int(request.POST.get("r_pain_intensity_before_therapy", 0))
                data.r_pain_intensity_after_therapy = int(request.POST.get("r_pain_intensity_after_therapy", 0))
                data.r_fever_or_chills = int(request.POST.get("r_fever_or_chills", 0))
                data.r_muscle_spams = int(request.POST.get("r_muscle_spams", 0))
                data.r_radiating_pain = int(request.POST.get("r_radiating_pain", 0))
                data.r_numbness_or_tingling = int(request.POST.get("r_numbness_or_tingling", 0))
                data.r_b_stiffness = int(request.POST.get("r_b_stiffness", 0))
                data.r_loss_of_range_of_motion = int(request.POST.get("r_loss_of_range_of_motion", 0))
                data.r_pain_with_movement = int(request.POST.get("r_pain_with_movement", 0))
                data.r_pain_that_worsens_at_night = int(request.POST.get("r_pain_that_worsens_at_night", 0))
                data.r_fatigue = int(request.POST.get("r_fatigue", 0))
                data.r_overall_relief_preception = int(request.POST.get("r_overall_relief_preception", 0))

                # Set `r_back_pain` to True and save
                data.r_back_pain = True
                data.save()

                messages.info(request, "Back Pain Post Therapy Evaluation Details Submitted Successfully")
                return redirect("/cl_home/")

            except ValueError:
                # Handle the case where conversion fails
                messages.error(request, "Invalid input format. Please enter valid numbers.")
                return redirect("/cl_home/")
        else:
            messages.info(request, "Post Therapy Details Already Uploaded")
            return redirect("/cl_home/")



def cl_kp_pte_up(request, rh_id):
    data = pain_relief.objects.get(type_of_pain="knee_pain", cl_rh_id=rh_id)
    
    if data.type_of_pain == "knee_pain" and data.cl_rh_id == rh_id:
        if request.method == "POST" and data.r_knee_pain is False:
            # Create a new instance of pain_relief or retrieve an existing one
            data.r_pain_intensity_before_therapy = request.POST.get("r_pain_intensity_before_therapy")
            data.r_pain_intensity_after_therapy = request.POST.get("r_pain_intensity_after_therapy")
            data.r_swelling = request.POST.get("r_swelling")
            data.r_stiffness = request.POST.get("r_stiffness")
            data.r_warmth_and_redness = request.POST.get("r_warmth_and_redness")
            data.r_weakness_or_instability = request.POST.get("r_weakness_or_instability")
            data.r_popping_or_grinding_sensation = request.POST.get("r_popping_or_grinding_sensation")
            data.r_limited_range_of_motion = request.POST.get("r_limited_range_of_motion")
            data.r_pain_with_certain_movements = request.POST.get("r_pain_with_certain_movements")
            data.r_tenderness = request.POST.get("r_tenderness")
            data.r_bearing_weight = request.POST.get("r_bearing_weight")
            data.r_overall_relief_preception = request.POST.get("r_overall_relief_preception")
            # Save the new or updated instance
            data.r_knee_pain = True
            data.save()
            
            messages.info(request, "KneePain Post Therapy Evaluation Submitted Successfully")
            return redirect("/cl_home/")
        else:
            messages.info(request, "Post Therapy Details Already Uploaded")
            return redirect("/cl_req/")
        
    else:
            messages.info(request, "Post Therapy Details Already Uploaded")
            return redirect("/cl_home/")
