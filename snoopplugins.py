#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>
"""Плагины Snoop Project/Черновик"""

import click
import csv
import ipaddress
import itertools
import json
import locale
import os
import platform
import re
import random
import requests
import shutil
import socket
import sys
import threading
import time
import webbrowser

from collections import Counter
from colorama import Fore, Style, init
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from rich.console import Console
from rich.progress import track, BarColumn, TimeRemainingColumn, SpinnerColumn, TimeElapsedColumn, Progress
from rich.table import Table
from rich.panel import Panel
from rich.style import Style as STL
from urllib.parse import urlparse

import snoopbanner


locale.setlocale(locale.LC_ALL, '')
init(autoreset=True)
console = Console()
time_date = time.localtime()
head0 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
         f'Chrome/{random.choice(range(97, 108, 1))}.0.{random.choice(range(2007, 3008, 23))}.100 Safari/537.36'}


def ravno():
    console.rule(characters='=', style="cyan bold")


def helpend():
    console.rule("[bold red]Конец справки")


wZ1bad = []  #отфильтрованные ip (не ip) или отфильтрованные данные Yandex, отфильтрованные 'геокоординаты'
azS = []  #список результатов future request
coord = []  #координаты многоцелевой список


class ElapsedFuturesSession(FuturesSession):
    def request(self, method, url, *args, **kwargs):
        return super(ElapsedFuturesSession, self).request(method, url, *args, **kwargs)


my_session = requests.Session()
da = requests.adapters.HTTPAdapter(max_retries=3)
my_session.mount('https://', da)


dirresults = os.getcwd()
sessionY = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=10), session=my_session)
progressYa = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)


def Erf(hvostfile):
    print(f"\033[31;1mНе могу найти_прочитать файл: '{hvostfile}'.\033[0m \033[36m\n " + \
          f"\nПожалуйста, укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n" + \
          f"\033[36mПо умолчанию, например, блокнот в OS Windows сохраняет текст в кодировке — ANSI.\033[0m\n" + \
          f"\033[36mОткройте ваш файл '{hvostfile}' и измените кодировку [файл ---> сохранить как ---> utf-8].\n" + \
          f"\033[36mИли удалите из файла нечитаемые спецсимволы.")
    ravno()


## Модуль Yandex_parser.
# api https://yandex.ru/dev/id/doc/dg/reference/response.html#response__norights_5
def module3():
    while True:
        listlogin = []
        dicYa = {}

