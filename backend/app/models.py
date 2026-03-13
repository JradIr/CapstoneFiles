from django.db import models

class Users(models.Model): 
    username = models.CharField(max_length=200, unique=True)
    password_hash = models.TextField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AdminAccounts(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
        ('maker', 'Maker'),
        ('admin', 'Admin'),
    ]

    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('waiting', 'Waiting'),
    ]

    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        'Users',  # assuming you have a User model for patients
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    staff = models.ForeignKey(
        'AdminAccounts',  # links to your AdminAccount model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointments {self.appointment_id} - {self.patient} with {self.staff} on {self.appointment_date}"

class Treatments(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(
        'Appointments',  # links to Appointment model
        on_delete=models.CASCADE,
        related_name='treatments'
    )
    treatment_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    treatment_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.treatment_type} on {self.treatment_date} (₱{self.cost})"

class Billing(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('bank', 'Bank'),
    ]

    billing_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(
        'Appointments',
        on_delete=models.CASCADE,
        related_name='billings'
    )
    patient = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        related_name='billings'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing {self.billing_id} - {self.patient} ({self.total_amount} via {self.payment_method})"
class MedicalHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        related_name='medical_histories'
    )
    allergies = models.TextField(null=True, blank=True)
    existing_conditions = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    past_treatments = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical History for {self.patient}"

class WaitingList(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('scheduled', 'Scheduled'),
        ('expired', 'Expired'),
    ]

    waiting_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        related_name='waiting_list_entries'
    )
    requested_date = models.DateField()
    priority_score = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WaitingList {self.waiting_id} - {self.patient} ({self.status})"

class Notifications(models.Model):
    TYPE_CHOICES = [
        ('appointment reminder', 'Appointment Reminder'),
        ('billing reminder', 'Billing Reminder'),
        ('system alert', 'System Alert'),
    ]

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('pending', 'Pending'),
        ('read', 'Read'),
    ]

    notification_id = models.AutoField(primary_key=True)
    recipient_user = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    recipient_admin = models.ForeignKey(
        'AdminAccounts',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.notification_id} - {self.type} ({self.status})"

class AuditLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    admin = models.ForeignKey(
        'AdminAccounts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50)
    table_name = models.CharField(max_length=50)
    record_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuditLog {self.log_id} - {self.action} on {self.table_name}"

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    appointment = models.ForeignKey(
        'Appointments',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    rating = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.feedback_id} - {self.patient} ({self.rating}/5)"

class Schedules(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    schedule_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(
        'AdminAccounts',
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.staff} - {self.day_of_week} ({self.start_time} to {self.end_time})"
