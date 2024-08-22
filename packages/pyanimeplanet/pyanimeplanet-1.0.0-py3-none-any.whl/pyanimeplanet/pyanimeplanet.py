from bs4 import BeautifulSoup
import math
import re
import sys
from selenium import webdriver

def set_username(name):
    global username
    username = name

def count_extract(source):
    return str(str(source).split('>')[1]).split('<')[0]

def check_username(name):
    profile_link = f"https://www.anime-planet.com/users/{name}"
    dr = webdriver.Chrome()
    dr.get(profile_link)
    source = BeautifulSoup(dr.page_source, 'html.parser')
    data = source.find('div', class_="lifeOnAnime")

    if str(data) == 'None':
        sys.exit("Error : username is not valid. Enter a valid username")
    elif name == "":
        sys.exit("Error : username is not valid. Enter a valid username")
    else:
        return True


def calculate_time_minutes(min,hours,days,weeks,months,years):
    hours_min = int(hours) * 60
    days_min = int(days) * 24 * 60
    weeks_min = int(weeks) * 7 * 24 * 60
    months_min = int(months) * 30 * 7 * 24 * 60
    years_min = int(years) * 12 * 30 * 7 * 24 * 60    
    total_minutes = int(min) + hours_min + days_min + weeks_min + months_min + years_min
    
    return total_minutes

def calculate_time_hours(min,hours,days,weeks,months,years):
    in_minutes = calculate_time_minutes(min,hours,days,weeks,months,years)
    return format(float(in_minutes / 60),".2f")

def get_total_anime_rating(source):
    total_anime_rating = int(str(str(source.find('p', class_= "plr-total pure-1-4")).split('>')[1]).split('\n')[1])
    return total_anime_rating

def anime_stats():
    if check_username(username):
        profile_link = f"https://www.anime-planet.com/users/{username}"
        dr = webdriver.Chrome()
        dr.get(profile_link)
        source = BeautifulSoup(dr.page_source, 'html.parser')
        animelist_data = source.find('div', class_="plr-list pure-1 md-1-2")
     
        # watched
        watched = (animelist_data.find('li',class_="status1")).find('span',class_="slCount")
        watched_count = count_extract(watched)
     
        # watching
        watching = (animelist_data.find('li',class_="status2")).find('span',class_="slCount")
        watching_count = count_extract(watching)
     
        want_to_watch = (animelist_data.find('li',class_="status4")).find('span',class_="slCount")
        want_to_watch_count = count_extract(want_to_watch)
     
        stalled = (animelist_data.find('li',class_="status5")).find('span',class_="slCount")
        stalled_count = count_extract(stalled)
     
        dropped = (animelist_data.find('li',class_="status3")).find('span',class_="slCount")
        dropped_count = count_extract(dropped)
     
        wont_watch = (animelist_data.find('li',class_="status6")).find('span',class_="slCount")
        wont_watch_count = count_extract(wont_watch)
     
        total_episodes = (animelist_data.find('i', id="totalEps"))
        total_episodes_count = count_extract(total_episodes).replace(',','')
     
        life_on_anime_data = str(source.find('ul', class_= "loa-labels pure-g")).split('>')
        minutes = str(life_on_anime_data[2]).split('\n')[0]
        hours = str(life_on_anime_data[6]).split('\n')[0]
        days = str(life_on_anime_data[10]).split('\n')[0]
        weeks = str(life_on_anime_data[14]).split('\n')[0]
        months = str(life_on_anime_data[18]).split('\n')[0]
        years = str(life_on_anime_data[22]).split('\n')[0]
        life_on_anime_min = calculate_time_minutes(minutes,hours,days,weeks,months,years)
        life_on_anime_hours = calculate_time_hours(minutes,hours,days,weeks,months,years)
        total_anime_rating = get_total_anime_rating(source)
     
        animestats = {
            "watched": int(watched_count), 
            "watching" : int(watching_count), 
            "want to watch" : int(want_to_watch_count), 
            "stalled" : int(stalled_count), 
            "dropped" : int(dropped_count), 
            "won't watch" : int(wont_watch_count),
            "total episodes" : int(total_episodes_count),
            "total watchtime (in minutes)" : life_on_anime_min,
            "total watchtime (in hours)" : float(life_on_anime_hours),
            "total anime ratings" : total_anime_rating,
        }
     
        return animestats

