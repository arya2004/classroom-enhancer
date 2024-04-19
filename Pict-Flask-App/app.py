from flask import Flask, request, jsonify
import os
import requests
import json
import assemblyai as aai
import pymongo
from bson import json_util

client = pymongo.MongoClient("mongodb+srv://admin:ZdltdZvnbWb0aUk7@cluster0.oygcfbr.mongodb.net/")
db = client["Pict-Project"]
collection_Questions = db["Questions"]
collection_Transcript = db["Transcript"]

correct_answer_score = 0
wrong_answer_score = 0
total_score = 0
current_question = [[]]
question_json = []
chat_history = []
Transcript = {}
answers = []
time = []
count = 0
percentage = {'percentage': 0}

Current_Transcript = {}

def generate_questions(text):
    # Function definition here

def transcribe_video(video_path, api_key="8d5a3a57e9e84a5aa440531dbbc6c757", segment_duration=120):
    # Function definition here

def to_markdown(text):
    # Function definition here

def create_pdf(filename, text):
    # Function definition here

def gen_summary(article_text):
    # Function definition here

def generate_flowchart(text):
    # Function definition here

def generate_flowchart_advance(text):
    # Function definition here

def get_transcript():
    # Function definition here

def llm_function(query):
    # Function definition here

def generateimage(transcription):
    # Function definition here
Step 4: Handle API Routes

python
Copy code
@app.route('/generate_questions', methods=['POST'])
def generate_questions_api():
    # Route implementation here

@app.route('/transcribe_video', methods=['POST'])
def transcribe_video_api():
    # Route implementation here

@app.route('/get_question', methods=['GET'])
def get_question_api():
    # Route implementation here