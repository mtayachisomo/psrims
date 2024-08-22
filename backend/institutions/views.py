# institutions/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import ( Region, District, Institution, InstitutionUser, Department, UserDepartment, 
                     InstitutionDepartment, Mandate, Mission, Vision, StrategicObjective, ThematicArea, ReformArea,
                     Problem, Justification, Outcome, OutcomeIndicator, Output, OutputIndicator, Activity, FocusArea,
                     ReformStatus, Period, ReformAreaPeriod, ReformFocusArea, Weight, OutputTargets, OutcomeTargets,
                     OutputMov, OutputCSF, OutputInstrument, OutcomeMoV, OutcomeCSF, OutcomeInstrument, OutputBudget,
                     ReformBudget, OrgResponsibility, GovtObligation, IndicatorPeriod, Budget, SpecialReportingPermission,
                     OutputReportingPeriod, OutputActual, OutputReportingPeriod, OutputACR,
                     ReformAreaACR, ReformAreaCriteria, ReformAreaSector, ReformAreaSectorMapping, ReformCategory,
                     ReformCategoryMapping, ThematicAreaACR, OutputProgress, OutputWeights, AnnualOutputACR,
                     AnnualReformAreaACR, EndContractOutputWeights, EndofContractOutputACR, EndContractOutputWeights,
                     EndContractReformAreaACR
                     
)


import logging
import numpy as np
from django.db import IntegrityError, transaction
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, F, Count, Avg, Q, OuterRef, Subquery, Max
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import Lower
from users.permissions import Security  # Import the Security class
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    RegionSerializer, RegionListSerializer, RegionCreateSerializer, RegionUpdateSerializer,
    DistrictSerializer, DistrictListSerializer, DistrictCreateSerializer, DistrictUpdateSerializer,
    InstitutionSerializer, InstitutionListSerializer, InstitutionCreateSerializer, InstitutionUpdateSerializer, 
    InstitutionUserSerializer, UserInstitutionSerializer, DepartmentSerializer, UserDepartmentSerializer,
    UserDepartmentCreateSerializer,
    UserDepartmentUpdateSerializer, InstitutionDepartmentSerializer,
    InstitutionDepartmentCreateSerializer, MandateSerializer, MandateCreateSerializer, MandateUpdateSerializer,
    MissionSerializer, MissionCreateSerializer, MissionUpdateSerializer, VisionSerializer, VisionCreateSerializer, 
    VisionUpdateSerializer, StrategicObjectiveCreateSerializer, StrategicObjectiveResponseSerializer, ThematicAreaCreateSerializer,
    ThematicAreaListSerializer, ThematicAreaSerializer, ReformAreaCreateSerializer, ReformAreaListSerializer, 
    ReformAreaDetailSerializer, ProblemCreateSerializer, ProblemResponseSerializer, JustificationCreateSerializer, JustificationResponseSerializer, CreateOutcomeRequestSerializer, OutcomeResponseSerializer,  CreateOutcomeIndicatorSerializer, OutcomeIndicatorResponseSerializer, CreateOutputRequestSerializer,
    OutputResponseSerializer, CreateOutputIndicatorRequestSerializer, OutputIndicatorResponseSerializer, CreateActivityRequestSerializer,
    ActivityResponseSerializer, FocusAreaCreateSerializer, FocusAreaResponseSerializer, ReformStatusCreateSerializer, ReformStatusResponseSerializer,
    PeriodCreateSerializer, PeriodResponseSerializer, CreateReformAreaPeriodRequestSerializer, ReformAreaPeriodResponseSerializer, 
    ReformFocusAreaCreateSerializer, ReformFocusAreaResponseSerializer, WeightCreateSerializer, 
    WeightResponseSerializer, OutputTargetsCreateSerializer, OutputTargetsResponseSerializer, 
    OutcomeTargetsCreateSerializer, OutcomeTargetsResponseSerializer, OutputMovSerializer, 
    OutputCSFSerializer, OutputInstrumentSerializer, OutputMovSerializer,OutputMovCreateSerializer, OutputMovResponseSerializer, OutcomeMoVSerializer,
    OutcomeCSFSerializer, OutcomeInstrumentSerializer, OutputBudgetCreateSerializer, 
    OutputBudgetResponseSerializer, ReformBudgetCreateSerializer, ReformBudgetResponseSerializer,
    OrgResponsibilitySerializer, GovtObligationSerializer,
    OrgResponsibilityCreateSerializer, GovtObligationCreateSerializer, OrgResponsibilityResponseSerializer, 
    GovtObligationResponseSerializer, IndicatorPeriodCreateSerializer, IndicatorPeriodResponseSerializer, IndicatorPeriodListResponseSerializer,
    BudgetSerializer, OutputCSFCreateSerializer, OutputCSFResponseSerializer, OutputInstrumentCreateSerializer, 
    OutputInstrumentResponseSerializer, OutputCSFSerializer, OutputInstrumentSerializer, OutcomeMoVSerializer, OutcomeCSFSerializer, OutcomeInstrumentSerializer,
    OutcomeMoVCreateSerializer, OutcomeCSFCreateSerializer, OutcomeInstrumentCreateSerializer,
    SpecialReportingPermissionSerializer, OutputActualSerializer, OutputReportingPeriodSerializer,OutputIndicatorReportingResponseSerializer,
    OutputACRSerializer, ReformAreaACRSerializer, ActivityResponseSerializer, ReformAreaCriteriaSerializer,
    ReformAreaSectorSerializer, ReformAreaSectorMappingSerializer, ReformCategorySerializer, ReformCategoryMappingSerializer,
    ThematicAreaACRSerializer, OutputProgressSerializer,OutputWeightsSerializer,  AnnualOutputACRSerializer,
    AnnualReformAreaACRSerializer, EndofContractOutputACRSerializer, EndContractOutputWeightsSerializer,
    EndContractReformAreaACRSerializer



)
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import PermissionDenied  # Import PermissionDenied



# List all regions
class RegionListView(generics.ListAPIView):
    queryset = Region.objects.filter(deleted=False)  # Exclude deleted regions
    serializer_class = RegionListSerializer
    permission_classes = [AllowAny]  # Allow any access, change to IsAuthenticated if needed

# Create a new region
class RegionCreateView(generics.CreateAPIView):
    serializer_class = RegionCreateSerializer
    permission_classes = [AllowAny]  # Allow any access, change to IsAuthenticated if needed

    def perform_create(self, serializer):
        # Perform create logic here if any
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Retrieve a region by ID
class RegionRetrieveView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]  # Allow any access, change to IsAuthenticated if needed

