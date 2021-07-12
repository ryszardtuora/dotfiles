import requests
import subprocess
import psutil
import time
import json
import re

LONG_INTERVAL = 900 
INTERVAL = 1 

WHITE = "#ECF0F1"
TEAL = "#1ABC9C"
RED = "#C0392B"
GREEN = "#2ECC71"
YELLOW = "#F39C12"
PURPLE = "#be3ff2"#"#9B59B6"#"#8E44AD"

LOCATION = "Warsaw" # your city 

volume_regex = re.compile(r"Volume:.+")

INITIAL_BLOCK = {"full_text": "λ [", "color": TEAL}
FINAL_BLOCK = {"full_text": "] ", "color": TEAL}

def get_audio_block():
    command = ["pactl", "list", "sinks"]
    process = subprocess.Popen(command, stdout = subprocess.PIPE)
    text = process.stdout.read().decode("utf-8")
    match = volume_regex.search(text).group(0)
    volume = int(match.split()[4].replace("%", ""))
    full_text = f"VOL: {volume:3.0f}%"
    audio_block = {"full_text": full_text, "color": WHITE}
    return audio_block

def _bitcoin_gen():
    price = 0
    while True:
        btc_addr = f"https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(btc_addr)
        btc_data = response.json()
        try:
            price_string = btc_data["bpi"]["USD"]["rate"].split('.', 1)[0].replace(",", ".")
            new_price = float(price_string) 
            full_text = f"BTC: {price_string} $"
            if new_price > price:
                color = GREEN
            else:
                color = RED
            btc_block = {"full_text": full_text, "color": color}
            price = new_price
        except KeyError:
            full_text = "BTC data unavailable"
            btc_block = {"full_text": full_text, "color": RED}
        yield btc_block

btc_generator = _bitcoin_gen()

def get_bitcoin_block():
    btc_block = next(btc_generator)
    return btc_block 

def get_weather_block():
    weather_addr = f"http://wttr.in/{LOCATION}?format=j1"
    response = requests.get(weather_addr)
    weather_data = response.json()
    try:
        current_data = weather_data["current_condition"][0]
        temp = current_data["temp_C"]
        humidity = current_data["humidity"]
        pressure = current_data["pressure"]
        full_text = f"{temp}° HUM: {humidity}% {pressure} hPa" 
        weather_block = {"full_text": full_text, "color": YELLOW}
    except KeyError:
        full_text = "Weather data unavailable"
        weather_block = {"full_text": full_text, "color": RED}
    return weather_block

def _net_block_gen():
    net_data = psutil.net_io_counters()
    while True:
        new_net_data = psutil.net_io_counters()
        down_diff = new_net_data.bytes_recv - net_data.bytes_recv
        up_diff = new_net_data.bytes_sent - net_data.bytes_sent
        down_kb = down_diff / 1024
        up_kb = up_diff / 1024
        net_data = new_net_data
        if down_kb < 1024:
            down_val = f"{down_kb:5.1f} KB" 
        else:
            down_val = f"{(down_kb/1024):5.1f} MB"
        if up_kb < 1024:
            up_val = f"{up_kb:5.1f} KB" 
        else:
            up_val = f"{(up_kb/1024):5.1f} MB"
        full_text = f"UP: {up_val} | DOWN: {down_val}"
        if 0 in [down_kb, up_kb]:
            color = RED
        else:
            color = WHITE
        net_block = {"full_text": full_text, "color": color}
        yield net_block

net_generator = _net_block_gen()

def get_net_block():
    net_block = next(net_generator)
    return net_block

def get_memory_block():
    memory_data = psutil.virtual_memory()
    memory_percent = memory_data.percent
    color = WHITE
    if memory_percent > 20:
        color = YELLOW
        if memory_percent > 80:
            color = RED
    full_text = f"MEM: {memory_percent:4.1f}%"
    memory_block = {"full_text": full_text, "color": color}
    return memory_block

def get_cpu_block():
    cpu_percent = psutil.cpu_percent()
    color = WHITE
    temperature_data = psutil.sensors_temperatures()
    k10_data = temperature_data["k10temp"]
    die_data = [e for e in k10_data if e.label == "Tdie"][0]
    temperature = die_data.current
    if temperature > 55:
        color = YELLOW
        if temperature > 80:
            color = RED
    full_text = f"CPU: {cpu_percent:4.1f}% {temperature:.1f}°"
    cpu_block = {"full_text": full_text, "color": color}
    return cpu_block


def get_disk_block():
    process = subprocess.Popen(["df",  "-h", "--total"], stdout=subprocess.PIPE)
    filterer = subprocess.Popen(["grep", "total"], stdin=process.stdout, stdout=subprocess.PIPE) 
    out = filterer.stdout.read().decode("utf-8")
    vals = out.split()
    _, _, _, free_gb, used_pc, _ = vals
    free_pc = 100 - int(used_pc.replace("%", ""))
    if free_pc < 5:
        color = RED
    else:
        color = WHITE
    full_text = f"Free HDD: {free_gb} = {free_pc}%"
    disk_block = {"full_text": full_text, "color": color}
    return disk_block

def get_time_block():
    full_text = time.ctime() 
    timeblock = {"full_text": full_text, "color": PURPLE}
    return timeblock

print('{ "version": 1 }')
print('[')

interval_counter = LONG_INTERVAL 
while True:
    if interval_counter >= LONG_INTERVAL:
        interval_counter = 0
        long_blocks = [get_bitcoin_block(), get_weather_block()] 
    short_blocks = [interval_counter, get_audio_block(), get_net_block(), get_cpu_block(), get_memory_block(), get_disk_block(), get_time_block()]
    blocks = [INITIAL_BLOCK] + long_blocks + short_blocks + [FINAL_BLOCK]
    print(json.dumps(blocks, ensure_ascii=False)+",")
    time.sleep(INTERVAL)
    interval_counter += INTERVAL