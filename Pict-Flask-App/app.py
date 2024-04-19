from flask import Flask, request, jsonify
import os
import requests
import json
import assemblyai as aai
import pymongo
from bson import json_util

