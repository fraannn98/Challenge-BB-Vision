import requests
import json
import math

#La función get_id extrae el ID de cada película y lo utiliza como parámetro de la función get_movies
#para obtener un diccionario de cada película de la plataforma con sus metadatos e ir almacenando cada diccionario en una lista.
def get_id(url_list,url_details,url_comments):
    movie_list = []
    response = requests.get(url_list, params = {'limit': 50})
    if response.status_code == 200:
        payload = response.json()
        datas = payload.get('data',[])
        if datas:
            movies_count = datas['movie_count']
            limit = datas['limit']
            number_page = total_pages(movies_count,limit)           
    for i in range(1,number_page + 1):       
        response = requests.get(url_list, params = {'page':i, 'limit': limit})
        if response.status_code == 200:
            payload = response.json()
            datas = payload.get('data',[])
            if datas:
                movies = datas['movies']
                for j in movies:
                    id = j['id']
                    movie = get_movies(url_details,id,url_comments) #En la variable movie almacenamos el diccionario que devuelve la función get_movies
                    movie_list.append(movie)	#y lo agregamos a la lista movie_list.	
        print("Página número:",i)
    return movie_list           


#La función get_movies devuelve un diccionario con todos los metadatos de la película que pasemos como parámetro con el ID
def get_movies(url_details,id,url_comments):
    d = {}
    response = requests.get(url_details, params = {'movie_id':id})
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
        # d['comentarios'] = get_comments(id,url_comments)
    return d	

#la función get_comments devuelve los comentarios de cada película (al no funcionar el endpoint, dejo comentada la función)
# def get_comments(id,url_comments):
#     response = requests.get(url_comments, params = {'movie_id':id})
#     if response.status_code == 200:
#         comentarios = response['data']['comments']
#     return comentarios    

#La función total_pages devuelve la cantidad total de paginas que tiene la plataforma.
def total_pages(movies_count,limit):            
    if movies_count%limit != 0:
        number_page = math.floor(movies_count/limit) + 1
    else:
        number_page = movies_count/limit
    return number_page

if __name__ == '__main__':
    url_list = 'https://yts.mx/api/v2/list_movies.json'
    url_details = 'https://yts.mx/api/v2/movie_details.json'
    url_comments = 'https://yts.mx/api/v2/movie_comments.json'
    movie_list = get_id(url_list,url_details,url_comments)
    
    #Con la lista completa con todos los contenidos de la plataforma, generamos el archivo json.
    with open('movies.json', 'w') as f:
	    json.dump(movie_list, f, indent=4)