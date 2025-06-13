from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv
import base64
import json
import random

load_dotenv()

app = Flask(__name__)

SETTINGS_FILE = 'settings.json'

# Prompt templates and elements
PROMPT_TEMPLATES = [
    "{subject} {action} {location} {lighting} {style} {camera}",
    "{subject} {action} {location} {style} {camera} {lighting}",
    "{style} {subject} {action} {location} {camera} {lighting}",
    "{location} {subject} {action} {style} {lighting} {camera}",
]

SUBJECTS = [
    "a young woman",
    "a young man",
    "a teenage girl",
    "a teenage boy",
    "a college student",
    "a young couple",
    "a group of friends",
]

ACTIONS = [
    "casually sitting",
    "laughing naturally",
    "walking down the street",
    "hanging out with friends",
    "enjoying a coffee",
    "reading a book",
    "listening to music",
    "taking a selfie",
    "chatting on the phone",
    "browsing on their phone",
    "waiting for the bus",
    "studying in a cafe",
    "shopping at a mall",
    "exploring the city",
    "having a picnic",
    "playing with their phone",
    "taking photos",
    "enjoying the sunset",
    "having a snack",
    "drinking water",
    "eating street food",
    "window shopping",
    "waiting in line",
    "using a laptop",
    "drawing in a sketchbook",
    "playing a game on their phone",
    "looking at their reflection",
    "tying shoelaces",
    "adjusting their bag",
    "checking watch",
    "hailing a taxi",
    "crossing the road",
    "stretching",
    "yawning",
    "looking bored",
    "looking thoughtful",
    "daydreaming",
    "people-watching",
    "texting a friend",
    "taking notes",
    "making a call",
    "arranging flowers",
    "folding laundry",
    "cooking a meal",
    "washing dishes",
    "doing homework",
    "exercising in the park",
    "feeding pigeons",
    "riding a bicycle",
    "skateboarding",
    "walking a dog",
    "playing a guitar",
    "singing along to music",
    "dancing in a subtle way",
    "applying makeup",
    "combing hair",
    "trying on clothes",
    "packing a suitcase",
    "unpacking groceries",
    "watering plants",
    "gardening",
    "writing in a journal",
    "painting a picture",
    "playing chess",
    "meditating",
    "practicing yoga",
    "doing a puzzle",
    "fixing something small",
    "knitting or crocheting",
    "playing with a cat",
    "playing with a dog",
    "feeding a pet",
    "cleaning glasses",
    "drinking tea",
    "drinking soda",
    "eating an ice cream",
    "eating a sandwich",
    "eating pizza",
    "eating fruit",
    "eating cereal",
    "drinking coffee",
    "writing a letter",
    "reading a newspaper",
    "looking out a window",
    "staring at the ceiling",
    "pondering",
    "thinking deeply",
    "listening intently",
    "gazing into the distance",
    "checking notifications",
    "swiping on a dating app",
    "scrolling social media",
    "taking a video call",
    "filming a TikTok",
    "vlogging",
    "podcasting",
]

LOCATIONS = [
    "in a cozy cafe",
    "at a local park",
    "on a city street",
    "in a shopping mall",
    "at a bus stop",
    "in a library",
    "at a beach",
    "in a college campus",
    "at a train station",
    "in a small restaurant",
    "at a local market",
    "in a public garden",
    "at a street corner",
    "in a small bookstore",
    "at a food court",
    "on a subway platform",
    "in a quiet alleyway",
    "by a riverbank",
    "on a bridge overlooking the city",
    "in an art gallery",
    "at a laundromat",
    "in a diner",
    "at a university lecture hall",
    "in a vintage shop",
    "at a flea market",
    "on a park bench",
    "in a crowded square",
    "near a fountain",
    "on a rooftop",
    "inside a bookstore",
    "at a coworking space",
    "in a dimly lit bar",
    "at a concert venue",
    "in a theatre lobby",
    "at a sports stadium",
    "in a community center",
    "at a local bakery",
    "in front of a mural",
    "on a pedestrian bridge",
    "in a busy intersection",
    "at a construction site (from a distance)",
    "in a quiet cul-de-sac",
    "at a drive-thru",
    "in a parking lot",
    "at a gas station",
    "in a suburban backyard",
    "on a balcony",
    "in a shared apartment living room",
    "in a messy bedroom",
    "in a kitchen",
    "on a staircase",
    "in a hallway",
    "in a garage",
    "at a bus terminal",
    "at an airport gate",
    "on a ferry",
    "inside a taxi",
    "on a bicycle path",
    "in a skate park",
    "at a dog park",
    "in a music studio",
    "at a recording booth",
    "in a classroom",
    "at a laboratory",
    "in a workshop",
    "at a flower shop",
    "in a grocery store aisle",
    "at a farmer's market",
    "in a public restroom (reflection)",
    "at a barber shop",
    "at a hair salon",
    "in a fitting room",
    "at a thrift store",
    "in a luggage claim area",
    "at a security checkpoint",
    "in a cafe with outdoor seating",
    "at a waterfront",
    "in a bustling food market",
    "at a street performance",
    "in an urban garden",
    "at a local community garden",
]

