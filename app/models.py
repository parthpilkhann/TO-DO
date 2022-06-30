from django.db import models    # from "django.db" package we imported models module 
from django.contrib.auth.models import User   # imported User model

class TODO(models.Model):           # a TODO class is created and arguments are passed so that our TODO class inherits all the attributes of the 'Model' class which are present in 'models' module.
    status_choices = [              # a list is created which holds status choices
    ('C', 'completed'),
    ('P', 'pending')
    ]
    priority_choices= [
        ('1', '1️⃣'),
        ('2', '2️⃣'),
        ('3', '3️⃣'),
        ('4', '4️⃣'),
        ('5', '5️⃣'),
        ('6', '6️⃣'),
        ('7', '7️⃣'),
        ('8', '8️⃣'),
        ('9', '9️⃣'),
        ('10', '🔟'),
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices = status_choices)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices = priority_choices)
    user = models.ForeignKey( User, on_delete=models.CASCADE )     # how to use foreign key---> https://riptutorial.com/django/example/30649/foreignkey
                                                                    # here it maps the attributes of 'User' class in django to our variable named  'user'.
                                                                    # on_delete means if we delete a user here, all its TODO's also get deleted because the command is defined in foreignkey and is defined in TODO class.
                                                                    