from django.forms import ModelForm    #imported the form class
from app.models import TODO             #imported our TODO
                
class TODOForm (ModelForm):            #passed all the attributes of modelform to our TODOform class
    class Meta:                         
        model = TODO                    # here we tell django what is the model name
        fields = ['title', 'status', 'priority']
