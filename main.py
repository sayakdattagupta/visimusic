from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import style
import io
import os
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['database']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(filename))
        conn = sqlite3.connect(file.filename)
        cursor = conn.cursor()

        cursor.execute('SELECT title, totalPlayTimeMs FROM Song ORDER BY totalPlayTimeMs DESC LIMIT 10')
        data = cursor.fetchall()

        song = []
        listeningtime = []

        fig, ax = plt.subplots()

        for row in data:
            song.append(row[0])
            listeningtime.append(row[1])

        listeningtime = [x / 60000 for x in listeningtime]

        song = [x[:16]+"..." for x in song]

        plt.style.use('fivethirtyeight')
        ax.invert_yaxis()
        ax.barh(song,listeningtime,align='center')
        ax.set_xlabel("Listening time in Minutes")
        ax.set_ylabel("Song Name")

        img = io.BytesIO()
        fig.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('graph.html', plot_url=plot_url)
    else:
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
