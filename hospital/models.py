from django.db import models
from django.http import JsonResponse
import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomToken(models.Model):
    key = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.OneToOneField('Admin', on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.OneToOneField('MedDoctor', on_delete=models.CASCADE, null=True, blank=True)
    pharmacist = models.OneToOneField('Pharmacist', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255, blank=True, null=True)  # Token field

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Validate hashed password

    def generate_token(self):
        self.token = str(uuid.uuid4())
        self.save()


# Patient Model
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    
class MedDoctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255, blank=True, null=True)  # Token field

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Compare raw password with hashed password

    def generate_token(self):
        self.token = str(uuid.uuid4())
        self.save()
    
###### DoctorProfile Model #############
class DoctorProfile(models.Model):
    doctor = models.ForeignKey(MedDoctor, on_delete=models.CASCADE)
    address = models.TextField()  # Doctor's address

    def __str__(self):
        return self.doctor.name

# Pharmacist Model
class Pharmacist(models.Model):
    pharmacist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255, blank=True, null=True)  # Token field

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # Use Django's check_password function to verify the password
        return check_password(raw_password, self.password)

    def generate_token(self):
        self.token = str(uuid.uuid4())
        self.save()

    def __str__(self):
        return self.email




# Reports Model
class Report(models.Model):
    doctor = models.ForeignKey(MedDoctor, on_delete=models.CASCADE)  # Reference to Doctor
    subject = models.CharField(max_length=255)
    message = models.TextField()


    def __str__(self):
        return self.subject

# Support Tickets Model
class SupportTicket(models.Model):
    ticket_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.ticket_id
    
# Support Model
class Support(models.Model):
    support_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.support_id

#Contacts Model
class Contact(models.Model):
    contact_id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# Patient Diagnosis Model
class PatientDiagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescribed_medicine = models.TextField()
    dosage = models.CharField(max_length=50)
    # next_checkup = models.DateField()

    def __str__(self):
        return f"Diagnosis for {self.patient.name}"

# Appointments Model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Appointment for {self.patient.name} on {self.date}"
    
class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)  # Auto-generated unique ID
    patient_name = models.CharField(max_length=255)  # Patient's name
    date = models.DateField()  # Appointment date
    time = models.TimeField()  # Appointment time

    def __str__(self):
        return f"Appointment {self.appointment_id} for {self.patient_name} on {self.date} at {self.time}"


# Medicine Inventory Model
class MedicineInventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def stock_value(self):
        return self.quantity * self.price
    
def get_doctors_count(request):
    count = MedDoctor.objects.count()
    return JsonResponse({'count': count})

def get_patients_count(request):
    count = Patient.objects.count()
    return JsonResponse({'count': count})

def get_pharmacists_count(request):
    count = Pharmacist.objects.count()
    return JsonResponse({'count': count})

def get_appointments_count(request):
    count = Appointments.objects.count()
    return JsonResponse({'count': count})

def get_admin_count(request):
    count = Admin.objects.count()
    return JsonResponse({'count': count})

def get_medicines_count(request):
    count = MedicineInventory.objects.count()
    return JsonResponse({'count': count})