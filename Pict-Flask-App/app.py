from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import os
import requests
import json
import assemblyai as aai
import ast
import threading
from flask_cors import CORS
import pathlib
import textwrap
import json
import requests
import schemdraw
from schemdraw.flow import *
import google.generativeai as genai
import graphviz
from IPython.display import display
from IPython.display import Markdown
import json
import requests
import schemdraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pathlib
import textwrap
import pymongo
from bson import json_util
import os
import google.generativeai as genai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

CORS(app)

import json
import requests
import ast
from flask import jsonify
from flask import jsonify


client = pymongo.MongoClient("mongodb+srv://admin:ZdltdZvnbWb0aUk7@cluster0.oygcfbr.mongodb.net/")
db = client["Pict-Project"]
collection_Questions = db["Questions"]
collection_Transcript = db["Transcript"]
correct_answer_score = 0
wrong_answer_score = 0
total_score = 0
current_question = [
    [

    ]
]
question_json = []
chat_history = []
Transcript = {}
answers = []
time = []
count =0 
percentage={'percentage':0}

Current_Transcript = {}
def generate_questions(text):
    url = "https://api.edenai.run/v2/text/generation"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGRjMWZlZGYtNzZlOS00YWIyLThjNTgtMDA5NDY0N2M1NDlmIiwidHlwZSI6ImFwaV90b2tlbiJ9.yRjtRKTk-R4-ckG3R7hrBBJOVeoNAw5zUW01ok5s3hs"}


    # Define the text for the prompts (easy and difficult)
    easy_prompt = (""" (generate very easy questions with easy options)
            {
            {
                "question": "{question1}",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "{answer1}"
            },
            {
                "question": "{question2}",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "{answer2}"
            },
            {
                "question": "{question3}",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "{answer3}"
            }
            }
            (output only in proper json format given above)
    """+ text)
        

    difficult_prompt = (""" (generate very hard questions with very difficult options in relation to '{easy_prompt}'
            {
            {
                "question": "{question1}",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "{answer1}"
            },
            {
                "question": "{question2}",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "{answer2}"
            },
            {
                "question": "{question3}",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "{answer3}"
            }
            }
            (output only in proper json format given above)
    """+ text)

    # Define payloads for easy and difficult prompts
    easy_payload = {
        "providers": "openai,cohere",
        "text": easy_prompt,
        "temperature": 0.2,
        "max_tokens": 1000,
        "fallback_providers": ""
    }




    difficult_payload = {
        "providers": "openai,cohere",
        "text": difficult_prompt,
        "temperature": 0.5,
        "max_tokens": 1000,
        "fallback_providers": ""
    }
    raw_percentage = percentage['percentage']

    # For demonstration purposes, assuming correct answer percentage
    raw_percentage = 60

    # Determine which prompt to use based on correct answer percentage
    if raw_percentage > 70:
        payload = difficult_payload  # Use difficult prompt
    else:
        payload = easy_payload  # Use easy prompt

    # Make a request to generate questions based on the selected prompt
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    generated_text = result['openai']['generated_text']

    # Remove dots
    generated_text = generated_text.replace(".","")
    # Remove extra spaces
    generated_text = " ".join(generated_text.split())

    # Convert to valid JSON format
    data = ast.literal_eval(generated_text)
    data_to_insert = data




    return data



def transcribe_video(video_path, api_key = "8d5a3a57e9e84a5aa440531dbbc6c757" , segment_duration=120):
    # Set your AssemblyAI API key
    aai.settings.api_key = api_key

    # Initialize the transcriber
    transcriber = aai.Transcriber()

    # Load the video file
    video_clip = VideoFileClip(video_path)

    # Get the total duration of the video
    total_duration = video_clip.duration

    # Iterate through the video in segments of segment_duration seconds
    for start_time in range(0, int(total_duration), segment_duration):
        # Calculate the end time of the segment
        end_time = min(start_time + segment_duration, total_duration)

        # Extract the segment from the video
        segment_clip = video_clip.subclip(start_time, end_time)

        # Save the segment as a temporary audio file
        segment_audio_file = f"audio_segment_{start_time}.wav"
        segment_clip.audio.write_audiofile(segment_audio_file)

        # Transcribe the segment
        transcript = transcriber.transcribe(segment_audio_file)

        # Print the transcribed text
        print(f"Transcription for segment {start_time}-{end_time} seconds:")
        print(transcript.text)
        print("-" * 50)
       
        # Remove the temporary audio file
        os.remove(segment_audio_file)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def create_pdf(filename, text):
    c = canvas.Canvas(filename, pagesize=letter)
    y_position = 750
    for line in text.split('\n'):
        c.drawString(100, y_position, line)
        y_position -= 20
    c.save()

