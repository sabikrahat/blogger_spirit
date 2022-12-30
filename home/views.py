from django.shortcuts import redirect, render
import pymongo
import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from home.models import PostModel, TransferPoint, UserModel
from django.db import transaction

# Create your views here.

def mongoDBConnect():
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
    try:
        user = UserModel.objects.get(email=request.session['email'])
        posts = PostModel.objects.all()
        print(posts)
        return render(request, 'home.html', {'posts': posts, 'user': user})
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')
    

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
        if request.POST.get('name') and request.POST.get('email') and request.POST.get('password') and request.POST.get('phone'):

            userModel = UserModel()
            userModel.name = request.POST.get('name')
            userModel.email = request.POST.get('email')
            userModel.password = make_password(request.POST.get('password'))
            userModel.phone = request.POST.get('phone')

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


def logout(request):
    try:
        del request.session['email']
        messages.success(request, "Successfully logged out.")
    except:
        messages.error(request, "An error occurred. Try again.")
        return redirect('login')
    return redirect('login')

def privacy(request):
    return render(request, 'privacy-policy.html')

def terms(request):
    return render(request, 'terms-and-conditions.html')

def writePost(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        if request.method == 'POST':
            if request.POST.get('title') and request.POST.get('description'):
                postModel = PostModel()
                postModel.publisherId = user.id
                postModel.title = request.POST.get('title')
                postModel.description = request.POST.get('description')

                if len(request.FILES) != 0:
                    postModel.img = request.FILES['image']
                
                try: 
                    postModel.save()
                except Exception as e:
                    print(e)
                    messages.error(request, "An error occurred. " + str(e))
                    return render(request, 'write-post.html')

                messages.success(request, "Post saved successfully...!")
                return render(request, 'write-post.html')
        
        else:
            return render(request, 'write-post.html')
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')


def transferPoint(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])

        if request.method == 'POST':
            if request.POST.get('email') and request.POST.get('point'):

                with transaction.atomic():
                    try:
                        receiver = UserModel.objects.get(email=request.POST.get('email'))

                        trasferPoint = TransferPoint()
                        trasferPoint.senderEmail = user.email
                        trasferPoint.receiverEmail = receiver.email
                        trasferPoint.point = request.POST.get('point')


                        # Action #1
                        user.point = user.point - int(request.POST.get('point'))
                        user.save()

                        # Action #2
                        receiver.point = receiver.point + int(request.POST.get('point'))
                        receiver.save()

                        # Action #3
                        trasferPoint.save()
                    except Exception as e:
                        print(e)
                        messages.error(request, "An error occurred. " + str(e))
                        return render(request, 'transfer-point.html', {'user': user})
                    messages.success(request, "Point transfered successfully...!", {'user': user})
                    return render(request, 'transfer-point.html')
        else:
            return render(request, 'transfer-point.html', {'user': user})

    except:
        messages.error(request, 'You need to login first')
        return redirect('login')