LIGHTING = [
    "in natural daylight",
    "in soft morning light",
    "in golden hour sunlight",
    "in bright afternoon light",
    "in overcast daylight",
    "in warm indoor lighting",
    "in cool fluorescent lighting",
    "in mixed natural and artificial light",
    "in diffused window light",
    "in ambient city light",
    "with a harsh flash",
    "with a soft flash",
    "under streetlights",
    "with neon lights",
    "in dramatic shadows",
    "backlit by the sun",
    "with a soft glow from a lamp",
    "in a dimly lit room",
    "with directional light",
    "with diffused light",
    "with warm natural light",
    "with cool natural light",
    "under a bright spotlight",
    "with dappled light",
    "with window light",
    "with harsh shadows",
    "with rim lighting",
    "with soft, even lighting",
    "with low key lighting",
    "with high key lighting",
    "with a cinematic feel",
    "with strong contrast",
    "with a subtle play of light and shadow",
]

STYLES = [
    "candid amateur photo",
    "casual snapshot",
    "spontaneous moment",
    "authentic candid shot",
    "natural candid photo",
    "real-life moment",
    "genuine candid capture",
    "unposed snapshot",
    "everyday moment",
    "lifestyle photo",
    "overexposed",
    "slightly overexposed",
    "underexposed",
    "grainy film photo",
    "blurry motion shot",
    "off-center composition",
    "imperfect framing",
    "raw and unedited",
    "natural colors",
    "muted tones",
    "vibrant colors",
    "black and white",
    "sepia toned",
    "vintage aesthetic",
    "lo-fi photography",
    "streaky light leak",
    "dust and scratches on the lens",
    "finger over the lens",
    "accidental flash",
    "unintended glare",
    "a quick, unthinking shot",
    "a fleeting moment captured",
    "a glimpse into daily life",
    "a slice of life image",
    "a stolen glance",
    "a perfectly imperfect moment",
    "a photo with character",
    "a slightly shaky shot",
    "a candid street photograph",
    "a casual portrait",
    "a documentary style image",
    "a personal memory",
    "a raw photo",
    "a simple photo",
    "an honest capture",
]

