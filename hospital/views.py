from rest_framework import viewsets
from .models import (
    Patient, MedDoctor, Pharmacist, Report, SupportTicket, 
    PatientDiagnosis, Appointment, MedicineInventory,Contact, DoctorProfile, Support, Appointments,
    Admin, CustomToken
)
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import uuid
from django.http import HttpResponse

from django.db.models import Sum, F

from .serializers import (
    PatientSerializer, DoctorSerializer, PharmacistSerializer, ContactSerializer,
    ReportSerializer, SupportTicketSerializer, PatientDiagnosisSerializer,
    AppointmentSerializer, MedicineInventorySerializer, CountSerializer, 
    DoctorProfileSerializer, SupportSerializer, AppointmentsSerializer,
    AdminSerializer,
    DoctorRegistrationSerializer, PharmacistRegistrationSerializer, DoctorLoginSerializer, 
    PharmacistLoginSerializer, AdminRegistrationSerializer, AdminLoginSerializer
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

def index(request):
    return HttpResponse("Welcome to my app!")

class AdminRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            token, _ = CustomToken.objects.get_or_create(admin=admin)
            return Response({
                "message": "Admin registered successfully",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorRegistrationView(APIView):
    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This saves the doctor data to Doctor model
            return Response({
                "message": "Doctor registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Doctor Login View
class DoctorLoginView(APIView):
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data
            doctor.generate_token()  # Generate token for the session
            return Response({
                "message": "Login successful",
                "token": doctor.token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PharmacistRegistrationView(APIView):
    def post(self, request):
        serializer = PharmacistRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save pharmacist data to the Pharmacist model
            return Response({
                "message": "Pharmacist registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PharmacistLoginView(APIView):
    def post(self, request):
        serializer = PharmacistLoginSerializer(data=request.data)
        if serializer.is_valid():
            pharmacist = serializer.validated_data
            pharmacist.generate_token()  # Generate token for the session
            return Response({
                "message": "Login successful",
                "token": pharmacist.token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save admin data to the Admin model
            return Response({
                "message": "Admin registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.validated_data
            admin.generate_token()  # Generate a unique token for the session
            return Response({
                "message": "Login successful",
                "token": admin.token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    
    @action(detail=False, methods=['get'], url_path='count') #admin count
    def get_admin_count(self, request):
        count = Admin.objects.count()
        return Response(CountSerializer({'count': count}).data)

class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()  
    serializer_class = AppointmentsSerializer  
    
    @action(detail=False, methods=['get'], url_path='count')
    def get_appointments_count(self, request):
        count = Appointments.objects.count()
        return Response(CountSerializer({'count': count}).data)

class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = MedDoctor.objects.all()
    serializer_class = DoctorSerializer

class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

class PatientDiagnosisViewSet(viewsets.ModelViewSet):
    queryset = PatientDiagnosis.objects.all()
    serializer_class = PatientDiagnosisSerializer

class AppointmentViewSet(viewsets.ModelViewSet): ###duplicate###
    queryset = Appointment.objects.all()  
    serializer_class = AppointmentSerializer 
    

class MedicineInventoryViewSet(viewsets.ModelViewSet):
    queryset = MedicineInventory.objects.all()
    serializer_class = MedicineInventorySerializer
    
    @action(detail=False, methods=['get'], url_path='count')
    def get_medicine_count(self, request):
        count = MedicineInventory.objects.count()
        return Response(CountSerializer({'count': count}).data)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @action(detail=False, methods=['get'], url_path='count')
    def get_patient_count(self, request):
        """
        Returns the total count of patients.
        """
        count = Patient.objects.count()
        return Response(CountSerializer({'count': count}).data)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = MedDoctor.objects.all()
    serializer_class = DoctorSerializer

    @action(detail=False, methods=['get'], url_path='count')
    def get_doctor_count(self, request):
        """
        Returns the total count of doctors.
        """
        count = MedDoctor.objects.count()
        # Use the CountSerializer to return the count
        return Response(CountSerializer({'count': count}).data)
    
class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

    @action(detail=False, methods=['get'], url_path='count')
    def get_pharmacist_count(self, request):
        """
        Returns the total count of pharmacists.
        """
        count = Pharmacist.objects.count()
        # Use the CountSerializer to return the count
        return Response(CountSerializer({'count': count}).data)
    

class TotalStockValueView(APIView):
    def get(self, request, *args, **kwargs):
        total_stock_value = MedicineInventory.objects.aggregate(
            total_value=Sum(F('price') * F('quantity'))
        )['total_value'] or 0
        return Response({"total_stock_value": total_stock_value})