# Парсинг.
        def parsingYa():
            for login in listlogin:
                urlYa = f'https://yandex.ru/collections/api/users/{login}/'
                #urlYa = f'https://yandex.ru/znatoki/api/user/public/{login}/'
                try:
                    r = sessionY.get(urlYa, headers=head0, timeout=3)
                    azS.append(r)
                except Exception:
                    print(Fore.RED + "\nОшибка" + Style.RESET_ALL)
                    if Ya != '4':
                        ravno()
                    continue

            with progressYa:
                if Ya == '4':
                    task = progressYa.add_task("", total=len(listlogin))

                for reqY, login in zip(azS, listlogin):
                    if Ya == '4':
                        progressYa.update(task, advance=1, refresh=True)
                    try:
                        rY = reqY.result()
                    except Exception:
                        print(f"\n{Fore.RED}Ошибка сети пропуск —> '{Style.RESET_ALL}{Style.BRIGHT}" + \
                              f"{Fore.RED}{login}{Style.RESET_ALL}{Fore.RED}'{Style.RESET_ALL}")
                        continue
                    #print(rY.text)
                    try:
                        rdict = json.loads(rY.text)
                        if rdict.get('title') == "404 Not Found":  #равно
                            raise Exception("")
                    except Exception:
                        rdict = {}
                        rdict.update(public_id="Увы", display_name="-No-")

                    login_tab = login.split(sep='@', maxsplit=1)[0]
                    pub = rdict.get("public_id")
                    name = rdict.get("display_name")
                    email = f"{login_tab}@yandex.ru"
                    avatar = rdict.get("default_avatar_id")

                    if rdict.get("display_name") == "-No-":
                        if Ya != '4':
                            print(Style.BRIGHT + Fore.RED + "\nНе сработало")
                            console.rule(characters="=", style="cyan bold\n")
                        else:
                            continue
                        continue
                    else:
                        table1 = Table(title=f"\n{Style.DIM}{Fore.CYAN}demo_func{Style.RESET_ALL}", style="green")
                        table1.add_column("Имя", style="magenta", overflow="fold")
                        table1.add_column("Логин", style="cyan", overflow="fold")
                        table1.add_column("E-mail", style="cyan", overflow="fold")
                        if Ya == '3':
                            table1.add_row(name, "Пропуск", "Пропуск")
                        else:
                            table1.add_row(name, login_tab, email)
                        console.print(table1)

                        otzyv = f"https://reviews.yandex.ru/user/{pub}"
                        market = f"https://market.yandex.ru/user/{pub}/reviews"

                        if Ya == '3':
                            music = f"\033[33;1mПропуск\033[0m"
                        else:
                            music = f"https://music.yandex.ru/users/{login}/tracks"
                        dzen = f"https://zen.yandex.ru/user/{pub}"
                        qu = f"https://yandex.ru/q/profile/{pub}/"
                        avatar_html = f"https://avatars.mds.yandex.net/get-yapic/{avatar}/islands-retina-50"
                        avatar_cli = f"https://avatars.mds.yandex.net/get-yapic/{avatar}/islands-300"

                        print("\033[32;1mЯ.Отзывы:\033[0m", otzyv)
                        print("\033[32;1mЯ.Маркет:\033[0m", market)
                        print("\033[32;1mЯ.Музыка:\033[0m", music)
                        print("\033[32;1mЯ.Дзен:\033[0m", dzen)
                        print("\033[32;1mЯ.Кью:\033[0m", qu)
                        print("\033[32;1mЯ.Avatar:\033[0m", avatar_cli)

                        yalist = [avatar_html, otzyv, market, music, dzen, qu]

                    for webopen in yalist:
                        if webopen == music and Ya == '3':
                            continue
                        else:
                            if "arm" in platform.platform(aliased=True, terse=0) or "aarch64" in platform.platform(aliased=True, terse=0):
                                pass
                            else:
                                webbrowser.open(webopen)
            ravno()
            azS.clear()

        print("\n\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Указать логин пользователя\n" + \
              "[\033[0m\033[32;1m2\033[0m\033[36m] --> Указать публичную ссылку на Яндекс.Диск\n" + \
              "[\033[0m\033[32;1m3\033[0m\033[36m] --> Указать идентификатор пользователя\n" + \
              "[\033[0m\033[32;1m4\033[0m\033[36m] --> Указать файл с именами пользователей\n" + \
              "[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n" + \
              "[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n")

        Ya = console.input("[cyan]ввод --->  [/cyan]")

