import requests
from bs4 import BeautifulSoup
import telebot
import time

start_time = time.time()

token = '6814755359:AAFya7IubI7uVRY3wvPz33rhkfKlDXJfY3o'
bot = telebot.TeleBot(token)


def get_bs(url):
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")
    all_links = bs.find_all("a", "_93444fe79c--link--eoxce")
    all_texts = bs.find_all("p", "_93444fe79c--color_black_100--Ephi7 _93444fe79c--lineHeight_20px--fX7_V _93444fe79c--fontWeight_normal--JEG_c _93444fe79c--fontSize_14px--reQMB _93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq")
    links_and_texts = [all_links, all_texts]
    return(links_and_texts)


def get_links_pages(all_links):     # Создает список из ссылок на объявления из страницы выдачи поиска и возвращет его значение функции     
    i = 0
    spisok = [1]
    for link in all_links:
        a = link["href"] + f'\n'
        if i == 0:
            spisok[i] = a
            i += 1
        elif a != spisok[i-1]:
            spisok.append(a)
            i += 1
    return(spisok)


def main(url, words1, words2, words3, loc, loc_num):
    print(f"Начался парсинг по локации {loc} объявлений с ключевыми словами {words1} {words2} {words3}")
    links_and_texts = get_bs(url)

    links = get_links_pages(links_and_texts[0]) # Получаем ссылки на объявления в первой страницы в выдаче
    texts = links_and_texts[1]                  # Получаем тексты объявлений на первой странице
    i=2
    while i:              # Получаем ссылки на объявления и тексты объявлений во всех остальных страницах в выдаче
        a = str(i)
        url_any = url + '&p=' + a
        #print(url_any[-3:])
        links_and_texts_other = get_bs(url_any)
        links_pages = get_links_pages(links_and_texts_other[0])
        texts_other = links_and_texts_other[1] 
        if links_pages[0] == links[0]:  # Если закончились страницы в выдаче, будет выдаваться первая страница, значит заканчиваем цикл
            break
        links.extend(links_pages)
        texts.extend(texts_other)
        i += 1

    file = open(f'links {loc}.txt', 'w+')
    file.writelines(links)
    file.close
    print(f"Операция выполнена! Из {i-1} страниц в файл links.txt добавлено {len(links)} ссылок на объявления и в них текстов {len(texts)}")

    #file = open('links.txt', 'r')
    #spisok = file.readlines()
    file1 = open(f'words {loc} {words1} {words2} {words3}.txt', 'w+')
    #file2 = open('texts.txt', 'w+')
    #file2.writelines(texts)
    result = []
    text = f"Фразы - {words1} {words2} {words3} в локации {loc} встречается в следующих объявлениях:\n"
    file1.write(text)

    words = [words1, words2, words3]
    y = len(links)
    for i in range(1, y):
        #if i%100==0:
        #    print(i)
        for w in range(0, 3):
            if words[w]:
                if words[w] in texts[i].text or words[w].capitalize() in texts[i].text or words[w].upper() in texts[i].text:
                    file1.write(links[i])
                    result.append(links[i])
                    break

    text = (f'Всего  {len(result)} объявлений')
    file1.write(text)
    file1.close
    #file2.close
    print(f"В локации {loc} в этих объявлениях есть искомые фразы {words1} {words2} {words3}:", result)
    print(f"Всего {len(result)} шт")
    text_bot = f"Фразы - {words1} {words2} {words3} в локации {loc} встречается {len(result)} раз в следующих объявлениях:"

    bot.send_message('357505388', text_bot)
    #for x in result:
    #    bot.send_message('357505388', x)
    all_time = time.time() - start_time
    print(f"Парсинг длился {round(all_time,1)} секунд или {round(all_time / 60,1)} минут")