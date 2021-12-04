# ! pip install bs4
# ! pip install requests

import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option('display.max_columns',None)


### 1. CATEGORY -> COMEDY MOVIES & TV SERIES ###

comedyMovieRequestList = ["https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&view=advanced",
                     "https://www.imdb.com/search/title/?genres=comedy&start=51&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=comedy&start=101&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=comedy&start=151&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=comedy&start=201&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=comedy&start=251&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=comedy&start=301&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=comedy&start=351&explore=title_type,genres&ref_=adv_nxt"]


comedy_movie_name = []
comedy_movie_year = []
comedy_movie_time = []
comedy_movie_rating = []
comedy_movie_genres = []
comedy_movie_metascore = []
comedy_movie_exp = []
comedy_movie_director = []
comedy_votes = []

comedy_movie_list_len = len(comedyMovieRequestList)

for i in range (comedy_movie_list_len):
    url = comedyMovieRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        comedy_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        comedy_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        comedy_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        comedy_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        comedy_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        comedy_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        comedy_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            comedy_movie_director.append(cast[0])

        else:
            cast = None
            comedy_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        comedy_votes.append(votes)


comedy = {'Movie': comedy_movie_name, 'Production Year': comedy_movie_year, 'Watchtime': comedy_movie_time, 'Rating': comedy_movie_rating,
                         'Metascore': comedy_movie_metascore, 'Genres': comedy_movie_genres, 'Description': comedy_movie_exp, 'Votes':comedy_votes,
                         "Director": comedy_movie_director}

ComedyMovies = pd.DataFrame.from_dict(comedy, orient='index')
ComedyMovies = ComedyMovies.transpose()



### 2. CATEGORY -> SCI-FI MOVIES & TV SHOWS ###

scifiRequestList = ["https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_2",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=51&explore=title_type,genres&ref_=adv_nxt",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=101&explore=title_type,genres&ref_=adv_nxt",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=151&explore=title_type,genres&ref_=adv_nxt",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=201&explore=title_type,genres&ref_=adv_nxt",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=251&explore=title_type,genres&ref_=adv_nxt",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=301&explore=title_type,genres&ref_=adv_nxt",
                    "https://www.imdb.com/search/title/?genres=sci-fi&start=351&explore=title_type,genres&ref_=adv_nxt"]


scifi_movie_name = []
scifi_movie_year = []
scifi_movie_time = []
scifi_movie_rating = []
scifi_movie_genres = []
scifi_movie_metascore = []
scifi_movie_exp = []
scifi_movie_director = []
scifi_votes = []


scifi_movie_list_len = len(scifiRequestList)

for i in range (scifi_movie_list_len):
    url = scifiRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        scifi_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        scifi_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        scifi_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        scifi_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        scifi_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        scifi_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        scifi_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n","").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            scifi_movie_director.append(cast[0])

        else:
           cast = None
           scifi_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        scifi_votes.append(votes)

scifi = {'Movie': scifi_movie_name, 'Production Year': scifi_movie_year, 'Watchtime': scifi_movie_time, 'Rating': scifi_movie_rating,
                         'Metascore': scifi_movie_metascore, 'Genres': scifi_movie_genres, 'Description': scifi_movie_exp,'Votes':scifi_votes,
                         "Director": scifi_movie_director}

ScifiMovies = pd.DataFrame.from_dict(scifi, orient='index')
ScifiMovies = ScifiMovies.transpose()



### 3. CATEGORY -> HORROR MOVIES & TV SHOWS ###

horrorRequestList = ["https://www.imdb.com/search/title/?genres=horror&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_3",
                     "https://www.imdb.com/search/title/?genres=horror&start=51&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=horror&start=101&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=horror&start=151&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=horror&start=201&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=horror&start=251&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=horror&start=301&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=horror&start=351&explore=title_type,genres&ref_=adv_nxt"]


horror_movie_name = []
horror_movie_year = []
horror_movie_time = []
horror_movie_rating = []
horror_movie_genres = []
horror_movie_metascore = []
horror_movie_exp = []
horror_movie_director = []
horror_votes = []


horror_movie_list_len = len(horrorRequestList)

for i in range (horror_movie_list_len):
    url = horrorRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        horror_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        horror_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        horror_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        horror_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        horror_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        horror_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        horror_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            horror_movie_director.append(cast[0])

        else:
            cast = None
            horror_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        horror_votes.append(votes)