# Выход.
        if Ya == "q":
            print(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

# Help.
        elif Ya == "help":
            snoopbanner.help_yandex_parser()
            helpend()

# Указать login.
        elif Ya == '1':
            print("\033[36m└──Введите login/email разыскиваемого пользователя, например,\033[0m\033[32;1m bobbimonov\033[0m\n")
            login = console.input("[cyan]login/email --->  [/cyan]")
            login = login.split(sep='@', maxsplit=1)[0]
            listlogin.append(login)

            parsingYa()

# Указать ссылку на Я.Диск.
        elif Ya == '2':
            print("\033[36m└──Введите публичную ссылку на Яндекс.Диск, например,\033[0m\033[32;1m https://yadi.sk/d/7C6Z9q_Ds1wXkw\033[0m\n")
            urlYD = console.input("[cyan]url --->  [/cyan]")

            try:
                r2 = my_session.get(urlYD, headers=head0, timeout=3)
            except Exception:
                print(Fore.RED + "\nОшибка" + Style.RESET_ALL)
                console.rule(characters='=', style="cyan bold\n")
                continue
            try:
                login = r2.text.split('displayName":"')[1].split('"')[0]
            except Exception:
                login = "NoneStop"
                print(Style.BRIGHT + Fore.RED + "\nНе сработало")

            if login != "NoneStop":
                listlogin.append(login)
                parsingYa()

# Указать идентиффикатор Яндекс пользователя.
        elif Ya == '3':
            print("\033[36m└──Введите идентификатор пользователя Яндекс, например,\033[0m\033[32;1m tr6r2c8ea4tvdt3xmpy5atuwg0\033[0m\n")
            login = console.input("[cyan]hash --->  [/cyan]")
            listlogin.append(login)

            if len(login) != 26:
                print(Style.BRIGHT + Fore.RED + "└──Неверно указан идентификатор пользователя" + Style.RESET_ALL)
                ravno()
            else:
                parsingYa()

# Указать файл с логинами.
        elif Ya == '4':
            print("\033[31;1m└──В demo version этот метод плагина недоступен\033[0m\n")
            snoopbanner.donate()
        else:
            print(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
            ravno()


## Модуль Reverse Vgeocoder.
def module2():
    print(Style.BRIGHT + Fore.RED + "└──Плагин Reverse Vgeocoder 'сложен' и не поддерживается (по умолчанию) в Snoop_termux\n\nВыход\n" + Style.RESET_ALL)

## Модуль GEO_IP/domain.
def module1():
# Домен > IPv4/v6.
    def res46(dipp):
        try:
            res46 = socket.getaddrinfo(f"{dipp}", 443)
        except Exception:
            pass
        try:
            res4 = res46[0][4][0] if ipaddress.IPv4Address(res46[0][4][0]) else ""
        except Exception:
            res4 = "-"
        try:
            res6 = res46[-1][4][0] if ipaddress.IPv6Address(res46[-1][4][0]) else ""
        except Exception:
            res6 = "-"
        #print(res46)
        return res4, res6

# Запрос future request.
    def reqZ():
        try:
            r = req.result()
            return r.text
        except requests.exceptions.ConnectionError:
            print(Fore.RED + "\nОшибка соединения\n" + Style.RESET_ALL)
        except requests.exceptions.Timeout:
            print(Fore.RED + "\nОшибка таймаут\n" + Style.RESET_ALL)
        except requests.exceptions.RequestException:
            print(Fore.RED + "\nОшибка не идентифицирована\n" + Style.RESET_ALL)
        except requests.exceptions.HTTPError:
            print(Fore.RED + "\nОшибка HTTPS\n" + Style.RESET_ALL)
        return "Err"

# Выбор поиска одиночный или '-f'.
    ravno()
    print("\n\033[36mВведите домен (пример:\033[0m \033[32;1mexample.com\033[0m\033[36m), или IPv4/IPv6 (пример:\033[0m" + \
          "\033[32;1m8.8.8.8\033[0m\033[36m),\n" + \
          "или url (пример: \033[32;1mhttps://example.com/1/2/3/foo\033[0m\033[36m), \n" + \
          "или укажите файл с данными, выбрав ключ (пример:\033[0m \033[32;1m--file\033[0m\033[36m или\033[0m " +\
          "\033[32;1m-f\033[0m\033[36m)\n" + \
          "[\033[0m\033[32;1m-f\033[0m\033[36m] --> обработатка файла данных\n" + \
          "[\033[0m\033[32;1menter\033[0m\033[36m] --> информация о своем GEO_IP\n" + \
          "[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход")


    dip = console.input("\n[cyan]ввод --->  [/cyan]")

# выход.
    if dip == "q":
        print(Style.BRIGHT + Fore.RED + "Выход")
        sys.exit()

# проверка данных.
    elif dip == '--file' or dip == '-f':
        while True:
            print("""\033[36m├──Выберите тип поиска
│
[\033[0m\033[32;1m1\033[0m\033[36m] --> Online (медленно)
[\033[0m\033[32;1m2\033[0m\033[36m] --> Offline (быстро)
[\033[0m\033[32;1m3\033[0m\033[36m] --> Offline_тихий (очень быстро)
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[31;1mq\033[0m\033[36m] --> Выход\033[0m""")

            dipbaza = input('\n')

# Выход.
            if dipbaza == "q":
                print("\033[31;1mВыход\033[0m")
                sys.exit(0)
# Справка.
            elif dipbaza == "help":
                snoopbanner.geo_ip_domain()
                helpend()

# Оффлайн поиск.
# Открываем GeoCity.
            elif dipbaza == "2" or dipbaza == "3":
                while True:
                    print("\033[31;1m└──В demo version этот метод плагина недоступен\033[0m\n")
                    snoopbanner.donate()
                    break

                break

# Онлайн поиск.
            elif dipbaza == "1":
                print("\033[31;1m└──В demo version этот метод плагина недоступен\033[0m\n")
                snoopbanner.donate()
                break

# Неверный выбор ключа при оффлайн/онлайн поиске. Выход.
            else:
                print(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
                ravno()

# одиночный запрос.
    else:
        def ip_check(url_api, dip, res4, err):
            if dip == "": url_api = url_api
            elif res4 == "-": url_api = f"{url_api}{dip}"
            else: url_api = f"{url_api}{res4}"

            try:
                r = my_session.get(url=url_api, headers=head0, timeout=3)
                dip_dic = json.loads(r.text)
                T1 = dip_dic["country_code"] if err is False else dip_dic["country"]["isoCode"]
                T2 = dip_dic["region"] if err is False else dip_dic["city"]["name"]
                T3 = dip_dic["latitude"] if err is False else dip_dic["location"]["latitude"]
                T4 = dip_dic["longitude"] if err is False else dip_dic["location"]["longitude"]
                if err is True and res4 == '-':
                    T5 = my_session.get(url=f"https://ipinfo.io/ip", timeout=3).text
                else:
                    T5 = dip_dic.get("ip")
            except Exception:
                try:
                    if err is True:
                        if dip == '': p = ''
                        elif res4 != '-': p = res4 + '/'
                        else: dip + '/'
                        console.log("[bold yellow]--> Внимание! Последний доступный url_ip[/bold yellow]")
                        T1 = my_session.get(url=f"https://ipinfo.io/{p}country", timeout=3).text
                        T2 = my_session.get(url=f"https://ipinfo.io/{p}region", timeout=3).text
                        T5 = my_session.get(url=f"https://ipinfo.io/{p}ip", timeout=3).text

                        T3 = "stop"
                        T4 = "stop"
                        return T1, T2, T3, T4, T5
#                        raise Exception("")
                    return ip_check('https://ipdb.ipcalc.co/ipdata/', dip, res4, err=True)
                except:
                    T1 = "-"
                    T2 = "-"
                    T3 = "stop"
                    T4 = "stop"
                    T5 = "-"
                    print("""\033[31;1m\n
|\ | _ ._  _
| \|(_)| |(/_\033[0m""")

            return T1, T2, T3, T4, T5


        zagol = "Мой ip" if dip == "" else dip

        if '.' not in dip and ':' not in dip and dip != "" or (dip != "" and len(dip) <= 4):
            print(Style.BRIGHT + Fore.RED + "└──Неверный ввод \n\nвыход" + Style.RESET_ALL)
            sys.exit()
        else:
            u = urlparse(dip).hostname
            if bool(u) is False:
                dip = dip.split("/")[0].strip()
            else:
                dip = u.replace("www.", "").strip()

            domain = socket.getfqdn(dip)
            try:
                ipaddress.ip_address(dip)
                resD1 = domain
            except Exception:
                resD1 = dip

        with console.status("[cyan]работаю[/cyan]"):
            try: # IP/Домен > Домен и IPv4v6.
                res4, res6 = res46(resD1)
            except Exception:
                res4 = "-"

            T1, T2, T3, T4, T5 = ip_check('https://ipwho.is/', dip, res4, err=False)

            try:
                if ipaddress.IPv4Address(dip): res4 = dip
            except Exception: pass
            try:
                if ipaddress.IPv6Address(dip): res6 = dip
            except Exception: pass

            table = Table(title=zagol, title_style="italic bold red", style="green", header_style='green')
            table.add_column("Код", style="magenta")
            if dip == "":
                table.add_column("IP", style="cyan", overflow="fold")
            else:
                table.add_column("IPv4", style="cyan", overflow="fold")
                table.add_column("IPv6", style="cyan", overflow="fold")
            table.add_column("Домен", style="green", overflow="fold")
            table.add_column("Регион", style="green", overflow="fold")
            if dip == "":
                table.add_row(T1, T5, domain, T2)
            else:
                table.add_row(T1, res4, res6, domain, T2)
            console.print(table)
            if T3 == "stop" and T4 == "stop":
                print("\n")
                URL_GEO = ""
            else:
                URL_GEO = f"https://www.openstreetmap.org/#map=13/{T3}/{T4}"
                URL_GEO2 = f"https://www.google.com/maps/@{T3},{T4},12z"
                print(Style.BRIGHT + Fore.BLACK + f"{URL_GEO}" + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.BLACK + f"{URL_GEO2}\n" + Style.RESET_ALL)

        module1()


if __name__ == "__main__":
    module1()
