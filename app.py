from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send
import os
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent



def openChrome():
    driver.get('https://chat.openai.com/')

    driver.delete_all_cookies()

    # Ruta al archivo JSON
    archivo = 'cookies.json'

    # Leer el archivo JSON
    with open(archivo, 'r') as f:
        # Cargar el contenido del archivo como un objeto JSON
        data = json.load(f)

    # Mostrar los objetos JSON por consola
    for objeto in data:
        # print(objeto)
        driver.add_cookie(objeto)


    driver.get('https://chat.openai.com/')


    time.sleep(5)
    skip_popups()

    #Enviar Hola
    # time.sleep(1)
    # sendHola()


def getHTMLChat():
    element = driver.find_element(By.XPATH, "//div[@class='flex flex-col text-sm dark:bg-gray-800']")
    div_html = element.get_attribute('innerHTML')
    return(div_html)



def skip_popups():

    skip = driver.find_elements(By.TAG_NAME, "div")

    # for index, element in enumerate(skip):
    #     print(f"Elemento en posición {index}: {element}")

    # skip = driver.find_element_by_class_name("btn relative btn-neutral ml-auto")
    # driver.find_element_by_xpath("//div[contains(@class, 'first_name')]")
    # driver.find_element_by_class_name("first_name")
    # skip[1].click()

    # arrow = driver.find_element_by_xpath('//div[@class="btn relative btn-neutral ml-auto"]')

    arrow = driver.find_element(By.XPATH, "//button[@class='btn relative btn-neutral ml-auto']")
    arrow.click()
    time.sleep(1)

    arrow = driver.find_element(By.XPATH, "//button[@class='btn relative btn-neutral ml-auto']")
    arrow.click()
    time.sleep(1)

    arrow = driver.find_element(By.XPATH, "//button[@class='btn relative btn-primary ml-auto']")
    arrow.click()
    time.sleep(1)

    
    # skip=driver.find_elements(By.TAG_NAME,"div")
    # skip[45].click()
    # skip=driver.find_elements(By.TAG_NAME,"div")
    # try:
    #     skip[46].click()
    # except:
    #     skip[45].click()
    # skip=driver.find_elements(By.TAG_NAME,"div")
    # skip[51].click()

def newChat():
    element = driver.find_element(By.XPATH, "//a[@class='flex py-3 px-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer text-sm rounded-md border border-white/20 hover:bg-gray-500/10 mb-1 flex-shrink-0']")
    element.click()
    # div_html = element.get_attribute('innerHTML')

    # print(div_html)

    time.sleep(2)
    enviar_html()


def stopGenerating():
    element = driver.find_element(By.XPATH, "//button[@class='btn relative btn-neutral border-0 md:border']")
    
    div_html = element.get_attribute('innerHTML')
    patron = r"\bRegenerate response\b"
    
    if re.search(patron, div_html):
        # print("La cadena cumple con la expresión regular.")
        element.click()
        time.sleep(2)
        enviar_html()

        time.sleep(3)
        element = driver.find_element(By.XPATH, "//div[@class='h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center']")
        div_html = element.get_attribute('innerHTML')

        while re.search(r'\bStop generating\b', div_html):
            enviar_html()
            element = driver.find_element(By.XPATH, "//div[@class='h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center']")
            div_html = element.get_attribute('innerHTML')
            time.sleep(1)

    else:
        # print("La cadena no cumple con la expresión regular.")
        element.click()
        time.sleep(2)
        enviar_html()
    
    
    
    # div_html = element.get_attribute('innerHTML')

    # print(div_html)

    


