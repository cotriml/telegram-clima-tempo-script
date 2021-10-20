# -*- coding: utf-8 -*-
import requests
from dotenv import dotenv_values

# Environment Variables
ENV = dotenv_values()

# Clima Tempo Variables
climaTempoToken = ENV.get('CLIMATEMPOTOKEN')
climaTempoLocaleId = ENV.get('CLIMATEMPOLOCALEID')
climaTempoHostName = ENV.get('CLIMATEMPOHOSTNAME')

# Telegram Variables
telegramToken = ENV.get('TELEGRAMTOKEN')
telegramChatId = ENV.get('TELEGRAMCHATID')
telegramHostName = ENV.get('TELEGRAMHOSTNAME')


def getCurrentWeather():
    climaTempoUrl = '{0}/api/v1/weather/locale/{1}/current?token={2}'.format(
        climaTempoHostName, climaTempoLocaleId, climaTempoToken)
    res = requests.get(climaTempoUrl)
    if res.status_code != 200:
        raise Exception('Error trying to get Current Weather on Clima Tempo')
    return res.json()


def getForecastWeather():
    climaTempoUrl = '{0}/api/v2/forecast/locale/{1}/days/15?token={2}'.format(
        climaTempoHostName, climaTempoLocaleId, climaTempoToken)
    res = requests.get(climaTempoUrl)
    if res.status_code != 200:
        raise Exception('Error trying to get Forecast Weather on Clima Tempo')
    return res.json()


def sendTelegramMessage(message):
    telegramUrl = "{0}/{1}/sendMessage?chat_id={2}&text={3}&parse_mode=html".format(
        telegramHostName, telegramToken, telegramChatId, message
    )
    res = requests.get(telegramUrl)
    if res.status_code != 200:
        raise Exception('Error trying to send Telegram message')
    return res.json()


def formatTelegramMessage(currentWeatherResponse, forecastWeatherResponse):
    textMessage = '☀️🌤⛅️🌥☁️🌦🌧⛈🌩🌨❄️\n{0}\n\n<b>Cidade: {1}</b>\n<b>Temperatura:</b> {2}º\n<b>Sensação Térmica:</b> {3}º\n<b>Condição:</b> {4}\n<b>Chance de Chuva:</b> {5}%\n<b>Mínima:</b> {6}º\n<b>Máxima:</b> {7}º'.format(
        currentWeatherResponse['data']['date'],
        currentWeatherResponse['name'],
        currentWeatherResponse['data']['temperature'],
        currentWeatherResponse['data']['sensation'],
        currentWeatherResponse['data']['condition'],
        forecastWeatherResponse['data'][0]['rain']['precipitation'],
        forecastWeatherResponse['data'][0]['temperature']['min'],
        forecastWeatherResponse['data'][0]['temperature']['max']
    )
    return textMessage


try:
    getCurrentWeatherResponse = getCurrentWeather()
    getForecastWeatherResponse = getForecastWeather()
    getFormatTelegramMessage = formatTelegramMessage(
        getCurrentWeatherResponse, getForecastWeatherResponse)
    sendTelegramMessage(getFormatTelegramMessage)
except Exception as e:
    errorMessage = 'Failed! ' + str(e)
    sendTelegramMessage(errorMessage)
    print(errorMessage)
