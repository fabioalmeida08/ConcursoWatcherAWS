from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp
import json
import boto3
import telebot
from mypy_boto3_ssm import SSMClient
from datetime import datetime
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def initialise_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    return driver

def lambda_handler(event, context):
    try:
        ssm: SSMClient = boto3.client("ssm")
        bot_token = ssm.get_parameter(Name="/Telegram/TokenBot", WithDecryption=True)["Parameter"]["Value"]
        chat_id = ssm.get_parameter(Name="/Telegram/MyChatID", WithDecryption=True)["Parameter"]["Value"]
        last_date = ssm.get_parameter(Name="/Concurso/LastUpdatedDate", WithDecryption=True)["Parameter"]["Value"]
        bot = telebot.TeleBot(bot_token)

        driver = initialise_driver()

        url = os.getenv("SITE_URL")
        driver.get(url)

        resultados = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
            (By.ID, "blocoPublicacoes")
            )
        )
        lista_atualização = resultados.find_element(By.TAG_NAME, "ul")
        elementos_lista = lista_atualização.find_elements(By.TAG_NAME, "li")

        eventos = []
        for li in elementos_lista:
            try:
                a_tag = li.find_element(By.TAG_NAME, "a")  
                link = a_tag.get_attribute("href") 
                date = li.find_element(By.TAG_NAME, "span")
                evento = {"titulo": li.text, "url": link, "data": date.text}
                eventos.append(evento)
            except Exception as e:
                logger.exception(e)
                print("Nenhum link encontrado nesse item.")

        last_event = max(eventos, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))
        logger.info(last_event)
        if datetime.strptime(last_event["data"], "%d/%m/%Y") > datetime.strptime(last_date, "%d/%m/%Y"):
            titulo = last_event["titulo"]
            url = last_event["url"]
            last_date = last_event["data"]
            bot.send_message(chat_id=chat_id,text=f"{titulo}\n {url}")
            ssm.put_parameter(
                Name="/Concurso/LastUpdatedDate",
                Value=last_date,
                Type="SecureString",  
                Overwrite=True 
            )

        driver.quit()

        return {
            "statusCode": 200
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "Error": "internal server error",
                }
            ),
        }
