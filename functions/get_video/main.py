import os
import json
from flask import Flask, request, jsonify
import requests

LUMA_APP_URL = "https://api.lumalabs.ai/dream-machine/v1/generations"
LUMA_API_KEY = os.environ.get('LUMA_API_KEY')

def generate_video(request):
    path = request.path
    method = request.method
    
    if path == "/" and method == "POST":
        try:
            req_json = request.get_json()

            payload = {
                "prompt": req_json.get("prompt"),
                "model": req_json.get("model"),
                "keyframes": req_json.get("keyframes")
            }

            headers = {
                "Authorization": f"Bearer {LUMA_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(LUMA_APP_URL, json=payload, headers=headers)
            return jsonify({
                "status": response.status_code,
                "response": response.json()
            }) 
        except Exception as e:
            return jsonify({
                "status": 500,
                "error": str(e)
            }), 500
            
    elif path.startswith("/check-status") and method == "GET":
        try:
            job_id = path.split("/check-status/")[1]
            headers = {
                "Authorization": f"Bearer {LUMA_API_KEY}",
                "Accept": "application/json"
            }
            url = f"https://api.lumalabs.ai/dream-machine/v1/generations/{job_id}"

            response = requests.get(url, headers=headers)

            return jsonify(response.json())

        except Exception as e:
            return jsonify({
                "status": 500,
                "error": str(e)
            }), 500

    else:
        return jsonify({
            "status": 404,
            "error": "Not Found"
        }), 404
    
