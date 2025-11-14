import json
import threading
import time
import serial
import pyautogui
import os
import sys
import socket
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Text, Scrollbar, END, DISABLED, NORMAL
from pathlib import Path

# ---------------- PATH CONFIG ----------------
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"I:\Dev\Electronics\Presentor-Remote\build\assets\frame0")

# ---------------- GLOBALS ----------------
STATUS = False
SERIAL_CONN = None
SERIAL_THREAD = None

# ---------------- HELPERS ----------------
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def save_port_input(port_input):
    with open("port_config.json", "w") as json_file:
        json.dump({"port": port_input}, json_file)

def load_port_input():
    try:
        with open("port_config.json", "r") as json_file:
            data = json.load(json_file)
            return data.get("port", "")
    except FileNotFoundError:
        return ""

# ---------------- SINGLE INSTANCE CHECK ----------------
def check_already_running():
    """Prevent multiple instances. Creates a local socket lock."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 65432))
        return s  # keep socket open to maintain the lock
    except OSError:
        messagebox.showinfo("Already Running", "Presenter Remote is already running!")
        sys.exit()

# ---------------- SERIAL OUTPUT APPEND ----------------
def append_serial_text(message):
    serial_text.config(state=NORMAL)
    serial_text.insert(END, message + "\n")
    serial_text.see(END)  # auto scroll
    serial_text.config(state=DISABLED)

# ---------------- SERIAL LISTENER ----------------
def listen_serial(port):
    global STATUS, SERIAL_CONN
    try:
        SERIAL_CONN = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)
        print(f"[CONNECTED] {port}")
        window.after(0, lambda: update_status_images(True))

        while STATUS:
            if SERIAL_CONN.in_waiting > 0:
                data = SERIAL_CONN.readline().decode(errors="ignore").strip()
                if not data:
                    continue
                # Print to GUI text box
                print(f"Arduino: {data}")

                # PowerPoint + Scroll commands
                if data == "NEXT":
                    pyautogui.press("right")
                elif data == "PREVIOUS":
                    pyautogui.press("left")
                elif data == "START":
                    os.system('start powerpnt')
                elif data == "END":
                    pyautogui.press("esc")
                elif data == "BLACK":
                    pyautogui.press("b")
                elif data == "WHITE":
                    pyautogui.press("w")
                elif data == "UP":
                    pyautogui.press("up")
                elif data == "DOWN":
                    pyautogui.press("down")
                elif data == "APP":
                    pyautogui.press("f5")
                elif data == "EXIT":
                    pyautogui.hotkey('alt', 'f4', interval=0.1)
                elif data == "PAUSE":
                    pyautogui.press("space")
                elif data == "TASK":
                    pyautogui.hotkey('ctrl', 'shift', 'esc', interval=0.1)
        

        # cleanup
        if SERIAL_CONN and SERIAL_CONN.is_open:
            try:
                SERIAL_CONN.close()
            except:
                pass
        print("Serial closed.")
        window.after(0, lambda: update_status_images(False))

    except serial.SerialException as e:
        print(f"[SerialException] {e}")
        window.after(0, lambda: messagebox.showerror("Connection Error", f"Could not connect to {port}\n\n{e}"))
        STATUS = False
        window.after(0, lambda: update_status_images(False))
    except Exception as e:
        print(f"[Error] {e}")
        window.after(0, lambda: messagebox.showerror("Error", str(e)))
        STATUS = False
        window.after(0, lambda: update_status_images(False))

# ---------------- UI HANDLERS ----------------
def start_button_clicked():
    global STATUS, SERIAL_THREAD
    port_input = entry_1.get().strip()

    if not port_input:
        messagebox.showerror("Input Error", "Please enter a valid port.")
        return

    if not port_input.upper().startswith("COM"):
        messagebox.showerror("Input Error", "Invalid port. Please enter COM1, COM2, COM3 etc.")
        return

    save_port_input(port_input)

    if not STATUS:
        STATUS = True
        update_status_images(True)
        SERIAL_THREAD = threading.Thread(target=listen_serial, args=(port_input,), daemon=True)
        SERIAL_THREAD.start()

        # Place the serial/output text box and scrollbar now
        serial_text.place(x=525, y=540, width=420, height=110)
        scrollbar.place(x=945, y=540, height=110)

    else:
        messagebox.showinfo("Info", "Already connected.")

def stop_button_clicked():
    global STATUS, SERIAL_CONN
    if STATUS:
        STATUS = False
        try:
            if SERIAL_CONN and SERIAL_CONN.is_open:
                SERIAL_CONN.close()
        except:
            pass
        update_status_images(False)
        print("Disconnected from serial.")
    else:
        print("Already disconnected.")

def update_status_images(online=False):
    if online:
        canvas.itemconfig(image_4, state="normal")
        canvas.itemconfig(image_5, state="hidden")
        button_1.place_forget()
        button_2.place(x=613.0, y=450.0, width=213.098, height=63.0)
    else:
        canvas.itemconfig(image_4, state="hidden")
        canvas.itemconfig(image_5, state="normal")
        button_2.place_forget()
        button_1.place(x=613.0, y=450.0, width=213.098, height=63.0)

# ---------------- UI SETUP ----------------
lock_socket = check_already_running()  # ensure single instance

window = Tk()
window.title("Presenter Remote - Made by Riviya_X")
window.geometry("1071x703")
window.configure(bg="#FFFFFF")

try:
    window.iconbitmap('logo.ico')
except:
    pass
window.resizable(False, False)

initial_port = load_port_input()

canvas = Canvas(window, bg="#FFFFFF", height=703, width=1071, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(535.0, 351.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(533.0, 351.0, image=image_image_2)

canvas.create_text(106.0, 386.0, anchor="nw", text="PRESENTER REMOTE", fill="#FFFFFF", font=("Poppins Bold", 32 * -1))
canvas.create_text(121.0, 454.0, anchor="nw", text="     CONTROL YOUR POWERPOINT\nPRESENTATION WITH YOUR REMOTE", fill="#FFFFFF", font=("Poppins Medium", 16 * -1))
canvas.create_text(117.0, 625.0, anchor="nw", text="CONCEPT & DESIGN BY RIVIYA_X", fill="#404040", font=("Poppins Medium", 16 * -1))

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(256.0, 251.0, image=image_image_3)

canvas.create_rectangle(473.0, 63.0, 478.0, 645.0, fill="#FFFFFF", outline="")
canvas.create_text(535.0, 204.0, anchor="nw", text="STATUS", fill="#FFFFFF", font=("Poppins Bold", 24 * -1))

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))  # Online
image_4 = canvas.create_image(709.739, 224.647, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))  # Offline
image_5 = canvas.create_image(709.739, 222.647, image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(720.0, 348.0, image=image_image_6)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(749.0, 347.0, image=entry_image_1)

entry_1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_1.place(x=627.0, y=323.0, width=244.0, height=46.0)
entry_1.insert(0, initial_port)

canvas.create_text(559.0, 288.0, anchor="nw", text="PORT:", fill="#FFFFFF", font=("Poppins Medium", 24 * -1))

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=start_button_clicked, relief="flat")
button_1.place(x=613.0, y=450.0, width=213.098, height=63.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=stop_button_clicked, relief="flat")

# ---------------- SERIAL OUTPUT TEXT BOX WITH SCROLLBAR (Initially Hidden) ----------------
serial_text = Text(window, bg="#F0F0F0", fg="#000000", font=("Courier", 12), state=DISABLED)
scrollbar = Scrollbar(window, command=serial_text.yview)
serial_text.configure(yscrollcommand=scrollbar.set)
# Do NOT place them yet; will appear after pressing Start

# ---------------- REDIRECT PRINT TO TEXT BOX ----------------
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, message)
        self.text_widget.see(END)
        self.text_widget.config(state=DISABLED)

    def flush(self):
        pass

sys.stdout = StdoutRedirector(serial_text)
sys.stderr = StdoutRedirector(serial_text)  # also capture errors

update_status_images(False)
window.mainloop()
