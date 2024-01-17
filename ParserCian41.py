import requests
from bs4 import BeautifulSoup
import telebot
import time

start_time = time.time()

token = '6814755359:AAFya7IubI7uVRY3wvPz33rhkfKlDXJfY3o'
bot = telebot.TeleBot(token)


def get_links_pages(url):     # Создает список из ссылок на объявления из страницы выдачи поиска и возвращет его значение функции
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    all = bs.find_all("a", "_93444fe79c--link--eoxce")

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


def get_text_opis(url):       # Ищет на странице объявления поле с текстом описания и возвращает этот текс функции
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    all_links = bs.find_all("span", "a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__pre-wrap--fXAax")
    
    return(all_links)


def main(url, words1, words2, words3, loc):
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    all_pages = bs.find_all('a', '_93444fe79c--list-itemLink--BU9w6')

    links = get_links_pages(url) # Получаем ссылки на объявления в первой страницы в выдаче
    i=2
    while i:              # Получаем ссылки на объявления во всех остальных страницах в выдаче
        a = str(i)
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
    text = f"Фразы - {words1} {words2} {words3} в локации {loc} встречается в следующих объявлениях:\n"
    file1.write(text)

    words = [words1, words2, words3]
    i = 1
    for x in spisok:
        if i%10==0:
            print(i)
        i += 1
        for y in get_text_opis(x):
            for w in range(0, 3):
                if words[w]:
                    if words[w] in y.text or words[w].capitalize() in y.text or words[w].upper() in y.text:
                        file1.write(x)
                        result.append(x)
                        break
    text = (f'Всего  {len(result)} объявлений по л')
    file1.write(text)
    file1.close
    file.close
    print(f"В локации {loc} в этих объявлениях есть искомые фразы {words1} {words2} {words3}:", result)
    print(f"Всего {len(result)} шт")
    text_bot = f"Фразы - {words1} {words2} {words3} в локации {loc} встречается {len(result)} раз в следующих объявлениях:"

    bot.send_message('357505388', text_bot)
    #for x in result:
    #    bot.send_message('357505388', x)
    all_time = time.time() - start_time
    print(f"Парсинг длился {round(all_time,1)} секунд или {round(all_time / 60,1)} минут")