horror= {'Movie': horror_movie_name, 'Production Year': horror_movie_year, 'Watchtime': horror_movie_time, 'Rating': horror_movie_rating,
                         'Metascore': horror_movie_metascore, 'Genres': horror_movie_genres, 'Description': horror_movie_exp,'Votes':horror_votes,
                         "Director": horror_movie_director}

HorrorMovies = pd.DataFrame.from_dict(horror, orient='index')
HorrorMovies = HorrorMovies.transpose()



### 4. CATEGORY -> ROMANCE MOVIES & TV SHOWS ###

romanceRequestList = ["https://www.imdb.com/search/title/?genres=romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_1",
                      "https://www.imdb.com/search/title/?genres=romance&start=51&explore=title_type,genres&ref_=adv_nxt",
                      "https://www.imdb.com/search/title/?genres=romance&start=101&explore=title_type,genres&ref_=adv_nxt",
                      "https://www.imdb.com/search/title/?genres=romance&start=151&explore=title_type,genres&ref_=adv_nxt",
                      "https://www.imdb.com/search/title/?genres=romance&start=201&explore=title_type,genres&ref_=adv_nxt",
                      "https://www.imdb.com/search/title/?genres=romance&start=251&explore=title_type,genres&ref_=adv_nxt",
                      "https://www.imdb.com/search/title/?genres=romance&start=301&explore=title_type,genres&ref_=adv_nxt",
                      "https://www.imdb.com/search/title/?genres=romance&start=351&explore=title_type,genres&ref_=adv_nxt"]


romance_movie_name = []
romance_movie_year = []
romance_movie_time = []
romance_movie_rating = []
romance_movie_genres = []
romance_movie_metascore = []
romance_movie_exp = []
romance_movie_director = []
romance_votes =[]

romance_movie_list_len = len(romanceRequestList)

for i in range (romance_movie_list_len):
    url = romanceRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        romance_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        romance_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        romance_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        romance_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        romance_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        romance_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        romance_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            romance_movie_director.append(cast[0])

        else:
            cast = None
            romance_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        romance_votes.append(votes)


romance= {'Movie': romance_movie_name, 'Production Year': romance_movie_year, 'Watchtime': romance_movie_time, 'Rating': romance_movie_rating,
                         'Metascore': romance_movie_metascore, 'Genres': romance_movie_genres, 'Description': romance_movie_exp,'Votes':romance_votes,
                         "Director": romance_movie_director}

RomanceMovies = pd.DataFrame.from_dict(romance, orient='index')
RomanceMovies = RomanceMovies.transpose()
RomanceMovies.head()



### 5. CATEGORY -> ACTION MOVIES & TV SHOWS ###
actionRequestList = ["https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2",
                     "https://www.imdb.com/search/title/?genres=action&start=51&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=action&start=101&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=action&start=151&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=action&start=201&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=action&start=251&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=action&start=301&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=action&start=351&explore=title_type,genres&ref_=adv_nxt"]


action_movie_name = []
action_movie_year = []
action_movie_time = []
action_movie_rating = []
action_movie_genres = []
action_movie_metascore = []
action_movie_exp = []
action_movie_director = []
action_votes =[]

action_movie_list_len = len(actionRequestList)

for i in range (action_movie_list_len):
    url = actionRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        action_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        action_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        action_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        action_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        action_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        action_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        action_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            action_movie_director.append(cast[0])

        else:
            cast = None
            action_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        action_votes.append(votes)


action= {'Movie': action_movie_name, 'Production Year': action_movie_year, 'Watchtime': action_movie_time, 'Rating': action_movie_rating,
                         'Metascore': action_movie_metascore, 'Genres': action_movie_genres, 'Description': action_movie_exp,'Votes':action_votes,
                         "Director": action_movie_director}

ActionMovies = pd.DataFrame.from_dict(action, orient='index')
ActionMovies = ActionMovies.transpose()
ActionMovies.head()



### 6. CATEGORY -> THRILLER MOVIES & TV SHOWS ###

thrillerRequestList = ["https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_3",
                       "https://www.imdb.com/search/title/?genres=thriller&start=51&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=thriller&start=101&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=thriller&start=151&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=thriller&start=201&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=thriller&start=251&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=thriller&start=301&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=thriller&start=351&explore=title_type,genres&ref_=adv_nxt"]


