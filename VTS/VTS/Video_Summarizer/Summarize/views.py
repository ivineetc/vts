from django.shortcuts import render
from .models import Summary
from django.shortcuts import redirect
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from google_auth_oauthlib.flow import Flow

from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa


# Create your views here.
def index(request):
    return render(request,"index.html")

def home(request):
    if request.method == 'POST':
        if 'video_url' in request.POST:
            video_url = request.POST['video_url']
            video_id = video_url.split('=')[1]

            from IPython.display import YouTubeVideo
            YouTubeVideo(video_id)

        # Authenticate and build the YouTube API client
        # creds = Credentials.from_authorized_user_file('credentials.json')
        # youtube = build('youtube', 'v3', credentials=creds)

        # Get the video transcript
        # transcript = YouTubeTranscriptApi.get_transcript(video_id)
        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript[0:5]
        result = ""
        for i in transcript:
            result += ' ' + i['text']

        # Convert the transcript to plain text
        # text = '\n'.join([t['text'] for t in transcript])

        # Summarize the text
        summarizer = pipeline('summarization')
        # summary = summarizer(text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']
        num_iters = int(len(result)/1000)
        summarized_text = []
        for i in range(0, num_iters + 1):
            start = 0
            start = i * 1000
            end = (1 + 1) * 1000
            out = summarizer(result[start:end])
            out = out[0]
            out = out['summary_text']
            summarized_text.append(out)

        # Render the template with the summary
        return render(request, 'index.html', {'summary': summarized_text})

    return render(request, 'index.html')

def download_summary(request):
    if request.method == 'POST':
        summary = request.POST.get('summary', '')
        pdf_file = generate_pdf(summary)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="summary.pdf"'
        return response
    else:
        return HttpResponse('Error: Invalid request method.')


def generate_pdf(summary):
    html = f'<html><head><meta charset="UTF-8"><title>Summary</title></head><body><p>{summary}</p></body></html>'
    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=pdf_file, encoding='UTF-8')
    pdf_file.seek(0)
    return pdf_file


def assesment(request):
    summary = Summary.objects.all()
    return render(request,"index.html",{'summary':summary})




# def get_auth(request):
#     # Define the OAuth 2.0 scopes that your application needs
#     scopes = [
#         'https://www.googleapis.com/auth/youtube.force-ssl',
#         'https://www.googleapis.com/auth/youtube.readonly'
#     ]

#     # Set up the OAuth 2.0 flow
#     flow = Flow.from_client_secrets_file(
#         'client_secrets.json', scopes=scopes,
#         redirect_uri='http://localhost:8000/oauth2callback/'
#     )

#     # Generate the authorization URL and redirect the user to it
#     auth_url, _ = flow.authorization_url(prompt='consent')
#     return redirect(auth_url)



# def Sum(request):
#     v_url = request.POST["link"]
#     v_obj = Summary(link=v_url)
#     v_obj.save()
#     return render(request, "index.html",{'msg':"Data saved successfully"})



