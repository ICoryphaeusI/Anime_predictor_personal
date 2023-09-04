import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from time import sleep


class Shikimori:
    
    def __init__(self):
        pass

    #Получет суп для ссылки
    def get_soup(self, url):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers = headers)
        sleep(3)
        soup = BeautifulSoup(response.text, 'html')

        return soup
    
    #Поиск ссылки на страницу аниме
    def find_anime_url(self, soup):
        name_link = soup.find('div', class_='menu-slide-outer x199').find('article').find('a').get('href')

        return name_link

    #Поиск всех ссылок на страницы аниме
    #На каждой страницы 10 элементов, для получения данныъ со всех аниме необходимо сделать цикл для страничного парсера 
    def find_all_anime_links(self, soup):
        data_of_10 = [] #Пустой список, который в последствии будет заполнен 10-ю элементами
        titles = soup.findAll('article') #переменная с "soup" информация о всех элементах на странице, в которой находяться ссылки на страницы элементов
        for title in titles:
            name_link = title.find('a').get('href')
            data_of_10.append(name_link)
        
        return data_of_10

    #Переход на страницу аниме
    def go_to_link(self, link):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response_second = requests.get(link, headers=headers)
        soup_second = BeautifulSoup(response_second.text, 'lxml')

        return soup_second
    
    #Ищет название тайтла на русском языке
    def find_anime_name(self, soup):
        anime_name = soup.find('header', class_='head').text
        anime_name = anime_name.split("/")[0]

        return anime_name[:-1]
    
    #Ищет все характеристики тайтла, преобразовывая их в список вида "soup"
    def find_all_characteristics(self, soup):
        characteristics_data = []
        all_characteristics = soup.findAll('div', class_='line-container')
        for i in all_characteristics:
            characteristics_data.append(i)

        return characteristics_data
    
    #Ищет тип тайтла
    def find_type(self, data):
        for i in data:
            if 'Тип' in str(i):
                i = i.text
                i = i.split(':')[1]
                i = i[1: -2:]
                return i
            else:
                pass
    
    #Ищет кол-во эпизодов
    def episode_count(self, data):
        for i in data:
            if 'Эпизоды' in str(i):
                i = i.text
                i = i.split(':')[1]
                i = i[1: -2:]

                return i

            else:
                pass

    #Ищет дату выходу следуещего эпизода, если статус - онгоинг
    def next_episode(self, data, soup):
        for i in data:
            if 'Следующий эпизод' in str(i):
                date = soup.find('span', class_='local-time').get('data-datetime')
                date = datetime.fromisoformat(date)
                
                return str(date.date())
            
            else:
                pass
    
    #Ищет статус "онгоинг" или "вышел" у выбранного тайтла
    def status(self, data):
        for i in data:
            if 'Статус' in (str(i)):
                russian_words = re.findall('[а-яА-Я]+', str(i))
                
                return russian_words[1]
            else:
                pass

    #Ищет год издания тайтла
    def year(self, data):
        for i in data:
            if 'Статус' in (str(i)):
                digits_only = re.sub(r'\D+', ' ', str(i))
                digits_only = digits_only.split()
                for i in digits_only:
                    if len(i) != 4:
                        digits_only.remove(i)
                return digits_only[0]
            else:
                pass
    
    #Ищет жанры у выбранного тайтла
    def genres(self, data):
        for i in data:
            if 'Жанры' in str(i):
                i = i.text
                i = re.sub('[^а-яА-Я]', '', i)
                words = [word for word in re.findall('[А-Я][а-я]*', i)]
                
                return words[1:]

            else:
                pass

    #Выводит возрастное ограничение для просмотр тайтла
    def age_limit(self, data):
        for i in data:
            if 'Рейтинг' in str(i):
                i = i.text
                i = i.replace(' ', '')
                i = i.split(':')[1]
                
                return i

            else:
                pass
    
    #Выводит рейтенг тайтла по 10.0 бальной шкале
    def rate(self, soup):
        score = soup.find('div', class_='text-score').text
        digits_only = re.sub(r'\D', '', score)
        digits_only = digits_only[:1] + '.' + digits_only[1:]

        return digits_only
    
    #Выводит студию-издателя тайтла
    def studio(self, soup):
        string = soup.find('div', class_='c-info-right')
        string = str(string)
        start = string.index('Аниме студии')
        result = string[start:]
        new_result = result.split('">')[0]
        new_result = new_result[13:]
        
        return new_result

    #Выводит список из строк, хронящие в себе ссылки и кол-во: комментариев, отзывов и рецензий. Обязательно для выполнения для поиск информации по: комментариям, отзывам и рецензиям
    def addinion_links(self, soup):
        links = soup.find('div', class_='additional-links').find('div', class_='line-container')
        links = str(links)
        links_list = links.split('/span')

        return links_list
    
    #Выводит кол-во комментариев у тайтла, необходимо дать данные, полчученные из команды "addinion_links"
    def comment_count(self, data):
        for i in data:
            if 'комментар' in i:
                i = i[-25:]
                numbers = re.findall('\d+', i)

                return numbers
            
            else:
                pass
    
    #Выводит кол-во отзывов у тайтла, необходимо дать данные, полчученные из команды "addinion_links"
    def review_count(self, data):
        for i in data:
            if 'отзыв' in i:
                i = i[-15:]
                numbers = re.findall('\d+', i)

                return numbers
            
            else:
                pass

    #Выводит кол-во рецензий у тайтла, необходимо дать данные, полчученные из команды "addinion_links"
    def critiques_count(self, data):
        for i in data:
            if 'реценз' in i:
                i = i[-15:]
                numbers = re.findall('\d+', i)

                return numbers
            
            else:
                pass

    #Создает список, состоящих из ссылок, который будет использовать для перехода на страницы с коментариями, отзовами и рецензиями тайтла
    def get_title_links(self, soup):
        some_links = soup.find('div', class_='additional-links')
        some_linkss = some_links.find_all('span', {'class': 'linkeable'})
        links_data = []
        for i in some_linkss:
            links_data.append(i['data-href'])
        
        return links_data
    
    #Выводит ссылку на страницу со всеми комментариями к тайтлу, необходимо дать данные, полчученные из команды "get_title_links"
    def comments_link(self, data):
        for i in data:
            if 'obsuzhdenie' in i:
                
                return i
            
            else:
                pass

    #Выводит ссылку на страницу со всеми обзорами к тайтлу, необходимо дать данные, полчученные из команды "get_title_links"
    def reviews_link(self, data):
        for i in data:
            if 'reviews' in i:
                
                return i
            
            else:
                pass

    #Выводит ссылку на страницу со всеми рецезиями к тайтлу, необходимо дать данные, полчученные из команды "get_title_links"
    def critiques_link(self, data):
        for i in data:
            if 'critiques' in i:
                
                return i
            
            else:
                pass
    
    #Выводит ссылку на coub-ы с этим аниме, необходима вставить ссылку на страницу самого тайтла
    def coub(self, link):
        coub_link = str(link) + '/coub'

        return coub_link
    
    #Выводит ссылку на косплеями с этим аниме, необходима вставить ссылку на страницу самого тайтла
    def cosplay(self, link):
        cosplay_link = link + '/cosplay'

        return cosplay_link
    
    #Выводит автора тайтла, необходимо вставить ссылку тайтла
    def author(self, link):
        res_link = link + '/resources'
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                }
        response_third = requests.get(res_link, headers=headers)
        soupp = BeautifulSoup(response_third.text, 'lxml')
        auth = soupp.find('div', class_='c-column c-authors block_m').find_all('div', class_='b-db_entry-variant-list_item')
        string = str(auth[0])
        string = string.split('data-url')[1]
        string = string.split('><div class')[0]
        string = string[2:-1]
        response = requests.get(string, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find('header', class_='head').find('meta').get('content')
        
        return name
    
    #Выводит ссылку на автора оригинала, необходимо вставить ссылку тайтла
    def author_link(self, link):
        res_link = link + '/resources'
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                }
        response_third = requests.get(res_link, headers=headers)
        soupp = BeautifulSoup(response_third.text, 'lxml')
        auth = soupp.find('div', class_='c-column c-authors block_m').find_all('div', class_='b-db_entry-variant-list_item')
        string = str(auth[0])
        string = string.split('data-url')[1]
        string = string.split('><div class')[0]
        string = string[2:-1]

        return string



