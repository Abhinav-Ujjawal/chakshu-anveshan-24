import board 
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import LED
from gpiozero import Buzzer
import subprocess
from PIL import Image
import numpy as np
from google.cloud import storage
import pygame


command = "libcamera-hello"

def upload(bucket_name, src, dest_blob):
	storage_client = storage.Client()
	bucket = storage_client.bucket(bucket_name)
	blob = bucket.blob(dest_blob)
	blob.upload_from_filename(src)
	print(f"File {src} uploaded to {dest_blob}")
	
def download(bucket_name, src_blob, dest_file_name):
	storage_client = storage.Client()
	bucket = storage_client.bucket(bucket_name)
	blob = bucket.blob(src_blob)
	blob.download_to_filename(dest_file_name)
	print(f"Downloaded {src_blob} to {dest_file_name}")
	
def play_audio(file_path):
	pygame.mixer.init()
	pygame.mixer.music.load(file_path)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(10)

def capture():
	subprocess.call(f"libcamera-still -t 500 --viewfinder-width 2312 --viewfinder-height 1736 --width 4624 --height 3472 -o image.jpg", shell=True)
	upload("chakshu-anveshan", "image.jpg", "image.jpg")
	time.sleep(20)
	download("chakshu-anveshan", "audio.mp3", "audio.mp3")
	play_audio("audio.mp3")
	

Motor = LED(4)
buzz = Buzzer(27)
Motor_2 = LED(22)

i2c = busio.I2C(board.SCL, board.SDA)
ads= ADS.ADS1115(i2c)
channel = AnalogIn(ads,ADS.P0)
channel_1 = AnalogIn(ads,ADS.P1)
while True:
	print("Analog Value: " ,channel.value, "Voltage: ", channel.voltage)
	if (channel.voltage >= 2.5):
		#subprocess.call(command, shell=True)
		buzz.off()
		Motor.on()
		time.sleep(0.5)
		buzz.on()
		Motor.off()
		capture()
	else:
		Motor.off()
		buzz.on()
	if (channel_1.voltage >= 2.5):
		buzz.off()
		Motor.on()
		time.sleep(0.5)
		buzz.on()
		Motor.off()
		capture()
	else:
		Motor_2.off()
		buzz.on()
	print("Analog Value_1: " ,channel_1.value, "Voltage: ", channel_1.voltage)
	time.sleep(0.2)
