from flask import Flask, render_template, request, redirect, url_for
import random
import os

app = Flask(__name__)

# Mock genre list
GENRES = ["Pop", "Rock", "Jazz", "Classical", "Hip-Hop", "Electronic", "Country", "R&B"]

user_profiles = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Mock predicted genre
            predicted_genre = random.choice(GENRES)
            confidence = round(random.uniform(0.7, 0.99), 2)
            return render_template('genre.html', song=file.filename, genre=predicted_genre, confidence=confidence)
    return render_template('upload.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        username = request.form['username']
        selected_genres = request.form.getlist('genres')
        user_profiles[username] = selected_genres
        return redirect(url_for('blend'))
    return render_template('preferences.html', genres=GENRES)

@app.route('/blend', methods=['GET', 'POST'])
def blend():
    if request.method == 'POST':
        user1 = request.form['user1']
        user2 = request.form['user2']

        if user1 in user_profiles and user2 in user_profiles:
            blend_genres = list(set(user_profiles[user1]) | set(user_profiles[user2]))
            return render_template('blend.html', user1=user1, user2=user2, blend_genres=blend_genres)
        else:
            return "One or both users not found!"
    return render_template('blend.html')
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)


