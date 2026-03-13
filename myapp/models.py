from django.db import models

class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=8)

class Services(models.Model):
    
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    description=models.CharField(max_length=100)
    image = models.ImageField(upload_to='services_images/', default='services_images/default.jpg')

    def __str__(self):
        return self.name



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bookings')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField()
    concerns = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Services, related_name='bookings')  


    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]


    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

class Status(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    service = models.ForeignKey('Services', on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.booking.id} - {self.service.name} - {self.status}"

