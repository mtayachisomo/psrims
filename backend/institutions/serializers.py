# institutions/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import (Region, District, Institution, InstitutionUser, Department, UserDepartment, 
                     InstitutionDepartment, Mandate, Mission, Vision, StrategicObjective, ThematicArea, ReformArea,
                     Problem, Justification, Outcome, OutcomeIndicator, Output, OutputIndicator, Activity, FocusArea,
                     ReformStatus, Period, ReformAreaPeriod, ReformFocusArea, Weight, OutputTargets, OutcomeTargets,
                     OutputMov, OutputCSF, OutputInstrument, OutcomeMoV, OutcomeCSF, OutcomeInstrument, Budget, 
                     OutputBudget, ReformBudget, OrgResponsibility, GovtObligation, IndicatorPeriod, SpecialReportingPermission,
                     OutputActual, OutputReportingPeriod, OutputACR, ReformAreaACR, ReformAreaCriteria, ReformAreaSector, 
                     ReformAreaSectorMapping, ReformCategory, ReformCategoryMapping, ThematicAreaACR, OutputProgress,
                     OutputWeights, AnnualOutputACR, AnnualReformAreaACR, EndContractOutputWeights, EndofContractOutputACR,
                     EndofContractOutputACR, EndContractReformAreaACR
)
from users.models import User
from django.urls import reverse
from django.db.models import Max, Avg

class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region', 'updated_at', 'created_at']

    def validate_region(self, value):
        if Region.objects.filter(region=value).exists():
            raise serializers.ValidationError("Region already exists.")
        return value

class RegionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region', 'updated_at', 'created_at']

    def update(self, instance, validated_data):
        instance.region = validated_data.get('region', instance.region)
        instance.save()
        return instance

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region', 'updated_at', 'created_at', 'deleted']

class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region', 'updated_at', 'created_at']

class DistrictCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'region', 'district', 'updated_at', 'created_at']

    def validate_district(self, value):
        if District.objects.filter(district=value).exists():
            raise serializers.ValidationError("District already exists.")
        return value


class DistrictUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'region', 'district', 'updated_at', 'created_at']

    def update(self, instance, validated_data):
        instance.region = validated_data.get('region', instance.region)
        instance.district = validated_data.get('district', instance.district)
        instance.save()
        return instance

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'region', 'district', 'updated_at', 'created_at', 'deleted']

class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'region', 'district', 'updated_at', 'created_at']

class InstitutionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'district', 'institution_name', 'email', 'phone', 'updated_at', 'created_at']

    def validate_email(self, value):
        if Institution.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered with us.")
        return value

class InstitutionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'district', 'institution_name', 'email', 'phone', 'updated_at', 'created_at']

    def update(self, instance, validated_data):
        instance.district = validated_data.get('district', instance.district)
        instance.institution_name = validated_data.get('institution_name', instance.institution_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'district', 'institution_name', 'email', 'phone', 'updated_at', 'created_at', 'deleted']

class InstitutionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'district', 'institution_name', 'email', 'phone', 'updated_at', 'created_at']

class InstitutionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionUser
        fields = ['id', 'user', 'institution', 'created_at', 'updated_at']

    def create(self, validated_data):
        institution_user = InstitutionUser.objects.create(**validated_data)
        return institution_user

class UserInstitutionSerializer(serializers.ModelSerializer):
    institutions = InstitutionListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'institutions']
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'created_at', 'updated_at', 'deleted']

class UserDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartment
        fields = ['id', 'user', 'department', 'created_at', 'updated_at', 'deleted']

class UserDepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartment
        fields = ['id', 'user', 'department', 'created_at', 'updated_at', 'deleted']

class UserDepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartment
        fields = ['id', 'user', 'department', 'created_at', 'updated_at', 'deleted']


# InstitutionDepartment serializers
class InstitutionDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionDepartment
        fields = ['id', 'institution', 'department', 'created_at', 'updated_at', 'deleted']

class InstitutionDepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionDepartment
        fields = ['id', 'institution', 'department', 'created_at', 'updated_at', 'deleted']
        
class MandateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mandate
        fields = ['id', 'institution', 'mandate', 'updated_at', 'created_at', 'deleted']

class MandateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mandate
        fields = ['institution', 'mandate']

    def create(self, validated_data):
        # Update the previous mandate entry's 'deleted' field to True
        Mandate.objects.filter(institution=validated_data['institution'], deleted=False).update(deleted=True)
        return super().create(validated_data)

class MandateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mandate
        fields = ['mandate']

    def update(self, instance, validated_data):
        instance.mandate = validated_data.get('mandate', instance.mandate)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
    
class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'institution', 'mission', 'updated_at', 'created_at', 'deleted']

class MissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['institution', 'mission']

    def create(self, validated_data):
        Mission.objects.filter(institution=validated_data['institution'], deleted=False).update(deleted=True)
        return super().create(validated_data)

class MissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['mission']

    def update(self, instance, validated_data):
        instance.mission = validated_data.get('mission', instance.mission)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
    
class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = ['id', 'institution', 'vision', 'updated_at', 'created_at', 'deleted']

class VisionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = ['institution', 'vision']

    def create(self, validated_data):
        Vision.objects.filter(institution=validated_data['institution'], deleted=False).update(deleted=True)
        return super().create(validated_data)

class VisionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = ['vision']

    def update(self, instance, validated_data):
        instance.vision = validated_data.get('vision', instance.vision)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
    


class StrategicObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicObjective
        fields = ['id', 'institution', 'objective', 'updated_at', 'created_at', 'deleted']

class StrategicObjectiveCreateSerializer(serializers.Serializer):
    institution_id = serializers.IntegerField()
    objectives = serializers.ListField(child=serializers.CharField())

class StrategicObjectiveResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicObjective
        fields = ['id', 'institution', 'objective', 'updated_at', 'created_at', 'deleted']

class ThematicAreaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicArea
        fields = ['thematic_area', 'description']

class ThematicAreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicArea
        fields = ['id', 'thematic_area', 'description', 'created_at', 'updated_at']

class ReformAreaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformArea
        fields = ['id', 'objective', 'institution', 'thematic_area', 'reform_area', 'year']

class ReformAreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformArea
        fields = ['id', 'objective', 'institution', 'thematic_area', 'reform_area', 'year', 'updated_at', 'created_at']

 
class ProblemCreateSerializer(serializers.Serializer):
    reform_area_id = serializers.IntegerField()
    problems = serializers.ListField(child=serializers.CharField())

class ProblemResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'reform_area_id', 'problem', 'updated_at', 'created_at', 'deleted']
        
class JustificationCreateSerializer(serializers.Serializer):
    reform_area_id = serializers.IntegerField()
    justifications = serializers.ListField(child=serializers.CharField())

class JustificationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = ['id', 'reform_area_id', 'justification', 'updated_at', 'created_at', 'deleted']

class CreateOutcomeRequestSerializer(serializers.ModelSerializer):
    outcomes = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = Outcome
        fields = ['reform_area', 'outcomes']

    def create(self, validated_data):
        outcomes_data = validated_data.pop('outcomes')
        reform_area = validated_data.pop('reform_area')
        outcomes = []
        for outcome_text in outcomes_data:
            outcome = Outcome.objects.create(reform_area=reform_area, outcomes=outcome_text)
            outcomes.append(outcome)
        return outcomes


class CreateOutcomeIndicatorSerializer(serializers.ModelSerializer):
    indicators = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = OutcomeIndicator
        fields = ['outcome', 'indicators']

    def create(self, validated_data):
        indicators_data = validated_data.pop('indicators')
        outcome = validated_data.pop('outcome')
        indicators = []
        for indicator_text in indicators_data:
            indicator = OutcomeIndicator.objects.create(outcome=outcome, indicator=indicator_text)
            indicators.append(indicator)
        return indicators

class OutcomeTargetsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeTargets
        fields = ['outcome_indicator', 'year', 'baseline', 'H1_target', 'H2_target', 'total_target', 'responsibility']

class OutcomeMoVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeMoV
        fields = ['id', 'outcome_indicator', 'mov', 'updated_at', 'created_at', 'deleted']
        
        
    def validate(self, data):
        data.setdefault('mov', 'N/A')
        return data


    def to_representation(self, instance):
        if instance.deleted:
            return {}
        return super().to_representation(instance)


class OutcomeCSFSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCSF
        fields = ['id', 'outcome_indicator', 'csf', 'updated_at', 'created_at', 'deleted']

    def to_representation(self, instance):
        if instance.deleted:
            return {}
        return super().to_representation(instance)
    
    def validate(self, data):
        data.setdefault('csf', 'N/A')
        return data

class OutcomeInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeInstrument
        fields = ['id', 'outcome_indicator', 'instrument', 'updated_at', 'created_at', 'deleted']

    def to_representation(self, instance):
        if instance.deleted:
            return {}
        return super().to_representation(instance)
    
    def validate(self, data):
        data.setdefault('instrument', 'N/A')
        return data


class OutcomeIndicatorResponseSerializer(serializers.ModelSerializer):
    outcome_targets = serializers.SerializerMethodField()
    outcome_movs = serializers.SerializerMethodField()
    outcome_csfs = serializers.SerializerMethodField()
    outcome_instruments = serializers.SerializerMethodField()

    class Meta:
        model = OutcomeIndicator
        fields = ['id', 'outcome_id', 'indicator', 'updated_at', 'created_at', 'deleted', 'outcome_targets', 'outcome_movs', 'outcome_csfs', 'outcome_instruments']

    def get_outcome_targets(self, obj):
        outcome_targets = obj.outcome_targets.filter(deleted=False)
        return OutcomeTargetsBaseSerializer(outcome_targets, many=True).data

    def get_outcome_movs(self, obj):
        outcome_movs = obj.outcome_movs.filter(deleted=False)
        return OutcomeMoVSerializer(outcome_movs, many=True).data

    def get_outcome_csfs(self, obj):
        outcome_csfs = obj.outcome_csfs.filter(deleted=False)
        return OutcomeCSFSerializer(outcome_csfs, many=True).data

    def get_outcome_instruments(self, obj):
        outcome_instruments = obj.outcome_instruments.filter(deleted=False)
        return OutcomeInstrumentSerializer(outcome_instruments, many=True).data

class CreateOutputRequestSerializer(serializers.ModelSerializer):
    outputs = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = Output
        fields = ['reform_area', 'outcome', 'outputs']

    def create(self, validated_data):
        outputs_data = validated_data.pop('outputs')
        reform_area = validated_data.pop('reform_area')
        outcome = validated_data.pop('outcome')
        outputs = []
        for output_text in outputs_data:
            output = Output.objects.create(reform_area=reform_area, outcome=outcome, output=output_text)
            outputs.append(output)
        return outputs


class CreateOutputIndicatorRequestSerializer(serializers.ModelSerializer):
    indicators = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = OutputIndicator
        fields = ['output', 'indicators']

    def create(self, validated_data):
        indicators_data = validated_data.pop('indicators')
        output = validated_data.pop('output')
        indicators = []
        for indicator_text in indicators_data:
            indicator = OutputIndicator.objects.create(output=output, indicator=indicator_text)
            indicators.append(indicator)
        return indicators

        
class OutputTargetsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputTargets
        fields = [
            'id', 'output_indicator', 'year', 'baseline', 'Q1_target', 'Q2_target', 
            'Q3_target', 'Q4_target', 'total_target', 'responsibility', 'created_at', 
            'updated_at', 'deleted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted']

class OutputTargetsCreateSerializer(OutputTargetsBaseSerializer):
    class Meta(OutputTargetsBaseSerializer.Meta):
        pass

class OutputTargetsResponseSerializer(OutputTargetsBaseSerializer):
    class Meta(OutputTargetsBaseSerializer.Meta):
        pass

class OutputTargetsListResponseSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    data = OutputTargetsResponseSerializer(many=True)
    
class OutputWeightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputWeights
        fields = ['id', 'Q1w', 'Q2w', 'Q3w', 'Q4w', 'year', 'output_id', 'created_at', 'updated_at', 'deleted']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted']

class EndContractOutputWeightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndContractOutputWeights
        fields = '__all__'
        
class OutputMovCreateSerializer(serializers.Serializer):
    output_indicator_id = serializers.IntegerField()
    movs = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

class OutputMovResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputMov
        fields = ['id', 'output_indicator', 'mov', 'updated_at', 'created_at', 'deleted']

class OutputCSFCreateSerializer(serializers.Serializer):
    output_indicator_id = serializers.IntegerField()
    output_csfs = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

class OutputCSFResponseSerializer(serializers.ModelSerializer):
    output_indicator_id = serializers.IntegerField(source='output_indicator.id')

    class Meta:
        model = OutputCSF
        fields = ['id', 'output_indicator_id', 'output_csf', 'updated_at', 'created_at', 'deleted']

class OutputInstrumentCreateSerializer(serializers.Serializer):
    output_indicator_id = serializers.IntegerField()
    output_instruments = serializers.ListField(
        child=serializers.CharField(max_length=45)
    )

