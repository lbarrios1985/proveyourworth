#!/usr/bin/env python
# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup, Tag
from PIL import Image, ImageDraw
from pathlib import Path

"""
test proveyourworth/level3
"""
start_uri = "http://www.proveyourworth.net/level3/start"
activate_uri = "http://www.proveyourworth.net/level3/activate?statefulhash"
payload = "http://www.proveyourworth.net/level3/payload"
file_path = Path("./")

session1 = requests.Session()
session = requests.Session()
session.get(start_uri)
cookie = session.cookies.get("PHPSESSID")

def start_session(start_uri: str) -> None:
    print(f'Hash: {cookie}')


def get_hash(start_uri: str) -> str:
    request = session.get(start_uri)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup.find("input", {"name": "statefulhash"})['value']


def activate(activate_uri, get_hash: str) -> None:
    get_hash = get_hash(start_uri)
    session.get(activate_uri+f'={get_hash}')
    print(f"Hash: {get_hash}")


def get_image_to_sign(uri_image: str) -> bytes:
    request = session.get(uri_image, stream=True)
    image = request.raw
    return image


def sing_image(image: bytes) -> None:
    image = Image.open(image)
    draw = ImageDraw.Draw(image)
    draw.text((20, 70), f"Luis Barrios, \n Hash:{get_hash(start_uri)} \n nikeven@gmail.com \n Python Developer", fill=(
        1024, 1024, 0))
    image.save("image.jpg", "JPEG")


def post_back_to(payload: str) -> None:
    payload = session.get(payload)
    
    print("****************************")
    print(payload.headers)
    
    post_uri = f"{payload.headers['X-Post-Back-To']}"
    file = {
        "image": open(file_path / "image.jpg", "rb"),
        "code": open(file_path / "code.py", "rb"),
        "resume": open(file_path / "resume.pdf", "rb")
    }
    data = {
        "email": "nikeven@gmail.com",
        "name": "Luis Barrios",
        "aboutme": "Desarrollador Full stack,especializado en el Desarrollo de Aplicaciones Web, bajo diferentes lenguajes de programación (Python, Php, Javascript) y Frameworks (Django, Laravel, Nodejs, Vuejs). ",
        "code":"https://github.com/lbarrios1985/proveyourworth/code.py",
        "resume":"https://www.linkedin.com/in/luis-barrios-8b5505137/",
        "image":"https://github.com/lbarrios1985/proveyourworth/image.jpg"
    }
    
    cookie = session.cookies.get("PHPSESSID")
    one = requests.cookies.RequestsCookieJar()
    one.set("PHPSESSID", cookie)
    # print(one)
    one.update(session1.cookies)
    # print(session.cookies)
    # print(one)


    # session.cookies.set("PHPSESSID", cookie)
    
    request = session1.post(post_uri, data=data, files=file, cookies= one)
    print(request.status_code)
    print(request.text)

if __name__ == '__main__':
    print("-"*8 + "🚬🗿 start PHPSESSID" + "-"*8)
    start_session(start_uri)
    print("-"*8 + "🤘💀 hacking PHPSESSID" + "-"*8)
    print("-"*8 + "🇧🇴♋ activate PHPSESSID" + "-"*8)
    activate(activate_uri, get_hash)
    print("-"*8 + "🖖👽 activated payload" + "-"*8)
    sing_image(get_image_to_sign(payload))
    print("-"*8 + "status code:")
    post_back_to(payload)
