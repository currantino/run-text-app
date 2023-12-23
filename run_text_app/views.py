import hashlib
import logging
import os

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from minio import Minio, S3Error

from .forms import MessageForVideoForm
from .models import VideoRequest
from .text_to_video import text_to_video

MEDIA_MP4 = "media/mp4"

minio_client = Minio(settings.MINIO_ENDPOINT, settings.MINIO_ACCESS_KEY, settings.MINIO_SECRET_KEY, secure=False)
if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
    minio_client.make_bucket(settings.MINIO_BUCKET_NAME)


def run_text(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = MessageForVideoForm(request.POST)
        if not form.is_valid():
            return render(request, "error.html",
                          context={'message': 'Invalid form! Must not be longer than 30 characters'}, status=400)

        message = form.cleaned_data['message']
        req = VideoRequest.objects.create(msg=message)
        hashed_message = hashlib.md5(message.encode()).hexdigest()
        try:
            return get_video_from_minio(hashed_message)
        except S3Error as e:
            logging.info("Could not get video from minio")

        video_file_path, video_size = generate_video(hashed_message, message)

        if not os.path.exists(video_file_path):
            return HttpResponse(status=500, content="Could not create video.")
        with open(video_file_path, 'rb') as video:
            try:
                minio_client.put_object(settings.MINIO_BUCKET_NAME, hashed_message, data=video,
                                        content_type=MEDIA_MP4, length=video_size)
                logging.info("Uploaded video to minio.")
                video.seek(0)
            except S3Error as e:
                logging.warning("Could not upload video to minio!")
            response = create_video_response(hashed_message, video)
            os.remove(video_file_path)
            return response

    else:
        return HttpResponseNotAllowed(permitted_methods="POST")


def generate_video(hashed_message, message):
    video_file_path = os.path.join(settings.MEDIA_ROOT, f'{hashed_message}.mp4')
    text_to_video(message, filename=video_file_path)
    video_size = os.path.getsize(video_file_path)
    return video_file_path, video_size


def get_video_from_minio(hashed_message):
    try:
        with minio_client.get_object(settings.MINIO_BUCKET_NAME, hashed_message) as video:
            response = create_video_response(hashed_message, video)
            video.release_conn()
            video.close()
            logging.info("Returning video from minio.")
            return response
    except S3Error as e:
        logging.warning("Could not get video from minio!")
        raise e


def create_video_response(filename, video):
    response = HttpResponse(video.read(), content_type=MEDIA_MP4)
    response['Content-Disposition'] = f'attachment; filename={filename}.mp4'
    return response


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {'form': MessageForVideoForm()})


def requests(request):
    data = VideoRequest.objects.all()
    context = {'requests': data}
    return render(request, "requests.html", context)