class OutputInstrumentResponseSerializer(serializers.ModelSerializer):
    output_indicator_id = serializers.IntegerField(source='output_indicator.id')

    class Meta:
        model = OutputInstrument
        fields = ['id', 'output_indicator_id', 'output_instrument', 'updated_at', 'created_at', 'deleted']

class OutputMovSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputMov
        fields = ['id', 'output_indicator', 'mov', 'updated_at', 'created_at', 'deleted']
        
    def validate(self, data):
        data.setdefault('mov', 'N/A')
        return data

class OutputCSFSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputCSF
        fields = ['id', 'output_indicator', 'output_csf', 'updated_at', 'created_at', 'deleted']
        
    def validate(self, data):
        data.setdefault('output_csf', 'N/A')
        return data

class OutputInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputInstrument
        fields = ['id', 'output_indicator', 'output_instrument', 'updated_at', 'created_at', 'deleted']
        
    def validate(self, data):
        data.setdefault('output_instrument', 'N/A')
        return data

class OutputIndicatorResponseSerializer(serializers.ModelSerializer):
    output_targets = OutputTargetsBaseSerializer(many=True, read_only=True)
    output_movs = OutputMovSerializer(many=True, read_only=True)
    output_csfs = OutputCSFSerializer(many=True, read_only=True)
    output_instruments = OutputInstrumentSerializer(many=True, read_only=True)
    output_actual = serializers.SerializerMethodField()

    class Meta:
        model = OutputIndicator
        fields = ['id', 'output_id', 'indicator', 'updated_at', 'created_at', 'deleted', 'output_targets', 'output_movs', 'output_csfs', 'output_instruments', 'output_actual']

    def get_output_actual(self, obj):
        output_indicator_id = obj.id
        current_year = timezone.now().year
        output_actual = OutputActual.objects.filter(output_indicator_id=output_indicator_id, year=current_year).first()
        
        if output_actual:
            return {
                'output_actual': output_actual.output_actual,
                'ACR': output_actual.ACR,
                'extra_acr': output_actual.extra_acr,
                'created_at': output_actual.created_at,
                'updated_at': output_actual.updated_at,
                'deleted': output_actual.deleted,
            }
        else:
            return None

class CreateActivityRequestSerializer(serializers.ModelSerializer):
    activities = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = Activity
        fields = ['output', 'activities']

    def create(self, validated_data):
        activities_data = validated_data.pop('activities')
        output = validated_data.pop('output')
        activities = []
        for activity_text in activities_data:
            activity = Activity.objects.create(output=output, activity=activity_text)
            activities.append(activity)
        return activities

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'activity', 'budget', 'fund_source', 'created_at', 'updated_at', 'deleted']

class ActivityResponseSerializer(serializers.ModelSerializer):
    budgets = BudgetSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'output', 'activity', 'updated_at', 'created_at', 'deleted', 'budgets']

class OutputACRSerializer(serializers.ModelSerializer):
    average_acr = serializers.FloatField()  

    class Meta:
        model = OutputACR
        fields = '__all__'
        
class OutputResponseSerializer(serializers.ModelSerializer):
    output_indicators = OutputIndicatorResponseSerializer(many=True, read_only=True)
    activities = ActivityResponseSerializer(many=True, read_only=True)
    output_acrs = OutputACRSerializer(many=True, read_only=True)

    class Meta:
        model = Output
        fields = ['id', 'output', 'updated_at', 'created_at', 'deleted', 'output_indicators', 'activities', 'output_acrs']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['output'] = [rep['output']]  # Ensure output is always represented as a list
        return rep

    def to_internal_value(self, data):
        if 'output' in data and isinstance(data['output'], list) and len(data['output']) > 0:
            data['output'] = data['output'][0]  # Take the first item of the list as string
        return super().to_internal_value(data)
    
class OutputIndicatorReportingResponseSerializer(serializers.ModelSerializer):
    output_indicators = serializers.SerializerMethodField()
    

    class Meta:
        model = Output
        fields = ['id', 'output', 'updated_at', 'created_at', 'deleted', 'output_indicators']
        
    def get_output_indicators(self, obj):
        current_date = timezone.now().date()
        active_period = OutputReportingPeriod.objects.filter(start_date__lte=current_date, end_date__gte=current_date, is_active=True).first()
        
        if not active_period:
            return []  # No active period found, return empty list
        
        active_quarter = active_period.output_label

        indicators = obj.output_indicators.filter(deleted=False)
        filtered_indicators = []

        for indicator in indicators:
            targets = indicator.output_targets.filter(year=current_date.year).first()
            if not targets:
                continue

            if (
                (active_quarter == 'Q1' and targets.Q1_target > 0) or
                (active_quarter == 'Q2' and targets.Q2_target > 0) or
                (active_quarter == 'Q3' and targets.Q3_target > 0) or
                (active_quarter == 'Q4' and targets.Q4_target > 0)
            ):
                filtered_indicators.append(indicator)

        return OutputIndicatorResponseSerializer(filtered_indicators, many=True).data

