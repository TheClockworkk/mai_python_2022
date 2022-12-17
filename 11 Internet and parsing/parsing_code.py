import requests # импортируем библиотеку. предварительно необходимо установить ее в python: pip install requests
from bs4 import BeautifulSoup, BeautifulStoneSoup # для парсинга веб-страниц понадобится библиотека BeautifulSoup. устанвока: pip install bs4
import lxml
import json
from pprint import pprint


# Пример 1 - Парсинг сайта. Запрос без авторизации. При неообходимости - с заголовком запроса (некоторые сайты защищаются от роботов-парсеров, поэтому приходится эмулировать браузер (у которого заполнен заголовок запроса)
url = r"https://www.s7.ru/ru/about/ourfleet.dot"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}

try:
	r = requests.get(url, headers=headers)
	# print(r.text)
	# при получении данных необходимо проверить, было ли оно успешным, через r.status_code
	print(r.status_code)  # отображаем код ответа HTTP. 200 - ОК, 404 - ресурс не найден, 500* - различные коды ошибок сервера. подробно:
	
	# другие полезные свойства объекта response:
	print(r.url)  # отображаем url источника, который нам вернулся. он может отличаться от исходного!
	print(r.headers)  # отображаем заголовок ответа сервера
	# содержимое страницы можно получить в виде текста либо в бинарном виде:
	# print(r.text)  # получаем обычный html-код страницы
	# print(r.content)  # получаем html-код страницы как двоичный объект

	# создаем парсер. в качестве параметра передаем название движка, который может парсить html-страницы - lxml
    # если у вас не установлен lxml: pip install lxml. этот параметр можно опустить. рабоать будет, но появится предупреждение
	bs = BeautifulSoup(r.text, "lxml")
	# после анализа кода страницы находим html-тег, внутри которого содержится нужная дла нас информация о воздушном флоте авиакомпании
	# find_all() находит все теги, find() берет только первый по списку и останавливает поиск
	# для уточнения поиска (т.к. тегов div очень много) используются атрибуты, сопровождающие этот тег
	# ("div", attrs={"class":"company-main-cont"}) соответствует коду html
	# ...........
	div_bs = bs.find_all("div", attrs={"class":"company-main-cont"})
	rows_bs = div_bs[0].findChildren("div", attrs={"class": "row"}, recursive=False)
	# print(len(rows_bs))
	# результат поиска - список объектов-тегов. работаем с ними как с обычным списком:
	for row in rows_bs:
			print(row.find("h3").text)
			cols_bs = row.find_all("div", attrs={"class": "col-md-11"})
			for col in cols_bs:
					print(col.text)
			print()
			# атрибуты - это словарь, поэтому значение атрибута получается аналогично
			# например, в строке ниже получаем ссылку на изображение самолета, которая находится в теге src
			img = row.find("img")["src"]
			# обратите внимание на параметр allow_redirects=True. некоторые html-страницы при запросе на один url
			# перенаправляют на другой url и именно по нему вы получаете нужные данные. True разрешает редиректы
			rfile = requests.get(url, allow_redirects=True)
			# сохраняем полученное изображение в файл. открываем его в режиме "запись+двоичный" wb, т.к.
			# изображение - это файл в двоичном формате
			open(row.find("h3").text + ".png", 'wb').write(rfile.content)
    # print(r.status_code)	
except Exception as e:
	print(e)


# Пример 2 Запрос к API без авторизации
# мы знаем url и все параметры. ключ или логин-пароль пользователя не нужны

# здесь и запрос, и данные для запроса передаются в одном url
# https://open-meteo.com/en/docs
# api.open-meteo.com - адрес ресурса, v1 - версия api, gem - метод API, который мы вызываем
# API использует Global Environmental Multiscale Model (GEM) from the Canadian weather service, отсюда и название
url = "https://api.open-meteo.com/v1/gem?latitude=35.678&longitude=139.682&hourly=temperature_2m,dewpoint_2m,windspeed_10m,winddirection_120m"

# подаем запрос через requests
# если идет только запрос, без пакета данных, подаем его через get
# try:
# 	r = requests.get(url)
# 	print(r.text)
# 	json_data = json.loads(r.text)
# 	print(type(json_data))
# except Exception as e:
# 	print(e)






# url = "http://stat.gibdd.ru/map/getDTPCardData"

# # некоторые интернет-источники требуют, чтобы вы передавали параметры запроса отдельно
# # в этом случае вы не можете задать параметры запроса в url и должны дополнительно передать данныые, как правило, в формате json
# # payload - фильтр данных для ресурса stat.gibdd.ru
# payload = {"data":"{\"date\":[\"MONTHS:1.2022\",\"MONTHS:2.2019\"],\"ParReg\":\"45\",\"order\":{\"type\":\"1\",\"fieldName\":\"dat\"},\"reg\":\"45268592\",\"ind\":\"1\",\"st\":\"1\",\"en\":\"16\"}"}

# payload2 = {"data":""}
# req_data = {"date":["MONTHS:1.2022"],"ParReg":"45",
#             "order":{"type":"1","fieldName":"dat"},"reg":"45268592","ind":"1","st":"1","en":"16"}
# req_data["en"] = str(100)
# print(req_data)

# # чтобы сформировать собственный json для запроса, используйте функцию json.dumps(), которая превращает словарь, содержащий ваши параметры, в строку
# # некоторые ресурсы (stat.gibdd.ru в их числе) требуют, чтобы данные были переданы в так называемой "компактной записи", т.е. не содержали ни одного лишнего пробела
# # к сожалению, json.loads автоматически вставляет пробелы. убирайте их функцией str.replace(" ", "")
# payload2["data"] = json.dumps(req_data).replace(" ", "")
# # payload2["data"] = json.dumps(req_data)
# print(f"payload2:\n{payload2}\npayload:\n{payload}")

# try:
#     # если вы передаете данные вместе с url запроса, используйте метод POST вместо GET
#     # в данном случае формат передаваемых данных будет json (а не, например, data, который вы используете для авторизации на сайте через форму логина-пароля)
#     r = requests.post(url, json=payload2)
#     print(r.status_code)
#     if r.status_code == 200:
#         # в ответ на ваш запрос сайт также возвращает данные в формате json. преобразуйте их в словарь методом json.loads()
#         json_data = json.loads(r.text)
#         print(f'Тип данных: {type(json_data)}, тип значения: {type(json_data["data"])}')
#         json_cards = json.loads(json_data["data"])
#         print(f'Тип данных: {type(json_cards)}, количество карточек: {len(json_cards["tab"])}')
# except Exception as e:
#     print(e)

