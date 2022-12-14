from logging.handlers import DatagramHandler
import uvicorn
from gogoanime import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json


import sqlite3





app = FastAPI()


conn = sqlite3.connect("test.db")
c = conn.cursor()

#c.execute('''CREATE TABLE animes(anime_id TEXT,title TEXT,year TEXT,other_names TEXT,type TEXT,status TEXT,genre TEXT,episodes TEXT, image_url TEXT, plot_summary TEXT)''')
# c.execute('''CREATE TABLE popular(page TEXT,title TEXT,image_url TEXT,url TEXT,released TEXT)''')
#c.execute('''CREATE TABLE episode(anime_id TEXT,iframe TEXT,episode_id TEXT,episode_number TEXT)''')



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get('/api/details/{animeid}')
async def details(animeid: str):
    animeData = {}
    c.execute('SELECT * FROM animes WHERE anime_id=?;',(animeid,))
    data = c.fetchone()
    if not data:

        detail = GogoanimeParser.details(animeid=animeid)
        add_to_Tasks_table = "INSERT INTO animes (anime_id,title, year,other_names,type,status,genre,episodes,image_url,plot_summary) values (?,?,?,?, ?,?,?, ?,?,?)"
        c.execute(add_to_Tasks_table,(animeid,detail['title'],detail['year'],detail['other_names'],detail['type'],detail['status'], detail['genre'],detail['episodes'],detail['image_url'],detail['plot_summary']))
        conn.commit()
        return detail
    else:
        animeData["anime_id"]=data[0]
        animeData["title"]=data[1]
        animeData["year"]=data[2]
        animeData["other_names"]=data[3]
        animeData["type"]=data[4]
        animeData["status"]=data[5]
        animeData["genre"]=data[6]
        animeData["episodes"]=data[7]
        animeData["image_url"]=data[8]
        animeData["plot_summary"]=data[9]
   
        return animeData


@app.get('/api/recently/{page}')
async def recently(page: int):
    recently = GogoanimeParser.get_recently_uploaded(page=page)
    return json.loads(recently)

@app.get('/api/latest/{page}')
async def latest(page: int):
    latest = GogoanimeParser.latest(page=page)
    return json.loads(latest)


@app.get('/api/{animeid}/episode/{episode_num}')
async def episode(animeid: str, episode_num: int):
    episodeData = {}
    c.execute('SELECT * FROM episode WHERE anime_id=? AND episode_number = ?;',(animeid,episode_num,))
    data = c.fetchone()
    if not data:
        episode = GogoanimeParser.episode(animeid=animeid, episode_num=episode_num)
        add_episode = "INSERT INTO episode (anime_id,iframe,episode_id,episode_number) values (?,?,?,?)"
        c.execute(add_episode,(animeid,episode['iframe'],episode['epid'],episode_num))
        conn.commit()
        return episode
    else:  
        episodeData['anime_id'] = data[0]
        episodeData['iframe'] = data[1]
        episodeData['epid'] = data[2]
        episodeData['episode_num'] = data[3]

        return episodeData

  

@app.get('/api/popular/{page}')
async def popular(page: int):
    animeData = []
    add_to_popular = "INSERT INTO popular (page,title, image_url,url,released) values (?,?,?,?,?)"

    
    c.execute('SELECT * FROM popular WHERE page=?;',(page,))
    fetchAll = c.fetchall()
    if not fetchAll:
        popular = GogoanimeParser.popular(page=page)
        data = json.loads(popular)
        for x in data:
            c.execute(add_to_popular,(page,x['title'],x['image_url'],x['url'],x['released']))
            conn.commit()
        return json.loads(popular)



    else:
        for x in fetchAll:
            animeData.append({"page":x[0],"title":x[1],"image_url":x[2],"url":x[3],"released":x[4]})



        return animeData

@app.get('/api/new-season/{page}')
async def newseason(page: int):
    newseason = GogoanimeParser.newSeason(page=page)
    return json.loads(newseason)

@app.get('/api/movies/{page}')
async def movies(page: int):
    movies = GogoanimeParser.movies(page=page)
    return json.loads(movies)

@app.get('/api/search/{key}/{page}')
async def search(key: str ,page: int):
    search = GogoanimeParser.search(key=key,page=page)
    return search


@app.get('/api/category/{genre}/{page}')
async def genre(genre: str, page: int):
    genre = GogoanimeParser.genre(genre_name=genre, page=page)
    return genre




@app.get('/api/schedule/{animeid}')
async def details(animeid: str):
    schedule = GogoanimeParser.schedule(animeid=animeid)
    return schedule





@app.get("/")
def main():
    return {
        "message": "Hello my friend"
    }
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
