import requests
from bs4 import BeautifulSoup
import telebot
import time

start_time = time.time()

token = '6814755359:AAFya7IubI7uVRY3wvPz33rhkfKlDXJfY3o'
bot = telebot.TeleBot(token)


#url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&in_polygon%5B1%5D=30.2236109_60.0527918%2C30.2133112_60.051073%2C30.2006082_60.049526%2C30.1841288_60.0471196%2C30.1738291_60.04351%2C30.1717691_60.0383534%2C30.1772623_60.0337125%2C30.1817255_60.0287278%2C30.1851587_60.0247745%2C30.1872187_60.0203054%2C30.1879053_60.0158364%2C30.1882486_60.0113674%2C30.1861887_60.0068983%2C30.1820688_60.0027731%2C30.1810389_59.9986478%2C30.1820688_59.993835%2C30.1844721_59.9897098%2C30.185502_59.9855845%2C30.1923685_59.9831781%2C30.2016382_59.9821468%2C30.2109079_59.981803%2C30.2212076_59.9816311%2C30.2304773_59.9816311%2C30.239747_59.9816311%2C30.2490168_59.9814592%2C30.2579431_59.9807717%2C30.2672129_59.9800842%2C30.2768259_59.9799123%2C30.285409_59.9799123%2C30.2936487_59.980256%2C30.3005152_59.9826624%2C30.3039484_59.9864439%2C30.306695_59.9903973%2C30.3063517_59.9946944%2C30.3063517_59.9995072%2C30.3063517_60.0038044%2C30.3029184_60.0075859%2C30.2984552_60.0122268%2C30.293992_60.0165239%2C30.2864389_60.0192741%2C30.2785425_60.0208211%2C30.272706_60.0237431%2C30.2692728_60.0275246%2C30.2648096_60.031478%2C30.2624063_60.0362908%2C30.2606897_60.0409317%2C30.2555399_60.0441976%2C30.2469568_60.0469477%2C30.2376871_60.0481509%2C30.2236109_60.0527918&max_house_year=2022&min_house_year=1960&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&room2=1&sort=price_object_order'
#url = argv[0]
#words1 = argv[1]
#ords2 = argv[2]
#words3 = argv[3]




def get_links(all):
    i = 0
    spisok = [1]
    for link in all:
        a = link["href"] + f'\n'
        if i == 0:
            spisok[i] = a
            i += 1
        elif a != spisok[i-1]:
            spisok.append(a)
            i += 1
    return(spisok)

def get_links_pages(url):
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    all_links = bs.find_all("a", "_93444fe79c--link--eoxce")
    
    return(get_links(all_links))


def get_words(url):
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    all_links = bs.find_all("span", "a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__pre-wrap--fXAax")
    
    return(all_links)


def main(url, words1, words2, words3):
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    all_pages = bs.find_all('a', '_93444fe79c--list-itemLink--BU9w6')

    links = get_links_pages(url) # Получаем ссылки на объявления в первой страницы в выдаче
    i=2
    while i:              # Получаем ссылки на объявления во всех остальных страницах в выдаче
        a = str(i)
        print(type(i))
        url_any = url + '&p=' + a
        print(url_any)
        pages = get_links_pages(url_any)
        if pages[0] == links[0]:  # Если закончились страницы в выдаче, будет выдаваться первая страница, значит заканчиваем цикл
            break
        links.extend(get_links_pages(url_any))
        i += 1

    file = open('links.txt', 'w+')
    file.writelines(links)
    file.close
    print("Операция выполнена! В файл links.txt добавлено", len(links), "ссылок на объявления")

    file = open('links.txt', 'r')
    spisok = file.readlines()
    file1 = open('words.txt', 'w+')

    result = []
    text = "Фразы - " + words1 + words2 + words3 + " встречается в следующих объявлениях:" + f"\n"
    file1.write(text)

    words = [words1, words2, words3]
    i = 1
    for x in spisok:
        print(i)
        i += 1
        for y in get_words(x):
            for w in range(0, 3):
                if words[w]:
                    if words[w] in y.text or words[w].capitalize() in y.text or words[w].upper() in y.text:
                        file1.write(x)
                        result.append(x)
                        break
    text = (f'Всего  {len(result)} объявлений')
    file1.write(text)
    file1.close
    file.close
    print("В этих объявлениях есть искомая фраза:", result)
    print(len(result))
    text_bot = f"Фразы - {words1} {words2} {words3} встречается {len(result)} раз в следующих объявлениях:"

    bot.send_message('357505388', text_bot)
    #for x in result:
    #    bot.send_message('357505388', x)
    all_time = time.time() - start_time
    print(f"Парсинг длился {round(all_time,1)} секунд или {round(all_time / 60,1)} минут")