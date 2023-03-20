import sqlite3, matplotlib.pyplot as plt
from matplotlib import style

table = sqlite3.connect('ENTER DATABASE DIRECTORY')

cursor = table.cursor()
    
def graph_mostlistenedsongs():
    cursor.execute('SELECT title, totalPlayTimeMs FROM Song ORDER BY totalPlayTimeMs DESC LIMIT 10')
    data = cursor.fetchall()

    song = []
    listeningtime = []
    
    for row in data:
        song.append(row[0])
        listeningtime.append(row[1])

    listeningtime = [x / 60000 for x in listeningtime]

    song = [x[:16]+"..." for x in song]

    plt.style.use('fivethirtyeight')
    plt.rc('font', size=8) 
    plt.bar(song,listeningtime,width=0.50)
    plt.xlabel("Song Name")
    plt.ylabel("Listening time in Minutes")
    plt.show()

graph_mostlistenedsongs()
cursor.close
table.close()
