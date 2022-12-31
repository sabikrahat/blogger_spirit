from django.shortcuts import redirect, render
import pymongo
import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from home.models import PostModel, TransferPoint, UserModel
from django.db import transaction
from django.db import connection

# Create your views here.

# home function
def home(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        #
        cursor = connection.cursor()
        cursor.execute('CALL getPosts()')
        posts = cursor.fetchall()
        cursor.close()
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getSendedPoint(%s)', [user.email])
        sended = cursor.fetchall()[0][0]
        if sended is None:
            sended = 0
        cursor.close()
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getReceivedPoint(%s)', [user.email])
        received = cursor.fetchall()[0][0]
        if received is None:
            received = 0
        cursor.close()
        #
        return render(request, 'home.html', {'user': user, 'posts': posts, 'sended': sended, 'received': received})
    except:
        messages.error(request, 'You need to login first')
        return redirect('../authentication')

# authentication function
def authentication(request):
    return render(request, 'authentication.html')
    
# login function
def login(request):
    if request.method == 'POST':
        try:
            userDetail = UserModel.objects.get(email=request.POST.get('email'))
            if check_password(request.POST.get('password'), (userDetail.password)):
                request.session['email'] = userDetail.email
                # print('Logged in successfully...!')
                return redirect('../')
            else:
                messages.error(request, 'Password incorrect...!')
        except UserModel.DoesNotExist as e:
            messages.error(request, 'No user found of this email....!')
    return redirect('../authentication')

# signup function
def signup(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('email') and request.POST.get('password'):

            userModel = UserModel()
            userModel.name = request.POST.get('name')
            userModel.email = request.POST.get('email')
            userModel.password = make_password(request.POST.get('password'))

            if len(request.FILES) != 0:
                userModel.img = request.FILES['image']

            if userModel.isExists():
                messages.error(
                    request, request.POST.get('email') + " email address already registered...! Please Log in.")
                return redirect('../authentication')
            else:
                userModel.save()
                messages.success(request, "Hello " + request.POST.get('name') + ", registration details saved successfully...! Please Log in now.")
                return redirect('../authentication')
    else:
        return redirect('../authentication')


def logout(request):
    try:
        del request.session['email']
        messages.success(request, "Successfully logged out.")
    except:
        messages.error(request, "An error occurred. Try again.")
        return redirect('authentication')
    return redirect('authentication')

def privacy(request):
    return render(request, 'privacy-policy.html')

def terms(request):
    return render(request, 'terms-and-conditions.html')

def writePost(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getSendedPoint(%s)', [user.email])
        sended = cursor.fetchall()[0][0]
        if sended is None:
            sended = 0
        cursor.close()
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getReceivedPoint(%s)', [user.email])
        received = cursor.fetchall()[0][0]
        if received is None:
            received = 0
        cursor.close()
        #
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
                    return render(request, 'write-post.html', {'user': user, 'sended': sended, 'received': received})

                messages.success(request, "Post saved successfully...!")
                return redirect('/')
        
        else:
            return render(request, 'write-post.html', {'user': user, 'sended': sended, 'received': received})
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')


def transferPoint(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getSendedPoint(%s)', [user.email])
        sended = cursor.fetchall()[0][0]
        if sended is None:
            sended = 0
        cursor.close()
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getReceivedPoint(%s)', [user.email])
        received = cursor.fetchall()[0][0]
        if received is None:
            received = 0
        cursor.close()
        #

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
                    return redirect('/')
        else:
            return render(request, 'transfer-point.html', {'user': user, 'sended': sended, 'received': received})

    except:
        messages.error(request, 'You need to login first')
        return redirect('login')


def feedback(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getSendedPoint(%s)', [user.email])
        sended = cursor.fetchall()[0][0]
        if sended is None:
            sended = 0
        cursor.close()
        #
        cursor = connection.cursor()
        cursor.execute('SELECT getReceivedPoint(%s)', [user.email])
        received = cursor.fetchall()[0][0]
        if received is None:
            received = 0
        cursor.close()
        #
        # Connect to the MongoDB, change the connection string per your MongoDB environment
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        print(client)

        # Set the db object to point to the business database
        db = client['blogger_spirit']
        collection = db['user_feedbacks']

        # Showcasing the count() method of find, count the total number of documents in collection
        # print('Total number of documents in collection: ', collection.count_documents({}))
        cursor = collection.find({})
        feedbacks = [document for document in cursor]
        # print(feedbacks)
        # print('Total number of documents in collection: ', len(feedbacks))
        #
        if request.method == 'POST':
            if request.POST.get('email') and request.POST.get('feedback'):
                #
                email = request.POST.get('email')
                feedback = request.POST.get('feedback')
                now = datetime.datetime.utcnow()
                dictionary = {'email': email, 'feedback': feedback, 'created_at': now}
                collection.insert_one(dictionary)
                messages.success(request, "Feedback saved successfully...!")
                return redirect('/')
        
        return render(request, 'feedback.html', {'user': user, 'sended': sended, 'received': received, 'feedbacks': feedbacks})
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')