thriller_movie_name = []
thriller_movie_year = []
thriller_movie_time = []
thriller_movie_rating = []
thriller_movie_genres = []
thriller_movie_metascore = []
thriller_movie_exp = []
thriller_movie_director = []
thriller_votes =[]

thriller_movie_list_len = len(thrillerRequestList)

for i in range (thriller_movie_list_len):
    url = thrillerRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        thriller_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        thriller_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        thriller_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        thriller_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        thriller_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        thriller_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        thriller_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            thriller_movie_director.append(cast[0])

        else:
            cast = None
            thriller_movie_director.append(cast)


        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        thriller_votes.append(votes)


thriller= {'Movie': thriller_movie_name, 'Production Year': thriller_movie_year, 'Watchtime': thriller_movie_time, 'Rating': thriller_movie_rating,
                         'Metascore': thriller_movie_metascore, 'Genres': thriller_movie_genres, 'Description': thriller_movie_exp,'Votes':thriller_votes,
                         "Director": thriller_movie_director}


ThrillerMovies = pd.DataFrame.from_dict(thriller, orient='index')
ThrillerMovies = ThrillerMovies.transpose()
ThrillerMovies.head()


### 7. CATEGORY -> DRAMA MOVIES & TV SHOWS ###

dramaRequestList = ["https://www.imdb.com/search/title/?genres=drama&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=Q5TP06SQYBQWVCQBRAZH&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_1",
                       "https://www.imdb.com/search/title/?genres=drama&start=51&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=drama&start=101&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=drama&start=151&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=drama&start=201&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=drama&start=251&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=drama&start=301&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=drama&start=351&explore=title_type,genres&ref_=adv_nxt"]


drama_movie_name = []
drama_movie_year = []
drama_movie_time = []
drama_movie_rating = []
drama_movie_genres = []
drama_movie_metascore = []
drama_movie_exp = []
drama_movie_director = []
drama_votes =[]

drama_movie_list_len = len(dramaRequestList)

for i in range (drama_movie_list_len):
    url = dramaRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        drama_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        drama_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        drama_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        drama_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        drama_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        drama_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        drama_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            drama_movie_director.append(cast[0])

        else:
            cast = None
            drama_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        drama_votes.append(votes)


drama= {'Movie': drama_movie_name, 'Production Year': drama_movie_year, 'Watchtime': drama_movie_time, 'Rating': drama_movie_rating,
                         'Metascore': drama_movie_metascore, 'Genres': drama_movie_genres, 'Description': drama_movie_exp,'Votes':drama_votes,
                         "Director": drama_movie_director}

DramaMovies = pd.DataFrame.from_dict(drama, orient='index')
DramaMovies = DramaMovies.transpose()
DramaMovies.head()


### 8. CATEGORY -> MYSTERY MOVIES & TV SHOWS ###

mysteryRequestList = ["https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_2",
                       "https://www.imdb.com/search/title/?genres=mystery&start=51&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=mystery&start=101&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=mystery&start=151&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=mystery&start=201&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=mystery&start=251&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=mystery&start=301&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=mystery&start=351&explore=title_type,genres&ref_=adv_nxt"]


mystery_movie_name = []
mystery_movie_year = []
mystery_movie_time = []
mystery_movie_rating = []
mystery_movie_genres = []
mystery_movie_metascore = []
mystery_movie_exp = []
mystery_movie_director = []
mystery_votes =[]

mystery_movie_list_len = len(mysteryRequestList)

for i in range (mystery_movie_list_len):
    url = mysteryRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        mystery_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        mystery_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        mystery_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        mystery_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        mystery_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        mystery_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        mystery_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()
        if 'Director' in cast:
            cast = cast.split('|')

            mystery_movie_director.append(cast[0])

        else:
            cast = None
            mystery_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        mystery_votes.append(votes)


mystery= {'Movie': mystery_movie_name, 'Production Year': mystery_movie_year, 'Watchtime': mystery_movie_time, 'Rating': mystery_movie_rating,
                         'Metascore': mystery_movie_metascore, 'Genres': mystery_movie_genres, 'Description': mystery_movie_exp,'Votes':mystery_votes,
                         "Director": mystery_movie_director}

MysteryMovies = pd.DataFrame.from_dict(mystery, orient='index')
MysteryMovies = MysteryMovies.transpose()
MysteryMovies.head()





### 9. CATEGORY -> CRIME MOVIES & TV SHOWS ###

