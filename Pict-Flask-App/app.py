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