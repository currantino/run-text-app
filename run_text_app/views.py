import hashlib
import os

from django.conf import settings
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, Http404

from .text_to_video import text_to_video


def run_text(request: HttpRequest) -> HttpResponse:
    message = request.GET.get("message")
    if message is None:
        print("****************")
        print("No message provided")
        print("****************")
        raise BadRequest
    hashed_message = hashlib.md5(message.encode()).hexdigest()
    video_file_path = os.path.join(settings.MEDIA_ROOT, f'{hashed_message}.mp4')
    text_to_video(message, filename=video_file_path)
    if os.path.exists(video_file_path):
        with open(video_file_path, 'rb') as video:
            response = HttpResponse(video.read(), content_type="media/mp4")
            response['Content-Disposition'] = f'inline; filename={hashed_message}.mp4'
            return response
    else:
        raise Http404
