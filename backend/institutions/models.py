# institutions/models.py
from django.db import models
from users.models import User
from django.db.models import Sum, Avg, Count


class Region(models.Model):
    region = models.CharField(max_length=50, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.region

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.CharField(max_length=50, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.district

class Institution(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=45)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.institution_name
    

class InstitutionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'institution')

    def __str__(self):
        return f"{self.user.email} - {self.institution.institution_name}"

# Update Institution model to use the through table for the many-to-many relationship
Institution.users = models.ManyToManyField(User, through=InstitutionUser, related_name='institutions')

class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.department_name
    
class UserDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'department')

    def __str__(self):
        return f"{self.user.email} - {self.department.name}"
    
# InstitutionDepartment model
class InstitutionDepartment(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('institution', 'department')

    def __str__(self):
        return f"{self.institution.institution_name} - {self.department.department_name}"
    
class Mandate(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    mandate = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.mandate
    
class Mission(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    mission = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.mission
    
class Vision(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    vision = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.vision
    
class StrategicObjective(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    objective = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.objective
    
class ThematicArea(models.Model):
    thematic_area = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.thematic_area
    
class ReformArea(models.Model):
    objective = models.ForeignKey('StrategicObjective', on_delete=models.CASCADE)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    thematic_area = models.ForeignKey(ThematicArea, on_delete=models.CASCADE)
    reform_area = models.TextField()
    year = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.reform_area
    
class Problem(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='problems', on_delete=models.CASCADE)
    problem = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.problem
    
class Outcome(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='outcomes', on_delete=models.CASCADE)
    outcomes = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.outcomes

class OutcomeIndicator(models.Model):
    outcome = models.ForeignKey(Outcome, related_name='outcome_indicators', on_delete=models.CASCADE)
    indicator = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.indicator

class Output(models.Model):
    reform_area = models.ForeignKey('ReformArea', related_name='outputs', on_delete=models.CASCADE)
    outcome = models.ForeignKey('Outcome', related_name='outputs', on_delete=models.CASCADE)
    output = models.CharField(max_length=150)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.output

class OutputIndicator(models.Model):
    output = models.ForeignKey(Output, related_name='output_indicators', on_delete=models.CASCADE)
    indicator = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.indicator


class Activity(models.Model):
    output = models.ForeignKey(Output, related_name='activities', on_delete=models.CASCADE)
    activity = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.activity

class Justification(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='justifications', on_delete=models.CASCADE)    
    justification = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.justification
    
class FocusArea(models.Model):
    thematic_area = models.ForeignKey('ThematicArea', related_name='focus_areas', on_delete=models.CASCADE)
    focus_area = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.focus_area

class ReformStatus(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='reform_statuses', on_delete=models.CASCADE)
    new_reform_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Reform Status for {self.reform_area}: {self.reform_status}"

class Period(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    year = models.IntegerField()
    period = models.CharField(max_length=45)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.period} - {self.year}"
    
class ReformAreaPeriod(models.Model):
    reform_area = models.ForeignKey('ReformArea', on_delete=models.CASCADE, related_name='reform_area_periods')
    period = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reform_area} - {self.period}"
    
class ReformFocusArea(models.Model):
    reform_area = models.ForeignKey('ReformArea', on_delete=models.CASCADE, related_name='reform_focus_areas')
    focus_area = models.ForeignKey('FocusArea', on_delete=models.CASCADE, related_name='focus_areas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reform_area} - {self.focus_area}"
    
    
class Weight(models.Model):
    reform_area = models.ForeignKey('ReformArea', on_delete=models.CASCADE, related_name='weights')
    weight = models.FloatField()
    justification = models.TextField()  # Added justification field
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reform_area} - {self.weight}"

    
class OutputTargets(models.Model):
    output_indicator = models.ForeignKey(OutputIndicator, on_delete=models.CASCADE, related_name='output_targets')
    year = models.IntegerField(default=0)
    baseline = models.IntegerField(default=0)
    Q1_target = models.IntegerField(default=0)
    Q2_target = models.IntegerField(default=0)
    Q3_target = models.IntegerField(default=0)
    Q4_target = models.IntegerField(default=0)
    total_target = models.IntegerField(default=0)
    responsibility = models.CharField(max_length=45, default="N/A")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.output_indicator} - {self.year}"
    

    
class OutputMov(models.Model):
    output_indicator = models.ForeignKey(OutputIndicator, on_delete=models.CASCADE, related_name='output_movs')
    mov = models.CharField(max_length=255, default="N/A")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class OutputCSF(models.Model):
    output_indicator = models.ForeignKey(OutputIndicator, on_delete=models.CASCADE, related_name='output_csfs')
    output_csf = models.CharField(max_length=100, default="N/A")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class OutputInstrument(models.Model):
    output_indicator = models.ForeignKey(OutputIndicator, on_delete=models.CASCADE, related_name='output_instruments')
    output_instrument = models.CharField(max_length=45, default="N/A")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class OutcomeTargets(models.Model):
    outcome_indicator = models.ForeignKey(OutcomeIndicator, on_delete=models.CASCADE, related_name='outcome_targets')
    year = models.IntegerField(default=0)
    baseline = models.IntegerField(default=0)
    H1_target = models.IntegerField(default=0)
    H2_target = models.IntegerField(default=0)
    total_target = models.IntegerField(default=0)
    responsibility = models.CharField(max_length=45, default="N/A")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.outcome_indicator} - {self.year}"    


class OutcomeMoV(models.Model):
    outcome_indicator = models.ForeignKey(OutcomeIndicator, related_name='outcome_movs', on_delete=models.CASCADE)
    mov = models.CharField(max_length=45, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class OutcomeCSF(models.Model):
    outcome_indicator = models.ForeignKey(OutcomeIndicator, related_name='outcome_csfs', on_delete=models.CASCADE)
    csf = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class OutcomeInstrument(models.Model):
    outcome_indicator = models.ForeignKey(OutcomeIndicator, related_name='outcome_instruments', on_delete=models.CASCADE)
    instrument = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)


class Budget(models.Model):
    activity = models.ForeignKey(Activity, related_name='budgets', on_delete=models.CASCADE)
    budget = models.IntegerField()
    fund_source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fund_source} - {self.budget}"

class OutputBudget(models.Model):
    output = models.ForeignKey(Output, on_delete=models.CASCADE)
    budget = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.output} - {self.budget}"

