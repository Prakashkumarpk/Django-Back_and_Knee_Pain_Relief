from django.db import models

class registration(models.Model):

    name=models.CharField(max_length=50,null=True)
    email=models.EmailField(max_length=50,null=True)
    mobile_no=models.CharField(max_length=50,null=True)
    department=models.CharField(max_length=50,null=True)

    rh_id= models.CharField(max_length=100, null=True)
    password=models.CharField(max_length=50,null=True)
    
    accept=models.BooleanField(default=False,null=True)
    reject=models.BooleanField(default=False,null=True)

    cl_login=models.BooleanField(default=False,null=True)
    cl_logout=models.BooleanField(default=False,null=True)

    knee_pain =models.BooleanField(default=False,null=True)
    back_pain =models.BooleanField(default=False,null=True)

    

class pain_relief(models.Model):
    # project_id=models.IntegerField(max_length=50, null=True)

    type_of_pain=models.CharField(max_length=50,null=True)

    cl_rh_id= models.CharField(max_length=100, null=True)
    client_login=models.BooleanField(default=False,null=True)
    client_logout=models.BooleanField(default=False,null=True)

    status = models.CharField(max_length=50,null=True,default="Pending")

    pm_bp_scan=models.BooleanField(default=False, null=True)
    rt_bp_scan=models.BooleanField(default=False, null=True)
    ef_bp_scan=models.BooleanField(default=False, null=True)

    pm_kp_scan=models.BooleanField(default=False, null=True)
    rt_kp_scan=models.BooleanField(default=False, null=True)
    ef_kp_scan=models.BooleanField(default=False, null=True)

    r_back_pain=models.BooleanField(default=False,null=True)
    r_knee_pain=models.BooleanField(default=False,null=True)


#back_pain symptoms

    dull_aching_pain=models.IntegerField(null=True)
    sharp_stabbing_pain=models.IntegerField(null=True)
    muscle_spasms=models.IntegerField(null=True)
    radiating_pain=models.IntegerField(null=True)
    numbness_or_tingling=models.IntegerField(null=True)
    weakness=models.IntegerField(null=True)
    b_stiffness=models.IntegerField(null=True)
    pain_with_movement=models.IntegerField(null=True)
    pain_that_worsens_at_night=models.IntegerField( null=True)
    fatigue=models.IntegerField(null=True)
    loss_of_range_of_motion=models.IntegerField(null=True)
    fever_or_chills=models.IntegerField(null=True)

#knee_pain sympotms

    pain=models.IntegerField(null=True)
    swelling=models.IntegerField(null=True)
    stiffness=models.IntegerField(null=True)
    warmth_and_redness=models.IntegerField(null=True)
    weakness_or_instability=models.IntegerField(null=True)
    popping_or_grinding_sensation=models.IntegerField(null=True)
    limites_range_of_motion=models.IntegerField(null=True)
    pain_with_certain_movements=models.IntegerField(null=True)
    tenderness=models.IntegerField(null=True)
    bearing_weight=models.IntegerField(null=True)


    severity=models.IntegerField(null=True)
    type_of_backpain=models.CharField(max_length=50,null=True)
    type_of_kneepain=models.CharField(max_length=50,null=True)


    therapy=models.CharField(max_length=50,null=True)
    duration=models.CharField(max_length=50,null=True)

    #After Therapy Symptoms

    r_pain_intensity_before_therapy=models.IntegerField(null=True)
    r_pain_intensity_after_therapy=models.IntegerField(null=True)
    r_overall_relief_preception=models.IntegerField(null=True)

    #Backpain
   
    r_fever_or_chills=models.IntegerField(null=True)
    r_muscle_spams=models.IntegerField(null=True)
    r_radiating_pain=models.IntegerField(null=True)
    r_numbness_or_tingling=models.IntegerField(null=True)
    r_b_stiffness=models.IntegerField(null=True)
    r_loss_of_range_of_motion=models.IntegerField(null=True)
    r_pain_with_movement=models.IntegerField(null=True)
    r_pain_that_worsens_at_night=models.IntegerField(null=True)
    r_fatigue=models.IntegerField(null=True)

    #Kneepain

    r_swelling=models.IntegerField(null=True)
    r_stiffness=models.IntegerField(null=True)
    r_warmth_and_redness=models.IntegerField(null=True)
    r_weakness_or_instability=models.IntegerField(null=True)
    r_popping_or_grinding_sensation=models.IntegerField(null=True)
    r_limited_range_of_motion=models.IntegerField(null=True)
    r_pain_with_certain_movements=models.IntegerField(null=True)
    r_tenderness=models.IntegerField(null=True)
    r_bearing_weight=models.IntegerField(null=True)

    #final result

    effectiveness=models.IntegerField(null=True)


    #Final Report

    bp_f_report=models.FileField(upload_to="bp_final_report/",null=True,blank=True)
    kp_f_report=models.FileField(upload_to="kp_final_report/",null=True,blank=True)

    bp_f_rep_view=models.BooleanField(default=False,null=True)
    kp_f_rep_view=models.BooleanField(default=False,null=True)


   
    
