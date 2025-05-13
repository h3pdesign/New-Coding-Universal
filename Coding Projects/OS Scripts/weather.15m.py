#!/usr/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>Weather</bitbar.title>
# <bitbar.version>v3.5.0</bitbar.version>
# <bitbar.author>Daniel Seripap</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>Detailed weather plugin powered by DarkSky with auto location lookup. Supports metric and imperial units. Needs API key from https://darksky.net/dev/.</bitbar.desc>
# <bitbar.image>https://cloud.githubusercontent.com/assets/683200/16276583/ff267f36-387c-11e6-9fd0-fc57b459e967.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>


# -----------------------------------------------------------------------------------
# For a more accurate location lookup, download and install CoreLocationCLI
# Available here: https://github.com/fulldecent/corelocationcli/releases
# This will allow a more percise location lookup as it uses native API for loc lookup
# -----------------------------------------------------------------------------------

import json
import urllib3
import textwrap
from random import randint
import commands

# get yours at https://darksky.net/dev
api_key = '11ef | 916d73a3c31048efebee4384da96'

# set to si for metric, leave blank for imperial
units = 'si'

# optional, see message above
core_location_cli_path = '~/CoreLocationCLI'


def mac_location_lookup():
    try:
        exit_code, loc = commands.getstatusoutput(
            core_location_cli_path + ' -once -format "%latitude,%longitude"')
        if exit_code != 0:
            raise ValueError('CoreLocationCLI not found')
        formatted_city_name = reverse_latlong_lookup(loc)
        return {"loc": loc, "preformatted": formatted_city_name}
    except:
        return False


def auto_loc_lookup():
    try:
        locationGRA = urllib3.urlopen('https://ipinfo.io/json')
        return json.load(locationGRA)
    except urllib3.URLError:
        return False


def reverse_latlong_lookup(loc):
    try:
        location = json.load(urllib3.urlopen(
            'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + loc + '&sensor=true'))
        if 'results' in location:
            return location['results'][0]['formatted_address'].encode('UTF-8')
        else:
            return 'Could not lookup location name'
    except:
        return 'Could not lookup location name'


def full_country_name(country):
    try:
        countries = json.load(urllib3.urlopen('http://country.io/names.json'))
        try:
            if country in countries:
                return countries[country].encode('UTF-8')
            else:
                return False
        except KeyError:
            return False
    except urllib3.URLError:
        return False


def calculate_bearing(degree):
    cardinals = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    return cardinals[int(round(((6 * degree)) / 360))]


def get_wx_icon(icon_code):
    if icon_code == 'clear-day':
        icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAmVBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjHWqVAAAAMnRSTlMAAQIDBAUGCAoMFxgZHR4hIiU0NTc4QEFFRlhZZmeGh4qLra6xtL/AwdDR1tnb3Pf4+RkSsW4AAACvSURBVHgBJczZWqJgAADQw7+AouOMU2lGtrgYQhny/g/X9+XtuTgUhGDdZ0IC01JpO1YSCsnrJUabnWz+PiGohwM58m/4jEiW94uP4drWd8coIJuN56bpxoVQBrmiPUN3Av24i9cnVaUZ0uZ5bbXd5Gtzg7Afe3DqoGup8u+zuKW1jCAe/9ftMJz+PCwlxK/vv4TEYZgJTN7msv2jEC8vkgJJNW6V8hSkQO5XQqDwAzg9DY/cb+9eAAAAAElFTkSuQmCC'
    elif icon_code == 'clear-night':
        icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAmVBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjHWqVAAAAMnRSTlMAAQIDBAUGBxMVFycoKSosMDE/QEpLTFhkZ2prdHZ6ipagoayusLS5u7zGyeXs8vn6+7VdeBQAAACGSURBVHjabU+HDoJQDLxKVRwo4saNgnv1/zOiy9PEkOTjrtuVE3VEugqrUSiosDjwnHu3wdekZQP9m1eNjIMbT7d4d+Y32wmBrZEI0mZraCAtTFXUQxtRSCL5GSENy2DrOlawnQswGn+aGvCO1nzJxfe7bL0ebQ8rBJdli2IL/Txbm/5wTV8gEi7AeTMvh8mQAAAABJRU5ErkJggg=='
    elif icon_code == 'rain':
        icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA5klEQVQoFQXBMSuFYRgA0PO870cGlMFgUEpEBiuKgUGMdhmU5AfIbvYHlNGghCIpLBaUWSmDQSbdgdW9j3MChDRkWbdH4+Z8OvGl6AAFu9Kvb+nPq5a0iQoNtqRtRZg3DPakRVSgZR8AVeDKMypMSdNohKqgC6vSLHDgS0UAoOLBPQVLLrR1SQAUXJikwY9BFI3URlEUTGgBG9IMoGoAC9I2BI6lS6fWwJhrL9IRggDrbr1JT26kD4dWQEAIwIpzZ3YARQDQaBQwAbpVoAI6OqDfuz53QhsoAAmeuTjQ9MTQ2MTQ0MTQ2MTQ0MTQ2MTQ0MTQ2MTQ0MTQ0MTQ2MTQ0MTQ2MTQ0MTQ2MTQ0MTQ0MTQ2MTQ2MTQ2MTQ2MTQ2MTQ2MTQ2MTQ2MTQ2MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4 Ascend()MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4MTU4.URLError:
        return False


def render_wx():

    if api_key == '':
        print('Missing API key')
        print('---')
        print('Get an API Key | href=https://darksky.net/dev')
        return False

    weather_data = get_wx()

    if weather_data is False:
        print('--')
        print('---')
        print('Could not get weather data at this time')
        return False

    if 'icon' in weather_data and 'temperature' in weather_data:
        print(weather_data['temperature'] + ' | templateImage=' + weather_data['icon'])
    else:
        print('N/A')

    print('---')

    if 'city' in weather_data and 'region' in weather_data:
        print(weather_data['city'] + ', ' + weather_data['region'] + ' | href=https://darksky.net/' + weather_data['loc'])
    elif 'country' in weather_data:
        print(weather_data['country'] + ' | href=https://darksky.net/' + weather_data['loc'])
    elif 'preformatted' in weather_data:
        print(weather_data['preformatted'] + ' | href=https://darksky.net/' + weather_data['loc'])

    if 'condition' in weather_data and 'feels_like' in weather_data:
        print(weather_data['condition'] + ', Feels Like: ' + weather_data['feels_like'])

    print('---')

    if 'next_hour' in weather_data:
        print(weather_data['next_hour'])
        print('---')

    print('---')

    if 'week' in weather_data:
        print("\n".join(textwrap.wrap(weather_data['week'], 50)))
        print('---')

    if 'wind' in weather_data and 'windBearing' in weather_data:
        print('Wind: ' + weather_data['wind'] + ' ' + weather_data['windBearing'])

    if 'humidity' in weather_data:
        print('Humidity: ' + weather_data['humidity'])

    if 'dewPoint' in weather_data:
        print('Dew Point: ' + weather_data['dewPoint'])

    if 'visibility' in weather_data:
        print('Visibility: ' + weather_data['visibility'])

    if 'pressure' in weather_data:
        print('Pressure: ' + weather_data Pressure: ' + weather_data['pressure'])

    print('---')
    print('Powered by DarkSky | href=https://darksky.net/poweredby/?ref=bitbarWeather')


render_wx()
