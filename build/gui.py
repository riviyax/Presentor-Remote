import json
import threading
import time
import serial
import pyautogui
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
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
    """Save port to JSON"""
    with open("port_config.json", "w") as json_file:
        json.dump({"port": port_input}, json_file)


def load_port_input():
    """Load port from JSON"""
    try:
        with open("port_config.json", "r") as json_file:
            data = json.load(json_file)
            return data.get("port", "")
    except FileNotFoundError:
        return ""


# ---------------- SERIAL LISTENER ----------------
def listen_serial(port):
    global STATUS, SERIAL_CONN

    try:
        SERIAL_CONN = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)
        print(f"[CONNECTED] {port}")
        update_status_images(True)

        while STATUS:
            if SERIAL_CONN.in_waiting > 0:
                data = SERIAL_CONN.readline().decode(errors="ignore").strip()
                print("Arduino:", data)

                # PowerPoint commands
                if data == "NEXT":
                    pyautogui.press("right")
                elif data == "PREVIOUS":
                    pyautogui.press("left")
                elif data == "START":
                    pyautogui.press("f5")
                elif data == "END":
                    pyautogui.press("esc")
                elif data == "BLACK":
                    pyautogui.press("b")
                elif data == "WHITE":
                    pyautogui.press("w")

        if SERIAL_CONN and SERIAL_CONN.is_open:
            SERIAL_CONN.close()
            print("Serial closed.")
            update_status_images(False)

    except serial.SerialException as e:
        messagebox.showerror("Connection Error", f"Could not connect to {port}\n\n{e}")
        update_status_images(False)
        STATUS = False


# ---------------- UI HANDLERS ----------------
def start_button_clicked():
    global STATUS, SERIAL_THREAD, SERIAL_CONN

    port_input = entry_1.get().strip()

    if not port_input:
        messagebox.showerror("Input Error", "Please enter a valid port.")
        return

    if not STATUS:
        try:
            STATUS = True
            save_port_input(port_input)
            SERIAL_THREAD = threading.Thread(target=listen_serial, args=(port_input,), daemon=True)
            SERIAL_THREAD.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")
            STATUS = False
            update_status_images(False)
    else:
        STATUS = False
        if SERIAL_CONN and SERIAL_CONN.is_open:
            SERIAL_CONN.close()
        update_status_images(False)
        messagebox.showinfo("Disconnected", "Serial connection closed.")


def update_status_images(online=False):
    """Switch between online/offline indicator images"""
    if online:
        canvas.itemconfig(image_4, state="normal")  # online icon visible
        canvas.itemconfig(image_5, state="hidden")  # offline hidden
    else:
        canvas.itemconfig(image_4, state="hidden")
        canvas.itemconfig(image_5, state="normal")


# ---------------- UI SETUP ----------------
window = Tk()
window.title("Presenter Remote - Made by Riviya_X")
window.geometry("1071x703")
window.configure(bg="#FFFFFF")
window.iconbitmap('logo.ico')
window.resizable(False, False)

# Load saved port
initial_port = load_port_input()

# Canvas
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=703,
    width=1071,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Backgrounds and graphics
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(535.0, 351.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(533.0, 351.0, image=image_image_2)

canvas.create_text(106.0, 386.0, anchor="nw", text="PRESENTER REMOTE",
                   fill="#FFFFFF", font=("Poppins Bold", 32 * -1))
canvas.create_text(121.0, 454.0, anchor="nw",
                   text=" CONTROL YOUR POWERPOINT\nPRESENTATION WITH YOUR REMOTE",
                   fill="#FFFFFF", font=("Poppins Medium", 16 * -1))
canvas.create_text(117.0, 625.0, anchor="nw",
                   text="CONCEPT & DESIGN BY RIVIYA_X",
                   fill="#404040", font=("Poppins Medium", 16 * -1))

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(256.0, 251.0, image=image_image_3)

canvas.create_rectangle(473.0, 63.0, 478.0, 645.0, fill="#FFFFFF", outline="")
canvas.create_text(535.0, 204.0, anchor="nw",
                   text="STATUS", fill="#FFFFFF", font=("Poppins Bold", 24 * -1))

# Online & Offline images
image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))  # Online
image_4 = canvas.create_image(709.739990234375, 224.64785766601562, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))  # Offline
image_5 = canvas.create_image(709.739990234375, 222.64785766601562, image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(720.0, 348.0, image=image_image_6)

# Entry
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(749.0, 347.0, image=entry_image_1)

entry_1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_1.place(x=627.0, y=323.0, width=244.0, height=46.0)
entry_1.insert(0, initial_port)

canvas.create_text(559.0, 288.0, anchor="nw", text="PORT:",
                   fill="#FFFFFF", font=("Poppins Medium", 24 * -1))

# Start button
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_button_clicked,
    relief="flat"
)
button_1.place(x=613.0, y=450.0, width=213.09805297851562, height=63.0)

# Initial state: Offline
update_status_images(False)

window.mainloop()
