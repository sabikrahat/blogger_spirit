from django.shortcuts import redirect, render
import pymongo
import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from home.models import UserModel

# Create your views here.

def connection():
    # Connect to the MongoDB, change the connection string per your MongoDB environment
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    print(client)

    # Set the db object to point to the business database
    db = client['test_db']
    collection = db['test_collection']

    dictionary = {'name': 'Test Name', 'age': 30, 'created_at': datetime.datetime.utcnow()}
    collection.insert_one(dictionary)

    # Showcasing the count() method of find, count the total number of documents in collection
    print('Total number of documents in collection: ', collection.count_documents({}))


def home(request):
    # isLoggedIn = False
    # try:
    #     if request.session['email'] is not None:
    #         isLoggedIn = True
    # except:
    #     isLoggedIn = False
    
    # if isLoggedIn:
    #     return render(request, 'home.html', {'isLoggedIn': isLoggedIn})
    # else:
    #     redirect('login')
        # return render(request, 'login.html')
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        try:
            userDetail = UserModel.objects.get(email=request.POST.get('email'))
            if check_password(request.POST.get('password'), (userDetail.password)):
                request.session['email'] = userDetail.email
                return redirect('/')
            else:
                messages.error(request, 'Password incorrect...!')
        except UserModel.DoesNotExist as e:
            messages.error(request, 'No user found of this email....!')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('email') and request.POST.get('password') and request.POST.get('phone') and request.POST.get('balance'):

            userModel = UserModel()
            userModel.name = request.POST.get('name')
            userModel.email = request.POST.get('email')
            userModel.password = make_password(request.POST.get('password'))
            userModel.phone = request.POST.get('phone')
            userModel.balance = request.POST.get('balance')

            if len(request.FILES) != 0:
                userModel.img = request.FILES['image']

            if userModel.isExists():
                messages.error(request, "Email address already registered!")
                return render(request, 'register.html')
            else:
                userModel.save()
                messages.success(request, "Registration details saved successfully...! Please Log in now.")
                return render(request, 'register.html')

    return render(request, 'register.html')


# def logout(request):
#     try:
#         del request.session['email']
#         messages.success(request, "Successfully logged out.")
#     except:
#         messages.error(request, "An error occurred. Try again.")
#         return redirect('/')
#     return redirect('/')

