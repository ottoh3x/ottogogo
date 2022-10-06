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


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/details/{animeid}')
async def details(animeid: str):
    animeData = []
    c.execute('SELECT * FROM animes WHERE anime_id=?;',(animeid,))
    
    data = c.fetchone()
    animeData.append({
        "anime_id":data[0],
        "title":data[1],
        "year":data[2],
        "other_names":data[3],
        "type":data[4],
        "status":data[5],
        "genre":data[6],
        "episodes":data[7],
        "image_url":data[8],
        "plot_summary":data[9],
    })
    print(len(data))
  
    return animeData


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


@app.get('/api/popular/{page}')
async def popular(page: int):
    popular = GogoanimeParser.popular(page=page)
  
    return json.loads(popular)

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


@app.get('/api/{animeid}/episode/{episode_num}')
async def episode(animeid: str, episode_num: int):
    episode = GogoanimeParser.episode(animeid=animeid, episode_num=episode_num)
    return episode


@app.get("/")
def main():
    return {
        "message": "Hello my friend"
    }
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