crimeRequestList =  ["https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_3",
                     "https://www.imdb.com/search/title/?genres=crime&start=51&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=crime&start=101&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=crime&start=151&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=crime&start=201&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=crime&start=251&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=crime&start=301&explore=title_type,genres&ref_=adv_nxt",
                     "https://www.imdb.com/search/title/?genres=crime&start=351&explore=title_type,genres&ref_=adv_nxt"
                     ]

crime_movie_name = []
crime_movie_year = []
crime_movie_time = []
crime_movie_rating = []
crime_movie_genres = []
crime_movie_metascore = []
crime_movie_exp = []
crime_movie_director = []
crime_votes =[]

crime_movie_list_len = len(crimeRequestList)

for i in range (crime_movie_list_len):
    url = crimeRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        crime_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        crime_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        crime_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        crime_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        crime_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        crime_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        crime_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()

        if 'Director' in cast:
            cast = cast.split('|')

            crime_movie_director.append(cast[0])

        else:
            cast = None
            crime_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        crime_votes.append(votes)


crime= {'Movie': crime_movie_name, 'Production Year': crime_movie_year, 'Watchtime': crime_movie_time, 'Rating': crime_movie_rating,
                         'Metascore': crime_movie_metascore, 'Genres': crime_movie_genres, 'Description': crime_movie_exp,'Votes':crime_votes,
                         "Director": crime_movie_director}

CrimeMovies = pd.DataFrame.from_dict(crime, orient='index')
CrimeMovies = CrimeMovies.transpose()
CrimeMovies.head()


### 10. CATEGORY -> ADVENTURE MOVIES & TV SHOWS ###
adventureRequestList = ["https://www.imdb.com/search/title/?genres=adventure&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_2",
                       "https://www.imdb.com/search/title/?genres=adventure&start=51&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=adventure&start=101&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=adventure&start=151&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=adventure&start=201&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=adventure&start=251&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=adventure&start=301&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=adventure&start=351&explore=title_type,genres&ref_=adv_nxt"]


adventure_movie_name = []
adventure_movie_year = []
adventure_movie_time = []
adventure_movie_rating = []
adventure_movie_genres = []
adventure_movie_metascore = []
adventure_movie_exp = []
adventure_movie_director = []
adventure_votes =[]

adventure_movie_list_len = len(adventureRequestList)

for i in range (adventure_movie_list_len):
    url = adventureRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        adventure_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        adventure_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        adventure_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        adventure_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        adventure_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        adventure_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        adventure_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()

        if 'Director' in cast:
            cast = cast.split('|')

            adventure_movie_director.append(cast[0])

        else:
            cast = None
            adventure_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        adventure_votes.append(votes)


adventure= {'Movie': adventure_movie_name, 'Production Year': adventure_movie_year, 'Watchtime': adventure_movie_time, 'Rating': adventure_movie_rating,
                         'Metascore': adventure_movie_metascore, 'Genres': adventure_movie_genres, 'Description': adventure_movie_exp,'Votes':adventure_votes,
                         "Director": adventure_movie_director}

AdventureMovies = pd.DataFrame.from_dict(adventure, orient='index')
AdventureMovies = AdventureMovies.transpose()
AdventureMovies.head()



### 11. CATEGORY -> FANTASY MOVIES & TV SHOWS ###

fantasyRequestList = ["https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=433TK6V35DY4TQZN3KKK&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_3",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=51&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=101&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=151&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=201&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=251&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=301&explore=title_type,genres&ref_=adv_nxt",
                       "https://www.imdb.com/search/title/?genres=fantasy&start=351&explore=title_type,genres&ref_=adv_nxt"]


fantasy_movie_name = []
fantasy_movie_year = []
fantasy_movie_time = []
fantasy_movie_rating = []
fantasy_movie_genres = []
fantasy_movie_metascore = []
fantasy_movie_exp = []
fantasy_movie_director = []
fantasy_votes =[]

fantasy_movie_list_len = len(fantasyRequestList)

for i in range (fantasy_movie_list_len):
    url = fantasyRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        fantasy_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        fantasy_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        fantasy_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        fantasy_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        fantasy_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        fantasy_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        fantasy_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()

        if 'Director' in cast:
            cast = cast.split('|')

            fantasy_movie_director.append(cast[0])

        else:
            cast = None
            fantasy_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        fantasy_votes.append(votes)


