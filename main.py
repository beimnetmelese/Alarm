import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import time
import threading
import pygame
from datetime import datetime

pygame.mixer.init()

ALARM_SOUND_PATH = "alarm.mp3"

alarms = []

def load_sound():
    global ALARM_SOUND_PATH
    ALARM_SOUND_PATH = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    pygame.mixer.music.load(ALARM_SOUND_PATH)

def set_alarm():
    alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    selected_days = [day for day, var in days_vars.items() if var.get()]
    if not selected_days:
        messagebox.showwarning("Invalid Input", "Please select at least one day for the alarm.")
        return
    alarm_info = {
        "time": alarm_time,
        "days": selected_days,
        "sound": ALARM_SOUND_PATH
    }
    alarms.append(alarm_info)
    update_alarm_list()
    start_alarm_thread(alarm_info)

def start_alarm_thread(alarm_info):
    alarm_thread = threading.Thread(target=check_alarm, args=(alarm_info,))
    alarm_thread.daemon = True
    alarm_thread.start()

def check_alarm(alarm_info):
    while True:
        current_time = time.strftime("%H:%M:%S")
        current_day = datetime.today().strftime('%A')
        if current_time == alarm_info['time'] and current_day in alarm_info['days']:
            pygame.mixer.music.load(alarm_info['sound'])
            pygame.mixer.music.play(-1) 
            show_wake_up_message()
            break
        time.sleep(1)

def show_wake_up_message():
    wake_up_popup = tk.Toplevel(root)
    wake_up_popup.title("Wake Up!")
    wake_up_popup.geometry("300x200")
    wake_up_popup.configure(bg="#F5F5F5")
    
    tk.Label(wake_up_popup, text="Time to wake up!", font=("Helvetica", 16), bg="#F5F5F5").pack(pady=20)
    
    ttk.Button(wake_up_popup, text="Stop Alarm", command=lambda: stop_alarm(wake_up_popup)).pack(pady=5)
    ttk.Button(wake_up_popup, text="Snooze", command=lambda: snooze_alarm(wake_up_popup)).pack(pady=5)

def stop_alarm(popup):
    pygame.mixer.music.stop()
    popup.destroy()

def snooze_alarm(popup):
    snooze_minutes = int(snooze_time.get())
    stop_alarm(popup)
    snooze_until = time.time() + snooze_minutes * 60
    while time.time() < snooze_until:
        time.sleep(1)
    pygame.mixer.music.load(ALARM_SOUND_PATH)
    pygame.mixer.music.play(-1)  
    show_wake_up_message()

def update_alarm_list():
    for widget in alarm_list_frame.winfo_children():
        widget.destroy()
    for idx, alarm in enumerate(alarms):
        alarm_text = f"{alarm['time']} on {', '.join(alarm['days'])}"
        ttk.Label(alarm_list_frame, text=alarm_text).grid(row=idx, column=0, padx=5, pady=2)
        ttk.Button(alarm_list_frame, text="Delete", command=lambda idx=idx: delete_alarm(idx)).grid(row=idx, column=1, padx=5, pady=2)

def delete_alarm(idx):
    del alarms[idx]
    update_alarm_list()

root = tk.Tk()
root.title("Alarm Clock")
root.geometry("700x600")
root.configure(bg="#E8E8E8")

hour = tk.StringVar()
minute = tk.StringVar()
second = tk.StringVar()
snooze_time = tk.StringVar(value="5")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))

title_frame = ttk.Frame(root, padding=(20, 10))
title_frame.pack()

ttk.Label(title_frame, text="Alarm Clock", font=("Helvetica", 18, "bold")).pack()
ttk.Label(title_frame, text="Set and manage your alarms easily", font=("Helvetica", 12)).pack()

settings_frame = ttk.Frame(root, padding=(20, 10))
settings_frame.pack()

ttk.Label(settings_frame, text="Hour (24-hour format):").grid(row=0, column=0, padx=5, pady=5, sticky="E")
ttk.Entry(settings_frame, textvariable=hour).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(settings_frame, text="Minute:").grid(row=1, column=0, padx=5, pady=5, sticky="E")
ttk.Entry(settings_frame, textvariable=minute).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(settings_frame, text="Second:").grid(row=2, column=0, padx=5, pady=5, sticky="E")
ttk.Entry(settings_frame, textvariable=second).grid(row=2, column=1, padx=5, pady=5)

days_frame = ttk.LabelFrame(settings_frame, text="Days", padding=(10, 5))
days_frame.grid(row=3, column=0, columnspan=2, pady=10)

days_vars = {day: tk.BooleanVar() for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
for idx, (day, var) in enumerate(days_vars.items()):
    ttk.Checkbutton(days_frame, text=day, variable=var).grid(row=0, column=idx, padx=5)

ttk.Button(settings_frame, text="Set Alarm", command=set_alarm).grid(row=4, column=0, columnspan=2, pady=10)

ttk.Button(settings_frame, text="Choose Alarm Sound", command=load_sound).grid(row=5, column=0, columnspan=2, pady=10)

ttk.Label(settings_frame, text="Snooze Time (minutes):").grid(row=6, column=0, padx=5, pady=5, sticky="E")
ttk.Entry(settings_frame, textvariable=snooze_time).grid(row=6, column=1, padx=5, pady=5)

alarm_list_frame = ttk.Frame(root, padding=(20, 10))
alarm_list_frame.pack()

ttk.Label(alarm_list_frame, text="Current Alarms:", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

root.mainloop()
