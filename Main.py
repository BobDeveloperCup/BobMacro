import threading
import time
import ctypes
import webbrowser
import urllib.request
import io
import tkinter as tk
from PIL import Image, ImageTk

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
IMAGE_RAW_URL = "https://raw.githubusercontent.com/BobDeveloperCup/BobMacro/main/Icon.png"

def mouse_click():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

mapped_keys = {
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46, 'G': 0x47,
    'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E,
    'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54, 'U': 0x55,
    'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59, 'Z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36,
    '7': 0x37, '8': 0x38, '9': 0x39,
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74, 'F6': 0x75,
    'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
    'ESPACO': 0x20, 'ENTER': 0x0D, 'SHIFT': 0x10, 'CTRL': 0x11
}

class BobMacroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BobClicker v1.0.0")
        self.root.geometry("450x480")
        self.root.configure(bg="#0B0B0E")
        self.root.resizable(False, False)
        
        self.running = False
        self.spam_active = False
        self.window_focused = True
        
        self.cached_activation_code = None
        self.cached_delay = 0.1
        
        self.create_ui()
        self.check_window_focus()
        threading.Thread(target=self.load_network_logo, daemon=True).start()

    def open_channel(self, event):
        webbrowser.open_new("https://bobdevelopercup.github.io/BobDeveloperCup-Links/")

    def check_window_focus(self):
        try:
            active_window_id = ctypes.windll.user32.GetForegroundWindow()
            our_window_id = self.root.winfo_id()
            
            current_parent_window = ctypes.windll.user32.GetParent(active_window_id)
            real_active_id = current_parent_window if current_parent_window != 0 else active_window_id

            if real_active_id == our_window_id or active_window_id == our_window_id:
                if not self.window_focused:
                    self.window_focused = True
                    if self.spam_active:
                        self.spam_active = False
                        self.lbl_info.config(text="STATUS: PAUSED (WINDOW FOCUSED)", fg="#FFCC00")
            else:
                self.window_focused = False
        except Exception:
            pass
            
        self.root.after(100, self.check_window_focus)

    def load_network_logo(self):
        try:
            with urllib.request.urlopen(IMAGE_RAW_URL, timeout=10) as response:
                image_data = response.read()
            raw_image = Image.open(io.BytesIO(image_data))
            
            width, height = raw_image.size
            raw_image = raw_image.resize((width // 3, height // 3), Image.Resampling.LANCZOS)
            
            self.logo_img = ImageTk.PhotoImage(raw_image)
            self.root.after(0, lambda: self.lbl_logo.config(image=self.logo_img))
        except Exception:
            pass

    def create_ui(self):
        header_frame = tk.Frame(self.root, bg="#111118", height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        self.lbl_logo = tk.Label(header_frame, bg="#111118")
        self.lbl_logo.pack(side="left", padx=20, pady=10)

        texto_titulo_frame = tk.Frame(header_frame, bg="#111118")
        texto_titulo_frame.pack(side="left", fill="y", pady=15)

        titulo = tk.Label(
            texto_titulo_frame, 
            text="BobClicker", 
            font=("Segoe UI", 18, "bold"), 
            bg="#111118", 
            fg="#FFFFFF"
        )
        titulo.pack(anchor="w")
        
        versao = tk.Label(
            texto_titulo_frame, 
            text="premium execution edition", 
            font=("Segoe UI Semibold", 8), 
            bg="#111118", 
            fg="#7B2CBF"
        )
        versao.pack(anchor="w")

        divisor = tk.Frame(self.root, bg="#1A1A26", height=2)
        divisor.pack(fill="x")

        container = tk.Frame(self.root, bg="#0B0B0E")
        container.pack(pady=15, padx=30, fill="both", expand=True)

        def create_styled_field(row, text, default_val):
            tk.Label(container, text=text, font=("Segoe UI Semibold", 9), bg="#0B0B0E", fg="#8E8E9F").grid(row=row, column=0, sticky="w", pady=6)
            
            borda_input = tk.Frame(container, bg="#1E1E2A", padx=1, pady=1)
            borda_input.grid(row=row, column=1, padx=15, pady=6, sticky="we")
            
            input_field = tk.Entry(
                borda_input, 
                font=("Consolas", 11), 
                bg="#13131A", 
                fg="#FFFFFF", 
                insertbackground="#9D4EDD", 
                bd=0,
                highlightthickness=0
            )
            input_field.pack(fill="both", ipadx=8, ipady=5)
            input_field.insert(0, default_val)
            
            input_field.bind("<FocusIn>", lambda e: borda_input.config(bg="#9D4EDD"))
            input_field.bind("<FocusOut>", lambda e: borda_input.config(bg="#1E1E2A"))
            
            return input_field

        self.txt_min = create_styled_field(0, "MINUTES", "0")
        self.txt_sec = create_styled_field(1, "SECONDS", "0")
        self.txt_ms = create_styled_field(2, "MILLISECONDS", "100")
        self.txt_ativacao = create_styled_field(3, "TOGGLE KEY", "F8")

        container.grid_columnconfigure(1, weight=1)

        self.borda_btn = tk.Frame(self.root, bg="#7B2CBF", padx=1, pady=1)
        self.borda_btn.pack(pady=10)

        self.btn_status = tk.Button(
            self.borda_btn, 
            text="START SERVICE", 
            font=("Segoe UI Black", 10), 
            bg="#13131A", 
            fg="#7B2CBF", 
            bd=0, 
            highlightthickness=0,
            activebackground="#7B2CBF", 
            activeforeground="#0B0B0E",
            command=self.toggle_state,
            cursor="hand2"
        )
        self.btn_status.pack(ipadx=35, ipady=10)

        lbl_credito = tk.Label(
            self.root,
            text="Made By - BobDeveloperCup",
            font=("Segoe UI Bold", 9, "underline"),
            bg="#0B0B0E",
            fg="#9D4EDD",
            cursor="hand2"
        )
        lbl_credito.pack(pady=5)
        lbl_credito.bind("<Button-1>", self.open_channel)

        footer_frame = tk.Frame(self.root, bg="#08080A", height=35)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        self.lbl_info = tk.Label(
            footer_frame, 
            text="STATUS: INACTIVE", 
            font=("Segoe UI Bold", 8), 
            bg="#08080A", 
            fg="#555565"
        )
        self.lbl_info.pack(side="left", padx=20, expand=True, anchor="w")

    def toggle_state(self):
        if not self.running:
            try:
                minutes = float(self.txt_min.get() or 0) * 60
                seconds = float(self.txt_sec.get() or 0)
                milliseconds = float(self.txt_ms.get() or 0) / 1000
                self.cached_delay = minutes + seconds + milliseconds
                if self.cached_delay <= 0:
                    self.cached_delay = 0.005
            except ValueError:
                self.cached_delay = 0.1

            tecla_start_raw = self.txt_ativacao.get().upper().strip()
            self.cached_activation_code = mapped_keys.get(tecla_start_raw, None)

            if not self.cached_activation_code:
                return

            self.running = True
            self.spam_active = False
            self.borda_btn.config(bg="#FF3344")
            self.btn_status.config(text="STOP SERVICE", fg="#FF3344", bg="#181316")
            self.lbl_info.config(text="STATUS: WAITING FOR TOGGLE KEY...", fg="#FFB703")
            threading.Thread(target=self.spam_loop, daemon=True).start()
        else:
            self.running = False
            self.spam_active = False
            self.borda_btn.config(bg="#7B2CBF")
            self.btn_status.config(text="START SERVICE", fg="#7B2CBF", bg="#13131A")
            self.lbl_info.config(text="STATUS: INACTIVE", fg="#555565")

    def spam_loop(self):
        tuple_pressionada_anterior = False

        while self.running:
            estado_tecla = (ctypes.windll.user32.GetAsyncKeyState(self.cached_activation_code) & 0x8000) != 0

            if estado_tecla:
                if not tuple_pressionada_anterior:
                    self.spam_active = not self.spam_active
                    tuple_pressionada_anterior = True
                    if self.spam_active:
                        self.lbl_info.config(text="STATUS: ACTIVE (CLICKING)", fg="#00FFA3")
                    else:
                        self.lbl_info.config(text="STATUS: PAUSED (WAITING)", fg="#FFB703")
            else:
                tuple_pressionada_anterior = False

            if self.spam_active and not self.window_focused:
                mouse_click()
                time.sleep(self.cached_delay)
            else:
                time.sleep(0.03)

if __name__ == "__main__":
    root = tk.Tk()
    app = BobMacroUI(root)
    root.mainloop()
