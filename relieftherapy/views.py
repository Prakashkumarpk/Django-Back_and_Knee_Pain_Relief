from django.shortcuts import render,redirect
from django.contrib import messages
from admins.models import *
from django.core.mail import send_mail
from utils.dataset_paths import RT_BP_DATASET,RT_KP_DATASET

# Create your views here.

def rt_home(request):
    return render(request,"relieftherapy/rt_home.html")

def rt_login_reg(request):
    return render(request,'relieftherapy/rt_login_reg.html')

def rt_reg(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        mobile_no=request.POST['mobile_no']
        department=request.POST['department']
        registration(name=name,email=email,mobile_no=mobile_no,department=department).save()
        messages.info(request," Relieftherapy Registration successful")
        return redirect('/rt_login_reg/')
    else:
        return render(request,'relieftherapy/rt_login_reg.html')
    

def rt_validate_login(request):
    if request.method=='POST':
        
        email = request.POST['email']
        password = request.POST['password']
        try:
            
            data = registration.objects.get(email=email, password=password, department="RELIEFTHERAPY")
            if data.accept:
                
                messages.info(request, "Relieftherapy Login Successful")
                return redirect("/rt_home/")
            else:
                
                messages.info(request, "Wrong Credentials")
                return render(request,'relieftherapy/rt_login_reg.html')
        except:
            
            messages.info(request, "Wrong Credentials")
            return render(request,'relieftherapy/rt_login_reg.html')
    return render(request,'relieftherapy/rt_login_reg.html')


def rt_logout(request):
    messages.info(request,"Relieftherapy Logout Successful")
    return redirect("/")


def rt_bp_req(request):
    obj=pain_relief.objects.all()
    return render(request,"relieftherapy/rt_bp_req.html",{"obj":obj})

def rt_kp_req(request):
    obj=pain_relief.objects.all()
    return render(request,"relieftherapy/rt_kp_req.html",{"obj":obj})

def rt_bp_analyze(request):
    obj=pain_relief.objects.all()
    return render(request,"relieftherapy/rt_bp_analyze.html",{"obj":obj})

def rt_kp_analyze(request):
    obj=pain_relief.objects.all()
    return render(request,"relieftherapy/rt_kp_analyze.html",{"obj":obj})


from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail

def rt_bp_analyze_process(request, cl_rh_id):
    con = pain_relief.objects.get(cl_rh_id=cl_rh_id, type_of_pain="back_pain")
    id = con.cl_rh_id
    obj = registration.objects.get(rh_id=id)

    # Source data from the pain_relief model
    source_data = [
        con.dull_aching_pain,
        con.sharp_stabbing_pain,
        con.muscle_spasms,
        con.radiating_pain,
        con.numbness_or_tingling,
        con.weakness,
        con.b_stiffness,
        con.pain_with_movement,
        con.pain_that_worsens_at_night,
        con.fatigue,
        con.loss_of_range_of_motion,
        con.fever_or_chills,
        con.severity,
        con.type_of_backpain
    ]

    dataset_path = RT_BP_DATASET

    # Load dataset with error handling
    try:
        data = pd.read_csv(dataset_path, on_bad_lines='skip')
    except Exception as e:
        messages.error(request, f"Error reading the dataset: {e}")
        return redirect("/rt_bp_analyze/")

    # Encode all categorical columns
    le_dict = {}  # Store LabelEncoders for inverse transformations
    for column in data.columns:
        if data[column].dtype == 'object':  # Check if column is categorical
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
            le_dict[column] = le  # Save encoder for later use

    # Features (X) and target labels (y)
    X = data.drop(['therapy', 'duration'], axis=1)
    y_therapy = data['therapy']
    y_duration = data['duration']

    # Train classifiers
    rf_therapy = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_therapy.fit(X, y_therapy)

    rf_duration = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_duration.fit(X, y_duration)

    # Encode source data
    source_data_encoded = []
    for i, val in enumerate(source_data):
        col_name = X.columns[i]
        if col_name in le_dict:
            # Transform each source data value using the corresponding LabelEncoder
            source_data_encoded.append(le_dict[col_name].transform([val])[0])
        else:
            # If there's no encoding for a column, append the value directly
            source_data_encoded.append(val)

    # Predict therapy and duration
    predicted_therapy = le_dict['therapy'].inverse_transform(rf_therapy.predict([source_data_encoded]))[0]
    predicted_duration = le_dict['duration'].inverse_transform(rf_duration.predict([source_data_encoded]))[0]

    # Update pain_relief object
    con.therapy = predicted_therapy
    con.duration = predicted_duration
    con.rt_bp_scan = True
    con.status = "ReliefTherapy Done"
    con.save()

    # Send Mail
    subject = 'Personalized Therapy Suggestion for Your Back Pain Relief'
    plain_message = f"""Dear {obj.name},\nWe have reviewed your recent assessment and have tailored a therapy plan 
specifically to address your Back pain concerns. Based on your reported symptoms, we recommend the following therapy:\n
Therapy Suggested: {con.therapy} \nDuration: {con.duration}\n
Please follow the suggested regimen and let us know if you have any questions. Our team is here to support you throughout this journey.\n
After Completing the Suggested Therapy kindly Login and update your results in the Portal \n
Warm regards,\n Admin Team"""

    send_mail(subject, plain_message, 'prakashkumar03.surya@gmail.com', [obj.email], fail_silently=False)

    # Success message
    messages.info(request, f"{con.cl_rh_id} :: Backpain ReliefTherapy Processed Successfully")
    messages.info(request, f"{con.cl_rh_id} :: BackPain Therapy sent to the registered Mail ID")
    return redirect("/rt_bp_analyze/")


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from django.shortcuts import redirect
from django.contrib import messages
from admins.models import pain_relief

def rt_kp_analyze_process(request, cl_rh_id):
    # Fetch knee pain data for the specific client
    con = pain_relief.objects.get(cl_rh_id=cl_rh_id, type_of_pain="knee_pain")
    id=con.cl_rh_id
    obj =registration.objects.get(rh_id=id)

    # Attributes as input features
    source_data = {
        'pain': con.pain,
        'swelling': con.swelling,
        'stiffness': con.stiffness,
        'warmth_and_redness': con.warmth_and_redness,
        'weakness_or_instability': con.weakness_or_instability,
        'popping_or_grinding_sensation': con.popping_or_grinding_sensation,
        'limites_range_of_motion': con.limites_range_of_motion,
        'pain_with_certain_movements': con.pain_with_certain_movements,
        'tenderness': con.tenderness,
        'bearing_weight': con.bearing_weight,
        'severity': con.severity,
        'type_of_knee_pain': con.type_of_kneepain
    }

    # Load dataset and preprocess
    
    df = pd.read_csv(RT_KP_DATASET)

    # Encode target variables (therapy and duration)
    label_encoder_therapy = LabelEncoder()
    label_encoder_duration = LabelEncoder()
    df['therapy'] = label_encoder_therapy.fit_transform(df['therapy'])
    df['duration'] = label_encoder_duration.fit_transform(df['duration'])

    # Encode all non-numeric (categorical) features in the dataset
    label_encoders = {}
    for column in df.columns:
        if df[column].dtype == 'object':
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le

    # Split data into features (X) and target variables (y)
    X = df.drop(columns=['therapy', 'duration'])
    y_therapy = df['therapy']
    y_duration = df['duration']

    # Split data into training and testing sets
    X_train, X_test, y_train_therapy, y_test_therapy = train_test_split(X, y_therapy, test_size=0.2, random_state=42)
    _, _, y_train_duration, y_test_duration = train_test_split(X, y_duration, test_size=0.2, random_state=42)

    # Train RandomForestClassifier for therapy
    clf_therapy = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_therapy.fit(X_train, y_train_therapy)

    # Train RandomForestClassifier for duration
    clf_duration = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_duration.fit(X_train, y_train_duration)

    # Prepare client data for prediction, encode categorical features in source_data
    client_data = pd.DataFrame([source_data])
    for column in client_data.columns:
        if column in label_encoders:
            client_data[column] = label_encoders[column].transform(client_data[column])

    # Predict therapy and duration
    therapy_pred = clf_therapy.predict(client_data)
    duration_pred = clf_duration.predict(client_data)

    # Decode predicted values back to original labels
    therapy_result = label_encoder_therapy.inverse_transform(therapy_pred)[0]
    duration_result = label_encoder_duration.inverse_transform(duration_pred)[0]

    # Update the database with the results
    con.therapy = therapy_result
    con.duration = duration_result
    con.rt_kp_scan = True
    con.status = "ReliefTherapy Done"
    con.save()

    #Send Mail
    subject = 'Personalized Therapy Suggestion for Your Knee Pain Relief'
    plain_message = f"""Dear {obj.name},\nWe have reviewed your recent assessment and have tailored a therapy plan 
specifically to address your knee pain concerns. Based on your reported symptoms, we recommend the following therapy\n
Therapy Suggested: {con.therapy} \nDuration: {con.duration}\n
Please follow the suggested regimen and let us know if you have any questions. Our team is here to support you throughout this journey.\n
After Completing the Suggested Therapy kindly Login and update your results in the Portal \n
Warm regards,\n Admin Team"""

    send_mail(subject, plain_message, 'prakashkumar03.surya@gmail.com', [obj.email], fail_silently=False)
    

    # Message and redirect
    messages.info(request, f"{con.cl_rh_id} :: Kneepain ReliefTherapy Processed Successfully with Therapy")
    messages.info(request, f"{con.cl_rh_id} :: KneePain Therapy sent to the registered Mail ID")  
    return redirect("/rt_kp_analyze/")

def rt_bp_report(request):
    obj=pain_relief.objects.all()
    return render(request,"relieftherapy/rt_bp_report.html",{"obj":obj})

def rt_kp_report(request):
    obj=pain_relief.objects.all()
    return render(request,"relieftherapy/rt_kp_report.html",{"obj":obj})