class ReformBudget(models.Model):
    reform_area = models.ForeignKey('ReformArea', on_delete=models.CASCADE)
    budget = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.IntegerField(default=0)
    
    def __str__(self):
        return self.budget


class OrgResponsibility(models.Model):
    institution_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    responsibility = models.CharField(max_length=255)
    year = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.responsibility


class GovtObligation(models.Model):
    institution_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    govt_obligation = models.CharField(max_length=255)
    year = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.govt_obligation
    
class IndicatorPeriod(models.Model):
    output_indicator = models.ForeignKey(OutputIndicator, on_delete=models.CASCADE)
    period = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"IndicatorPeriod(period={self.period}, output_indicator={self.output_indicator})"

class OutputReportingPeriod(models.Model):
    OUTPUT_LABELS = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ]

    start_date = models.DateField()
    end_date = models.DateField()
    output_label = models.CharField(max_length=2, choices=OUTPUT_LABELS)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.output_label} ({self.start_date} - {self.end_date})"
    
    
class OutputActual(models.Model):
    id = models.BigAutoField(primary_key=True)
    output_actual = models.FloatField()
    ACR = models.FloatField()
    extra_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    year = models.IntegerField()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    output_indicator = models.ForeignKey(
        OutputIndicator,
        on_delete=models.CASCADE,
        null=True,  # Allow output_indicator to be nullable
    )
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE)

    def __str__(self):
        return f"OutputActual for {self.institution} in {self.output_reporting_period.output_label}"
    
    def save(self, *args, **kwargs):
        if self.ACR > 1:
            self.extra_acr = self.ACR - 1
            self.ACR = 1
        else:
            self.extra_acr = 0
        super().save(*args, **kwargs)

    