def gen_summary(article_text):
    GOOGLE_API_KEY="AIzaSyBtsmDXZBwuEM7mKoycKhirwoxoAewKb_o"

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(["summarise text using bullets with multiple titles ",article_text])
    final_text=response.text
    to_markdown(final_text)
    filename = "summary_pdf.pdf"
    create_pdf(filename,final_text)
    print(f"PDF file '{filename}' created successfully.")


def generate_flowchart(text):
    GOOGLE_API_KEY="AIzaSyBtsmDXZBwuEM7mKoycKhirwoxoAewKb_o"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(["summarise the text given",text])
    to_markdown(response.text)
    summary=response.text
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGRjMWZlZGYtNzZlOS00YWIyLThjNTgtMDA5NDY0N2M1NDlmIiwidHlwZSI6ImFwaV90b2tlbiJ9.yRjtRKTk-R4-ckG3R7hrBBJOVeoNAw5zUW01ok5s3hs"}
    generation_url = "https://api.edenai.run/v2/text/generation"
    generation_payload = {
        "providers": "openai,cohere",
        "text": f"generate 7 keysentences with only  3 words each based on summary where only first keysentence is just title '{summary}'",
        "temperature": 0.2,
        "max_tokens": 250,
        "fallback_providers": ""
    }
    generation_response = requests.post(generation_url, json=generation_payload, headers=headers)
    generation_result = json.loads(generation_response.text)
    key_sentences = [sentence.strip() for sentence in generation_result['openai']['generated_text'].split('\n') if sentence.strip()]
    for i, sentence in enumerate(key_sentences, 1):
        print(f"keysentence[{i}]: {sentence}")
    # Alternatively, if you want to organize them into separate lists or JSON format
    keysentence_lists = [{"keysentence": sentence} for sentence in key_sentences]
    # Convert to JSON
    keysentence_json = json.dumps(keysentence_lists, indent=4)
    # Drawing the flowchart
    with schemdraw.Drawing() as d:
        d+= Start().label("")
        d += Arrow().down(d.unit/4)
        d += Ellipse(w=12).label(key_sentences[0])
        d += Arrow().down(d.unit/4)
        d += Box(w=12).label(key_sentences[1])
        d += Arrow().down(d.unit/4)
        d += Ellipse(w=12).label(key_sentences[2])
        d += Arrow().down(d.unit/4)
        d += Box(w=12).label(key_sentences[3])
        d += Arrow().down(d.unit/4)
        d += Ellipse(w=12).label(key_sentences[4])
        d += Arrow().down(d.unit/4)
        d += Box(w=12).label(key_sentences[5])
        d += Arrow().down(d.unit/4)
        d += Ellipse(w=12).label(key_sentences[6])
        d.save("flowchart.pdf", dpi=50)
    
    
def generate_flowchart_advance(text):
    GOOGLE_API_KEY="AIzaSyBtsmDXZBwuEM7mKoycKhirwoxoAewKb_o"

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')


    # Text to be summarized

    response = model.generate_content(["summarise the text given",text])
    to_markdown(response.text)

    summary=response.text
    print(summary)

    ##################################################################################################################################################

    # Eden AI API credentials and URL
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGRjMWZlZGYtNzZlOS00YWIyLThjNTgtMDA5NDY0N2M1NDlmIiwidHlwZSI6ImFwaV90b2tlbiJ9.yRjtRKTk-R4-ckG3R7hrBBJOVeoNAw5zUW01ok5s3hs"}
    generation_url = "https://api.edenai.run/v2/text/generation"

    # Payload for key sentence generation
    generation_payload = {
        "providers": "openai,cohere",
        "text": f"""Based on the provided summary '{summary}', generate key sentences with the following structure:

    1. Key Sentence 1 (Title): [3-word sentence]
    2. Key Sentence 2 (Subtitle): [3-word sentence]
    - Sub-Key Sentence 1: [3-word sentence]
    - Sub-Key Sentence 2: [3-word sentence]
    3. Key Sentence 3 (Subtitle): [3-word sentence]
    - Sub-Key Sentence 1: [3-word sentence]
    - Sub-Key Sentence 2: [3-word sentence]
    4. Key Sentence 4: [3-word sentence]
    - Sub-Key Sentence 1: [3-word sentence]
    - Sub-Key Sentence 2: [3-word sentence]

    Each sentence should be composed of only three words and should be relevant to the summary content.""",
    
        "temperature": 0.3,
        "max_tokens": 250,
        "fallback_providers": ""
    }

    # Text generation request
    generation_response = requests.post(generation_url, json=generation_payload, headers=headers)
    generation_result = json.loads(generation_response.text)

    # Extracting key sentences
    key_sentences = [sentence.strip() for sentence in generation_result['openai']['generated_text'].split('\n') if sentence.strip()]

    # Printing key sentences with the specified format
    for i, sentence in enumerate(key_sentences, 1):
        print(f"keysentence[{i}]: {sentence}")

    # Alternatively, if you want to organize them into separate lists or JSON format
    keysentence_lists = [{"keysentence": sentence} for sentence in key_sentences]

    # Print keysentence lists
    print(keysentence_lists)

    # Convert to JSON
    keysentence_json = json.dumps(keysentence_lists, indent=4)
    print(keysentence_json)

    connections = {
        key_sentences[0]: [key_sentences[1], key_sentences[4],key_sentences[7]],
        key_sentences[1]: [key_sentences[2], key_sentences[3]],
        key_sentences[4]: [key_sentences[5], key_sentences[6]],
        key_sentences[7]: [key_sentences[8], key_sentences[9]]
    }

    # Create a new Graph object
    # Create a new Graph object with format 'png'
    dot = graphviz.Digraph(comment="Flowchart", format='png')  # Set format to 'png'

    dot.attr(dpi='300')  # Set DPI for better quality

    # Add edges based on the connections
    for source, targets in connections.items():
        for target in targets:
            dot.edge(source, target)

    # Save the dot object to a PNG file
    dot_file = dot.pipe(format='png')

    # Save the dot object to a PNG file
    file_path = "flowchart_connections.png"
    with open(file_path, 'wb') as f:
        f.write(dot.pipe(format='png'))

    print("Flowchart saved as flowchart_connections.png")

