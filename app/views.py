from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.utils import timezone
from .facerec.faster_video_stream import stream
from .facerec.click_photos import click
from .facerec.train_faces import trainer
from .models import User, Detected, Website
from .forms import UserForm, WebsiteForm
import cv2
import pickle
import face_recognition
import datetime
from cachetools import TTLCache
from .serializers import WebsiteSerializer
from rest_framework.decorators import api_view

cache = TTLCache(maxsize=20, ttl=60)


def identify1(frame, name, buf, buf_length, known_conf):

    if name in cache:
        return
    count = 0
    for ele in buf:
        count += ele.count(name)
    
    if count >= known_conf:
        timestamp = datetime.datetime.now(tz=timezone.utc)
        print(name, timestamp)
        cache[name] = 'detected'
        path = 'detected/{}_{}.jpg'.format(name, timestamp)
        write_path = 'media/' + path
        cv2.imwrite(write_path, frame)
        try:
            user = User.objects.get(name=name)
            user.detected_set.create(time_stamp=timestamp, photo=path)
        except:
            pass 	        




def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.5):

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    # X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    # print(closest_distances)
    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]



def identify_faces(video_capture):

    buf_length = 10
    known_conf = 6
    buf = [[]] * buf_length
    i = 0

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="app/facerec/models/trained_model.clf")
            print(predictions)

        process_this_frame = not process_this_frame

        face_names = []

        for name, (top, right, bottom, left) in predictions:

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            identify1(frame, name, buf, buf_length, known_conf)

            face_names.append(name)
            info = name

        buf[i] = face_names
        i = (i + 1) % buf_length


        # print(buf)


        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



def login(request):
    return render(request, 'app/login.html')

def pricing(request):
    return render(request, 'app/pricing.html')

def dashboard(request):
    return render(request, 'app/index.html')

def video_stream(request):
    stream()
    return HttpResponseRedirect(reverse('dashboard'))


def add_photos(request):
	user_list = User.objects.all()
	return render(request, 'app/add_photos.html', {'user_list': user_list})


def click_photos(request, user_id):
	cam = cv2.VideoCapture(0)
	user = get_object_or_404(User, id=user_id)
	click(user.name, user.id, cam)
	return HttpResponseRedirect(reverse('add_photos'))


def train_model(request):
	trainer()
	return HttpResponseRedirect(reverse('dashboard'))


def detected(request):
	if request.method == 'GET':
		date_formatted = datetime.datetime.today().date()
		date = request.GET.get('search_box', None)
		if date is not None:
			date_formatted = datetime.datetime.strptime(date, "%Y-%m-%d").date()
		det_list = Detected.objects.filter(time_stamp__date=date_formatted).order_by('time_stamp').reverse()
	# det_list = Detected.objects.all().order_by('time_stamp').reverse()
	return render(request, 'app/detected.html', {'det_list': det_list, 'date': date_formatted})


def identify(request):
    video_capture = cv2.VideoCapture(0)
    identify_faces(video_capture)

    return HttpResponseRedirect(reverse('dashboard'))

def identify_login(request):
    info = None
    video_capture = cv2.VideoCapture(0)
    buf_length = 10
    known_conf = 6
    buf = [[]] * buf_length
    i = 0

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="app/facerec/models/trained_model.clf")

        process_this_frame = not process_this_frame

        face_names = []

        for name, (top, right, bottom, left) in predictions:

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            identify1(frame, name, buf, buf_length, known_conf)

            face_names.append(name)
            info = name

        buf[i] = face_names
        i = (i + 1) % buf_length


        # print(buf)
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    users = User.objects.values_list('name', flat=True)
    print(users)

    if info is not None:
        if info in users:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            HttpResponseRedirect(reverse('login'))
    
    return HttpResponseRedirect(reverse('login'))



def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = UserForm()
    return render(request, 'app/add_user.html', {'form': form})

def add_website(request):
    if request.method == "POST":
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website = form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = WebsiteForm()
    return render(request, 'app/add_website.html', {'form': form})

def admin_website(request):
    website_list = Website.objects.all()
    return render(request,'app/admin_website.html', {'website_list': website_list})

def delete_website(request,website_id):
    website = get_object_or_404(Website ,website_id = website_id)
    website.delete()
    return HttpResponseRedirect(reverse('admin_website'))

@api_view(['GET'])
def getWebsites(request):

    if request.method == 'GET':
        websites = Website.objects.all()
        serializer = WebsiteSerializer(websites, many=True)
        return JsonResponse(serializer.data, safe=False)