CAMERA = [
    "taken with a disposable camera",
    "taken with a webcam",
]

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def generate_image(prompt, image_count=4, seed=None, aspect_ratio="IMAGE_ASPECT_RATIO_LANDSCAPE", model="IMAGEN_3_1"):
    settings = load_settings()
    auth_token = settings.get('authToken') or os.getenv('IMAGEFX_AUTH_TOKEN')
    
    if not auth_token:
        return {"error": "Authentication token not found"}, 401

    if not auth_token.startswith("Bearer"):
        auth_token = f"Bearer {auth_token}"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://labs.google',
        'priority': 'u=1, i',
        'referer': 'https://labs.google/',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'authorization': auth_token
    }

    data = {
        "userInput": {
            "candidatesCount": image_count,
            "prompts": [prompt],
            "seed": seed,
        },
        "clientContext": {
            "sessionId": ";1740656431200",
            "tool": "IMAGE_FX"
        },
        "modelInput": {
            "modelNameType": model
        },
        "aspectRatio": aspect_ratio
    }

    try:
        response = requests.post(
            "https://aisandbox-pa.googleapis.com/v1:runImageFx",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

@app.route('/')
def index():
    settings = load_settings()
    return render_template('index.html', default_count=settings.get('defaultCount', 4))

@app.route('/settings')
def settings_page():
    settings = load_settings()
    return render_template('settings.html', settings=settings)

@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = load_settings()
    # Don't send the full token in the response
    if 'authToken' in settings:
        settings['authToken'] = '********' if settings['authToken'] else ''
    return jsonify(settings)

@app.route('/api/settings', methods=['POST'])
def update_settings():
    try:
        data = request.get_json()
        settings = load_settings()
        
        if 'authToken' in data:
            settings['authToken'] = data['authToken']
        if 'defaultCount' in data:
            settings['defaultCount'] = data['defaultCount']
            
        save_settings(settings)
        return jsonify({"message": "Settings saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    count = int(data.get('count', 4))
    seed = data.get('seed')
    aspect_ratio = data.get('aspectRatio', 'IMAGE_ASPECT_RATIO_LANDSCAPE')
    model = data.get('model', 'IMAGEN_3_1')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    result = generate_image(prompt, count, seed, aspect_ratio, model)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

@app.route('/api/generate', methods=['GET'])
def api_generate():
    try:
        # Get parameters from query string
        prompt = request.args.get('prompt')
        count = int(request.args.get('count', 4))
        seed = request.args.get('seed')
        aspect_ratio = request.args.get('aspectRatio', 'IMAGE_ASPECT_RATIO_LANDSCAPE')
        model = request.args.get('model', 'IMAGEN_3_1')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
            
        if count < 1 or count > 8:
            return jsonify({"error": "Count must be between 1 and 8"}), 400
            
        # Use the default auth token from settings
        settings = load_settings()
        auth_token = settings.get('authToken') or os.getenv('IMAGEFX_AUTH_TOKEN')
        
        if not auth_token:
            return jsonify({"error": "Authentication token not configured"}), 500

        if not auth_token.startswith("Bearer"):
            auth_token = f"Bearer {auth_token}"

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'dnt': '1',
            'origin': 'https://labs.google',
            'priority': 'u=1, i',
            'referer': 'https://labs.google/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'authorization': auth_token
        }

        data = {
            "userInput": {
                "candidatesCount": count,
                "prompts": [prompt],
                "seed": int(seed) if seed else None,
            },
            "clientContext": {
                "sessionId": ";1740656431200",
                "tool": "IMAGE_FX"
            },
            "modelInput": {
                "modelNameType": model
            },
            "aspectRatio": aspect_ratio
        }

        response = requests.post(
            "https://aisandbox-pa.googleapis.com/v1:runImageFx",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        result = response.json()
        
        formatted_result = {
            "success": True,
            "images": []
        }
        
        for panel in result.get('imagePanels', []):
            for image in panel.get('generatedImages', []):
                formatted_result["images"].append({
                    "url": f"data:image/png;base64,{image['encodedImage']}",
                    "seed": image.get('seed'),
                    "prompt": prompt
                })
        
        return jsonify(formatted_result)
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api')
def api_docs():
    return render_template('api.html')

@app.route('/api/test')
def api_test():
    return render_template('api_test.html')

def generate_random_prompt(subject):
    """Generate a random candid amateur-style prompt using the provided subject."""
    template = random.choice(PROMPT_TEMPLATES)
    prompt = template.format(
        subject=subject,
        action=random.choice(ACTIONS),
        location=random.choice(LOCATIONS),
        lighting=random.choice(LIGHTING),
        style=random.choice(STYLES),
        camera=random.choice(CAMERA)
    )
    return prompt

@app.route('/api/random-prompt', methods=['POST'])
def get_random_prompt():
    """API endpoint to get a random prompt with the provided subject."""
    data = request.get_json()
    subject = data.get('subject', '')
    
    if not subject:
        return jsonify({"error": "Subject is required"}), 400
        
    return jsonify({"prompt": generate_random_prompt(subject)})

if __name__ == '__main__':
    app.run(debug=True) 