from django.shortcuts import render,redirect
from admins.models import *
from django.contrib import messages
from utils.dataset_paths import EF_BP_DATASET,EF_KP_DATASET

# Create your views here.

def ef_home(request):
    return render(request,"effectiveness/ef_home.html")

def ef_login_reg(request):
    return render(request,'effectiveness/ef_login_reg.html')

def ef_reg(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        mobile_no=request.POST['mobile_no']
        department=request.POST['department']
        registration(name=name,email=email,mobile_no=mobile_no,department=department).save()
        messages.info(request," Effectiveness Registration successful")
        return redirect('/ef_login_reg/')
    else:
        return render(request,'effectiveness/ef_login_reg.html')

def ef_validate_login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            data = registration.objects.get(email=email, password=password, department="EFFECTIVENESS")
            if data.accept:
                messages.info(request, "Effectiveness Login Successful")
                return redirect("/ef_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request,'effectiveness/ef_login_reg.html')
        except:
            messages.info(request, "Wrong Credentials")
            return render(request,'effevtiveness/ef_login_reg.html')
    return render(request,'effectiveness/ef_login_reg.html')


def ef_logout(request):
    messages.info(request,"Effectiveness Logout Successful")
    return redirect("/")

def ef_bp_req(request):
    obj=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,"effectiveness/ef_bp_req.html",{"obj":obj})

def ef_kp_req(request):
    obj=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,"effectiveness/ef_kp_req.html",{"obj":obj})

def ef_bp_analyze(request):
    obj=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,"effectiveness/ef_bp_analyze.html",{"obj":obj})

def ef_kp_analyze(request):
    obj=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,"effectiveness/ef_kp_analyze.html",{"obj":obj})

from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect
from admins.models import pain_relief  # Assuming the model is named `pain_relief`

def ef_bp_analyze_process(request, cl_rh_id):
    # Fetch the object from the database based on the client id and pain type
    con = pain_relief.objects.get(type_of_pain="back_pain", cl_rh_id=cl_rh_id)

    # Path to your dataset
    dataset_path = EF_BP_DATASET

    # Load the dataset
    df = pd.read_csv(dataset_path)

    # Features to use for training the model
    features = [
        'dull_aching_pain', 'sharp_stabbing_pain', 'muscle_spasms', 'radiating_pain',
        'numbness_or_tingling', 'weakness', 'b_stiffness', 'pain_with_movement',
        'pain_that_worsens_at_night', 'fatigue', 'loss_of_range_of_motion', 'fever_or_chills',
        'severity', 'type_of_back_pain', 'therapy', 'duration',
        'r_pain_intensity_before_therapy', 'r_pain_intensity_after_therapy', 'r_fever_or_chills',
        'r_muscle_spams', 'r_radiating_pain', 'r_numbness_or_tingling', 'r_b_stiffness',
        'r_loss_of_range_of_motion', 'r_pain_with_movement', 'r_pain_that_worsens_at_night',
        'r_fatigue', 'r_overall_relief_preception'
    ]

    # Target column
    target = 'effectiveness'

    # Drop rows with missing target values
    df = df.dropna(subset=[target])

    # Handle missing values in features (optional: customize to specific columns)
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Handle categorical columns: Encode 'type_of_back_pain', 'therapy', and 'duration'
    type_encoder = LabelEncoder()
    therapy_encoder = LabelEncoder()
    duration_encoder = LabelEncoder()

    df['type_of_back_pain'] = type_encoder.fit_transform(df['type_of_back_pain'])
    df['therapy'] = therapy_encoder.fit_transform(df['therapy'])
    df['duration'] = duration_encoder.fit_transform(df['duration'])

    # Extract features and target from the dataset
    X = df[features]
    y = df[target]

    # Preprocessing: Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Initialize Gaussian Naive Bayes model
    model = GaussianNB()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate the model's performance
    mse = mean_squared_error(y_test, y_pred)
    # messages.info(request, f"Model trained with MSE: {mse}")

    # Encode the current record's 'type_of_back_pain', 'therapy', and 'duration'
    current_type_encoded = type_encoder.transform([con.type_of_backpain])[0]
    current_therapy_encoded = therapy_encoder.transform([con.therapy])[0]
    current_duration_encoded = duration_encoder.transform([con.duration])[0]

    # Predict effectiveness for the current record
    X_current = scaler.transform([[ 
        con.dull_aching_pain, con.sharp_stabbing_pain, con.muscle_spasms, con.radiating_pain,
        con.numbness_or_tingling, con.weakness, con.b_stiffness, con.pain_with_movement,
        con.pain_that_worsens_at_night, con.fatigue, con.loss_of_range_of_motion, con.fever_or_chills,
        con.severity, current_type_encoded, current_therapy_encoded, current_duration_encoded,
        con.r_pain_intensity_before_therapy, con.r_pain_intensity_after_therapy, con.r_fever_or_chills,
        con.r_muscle_spams, con.r_radiating_pain, con.r_numbness_or_tingling, con.r_b_stiffness,
        con.r_loss_of_range_of_motion, con.r_pain_with_movement, con.r_pain_that_worsens_at_night,
        con.r_fatigue, con.r_overall_relief_preception
    ]])

    # Calculate the effectiveness prediction
    predicted_effectiveness = model.predict(X_current)[0]

    # Save the effectiveness prediction in the database
    con.effectiveness = predicted_effectiveness
    con.ef_bp_scan = True
    con.status = "Effectiveness Calculated"
    con.save()

    # Redirect after processing
    messages.info(request, f"{cl_rh_id} :: Effectiveness Calculated Successfully") 
    return redirect("/ef_bp_analyze/")