def sendPrompt(prompt):
    element = driver.find_element(By.XPATH, "//textarea[@class='m-0 w-full resize-none border-0 bg-transparent p-0 pr-7 focus:ring-0 focus-visible:ring-0 dark:bg-transparent pl-2 md:pl-0']")
    element.send_keys(Keys.TAB);
    element.clear();

    # promptAux = prompt.replace("\n", "")
    # element.send_keys(promptAux);

    driver.execute_script("arguments[0].value = arguments[1];", element, prompt)

    time.sleep(1)
    element.send_keys(Keys.ENTER);

    enviar_html()

    time.sleep(3)
    element = driver.find_element(By.XPATH, "//div[@class='h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center']")
    div_html = element.get_attribute('innerHTML')

    while re.search(r'\bStop generating\b', div_html):
        enviar_html()
        element = driver.find_element(By.XPATH, "//div[@class='h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center']")
        div_html = element.get_attribute('innerHTML')
        time.sleep(1)

    

def sendHola():
    element = driver.find_element(By.XPATH, "//textarea[@class='m-0 w-full resize-none border-0 bg-transparent p-0 pr-7 focus:ring-0 focus-visible:ring-0 dark:bg-transparent pl-2 md:pl-0']")
    element.send_keys(Keys.TAB);
    element.clear();
    element.send_keys("Hola");
    time.sleep(1)
    element.send_keys(Keys.ENTER);




op = webdriver.ChromeOptions()
op.add_argument(f"user-agent={UserAgent.random}")
op.add_argument("user-data-dir=./")

op.add_experimental_option("detach", True)
op.add_experimental_option("excludeSwitches", ["enable-logging"])


driver = uc.Chrome(chrome_options=op)



app = Flask(__name__, static_folder='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/static/css/<path:filename>')
# def serve_css(filename):
#     # return app.send_static_file('/static/css/' + filename)
#     return send_from_directory('/static/css', filename)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    print(os.path.dirname(os.getcwd()))
    return send_from_directory('./templates/static/css', filename)

@app.route('/_next/image')
def serve_avatar():
    print(os.path.dirname(os.getcwd()))
    return send_from_directory('./templates/static/image', 'avatar.webp')

# @app.route('/css/<path:filename>')
# def serve_static(filename):
#     root_dir = os.path.dirname(os.getcwd())
#     print(os.path.join(root_dir, 'flask-socket.io-simple-chat', 'templates', 'static', 'css'))
#     return send_from_directory(os.path.join(root_dir, 'flask-socket.io-simple-chat', 'templates', 'static', 'css'), filename)


@socketio.on('message')
def handleMessage(msg):
    print('Desde evento Message: ' + msg)
    send(msg, broadcast = True)

@socketio.on('evento1')
def handleMessage(msg):
    print('Desde evento evento1: ' + msg)
    # send(msg, broadcast = True)

@socketio.on('evento2')
def handleMessage(msg):
    print('Desde evento evento2: ' + msg)
    # send(msg, broadcast = True)

@socketio.on('evento3')
def handleMessage():
    print('Desde evento evento3')
    openChrome()
    # send(msg, broadcast = True)

@socketio.on('evento4')
def handleMessage():
    print('Desde evento evento4')
    # getHTMLChat()
    # send(msg, broadcast = True)

@socketio.on('postPrompt')
def handleMessage(prompt):
    print('Desde evento postPrompt')
    print(prompt)
    sendPrompt(prompt)
    # getHTMLChat()
    # send(msg, broadcast = True)

@socketio.on('enviar_html')
def enviar_html():
    codigo_html = '<h1>Ejemplo de código HTML enviado desde el servidor</h1>'
    print('Desde evento enviar_html')
    
    with open('archivo.html', 'r', encoding='utf-8') as file:
        arch_codigo_html = file.read()

    socketio.emit('html_recibido', getHTMLChat())


@socketio.on('newChatPost')
def newChatPost():
    print('Desde evento newChatPost')
    newChat()


@socketio.on('stopGeneratingPost')
def stopGeneratingPost():
    print('Desde evento stopGeneratingPost')
    stopGenerating()


if __name__ == '__main__':
    socketio.run(app)


openChrome()