class OutcomeResponseSerializer(serializers.ModelSerializer):
    outcome_indicators = serializers.SerializerMethodField()
    outputs = serializers.SerializerMethodField()

    class Meta:
        model = Outcome
        fields = ['id', 'outcomes', 'updated_at', 'created_at', 'deleted', 'outcome_indicators', 'outputs']

    def get_outcome_indicators(self, obj):
        outcome_indicators = obj.outcome_indicators.filter(deleted=False)
        return OutcomeIndicatorResponseSerializer(outcome_indicators, many=True).data

    def get_outputs(self, obj):
        outputs = obj.outputs.filter(deleted=False)
        return OutputResponseSerializer(outputs, many=True).data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['outcomes'] = [rep['outcomes']]  # Ensure outcomes is always represented as a list
        return rep

    def to_internal_value(self, data):
        if 'outcomes' in data and isinstance(data['outcomes'], list) and len(data['outcomes']) > 0:
            data['outcomes'] = data['outcomes'][0]  # Take the first item of the list as string
        return super().to_internal_value(data)


class CreateReformAreaPeriodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformAreaPeriod
        fields = ['reform_area', 'period']

class ReformAreaPeriodResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformAreaPeriod
        fields = ['id', 'reform_area', 'period', 'created_at', 'updated_at', 'deleted']

class ReformAreaPeriodListResponseSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    data = ReformAreaPeriodResponseSerializer(many=True)
      
class ReformAreaDetailSerializer(serializers.ModelSerializer):
    justifications = JustificationResponseSerializer(many=True, read_only=True)
    problems = ProblemResponseSerializer(many=True, read_only=True)
    outcomes = serializers.SerializerMethodField()
    reform_area_periods = ReformAreaPeriodResponseSerializer(many=True, read_only=True)

    class Meta:
        model = ReformArea
        fields = ['id', 'objective_id', 'institution_id', 'thematic_area_id', 'reform_area', 'year', 'updated_at', 'created_at', 'deleted', 'justifications', 'problems', 'outcomes', 'reform_area_periods']

    def get_outcomes(self, obj):
        outcomes = obj.outcomes.filter(deleted=False)
        return OutcomeResponseSerializer(outcomes, many=True).data

        
class FocusAreaCreateSerializer(serializers.Serializer):
    thematic_area_id = serializers.IntegerField()
    focus_areas = serializers.ListField(child=serializers.CharField(max_length=255))


class ReformFocusAreaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformFocusArea
        fields = ['id', 'reform_area', 'focus_area', 'created_at', 'updated_at', 'deleted']

class ReformFocusAreaListResponseSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    data = ReformFocusAreaResponseSerializer(many=True)

class FocusAreaResponseSerializer(serializers.ModelSerializer):
    reform_focus_areas = ReformFocusAreaResponseSerializer(many=True, read_only=True)

    class Meta:
        model = FocusArea
        fields = ['id', 'thematic_area_id', 'focus_area', 'updated_at', 'created_at', 'deleted', 'reform_focus_areas']

class ThematicAreaSerializer(serializers.ModelSerializer):
    reformaredetail = serializers.SerializerMethodField()
    focus_areas = FocusAreaResponseSerializer(many=True, read_only=True)

    class Meta:
        model = ThematicArea
        fields = ['id', 'thematic_area', 'description', 'created_at', 'updated_at', 'reformaredetail', 'focus_areas']

    def get_reformaredetail(self, obj):
        request = self.context.get('request')
        institution_id = request.query_params.get('institution_id')

        if institution_id:
            # Fetch the latest year for the given institution
            latest_year = ReformArea.objects.filter(
                institution_id=institution_id, deleted=False
            ).aggregate(latest_year=Max('year'))['latest_year']

            if latest_year:
                # Query all reform areas for the institution with the latest year and match the thematic area
                reform_areas = ReformArea.objects.filter(
                    institution_id=institution_id,
                    year=latest_year,
                    deleted=False,
                    thematic_area=obj
                )
                return ReformAreaDetailSerializer(reform_areas, many=True).data
        
        # Fallback to default behavior if institution_id is not provided
        reform_areas = obj.reformarea_set.filter(deleted=False)
        return ReformAreaDetailSerializer(reform_areas, many=True).data
            
