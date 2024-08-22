# institutions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    #region endpoints
    path('regions/all/', views.RegionListView.as_view(), name='region-list'),
    path('regions/', views.RegionCreateView.as_view(), name='region-create'),
    path('regions/<int:pk>/', views.RegionRetrieveView.as_view(), name='region-retrieve'),
    path('regions/<int:pk>/update/', views.RegionUpdateView.as_view(), name='region-update'),
    path('regions/<int:pk>/delete/', views.RegionDeleteView.as_view(), name='region-delete'),

    
    path('districts/', views.DistrictListCreate.as_view(), name='district-list-create'),
    path('districts/<int:pk>/', views.DistrictRetrieve.as_view(), name='district-retrieve'),
    path('districts/all/', views.DistrictList.as_view(), name='district-list'),
    path('districts/<int:pk>/update/', views.DistrictUpdate.as_view(), name='district-update'),
    path('districts/<int:pk>/delete/', views.DistrictDestroy.as_view(), name='district-delete'),
    path('institutions/', views.InstitutionListCreate.as_view(), name='institution-list-create'),
    path('institution-list/', views.InstitutionListView.as_view(), name='institution-list'),
    path('institutions/<int:pk>/', views.InstitutionRetrieve.as_view(), name='institution-retrieve'),
    path('institutions/<int:pk>/update/', views.InstitutionUpdate.as_view(), name='institution-update'),
    path('institutions/<int:pk>/delete/', views.InstitutionDestroy.as_view(), name='institution-destroy'),  
    path('institution-users/', views.UserInstitutionList.as_view(), name='institution-user-list'),
    path('institution-users/create/', views.InstitutionUserCreate.as_view(), name='institution-user-create'),
    path('institution-users/<int:pk>/', views.InstitutionUserRetrieve.as_view(), name='institution-user-retrieve'),
    path('institution-users/<int:pk>/update/', views.InstitutionUserUpdate.as_view(), name='institution-user-update'),
    path('institution-users/<int:pk>/delete/', views.InstitutionUserDestroy.as_view(), name='institution-user-destroy'),

    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentRetrieveView.as_view(), name='department-retrieve'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),
    
    # UserDepartment endpoints
    path('user-departments/', views.UserDepartmentListView.as_view(), name='user-department-list'),          # Read All UserDepartments
    path('user-departments/create/', views.UserDepartmentCreateView.as_view(), name='user-department-create'), # Create UserDepartment
    path('user-departments/<int:pk>/', views.UserDepartmentDetailView.as_view(), name='user-department-detail'), # Read One UserDepartment
    path('user-departments/update/<int:pk>/', views.UserDepartmentUpdateView.as_view(), name='user-department-update'), # Update UserDepartment
    path('user-departments/delete/<int:pk>/', views.UserDepartmentDeleteView.as_view(), name='user-department-delete'), # Delete UserDepartment

    # InstitutionDepartment endpoints
    path('institution-departments/', views.InstitutionDepartmentListView.as_view(), name='institution-department-list'),
    path('institution-departments/<int:pk>/', views.InstitutionDepartmentDetailView.as_view(), name='institution-department-detail'),
    path('institution-departments/create/', views.InstitutionDepartmentCreateView.as_view(), name='institution-department-create'),
    
     # Mandate endpoints
    path('mandates/', views.MandateListCreateView.as_view(), name='mandate-list-create'),
    path('mandates/<int:pk>/', views.MandateRetrieveView.as_view(), name='mandate-retrieve'),
    path('mandates/all/', views.MandateListView.as_view(), name='mandate-list-all'),
    path('mandates/deleted/', views.DeletedMandateListView.as_view(), name='deleted-mandate-list'),
    path('mandates/<int:pk>/update/', views.MandateUpdateView.as_view(), name='mandate-update'),
    path('mandates/<int:pk>/delete/', views.MandateDeleteView.as_view(), name='mandate-delete'),
    path('mandates/institution/<int:institution_id>/', views.get_mandate_by_institution, name='get_mandate_by_institution'),

    
    #Mission endpoints
    path('missions/', views.MissionListCreateView.as_view(), name='mission-list-create'),
    path('missions/<int:pk>/', views.MissionRetrieveView.as_view(), name='mission-retrieve'),
    path('missions/all/', views.MissionListView.as_view(), name='mission-list'),
    path('missions/deleted/', views.DeletedMissionListView.as_view(), name='deleted-mission-list'),
    path('missions/<int:pk>/update/', views.MissionUpdateView.as_view(), name='mission-update'),
    path('missions/<int:pk>/delete/', views.MissionDeleteView.as_view(), name='mission-delete'),
    path('missions/institution/<int:institution_id>/', views.get_mission_by_institution, name='get_mission_by_institution'),

    
    #Vision endpoints
    path('visions/', views.VisionListCreateView.as_view(), name='vision-list-create'),
    path('visions/<int:pk>/', views.VisionRetrieveView.as_view(), name='vision-retrieve'),
    path('visions/all/', views.VisionListView.as_view(), name='vision-list'),
    path('visions/deleted/', views.DeletedVisionListView.as_view(), name='deleted-vision-list'),
    path('visions/<int:pk>/update/', views.VisionUpdateView.as_view(), name='vision-update'),
    path('visions/<int:pk>/delete/', views.VisionDeleteView.as_view(), name='vision-delete'),
    path('visions/institution/<int:institution_id>/', views.get_vision_by_institution, name='get_vision_by_institution'),

    
    
    # Strategic Objective endpoints
    path('strategic-objectives/', views.create_institution_strategic_objectives),
    path('strategic-objectives/all/', views.get_all_strategic_objectives, name='get_all_strategic_objectives'),
    path('strategic-objectives/institution/<int:institution_id>/', views.get_strategic_objectives_by_institution, name='get_strategic_objectives_by_institution'),
    path('strategic-objectives/create/', views.create_institution_strategic_objectives, name='create_institution_strategic_objectives'),
    path('strategic-objectives/current/', views.get_current_strategic_objectives, name='get_current_strategic_objectives'),
    path('strategic-objectives/current/institution/<int:institution_id>/', views.get_current_strategic_objectives_by_institution, name='get_current_strategic_objectives_by_institution'),
    
    #Thematic Area endpoints
    path('thematic-areas/', views.ThematicAreaListCreate.as_view(), name='thematic-area-list-create'),
    path('thematic-areas/all/', views.ThematicAreaListView.as_view(), name='thematic-area-list'),
    path('thematic-areas/<int:pk>/', views.ThematicAreaRetrieve.as_view(), name='thematic-area-retrieve'),
    path('thematic-areas/<int:pk>/update/', views.ThematicAreaUpdate.as_view(), name='thematic-area-update'),
    path('thematic-areas/<int:pk>/delete/', views.ThematicAreaDestroy.as_view(), name='thematic-area-destroy'),
    
    #Reform Area endpoints
    path('reform-areas/', views.ReformAreaListCreate.as_view(), name='reformarea-list-create'),
    path('reform-areas/list/', views.ReformAreaListView.as_view(), name='reformarea-list-view'),
    path('reform_area/<int:reform_area_id>/', views.get_reform_area_by_id, name='get_reform_area_by_id'),
    path('reform-areas/institution/<int:institution_id>/', views.get_reform_areas_by_latest_year_and_institution, name='get_reform_areas_by_institution'),
    path('reform-areas/<int:pk>/update/', views.ReformAreaUpdate.as_view(), name='reformarea-update'),
    path('reform-areas/<int:pk>/delete/', views.ReformAreaDestroy.as_view(), name='reformarea-destroy'),
    path('reform-area-acr/create/', views.ReformAreaACRCreateView.as_view(), name='reform-area-acr-create'),
    path('reform_area_acr/output_reporting_period/<int:output_reporting_period_id>/', views.ReformAreaACRByOutputReportingPeriod.as_view(), name='reform-area-acr-by-output-reporting-period'),
    path('reform-area-acr/output-reporting-period/<int:output_reporting_period_id>/reform-area/<int:reform_area_id>/',views.ReformAreaACRByOutputReportingPeriodAndReformArea.as_view(), name='reform_area_acr_by_reporting_period_and_reform_area'),
    path('reform-area-acr/output-reporting-period/reform-area/<int:reform_area_id>/', views.ReformAreaACRByReformArea.as_view(), name='reform_area_acr_by_reporting_period_and_reform_area'),
    path('thematic-area-acr/', views.ThematicAreaACRCreateView.as_view(), name='thematic_area_acr_create'),
    path('thematic-area-acr/<int:thematic_area_id>/', views.ThematicAreaACRListView.as_view(), name='thematic_area_acr_list'),

    #Problem endpoints
    path('problems/', views.create_problems, name='create_problems'),
    path('problems/all/', views.get_all_problems, name='get_all_problems'),
    path('problems/reform-area/<int:reform_area_id>/', views.get_problems_by_reform_area, name='get_problems_by_reform_area'),
    path('problems/<int:problem_id>/', views.get_problem_by_id, name='get_problem_by_id'),
    path('problems/<int:problem_id>/update/', views.update_problem, name='update_problem'),
    path('problems/<int:problem_id>/delete/', views.delete_problem, name='delete_problem'),
    
    # Justification endpoints
    path('justifications/', views.create_justifications, name='create_justifications'),
    path('justifications/all/', views.get_all_justifications, name='get_all_justifications'),
    path('justifications/reform-area/<int:reform_area_id>/', views.get_justifications_by_reform_area, name='get_justifications_by_reform_area'),
    path('justifications/<int:justification_id>/', views.get_justification_by_id, name='get_justification_by_id'),
    path('justifications/<int:justification_id>/update/', views.update_justification, name='update_justification'),
    path('justifications/<int:justification_id>/delete/', views.delete_justification, name='delete_justification'),
    
    # Outcome endpoints
    path('outcomes/', views.create_outcomes, name='create_outcomes'),
    path('outcomes/all/', views.get_all_outcomes, name='list_outcomes'),
    path('outcomes/<int:outcome_id>/', views.get_outcomes_by_id, name='get_outcomes_by_id'),
    path('outcomes/update/<int:outcome_id>/', views.update_outcome, name='update_outcome'),
    path('outcomes/delete/<int:outcome_id>/', views.delete_outcome, name='delete_outcome'),
    path('outcomes/deleted/', views.get_deleted_outcomes, name='get_deleted_outcomes'),
    path('outcomes/reform_area/<int:reform_area_id>/', views.get_outcomes_by_reform_area, name='get_outcomes_by_reform_area'),

    # Outcome Indicator endpoints
    path('outcome-indicators/', views.create_outcome_indicators, name='create_outcome_indicators'),
    path('outcome-indicators/all/', views.get_all_outcome_indicators, name='list_outcome_indicators'),
    path('outcome-indicators/<int:indicator_id>/', views.get_outcome_indicator_by_id, name='get_outcome_indicator_by_id'),
    path('outcome-indicators/update/<int:indicator_id>/', views.update_outcome_indicator, name='update_outcome_indicator'),
    path('outcome-indicators/delete/<int:indicator_id>/', views.delete_outcome_indicator, name='delete_outcome_indicator'),
    path('outcome-indicators/deleted/', views.get_deleted_outcome_indicators, name='get_deleted_outcome_indicators'),

    # Output endpoints
    path('outputs/', views.create_outputs, name='create_outputs'),
    path('outputs/all/', views.get_all_outputs, name='list_outputs'),
    path('outputs/<int:output_id>/', views.get_output_by_id, name='get_output_by_id'),
    path('outputs/update/<int:output_id>/', views.update_output, name='update_output'),
    path('outputs/delete/<int:output_id>/', views.delete_output, name='delete_output'),
    path('outputs/deleted/', views.get_deleted_outputs, name='get_deleted_outputs'),
    path('outputs/outcome/<int:outcome_id>/', views.get_outputs_by_outcome_id, name='get_outputs_by_outcome_id'),
    path('outputs/reform_area/<int:reform_area_id>/', views.get_outputs_by_reform_area_id, name='get_outputs_with targets_by_reform_area_id'),
    path('notargeted/outputs/reform_area/<int:reform_area_id>/', views.get_no_targeted_outputs_by_reform_area_id, name='get_outputs_without_by_reform_area_id'),

    path('output-acr/', views.OutputACRCreateView.as_view(), name='output-acr-create'),
    path('output-acrs/all', views.OutputACRListView.as_view(), name='output-acr-list'),
    path('output-acr/<int:pk>/', views.OutputACRDetailView.as_view(), name='output-acr-detail'),
    path('output-acr/by-output/<int:output_id>/', views.OutputACRByOutputIDView.as_view(), name='output-acr-by-output-id'),


    path('annual-output-acr/', views.AnnualOutputACRView.as_view(), name='annual-output-acr'),
    path('annual-reformarea-output-acr/output-reporting-period/<int:output_reporting_period_id>/reform-area/<int:reform_area_id>/', views.AnnualReformAreaACRByOutputReportingPeriodAndReformArea.as_view(), name='annual_output_acr_by_reporting_period_and_reform_area'),
    path('annual-reform-area-acr/create/', views.AnnualReformAreaACRCreateView.as_view(), name='annual_reform_area_acr_create'),
    path('annual-output-acr/output-reporting-period/<int:output_reporting_period_id>/reform-area/<int:reform_area_id>/', views.AnnualOutputACRByOutputReportingPeriodAndReformArea.as_view(), name='annual_output_acr_by_reporting_period_and_reform_area'),


   
    # Output Indicator endpoints
    path('output-indicators/', views.create_output_indicators, name='create_output_indicators'),
    path('output-indicators/all/', views.get_all_output_indicators, name='list_output_indicators'),
    path('output-indicators/<int:indicator_id>/', views.get_output_indicator_by_id, name='get_output_indicator_by_id'),
    path('output-indicators/update/<int:indicator_id>/', views.update_output_indicator, name='update_output_indicator'),
    path('output-indicators/delete/<int:indicator_id>/', views.delete_output_indicator, name='delete_output_indicator'),
    path('output-indicators/deleted/', views.get_deleted_output_indicators, name='get_deleted_output_indicators'),

    # Activity endpoints
    path('activities/', views.create_activities, name='create_activities'),
    path('activities/all/', views.get_all_activities, name='list_activities'),
    path('activities/<int:activity_id>/', views.get_activity_by_id, name='get_activity_by_id'),
    path('activities/update/<int:activity_id>/', views.update_activity, name='update_activity'),
    path('activities/delete/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('activities/deleted/', views.get_deleted_activities, name='get_deleted_activities'),
    
    # Focus Area endpoints
    path('focus-areas/', views.create_focus_areas, name='create_focus_area'),
    path('focus-areas/all/', views.get_all_focus_areas, name='get_all_focus_areas'),
    path('focus-areas/<int:focus_area_id>/', views.get_focus_area_by_id, name='get_focus_area_by_id'),
    path('thematic-areas/<int:thematic_area_id>/focus-areas/', views.get_focus_areas_by_thematic_area, name='get_focus_areas_by_thematic_area'),
    path('focus-areas/<int:focus_area_id>/update/', views.update_focus_area, name='update_focus_area'),
    path('focus-areas/<int:focus_area_id>/delete/', views.delete_focus_area, name='delete_focus_area'),
    
    # Reform Status endpoints
    path('reform-statuses/', views.create_reform_statuses, name='create_reform_statuses'),
    path('reform-statuses/all/', views.get_all_reform_statuses, name='get_all_reform_statuses'),
    path('reform-statuses/<int:reform_status_id>/', views.get_reform_status_by_id, name='get_reform_status_by_id'),
    path('reform-status/reform-area/<int:reform_area_id>/', views.get_reform_status_by_reform_area, name='get_reform_status_by_reform_area'),
    path('reform-statuses/<int:reform_status_id>/update/', views.update_reform_status, name='update_reform_status'),
    path('reform-statuses/<int:reform_status_id>/delete/', views.delete_reform_status, name='delete_reform_status'),
    
    # Period endpoints
    path('periods/', views.create_period, name='create_period'),
    path('periods/all/', views.get_all_periods, name='get_all_periods'),
    path('periods/<int:period_id>/', views.get_period_by_id, name='get_period_by_id'),
    path('periods/institution/<int:institution_id>/', views.get_periods_by_latest_year_and_institution_id, name='get_periods_by_institution'),
    path('periods/<int:period_id>/update/', views.update_period, name='update_period'),
    path('periods/<int:period_id>/delete/', views.delete_period, name='delete_period'),
    
    #reformareaperiod
    path('reformareaperiod/', views.create_reform_area_period, name='create_reform_area_period'),
    path('reformareaperiod/<int:period_id>/', views.get_reform_area_period_by_id, name='get_reform_area_period_by_id'),
    path('reformareas/<int:reform_area_id>/periods/', views.get_reform_area_periods_by_reform_area_id, name='get_reform_area_periods_by_reform_area_id'),
    path('reformareaperiod/<int:period_id>/', views.update_reform_area_period, name='update_reform_area_period'),
    path('reformareaperiod/<int:period_id>/', views.delete_reform_area_period, name='delete_reform_area_period'),
    path('reformareaperiod/all/', views.get_reform_area_periods, name='get_reform_area_periods'),
    
    
    #reformfocuArea endpoints
    path('reformfocusarea/', views.create_reform_focus_area, name='create_reform_focus_area'),
    path('reformfocusarea/<int:id>/', views.get_reform_focus_area_by_id, name='get_reform_focus_area_by_id'),
    path('reformfocusarea/reform-area/<int:reform_area_id>/focus-areas/', views.get_reform_focus_areas_by_reform_area_id, name='get_reform_focus_areas_by_reform_area_id'),
    path('reformfocusarea/focus-area/<int:focus_area_id>/reform-areas/', views.get_reform_focus_areas_by_focus_area_id, name='get_reform_focus_areas_by_focus_area_id'),
    path('reformfocusarea/<int:id>/', views.update_reform_focus_area, name='update_reform_focus_area'),
    path('reformfocusarea/<int:id>/', views.delete_reform_focus_area, name='delete_reform_focus_area'),
    path('reformfocusarea/all/', views.get_reform_focus_areas, name='get_reform_focus_areas'),
    
    
    #weight endpoints
    path('weights/create/', views.create_weight, name='create_weight'),
    path('weights/all/', views.get_all_weights, name='get_all_weights'),
    path('weights/<int:weight_id>/', views.get_weight_by_id, name='get_weight_by_id'),
    path('weights/reform_area/<int:reform_area_id>/', views.get_weights_by_reform_area_id, name='get_weights_by_reform_area_id'),
    path('weights/<int:weight_id>/update/', views.update_weight, name='update_weight'),
    path('weights/<int:weight_id>/delete/', views.delete_weight, name='delete_weight'),
    
    #output-target endpoints
    path('output-targets/', views.create_output_target, name='create_output_target'),
    path('output-targets/all/', views.get_all_output_targets, name='get_all_output_targets'),
    path('output-targets/<int:id>/', views.delete_output_target, name='delete_output_target'),
    path('output-targets/indicator/<int:indicator_id>/', views.get_output_targets_by_indicator_id, name='get_output_targets_by_indicator_id'),
    path('output-targets/<int:id>/update/', views.update_output_target, name='update_output_target'),
    path('calculate-weights/<int:output_id>/<int:year>/', views.calculate_and_create_weights, name='calculate_weights'),
    path('calculate-end-of-contract-weights/<int:output_id>/<int:year>/', views.calculate_and_create_end_contract_weights, name='calculate_weights'),
    path('get-output-weights/<int:output_id>/<int:year>/', views.get_output_weights, name='get_output_weights'),
    path('get-end-contract-output-weights/<int:output_id>/<int:year>/', views.get_end_contract_output_weights, name='get_end_contract_output_weights'),

    
    #outputMoV endpoints
    path('output-movs/', views.create_output_movs, name='outputmov-list-create'),
    path('output-movs/<int:pk>/', views.OutputMovRetrieve.as_view(), name='outputmov-retrieve'),
    path('output-movs/update/<int:pk>/', views.OutputMovUpdate.as_view(), name='outputmov-update'),
    path('output-movs/delete/<int:pk>/', views.OutputMovDestroy.as_view(), name='outputmov-delete'),
    path('output-movs/indicator/<int:output_indicator_id>/', views.OutputMovByIndicatorList.as_view(), name='outputmov-by-indicator'),




    #outputCSFs endpoint
    path('output-csfs/', views.create_output_csfs, name='outputcsf-list-create'),
    path('output-csfs/<int:pk>/', views.OutputCSFRetrieveUpdateDestroy.as_view(), name='outputcsf-detail'),
    path('output-csfs/indicator/<int:output_indicator_id>/', views.OutputCSFByIndicatorList.as_view(), name='outputcsf-by-indicator'),
    
    #outputinstruments endpoint
    path('output-instruments/', views.create_output_instruments, name='outputinstrument-list-create'),
    path('output-instruments/<int:pk>/', views.OutputInstrumentRetrieveUpdateDestroy.as_view(), name='outputinstrument-detail'),
    path('output-instruments/indicator/<int:output_indicator_id>/', views.OutputInstrumentByIndicatorList.as_view(), name='outputinstrument-by-indicator'),

    #outcome-target endpoints
    path('outcome-targets/', views.create_outcome_target, name='create_outcome_target'),
    path('outcome-targets/all/', views.get_all_outcome_targets, name='get_all_outcome_targets'),
    path('outcome-targets/<int:outcome_targets_id>/', views.get_outcome_target_by_id, name='get_outcome_target_by_id'),
    path('outcome-targets/indicator/<int:indicator_id>/', views.get_outcome_targets_by_indicator, name='get_outcome_targets_by_indicator'),
    path('outcome-targets/<int:outcome_targets_id>/update/', views.update_outcome_target, name='update_outcome_target'),
    path('outcome-targets/<int:outcome_targets_id>/delete/', views.delete_outcome_target, name='delete_outcome_target'),
    
    # Outcome MoV endpoints
    path('outcome-movs/', views.create_outcome_movs, name='outcome-mov-list-create'),
    path('outcome-movs/<int:pk>/', views.OutcomeMoVRetrieve.as_view(), name='outcome-mov-Retrieve'),
    path('outcome-movs/all/', views.OutcomeMoVListView.as_view(), name='outcome-mov-ListView'),
    path('outcome-movs/update/<int:pk>/', views.OutcomeMoVUpdate.as_view(), name='outcome-mov-Update'),
    path('outcome-movs/delete/<int:pk>/', views.OutcomeMoVDestroy.as_view(), name='outcome-mov-Destroy'),
    path('outcome-movs/indicator/<int:outcome_indicator_id>/', views.get_outcome_movs_by_indicator, name='outcome-mov-by-indicator'),
    path('outcome_movs/delete/empty-arrays/all/', views.delete_all_outcome_mov, name='delete_outcome_mov'),

    path('outcome_movs/deleted/all/', views.DeletedOutcomeMoVListView.as_view(), name='delete_outcome_mov'),


    # Outcome CSF endpoints
    path('outcome-csfs/', views.create_outcome_csfs, name='outcome-csf-list-create'),
    path('outcome-csfs/<int:pk>/', views.OutcomeCSFDetail.as_view(), name='outcome-csf-detail'),
    path('outcome-csfs/indicator/<int:outcome_indicator_id>/', views.get_outcome_csfs_by_indicator, name='outcome-csf-by-indicator'),

    # Outcome Instrument endpoints
    path('outcome-instruments/', views.create_outcome_instruments, name='outcome-instrument-list-create'),
    path('outcome-instruments/<int:pk>/', views.OutcomeInstrumentDetail.as_view(), name='outcome-instrument-detail'),
    path('outcome-instruments/indicator/<int:outcome_indicator_id>/', views.get_outcome_instruments_by_indicator, name='outcome-instrument-by-indicator'),
    
    #Output-budget endpoints
    path('output-budgets/', views.create_output_budget, name='create-output-budget'),
    path('output-budgets/all/', views.get_all_output_budgets, name='get-all-output-budgets'),
    path('output-budgets/<int:output_budget_id>/', views.get_output_budget_by_id, name='get-output-budget-by-id'),
    path('output-budgets/<int:output_budget_id>/update/', views.update_output_budget, name='update-output-budget'),
    path('output-budgets/<int:output_budget_id>/delete/', views.delete_output_budget, name='delete-output-budget'),
    
    #reform-budget endpoints
    path('reform-budgets/', views.create_reform_budget, name='create-reform-budget'),
    path('reform-budgets/all/', views.get_all_reform_budgets, name='get-all-reform-budgets'),
    path('reform-budgets/<int:reform_budget_id>/', views.get_reform_budget_by_id, name='get-reform-budget-by-id'),
    path('reform-budgets/<int:reform_budget_id>/update/', views.update_reform_budget, name='update-reform-budget'),
    path('reform-budgets/<int:reform_budget_id>/delete/', views.delete_reform_budget, name='delete-reform-budget'),
    
    #budget endpoints
    path('budgets/', views.create_budget, name='create-budget'),
    path('budgets/all/', views.get_all_budgets, name='get-all-budgets'),
    path('budgets/<int:pk>/', views.get_budget_by_id, name='get-budget-by-id'),
    path('budgets/activity/<int:activity_id>/', views.get_budget_by_activity_id, name='get-budget-by-activity-id'),
    path('budgets/<int:pk>/update/', views.update_budget, name='update-budget'),
    path('budgets/<int:pk>/delete/', views.delete_budget, name='delete-budget'),
    
    
    # OrgResponsibility endpoints
    path('org-responsibilities/', views.create_org_responsibilities, name='orgresponsibility-list-create'),
    path('org-responsibilities/list/', views.get_all_org_responsibilities, name='orgresponsibility-list-view'),
    path('org-responsibilities/<int:org_responsibility_id>/', views.get_org_responsibility_by_id, name='get_org_responsibility_by_id'),
    path('org-responsibilities/institution/<int:institution_id>/', views.get_org_responsibility_by_institution_id, name='get_org_responsibilities_by_institution'),
    path('org-responsibilities/<int:org_responsibility_id>/update/', views.update_org_responsibility, name='orgresponsibility-update'),
    path('org-responsibilities/<int:org_responsibility_id>/delete/', views.delete_org_responsibility, name='orgresponsibility-destroy'),
    
    # GovtObligation endpoints
    path('govt-obligations/', views.create_govt_obligations, name='govtobligation-list-create'),
    path('govt-obligations/list/', views.get_all_govt_obligations, name='govtobligation-list-view'),
    path('govt-obligations/<int:govt_obligation_id>/', views.get_govt_obligation_by_id, name='get_govt_obligation_by_id'),
    path('govt-obligations/institution/<int:institution_id>/', views.get_govt_obligation_by_institution_id, name='get_govt_obligations_by_institution'),
    path('govt-obligations/<int:govt_obligation_id>/update/', views.update_govt_obligation, name='govtobligation-update'),
    path('govt-obligations/<int:govt_obligation_id>/delete/', views.delete_govt_obligation, name='govtobligation-destroy'),
    
    # IndicatorPeriod endpoints
    path('indicator-periods/', views.create_indicator_period, name='indicator-period-list-create'),
    path('indicator-periods/list/', views.get_all_indicator_periods, name='indicator-period-list-view'),
    path('indicator-periods/<int:period_id>/', views.get_indicator_period_by_id, name='get_indicator_period_by_id'),
    path('indicator-periods/indicator/<int:output_indicator_id>/latest/', views.get_latest_indicator_period, name='get_latest_indicator_period'),
    path('indicator-periods/<int:period_id>/update/', views.update_indicator_period, name='indicator-period-update'),
    path('indicator-periods/<int:period_id>/delete/', views.delete_indicator_period, name='indicator-period-destroy'),

    # Output Reporting Period endpoints
    path('output-reporting-period/', views.OutputReportingPeriodListCreate.as_view(), name='output-reporting-period-list-create'),
    path('output-reporting-period/<int:pk>/', views.OutputReportingPeriodRetrieve.as_view(), name='output-reporting-period-retrieve-update-destroy'),
    path('output-reporting-period/update/<int:pk>/', views.OutputReportingPeriodUpdate.as_view(), name='output-reporting-period-retrieve-update-destroy'),
    path('output-reporting-period/delete/<int:pk>/', views.OutputReportingPeriodDestroy.as_view(), name='output-reporting-period-retrieve-update-destroy'),
    path('output-reporting-period/all/', views.OutputReportingPeriodListCreate.as_view(), name='output-reporting-period-retrieve-update-destroy'),
    path('output-reporting-period/active/', views.ActiveOutputReportingPeriodRetrieve.as_view(), name='active-output-reporting-period'),
    path('output-reporting-period/current/', views.CurrentOutputReportingPeriod.as_view(), name='current-output-reporting-period'),

    
    path('output-actual/', views.OutputActualCreateView.as_view(), name='output-actual'),
    path('output-actual/<int:pk>/', views.OutputActualRetrieve.as_view(), name='output-actual-detail'),
    path('output-actual/by-output-indicator/<int:output_indicator_id>/current-year/', views.OutputActualByOutputIndicatorCurrentYear.as_view(), name='output-actual-by-output-indicator-current-year'),

    path('special-reporting-permission/grant/', views.GrantSpecialReportingPermissionView.as_view(), name='grant-special-reporting-permission'),
    
    path('reform-area-criteria/', views.ReformAreaCriteriaCreateView.as_view(), name='reform-area-criteria-create'),

    #Reform Area Sector
    path('reform-area-sector/', views.ReformAreaSectorCreateView.as_view(), name='reform-area-sector-create'),
    path('reform-area-sector/list/', views.ReformAreaSectorListView.as_view(), name='reform-area-sector-list'),
    path('reform-area-sector/<int:pk>/', views.ReformAreaSectorDetailView.as_view(), name='reform-area-sector-detail'),
    path('reform-area-sector/<int:pk>/update/', views.ReformAreaSectorUpdateView.as_view(), name='reform-area-sector-update'),
    path('reform-area-sector/<int:pk>/delete/', views.ReformAreaSectorDeleteView.as_view(), name='reform-area-sector-delete'),
    
    
    # ReformAreaSectorMapping URLs
    path('reform-area-sector-mapping/create/', views.ReformAreaSectorMappingCreateView.as_view(), name='reform-area-sector-mapping-create'),
    path('reform-area-sector-mapping/list/', views.ReformAreaSectorMappingListView.as_view(), name='reform-area-sector-mapping-list'),
    path('reform-area-sector-mapping/<int:pk>/', views.ReformAreaSectorMappingDetailView.as_view(), name='reform-area-sector-mapping-detail'),
    path('reform-area-sector-mapping/<int:pk>/update/', views.ReformAreaSectorMappingUpdateView.as_view(), name='reform-area-sector-mapping-update'),
    path('reform-area-sector-mapping/<int:pk>/delete/', views.ReformAreaSectorMappingDeleteView.as_view(), name='reform-area-sector-mapping-delete'),
    
    # Reform Category
    path('reform-category/', views.ReformCategoryCreateView.as_view(), name='reform-category-create'),
    path('reform-category/list/', views.ReformCategoryListView.as_view(), name='reform-category-list'),
    path('reform-category/<int:pk>/', views.ReformCategoryDetailView.as_view(), name='reform-category-detail'),
    path('reform-category/<int:pk>/update/', views.ReformCategoryUpdateView.as_view(), name='reform-category-update'),
    path('reform-category/<int:pk>/delete/', views.ReformCategoryDeleteView.as_view(), name='reform-category-delete'),


    # Reform Category Mapping
    path('reform-category-mapping/', views.ReformCategoryMappingCreateView.as_view(), name='reform-category-mapping-create'),
    path('reform-category-mapping/list/', views.ReformCategoryMappingListView.as_view(), name='reform-category-mapping-list'),
    path('reform-category-mapping/<int:pk>/', views.ReformCategoryMappingDetailView.as_view(), name='reform-category-mapping-detail'),
    path('reform-category-mapping/<int:pk>/update/', views.ReformCategoryMappingUpdateView.as_view(), name='reform-category-mapping-update'),
    path('reform-category-mapping/<int:pk>/delete/', views.ReformCategoryMappingDeleteView.as_view(), name='reform-category-mapping-delete'),
    
    # Output Progress endpoints
    path('output-progress/', views.OutputProgressListCreate.as_view(), name='output_progress_list_create'),
    path('output-progress/all/', views.get_all_output_progresses, name='get_all_output_progresses'),
    path('output-progress/<int:progress_id>/', views.get_output_progress_by_id, name='get_output_progress_by_id'),
    path('output-progress/reform-area/<int:reform_area_id>/', views.get_output_progresses_by_reform_area, name='get_output_progresses_by_reform_area'),
    path('output-progress/<int:progress_id>/update/', views.update_output_progress, name='update_output_progress'),
    path('output-progress/<int:progress_id>/delete/', views.delete_output_progress, name='delete_output_progress'),

    # End of contract endpoint 
    path('endof-contract-output-acr/', views.EndofContractOutputACRView.as_view(), name='endof-contract-output-acr'),
    path('get-end-contract-output-weights/<int:output_id>/<int:year>/', views.get_end_contract_output_weights, name='get_end_contract_output_weights'),
    path('end-contract-reform-area-acr/create/', views.EndContractReformAreaACRCreateView.as_view(), name='end_contract_reform_area_acr_create'),
    path('endcontract-reform-area-acr/<int:output_reporting_period_id>/<int:reform_area_id>/', views.EndContractReformAreaACRByOutputReportingPeriodAndReformArea.as_view(), name='endcontract_reform_area_acr_by_reporting_period_and_reform_area'),


]