fantasy= {'Movie': fantasy_movie_name, 'Production Year': fantasy_movie_year, 'Watchtime': fantasy_movie_time, 'Rating': fantasy_movie_rating,
                         'Metascore': fantasy_movie_metascore, 'Genres': fantasy_movie_genres, 'Description': fantasy_movie_exp,'Votes':fantasy_votes,
                         "Director": fantasy_movie_director}

FantasyMovies = pd.DataFrame.from_dict(fantasy, orient='index')
FantasyMovies = FantasyMovies.transpose()
FantasyMovies.head()




### 12. CATEGORY -> SUPERHERO MOVIES & TV SHOWS ###

superheroRequestList = ["https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_3",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=2",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=3",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=4",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=5",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=6",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=7",
                       "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=RDWWHMHGTWVGT0SYCQGT&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=8"]


superhero_movie_name = []
superhero_movie_year = []
superhero_movie_time = []
superhero_movie_rating = []
superhero_movie_genres = []
superhero_movie_metascore = []
superhero_movie_exp = []
superhero_movie_director = []
superhero_votes =[]

superhero_movie_list_len = len(superheroRequestList)

for i in range (superhero_movie_list_len):
    url = superheroRequestList[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        superhero_movie_name.append(name)

        year = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        superhero_movie_year.append(year)

        runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','') if store.p.find('span',class_ = 'runtime') else '0'
        superhero_movie_time.append(runtime)

        rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n','') if store.find('div', class_='inline-block ratings-imdb-rating') else 0
        superhero_movie_rating.append(rate)

        genres = store.p.find('span',class_ = 'genre').text.replace("\n","").replace(" ","") if store.p.find('span',class_ = 'genre') else ''
        superhero_movie_genres.append(genres)

        meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
        superhero_movie_metascore.append(meta)

        describe = store.find_all('p', class_='text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '*****'
        superhero_movie_exp.append(description_)

        cast = store.find("p", class_='').text.replace("\n", "").strip()

        if 'Director' in cast:
            cast = cast.split('|')

            superhero_movie_director.append(cast[0])

        else:
            cast = None
            superhero_movie_director.append(cast)

        votes = store.find('span', attrs={'name': 'nv'}).text if store.find('span', attrs={'name': 'nv'}) else '0'
        superhero_votes.append(votes)


superhero= {'Movie': superhero_movie_name, 'Production Year': superhero_movie_year, 'Watchtime': superhero_movie_time, 'Rating': superhero_movie_rating,
                         'Metascore': superhero_movie_metascore, 'Genres': superhero_movie_genres, 'Description': superhero_movie_exp,'Votes':superhero_votes,
                         "Director": superhero_movie_director}

SuperHeroMovies = pd.DataFrame.from_dict(action, orient='index')
SuperHeroMovies = SuperHeroMovies.transpose()



main_df = pd.concat([ActionMovies,AdventureMovies,ComedyMovies,CrimeMovies,DramaMovies,FantasyMovies,HorrorMovies,MysteryMovies,
                   RomanceMovies,ScifiMovies,SuperHeroMovies,ThrillerMovies])


main_df = main_df.iloc[main_df.astype(str).drop_duplicates(keep = False,ignore_index=True).index]


### SAVING MOVIES AS CSV FILE ###

main_df.to_csv('movie.csv', index=False)

ActionMovies.to_csv('action_movie.csv',index = False)
AdventureMovies.to_csv('adventure_movie.csv',index = False)
ComedyMovies.to_csv('comedy_movie.csv',index = False)
CrimeMovies.to_csv('crime_movie.csv',index = False)
DramaMovies.to_csv('drama_movie.csv',index = False)
FantasyMovies.to_csv('fantasy_movie.csv',index = False)
HorrorMovies.to_csv('horror_movie.csv',index = False)
MysteryMovies.to_csv('mystery_movie.csv',index = False)
RomanceMovies.to_csv('romance_movie.csv',index = False)
ScifiMovies.to_csv('scifi_movie.csv',index = False)
SuperHeroMovies.to_csv('superhero_movie.csv',index = False)
ThrillerMovies.to_csv('thriller_movie.csv',index = False)



new_df = main_df.drop_duplicates(subset ="Movie",keep = 'first').reset_index(drop = True)
new_df = new_df.sort_values(by = 'Movie')

new_df.to_csv('cleaned_movies.csv', index=False)






















