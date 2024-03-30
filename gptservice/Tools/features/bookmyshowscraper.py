import os
import json
from zenrows import ZenRowsClient

zenrows_key = os.environ.get('zenrows_key')

class BookMyShow:
    def __init__(self, **args):
        self.city = args.get('city')
        self.language = args.get('movie_language')
        self.movie = args.get('movie_name')
        self.date = args.get('date')

    def invoke_service(self):
        try:
            print("Payloads: %s, %s, %s, %s"% (self.city, self.language, self.movie, self.date))
            if self.city and self.language is not None and self.movie is None or self.movie == "dummy":        
                return self.list_movies()
            
            elif self.city and self.language and self.movie is not None:
                return self.get_movie_details()
        
        except Exception as e:
            print('Error extracting BookMyShow details')
            print(e)
            return

    def list_movies(self):
        url = "https://in.bookmyshow.com/explore/movies-"+self.city + "?languages=" + self.language.lower()
        names = []
        urls=[]
        data = self.triggerzenrowsapi(url)            
        for item in data:
            if isinstance(item, dict) and 'product' in item:
                if item['product'] == 'movies' and item['widget_id'] != 'COMING_SOON_WEB':
                    code = item['event_code']
                    title = item['title'].lower()
                    names.append(title)
                    moviestr = title.replace(" ", "-").replace(":", "")
                    urls.append("https://in.bookmyshow.com/"+self.city + "/movies/" + moviestr + "/" + code)
        return names,urls

    def triggerzenrowsapi(self, url):
        client = ZenRowsClient(zenrows_key)
        params = {"js_render":"true","autoparse":"true"}
        response = client.get(url,params=params)
        data = json.loads(response.text)
        return data
    
    def get_movie_details(self):
        names, urls = self.list_movies()
        for name in names:
            movie_words = self.movie.lower().split()
            name_words = name.lower().split()
            print(name_words, movie_words)
            match_count = sum(word in name_words for word in movie_words)
            if match_count >= 1:
                index = names.index(name)
                movie_name=names[index]
                url=urls[index]
                data = self.triggerzenrowsapi(url)  
                for item in data:
                    if isinstance(item, dict) and '@type' in item:
                        if item['@type'] == 'Movie':                            
                            language=item['inLanguage']
                            description=item['description']
                            pubdate=item['datePublished']
                            duration = item['duration']
                            hours = duration // 60
                            minutes = duration % 60
                return (f"Language: {language} Description: {description} releasedate: {pubdate} Url: {url} duration: {hours} hours {minutes} minutes")