def watched_list():
    try:
        stats = anime_stats()
        watched_anime = stats["watched"]
        number_of_pages = math.ceil(watched_anime / 35)

        watched_list = {
            "Anime" : [
                {"title" : "sample_title", "rating" : 5.0, "episodes" : 12},
            ]
        }

        for i in range (number_of_pages):
            page_url = f"https://www.anime-planet.com/users/{username}/anime/watched?sort=title&page={i+1}"
            dr = webdriver.Chrome()
            dr.get(page_url)
            source = BeautifulSoup(dr.page_source, 'html.parser')
            titles = source.find_all('h3', class_="cardName")
            episodes = re.findall(r"\w+-\w+-\w+=\"\d+\"",str(source.find_all('li',class_="card")))
            rating = source.find_all('div', class_="ttRating")
            counter = 0

            for title in titles:
                name = str(str(title).split('>')[1]).split('<')[0]
                episode = str(episodes[counter].split('"')[1])
                rate = str(str(rating[counter]).split('>')[1]).split('<')[0]
                data = [{"title" : str(name), "rating" : float(rate), "episodes" : int(episode)}]
                watched_list["Anime"].extend(data)
                counter += 1
        watched_list["Anime"].pop(0)
        return watched_list
    except AttributeError:
        sys.exit("Error!")

def watching_list():
    try:
        stats = anime_stats()
        watching_anime = stats["watching"]
        number_of_pages = math.ceil(watching_anime / 35)
        
        watching_list = {
            "Anime" : [
                {"title" : "sample_title", "rating" : 5.0, "episodes" : 12},
            ]
        }
        for i in range (number_of_pages):
            page_url = f"https://www.anime-planet.com/users/{username}/anime/watching?sort=title&page={i+1}"
            dr = webdriver.Chrome()
            dr.get(page_url)
            source = BeautifulSoup(dr.page_source, 'html.parser')
            titles = source.find_all('h3', class_="cardName")
            rating = source.find_all('div', class_="ttRating")
            episodes = re.findall(r"\w+-\w+-\w+=\"\d+\"",str(source.find_all('li',class_="card")))
            watched_episodes = re.findall(r"<\/span> \d+ eps", str(source))
            counter = 0

            for title in titles:
                name = str(str(title).split('>')[1]).split('<')[0]
                rate = str(str(rating[counter]).split('>')[1]).split('<')[0]
                episode = str(episodes[counter].split('"')[1])
                num_watched_episodes = watched_episodes[counter].split(' ')[1]
                
                data = [{"title" : str(name), "rating" : float(rate), "episodes" : int(episode), "watched episodes" : int(num_watched_episodes)}]
                watching_list["Anime"].extend(data)
                counter += 1
        watching_list["Anime"].pop(0)
        return watching_list
    except AttributeError:
        sys.exit("Error!")

def want_to_watch_list():
    try:
        stats = anime_stats()
        watched_anime = stats["want to watch"]
        number_of_pages = math.ceil(watched_anime / 35)

        wanttowatch_list = {
            "Anime" : [
                {"title" : "sample_title"},
            ]
        }

        for i in range (number_of_pages):
            page_url = f"https://www.anime-planet.com/users/{username}/anime/wanttowatch?sort=title&page={i+1}"
            dr = webdriver.Chrome()
            dr.get(page_url)
            source = BeautifulSoup(dr.page_source, 'html.parser')
            titles = source.find_all('h3', class_="cardName")

            for title in titles:
                name = str(str(title).split('>')[1]).split('<')[0]
                data = [{"title" : str(name)}]
                wanttowatch_list["Anime"].extend(data)
        wanttowatch_list["Anime"].pop(0)
        return wanttowatch_list
    except AttributeError:
        sys.exit("Error!")