'''
if __name__ == "__main__":
    from time import sleep
    data = []
    for p in range(1, 1018):
        print(p)
        soup = shiki.get_soup(f'https://shikimori.me/animes/page/{p}')
        sleep(3)
        all_anime_links = shiki.find_all_anime_links(soup)
        for title in all_anime_links:
            try:
                some_soup = shiki.go_to_link(title)
            except:
                pass
            try:
                anime_name = shiki.find_anime_name(some_soup)#Название
            except:
                anime_name = None
            try:
                all_characteristics = shiki.find_all_characteristics(some_soup)
            except:
                pass
            try:
                anime_type = shiki.find_type(all_characteristics)#Тип
            except:
                anime_type = None
            try:
                episodes = shiki.episode_count(all_characteristics)#Эпизоды кол-во
            except:
                episodes = None
            try:
                next_episode = shiki.next_episode(all_characteristics, some_soup)#Когда след эпизод
            except:
                next_episode = None
            try:
                status = shiki.status(all_characteristics)#Статус тайтла
            except:
                status = None
            try:
                year = shiki.year(all_characteristics)
            except:
                year = None
            try:
                genres = shiki.genres(all_characteristics)#Жанры
            except:
                genres = None
            try:
                age_limit = shiki.age_limit(all_characteristics)#Возростное ограничение
            except:
                age_limit = None
            try:
                rate = shiki.rate(some_soup)#Рейтинг
            except:
                rate = None
            try:
                studio = shiki.studio(some_soup)#Студия
            except:
                studio = None
            try:
                addition_links = shiki.addinion_links(some_soup)
            except:
                add_links = None
            try:
                comments_count = shiki.comment_count(addition_links)#Кол-во комментариев
            except:
                comments_count = None
            try:
                review_count = shiki.review_count(addition_links)#Кол-во отзывов
            except:
                review_count = None
            try:
                critiques_count = shiki.critiques_count(addition_links)#Кол-во рецензий
            except:
                critiques_link = None
            try:
                title_links = shiki.get_title_links(some_soup)
            except:
                title_links = None
            try:
                comments_link = shiki.comments_link(title_links)#Ссылка на комментарии
            except:
                comments_link = None
            try:
                review_link = shiki.reviews_link(title_links)
            except:
                review_link = None
            try:
                critiques_link = shiki.critiques_link(title_links)#Ссылка на рецензии
            except:
                critiques_link = None
            try:
                coub = shiki.coub(title)#Ссылка на коубы
            except:
                coub = None
            try:
                cosplay = shiki.cosplay(title)#Ссылка на косплей
            except:
                cosplay = None
            try:
                author = shiki.author(title)#Автор оригинала
            except:
                author = None
            try:
                author_link = shiki.author_link(title)
            except:
                author_link = None

            data.append([anime_name, year, anime_type, episodes, status, next_episode, genres, age_limit, rate, studio, author, author_link, title, comments_count, comments_link, review_count, review_link, critiques_count, critiques_link, coub, cosplay])
'''