# def ef_kp_analyze_process(request, cl_rh_id):
#     # Fetch the object from the database based on the client id and pain type
#     con = pain_relief.objects.get(type_of_pain="knee_pain", cl_rh_id=cl_rh_id)

#     # source

#     # before therapy 

#     pain=con.pain, 
#     swelling=con.swelling, 
#     stiffness=con.stiffness, 
#     warmth_and_redness=con.warmth_and_redness, 
#     weakness_or_instability=con.weakness_or_instability, 
#     popping_or_grinding_sensation=con.popping_or_grinding_sensation, 
#     limites_range_of_motion=con.limites_range_of_motion, 
#     pain_with_certain_movements=con.pain_with_certain_movements, 
#     tenderness=con.tenderness,
#     bearing_weight=con.bearing_weight, 
#     severity=con.severity, 
#     type_of_kneepain=con.type_of_backpain, 
#     therapy=con.therapy,
#     duration=con.duration, 
    
    
#     # after therapy 

#     r_swelling=con.r_swelling, 
#     r_stiffness=con.r_stiffness, 
#     r_warmth_and_redness=con.r_warmth_and_redness,
#     r_weakness_or_instability=con.r_weakness_or_instability, 
#     r_popping_or_grinding_sensation=con.r_popping_or_grinding_sensation,
#     r_limited_range_of_motion=con.r_limited_range_of_motion, 
#     r_pain_with_certain_movements=con.r_pain_with_certain_movements, 
#     r_tenderness=con.r_tenderness,
#     r_bearing_weight=con.r_bearing_weight, 
#     r_pain_intensity_before_therapy=con.r_pain_intensity_before_therapy, 
#     r_pain_intensity_after_therapy=con.r_pain_intensity_after_therapy, 
#     r_overall_relief_preception=con.r_overall_relief_preception,

#     #my dataset 
#     dataset="D:\PROJECT\02_KNEE_AND_BACK_REVIVAL\project\dataset\ef_bp.csv" 

#     #target 

#     effectiveness=con.effectiveness 
#     con.ef_kp_scan=True 
#     con.status="Effectiveness Done" 
#     con.save() 

#     messages.info(request, f"{cl_rh_id} :: Effectiveness Calculated Successfully") 
#     return redirect("/ef_kp_analyze/")


import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer  # To handle missing values
from django.contrib import messages
from django.shortcuts import redirect