def stalled_list():
    try:
        stats = anime_stats()
        watching_anime = stats["stalled"]
        number_of_pages = math.ceil(watching_anime / 35)
        
        stalled_list = {
            "Anime" : [
                {"title" : "sample_title", "rating" : 5.0, "episodes" : 12},
            ]
        }
        for i in range (number_of_pages):
            page_url = f"https://www.anime-planet.com/users/{username}/anime/stalled?sort=title&page={i+1}"
            dr = webdriver.Chrome()
            dr.get(page_url)
            source = BeautifulSoup(dr.page_source, 'html.parser')
            titles = source.find_all('h3', class_="cardName")
            rating = source.find_all('div', class_="ttRating")
            episodes = re.findall(r"\w+-\w+-\w+=\"\d+\"",str(source.find_all('li',class_="card")))
            watched_episodes = re.findall(r"<\/span> \d+ eps", str(source))
            counter = 0

            for title in titles:
                name = str(str(title).split('>')[1]).split('<')[0]
                rate = str(str(rating[counter]).split('>')[1]).split('<')[0]
                episode = str(episodes[counter].split('"')[1])
                num_watched_episodes = watched_episodes[counter].split(' ')[1]
                
                data = [{"title" : str(name), "rating" : float(rate), "episodes" : int(episode), "watched episodes" : int(num_watched_episodes)}]
                stalled_list["Anime"].extend(data)
                counter += 1
        stalled_list["Anime"].pop(0)
        return stalled_list
    except AttributeError:
        sys.exit("Error!")

def dropped_list():
    try:
        stats = anime_stats()
        watching_anime = stats["dropped"]
        number_of_pages = math.ceil(watching_anime / 35)
        
        dropped_list = {
            "Anime" : [
                {"title" : "sample_title", "rating" : 5.0, "episodes" : 12},
            ]
        }
        for i in range (number_of_pages):
            page_url = f"https://www.anime-planet.com/users/{username}/anime/dropped?sort=title&page={i+1}"
            dr = webdriver.Chrome()
            dr.get(page_url)
            source = BeautifulSoup(dr.page_source, 'html.parser')
            titles = source.find_all('h3', class_="cardName")
            rating = source.find_all('div', class_="ttRating")
            episodes = re.findall(r"\w+-\w+-\w+=\"\d+\"",str(source.find_all('li',class_="card")))
            watched_episodes = re.findall(r"<\/span> \d+ eps", str(source))
            counter = 0

            for title in titles:
                name = str(str(title).split('>')[1]).split('<')[0]
                rate = str(str(rating[counter]).split('>')[1]).split('<')[0]
                episode = str(episodes[counter].split('"')[1])
                num_watched_episodes = watched_episodes[counter].split(' ')[1]
                
                data = [{"title" : str(name), "rating" : float(rate), "episodes" : int(episode), "watched episodes" : int(num_watched_episodes)}]
                dropped_list["Anime"].extend(data)
                counter += 1
        dropped_list["Anime"].pop(0)
        return dropped_list
    except AttributeError:
        sys.exit("Error!")

def wont_watch_list():
    try:
        stats = anime_stats()
        watched_anime = stats["won't watch"]
        number_of_pages = math.ceil(watched_anime / 35)

        wontwatch_list = {
            "Anime" : [
                {"title" : "sample_title"},
            ]
        }

        for i in range (number_of_pages):
            page_url = f"https://www.anime-planet.com/users/{username}/anime/wontwatch?sort=title&page={i+1}"
            dr = webdriver.Chrome()
            dr.get(page_url)
            source = BeautifulSoup(dr.page_source, 'html.parser')
            titles = source.find_all('h3', class_="cardName")

            for title in titles:
                name = str(str(title).split('>')[1]).split('<')[0]
                data = [{"title" : str(name)}]
                wontwatch_list["Anime"].extend(data)
        wontwatch_list["Anime"].pop(0)

        return wontwatch_list
    except AttributeError:
        sys.exit("Error!")

def full_info():
    try:
        full_info = {
            "stats" : [],
            "watched" : [],
            "watching" : [],
            "want to watch" : [],
            "stalled" : [],
            "dropped" : [],
            "won't watch" : [],
        }
        stats = anime_stats()
        watched = watched_list()
        watching = watching_list()
        want_to_watch = want_to_watch_list()
        stalled = stalled_list()
        dropped = dropped_list()
        wont_watch = wont_watch_list()

        full_info['stats'].extend([stats])
        full_info['watched'].extend(watched['Anime'])
        full_info['watching'].extend(watching['Anime'])
        full_info['want to watch'].extend(want_to_watch['Anime'])
        full_info['stalled'].extend(stalled['Anime'])
        full_info['dropped'].extend(dropped['Anime'])
        full_info['won\'t watch'].extend(wont_watch['Anime'])

        return full_info
    except AttributeError:
        sys.exit("Error!")