class OutputACR(models.Model):
    output = models.ForeignKey(Output, related_name='output_acrs', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    average_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.output_reporting_period:
            return f"ACR for {self.output} in {self.year} - {self.output_reporting_period.output_label}"
        else:
            return f"ACR for {self.output} in {self.year}"
        
class ReformAreaACR(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='reform_area_acrs', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    average_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
   

    def save(self, *args, **kwargs):
        if self.average_acr > 1:
            self.extra_avg_acr = self.average_acr - 1
            self.average_acr = 1
        else:
            self.extra_avg_acr = 0
        super().save(*args, **kwargs)

    def __str__(self):
        if self.output_reporting_period:
            return f"ACR for {self.reform_area} in {self.year} - {self.output_reporting_period.output_label}"
        else:
            return f"ACR for {self.reform_area} in {self.year}"



    
class SpecialReportingPermission(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Permission for {self.institution} to report in {self.output_reporting_period.output_label}"
    
    
class ReformAreaCriteria(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='criteria', on_delete=models.CASCADE)
    effectiveness = models.TextField()
    efficiency = models.TextField()
    innovativeness = models.TextField()
    creativity = models.TextField()
    sustainability = models.TextField()
    transformativeness = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"ReformAreaCriteria {self.id}"

class ReformAreaSector(models.Model):
    sector = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"ReformAreaSector {self.id} - {self.sector}"
    
    
class ReformAreaSectorMapping(models.Model):
    reform_area = models.ForeignKey(ReformArea, on_delete=models.CASCADE, related_name='sector_mappings')
    sector = models.ForeignKey(ReformAreaSector, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reform_area} - {self.sector}"
    
class ReformCategory(models.Model):
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"ReformCategory {self.id} - {self.category}"


class ReformCategoryMapping(models.Model):
    reform_area = models.ForeignKey(ReformArea, on_delete=models.CASCADE, related_name='category_mappings')
    category = models.ForeignKey(ReformCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reform_area} - {self.category}"

class ThematicAreaACR(models.Model):
    thematic_area = models.ForeignKey(ThematicArea, related_name='thematic_area_acrs', on_delete=models.CASCADE)
    year = models.IntegerField()
    average_acr = models.FloatField(default=0)
    output_reporting_period = models.ForeignKey('OutputReportingPeriod', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('thematic_area', 'year')

    def save(self, *args, **kwargs):
        if self.average_acr > 1:
            self.extra_avg_acr = self.average_acr - 1
            self.average_acr = 1
        else:
            self.extra_avg_acr = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ACR for {self.thematic_area} in {self.year}"

class OutputProgress(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='output_progresses', on_delete=models.CASCADE)
    progress = models.TextField()
    output_reporting_period = models.ForeignKey('OutputReportingPeriod', on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.progress
    
class OutputWeights(models.Model):
    Q1w = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    Q2w = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    Q3w = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    Q4w = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    year = models.IntegerField()
    output_id = models.ForeignKey('Output', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"OutputWeights for {self.year}"

    class Meta:
        db_table = 'output_weights'
        unique_together = ('year', 'output_id')
        
    

class AnnualOutputACR(models.Model):
    output = models.ForeignKey(Output, related_name='annual_output_acrs', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    annual_average_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Annual ACR for {self.output} in {self.year}"


class AnnualReformAreaACR(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='annual_reform_area_acrs', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    average_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Annual ACR for {self.reform_area} in {self.year}"
    

class EndContractOutputWeights(models.Model):
    Q1w = models.DecimalField(max_digits=12, decimal_places=10, default=0)
    Q2w = models.DecimalField(max_digits=12, decimal_places=10, default=0)
    Q3w = models.DecimalField(max_digits=12, decimal_places=10, default=0)
    Q4w = models.DecimalField(max_digits=12, decimal_places=10, default=0)
    year = models.IntegerField()
    output = models.ForeignKey('Output', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"EndContractOutputWeights for {self.year}"

    class Meta:
        unique_together = ('output', 'year')

class EndofContractOutputACR(models.Model):
    output = models.ForeignKey(Output, related_name='end_contract_output_acrs', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    end_contract_average_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"End of Contract ACR for {self.output} in {self.year}"


class EndContractReformAreaACR(models.Model):
    reform_area = models.ForeignKey(ReformArea, related_name='end_contract_reform_area_acrs', on_delete=models.CASCADE)
    output_reporting_period = models.ForeignKey(OutputReportingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    average_acr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"End Contract ACR for {self.reform_area} in {self.year}"