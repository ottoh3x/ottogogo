from bs4 import BeautifulSoup
import json
import requests
import cfscrape
import base64


headers = {
   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
}
s = requests.Session()

scraper = cfscrape.create_scraper()



class GogoanimeParser():
    def __init__(self, page, animeid, episode_num, key):
        self.page = page
        self.animeid = animeid
        self.episode_num = episode_num

    def search(key, page):
        r = s.get(
            f'https://gogoanime.lu/search.html?keyword={key}&page={page}',headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        search = soup.find('div', 'last_episodes').find('ul', 'items')
        search_list = search.find_all('li')

        animes_res = [{}]
        animes = []
        for x in search_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            animes.append({"title": f"{title}", "image_url": f"{image_url}",
                          "url": f"{url}", "released": f"{released}"})

        animes_res.append(animes)
        searched_animes = json.dumps(animes)
        search_data = json.loads(searched_animes)
        return search_data

    def get_recently_uploaded(page):
        try:
            r = s.get(f'https://gogoanime.lu/?page={page}',headers=headers).text
            soup = BeautifulSoup(r, 'html.parser')
            recently = soup.find('div', 'last_episodes').find('ul', 'items')
            recently_list = recently.find_all('li')
            anilist = dict()

            gen_ani_res = [{}]
            gen_ani = []
            for x in recently_list:
                title = x.find('p', 'name').text
                image_url = x.find('img')['src']
                url = x.find('a')['href']
                url = url.replace('/', '')
                get_id = image_url.replace(
                    '.png', '').replace('.jpg', '').split('/')
                id = get_id[-1]
                episode = x.find('p', 'episode').text
                episode = episode.replace('Episode ', '')

                gen_ani.append({"title": f"{title}", "id": f"{id}",
                                "image_url": f"{image_url}", "url": f"{url}", "episode": f"{episode}"})

            gen_ani_res.append(gen_ani)
            jsonlist = json.dumps(gen_ani)

        except:
            print('im sorry otto i cannnot get the data :( ')
        return jsonlist

    def newSeason(page):
        r = s.get(
            f'https://gogoanime.lu/new-season.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        popular = soup.find('div', 'last_episodes').find('ul', 'items')
        popular_list = popular.find_all('li')

        newseason_animes_res = [{}]
        newseason_animes = []
        for x in popular_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            newseason_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        newseason_animes_res.append(newseason_animes)
        new_animes = json.dumps(newseason_animes)
        return new_animes

    def popular(page):
        r = s.get(f'https://gogoanime.lu/popular.html?page={page}',headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        popular = soup.find('div', 'last_episodes').find('ul', 'items')
        popular_list = popular.find_all('li')

        popular_animes_res = [{}]
        popular_animes = []
        for x in popular_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            popular_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        popular_animes_res.append(popular_animes)
        pop_animes = json.dumps(popular_animes)
        return pop_animes

    def movies(page):
        r = s.get(
            f'https://gogoanime.lu/anime-movies.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        movies = soup.find('div', 'last_episodes').find('ul', 'items')
        movies_list = movies.find_all('li')

        movie_animes_res = [{}]
        movies_animes = []
        for x in movies_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            movies_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        movie_animes_res.append(movies_animes)
        mov_animes = json.dumps(movies_animes)
        return mov_animes
   
    def latest(page):
       url = f"https://ajax.gogo-load.com/ajax/page-recent-release.html?page={page}&type=1"
       r = s.get(url).text
       soup = BeautifulSoup(r,"html.parser")
       anime = soup.find('ul','items').find_all('li')
       gen_ani_res = [{}]
       gen_ani = []
       for x in anime:
         url = x.find('a')['href']
         url = url.replace('/', '')
         title = x.find('p','name').text
         episode = x.find('p','episode').text
         image_url = x.img['src']
         get_id = image_url.replace(
                    '.png', '').replace('.jpg', '').split('/')
         id = get_id[-1]
         gen_ani.append({
           "title":title,
         'episode':episode,
         'image_url':image_url,
         'url': url,
            'id':id
       })
       gen_ani_res.append(gen_ani)
       jsonlist = json.dumps(gen_ani)

       return jsonlist

    def details(animeid):
        url = "https://gogoanime.lu/category/" + animeid
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
        image_url = source_url.get('src')
        title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
        lis = soup.find_all('p', {"class": "type"})
        plot_sum = lis[1]
        pl = plot_sum.get_text().split(':')
        pl.remove(pl[0])
        sum = ""
        plot_summary = sum.join(pl)
        type_of_show = lis[0].a['title']
        ai = lis[2].find_all('a')  # .find_all('title')
        genres = []
        for link in ai:
            genres.append(link.get('title'))
        year1 = lis[3].get_text()
        year2 = year1.split(" ")
        year = year2[1]
        status = lis[4].a.get_text()
        oth_names = lis[5].get_text()
        lnk = soup.find(id="episode_page")
        source_url = lnk.find_all("li")[-1].a
        ep_num = int(source_url.get("ep_end"))
        print(ep_num)
        res_detail_search = {"title": f"{title}", "year": f"{year}", "other_names": f"{oth_names}",
                             "type": f"{type_of_show}", "status": f"{status}", "genre": f"{genres}",
                             "episodes": f"{ep_num}", "image_url": f"{image_url}", "plot_summary": f"{plot_summary}"}

        return res_detail_search

    def genre(genre_name, page):
        try:
            url = f"https://gogoanime.lu/genre/{genre_name}?page={page}"
            response = s.get(url)
            plainText = response.text
            soup = BeautifulSoup(plainText, "html.parser")
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            gen_ani = []
            for anime in animes:  # For every anime found
                tits = anime.a["title"]
                image_url = anime.find('img')['src']
                urll = anime.a["href"]
                r = urll.split('/')
                released = anime.find('p', 'released').text
                released = released.strip()
                gen_ani.append(
                    {"title": f"{tits}", "url": f"{r[2]}", "image_url": f"{image_url}", "released": f"{released}"})

            return gen_ani
        except:
            print('not found')

    def episode(animeid, episode_num):
        links = {}
        URL_PATTERN = 'https://gogoanime.lu/{}-episode-{}'
        url = URL_PATTERN.format(animeid, episode_num)
        srcCode = s.get(url)
        soup = BeautifulSoup(srcCode.text, "html.parser")
        iframe = soup.find('div', 'anime_video_body')

        ifr = iframe.find('div', 'play-video').find('iframe')
        iframe = ifr['src']
        goload = soup.find('li','vidcdn').a['data-video']
        gogoserver = f"https:{goload}"
        epid = iframe.split('/')[3].split('?id=')[1].split('&')[0]
        
       

        links['iframe'] = f"https:{iframe}"
        links['gogoserver'] = gogoserver
        links['epid'] = epid
        return links
   
    def schedule(animeid):
        time = {}
        try:
            url=f"https://animeschedule.net/anime/{animeid}".replace("2nd-season",'2').replace('season-2',"2")
            r = s.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            t = soup.find(id="countdown-wrapper").time['datetime']
            time['time'] = t
            return time
        except:
            print("there is no schedule available")

