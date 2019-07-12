from machine import Pin, ADC, DAC, PWM
from time import sleep
from _thread import start_new_thread as thread
from random import randint
import network
import json
import urequests

#################################################### status
R = Pin(21, Pin.OUT)
G = Pin(19, Pin.OUT)
B = Pin(18, Pin.OUT)

def start_rgb_red():
  R.value(1)
  G.value(0)
  B.value(0)

def start_rgb_green():
  R.value(0)
  G.value(1)
  B.value(0)

#thread(start_rgb_red())

button = Pin(5, Pin.IN)

def butt():
  button_st = int(button.value())
  return button_st

'''
def press_button():
  return button.value()
  #sleep(0.2)
thread(press_button())
'''

def Force_Button():
  while True:
    a = button.value()
    if a == int(0):
      start_rgb_red()
    if a == int(1):
      start_rgb_green() 
    #print(a)
    sleep(0.1)
################################################################
led_up = Pin(0, Pin.OUT)
led_down = Pin(2, Pin.OUT)
led_rig = Pin(4, Pin.OUT)
led_lef = Pin(18, Pin.OUT)

light_dict = {1: led_lef,
            2:led_down,
            3:led_up,
            4:led_down}

led_up.value(0)
led_down.value(0)
led_lef.value(0)
led_rig.value(0)

"Joystick code"
PINX = 34   # needs to be a pin that supports ADC
PINY = 32   # needs to be a pin that supports ADC
PINSW = 27

cx = ADC(Pin(PINX))
cx.atten(ADC.ATTN_11DB)
cy = ADC(Pin(PINY))
cy.atten(ADC.ATTN_11DB)
sw = Pin(PINSW, Pin.IN, Pin.PULL_UP)

def button_pressed(p):
    print('Click')

def joystick(adc):
    return max(6, min(120, int(adc.read()/32)))

def check_joystick(dx, dy):
    "0=center, 1=left, 2=right, 3=up, 4=down, 5=up-left, 6=down-right, 7=up-right, 8=down-left"
    x = joystick(dx)
    y = joystick(dy)
    direction = 0
    if x < 14 and 54 < y < 64:
        direction = 1
    elif 113 < x and 54 < y < 64:
        direction = 2
    elif 54 < x < 64 and y < 13:
        direction = 3
    elif 54 < x < 64 and 113 < y:
        direction = 4
    elif x < 14 and y < 14:
        direction = 5
    elif 113 < x and 113 < y:
        direction = 6
    elif 113 < x and y < 14:
        direction = 7
    elif x < 14 and 113 < y:
        direction = 8
    return direction

sw.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)


"Buzzer code"
buzzer = PWM(Pin(25))

def start_buzzer(value):
    buzzer.freq(value)

def stop_buzzer():
    buzzer.deinit()


"RGB code"
R = Pin(21, Pin.OUT)
G = Pin(19, Pin.OUT)
B = Pin(18, Pin.OUT)

'''
def start_rgb_red():
    R.value(1)
    G.value(0)
    B.value(0)

def start_rgb_green():
    R.value(0)
    G.value(1)
    B.value(0)
'''
def start_rgb_blue():
    R.value(0)
    G.value(0)
    B.value(1)

def stop_rgb():
    R.value(0)
    G.value(0)
    B.value(0)


"Button code"
button = Pin(5, Pin.IN)
state=False
def press_button():
    return button.value()
def check_button():
    status = None
    if button.value() == 0:
        status = True
    elif button.value() == 1:
        status = False
    return status   #True = pressed, False = not pressed




start_val = False
button_val = False
datastat = {}
count_game = 0
first_game = True
http_dict = {}
day = 12

def check_start():
    while True:
        if check_button() == True:
        	start_val = True

def game(htp_dct):
    stop_rgb()
    temp_lst = []
    while len(temp_lst) != 10:
        print(temp_lst)
        check = check_joystick(cx,cy)
        light_on = 1
        light_dict[light_on].value(1)
        sleep(0.1)
        if check_joystick(cx, cy) != 0:
            if check_joystick(cx, cy) == light_on:
                temp_lst.append(True)
                light_dict[light_on].value(0)
            else:
                temp_lst.append(False)
                light_dict[light_on].value(0)
        else:
            temp_lst.append(False)
            light_dict[light_on].value(0)
    http_dict[str(day)] = (sum(temp_lst)/len(temp_lst))*100
    print(http_dict)
    day += 1
    print(day)
    end_end()

'''
def data():
    datastat.update(http_dict)
'''
def end_end():
    start_val = False
    update(str(day), http_dict)
	#display score
	#sent netPRO to server
    #data.update({count_game:count_correct})


##################################################################################


ssid = 'exceed16_8'
pwd = '12345678'
station = network.WLAN(network.STA_IF)
station.active(True)

url2 = "https://exceed.superposition.pknn.dev/data/kenmuayMC"
url1 = "https://exceed.superposition.pknn.dev/data/kenmuaySTAT"
data = {"9":60,"10":40,"11":0,"12":80}
headers = {"content-type":"application/json"}

def send():
  if not station.isconnected():
    station.connect(ssid, pwd)
    print('Connecting...')
    sleep(3)  
    if station.isconnected():
      print('connected')  
  js = json.dumps({"data":data})
  print(data)
  r = urequests.post(url1, data=js, headers=headers)
  results = r.json()
  print(results)
  sleep(2)

def receive():
  if not station.isconnected():
    station.connect(ssid, pwd)
    print('Connecting...')
    sleep(3)  
    if station.isconnected():
      print('connected')  
  js = json.dumps({"data":data})
  print(data)
  r = urequests.get(url2)
  results = r.json()
  print(results)
  sleep(2)
  
def update(key, data):
  if not station.isconnected():
    station.connect(ssid, pwd)
    print('Connecting...')
    sleep(3)  
    if station.isconnected():
      print('connected')  
  
  r = urequests.get(url1)
  results = r.json()
  print(results)
  results[key] = data
  r = urequests.post(url1, data=json.dumps({"data":results}), headers=headers)
  #print(r.json)
  print("end")
  
#thread(send(),())
#thread(receive(),())




#################################################################################
thread(game(http_dict),())
thread(Force_Button(),())
#thread(update('day', http_dict),())
