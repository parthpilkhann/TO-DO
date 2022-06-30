from telnetlib import STATUS
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # usercreationform for signup and authentication form for checking the authentication. they are both functions, their objects have to be created  and then be used
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loginUser, logout
from app.forms import TODOForm
from app.models import TODO


@login_required(login_url='login')
def home(request):          # this request object carries a lot of info with itself like (body saath thi kya?, url kya tha?, body mein form ki info., etc.)
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')         # here 2 objects are formed i.e todos and form, and rather than doing it by creating a variable named context (like in signup), we did it in the paranthesis itself.
        return render(request, 'index.html', context = { 'form' : form , 'todos' : todos})            # the second arg is directly taken from templates folder, if the file was within a folder inside the template folder,we would have to write the templates name
                                                        # files name should always be within apostrophe


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()               # created an object of the method usercreationform (an inbuilt form which we imported especially created for signup) and stored the object in the form variable.
        context = {
            "form": form        # in this we formed a dictionary type variable named context and bound its key named "form" to our object created (form) dont get confused, its like x=2.
        }                       # here context is made so that we can show the form we made here in the html page.
        return render(request, 'signup.html', context=context)  #here 'return render fn.' is used to send the control to signup.html and through context we are sending the form to the signup.html . 

    else:
        form = UserCreationForm(request.POST)   # the argument is for accessing the data
        if form.is_valid():
            user = form.save()  #save the data
            if form is not None:
                return redirect('login')        
        else:                   #if form is invalid, reload the page
            form = UserCreationForm()
            context = {
            "form": form
            }
            return render(request, 'signup.html', context=context)


def login(request):
    form = AuthenticationForm(data=request.POST)    # argument is for accessing the data, note that it is different from argument passed in usercreation form
    if request.method == 'GET':         #if request is get, we reload the page.
        context = {
            "form":form
        }
        return render(request, 'login.html', context=context)
    else:
        if form.is_valid():
            username = form.cleaned_data.get('username')     #accessed the data and stored in variable
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password) # we check if the username and password matches one of the users who signed up
            if user is not None:
                loginUser(request, user)                # we tell django to keep us logged in until we close the session
                return redirect('home')                 #send us to home where we can perform our operation
        else:
            context = {
            "form":form
            }
            return render(request, 'login.html', context=context)


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:      #if the user is logged in then only we can add the todo data
        user = request.user                 #stored the user's data in variable user.
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)            #prints the added data in the terminal
            todo = form.save(commit=False)      #  here we update the form object and let them know that don't save the values in the database right now, we might change some input with instance and then use .save() to save all values in the database.
                                                # This gives us the flexibility to get all values from the HTML form and customize them according to our requirement and then save the instance.
            todo.user = user
            todo.save()
            print (todo)
            return redirect ('home')            #sends home in both cases but in else case it send us to home with error. 
        else:
            return render(request, 'index.html', context = { 'form' : form })


def signout(request):
    logout(request)
    return redirect ('login')

def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect('home')

def change_status(request, id, status):# (pk = primary key)here we accessed that data whose pk is our id and made it an object and stored the object in todo variable i.e django asked us through pk "kis cheez ka obj get krna h" and we said id ka.
                                                #whats happeneing here is---> hamne index.html me code likha h agr status 'P' ho to url me (/change_status/{{todo.id}}/C) bhejo and vice versa. now, jab control url me (change_status) dekhega to vo url.py me jaega and uske saath 2 or cheeze jaengi, (change_status/<int:id>/<str:status>) id and status jo ki already url me pass ho chuka hoga,
                                                #  ab url se control views.py me jaega, and usme (change_status) function me arguments me data pass ho jaega i.e path function ne url ke andr se data uthha ke change_status fn. ki arguments me data pass krdia. ab functions ki arguments me 2 cheezein stored h (jis todo pe click kia h uski id and url me likha status).
    todo = TODO.objects.get(pk=id)           #this line means --> url me id pass hui h uska original data 'todo' me store krana.  i.e suppose hmara todo pending ('P') tha to url me 'C' pass hoga but hmare 'todo' me to original data 'P' hi jaega.     
    todo.status = status                    # iss code me hamne, 'todo.status' se original data access kia and '= status' se hmne original khatam krke use argument wala status assign krdia.  
    todo.save()
    return redirect ('home')