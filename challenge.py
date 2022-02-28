import requests
import json
import math

#La función get_id extrae el ID de cada película y lo utiliza como parámetro de la función get_movies
#para obtener un diccionario de cada película de la plataforma con sus metadatos e ir almacenando cada diccionario en una lista.
def get_id(url):
    movie_list = []
    url1 = 'https://yts.mx/api/v2/movie_details.json'
    response = requests.get(url, params = {'limit': 50})
    if response.status_code == 200:
        payload = response.json()
        datas = payload.get('data',[])
    	if datas:
        	movies_count = datas['movie_count']
        	limit = datas['limit']            
    		if movies_count%limit != 0:
        		number_page = math.floor(movies_count/limit) + 1
   		else:
        		number_page = movies_count/limit 
    for i in range(1,number_page + 1):       
        response = requests.get(url, params = {'page':i, 'limit': limit})
        if response.status_code == 200:
	    payload = response.json()
            datas = payload.get('data',[])
            if datas:
            	movies = datas['movies']                
        	for j in movies:
           		id = j['id']
            movie = get_movies(url1,id) #En la variable movie almacenamos el diccionario que devuelve la función get_movies
            movie_list.append(movie)	#y lo agregamos a la lista movie_list.	
   
#Con la lista completa con todos los contenidos de la plataforma, generamos el archivo json.
    with open('movies.json', 'w') as f:
	    json.dump(movie_list, f, indent=4)

#La función get_movies devuelve un diccionario con todos los metadatos de la película que pasemos como parámetro con el ID
def get_movies(url,id):
    d = {}
    response = requests.get(url, params = {'movie_id':id})
    if response.status_code == 200:
        payload = response.json()
        datas = payload.get('data',[])
        d['id'] = datas['movie'].get('id')
        d['titulo'] = datas['movie'].get('title')
        d['year'] = datas['movie'].get('year')
        d['genero'] = datas['movie'].get('genres')	
        d['sinopsis'] = datas['movie'].get('description_full')
        d['url'] = datas['movie'].get('url')
        d['rating']	= datas['movie'].get('rating')
        d['descargas'] = datas['movie'].get('download_count')
        d['likes'] = datas['movie'].get('like_count')
        d['idioma'] = datas['movie'].get('language')
        d['duracion'] = datas['movie'].get('runtime')
    return d		

url = 'https://yts.mx/api/v2/list_movies.json'
get_id(url)