def ef_kp_analyze_process(request, cl_rh_id):
    con = pain_relief.objects.get(type_of_pain="knee_pain", cl_rh_id=cl_rh_id)

    # Load your dataset
    dataset_path = EF_KP_DATASET
    df = pd.read_csv(dataset_path)

    # Debugging step: Print column names to check if 'therapy', 'duration', and 'type_of_knee_pain' are present
    print("Columns in dataset before one-hot encoding:", df.columns)

    # If 'therapy' and 'duration' columns exist, process them; else skip
    if 'therapy' in df.columns and 'duration' in df.columns:
        df = pd.get_dummies(df, columns=['therapy', 'duration'], drop_first=True)
    else:
        messages.error(request, "'therapy' or 'duration' columns are missing from the dataset.")
        return redirect("/ef_kp_analyze/")

    # Also one-hot encode the 'type_of_knee_pain' column if it exists
    if 'type_of_knee_pain' in df.columns:
        df = pd.get_dummies(df, columns=['type_of_knee_pain'], drop_first=True)

    # Debugging step: Print column names after one-hot encoding
    print("Columns in dataset after one-hot encoding:", df.columns)

    # Select the features (X) and target (y) from your dataset
    features = [
        'pain', 'swelling', 'stiffness', 'warmth_and_redness', 'weakness_or_instability',
        'popping_or_grinding_sensation', 'limites_range_of_motion', 'pain_with_certain_movements',
        'tenderness', 'bearing_weight', 'severity', 'r_swelling', 'r_stiffness', 'r_warmth_and_redness',
        'r_weakness_or_instability', 'r_popping_or_grinding_sensation', 'r_limited_range_of_motion',
        'r_pain_with_certain_movements', 'r_tenderness', 'r_bearing_weight'
    ]
    target = 'effectiveness'

    # Separate features and target variable
    X = df[features]
    y = df[target]

    # Handle missing values: Impute missing values with the median
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    # Scale the features for better model performance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Initialize the Gaussian Naive Bayes model
    model = GaussianNB()

    # Train the model
    model.fit(X_train, y_train)

    # Predict effectiveness
    y_pred = model.predict(X_test)

    # Calculate Mean Squared Error to evaluate model performance
    mse = mean_squared_error(y_test, y_pred)
    # messages.info(request, f"Gaussian Naive Bayes Regression Model Training Complete - MSE: {mse}")

    # Now, use the trained model to predict effectiveness for the given patient data (con)
    # Prepare the patient's data in the same format as the dataset
    patient_data = np.array([
        con.pain, con.swelling, con.stiffness, con.warmth_and_redness, con.weakness_or_instability,
        con.popping_or_grinding_sensation, con.limites_range_of_motion, con.pain_with_certain_movements,
        con.tenderness, con.bearing_weight, con.severity, con.r_swelling, con.r_stiffness,
        con.r_warmth_and_redness, con.r_weakness_or_instability, con.r_popping_or_grinding_sensation,
        con.r_limited_range_of_motion, con.r_pain_with_certain_movements, con.r_tenderness, con.r_bearing_weight
    ])

    # Ensure the patient's data is in the same format as the training data
    patient_data_df = pd.DataFrame([patient_data], columns=features)

    # Check if 'type_of_kneepain' exists and process it
    if 'type_of_kneepain' in patient_data_df.columns:
        patient_data_df = pd.get_dummies(patient_data_df, columns=['type_of_kneepain'], drop_first=True)
    else:
        # If it doesn't exist, add a default column to ensure the correct number of features
        print("'type_of_kneepain' column not found in the patient's data. Ensure it is correctly set.")

    # Ensure the patient data has the same number of features as the model expects
    patient_data_imputed = imputer.transform(patient_data_df)  # Impute missing values if any
    patient_data_scaled = scaler.transform(patient_data_imputed)

    # Predict effectiveness for the patient's data
    predicted_effectiveness = model.predict(patient_data_scaled)

    # Save the predicted effectiveness to the database
    con.effectiveness = predicted_effectiveness[0]
    con.ef_kp_scan = True
    con.status = "Effectiveness Calculated"
    con.save()

    messages.info(request, f"{cl_rh_id} :: Effectiveness Calculated Successfully")
    return redirect("/ef_kp_analyze/")

def ef_bp_report(request):
    obj=pain_relief.objects.filter(type_of_pain="back_pain")
    return render(request,"effectiveness/ef_bp_report.html",{"obj":obj})

def ef_kp_report(request):
    obj=pain_relief.objects.filter(type_of_pain="knee_pain")
    return render(request,"effectiveness/ef_kp_report.html",{"obj":obj})






















