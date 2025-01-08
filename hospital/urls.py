from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, DoctorViewSet, PharmacistViewSet,
    ReportViewSet, SupportTicketViewSet, PatientDiagnosisViewSet,
    AppointmentViewSet, MedicineInventoryViewSet,  DoctorProfileViewSet, 
    SupportViewSet, AppointmentsViewSet, ContactViewSet,
    AdminRegistrationView, 
    DoctorRegistrationView, PharmacistRegistrationView, DoctorLoginView, PharmacistLoginView,
    AdminRegistrationView, AdminLoginView, PharmacistViewSet, AdminViewSet, TotalStockValueView,
    
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'pharmacists', PharmacistViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'support-tickets', SupportTicketViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'patient-diagnosis', PatientDiagnosisViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'medicines', MedicineInventoryViewSet)
router.register(r'doctorprofiles', DoctorProfileViewSet)
router.register(r'supports', SupportViewSet)
router.register(r'medappointment', AppointmentsViewSet)
router.register(r'admins', AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/patients/count/', PatientViewSet.as_view({'get': 'get_patient_count'}), name='patient-count'),
    path('api/doctors/count/', DoctorViewSet.as_view({'get': 'get_doctor_count'}), name='doctor-count'),
    path('api/pharmacists/count/', PharmacistViewSet.as_view({'get': 'get_pharmacist_count'}), name='pharmacist-count'),
    path('api/admins/count/', AdminViewSet.as_view({'get': 'get_admin_count'}), name='admin-count'),
    path('api/appointments/count/', AppointmentsViewSet.as_view({'get': 'get_appointments_count'}), name='appointments-count'),
    path('api/medicines/count/', MedicineInventoryViewSet.as_view({'get': 'get_medicine_count'}), name='medicines-count'),
    path('api/medicines/total-stock-value/', TotalStockValueView.as_view(), name='total-stock-value'),
    
    
    path('auth/register/admin/', AdminRegistrationView.as_view(), name='register-admin'),
    path('auth/register/doctor/', DoctorRegistrationView.as_view(), name='register-doctor'),
    path('auth/register/pharmacist/', PharmacistRegistrationView.as_view(), name='register-pharmacist'),
    path('auth/login/doctor/', DoctorLoginView.as_view(), name='login-doctor'),
    path('auth/login/pharmacist/', PharmacistLoginView.as_view(), name='login-pharmacist'),
    path('auth/login/admin/', AdminLoginView.as_view(), name='login-admin'),
    
]