# Update a region
class RegionUpdateView(generics.UpdateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionUpdateSerializer
    permission_classes = [AllowAny]  # Allow any access, change to IsAuthenticated if needed

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# Delete a region
class RegionDeleteView(generics.DestroyAPIView):
    queryset = Region.objects.all()
    permission_classes = [AllowAny]  # Allow any access, change to IsAuthenticated if needed

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True  # Soft delete
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class DistrictListCreate(generics.ListCreateAPIView):
    queryset = District.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DistrictCreateSerializer
        return DistrictListSerializer
    
    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()

class DistrictRetrieve(generics.RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    
class DistrictList(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    
    
    
class DistrictUpdate(generics.UpdateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()
    
class DistrictDestroy(generics.DestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
    

class InstitutionListCreate(generics.ListCreateAPIView):
    queryset = Institution.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InstitutionCreateSerializer
        return InstitutionListSerializer
    
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'  # Use 'limit' as query parameter for page size
    
class InstitutionListView(generics.ListAPIView):
    serializer_class = InstitutionListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10
            
         # Retrieve the user ID
        user_id = self.request.user.id

        # Secure access
        security = Security()
        security.secureAccess('create_user', user_id)

        queryset = Institution.objects.filter(deleted=False)
        if search:
            queryset = queryset.filter(
                Q(institution_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        queryset = queryset.annotate(name_lower=Lower('institution_name')).order_by('name_lower')
        return queryset[skip: skip + limit]

class InstitutionRetrieve(generics.RetrieveAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]

class InstitutionUpdate(generics.UpdateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]
    
class InstitutionDestroy(generics.DestroyAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
    
class InstitutionUserRetrieve(generics.RetrieveAPIView):
    queryset = InstitutionUser.objects.all()
    serializer_class = InstitutionUserSerializer
    permission_classes = [IsAuthenticated]
    
class InstitutionUserUpdate(generics.UpdateAPIView):
    queryset = InstitutionUser.objects.all()
    serializer_class = InstitutionUserSerializer
    permission_classes = [IsAuthenticated]

class InstitutionUserDestroy(generics.DestroyAPIView):
    queryset = InstitutionUser.objects.all()
    serializer_class = InstitutionUserSerializer
    permission_classes = [IsAuthenticated]
    
class UserInstitutionList(generics.ListAPIView):
    serializer_class = UserInstitutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(deleted=False)

class InstitutionUserCreate(generics.CreateAPIView):
    queryset = InstitutionUser.objects.all()
    serializer_class = InstitutionUserSerializer
    permission_classes = [IsAuthenticated]
    
class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Use the custom pagination class

    def get_queryset(self):
        # Retrieve query parameters for pagination, skip, limit, and search
        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        # Ensure that skip and limit are integers
        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10

        # Retrieve the user ID
        user_id = self.request.user.id

        # Secure access
        security = Security()
        security.secureAccess('create_user', user_id)

        # Perform filtering and searching
        queryset = Department.objects.filter(deleted=False)
        if search:
            queryset = queryset.filter(
                Q(department_name__icontains=search)
            )

        # Apply pagination and return the queryset
        return queryset[skip: skip + limit]
    
class DepartmentRetrieveView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class DepartmentUpdateView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentDeleteView(generics.DestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
class UserDepartmentListView(generics.ListAPIView):
    queryset = UserDepartment.objects.filter(deleted=False)
    serializer_class = UserDepartmentSerializer
    permission_classes = [IsAuthenticated]

class UserDepartmentDetailView(generics.RetrieveAPIView):
    queryset = UserDepartment.objects.filter(deleted=False)
    serializer_class = UserDepartmentSerializer
    permission_classes = [IsAuthenticated]

class UserDepartmentCreateView(generics.CreateAPIView):
    queryset = UserDepartment.objects.all()
    serializer_class = UserDepartmentCreateSerializer
    permission_classes = [IsAuthenticated]

class UserDepartmentUpdateView(generics.UpdateAPIView):
    queryset = UserDepartment.objects.filter(deleted=False)
    serializer_class = UserDepartmentUpdateSerializer
    permission_classes = [IsAuthenticated]

class UserDepartmentDeleteView(generics.DestroyAPIView):
    queryset = UserDepartment.objects.filter(deleted=False)
    serializer_class = UserDepartmentSerializer
    permission_classes = [IsAuthenticated]
    
# InstitutionDepartment views
class InstitutionDepartmentListView(generics.ListAPIView):
    queryset = InstitutionDepartment.objects.filter(deleted=False)
    serializer_class = InstitutionDepartmentSerializer
    permission_classes = [IsAuthenticated]

class InstitutionDepartmentDetailView(generics.RetrieveAPIView):
    queryset = InstitutionDepartment.objects.filter(deleted=False)
    serializer_class = InstitutionDepartmentSerializer
    permission_classes = [IsAuthenticated]

class InstitutionDepartmentCreateView(generics.CreateAPIView):
    queryset = InstitutionDepartment.objects.all()
    serializer_class = InstitutionDepartmentCreateSerializer
    permission_classes = [IsAuthenticated]
    
# InstitutionDepartment views
class InstitutionDepartmentListView(generics.ListAPIView):
    queryset = InstitutionDepartment.objects.filter(deleted=False)
    serializer_class = InstitutionDepartmentSerializer
    permission_classes = [IsAuthenticated]

class InstitutionDepartmentDetailView(generics.RetrieveAPIView):
    queryset = InstitutionDepartment.objects.filter(deleted=False)
    serializer_class = InstitutionDepartmentSerializer
    permission_classes = [IsAuthenticated]

class InstitutionDepartmentCreateView(generics.CreateAPIView):
    queryset = InstitutionDepartment.objects.all()
    serializer_class = InstitutionDepartmentCreateSerializer
    permission_classes = [IsAuthenticated]
    
class MandateListCreateView(generics.ListCreateAPIView):
    queryset = Mandate.objects.filter(deleted=False)
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MandateCreateSerializer
        return MandateSerializer

    def perform_create(self, serializer):
        mandate_data = serializer.validated_data
        mandate = mandate_data.get('mandate')  # Corrected field name
        
        # Check if a mandate with the same text already exists
        existing_mandate = Mandate.objects.filter(mandate=mandate, deleted=False).first()  # Corrected field name
        
        if existing_mandate:
            # Update the existing mandate
            existing_mandate.deleted = False  # Set deleted to False
            existing_mandate.save()
            return existing_mandate
        else:
            # Create a new mandate
            # Secure access
            user_id = self.request.user.id
            security = Security()
            security.secureAccess("create_user", user_id)
            
            serializer.save()

class MandateRetrieveView(generics.RetrieveAPIView):
    queryset = Mandate.objects.filter(deleted=False)
    serializer_class = MandateSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mandate_by_institution(request, institution_id):
    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    mandate = Mandate.objects.filter(institution=institution, deleted=False).last()
    if not mandate:
        return Response({"error": "Mandate not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = MandateSerializer(mandate)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

class MandateListView(generics.ListAPIView):
    queryset = Mandate.objects.all()  # This already retrieves all mandates
    serializer_class = MandateSerializer
    permission_classes = [IsAuthenticated]
    
class DeletedMandateListView(generics.ListAPIView):
    queryset = Mandate.objects.filter(deleted=True)
    serializer_class = MandateSerializer
    
class MandateUpdateView(generics.UpdateAPIView):
    queryset = Mandate.objects.filter(deleted=False)
    serializer_class = MandateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Secure access
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()

class MandateDeleteView(generics.DestroyAPIView):
    queryset = Mandate.objects.filter(deleted=False)
    serializer_class = MandateSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # Secure access
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        instance.deleted = True
        instance.save()
        
class MissionListCreateView(generics.ListCreateAPIView):
    queryset = Mission.objects.filter(deleted=False)
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MissionCreateSerializer
        return MissionSerializer

    def perform_create(self, serializer):
        mission_data = serializer.validated_data
        mission = mission_data.get('mission')
        
        # Check if a mission with the same mission already exists
        existing_mission = Mission.objects.filter(mission=mission, deleted=False).first()
        
        if existing_mission:
            # Update the existing mission
            existing_mission.deleted = False  # Set deleted to False
            existing_mission.save()
            return existing_mission
        else:
            # Create a new mission
            # Secure access
            user_id = self.request.user.id
            security = Security()
            security.secureAccess("create_user", user_id)
            
            serializer.save()

class MissionRetrieveView(generics.RetrieveAPIView):
    queryset = Mission.objects.filter(deleted=False)
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mission_by_institution(request, institution_id):
    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    
    mission = Mission.objects.filter(institution=institution, deleted=False).last()
    if not mission:
        return Response({"error": "Mission not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = MissionSerializer(mission)
    return Response(response_serializer.data, status=status.HTTP_200_OK)
    
class MissionListView(generics.ListAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]
    
class DeletedMissionListView(generics.ListAPIView):
    queryset = Mission.objects.filter(deleted=True)
    serializer_class = MissionSerializer
    
class MissionUpdateView(generics.UpdateAPIView):
    queryset = Mission.objects.filter(deleted=False)
    serializer_class = MissionUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()

class MissionDeleteView(generics.DestroyAPIView):
    queryset = Mission.objects.filter(deleted=False)
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        instance.deleted = True
        instance.save()
        

class VisionListCreateView(generics.ListCreateAPIView):
    queryset = Vision.objects.filter(deleted=False)
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VisionCreateSerializer
        return VisionSerializer

    def perform_create(self, serializer):
        vision_data = serializer.validated_data
        vision = vision_data.get('vision')  # Corrected field name
        
        # Check if a vision with the same text already exists
        existing_vision = Vision.objects.filter(vision=vision, deleted=False).first()  # Corrected field name
        
        if existing_vision:
            # Update the existing vision
            existing_vision.deleted = False  # Set deleted to False
            existing_vision.save()
            return existing_vision
        else:
            # Create a new vision
            # Secure access
            user_id = self.request.user.id
            security = Security()
            security.secureAccess("create_user", user_id)
            
            serializer.save()


class VisionRetrieveView(generics.RetrieveAPIView):
    queryset = Vision.objects.filter(deleted=False)
    serializer_class = VisionSerializer
    permission_classes = [IsAuthenticated]
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vision_by_institution(request, institution_id):
    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    
    vision = Vision.objects.filter(institution=institution, deleted=False).last()
    if not vision:
        return Response({"error": "Vision not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = VisionSerializer(vision)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

    
class VisionListView(generics.ListAPIView):
    queryset = Vision.objects.all()
    serializer_class = VisionSerializer
    permission_classes = [IsAuthenticated]
    
class DeletedVisionListView(generics.ListAPIView):
    queryset = Vision.objects.filter(deleted=True)
    serializer_class = VisionSerializer
    
class VisionUpdateView(generics.UpdateAPIView):
    queryset = Vision.objects.filter(deleted=False)
    serializer_class = VisionUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()

class VisionDeleteView(generics.DestroyAPIView):
    queryset = Vision.objects.filter(deleted=False)
    serializer_class = VisionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        instance.deleted = True
        instance.save()
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_institution_strategic_objectives(request):
    serializer = StrategicObjectiveCreateSerializer(data=request.data)
    if serializer.is_valid():
        institution_id = serializer.validated_data['institution_id']
        objectives = serializer.validated_data['objectives']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        # Get the institution instance
        try:
            institution = Institution.objects.get(id=institution_id)
        except Institution.DoesNotExist:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
        
        existing_objectives = StrategicObjective.objects.filter(institution=institution)
        existing_objectives_ids = set(obj.id for obj in existing_objectives)
        
        new_objectives = []
        for objective_text in objectives:
            # Check if the objective already exists for the institution
            existing_objective = existing_objectives.filter(objective=objective_text).first()
            if existing_objective:
                # Update the existing objective only if it's deleted
                if existing_objective.deleted:
                    existing_objective.deleted = False
                    existing_objective.save()
                new_objectives.append(existing_objective)
            else:
                # Create a new objective
                new_objective = StrategicObjective.objects.create(
                    institution=institution,
                    objective=objective_text,
                    deleted=False
                )
                new_objectives.append(new_objective)
        
        # Set deleted to true for replaced objectives
        replaced_objectives = existing_objectives.exclude(id__in=[obj.id for obj in new_objectives])
        replaced_objectives.update(deleted=True)
        
        response_serializer = StrategicObjectiveResponseSerializer(new_objectives, many=True)
        return Response({"message": "Strategic Objectives created/updated successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_strategic_objectives(request):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    objectives = StrategicObjective.objects.all()
    response_serializer = StrategicObjectiveResponseSerializer(objectives, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_strategic_objectives_by_institution(request, institution_id):
    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    objectives = StrategicObjective.objects.filter(institution=institution, deleted=False)
    response_serializer = StrategicObjectiveResponseSerializer(objectives, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_strategic_objectives(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    objectives = StrategicObjective.objects.filter(deleted=False)
    response_serializer = StrategicObjectiveResponseSerializer(objectives, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_strategic_objectives_by_institution(request, institution_id):
    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    

    objectives = StrategicObjective.objects.filter(institution=institution, deleted=False)
    response_serializer = StrategicObjectiveResponseSerializer(objectives, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_strategic_objective_endpoint(request, objective_id):
    try:
        objective = StrategicObjective.objects.get(id=objective_id)
    except StrategicObjective.DoesNotExist:
        return Response({"error": "Strategic Objective not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = StrategicObjectiveResponseSerializer(objective, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_strategic_objective_endpoint(request, objective_id):
    try:
        objective = StrategicObjective.objects.get(id=objective_id)
    except StrategicObjective.DoesNotExist:
        return Response({"error": "Strategic Objective not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    objective.delete()
    return Response({"message": "Strategic Objective deleted successfully"}, status=status.HTTP_200_OK)

class ThematicAreaListCreate(generics.ListCreateAPIView):
    queryset = ThematicArea.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ThematicAreaCreateSerializer
        return ThematicAreaListSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            # Handling bulk creation
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Handling single creation
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Check if the user has the 'create_thematic_area' permission
        user_id = self.request.user.id
        security = Security()
        try:
            security.secureAccess("create_user", user_id)
        except PermissionDenied as e:
            raise PermissionDenied(str(e))

        serializer.save()

class ThematicAreaListView(generics.ListAPIView):
    serializer_class = ThematicAreaListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get('search', '')

        # Retrieve the user ID
        user_id = self.request.user.id

        # Secure access
        # Replace with your actual security logic
        security = Security()
        security.secureAccess('create_user', user_id)

        queryset = ThematicArea.objects.filter(deleted=False)
        if search:
            queryset = queryset.filter(
                Q(thematic_area__icontains=search) |
                Q(description__icontains=search)
            )

        queryset = queryset.annotate(name_lower=Lower('thematic_area')).order_by('name_lower')
        return queryset

class ThematicAreaRetrieve(generics.RetrieveAPIView):
    queryset = ThematicArea.objects.filter(deleted=False)
    serializer_class = ThematicAreaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        # Pass the request context to the serializer
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    
class ThematicAreaUpdate(generics.UpdateAPIView):
    queryset = ThematicArea.objects.filter(deleted=False)
    serializer_class = ThematicAreaSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()

class ThematicAreaDestroy(generics.DestroyAPIView):
    queryset = ThematicArea.objects.filter(deleted=False)
    serializer_class = ThematicAreaSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
        
class ReformAreaListCreate(generics.ListCreateAPIView):
    queryset = ReformArea.objects.filter(deleted=False)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReformAreaCreateSerializer
        return ReformAreaListSerializer

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        # Extract data from the request
        reform_area_data = {
            'objective_id': self.request.data.get('objective'),
            'institution_id': self.request.data.get('institution'),
            'thematic_area_id': self.request.data.get('thematic_area'),
            'reform_area': self.request.data.get('reform_area'),
            'year': self.request.data.get('year')
        }
        
        # Check if a record with the given fields already exists (excluding the year)
        existing_record = ReformArea.objects.filter(
            objective_id=reform_area_data['objective_id'],
            institution_id=reform_area_data['institution_id'],
            thematic_area_id=reform_area_data['thematic_area_id'],
            reform_area=reform_area_data['reform_area'],
            deleted=False  # Ensure the record is not marked as deleted
        ).first()
        
        if existing_record:
            # Update the existing record's year and timestamp
            existing_record.year = reform_area_data['year']
            existing_record.updated_at = timezone.now()
            existing_record.save()
            # Return the updated record
            serializer.instance = existing_record
        else:
            # Create a new record
            serializer.save()
    
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReformAreaListView(generics.ListAPIView):
    serializer_class = ReformAreaListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10
            
            
         # Retrieve the user ID
        user_id = self.request.user.id

        # Secure access
        security = Security()
        security.secureAccess('create_user', user_id)

        queryset = ReformArea.objects.filter(deleted=False)
        if search:
            queryset = queryset.filter(reform_area__icontains=search)

        return queryset[skip: skip + limit]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_area_by_id(request, reform_area_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    reform_area = get_object_or_404(ReformArea, id=reform_area_id)
    serializer = ReformAreaDetailSerializer(reform_area)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_areas_by_latest_year_and_institution(request, institution_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    # Query the latest year for the given institution ID
    latest_year = ReformArea.objects.filter(institution_id=institution_id, deleted=False).order_by('-year').values_list('year', flat=True).first()

    if latest_year is None:
        return Response({"message": "No reform areas found for the given institution"}, status=status.HTTP_404_NOT_FOUND)

    # Query all reform areas for the institution with the latest year
    reform_areas = ReformArea.objects.filter(
        institution_id=institution_id,
        year=latest_year,
        deleted=False
    )
    
    serializer = ReformAreaListSerializer(reform_areas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class ReformAreaUpdate(generics.UpdateAPIView):
    queryset = ReformArea.objects.filter(deleted=False)
    serializer_class = ReformAreaListSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        serializer.save()

class ReformAreaDestroy(generics.DestroyAPIView):
    queryset = ReformArea.objects.filter(deleted=False)
    serializer_class = ReformAreaListSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_problems(request):
    serializer = ProblemCreateSerializer(data=request.data)
    if serializer.is_valid():
        reform_area_id = serializer.validated_data['reform_area_id']
        problems = serializer.validated_data['problems']
        
        try:
            reform_area = ReformArea.objects.get(id=reform_area_id)
        except ReformArea.DoesNotExist:
            return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
    
        new_problems = []
        for problem_text in problems:
            new_problem = Problem.objects.create(
                reform_area_id=reform_area_id,
                problem=problem_text,
                deleted=False
            )
            new_problems.append(new_problem)
        
        response_serializer = ProblemResponseSerializer(new_problems, many=True)
        return Response({"message": "Problems created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_problems(request):
    problems = Problem.objects.filter(deleted=False)
    response_serializer = ProblemResponseSerializer(problems, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_problems_by_reform_area(request, reform_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    try:
        reform_area = ReformArea.objects.get(id=reform_area_id)
    except ReformArea.DoesNotExist:
        return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    problems = Problem.objects.filter(reform_area=reform_area, deleted=False)
    response_serializer = ProblemResponseSerializer(problems, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_problem_by_id(request, problem_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    try:
        problem = Problem.objects.get(id=problem_id, deleted=False)
    except Problem.DoesNotExist:
        return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = ProblemResponseSerializer(problem)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_problem(request, problem_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProblemResponseSerializer(problem, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_problem(request, problem_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    try:
        problem = Problem.objects.get(id=problem_id)
        problem.deleted = True
        problem.save()
        return Response({"message": "Problem deleted successfully"}, status=status.HTTP_200_OK)
    except Problem.DoesNotExist:
        return Response({"error": "Problem not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_justifications(request):
    serializer = JustificationCreateSerializer(data=request.data)
    if serializer.is_valid():
        reform_area_id = serializer.validated_data['reform_area_id']
        justifications = serializer.validated_data['justifications']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        try:
            reform_area = ReformArea.objects.get(id=reform_area_id)
        except ReformArea.DoesNotExist:
            return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_justifications = []
        for justification_text in justifications:
            new_justification = Justification.objects.create(
                reform_area_id=reform_area_id,
                justification=justification_text,
                deleted=False
            )
            new_justifications.append(new_justification)
        
        response_serializer = JustificationResponseSerializer(new_justifications, many=True)
        return Response({"message": "Justifications created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_justifications(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    justifications = Justification.objects.filter(deleted=False)
    response_serializer = JustificationResponseSerializer(justifications, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_justifications_by_reform_area(request, reform_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
     
    try:
        reform_area = ReformArea.objects.get(id=reform_area_id)
    except ReformArea.DoesNotExist:
        return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    justifications = Justification.objects.filter(reform_area=reform_area, deleted=False)
    response_serializer = JustificationResponseSerializer(justifications, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_justification_by_id(request, justification_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        justification = Justification.objects.get(id=justification_id, deleted=False)
    except Justification.DoesNotExist:
        return Response({"error": "Justification not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = JustificationResponseSerializer(justification)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_justification(request, justification_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        justification = Justification.objects.get(id=justification_id)
    except Justification.DoesNotExist:
        return Response({"error": "Justification not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = JustificationResponseSerializer(justification, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_justification(request, justification_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        justification = Justification.objects.get(id=justification_id)
        justification.deleted = True
        justification.save()
        return Response({"message": "Justification deleted successfully"}, status=status.HTTP_200_OK)
    except Justification.DoesNotExist:
        return Response({"error": "Justification not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outcomes(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = CreateOutcomeRequestSerializer(data=request.data)
    if serializer.is_valid():
        outcomes_data = serializer.validated_data.get('outcomes')
        reform_area = serializer.validated_data.get('reform_area')
        
        created_outcomes = []
        for outcome_text in outcomes_data:
            outcome = Outcome.objects.create(reform_area=reform_area, outcomes=outcome_text)
            created_outcomes.append(outcome)
        
        # Serialize the created outcomes using OutcomeResponseSerializer
        response_serializer = OutcomeResponseSerializer(created_outcomes, many=True)
        return Response({"message": "Outcomes created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'pages': self.page.paginator.num_pages,
            'data': data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_outcomes(request):
    pagination_class = CustomPagination()
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')

    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    queryset = Outcome.objects.filter(deleted=False)
    if search:
        queryset = queryset.filter(outcomes__icontains=search)

    # Ensure the queryset is ordered to avoid UnorderedObjectListWarning
    queryset = queryset.order_by('id')

    paginated_queryset = pagination_class.paginate_queryset(queryset, request)
    
    # Serialize the outcomes along with nested outcome indicators, outputs, and activities
    response_data = []
    for outcome in paginated_queryset:
        outcome_data = OutcomeResponseSerializer(outcome).data
        outcome_data['outputs'] = []
        for output in outcome.outputs.all():
            output_data = OutputResponseSerializer(output).data
            output_data['output_indicators'] = OutputIndicatorResponseSerializer(output.output_indicators.all(), many=True).data
            output_data['activities'] = ActivityResponseSerializer(output.activities.all(), many=True).data
            outcome_data['outputs'].append(output_data)
        response_data.append(outcome_data)

    return pagination_class.get_paginated_response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcomes_by_id(request, outcome_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        outcome = Outcome.objects.get(id=outcome_id, deleted=False)
    except Outcome.DoesNotExist:
        return Response({"error": "Outcome not found"}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the outcome along with nested outcome indicators, outputs, and activities
    outcome_data = OutcomeResponseSerializer(outcome).data
    outcome_data['outputs'] = []
    for output in outcome.outputs.all():
        output_data = OutputResponseSerializer(output).data
        output_data['output_indicators'] = OutputIndicatorResponseSerializer(output.output_indicators.all(), many=True).data
        output_data['activities'] = ActivityResponseSerializer(output.activities.all(), many=True).data
        outcome_data['outputs'].append(output_data)

    return Response(outcome_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcomes_by_reform_area(request, reform_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_area = ReformArea.objects.get(id=reform_area_id, deleted=False)
    except ReformArea.DoesNotExist:
        return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)

    outcomes = Outcome.objects.filter(reform_area=reform_area, deleted=False)
    serializer = OutcomeResponseSerializer(outcomes, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_outcome(request, outcome_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        outcome = Outcome.objects.get(id=outcome_id)
    except Outcome.DoesNotExist:
        return Response({"error": "Outcome not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    if 'outcomes' in data and isinstance(data['outcomes'], list) and len(data['outcomes']) > 0:
        data['outcomes'] = data['outcomes'][0]  # Ensure outcomes is a string from the first item of the array

    serializer = OutcomeResponseSerializer(outcome, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_outcome(request, outcome_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        outcome = Outcome.objects.get(id=outcome_id)
        outcome.deleted = True
        outcome.save()
        return Response({"message": "Outcome deleted successfully"}, status=status.HTTP_200_OK)
    except Outcome.DoesNotExist:
        return Response({"error": "Outcome not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deleted_outcomes(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    deleted_outcomes = Outcome.objects.filter(deleted=True)
    response_serializer = OutcomeResponseSerializer(deleted_outcomes, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outcome_indicators(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = CreateOutcomeIndicatorSerializer(data=request.data)
    if serializer.is_valid():
        indicators_data = serializer.validated_data.get('indicators')
        outcome = serializer.validated_data.get('outcome')
        
        created_indicators = []
        for indicator_text in indicators_data:
            indicator = OutcomeIndicator.objects.create(outcome=outcome, indicator=indicator_text)
            created_indicators.append(indicator)
        
        # Serialize the created indicators using OutcomeIndicatorResponseSerializer
        response_serializer = OutcomeIndicatorResponseSerializer(created_indicators, many=True)
        return Response({"message": "Outcome Indicators created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_outcome_indicators(request):
    
    pagination_class = CustomPagination()
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')

    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    queryset = OutcomeIndicator.objects.filter(deleted=False)
    if search:
        queryset = queryset.filter(indicator__icontains=search)

    paginated_queryset = pagination_class.paginate_queryset(queryset, request)
    response_serializer = OutcomeIndicatorResponseSerializer(paginated_queryset, many=True)
    return pagination_class.get_paginated_response(response_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcome_indicator_by_id(request, indicator_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        indicator = OutcomeIndicator.objects.get(id=indicator_id, deleted=False)
    except OutcomeIndicator.DoesNotExist:
        return Response({"error": "Outcome Indicator not found"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = OutcomeIndicatorResponseSerializer(indicator)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_outcome_indicator(request, indicator_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        indicator = OutcomeIndicator.objects.get(id=indicator_id)
    except OutcomeIndicator.DoesNotExist:
        return Response({"error": "Outcome Indicator not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutcomeIndicatorResponseSerializer(indicator, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_outcome_indicator(request, indicator_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
        
    try:
        indicator = OutcomeIndicator.objects.get(id=indicator_id)
        indicator.deleted = True
        indicator.save()
        return Response({"message": "Outcome Indicator deleted successfully"}, status=status.HTTP_200_OK)
    except OutcomeIndicator.DoesNotExist:
        return Response({"error": "Outcome Indicator not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deleted_outcome_indicators(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    deleted_indicators = OutcomeIndicator.objects.filter(deleted=True)
    response_serializer = OutcomeIndicatorResponseSerializer(deleted_indicators, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outputs(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    
    serializer = CreateOutputRequestSerializer(data=request.data)
    if serializer.is_valid():
        outputs_data = serializer.validated_data.get('outputs')
        reform_area = serializer.validated_data.get('reform_area')
        outcome = serializer.validated_data.get('outcome')

        created_outputs = []
        for output_text in outputs_data:
            output = Output.objects.create(reform_area=reform_area, outcome=outcome, output=output_text)
            created_outputs.append(output)

        # Serialize the created outputs using OutputResponseSerializer
        response_serializer = OutputResponseSerializer(created_outputs, many=True)
        return Response({"message": "Outputs created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_by_id(request, output_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id) 
    
    try:
        output = Output.objects.get(id=output_id, deleted=False)
    except Output.DoesNotExist:
        return Response({"error": "Output not found"}, status=status.HTTP_404_NOT_FOUND)

    output_data = OutputResponseSerializer(output).data
    output_data['output_indicators'] = OutputIndicatorResponseSerializer(output.output_indicators.all(), many=True, context={'request': request}).data
    output_data['activities'] = ActivityResponseSerializer(output.activities.all(), many=True).data

    return Response(output_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_outputs(request):
    pagination_class = CustomPagination()
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')

    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    queryset = Output.objects.filter(deleted=False)
    if search:
        queryset = queryset.filter(output__icontains=search)

    paginated_queryset = pagination_class.paginate_queryset(queryset, request)

    # Serialize the outputs along with nested output indicators and activities
    response_data = []
    for output in paginated_queryset:
        output_data = OutputResponseSerializer(output).data
        output_data['output_indicators'] = OutputIndicatorResponseSerializer(output.output_indicators.all(), many=True).data
        output_data['activities'] = ActivityResponseSerializer(output.activities.all(), many=True).data
        response_data.append(output_data)

    return pagination_class.get_paginated_response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outputs_by_outcome_id(request, outcome_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        outcome = Outcome.objects.get(id=outcome_id, deleted=False)
    except Outcome.DoesNotExist:
        return Response({"error": "Outcome not found"}, status=status.HTTP_404_NOT_FOUND)

    outputs = Output.objects.filter(outcome=outcome, deleted=False)
    serializer = OutputResponseSerializer(outputs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outputs_by_reform_area_id(request, reform_area_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_area = ReformArea.objects.get(id=reform_area_id, deleted=False)
    except ReformArea.DoesNotExist:
        return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get the latest active output reporting period
    current_date = timezone.now().date()
    active_period = OutputReportingPeriod.objects.filter(start_date__lte=current_date, end_date__gte=current_date, is_active=True).first()
    
    if not active_period:
        return Response({"error": "No active output reporting period found"}, status=status.HTTP_404_NOT_FOUND)

    # Debug: Check active period details
    print(f"Active Period: {active_period.output_label} from {active_period.start_date} to {active_period.end_date}")

    # Filter outputs based on the latest active period
    outputs = Output.objects.filter(reform_area=reform_area, deleted=False)
    filtered_outputs = []

    for output in outputs:
        indicators = output.output_indicators.filter(deleted=False)
        valid_indicators = []

        for indicator in indicators:
            # Check if there are output targets for the current year in the active period
            targets = indicator.output_targets.filter(year=current_date.year).first()
            if not targets:
                continue

            # Debug: Print target details
            print(f"Indicator: {indicator.id}, Targets: Q1={targets.Q1_target}, Q2={targets.Q2_target}, Q3={targets.Q3_target}, Q4={targets.Q4_target}")

            # Check if the current quarter has targets greater than 0
            if (
                (active_period.output_label == 'Q1' and targets.Q1_target > 0) or
                (active_period.output_label == 'Q2' and targets.Q2_target > 0) or
                (active_period.output_label == 'Q3' and targets.Q3_target > 0) or
                (active_period.output_label == 'Q4' and targets.Q4_target > 0)
            ):
                valid_indicators.append(indicator)

        if valid_indicators:
            filtered_outputs.append({
                "id": output.id,
                "output": output.output,  # Adjust the field name as per your actual model
                "updated_at": output.updated_at,
                "created_at": output.created_at,
                "deleted": output.deleted,
                "output_indicators": OutputIndicatorResponseSerializer(valid_indicators, many=True).data,
                "activities": ActivityResponseSerializer(output.activities.filter(deleted=False), many=True).data  # Assuming ActivitySerializer is defined
            })

    return Response(filtered_outputs)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_no_targeted_outputs_by_reform_area_id(request, reform_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_area = ReformArea.objects.get(id=reform_area_id, deleted=False)
    except ReformArea.DoesNotExist:
        return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)

    outputs = Output.objects.filter(reform_area=reform_area, deleted=False)
    serializer = OutputResponseSerializer(outputs, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_output(request, output_id):
    try:
        output = Output.objects.get(id=output_id)
    except Output.DoesNotExist:
        return Response({"error": f"Output with id {output_id} not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    if 'output' in data and isinstance(data['output'], list) and len(data['output']) > 0:
        data['output'] = data['output'][0]  # Ensure output is a string from the first item of the array

    serializer = OutputResponseSerializer(instance=output, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_output(request, output_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        output = Output.objects.get(id=output_id)
        output.deleted = True
        output.save()
        return Response({"message": "Output deleted successfully"}, status=status.HTTP_200_OK)
    except Output.DoesNotExist:
        return Response({"error": "Output not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deleted_outputs(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    deleted_outputs = Output.objects.filter(deleted=True)
    response_serializer = OutputResponseSerializer(deleted_outputs, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_indicators(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = CreateOutputIndicatorRequestSerializer(data=request.data)
    if serializer.is_valid():
        indicators_data = serializer.validated_data.get('indicators')
        output = serializer.validated_data.get('output')
        
        created_indicators = []
        for indicator_text in indicators_data:
            indicator = OutputIndicator.objects.create(output=output, indicator=indicator_text)
            created_indicators.append(indicator)
        
        # Serialize the created indicators using OutputIndicatorResponseSerializer
        response_serializer = OutputIndicatorResponseSerializer(created_indicators, many=True)
        return Response({"message": "Output Indicators created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_output_indicators(request):
    
    pagination_class = CustomPagination()
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')

    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    queryset = OutputIndicator.objects.filter(deleted=False)
    if search:
        queryset = queryset.filter(indicator__icontains=search)

    paginated_queryset = pagination_class.paginate_queryset(queryset, request)
    response_serializer = OutputIndicatorResponseSerializer(paginated_queryset, many=True)
    return pagination_class.get_paginated_response(response_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_indicator_by_id(request, indicator_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        indicator = OutputIndicator.objects.get(id=indicator_id, deleted=False)
    except OutputIndicator.DoesNotExist:
        return Response({"error": "Output Indicator not found"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = OutputIndicatorResponseSerializer(indicator)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_output_indicator(request, indicator_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        indicator = OutputIndicator.objects.get(id=indicator_id)
    except OutputIndicator.DoesNotExist:
        return Response({"error": "Output Indicator not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutputIndicatorResponseSerializer(indicator, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_output_indicator(request, indicator_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        indicator = OutputIndicator.objects.get(id=indicator_id)
        indicator.deleted = True
        indicator.save()
        return Response({"message": "Output Indicator deleted successfully"}, status=status.HTTP_200_OK)
    except OutputIndicator.DoesNotExist:
        return Response({"error": "Output Indicator not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deleted_output_indicators(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    deleted_indicators = OutputIndicator.objects.filter(deleted=True)
    response_serializer = OutputIndicatorResponseSerializer(deleted_indicators, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_activities(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = CreateActivityRequestSerializer(data=request.data)
    if serializer.is_valid():
        activities_data = serializer.validated_data.get('activities')
        output = serializer.validated_data.get('output')
        
        created_activities = []
        for activity_text in activities_data:
            activity = Activity.objects.create(output=output, activity=activity_text)
            created_activities.append(activity)
        
        # Serialize the created activities using ActivityResponseSerializer
        response_serializer = ActivityResponseSerializer(created_activities, many=True)
        return Response({"message": "Activities created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_activities(request):
    pagination_class = CustomPagination()
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '')

    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    queryset = Activity.objects.filter(deleted=False)
    if search:
        queryset = queryset.filter(activity__icontains=search)

    paginated_queryset = pagination_class.paginate_queryset(queryset, request)
    response_serializer = ActivityResponseSerializer(paginated_queryset, many=True)
    return pagination_class.get_paginated_response(response_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_activity_by_id(request, activity_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    try:
        activity = Activity.objects.get(id=activity_id, deleted=False)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = ActivityResponseSerializer(activity)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_activity(request, activity_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ActivityResponseSerializer(activity, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_activity(request, activity_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        activity = Activity.objects.get(id=activity_id)
        activity.deleted = True
        activity.save()
        return Response({"message": "Activity deleted successfully"}, status=status.HTTP_200_OK)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deleted_activities(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    deleted_activities = Activity.objects.filter(deleted=True)
    response_serializer = ActivityResponseSerializer(deleted_activities, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_budget(request):
    serializer = BudgetSerializer(data=request.data)
    if serializer.is_valid():
        budget = serializer.save()
        response_serializer = BudgetSerializer(budget)
        return Response({"message": "Budget created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_budgets(request):
    budgets = Budget.objects.filter(deleted=False)
    serializer = BudgetSerializer(budgets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_budget_by_id(request, pk):
    budget = get_object_or_404(Budget, pk=pk, deleted=False)
    serializer = BudgetSerializer(budget)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_budget_by_activity_id(request, activity_id):
    budgets = Budget.objects.filter(activity_id=activity_id, deleted=False)
    serializer = BudgetSerializer(budgets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, deleted=False)
    serializer = BudgetSerializer(budget, data=request.data)
    if serializer.is_valid():
        updated_budget = serializer.save()
        response_serializer = BudgetSerializer(updated_budget)
        return Response({"message": "Budget updated successfully", "data": response_serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, deleted=False)
    budget.deleted = True
    budget.save()
    return Response({"message": "Budget deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_focus_areas(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = FocusAreaCreateSerializer(data=request.data)
    if serializer.is_valid():
        thematic_area_id = serializer.validated_data['thematic_area_id']
        focus_areas = serializer.validated_data['focus_areas']

        try:
            thematic_area = ThematicArea.objects.get(id=thematic_area_id)
        except ThematicArea.DoesNotExist:
            return Response({"error": "Thematic Area not found"}, status=status.HTTP_404_NOT_FOUND)

        new_focus_areas = []
        for focus_area_text in focus_areas:
            new_focus_area = FocusArea.objects.create(
                thematic_area_id=thematic_area_id,
                focus_area=focus_area_text,
                deleted=False
            )
            new_focus_areas.append(new_focus_area)

        response_serializer = FocusAreaResponseSerializer(new_focus_areas, many=True)
        return Response({"message": "Focus Areas created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_focus_areas(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    focus_areas = FocusArea.objects.filter(deleted=False)
    response_serializer = FocusAreaResponseSerializer(focus_areas, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_focus_area_by_id(request, focus_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        focus_area = FocusArea.objects.get(id=focus_area_id, deleted=False)
    except FocusArea.DoesNotExist:
        return Response({"error": "Focus Area not found"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = FocusAreaResponseSerializer(focus_area)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_focus_area(request, focus_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        focus_area = FocusArea.objects.get(id=focus_area_id)
    except FocusArea.DoesNotExist:
        return Response({"error": "Focus Area not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FocusAreaResponseSerializer(focus_area, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_focus_areas_by_thematic_area(request, thematic_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        thematic_area = ThematicArea.objects.get(id=thematic_area_id)
    except ThematicArea.DoesNotExist:
        return Response({"error": "Thematic Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    focus_areas = FocusArea.objects.filter(thematic_area=thematic_area, deleted=False)
    response_serializer = FocusAreaResponseSerializer(focus_areas, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_focus_area(request, focus_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        focus_area = FocusArea.objects.get(id=focus_area_id)
        focus_area.deleted = True
        focus_area.save()
        return Response({"message": "Focus Area deleted successfully"}, status=status.HTTP_200_OK)
    except FocusArea.DoesNotExist:
        return Response({"error": "Focus Area not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reform_statuses(request):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = ReformStatusCreateSerializer(data=request.data)
    if serializer.is_valid():
        reform_area_id = serializer.validated_data['reform_area_id']
        new_reform_status = serializer.validated_data['reform_status']

        try:
            reform_area = ReformArea.objects.get(id=reform_area_id)
        except ReformArea.DoesNotExist:
            return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)

        new_reform_status_instance = ReformStatus.objects.create(
            reform_area_id=reform_area_id,
            new_reform_status=new_reform_status,
            deleted=False
        )

        response_serializer = ReformStatusResponseSerializer(new_reform_status_instance)
        return Response({"message": "Reform Status created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reform_statuses(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    reform_statuses = ReformStatus.objects.filter(deleted=False)
    response_serializer = ReformStatusResponseSerializer(reform_statuses, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_status_by_id(request, reform_status_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_status = ReformStatus.objects.get(id=reform_status_id, deleted=False)
    except ReformStatus.DoesNotExist:
        return Response({"error": "Reform Status not found"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = ReformStatusResponseSerializer(reform_status)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_status_by_reform_area(request, reform_area_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_status = ReformStatus.objects.get(reform_area_id=reform_area_id, deleted=False)
    except ReformStatus.DoesNotExist:
        return Response({"error": "Reform Status not found for the specified Reform Area"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = ReformStatusResponseSerializer(reform_status)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reform_status(request, reform_status_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_status = ReformStatus.objects.get(id=reform_status_id)
    except ReformStatus.DoesNotExist:
        return Response({"error": "Reform Status not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReformStatusResponseSerializer(reform_status, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reform_status(request, reform_status_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_status = ReformStatus.objects.get(id=reform_status_id)
        reform_status.deleted = True
        reform_status.save()
        return Response({"message": "Reform Status deleted successfully"}, status=status.HTTP_200_OK)
    except ReformStatus.DoesNotExist:
        return Response({"error": "Reform Status not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_period(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = PeriodCreateSerializer(data=request.data)
    if serializer.is_valid():
        period = serializer.save()
        response_serializer = PeriodResponseSerializer(period)
        return Response({"message": "Period created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_periods(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    periods = Period.objects.filter(deleted=False)
    response_serializer = PeriodResponseSerializer(periods, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_period_by_id(request, period_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id) 
    
    try:
        period = Period.objects.get(id=period_id, deleted=False)
    except Period.DoesNotExist:
        return Response({"error": "Period not found"}, status=status.HTTP_404_NOT_FOUND)

    response_serializer = PeriodResponseSerializer(period)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_periods_by_latest_year_and_institution_id(request, institution_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    # Query the latest year for the given institution ID
    latest_year = Period.objects.filter(institution_id=institution_id, deleted=False).aggregate(Max('year'))['year__max']

    if latest_year is None:
        return Response({"message": "No periods found for the given institution"}, status=status.HTTP_404_NOT_FOUND)

    # Query all periods for the institution with the latest year
    periods = Period.objects.filter(
        institution_id=institution_id,
        year=latest_year,
        deleted=False
    )
    
    response_serializer = PeriodResponseSerializer(periods, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_period(request, period_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
     
    try:
        period = Period.objects.get(id=period_id)
    except Period.DoesNotExist:
        return Response({"error": "Period not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PeriodCreateSerializer(period, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_serializer = PeriodResponseSerializer(period)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_period(request, period_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        period = Period.objects.get(id=period_id)
    except Period.DoesNotExist:
        return Response({"error": "Period not found"}, status=status.HTTP_404_NOT_FOUND)

    period.deleted = True
    period.save()
    return Response({"message": "Period deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reform_area_period(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = CreateReformAreaPeriodRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_area_periods(request, skip=1, limit=10):
    user_id = request.user.id
    security = Security()
    try:
        security.secureAccess("create_user", user_id)
    except PermissionDenied as e:
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    total_count = ReformAreaPeriod.objects.count()
    periods = ReformAreaPeriod.objects.filter(deleted=False).all()[(skip - 1) * limit:skip * limit]
    serializer = ReformAreaPeriodResponseSerializer(periods, many=True)

    total_pages = (total_count - 1) // limit + 1
    return Response({"pages": total_pages, "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_area_period_by_id(request, period_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        period = ReformAreaPeriod.objects.get(id=period_id, deleted=False)
    except ReformAreaPeriod.DoesNotExist:
        return Response({"error": "Reform Area Period not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReformAreaPeriodResponseSerializer(period)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_area_periods_by_reform_area_id(request, reform_area_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    reform_area = get_object_or_404(ReformArea, id=reform_area_id, deleted=False)
    periods = ReformAreaPeriod.objects.filter(reform_area=reform_area, deleted=False)
    
    serializer = ReformAreaPeriodResponseSerializer(periods, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reform_area_period(request, period_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        period = ReformAreaPeriod.objects.get(id=period_id, deleted=False)
    except ReformAreaPeriod.DoesNotExist:
        return Response({"error": "Reform Area Period not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CreateReformAreaPeriodRequestSerializer(period, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reform_area_period(request, period_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        period = ReformAreaPeriod.objects.get(id=period_id, deleted=False)
    except ReformAreaPeriod.DoesNotExist:
        return Response({"error": "Reform Area Period not found"}, status=status.HTTP_404_NOT_FOUND)
    
    period.deleted = True
    period.save()
    serializer = ReformAreaPeriodResponseSerializer(period)
    return Response({"message": "Reform Area Period deleted successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reform_focus_area(request):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    serializer = ReformFocusAreaCreateSerializer(data=request.data)
    if serializer.is_valid():
        reform_area = serializer.validated_data['reform_area']
        focus_area = serializer.validated_data['focus_area']

        # Check if an entry with the same reform_area and focus_area exists
        existing_entry = ReformFocusArea.objects.filter(
            reform_area=reform_area,
            focus_area=focus_area
        ).first()

        if existing_entry:
            # If an entry exists, update it (if needed) and return the existing entry data
            # Update logic can be added here if needed, for now, it just returns the existing entry
            existing_entry.save()  # Save call can be customized if additional update logic is needed
            return Response(ReformFocusAreaCreateSerializer(existing_entry).data, status=status.HTTP_200_OK)
        else:
            # If no existing entry, create a new one
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_focus_areas(request, skip=1, limit=10):
    user_id = request.user.id
    security = Security()
    try:
        security.secureAccess("READ_REFORM_FOCUS_AREA", user_id)
    except PermissionDenied as e:
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    total_count = ReformFocusArea.objects.count()
    reform_focus_areas = ReformFocusArea.objects.filter(deleted=False).all()[(skip - 1) * limit:skip * limit]
    serializer = ReformFocusAreaResponseSerializer(reform_focus_areas, many=True)

    total_pages = (total_count - 1) // limit + 1
    return Response({"pages": total_pages, "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_focus_area_by_id(request, id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_focus_area = ReformFocusArea.objects.get(id=id, deleted=False)
    except ReformFocusArea.DoesNotExist:
        return Response({"error": "Reform Focus Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReformFocusAreaResponseSerializer(reform_focus_area)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_focus_areas_by_reform_area_id(request, reform_area_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    reform_focus_areas = ReformFocusArea.objects.filter(reform_area_id=reform_area_id, deleted=False)
    serializer = ReformFocusAreaResponseSerializer(reform_focus_areas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_focus_areas_by_focus_area_id(request, focus_area_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    reform_focus_areas = ReformFocusArea.objects.filter(focus_area_id=focus_area_id, deleted=False)
    serializer = ReformFocusAreaResponseSerializer(reform_focus_areas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reform_focus_area(request, id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        reform_focus_area = ReformFocusArea.objects.get(id=id, deleted=False)
    except ReformFocusArea.DoesNotExist:
        return Response({"error": "Reform Focus Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReformFocusAreaCreateSerializer(reform_focus_area, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reform_focus_area(request, id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    try:
        reform_focus_area = ReformFocusArea.objects.get(id=id, deleted=False)
    except ReformFocusArea.DoesNotExist:
        return Response({"error": "Reform Focus Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    reform_focus_area.deleted = True
    reform_focus_area.save()
    serializer = ReformFocusAreaResponseSerializer(reform_focus_area)
    return Response({"message": "Reform Focus Area deleted successfully", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_weight(request):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    reform_area_id = request.data.get('reform_area')
    weight_value = request.data.get('weight')
    justification = request.data.get('justification')  # Get justification from request

    if not reform_area_id or weight_value is None:
        return Response({"detail": "Reform area and weight are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if a Weight entry already exists for the given reform_area_id
    weight_instance = Weight.objects.filter(reform_area_id=reform_area_id, deleted=False).first()

    if weight_instance:
        # Update existing weight entry
        weight_instance.weight = weight_value
        weight_instance.justification = justification  # Update justification
        weight_instance.save()
        serializer = WeightCreateSerializer(weight_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # Create new weight entry
        serializer = WeightCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_weights(request, skip=1, limit=10, search=""):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    query = Weight.objects.filter(deleted=False)
    if search:
        query = query.filter(reform_area__id=int(search))

    total_count = query.count()
    weights_data = query.all()[(skip - 1) * limit:skip * limit]
    serializer = WeightResponseSerializer(weights_data, many=True)

    total_pages = (total_count - 1) // limit + 1
    return Response({"pages": total_pages, "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weight_by_id(request, weight_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        weight = Weight.objects.get(id=weight_id, deleted=False)
    except Weight.DoesNotExist:
        return Response({"error": "Weight not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WeightResponseSerializer(weight)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weights_by_reform_area_id(request, reform_area_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    weights = Weight.objects.filter(reform_area__id=reform_area_id, deleted=False)
    serializer = WeightResponseSerializer(weights, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_weight(request, weight_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        weight = Weight.objects.get(id=weight_id, deleted=False)
    except Weight.DoesNotExist:
        return Response({"error": "Weight not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WeightCreateSerializer(weight, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_weight(request, weight_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        weight = Weight.objects.get(id=weight_id, deleted=False)
    except Weight.DoesNotExist:
        return Response({"error": "Weight not found"}, status=status.HTTP_404_NOT_FOUND)
    
    weight.deleted = True
    weight.save()
    serializer = WeightResponseSerializer(weight)
    return Response({"message": "Weight deleted successfully", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_target(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    serializer = OutputTargetsCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_output_targets(request):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    output_targets = OutputTargets.objects.filter(deleted=False)
    serializer = OutputTargetsResponseSerializer(output_targets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_targets_by_indicator_id(request, indicator_id):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    output_targets = OutputTargets.objects.filter(output_indicator_id=indicator_id, deleted=False)
    serializer = OutputTargetsResponseSerializer(output_targets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_output_target(request, id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        output_target = OutputTargets.objects.get(id=id, deleted=False)
        output_target.deleted = True
        output_target.save()
        serializer = OutputTargetsResponseSerializer(output_target)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except OutputTargets.DoesNotExist:
        return Response({"error": "OutputTarget not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_output_target(request, id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    try:
        output_target = OutputTargets.objects.get(id=id, deleted=False)
    except OutputTargets.DoesNotExist:
        return Response({"error": "OutputTarget not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutputTargetsCreateSerializer(output_target, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_and_create_weights(request, output_id, year):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    # Retrieve all OutputIndicators for the given output_id
    output_indicators = OutputTargets.objects.filter(
        output_indicator__output_id=output_id, 
        year=year, 
        deleted=False
    ).values_list('output_indicator', flat=True).distinct()
    
    if not output_indicators:
        return Response({"message": "No output indicators found for the given output and year."}, status=status.HTTP_404_NOT_FOUND)
    
    all_weights = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
    results = []
    
    for indicator_id in output_indicators:
        # Filter output targets by indicator_id
        output_targets = OutputTargets.objects.filter(
            output_indicator=indicator_id, 
            year=year, 
            deleted=False
        )
        
        if not output_targets.exists():
            continue
        
        # Calculate differences and total difference
        differences = []
        for target in output_targets:
            Q1_diff = max(target.Q1_target - target.baseline if target.Q1_target else 0, 0)
            Q2_diff = max(
                (target.Q2_target - target.Q1_target) if target.Q1_target else (target.Q2_target - target.baseline if target.Q2_target else 0),
                0
            )
            Q3_diff = max(
                (target.Q3_target - target.Q2_target) if target.Q2_target else (target.Q3_target - target.Q1_target if target.Q1_target else target.Q3_target - target.baseline if target.Q3_target else 0),
                0
            )
            Q4_diff = max(
                (target.Q4_target - target.Q3_target) if target.Q3_target else (target.Q4_target - target.Q2_target if target.Q2_target else (target.Q4_target - target.Q1_target if target.Q1_target else (target.Q4_target - target.baseline if target.Q4_target else 0))),
                0
            )
            
            total_diff = Q1_diff + Q2_diff + Q3_diff + Q4_diff
            
            # Logging the differences for each quarter
            print(f"Target ID: {target.id}")
            print(f"Q1 Difference: {Q1_diff}")
            print(f"Q2 Difference: {Q2_diff}")
            print(f"Q3 Difference: {Q3_diff}")
            print(f"Q4 Difference: {Q4_diff}")
            print(f"Total Difference: {total_diff}")
            
            differences.append({
                'Q1_diff': Q1_diff,
                'Q2_diff': Q2_diff,
                'Q3_diff': Q3_diff,
                'Q4_diff': Q4_diff,
                'total': total_diff
            })
        
        # Calculate weights for this indicator
        indicator_weights = []
        for diff in differences:
            if diff['total'] > 0:
                weight = {
                    'Q1w': diff['Q1_diff'] / diff['total'],
                    'Q2w': diff['Q2_diff'] / diff['total'],
                    'Q3w': diff['Q3_diff'] / diff['total'],
                    'Q4w': diff['Q4_diff'] / diff['total']
                }
                # Logging the weights for each quarter
                print(f"Weights for differences: {diff}")
                print(f"Q1 Weight: {weight['Q1w']}")
                print(f"Q2 Weight: {weight['Q2w']}")
                print(f"Q3 Weight: {weight['Q3w']}")
                print(f"Q4 Weight: {weight['Q4w']}")
                indicator_weights.append(weight)
        
        # Store the weights for harmonic mean calculation
        for weight in indicator_weights:
            if weight['Q1w'] > 0:
                all_weights['Q1'].append(weight['Q1w'])
                print(f"Q1 weight added: {weight['Q1w']}")
            if weight['Q2w'] > 0:
                all_weights['Q2'].append(weight['Q2w'])
                print(f"Q2 weight added: {weight['Q2w']}")
            if weight['Q3w'] > 0:
                all_weights['Q3'].append(weight['Q3w'])
                print(f"Q3 weight added: {weight['Q3w']}")
            if weight['Q4w'] > 0:
                all_weights['Q4'].append(weight['Q4w'])
                print(f"Q4 weight added: {weight['Q4w']}")
                
        # Save results for this indicator
        results.append({
            'output_indicator': indicator_id,
            'weights': indicator_weights
        })
    
    # Calculate harmonic means for each quarter
    harmonic_means = {}
    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        weights_list = all_weights[quarter]
        if weights_list:
            mean_reciprocal = np.mean(1 / np.array(weights_list))
            harmonic_means[quarter] = 1 / mean_reciprocal
            print(f"{quarter} harmonic mean calculated: {harmonic_means[quarter]}")
        else:
            harmonic_means[quarter] = 0
            print(f"No weights for {quarter}, harmonic mean set to 0")

    # Calculate total harmonic mean and normalize weights
    total_harmonic_mean = sum(harmonic_means.values())
    print(f"Total harmonic mean: {total_harmonic_mean}")

    if total_harmonic_mean == 0:
        normalized_weights = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
        print("Total harmonic mean is 0, normalized weights set to 0 for all quarters")
    else:
        normalized_weights = {
            quarter: (value / total_harmonic_mean) 
            for quarter, value in harmonic_means.items()
        }
        print(f"Normalized weights: {normalized_weights}")    
        
    # Save OutputWeights for the output
    output_instance = get_object_or_404(Output, id=output_id)
    
    OutputWeights.objects.update_or_create(
        output_id=output_instance,
        year=year,
        defaults={
            'Q1w': normalized_weights['Q1'],
            'Q2w': normalized_weights['Q2'],
            'Q3w': normalized_weights['Q3'],
            'Q4w': normalized_weights['Q4']
        }
    )
    
    # Return response
    return Response({"message": "Weights calculated and saved successfully", "results": results}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_and_create_end_contract_weights(request, output_id, year):
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)

    # Check if entry already exists
    existing_weights = EndContractOutputWeights.objects.filter(output_id=output_id, year=year).first()
    if existing_weights:
        print(f"Entry already exists for output_id: {output_id}, year: {year}")
        return Response({"message": "Weights already calculated for this output and year."}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve all OutputIndicators for the given output_id
    output_indicators = OutputTargets.objects.filter(
        output_indicator__output_id=output_id,
        year__in=[year, year + 1],  # Include both current year and next year
        deleted=False
    ).values_list('output_indicator', flat=True).distinct()

    if not output_indicators:
        print(f"No output indicators found for output_id: {output_id}")
        return Response({"message": "No output indicators found for the given output and year."}, status=status.HTTP_404_NOT_FOUND)

    # Initialize weights storage for Year 1 and Year 2
    all_weights = {
        'Q1Y1': [], 'Q2Y1': [], 'Q3Y1': [], 'Q4Y1': [],
        'Q1Y2': [], 'Q2Y2': [], 'Q3Y2': [], 'Q4Y2': []
    }

    print(f"Calculating weights for output_id: {output_id}, year: {year}")

    for indicator_id in output_indicators:
        # Filter output targets by indicator_id for both current and next year
        output_targets = OutputTargets.objects.filter(
            output_indicator=indicator_id,
            year__in=[year, year + 1],  # Include both current year and next year
            deleted=False
        )

        if not output_targets.exists():
            print(f"No output targets found for indicator_id: {indicator_id}")
            continue

        # Calculate differences and total difference for both years
        differences = []
        for target in output_targets:
            if target.year == year:
                next_year_target = OutputTargets.objects.filter(
                    output_indicator=indicator_id,
                    year=year + 1,
                    deleted=False
                ).first()

                Q1_diff = max(target.Q1_target - target.baseline if target.Q1_target else 0, 0)
                Q2_diff = max(
                    (target.Q2_target - target.Q1_target) if target.Q1_target else (target.Q2_target - target.baseline if target.Q2_target else 0),
                    0
                )
                Q3_diff = max(
                    (target.Q3_target - target.Q2_target) if target.Q2_target else (target.Q3_target - target.Q1_target if target.Q1_target else target.Q3_target - target.baseline if target.Q3_target else 0),
                    0
                )
                Q4_diff = max(
                    (target.Q4_target - target.Q3_target) if target.Q3_target else (target.Q4_target - target.Q2_target if target.Q2_target else (target.Q4_target - target.Q1_target if target.Q1_target else (target.Q4_target - target.baseline if target.Q4_target else 0))),
                    0
                )

                total_diff_current_year = Q1_diff + Q2_diff + Q3_diff + Q4_diff

                # Add next year's target if available
                if next_year_target:
                    Q1_diff_next_year = max(next_year_target.Q1_target - next_year_target.baseline if next_year_target.Q1_target else 0, 0)
                    Q2_diff_next_year = max(
                        (next_year_target.Q2_target - next_year_target.Q1_target) if next_year_target.Q1_target else (next_year_target.Q2_target - next_year_target.baseline if next_year_target.Q2_target else 0),
                        0
                    )
                    Q3_diff_next_year = max(
                        (next_year_target.Q3_target - next_year_target.Q2_target) if next_year_target.Q2_target else (next_year_target.Q3_target - next_year_target.Q1_target if next_year_target.Q1_target else next_year_target.Q3_target - next_year_target.baseline if next_year_target.Q3_target else 0),
                        0
                    )
                    Q4_diff_next_year = max(
                        (next_year_target.Q4_target - next_year_target.Q3_target) if next_year_target.Q3_target else (next_year_target.Q4_target - next_year_target.Q2_target if next_year_target.Q2_target else (next_year_target.Q4_target - next_year_target.Q1_target if next_year_target.Q1_target else (next_year_target.Q4_target - next_year_target.baseline if next_year_target.Q4_target else 0))),
                        0
                    )

                    total_diff_next_year = Q1_diff_next_year + Q2_diff_next_year + Q3_diff_next_year + Q4_diff_next_year
                else:
                    total_diff_next_year = 0

                total_diff = total_diff_current_year + total_diff_next_year

                differences.append({
                    'Q1_diff_current': Q1_diff,
                    'Q2_diff_current': Q2_diff,
                    'Q3_diff_current': Q3_diff,
                    'Q4_diff_current': Q4_diff,
                    'Q1_diff_next': Q1_diff_next_year,
                    'Q2_diff_next': Q2_diff_next_year,
                    'Q3_diff_next': Q3_diff_next_year,
                    'Q4_diff_next': Q4_diff_next_year,
                    'total_current': total_diff_current_year,
                    'total_next': total_diff_next_year,
                    'total': total_diff
                })

        # Calculate weights for this indicator
        indicator_weights = []
        for diff in differences:
            if diff['total'] > 0:
                weight = {
                    'Q1wY1': (diff['Q1_diff_current']) / diff['total'],
                    'Q2wY1': (diff['Q2_diff_current']) / diff['total'],
                    'Q3wY1': (diff['Q3_diff_current']) / diff['total'],
                    'Q4wY1': (diff['Q4_diff_current']) / diff['total'],
                    'Q1wY2': (diff['Q1_diff_next']) / diff['total'],
                    'Q2wY2': (diff['Q2_diff_next']) / diff['total'],
                    'Q3wY2': (diff['Q3_diff_next']) / diff['total'],
                    'Q4wY2': (diff['Q4_diff_next']) / diff['total']
                }
                indicator_weights.append(weight)

        # Store the weights for harmonic mean calculation
        for weight in indicator_weights:
            if weight['Q1wY1'] > 0:
                all_weights['Q1Y1'].append(weight['Q1wY1'])
            if weight['Q2wY1'] > 0:
                all_weights['Q2Y1'].append(weight['Q2wY1'])
            if weight['Q3wY1'] > 0:
                all_weights['Q3Y1'].append(weight['Q3wY1'])
            if weight['Q4wY1'] > 0:
                all_weights['Q4Y1'].append(weight['Q4wY1'])
            if weight['Q1wY2'] > 0:
                all_weights['Q1Y2'].append(weight['Q1wY2'])
            if weight['Q2wY2'] > 0:
                all_weights['Q2Y2'].append(weight['Q2wY2'])
            if weight['Q3wY2'] > 0:
                all_weights['Q3Y2'].append(weight['Q3wY2'])
            if weight['Q4wY2'] > 0:
                all_weights['Q4Y2'].append(weight['Q4wY2'])

    # Calculate harmonic means
    harmonic_means = {}
    for key, values in all_weights.items():
        if values:
            harmonic_mean = len(values) / sum(1 / v for v in values)
            harmonic_means[key] = harmonic_mean
        else:
            harmonic_means[key] = 0  # Assign 0 if no values

    print(f"Harmonic means calculated: {harmonic_means}")

    total_harmonic_mean = sum(harmonic_means.values())

    # Normalize weights to ensure they sum up to 1 for both years
    if total_harmonic_mean > 0:
        normalized_weights = {k: v / total_harmonic_mean for k, v in harmonic_means.items()}
    else:
        normalized_weights = harmonic_means

    print(f"Normalized weights: {normalized_weights}")

    # Save weights for the current year
    EndContractOutputWeights.objects.update_or_create(
        output_id=output_id,
        year=year,
        defaults={
            'Q1w': normalized_weights.get('Q1Y1', 0),
            'Q2w': normalized_weights.get('Q2Y1', 0),
            'Q3w': normalized_weights.get('Q3Y1', 0),
            'Q4w': normalized_weights.get('Q4Y1', 0)
        }
    )

    # Save weights for the next year
    EndContractOutputWeights.objects.update_or_create(
        output_id=output_id,
        year=year + 1,
        defaults={
            'Q1w': normalized_weights.get('Q1Y2', 0),
            'Q2w': normalized_weights.get('Q2Y2', 0),
            'Q3w': normalized_weights.get('Q3Y2', 0),
            'Q4w': normalized_weights.get('Q4Y2', 0)
        }
    )

    return Response({"message": "Weights calculated and saved successfully."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_output_weights(request, output_id, year):
    # Retrieve the OutputWeights for the specified output and year
    output_weights = OutputWeights.objects.filter(output_id=output_id, year=year).first()

    if not output_weights:
        return Response({"message": "No output weights found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutputWeightsSerializer(output_weights)
    return Response(serializer.data, status=status.HTTP_200_OK)

class AnnualOutputACRView(generics.CreateAPIView):
    serializer_class = AnnualOutputACRSerializer

    def create(self, request, *args, **kwargs):
        output_id = request.data.get('output')
        year = request.data.get('year')

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(is_active=True).first()
        if not active_period:
            return Response({"message": "No active output reporting period found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all OutputActuals for the given output and year
        output_actuals = OutputActual.objects.filter(output_indicator__output_id=output_id, year=year)

        if not output_actuals.exists():
            return Response({"message": "No output actuals found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the average ACR
        total_acr = sum(float(output_actual.ACR) for output_actual in output_actuals)
        count = output_actuals.count()
        average_acr = total_acr / float(count) if count > 0 else 0.0

        print(f"Output ID: {output_id}")
        print(f"Year: {year}")
        print(f"Total ACR: {total_acr}")
        print(f"Count of Output Actuals: {count}")
        print(f"Average ACR: {average_acr}")

        # Retrieve OutputWeights for the given output and year
        output_weights = OutputWeights.objects.filter(output_id=output_id, year=year).first()

        if not output_weights:
            return Response({"message": "No output weights found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

        # Determine the correct weight based on the active reporting period
        if active_period.output_label == 'Q1':
            weight = float(output_weights.Q1w)
            weighted_acr = average_acr * weight
        elif active_period.output_label == 'Q2':
            weight = float(output_weights.Q2w)
            weighted_acr = average_acr * weight
            
            # Retrieve previous quarter's annual_average_acr (Q1)
            previous_acr = AnnualOutputACR.objects.filter(output_id=output_id, year=year, output_reporting_period__output_label='Q1').first()
            if previous_acr:
                weighted_acr += float(previous_acr.annual_average_acr)
        elif active_period.output_label == 'Q3':
            weight = float(output_weights.Q3w)
            weighted_acr = average_acr * weight
            
            # Retrieve previous quarter's annual_average_acr (Q2)
            previous_acr = AnnualOutputACR.objects.filter(output_id=output_id, year=year, output_reporting_period__output_label='Q2').first()
            if previous_acr:
                weighted_acr += float(previous_acr.annual_average_acr)
        elif active_period.output_label == 'Q4':
            weight = float(output_weights.Q4w)
            weighted_acr = average_acr * weight
            
            # Retrieve previous quarter's annual_average_acr (Q3)
            previous_acr = AnnualOutputACR.objects.filter(output_id=output_id, year=year, output_reporting_period__output_label='Q3').first()
            if previous_acr:
                weighted_acr += float(previous_acr.annual_average_acr)
        else:
            return Response({"message": "Invalid reporting period."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Active Period: {active_period.output_label}")
        print(f"Weight Used: {weight}")
        print(f"Weighted ACR: {weighted_acr}")

        # Create or update AnnualOutputACR with weighted ACR and active reporting period
        annual_output_acr, created = AnnualOutputACR.objects.update_or_create(
            output_id=output_id,
            year=year,
            output_reporting_period=active_period,
            defaults={
                'annual_average_acr': weighted_acr,
                'deleted': False
            }
        )

        serializer = self.get_serializer(annual_output_acr)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class AnnualReformAreaACRCreateView(generics.CreateAPIView):
    serializer_class = AnnualReformAreaACRSerializer

    def create(self, request, *args, **kwargs):
        year = request.data.get('year')
        output_reporting_period_id = request.data.get('output_reporting_period_id')

        print(f"Received data - Year: {year}, Output Reporting Period ID: {output_reporting_period_id}")

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(id=output_reporting_period_id).first()
        if not active_period:
            print(f"Invalid output reporting period ID: {output_reporting_period_id}")
            return Response({"message": "Invalid output reporting period."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the latest year from ReformArea
        latest_year = ReformArea.objects.aggregate(Max('year'))['year__max']
        print(f"Latest year from ReformArea: {latest_year}")

        if not latest_year:
            print("No reform areas found.")
            return Response({"message": "No reform areas found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all ReformAreas for the latest year
        reform_areas = ReformArea.objects.filter(year=latest_year, deleted=False)
        if not reform_areas.exists():
            print("No reform areas found for the latest year.")
            return Response({"message": "No reform areas found for the latest year."}, status=status.HTTP_404_NOT_FOUND)

        # Iterate over each reform area and calculate average ACR
        for reform_area in reform_areas:
            # Get all AnnualOutputACR for the current ReformArea and active output reporting period
            related_annual_acrs = AnnualOutputACR.objects.filter(
                output__reform_area=reform_area,
                year=year,
                deleted=False,
                output_reporting_period_id=output_reporting_period_id
            )
            print(f"Related AnnualOutputACR count for ReformArea ID {reform_area.id}: {related_annual_acrs.count()}")

            # Calculate average ACR for the current ReformArea
            annual_output_acrs = related_annual_acrs.values_list('annual_average_acr', flat=True)
            print(f"Annual Output ACRs for ReformArea ID {reform_area.id}: {list(annual_output_acrs)}")

            if annual_output_acrs:
                average_acr = sum(annual_output_acrs) / len(annual_output_acrs)
            else:
                average_acr = 0
            print(f"Calculated average ACR for ReformArea ID {reform_area.id}: {average_acr}")

            # Check if there's an existing record with the same reform_area, year, and output reporting period
            existing_acr = AnnualReformAreaACR.objects.filter(
                reform_area=reform_area,
                year=year,
                output_reporting_period=active_period
            ).first()
            print(f"Existing ACR record for ReformArea ID {reform_area.id}: {existing_acr}")

            if existing_acr:
                # Update existing entry
                try:
                    with transaction.atomic():
                        existing_acr.average_acr = average_acr
                        existing_acr.save()
                        print(f"Updated existing entry for ReformArea ID {reform_area.id}.")
                except IntegrityError as e:
                    print(f"Error updating entry for ReformArea ID {reform_area.id}: {e}")
                    return Response({"message": "Error updating entry."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Create new entry
                try:
                    with transaction.atomic():
                        AnnualReformAreaACR.objects.create(
                            reform_area=reform_area,
                            year=year,
                            average_acr=average_acr,
                            output_reporting_period=active_period,
                            deleted=False
                        )
                        print(f"Created new entry for ReformArea ID {reform_area.id}.")
                except IntegrityError as e:
                    print(f"Error creating entry for ReformArea ID {reform_area.id}: {e}")
                    return Response({"message": "Error creating entry."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Annual Reform Area ACRs processed successfully."}, status=status.HTTP_200_OK)

    
class AnnualReformAreaACRByOutputReportingPeriodAndReformArea(generics.ListAPIView):
    serializer_class = AnnualReformAreaACRSerializer

    def get_queryset(self):
        output_reporting_period_id = self.kwargs['output_reporting_period_id']
        reform_area_id = self.kwargs['reform_area_id']

        # Get all outputs related to the reform area
        related_outputs = Output.objects.filter(reform_area_id=reform_area_id)

        # Get the latest year for the given output_reporting_period_id and related outputs
        latest_year = AnnualOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs
        ).aggregate(Max('year'))['year__max']

        # Return the entries with the latest year for the given reporting period and reform area
        return AnnualReformAreaACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            reform_area_id=reform_area_id,
            year=latest_year
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'output_reporting_period_id': self.kwargs['output_reporting_period_id']
        })
        return context

        
class AnnualOutputACRByOutputReportingPeriodAndReformArea(generics.ListAPIView):
    serializer_class = AnnualOutputACRSerializer

    def get_queryset(self):
        output_reporting_period_id = self.kwargs['output_reporting_period_id']
        reform_area_id = self.kwargs['reform_area_id']

        # Get all outputs related to the reform area
        related_outputs = Output.objects.filter(reform_area_id=reform_area_id)

        # Get the latest year for the given output_reporting_period_id and related outputs
        latest_year = AnnualOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs
        ).aggregate(Max('year'))['year__max']

        # Return the entries with the latest year for the given reporting period and reform area
        return AnnualOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs,
            year=latest_year
        )
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outcome_target(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    serializer = OutcomeTargetsCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_outcome_targets(request):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    outcome_targets = OutcomeTargets.objects.filter(deleted=False)
    serializer = OutcomeTargetsResponseSerializer(outcome_targets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcome_target_by_id(request, outcome_targets_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    try:
        outcome_target = OutcomeTargets.objects.get(id=outcome_targets_id, deleted=False)
    except OutcomeTargets.DoesNotExist:
        return Response({"error": "Outcome targets not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutcomeTargetsResponseSerializer(outcome_target)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_outcome_target(request, outcome_targets_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    try:
        outcome_target = OutcomeTargets.objects.get(id=outcome_targets_id, deleted=False)
    except OutcomeTargets.DoesNotExist:
        return Response({"error": "Outcome targets not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutcomeTargetsCreateSerializer(outcome_target, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcome_targets_by_indicator(request, indicator_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    
    outcome_targets = OutcomeTargets.objects.filter(outcome_indicator_id=indicator_id, deleted=False)
    serializer = OutcomeTargetsResponseSerializer(outcome_targets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_outcome_target(request, outcome_targets_id):
    
    user_id = request.user.id
    Security().secureAccess("create_user", user_id)
    try:
        outcome_target = OutcomeTargets.objects.get(id=outcome_targets_id, deleted=False)
        outcome_target.deleted = True
        outcome_target.save()
        serializer = OutcomeTargetsResponseSerializer(outcome_target)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except OutcomeTargets.DoesNotExist:
        return Response({"error": "Outcome targets not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_movs(request):
    serializer = OutputMovCreateSerializer(data=request.data)
    if serializer.is_valid():
        output_indicator_id = serializer.validated_data['output_indicator_id']
        movs = serializer.validated_data['movs']
        
        user_id = request.user.id
        # Assuming you have a similar security check for OutputMov creation
        Security().secureAccess("create_user", user_id)
        
        try:
            output_indicator = OutputIndicator.objects.get(id=output_indicator_id)
        except OutputIndicator.DoesNotExist:
            return Response({"error": "Output Indicator not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_movs = []
        for mov_text in movs:
            new_mov = OutputMov.objects.create(
                output_indicator_id=output_indicator_id,
                mov=mov_text,
                deleted=False
            )
            new_movs.append(new_mov)
        
        response_serializer = OutputMovResponseSerializer(new_movs, many=True)
        return Response({"message": "Output MOVs created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OutputMovListCreate(generics.ListCreateAPIView):
    queryset = OutputMov.objects.filter(deleted=False)
    serializer_class = OutputMovSerializer
    permission_classes = [IsAuthenticated]

class OutputMovRetrieve(generics.RetrieveAPIView):
    queryset = OutputMov.objects.filter(deleted=False)
    serializer_class = OutputMovSerializer
    permission_classes = [IsAuthenticated]
    
class OutputMovUpdate(generics.UpdateAPIView):
    queryset = OutputMov.objects.filter(deleted=False)
    serializer_class = OutputMovSerializer
    permission_classes = [IsAuthenticated]
    
class OutputMovDestroy(generics.DestroyAPIView):
    queryset = OutputMov.objects.filter(deleted=False)
    serializer_class = OutputMovSerializer
    permission_classes = [IsAuthenticated]

class OutputMovByIndicatorList(generics.ListAPIView):
    serializer_class = OutputMovSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        output_indicator_id = self.kwargs['output_indicator_id']
        return OutputMov.objects.filter(output_indicator_id=output_indicator_id, deleted=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_csfs(request):
    serializer = OutputCSFCreateSerializer(data=request.data)
    if serializer.is_valid():
        output_indicator_id = serializer.validated_data['output_indicator_id']
        output_csfs = serializer.validated_data['output_csfs']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        try:
            output_indicator = OutputIndicator.objects.get(id=output_indicator_id)
        except OutputIndicator.DoesNotExist:
            return Response({"error": "Output Indicator not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_csfs = []
        for csf_text in output_csfs:
            new_csf = OutputCSF.objects.create(
                output_indicator=output_indicator,
                output_csf=csf_text,
                deleted=False
            )
            new_csfs.append(new_csf)
        
        response_serializer = OutputCSFResponseSerializer(new_csfs, many=True)
        return Response({"message": "Output CSFs created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_instruments(request):
    serializer = OutputInstrumentCreateSerializer(data=request.data)
    if serializer.is_valid():
        output_indicator_id = serializer.validated_data['output_indicator_id']
        output_instruments = serializer.validated_data['output_instruments']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        try:
            output_indicator = OutputIndicator.objects.get(id=output_indicator_id)
        except OutputIndicator.DoesNotExist:
            return Response({"error": "Output Indicator not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_instruments = []
        for instrument_text in output_instruments:
            new_instrument = OutputInstrument.objects.create(
                output_indicator=output_indicator,
                output_instrument=instrument_text,
                deleted=False
            )
            new_instruments.append(new_instrument)
        
        response_serializer = OutputInstrumentResponseSerializer(new_instruments, many=True)
        return Response({"message": "Output Instruments created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OutputCSFListCreate(generics.ListCreateAPIView):
    queryset = OutputCSF.objects.filter(deleted=False)
    serializer_class = OutputCSFSerializer
    permission_classes = [IsAuthenticated]

class OutputCSFRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutputCSF.objects.filter(deleted=False)
    serializer_class = OutputCSFSerializer
    permission_classes = [IsAuthenticated]

class OutputCSFByIndicatorList(generics.ListAPIView):
    serializer_class = OutputCSFSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        output_indicator_id = self.kwargs['output_indicator_id']
        return OutputCSF.objects.filter(output_indicator_id=output_indicator_id, deleted=False)

class OutputInstrumentListCreate(generics.ListCreateAPIView):
    queryset = OutputInstrument.objects.filter(deleted=False)
    serializer_class = OutputInstrumentSerializer
    permission_classes = [IsAuthenticated]

class OutputInstrumentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutputInstrument.objects.filter(deleted=False)
    serializer_class = OutputInstrumentSerializer
    permission_classes = [IsAuthenticated]

class OutputInstrumentByIndicatorList(generics.ListAPIView):
    serializer_class = OutputInstrumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        output_indicator_id = self.kwargs['output_indicator_id']
        return OutputInstrument.objects.filter(output_indicator_id=output_indicator_id, deleted=False)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outcome_movs(request):
    serializer = OutcomeMoVCreateSerializer(data=request.data)
    if serializer.is_valid():
        outcome_indicator_id = serializer.validated_data['outcome_indicator_id']
        movs = serializer.validated_data['movs']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        outcome_indicator = get_object_or_404(OutcomeIndicator, id=outcome_indicator_id)
        
        new_movs = []
        for mov_text in movs:
            new_mov = OutcomeMoV.objects.create(
                outcome_indicator=outcome_indicator,
                mov=mov_text,
                deleted=False
            )
            new_movs.append(new_mov)
        
        response_serializer = OutcomeMoVSerializer(new_movs, many=True)
        return Response({"message": "Outcome MoVs created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outcome_csfs(request):
    serializer = OutcomeCSFCreateSerializer(data=request.data)
    if serializer.is_valid():
        outcome_indicator_id = serializer.validated_data['outcome_indicator_id']
        csfs = serializer.validated_data['csfs']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        outcome_indicator = get_object_or_404(OutcomeIndicator, id=outcome_indicator_id)
        
        new_csfs = []
        for csf_text in csfs:
            new_csf = OutcomeCSF.objects.create(
                outcome_indicator=outcome_indicator,
                csf=csf_text,
                deleted=False
            )
            new_csfs.append(new_csf)
        
        response_serializer = OutcomeCSFSerializer(new_csfs, many=True)
        return Response({"message": "Outcome CSFs created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outcome_instruments(request):
    serializer = OutcomeInstrumentCreateSerializer(data=request.data)
    if serializer.is_valid():
        outcome_indicator_id = serializer.validated_data['outcome_indicator_id']
        instruments = serializer.validated_data['instruments']
        
        user_id = request.user.id
        Security().secureAccess("create_user", user_id)
        
        outcome_indicator = get_object_or_404(OutcomeIndicator, id=outcome_indicator_id)
        
        new_instruments = []
        for instrument_text in instruments:
            new_instrument = OutcomeInstrument.objects.create(
                outcome_indicator=outcome_indicator,
                instrument=instrument_text,
                deleted=False
            )
            new_instruments.append(new_instrument)
        
        response_serializer = OutcomeInstrumentSerializer(new_instruments, many=True)
        return Response({"message": "Outcome Instruments created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OutcomeMoVListView(generics.ListAPIView):
    serializer_class = OutcomeMoVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OutcomeMoV.objects.filter(deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

class OutcomeMoVRetrieve(generics.RetrieveAPIView):
    queryset = OutcomeMoV.objects.filter(deleted=False)
    serializer_class = OutcomeMoVSerializer
    permission_classes = [IsAuthenticated]

    
class OutcomeMoVUpdate(generics.UpdateAPIView):
    queryset = OutcomeMoV.objects.filter(deleted=False)
    serializer_class = OutcomeMoVSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    
    
class OutcomeMoVDestroy(generics.DestroyAPIView):
    queryset = OutcomeMoV.objects.filter(deleted=False)
    serializer_class = OutcomeMoVSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True  # Soft delete
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class DeletedOutcomeMoVListView(generics.ListAPIView):
    serializer_class = OutcomeMoVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OutcomeMoV.objects.filter(deleted=True)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_outcome_mov(request):
    try:
        # Delete all records from OutcomeMoV
        deleted_count, _ = OutcomeMoV.objects.all().delete()
        
        return Response({
            "message": f"Successfully deleted {deleted_count} OutcomeMoV records."
        })
    except Exception as e:
        return Response({
            "error": f"Failed to delete OutcomeMoV records: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcome_movs_by_indicator(request, outcome_indicator_id):
    outcome_indicator = get_object_or_404(OutcomeIndicator, id=outcome_indicator_id)
    queryset = OutcomeMoV.objects.filter(outcome_indicator=outcome_indicator, deleted=False)
    serializer = OutcomeMoVSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class OutcomeCSFListCreate(generics.ListCreateAPIView):
    queryset = OutcomeCSF.objects.filter(deleted=False)
    serializer_class = OutcomeCSFSerializer
    permission_classes = [IsAuthenticated]

class OutcomeCSFDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutcomeCSF.objects.filter(deleted=False)
    serializer_class = OutcomeCSFSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcome_csfs_by_indicator(request, outcome_indicator_id):
    outcome_indicator = get_object_or_404(OutcomeIndicator, id=outcome_indicator_id)
    queryset = OutcomeCSF.objects.filter(outcome_indicator=outcome_indicator, deleted=False)
    serializer = OutcomeCSFSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class OutcomeInstrumentListCreate(generics.ListCreateAPIView):
    queryset = OutcomeInstrument.objects.filter(deleted=False)
    serializer_class = OutcomeInstrumentSerializer
    permission_classes = [IsAuthenticated]

class OutcomeInstrumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutcomeInstrument.objects.filter(deleted=False)
    serializer_class = OutcomeInstrumentSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcome_instruments_by_indicator(request, outcome_indicator_id):
    outcome_indicator = get_object_or_404(OutcomeIndicator, id=outcome_indicator_id)
    queryset = OutcomeInstrument.objects.filter(outcome_indicator=outcome_indicator, deleted=False)
    serializer = OutcomeInstrumentSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_budget(request):
    serializer = OutputBudgetCreateSerializer(data=request.data)
    if serializer.is_valid():
        output_budget = serializer.save()
        response_serializer = OutputBudgetResponseSerializer(output_budget)
        return Response({"message": "Output Budget created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_output_budgets(request):
    output_budgets = OutputBudget.objects.filter(deleted=False)
    response_serializer = OutputBudgetResponseSerializer(output_budgets, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_budget_by_id(request, output_budget_id):
    try:
        output_budget = OutputBudget.objects.get(id=output_budget_id, deleted=False)
    except OutputBudget.DoesNotExist:
        return Response({"error": "Output Budget not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = OutputBudgetResponseSerializer(output_budget)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_output_budget(request, output_budget_id):
    try:
        output_budget = OutputBudget.objects.get(id=output_budget_id)
    except OutputBudget.DoesNotExist:
        return Response({"error": "Output Budget not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OutputBudgetCreateSerializer(output_budget, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_serializer = OutputBudgetResponseSerializer(output_budget)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_output_budget(request, output_budget_id):
    try:
        output_budget = OutputBudget.objects.get(id=output_budget_id)
    except OutputBudget.DoesNotExist:
        return Response({"error": "Output Budget not found"}, status=status.HTTP_404_NOT_FOUND)

    output_budget.deleted = True
    output_budget.save()
    return Response({"message": "Output Budget deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reform_budget(request):
    serializer = ReformBudgetCreateSerializer(data=request.data)
    if serializer.is_valid():
        reform_budget = serializer.save()
        response_serializer = ReformBudgetResponseSerializer(reform_budget)
        return Response({"message": "Reform Budget created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reform_budgets(request):
    reform_budgets = ReformBudget.objects.filter(deleted=False)
    response_serializer = ReformBudgetResponseSerializer(reform_budgets, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reform_budget_by_id(request, reform_budget_id):
    try:
        reform_budget = ReformBudget.objects.get(id=reform_budget_id, deleted=False)
    except ReformBudget.DoesNotExist:
        return Response({"error": "Reform Budget not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = ReformBudgetResponseSerializer(reform_budget)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reform_budget(request, reform_budget_id):
    try:
        reform_budget = ReformBudget.objects.get(id=reform_budget_id)
    except ReformBudget.DoesNotExist:
        return Response({"error": "Reform Budget not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReformBudgetCreateSerializer(reform_budget, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_serializer = ReformBudgetResponseSerializer(reform_budget)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reform_budget(request, reform_budget_id):
    try:
        reform_budget = ReformBudget.objects.get(id=reform_budget_id)
    except ReformBudget.DoesNotExist:
        return Response({"error": "Reform Budget not found"}, status=status.HTTP_404_NOT_FOUND)

    reform_budget.deleted = True
    reform_budget.save()
    return Response({"message": "Reform Budget deleted successfully"}, status=status.HTTP_200_OK)

# OrgResponsibility Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_org_responsibilities(request):
    serializer = OrgResponsibilityCreateSerializer(data=request.data)
    if serializer.is_valid():
        institution_id = serializer.validated_data['institution_id']
        responsibilities = serializer.validated_data['responsibilities']
        year = serializer.validated_data['year']
        
        # Retrieve the Institution instance
        institution = get_object_or_404(Institution, id=institution_id)
        
        new_responsibilities = []
        for resp_text in responsibilities:
            new_resp = OrgResponsibility.objects.create(
                institution_id=institution,  # Assign the institution instance
                responsibility=resp_text,
                year=year,
                deleted=False
            )
            new_responsibilities.append(new_resp)
        
        response_serializer = OrgResponsibilityResponseSerializer(new_responsibilities, many=True)
        return Response({"message": "Org Responsibilities created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_org_responsibilities(request):
    org_responsibilities = OrgResponsibility.objects.filter(deleted=False)
    response_serializer = OrgResponsibilitySerializer(org_responsibilities, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_org_responsibility_by_id(request, org_responsibility_id):
    try:
        org_responsibility = OrgResponsibility.objects.get(id=org_responsibility_id, deleted=False)
    except OrgResponsibility.DoesNotExist:
        return Response({"error": "Org Responsibility not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = OrgResponsibilitySerializer(org_responsibility)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_org_responsibility_by_institution_id(request, institution_id):
    # Fetch the latest year for the given institution
    latest_year = OrgResponsibility.objects.filter(
        institution_id=institution_id, deleted=False
    ).aggregate(latest_year=Max('year'))['latest_year']

    if latest_year is not None:
        # Query OrgResponsibility entries with the latest year
        org_responsibilities = OrgResponsibility.objects.filter(
            institution_id=institution_id,
            year=latest_year,
            deleted=False
        )
        response_serializer = OrgResponsibilitySerializer(org_responsibilities, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    return Response([], status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_org_responsibility(request, org_responsibility_id):
    try:
        org_responsibility = OrgResponsibility.objects.get(id=org_responsibility_id)
    except OrgResponsibility.DoesNotExist:
        return Response({"error": "Org Responsibility not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrgResponsibilitySerializer(org_responsibility, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_serializer = OrgResponsibilitySerializer(org_responsibility)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_org_responsibility(request, org_responsibility_id):
    try:
        org_responsibility = OrgResponsibility.objects.get(id=org_responsibility_id)
    except OrgResponsibility.DoesNotExist:
        return Response({"error": "Org Responsibility not found"}, status=status.HTTP_404_NOT_FOUND)

    org_responsibility.deleted = True
    org_responsibility.save()
    return Response({"message": "Org Responsibility deleted successfully"}, status=status.HTTP_200_OK)

# GovtObligation Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_govt_obligations(request):
    serializer = GovtObligationCreateSerializer(data=request.data)
    if serializer.is_valid():
        institution_id = serializer.validated_data['institution_id']
        obligations = serializer.validated_data['govt_obligations']
        year = serializer.validated_data['year']
        
        # Retrieve the Institution instance
        institution = get_object_or_404(Institution, id=institution_id)
        
        new_obligations = []
        for obligation_text in obligations:
            new_obligation = GovtObligation.objects.create(
                institution_id=institution,  # Assign the institution instance
                govt_obligation=obligation_text,
                year=year,
                deleted=False
            )
            new_obligations.append(new_obligation)
        
        response_serializer = GovtObligationResponseSerializer(new_obligations, many=True)
        return Response({"message": "Govt Obligations created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_govt_obligations(request):
    govt_obligations = GovtObligation.objects.filter(deleted=False)
    response_serializer = GovtObligationSerializer(govt_obligations, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_govt_obligation_by_id(request, govt_obligation_id):
    try:
        govt_obligation = GovtObligation.objects.get(id=govt_obligation_id, deleted=False)
    except GovtObligation.DoesNotExist:
        return Response({"error": "Govt Obligation not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = GovtObligationSerializer(govt_obligation)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_govt_obligation_by_institution_id(request, institution_id):
    # Fetch the latest year for the given institution
    latest_year = GovtObligation.objects.filter(
        institution_id=institution_id, deleted=False
    ).aggregate(latest_year=Max('year'))['latest_year']

    if latest_year is not None:
        # Query GovtObligation entries with the latest year
        govt_obligations = GovtObligation.objects.filter(
            institution_id=institution_id,
            year=latest_year,
            deleted=False
        )
        response_serializer = GovtObligationResponseSerializer(govt_obligations, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    return Response([], status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_govt_obligation(request, govt_obligation_id):
    try:
        govt_obligation = GovtObligation.objects.get(id=govt_obligation_id)
    except GovtObligation.DoesNotExist:
        return Response({"error": "Govt Obligation not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = GovtObligationSerializer(govt_obligation, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_serializer = GovtObligationSerializer(govt_obligation)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_govt_obligation(request, govt_obligation_id):
    try:
        govt_obligation = GovtObligation.objects.get(id=govt_obligation_id)
    except GovtObligation.DoesNotExist:
        return Response({"error": "Govt Obligation not found"}, status=status.HTTP_404_NOT_FOUND)

    govt_obligation.deleted = True
    govt_obligation.save()
    return Response({"message": "Govt Obligation deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_indicator_period(request):
    serializer = IndicatorPeriodCreateSerializer(data=request.data)
    if serializer.is_valid():
        indicator_period = serializer.save()
        response_serializer = IndicatorPeriodResponseSerializer(indicator_period)
        return Response({"message": "Indicator Period created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_indicator_periods(request):
    indicator_periods = IndicatorPeriod.objects.filter(deleted=False)
    response_serializer = IndicatorPeriodListResponseSerializer(indicator_periods, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_indicator_period_by_id(request, period_id):
    try:
        indicator_period = IndicatorPeriod.objects.get(id=period_id, deleted=False)
    except IndicatorPeriod.DoesNotExist:
        return Response({"error": "Indicator period not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = IndicatorPeriodResponseSerializer(indicator_period)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_latest_indicator_period(request, output_indicator_id):
    indicator_period = IndicatorPeriod.objects.filter(output_indicator_id=output_indicator_id).order_by('-created_at').first()
    if indicator_period is None:
        return Response({"error": "Indicator Period not found"}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = IndicatorPeriodResponseSerializer(indicator_period)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_indicator_period(request, period_id):
    try:
        indicator_period = IndicatorPeriod.objects.get(id=period_id)
    except IndicatorPeriod.DoesNotExist:
        return Response({"error": "Indicator period not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = IndicatorPeriodCreateSerializer(indicator_period, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_serializer = IndicatorPeriodResponseSerializer(indicator_period)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_indicator_period(request, period_id):
    try:
        indicator_period = IndicatorPeriod.objects.get(id=period_id)
    except IndicatorPeriod.DoesNotExist:
        return Response({"error": "Indicator period not found"}, status=status.HTTP_404_NOT_FOUND)

    indicator_period.deleted = True
    indicator_period.save()
    return Response({"message": "Indicator Period deleted successfully"}, status=status.HTTP_200_OK)


class OutputActualRetrieve(generics.RetrieveAPIView):
    queryset = OutputActual.objects.all()
    serializer_class = OutputActualSerializer

class OutputActualByOutputIndicatorCurrentYear(generics.ListAPIView):
    serializer_class = OutputActualSerializer  # Specify the serializer class for serialization

    def get_queryset(self):
        output_indicator_id = self.kwargs['output_indicator_id']
        current_year = timezone.now().year  # Get the current year dynamically
        return OutputActual.objects.filter(output_indicator_id=output_indicator_id, year=current_year)
    
class SpecialReportingPermissionListCreate(generics.ListCreateAPIView):
    queryset = SpecialReportingPermission.objects.all()
    serializer_class = SpecialReportingPermissionSerializer

class SpecialReportingPermissionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecialReportingPermission.objects.all()
    serializer_class = SpecialReportingPermissionSerializer


class GrantSpecialReportingPermissionView(generics.CreateAPIView):
    serializer_class = SpecialReportingPermissionSerializer

    def create(self, request, *args, **kwargs):
        institution_id = request.data.get('institution_id')
        output_reporting_period_id = request.data.get('output_reporting_period_id')
        expires_at = datetime.now() + timedelta(days=14)  # Example grace period of 14 days

        permission, created = SpecialReportingPermission.objects.get_or_create(
            institution_id=institution_id,
            output_reporting_period_id=output_reporting_period_id,
            defaults={'expires_at': expires_at}
        )

        if not created:
            return Response({"message": "Permission already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Special reporting permission granted."}, status=status.HTTP_201_CREATED)



    
class OutputReportingPeriodListCreate(generics.ListCreateAPIView):
    queryset = OutputReportingPeriod.objects.all()
    serializer_class = OutputReportingPeriodSerializer

    def create(self, request, *args, **kwargs):
        output_label = request.data.get('output_label')
        current_year = date.today().year

        # Adjust start and end dates based on the provided logic
        if output_label == 'Q1':
            start_date = date(current_year, 4, 15)
            end_date = date(current_year, 7, 14)
        elif output_label == 'Q2':
            start_date = date(current_year, 7, 15)
            end_date = date(current_year, 10, 14)
        elif output_label == 'Q3':
            start_date = date(current_year, 10, 15)
            end_date = date(current_year + 1, 1, 14)
        elif output_label == 'Q4':
            start_date = date(current_year + 1, 1, 15)
            end_date = date(current_year + 1, 4, 14)
        else:
            return Response({"message": "Invalid output label."}, status=status.HTTP_400_BAD_REQUEST)

        # Deactivate all periods and activate the current one
        OutputReportingPeriod.objects.update(is_active=False)
        is_active = True if output_label == 'Q1' else False

        data = {
            'output_label': output_label,
            'start_date': start_date,
            'end_date': end_date,
            'is_active': is_active,
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)    

class ActiveOutputReportingPeriodRetrieve(generics.ListAPIView):
    serializer_class = OutputReportingPeriodSerializer

    def get_queryset(self):
        return OutputReportingPeriod.objects.filter(is_active=True)
    
class OutputReportingPeriodRetrieve(generics.RetrieveAPIView):
    queryset = OutputReportingPeriod.objects.all()
    serializer_class = OutputReportingPeriodSerializer
    
    
class OutputReportingPeriodUpdate(generics.UpdateAPIView):
    queryset = OutputReportingPeriod.objects.all()
    serializer_class = OutputReportingPeriodSerializer
    
class OutputReportingPeriodDestroy(generics.DestroyAPIView):
    queryset = OutputReportingPeriod.objects.all()
    serializer_class = OutputReportingPeriodSerializer
    
    
class OutputReportingPeriodList(generics.ListAPIView):
    queryset = OutputReportingPeriod.objects.all()
    serializer_class = OutputReportingPeriodSerializer

class CurrentOutputReportingPeriod(generics.ListAPIView):
    serializer_class = OutputReportingPeriodSerializer

    def get_queryset(self):
        current_date = timezone.now().date()
        return OutputReportingPeriod.objects.filter(
            is_active=True,
            start_date__lte=current_date,
            end_date__gte=current_date
        )


class OutputActualCreateView(generics.CreateAPIView):
    serializer_class = OutputActualSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save output_actual instance, which will automatically adjust ACR and extra_acr
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OutputACRCreateView(generics.CreateAPIView):
    serializer_class = OutputACRSerializer

    def create(self, request, *args, **kwargs):
        output_id = request.data.get('output')
        year = request.data.get('year')

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(is_active=True).first()
        if not active_period:
            return Response({"message": "No active output reporting period found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all OutputActuals for the given output and year
        output_actuals = OutputActual.objects.filter(output_indicator__output_id=output_id, year=year)

        if not output_actuals.exists():
            return Response({"message": "No output actuals found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the average ACR and extra ACR
        total_acr = 0
        count = 0
        for output_actual in output_actuals:
            acr = output_actual.ACR
            

            total_acr += acr 
            count += 1

        average_acr = total_acr / count if count > 0 else 0
        

        # Create or update OutputACR with output_reporting_period set to active_period
        output_acr, created = OutputACR.objects.update_or_create(
            output_id=output_id,
            year=year,
            defaults={'average_acr': average_acr, 'output_reporting_period': active_period, 'deleted': False}
        )

        serializer = self.get_serializer(output_acr)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
class OutputACRListView(generics.ListAPIView):
    queryset = OutputACR.objects.filter(deleted=False)
    serializer_class = OutputACRSerializer

class OutputACRDetailView(generics.RetrieveAPIView):
    queryset = OutputACR.objects.filter(deleted=False)
    serializer_class = OutputACRSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except OutputACR.DoesNotExist:
            return Response({"message": "OutputACR not found."}, status=status.HTTP_404_NOT_FOUND)
        
class OutputACRByOutputIDView(generics.ListAPIView):
    serializer_class = OutputACRSerializer

    def get_queryset(self):
        output_id = self.kwargs['output_id']
        return OutputACR.objects.filter(output_id=output_id, deleted=False)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No OutputACR found for the specified output ID."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class ReformAreaACRCreateView(generics.CreateAPIView):
    serializer_class = ReformAreaACRSerializer

    def create(self, request, *args, **kwargs):
        year = request.data.get('year')

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(is_active=True).first()
        if not active_period:
            return Response({"message": "No active output reporting period found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the latest year from ReformArea
        latest_year = ReformArea.objects.aggregate(Max('year'))['year__max']
        if not latest_year:
            return Response({"message": "No reform areas found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all ReformAreas for the latest year
        reform_areas = ReformArea.objects.filter(year=latest_year, deleted=False)
        if not reform_areas.exists():
            return Response({"message": "No reform areas found."}, status=status.HTTP_404_NOT_FOUND)

        reform_area_acrs = []

        # Iterate through each ReformArea
        for reform_area in reform_areas:
            # Get all Outputs for the current ReformArea
            outputs = Output.objects.filter(reform_area=reform_area, deleted=False)

            total_acr = 0
            count = 0
            output_ids_with_acr = []

            # Calculate total ACR for all outputs under the current ReformArea
            for output in outputs:
                output_acrs = OutputACR.objects.filter(output=output, year=year, deleted=False)
                
                if output_acrs.exists():
                    output_ids_with_acr.append(output.id)

                for output_acr in output_acrs:
                    total_acr += output_acr.average_acr
                    count += 1

            # Calculate average ACR for the current ReformArea
            average_acr = total_acr / count if count > 0 else 0
            
            # Logging the output ids with ACR and averages
            print(f"Reform Area ID: {reform_area.id}")
            print(f"Output IDs with ACR: {output_ids_with_acr}")
            print(f"Total ACR: {total_acr}")
            print(f"Count of Output ACRs: {count}")
            print(f"Average ACR for Reform Area: {average_acr}")

            try:
                with transaction.atomic():
                    # Check if a ReformAreaACR already exists for this reform_area and year
                    reform_area_acr, created = ReformAreaACR.objects.update_or_create(
                        reform_area=reform_area,
                        year=year,
                        defaults={
                            'average_acr': average_acr,
                            'output_reporting_period': active_period,
                            'deleted': False
                        }
                    )
                    # Add Output IDs with ACR to reform_area_acr for logging
                    reform_area_acrs.append({
                        'reform_area_acr': reform_area_acr,
                        'output_ids_with_acr': output_ids_with_acr
                    })

            except IntegrityError:
                return Response({"message": f"Duplicate entry for reform_area {reform_area} and year {year}."}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare the response data
        response_data = []
        for item in reform_area_acrs:
            reform_area_acr_data = ReformAreaACRSerializer(item['reform_area_acr']).data
            reform_area_acr_data['output_ids_with_acr'] = item['output_ids_with_acr']
            response_data.append(reform_area_acr_data)

        return Response(response_data, status=status.HTTP_201_CREATED)

    
    
class ThematicAreaACRListView(generics.ListAPIView):
    serializer_class = ThematicAreaACRSerializer

    def get_queryset(self):
        thematic_area_id = self.kwargs['thematic_area_id']
        return ThematicAreaACR.objects.filter(thematic_area_id=thematic_area_id, deleted=False)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReformAreaACRByOutputReportingPeriod(generics.ListAPIView):
    serializer_class = ReformAreaACRSerializer

    def get_queryset(self):
        output_reporting_period_id = self.kwargs['output_reporting_period_id']
        # Get the latest year for the given output_reporting_period_id
        latest_year = ReformAreaACR.objects.filter(output_reporting_period_id=output_reporting_period_id).aggregate(Max('year'))['year__max']
        # Return the entries with the latest year
        return ReformAreaACR.objects.filter(output_reporting_period_id=output_reporting_period_id, year=latest_year)
    
class ReformAreaACRByOutputReportingPeriodAndReformArea(generics.ListAPIView):
    serializer_class = ReformAreaACRSerializer

    def get_queryset(self):
        output_reporting_period_id = self.kwargs['output_reporting_period_id']
        reform_area_id = self.kwargs['reform_area_id']

        # Get the latest year for the given output_reporting_period_id and reform_area_id
        latest_year = ReformAreaACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            reform_area_id=reform_area_id
        ).aggregate(Max('year'))['year__max']

        # Return the entries with the latest year
        return ReformAreaACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            reform_area_id=reform_area_id,
            year=latest_year
        )
        


class ReformAreaACRByReformArea(generics.ListAPIView):
    serializer_class = ReformAreaACRSerializer

    def get_queryset(self):
        reform_area_id = self.kwargs['reform_area_id']

        # Subquery to get the latest created_at date for each reform_area_id
        latest_acr_subquery = ReformAreaACR.objects.filter(
            reform_area_id=OuterRef('reform_area_id')
        ).order_by('-created_at').values('created_at')[:1]

        # Subquery to get the latest output_reporting_period_id based on latest created_at date
        latest_output_reporting_period_subquery = ReformAreaACR.objects.filter(
            reform_area_id=reform_area_id,
            created_at=Subquery(latest_acr_subquery)
        ).values('output_reporting_period_id')[:1]

        # Filter the ReformAreaACR entries based on the latest output_reporting_period_id
        return ReformAreaACR.objects.filter(
            reform_area_id=reform_area_id,
            output_reporting_period_id=Subquery(latest_output_reporting_period_subquery)
        )

        
class ThematicAreaACRCreateView(generics.CreateAPIView):
    serializer_class = ThematicAreaACRSerializer

    def create(self, request, *args, **kwargs):
        year = request.data.get('year')

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(is_active=True).first()
        if not active_period:
            return Response({"message": "No active output reporting period found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all ReformAreas for the given year
        reform_areas = ReformArea.objects.filter(year=year, deleted=False)
        if not reform_areas.exists():
            return Response({"message": "No reform areas found."}, status=status.HTTP_404_NOT_FOUND)

        thematic_acrs = {}

        for reform_area in reform_areas:
            thematic_area_id = reform_area.thematic_area_id
            if thematic_area_id not in thematic_acrs:
                thematic_acrs[thematic_area_id] = {
                    "total_acr": 0,
                    "count": 0
                }

            reform_area_acrs = ReformAreaACR.objects.filter(reform_area_id=reform_area.id, year=year, deleted=False)
            for acr in reform_area_acrs:
                thematic_acrs[thematic_area_id]["total_acr"] += acr.average_acr
                thematic_acrs[thematic_area_id]["count"] += 1

        thematic_area_acr_list = []
        for thematic_area_id, acr_data in thematic_acrs.items():
            if acr_data["count"] > 0:
                total_acr = acr_data["total_acr"]
                count = acr_data["count"]
                average_acr = total_acr / count
             
                

                try:
                    with transaction.atomic():
                        thematic_area_acr, created = ThematicAreaACR.objects.update_or_create(
                            thematic_area_id=thematic_area_id,
                            year=year,
                            defaults={
                                'average_acr': average_acr,
                                'output_reporting_period': active_period,
                                'deleted': False
                            }
                        )
                        thematic_area_acr_list.append(thematic_area_acr)
                except IntegrityError:
                    return Response({"message": f"Duplicate entry for thematic_area {thematic_area_id} and year {year}."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(thematic_area_acr_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
             
class GrantSpecialReportingPermissionView(generics.CreateAPIView):
    queryset = SpecialReportingPermission.objects.all()
    serializer_class = SpecialReportingPermissionSerializer
    
class ReformAreaCriteriaCreateView(generics.CreateAPIView):
    queryset = ReformAreaCriteria.objects.all()
    serializer_class = ReformAreaCriteriaSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReformAreaCriteriaSerializer
        return ReformAreaCriteriaSerializer
    
    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        reform_area_id = self.request.data.get('reform_area')
        
        # Check if a record with the given reform_area_id already exists
        existing_record = ReformAreaCriteria.objects.filter(reform_area_id=reform_area_id).first()
        
        if existing_record:
            # Update existing record
            serializer.instance = existing_record
            serializer.validated_data['updated_at'] = timezone.now()  # Update the timestamp
            serializer.save()
        else:
            # Create a new record
            serializer.save()
    
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        security = Security()
        security.secureAccess("create_user", user_id)
        
        reform_area_id = request.data.get('reform_area')
        
        # Check if a record with the given reform_area_id already exists
        existing_record = ReformAreaCriteria.objects.filter(reform_area_id=reform_area_id).first()
        
        if existing_record:
            # Update existing record
            serializer = self.get_serializer(existing_record, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Create a new record
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_update(self, serializer):
        serializer.save()
    
class ReformAreaSectorCreateView(generics.CreateAPIView):
    queryset = ReformAreaSector.objects.all()
    serializer_class = ReformAreaSectorSerializer

class ReformAreaSectorListView(generics.ListAPIView):
    queryset = ReformAreaSector.objects.all()
    serializer_class = ReformAreaSectorSerializer

class ReformAreaSectorDetailView(generics.RetrieveAPIView):
    queryset = ReformAreaSector.objects.all()
    serializer_class = ReformAreaSectorSerializer

class ReformAreaSectorUpdateView(generics.UpdateAPIView):
    queryset = ReformAreaSector.objects.all()
    serializer_class = ReformAreaSectorSerializer

class ReformAreaSectorDeleteView(generics.DestroyAPIView):
    queryset = ReformAreaSector.objects.all()
    serializer_class = ReformAreaSectorSerializer
    
class ReformAreaSectorMappingCreateView(generics.CreateAPIView):
    queryset = ReformAreaSectorMapping.objects.all()
    serializer_class = ReformAreaSectorMappingSerializer

class ReformAreaSectorMappingListView(generics.ListAPIView):
    queryset = ReformAreaSectorMapping.objects.all()
    serializer_class = ReformAreaSectorMappingSerializer

class ReformAreaSectorMappingDetailView(generics.RetrieveAPIView):
    queryset = ReformAreaSectorMapping.objects.all()
    serializer_class = ReformAreaSectorMappingSerializer

class ReformAreaSectorMappingUpdateView(generics.UpdateAPIView):
    queryset = ReformAreaSectorMapping.objects.all()
    serializer_class = ReformAreaSectorMappingSerializer

class ReformAreaSectorMappingDeleteView(generics.DestroyAPIView):
    queryset = ReformAreaSectorMapping.objects.all()
    serializer_class = ReformAreaSectorMappingSerializer
    
class ReformCategoryCreateView(generics.CreateAPIView):
    queryset = ReformCategory.objects.all()
    serializer_class = ReformCategorySerializer

class ReformCategoryListView(generics.ListAPIView):
    queryset = ReformCategory.objects.all()
    serializer_class = ReformCategorySerializer

class ReformCategoryDetailView(generics.RetrieveAPIView):
    queryset = ReformCategory.objects.all()
    serializer_class = ReformCategorySerializer

class ReformCategoryUpdateView(generics.UpdateAPIView):
    queryset = ReformCategory.objects.all()
    serializer_class = ReformCategorySerializer

class ReformCategoryDeleteView(generics.DestroyAPIView):
    queryset = ReformCategory.objects.all()
    serializer_class = ReformCategorySerializer

class ReformCategoryMappingCreateView(generics.CreateAPIView):
    queryset = ReformCategoryMapping.objects.all()
    serializer_class = ReformCategoryMappingSerializer

class ReformCategoryMappingListView(generics.ListAPIView):
    queryset = ReformCategoryMapping.objects.all()
    serializer_class = ReformCategoryMappingSerializer

class ReformCategoryMappingDetailView(generics.RetrieveAPIView):
    queryset = ReformCategoryMapping.objects.all()
    serializer_class = ReformCategoryMappingSerializer

class ReformCategoryMappingUpdateView(generics.UpdateAPIView):
    queryset = ReformCategoryMapping.objects.all()
    serializer_class = ReformCategoryMappingSerializer

class ReformCategoryMappingDeleteView(generics.DestroyAPIView):
    queryset = ReformCategoryMapping.objects.all()
    serializer_class = ReformCategoryMappingSerializer

class OutputProgressListCreate(generics.ListCreateAPIView):
    queryset = OutputProgress.objects.filter(deleted=False)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return OutputProgressSerializer
    
    def perform_create(self, serializer):
        reform_area_id = self.request.data.get('reform_area')
        output_reporting_period_id = self.request.data.get('output_reporting_period')
        progress = self.request.data.get('progress')

        if reform_area_id and output_reporting_period_id:
            try:
                existing_entry = OutputProgress.objects.get(
                    reform_area_id=reform_area_id,
                    output_reporting_period_id=output_reporting_period_id,
                    deleted=False
                )
                existing_entry.progress = progress
                existing_entry.save()
                self.serializer = self.get_serializer(existing_entry)
                self.created = False
            except OutputProgress.DoesNotExist:
                serializer.save()
                self.created = True

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if hasattr(self, 'created') and not self.created:
            return Response(self.serializer.data, status=status.HTTP_200_OK)
        return response 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_progress_by_id(request, progress_id):
    output_progress = get_object_or_404(OutputProgress, id=progress_id)
    serializer = OutputProgressSerializer(output_progress)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_output_progress(request, progress_id):
    try:
        output_progress = OutputProgress.objects.get(id=progress_id)
    except OutputProgress.DoesNotExist:
        return Response({"error": "Output Progress not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OutputProgressSerializer(output_progress, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_output_progress(request, progress_id):
    try:
        output_progress = OutputProgress.objects.get(id=progress_id)
        output_progress.deleted = True
        output_progress.save()
        return Response({"message": "Output Progress deleted successfully"}, status=status.HTTP_200_OK)
    except OutputProgress.DoesNotExist:
        return Response({"error": "Output Progress not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_progresses_by_reform_area(request, reform_area_id):
    try:
        reform_area = ReformArea.objects.get(id=reform_area_id)
    except ReformArea.DoesNotExist:
        return Response({"error": "Reform Area not found"}, status=status.HTTP_404_NOT_FOUND)
    
    output_progresses = OutputProgress.objects.filter(reform_area=reform_area, deleted=False)
    serializer = OutputProgressSerializer(output_progresses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_output_progresses(request):
    output_progresses = OutputProgress.objects.filter(deleted=False)
    serializer = OutputProgressSerializer(output_progresses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class EndofContractOutputACRView(generics.CreateAPIView):
    serializer_class = EndofContractOutputACRSerializer

    def create(self, request, *args, **kwargs):
        output_id = request.data.get('output')
        year = request.data.get('year')

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(is_active=True).first()
        if not active_period:
            return Response({"message": "No active output reporting period found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all OutputActuals for the given output and year
        output_actuals = OutputActual.objects.filter(output_indicator__output_id=output_id, year=year)

        if not output_actuals.exists():
            return Response({"message": "No output actuals found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the average ACR
        total_acr = sum(float(output_actual.ACR) for output_actual in output_actuals)
        count = output_actuals.count()
        average_acr = total_acr / float(count) if count > 0 else 0.0

        print(f"Output ID: {output_id}")
        print(f"Year: {year}")
        print(f"Total ACR: {total_acr}")
        print(f"Count of Output Actuals: {count}")
        print(f"Average ACR: {average_acr}")

        # Retrieve OutputWeights for the given output and year
        end_contract_weights = EndContractOutputWeights.objects.filter(output_id=output_id, year=year).first()


        if not end_contract_weights:
            return Response({"message": "No output weights found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

        # Determine the correct weight based on the active reporting period
        if active_period.output_label == 'Q1':
            weight = float(end_contract_weights.Q1w)
            weighted_acr = average_acr * weight
        elif active_period.output_label == 'Q2':
            weight = float(end_contract_weights.Q2w)
            weighted_acr = average_acr * weight
            
            # Retrieve previous quarter's end_contract_average_acr (Q1)
            previous_acr = EndofContractOutputACR.objects.filter(output_id=output_id, year=year, output_reporting_period__output_label='Q1').first()
            if previous_acr:
                weighted_acr += float(previous_acr.end_contract_average_acr)
        elif active_period.output_label == 'Q3':
            weight = float(end_contract_weights.Q3w)
            weighted_acr = average_acr * weight
            
            # Retrieve previous quarter's end_contract_average_acr (Q2)
            previous_acr = EndofContractOutputACR.objects.filter(output_id=output_id, year=year, output_reporting_period__output_label='Q2').first()
            if previous_acr:
                weighted_acr += float(previous_acr.end_contract_average_acr)
        elif active_period.output_label == 'Q4':
            weight = float(end_contract_weights.Q4w)
            weighted_acr = average_acr * weight
            
            # Retrieve previous quarter's end_contract_average_acr (Q3)
            previous_acr = EndofContractOutputACR.objects.filter(output_id=output_id, year=year, output_reporting_period__output_label='Q3').first()
            if previous_acr:
                weighted_acr += float(previous_acr.end_contract_average_acr)
        else:
            return Response({"message": "Invalid reporting period."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Active Period: {active_period.output_label}")
        print(f"Weight Used: {weight}")
        print(f"Weighted ACR: {weighted_acr}")

        # Create or update EndofContractOutputACR with weighted ACR and active reporting period
        end_of_contract_acr, created = EndofContractOutputACR.objects.update_or_create(
            output_id=output_id,
            year=year,
            output_reporting_period=active_period,
            defaults={
                'end_contract_average_acr': weighted_acr,
                'deleted': False
            }
        )

        serializer = self.get_serializer(end_of_contract_acr)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    

@api_view(['GET'])
def get_end_contract_output_weights(request, output_id, year):
    # Retrieve the EndContractOutputWeights for the specified output and year
    end_contract_weights = EndContractOutputWeights.objects.filter(output_id=output_id, year=year).first()

    if not end_contract_weights:
        return Response({"message": "No end contract output weights found for the specified output and year."}, status=status.HTTP_404_NOT_FOUND)

    serializer = EndContractOutputWeightsSerializer(end_contract_weights)
    return Response(serializer.data, status=status.HTTP_200_OK)


class EndContractReformAreaACRCreateView(generics.CreateAPIView):
    serializer_class = EndofContractOutputACRSerializer

    def create(self, request, *args, **kwargs):
        year = request.data.get('year')
        output_reporting_period_id = request.data.get('output_reporting_period_id')

        print(f"Received data - Year: {year}, Output Reporting Period ID: {output_reporting_period_id}")

        # Get active output reporting period
        active_period = OutputReportingPeriod.objects.filter(id=output_reporting_period_id).first()
        if not active_period:
            print(f"Invalid output reporting period ID: {output_reporting_period_id}")
            return Response({"message": "Invalid output reporting period."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the latest year from ReformArea
        latest_year = ReformArea.objects.aggregate(Max('year'))['year__max']
        print(f"Latest year from ReformArea: {latest_year}")

        if not latest_year:
            print("No reform areas found.")
            return Response({"message": "No reform areas found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all ReformAreas for the latest year
        reform_areas = ReformArea.objects.filter(year=latest_year, deleted=False)
        if not reform_areas.exists():
            print("No reform areas found for the latest year.")
            return Response({"message": "No reform areas found for the latest year."}, status=status.HTTP_404_NOT_FOUND)

        # Iterate over each reform area and calculate average ACR
        for reform_area in reform_areas:
            # Get all EndContractOutputACR for the current ReformArea and active output reporting period
            related_end_contract_acrs = EndofContractOutputACR.objects.filter(
                output__reform_area=reform_area,
                year=year,
                deleted=False,
                output_reporting_period_id=output_reporting_period_id
            )
            print(f"Related EndContractOutputACR count for ReformArea ID {reform_area.id}: {related_end_contract_acrs.count()}")

            # Calculate average ACR for the current ReformArea
            end_contract_output_acrs = related_end_contract_acrs.values_list('end_contract_average_acr', flat=True)
            print(f"End Contract Output ACRs for ReformArea ID {reform_area.id}: {list(end_contract_output_acrs)}")

            if end_contract_output_acrs:
                average_acr = sum(end_contract_output_acrs) / len(end_contract_output_acrs)
            else:
                average_acr = 0
            print(f"Calculated average ACR for ReformArea ID {reform_area.id}: {average_acr}")

            # Check if there's an existing record with the same reform_area, year, and output reporting period
            existing_acr = EndContractReformAreaACR.objects.filter(
                reform_area=reform_area,
                year=year,
                output_reporting_period=active_period
            ).first()
            print(f"Existing ACR record for ReformArea ID {reform_area.id}: {existing_acr}")

            if existing_acr:
                # Update existing entry
                try:
                    with transaction.atomic():
                        existing_acr.average_acr = average_acr
                        existing_acr.save()
                        print(f"Updated existing entry for ReformArea ID {reform_area.id}.")
                except IntegrityError as e:
                    print(f"Error updating entry for ReformArea ID {reform_area.id}: {e}")
                    return Response({"message": "Error updating entry."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Create new entry
                try:
                    with transaction.atomic():
                        EndContractReformAreaACR.objects.create(
                            reform_area=reform_area,
                            year=year,
                            average_acr=average_acr,
                            output_reporting_period=active_period,
                            deleted=False
                        )
                        print(f"Created new entry for ReformArea ID {reform_area.id}.")
                except IntegrityError as e:
                    print(f"Error creating entry for ReformArea ID {reform_area.id}: {e}")
                    return Response({"message": "Error creating entry."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "End Contract Reform Area ACRs processed successfully."}, status=status.HTTP_200_OK)
    

class EndContractReformAreaACRByOutputReportingPeriodAndReformArea(generics.ListAPIView):
    serializer_class = EndContractReformAreaACRSerializer

    def get_queryset(self):
        output_reporting_period_id = self.kwargs['output_reporting_period_id']
        reform_area_id = self.kwargs['reform_area_id']

        related_outputs = Output.objects.filter(reform_area_id=reform_area_id)

        latest_year = EndofContractOutputACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            output__in=related_outputs
        ).aggregate(Max('year'))['year__max']

        return EndContractReformAreaACR.objects.filter(
            output_reporting_period_id=output_reporting_period_id,
            reform_area_id=reform_area_id,
            year=latest_year
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'output_reporting_period_id': self.kwargs['output_reporting_period_id']
        })
        return context
