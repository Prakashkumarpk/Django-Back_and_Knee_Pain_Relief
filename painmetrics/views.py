from django.shortcuts import render,redirect
from admins.models import *
from django.contrib import messages
from utils.dataset_paths import PM_BP_DATASET,PM_KP_DATASET

# Create your views here.

def pm_home(request):
    return render(request,"painmetrics/pm_home.html")


def pm_login_reg(request):
    return render(request,"painmetrics/pm_login_reg.html")

def pm_reg(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        mobile_no=request.POST['mobile_no']
        department=request.POST['department']
        registration(name=name,email=email,mobile_no=mobile_no,department=department).save()
        messages.info(request," Painmetrics Registration successful")
        return redirect('/pm_login_reg/')
    else:
        return render(request, "painmetrics/pm_login_reg.html")
    

def pm_validate_login(request):

    if request.method=='POST':        
        email = request.POST['email']
        password = request.POST['password']
        try:    
            data = registration.objects.get(email=email, password=password,department="PAINMETRICS")
            if data.accept:    
                messages.info(request, "Painmetrics Login Successful")
                return redirect("/pm_home/")
            else:    
                messages.info(request, "Wrong Credentials")
                return render(request, "painmetrics/pm_login_reg.html")
        except:   
            messages.info(request, "Wrong Credentials")
            return render(request, "painmetrics/pm_login_reg.html")
    return render(request, "painmetrics/pm_login_reg.html")


def pm_logout(request):
    messages.info(request,"Painmetrics Logout Successful")
    return redirect("/")

def pm_bp_req(request):
    obj=pain_relief.objects.all()
    return render(request,"painmetrics/pm_bp_req.html",{"obj":obj})

def pm_kp_req(request):
    obj=pain_relief.objects.all()
    return render(request,"painmetrics/pm_kp_req.html",{"obj":obj})


def pm_bp_analyze(request):
    obj=pain_relief.objects.all()
    return render(request,"painmetrics/pm_bp_analyze.html",{"obj":obj})

def pm_kp_analyze(request):
    obj=pain_relief.objects.all()
    return render(request,"painmetrics/pm_kp_analyze.html",{"obj":obj})


from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import pandas as pd
from django.shortcuts import redirect
from django.contrib import messages

def pm_bp_analyze_process(request, cl_rh_id):
    # Fetch data from the Django model
    con = pain_relief.objects.get(cl_rh_id=cl_rh_id, type_of_pain="back_pain")

    # Extract source data from the database
    dull_aching_pain = con.dull_aching_pain
    sharp_stabbing_pain = con.sharp_stabbing_pain
    muscle_spasms = con.muscle_spasms
    radiating_pain = con.radiating_pain
    numbness_or_tingling = con.numbness_or_tingling
    weakness = con.weakness
    b_stiffness = con.b_stiffness
    pain_with_movement = con.pain_with_movement
    pain_that_worsens_at_night = con.pain_that_worsens_at_night
    fatigue = con.fatigue
    loss_of_range_of_motion = con.loss_of_range_of_motion
    fever_or_chills = con.fever_or_chills

    # Load dataset
    data = pd.read_csv(PM_BP_DATASET)

    # Ensure the target 'type_of_back_pain' is categorical for the classifier
    data["type_of_back_pain"] = data["type_of_back_pain"].astype("category")

    # Define features and target
    # Drop only the non-feature columns and make sure to one-hot encode categorical data
    features = data.drop(columns=["severity", "type_of_back_pain"])
    X = pd.get_dummies(features, drop_first=True)  # Convert any categorical data in X to dummy variables
    y_severity = data["severity"].astype(float)  # Ensure severity is numeric
    y_type = data["type_of_back_pain"].cat.codes  # Convert to numerical codes for classification

    # Initialize Random Forest models
    rf_severity = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_type = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train models
    rf_severity.fit(X, y_severity)
    rf_type.fit(X, y_type)

    # Prepare input data for prediction (ensure the order of features matches X after one-hot encoding)
    input_data = [[
        dull_aching_pain, sharp_stabbing_pain, muscle_spasms,
        radiating_pain, numbness_or_tingling, weakness, b_stiffness,
        pain_with_movement, pain_that_worsens_at_night, fatigue,
        loss_of_range_of_motion, fever_or_chills
    ]]
    input_data_df = pd.DataFrame(input_data, columns=features.columns)
    input_data_encoded = pd.get_dummies(input_data_df, drop_first=True).reindex(columns=X.columns, fill_value=0)

    # Make predictions
    predicted_severity = rf_severity.predict(input_data_encoded)[0]
    predicted_type_encoded = rf_type.predict(input_data_encoded)[0]

    # Decode the predicted type back to the original category
    predicted_type = data["type_of_back_pain"].cat.categories[predicted_type_encoded]

    # Update the model with predictions and status
    con.severity = predicted_severity
    con.type_of_backpain = predicted_type
    con.pm_bp_scan = True
    con.status = "Painmetrics Done"
    con.save()

    # Inform the user and redirect
    messages.info(request, f"{cl_rh_id} :: BackPain Painmetrics Processed Successfully")
    return redirect("/pm_bp_analyze/")


from django.shortcuts import redirect
from django.contrib import messages
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def pm_kp_analyze_process(request, cl_rh_id):
    # Fetch data from the Django model
    con = pain_relief.objects.get(cl_rh_id=cl_rh_id, type_of_pain="knee_pain")

    # Source data (features)
    pain = con.pain
    swelling = con.swelling
    stiffness = con.stiffness
    warmth_and_redness = con.warmth_and_redness
    weakness_or_instability = con.weakness_or_instability
    popping_or_grinding_sensation = con.popping_or_grinding_sensation
    limites_range_of_motion = con.limites_range_of_motion
    pain_with_certain_movements = con.pain_with_certain_movements
    tenderness = con.tenderness
    bearing_weight = con.bearing_weight

    # Load dataset (same dataset you provided)
    data = pd.read_csv(PM_KP_DATASET)

    # Define features and target columns
    features = data.drop(columns=["severity", "type_of_knee_pain"])  # Ensure only features remain in X
    X = pd.get_dummies(features, drop_first=True)  # One-hot encode categorical features, if any

    # Encode target variables
    y_severity = data["severity"].astype("category").cat.codes  # Convert severity to numerical codes
    y_type = data["type_of_knee_pain"].astype("category").cat.codes  # Convert type_of_knee_pain to numerical codes

    # Initialize RandomForestClassifier for severity and type prediction
    rf_severity = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_type = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train models
    rf_severity.fit(X, y_severity)
    rf_type.fit(X, y_type)

    # Prepare input data (ensure the column order matches after one-hot encoding)
    input_data = [[
        pain, swelling, stiffness, warmth_and_redness,
        weakness_or_instability, popping_or_grinding_sensation,
        limites_range_of_motion, pain_with_certain_movements,
        tenderness, bearing_weight
    ]]
    input_data_df = pd.DataFrame(input_data, columns=features.columns)
    input_data_encoded = pd.get_dummies(input_data_df, drop_first=True).reindex(columns=X.columns, fill_value=0)

    # Make predictions
    predicted_severity_encoded = rf_severity.predict(input_data_encoded)[0]
    predicted_type_encoded = rf_type.predict(input_data_encoded)[0]

    # Decode predictions back to original categories
    predicted_severity = data["severity"].astype("category").cat.categories[predicted_severity_encoded]
    predicted_type = data["type_of_knee_pain"].astype("category").cat.categories[predicted_type_encoded]

    # Update the model with predictions and status
    con.severity = predicted_severity
    con.type_of_kneepain = predicted_type
    con.pm_kp_scan = True
    con.status = "Painmetrics Done"
    con.save()

    # Inform the user and redirect
    messages.info(request, f"{cl_rh_id} :: KneePain Painmetrics Processed Successfully")
    return redirect("/pm_kp_analyze/")


def pm_bp_report(request):
    obj=pain_relief.objects.all()
    return render(request,"painmetrics/pm_bp_report.html",{"obj":obj})

def pm_kp_report(request):
    obj=pain_relief.objects.all()
    return render(request,"painmetrics/pm_kp_report.html",{"obj":obj})