class ReformStatusCreateSerializer(serializers.Serializer):
    reform_area_id = serializers.IntegerField()
    reform_status = serializers.IntegerField()

class ReformStatusResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformStatus
        fields = ['id', 'reform_area_id', 'new_reform_status', 'updated_at', 'created_at', 'deleted']

class PeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['institution', 'year', 'period']

class PeriodResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'institution', 'year', 'period', 'updated_at', 'created_at', 'deleted']
        

    
class ReformFocusAreaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformFocusArea
        fields = ['reform_area', 'focus_area']

class ReformFocusAreaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformFocusArea
        fields = ['id', 'reform_area', 'focus_area', 'created_at', 'updated_at', 'deleted']

class ReformFocusAreaListResponseSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    data = ReformFocusAreaResponseSerializer(many=True)
    
class WeightCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['reform_area', 'weight', 'justification']

class WeightResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['id', 'reform_area', 'weight', 'justification', 'updated_at', 'created_at', 'deleted']

class WeightListResponseSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    data = WeightResponseSerializer(many=True)
    

class OutcomeTargetsCreateSerializer(OutcomeTargetsBaseSerializer):
    pass

class OutcomeTargetsResponseSerializer(OutcomeTargetsBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    deleted = serializers.BooleanField(read_only=True)

    class Meta:
        model = OutcomeTargets
        fields = OutcomeTargetsBaseSerializer.Meta.fields + ['id', 'updated_at', 'created_at', 'deleted']

class OutcomeTargetsListResponseSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    data = OutcomeTargetsResponseSerializer(many=True)

    

class OutcomeMoVCreateSerializer(serializers.ModelSerializer):
    outcome_indicator_id = serializers.IntegerField()
    movs = serializers.ListField(child=serializers.CharField(max_length=45))

    class Meta:
        model = OutcomeMoV
        fields = ['outcome_indicator_id', 'movs']

class OutcomeCSFCreateSerializer(serializers.ModelSerializer):
    outcome_indicator_id = serializers.IntegerField()
    csfs = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = OutcomeCSF
        fields = ['outcome_indicator_id', 'csfs']

class OutcomeInstrumentCreateSerializer(serializers.ModelSerializer):
    outcome_indicator_id = serializers.IntegerField()
    instruments = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = OutcomeInstrument
        fields = ['outcome_indicator_id', 'instruments']


class OutputBudgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputBudget
        fields = ['output', 'budget']

class OutputBudgetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputBudget
        fields = ['id', 'output', 'budget', 'updated_at', 'created_at', 'deleted']

class ReformBudgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformBudget
        fields = ['reform_area', 'budget']

class ReformBudgetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformBudget
        fields = ['id', 'reform_area', 'budget', 'updated_at', 'created_at', 'deleted']
        
class OrgResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgResponsibility
        fields = ['id', 'institution_id', 'responsibility', 'year', 'updated_at', 'created_at', 'deleted']

class GovtObligationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovtObligation
        fields = ['id', 'institution_id', 'govt_obligation', 'year', 'updated_at', 'created_at', 'deleted']

class OrgResponsibilityCreateSerializer(serializers.Serializer):
    institution_id = serializers.IntegerField()
    responsibilities = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    year = serializers.IntegerField()

class GovtObligationCreateSerializer(serializers.Serializer):
    institution_id = serializers.IntegerField()
    govt_obligations = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    year = serializers.IntegerField()

class OrgResponsibilityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgResponsibility
        fields = ['id', 'institution_id', 'responsibility', 'year', 'updated_at', 'created_at', 'deleted']

class GovtObligationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovtObligation
        fields = ['id', 'institution_id', 'govt_obligation', 'year', 'updated_at', 'created_at', 'deleted']
           
class IndicatorPeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorPeriod
        fields = ['output_indicator', 'period']  # Changed 'output_indicator_id' to 'output_indicator'

class IndicatorPeriodResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorPeriod
        fields = ['id', 'output_indicator', 'period', 'created_at', 'updated_at', 'deleted']

class IndicatorPeriodListResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorPeriod
        fields = ['id', 'output_indicator', 'period', 'created_at', 'updated_at', 'deleted']
        
        
class OutputReportingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputReportingPeriod
        fields = '__all__'
        

class OutputActualSerializer(serializers.ModelSerializer):
    institution_id = serializers.IntegerField()
    output_indicator_id = serializers.IntegerField()
    output_actual = serializers.FloatField()
    year = serializers.IntegerField()

    class Meta:
        model = OutputActual
        fields = ['output_indicator_id', 'output_reporting_period', 'institution_id', 'output_actual', 'ACR', 'created_at', 'updated_at', 'deleted', 'year']
        read_only_fields = ['output_reporting_period', 'ACR', 'created_at', 'updated_at', 'deleted']

    def create(self, validated_data):
        institution_id = validated_data['institution_id']
        output_indicator_id = validated_data['output_indicator_id']
        year = validated_data['year']

        # Find active reporting period for the given year
        active_period = OutputReportingPeriod.objects.filter(
            is_active=True,
            start_date__year=year
        ).first()

        if not active_period:
            raise serializers.ValidationError("No active output reporting period found for the specified year.")

        # Check if an existing OutputActual instance needs to be updated
        existing_output_actual = OutputActual.objects.filter(
            output_indicator_id=output_indicator_id,
            year=year,
            output_reporting_period=active_period
        ).first()

        if existing_output_actual:
            # Update the existing OutputActual instance
            existing_output_actual.output_actual = validated_data['output_actual']
            existing_output_actual.updated_at = timezone.now()
            output_actual = existing_output_actual
        else:
            # Create a new OutputActual instance
            output_actual = OutputActual.objects.create(
                institution_id=institution_id,
                output_indicator_id=output_indicator_id,
                year=year,
                output_actual=validated_data['output_actual'],
                output_reporting_period=active_period,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                deleted=False,
                ACR=0.0  # Initialize ACR if necessary, or it can be calculated further
            )

        # Calculate ACR based on the rules for the active period
        output_target = OutputTargets.objects.filter(output_indicator_id=output_indicator_id, year=year).first()
        if not output_target:
            raise serializers.ValidationError("No output target found for the selected output indicator and year.")

        if active_period.output_label == 'Q1':
            output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q1_target - output_target.baseline)
        elif active_period.output_label == 'Q2':
            prev_actual = OutputActual.objects.filter(output_indicator_id=output_indicator_id, year=year, output_reporting_period__output_label='Q1').first()
            if not prev_actual:
                output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q2_target - output_target.baseline)
            else:
                output_actual.ACR = (output_actual.output_actual - prev_actual.output_actual) / (output_target.Q2_target - output_target.Q1_target) if output_target.Q1_target != 0 else (output_actual.output_actual - output_target.baseline) / (output_target.Q2_target - output_target.baseline)
        elif active_period.output_label == 'Q3':
            prev_actual = OutputActual.objects.filter(output_indicator_id=output_indicator_id, year=year, output_reporting_period__output_label='Q2').first()
            if not prev_actual:
                output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q3_target - output_target.baseline)
            else:
                if output_target.Q2_target != 0:
                    output_actual.ACR = (output_actual.output_actual - prev_actual.output_actual) / (output_target.Q3_target - output_target.Q2_target)
                elif output_target.Q1_target != 0:
                    output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q3_target - output_target.Q1_target)
                else:
                    output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q3_target - output_target.baseline)
        elif active_period.output_label == 'Q4':
            prev_actual = OutputActual.objects.filter(output_indicator_id=output_indicator_id, year=year, output_reporting_period__output_label='Q3').first()
            if not prev_actual:
                output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q4_target - output_target.Q3_target)
            else:
                if output_target.Q3_target != 0:
                    output_actual.ACR = (output_actual.output_actual - prev_actual.output_actual) / (output_target.Q4_target - output_target.Q3_target)
                elif output_target.Q2_target != 0:
                    output_actual.ACR = (output_actual.output_actual - prev_actual.output_actual) / (output_target.Q4_target - output_target.Q2_target)
                elif output_target.Q1_target != 0:
                    output_actual.ACR = (output_actual.output_actual - prev_actual.output_actual) / (output_target.Q4_target - output_target.Q1_target)
                else:
                    output_actual.ACR = (output_actual.output_actual - output_target.baseline) / (output_target.Q4_target - output_target.baseline)
         # Set ACR to 0 if it is negative
        if output_actual.ACR < 0:
            output_actual.ACR = 0


        # Save the updated OutputActual instance with ACR
        output_actual.save()

        return output_actual

        
class ReformAreaACRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformAreaACR
        fields = ('id', 'year', 'average_acr', 'created_at', 'updated_at', 'deleted', 'output_reporting_period_id', 'reform_area_id')


        
class SpecialReportingPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialReportingPermission
        fields = ['institution', 'output_reporting_period', 'granted_at', 'expires_at']
        

class ReformAreaCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformAreaCriteria
        fields = '__all__'
        
class ReformAreaSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformAreaSector
        fields = '__all__'
        
class ReformAreaSectorMappingSerializer(serializers.ModelSerializer):
    reform_area = serializers.PrimaryKeyRelatedField(queryset=ReformArea.objects.all())
    sector = serializers.PrimaryKeyRelatedField(queryset=ReformAreaSector.objects.all())

    class Meta:
        model = ReformAreaSectorMapping
        fields = '__all__'
        

class ReformCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReformCategory
        fields = '__all__'

class ReformCategoryMappingSerializer(serializers.ModelSerializer):
    reform_area = serializers.PrimaryKeyRelatedField(queryset=ReformArea.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=ReformCategory.objects.all())

    class Meta:
        model = ReformCategoryMapping
        fields = '__all__'


class ThematicAreaACRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicAreaACR
        fields = ('id', 'year', 'average_acr', 'output_reporting_period_id', 'thematic_area_id')
        
class OutputProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputProgress
        fields = ['id', 'reform_area', 'progress', 'output_reporting_period', 'updated_at', 'created_at', 'deleted']
        
class AnnualOutputACRSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnualOutputACR
        fields = '__all__'
        
class AnnualOutputACRSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnualOutputACR
        fields = '__all__'
        
class AnnualReformAreaACRSerializer(serializers.ModelSerializer):
    annual_output_acrs = serializers.SerializerMethodField() 

    class Meta:
        model = AnnualReformAreaACR
        fields = ('id', 'year', 'average_acr', 'created_at', 'updated_at', 'deleted', 'output_reporting_period_id', 'reform_area_id', 'annual_output_acrs')

    def get_annual_output_acrs(self, obj):
        output_reporting_period_id = self.context.get('output_reporting_period_id')

        if not output_reporting_period_id:
            return []

        related_outputs = Output.objects.filter(reform_area_id=obj.reform_area_id)

        latest_year = AnnualOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs
        ).aggregate(Max('year'))['year__max']

        annual_output_acrs = AnnualOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs,
            year=latest_year
        )
        return AnnualOutputACRSerializer(annual_output_acrs, many=True).data

    def calculate_average_acr(self, reform_area, year):
        # Get all AnnualOutputACR for the current ReformArea
        related_annual_acrs = AnnualOutputACR.objects.filter(
            output__reform_area=reform_area,
            year=year,
            deleted=False
        )
        
        # Calculate and return the average ACR
        return related_annual_acrs.aggregate(Avg('annual_average_acr'))['annual_average_acr__avg'] or 0


class EndofContractOutputACRSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndofContractOutputACR
        fields = ('id', 'output', 'output_reporting_period', 'year', 'end_contract_average_acr')

class EndContractReformAreaACRSerializer(serializers.ModelSerializer):
    end_contract_output_acrs = serializers.SerializerMethodField()

    class Meta:
        model = EndContractReformAreaACR
        fields = ('id', 'year', 'average_acr', 'created_at', 'updated_at', 'deleted', 'output_reporting_period', 'reform_area_id', 'end_contract_output_acrs')

    def get_end_contract_output_acrs(self, obj):
        output_reporting_period_id = self.context.get('output_reporting_period_id')

        if not output_reporting_period_id:
            return []

        related_outputs = Output.objects.filter(reform_area_id=obj.reform_area_id)

        latest_year = EndofContractOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs
        ).aggregate(Max('year'))['year__max']

        end_contract_output_acrs = EndofContractOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs,
            year=latest_year
        )
        return EndofContractOutputACRSerializer(end_contract_output_acrs, many=True).data

    def calculate_average_acr(self, reform_area, year):
        related_end_contract_acrs = EndofContractOutputACR.objects.filter(
            output__reform_area=reform_area,
            year=year,
            deleted=False
        )
        
        return related_end_contract_acrs.aggregate(Avg('end_contract_average_acr'))['end_contract_average_acr__avg'] or 0