def get_transcript():
    values = list(Transcript.values())
    result = ' '.join(map(str, values))
    return result

os.environ['GOOGLE_API_KEY'] = "AIzaSyDLSIlCEg-hm7EC36BEEh0ZULMC2p0lpkk"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Select the model
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
messages = [
    {
        "role": "system",
        "context" : f"""{get_transcript()}"""
    },
    {
        "role": "assistant",
        "content": f"""Ask me anything! I'm here to help you with your queries."""
    }
]

# Function to process and store Query and Response


def llm_function(query):
    text=get_transcript()
    print(text)
    response = model.generate_content(query).text.strip("").replace("", "")
    system_message = {"role": "system", "context" : f"""{get_transcript()}"""}

    # Add the system message to the top of the messages list
    messages.insert(0, system_message)
    if len(response.splitlines()) > 6:
        response_lines = response.splitlines()[:6]
        response = "\n".join(response_lines)

    output_json = {
        "user_role": "user",
        "user_content": query,
        "assistant_role": "assistant",
        "assistant_content": response
    }

    messages.append({
        "role": "user",
        "content": query
    })
    messages.append({
        "role": "assistant",
        "content": response
    })
    return output_json
# Route for handling incoming chat requests
def generateimage(transcription):
    if transcription == "":
        return None
    genai.configure(api_key="AIzaSyBtsmDXZBwuEM7mKoycKhirwoxoAewKb_o")
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(["Given a transcription, find out the core theme of the topic and generate a prompt suitable for text-to-image generation to create relevant image illustrations. Consider the tone, mood, and key elements of the transcription to guide the creation of the visual representation. Ensure that the generated prompt captures the essence and context of the text accurately for effective visual storytelling. Transcription : ", transcription])
    to_markdown(response.text)

    summary = response.text
    print(response.text)
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGRjMWZlZGYtNzZlOS00YWIyLThjNTgtMDA5NDY0N2M1NDlmIiwidHlwZSI6ImFwaV90b2tlbiJ9.yRjtRKTk-R4-ckG3R7hrBBJOVeoNAw5zUW01ok5s3hs"}
    url = "https://api.edenai.run/v2/image/generation"
    payload = {
        "providers": "replicate",
        "text": response.text,
        "resolution": "512x512",
        "fallback_providers": "amazon"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    image_url = result['replicate']['items'][0]['image_resource_url']
    # replicate
    return image_url







@app.route('/generate_questions', methods=['POST'])
def generate_questions_api():
    data = request.get_json()
    text = data.get('text', '')  # Get the 'text' value from the request data or use an empty string if it doesn't exist
    if not text:
        return jsonify({'error': 'No text provided'}), 400  # Return an error response if 'text' is not provided
    print(text)
    new_questions = generate_questions(text)
    # question_json.append(new_questions)
    print(new_questions)
    ans=json.loads(new_questions)
    return jsonify(ans)



@app.route('/transcribe_video', methods=['POST'])
def transcribe_video_api():
    data = request.get_json()
    video_path = data.get('video_path', '')
    print(video_path)
    api_key = "8d5a3a57e9e84a5aa440531dbbc6c757"
    aai.settings.api_key = api_key

    # Initialize the transcriber
    transcriber = aai.Transcriber()

    # Load the video file
    video_clip = VideoFileClip(video_path)

    # Get the total duration of the video
    total_duration = video_clip.duration

    # Iterate through the video in segments of segment_duration seconds
    segment_duration = 120  # Define the segment duration

    for start_time in range(0, int(total_duration), segment_duration):
        # Calculate the end time of the segment
        end_time = min(start_time + segment_duration, total_duration)

        # Extract the segment from the video
        segment_clip = video_clip.subclip(start_time, end_time)

        # Save the segment as a temporary audio file
        segment_audio_file = f"audio_segment_{start_time}.wav"
        segment_clip.audio.write_audiofile(segment_audio_file)

        # Transcribe the segment
        transcript = transcriber.transcribe(segment_audio_file)

        # Print the transcribed text
        print(f"Transcription for segment {start_time}-{end_time} seconds:")
        print(transcript.text)
        print("-" * 50)
        print("done")
        text = transcript.text

        new_questions = generate_questions(text)
        current_question.clear()
        
        current_question.append(new_questions)
        
        Transcript[segment_audio_file] = str(text)
        Current_Transcript.clear()
        Current_Transcript[f"{video_path}"] = str(text)

        
        question_json.append(new_questions)

        # Remove the temporary audio file
        os.remove(segment_audio_file)
        
    
    collection_Transcript.insert_one({f"Transcript {video_path}": get_transcript()})
    

    try:
        for question_set in question_json:
            collection_Questions.insert_many(question_set)
    except Exception as e:
        print(f"An error occurred while inserting questions into the collection: {e}")


    
    return "done"


@app.route('/get_question', methods=['GET'])
def get_question_api():
    return json.loads(json_util.dumps(question_json))


@app.route('/get_current_question', methods=['GET'])
def get_current_question_api():
    return json.loads(json_util.dumps(current_question))

@app.route('/get_transcript', methods=['GET'])
def get_transcript_api():
    values = list(Transcript.values())
    result = ' '.join(map(str, values))
    return jsonify(result)

@app.route('/get_current_transcript', methods=['GET'])
def get_current_transcript_api():

    values = list(Current_Transcript.values())
    result = ' '.join(map(str, values))
    return jsonify(result)



@app.route('/summarize_text_with_bullets', methods=['GET'])
def summarize_text_with_bullets_api():
    
    data=get_transcript()
    print(data)
    gen_summary(data)
    return jsonify("summary generated successfully")

@app.route('/generate_flowchart', methods=['GET'])
def generate_flowchart_api():
    data=get_transcript()
    generate_flowchart(data)
    return jsonify("flow chart generated successfully")

@app.route('/generate_flowchart_advance', methods=['GET'])
def generate_flowchart_advance_api():
    data=get_transcript()
    generate_flowchart_advance(data)
    return jsonify("Advance flow chart generated successfully")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data['query']
    response_json = llm_function(query)
    return jsonify(response_json)

@app.route('/history', methods=['GET'])
def history():
    return jsonify(messages)

@app.route('/correct_answer', methods=['GET'])
def correct_answer():
    global correct_answer_score
    answers.append(1)
    correct_answer_score += 1
    percentage['percentage'] = (correct_answer_score/(correct_answer_score+wrong_answer_score))*100
    return jsonify("correct answer saved successfully")

@app.route('/wrong_answer', methods=['GET'])
def wrong_answer(): 
    answers.append(0)
    global wrong_answer_score
    wrong_answer_score += 1
    percentage['percentage'] = (correct_answer_score/(correct_answer_score+wrong_answer_score))*100
    return jsonify("wrong answer saved successfully")

@app.route('/get_answer', methods=['GET'])
def get_answer():
    return jsonify(answers)

@app.route('/get_time', methods=['GET'])
def get_time():
    return jsonify(time)

@app.route('/get_num_correct',methods=['GET'])
def get_num_correct():
    return jsonify(correct_answer_score)


@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    recipient_email = data.get('recipient_email')
    subject = data.get('subject')
    doubt = data.get('doubt')

    sender_email = "rising1champions@gmail.com" 
    sender_password = "rowm ftof qxav crnn"

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender_email, sender_password)
    
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = recipient_email
    email_message['Subject'] = subject
    message = f"Doubt/Feedback : {doubt}"
    email_message.attach(MIMEText(message, 'plain'))

    smtp_server.send_message(email_message)
    smtp_server.quit()
    return jsonify({'message': 'Feedback sent successfully'})

@app.route('/get_percentage', methods=['GET'])
def get_percentage():
    return jsonify(percentage)
    
@app.route('/generate_image', methods=['GET'])
def generate_image():
    values = list(Current_Transcript.values())
    result = ' '.join(map(str, values))
    image_url = generateimage(result)
    return jsonify({"image_url" : image_url})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)