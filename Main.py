import tkinter as tk
import threading
import time
import ctypes
import webbrowser

MAPVK_VK_TO_VSC = 0
KEYEVENTF_KEYUP = 0x0002

def pressionar_tecla(hex_key):
    scan_code = ctypes.windll.user32.MapVirtualKeyW(hex_key, MAPVK_VK_TO_VSC)
    ctypes.windll.user32.keybd_event(hex_key, scan_code, 0, 0)
    time.sleep(0.01)
    ctypes.windll.user32.keybd_event(hex_key, scan_code, KEYEVENTF_KEYUP, 0)

teclas_mapeadas = {
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46, 'G': 0x47,
    'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E,
    'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54, 'U': 0x55,
    'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59, 'Z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36,
    '7': 0x37, '8': 0x38, '9': 0x39,
    'ESPACO': 0x20, 'ENTER': 0x0D, 'SHIFT': 0x10, 'CTRL': 0x11
}

class BobMacroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BobMacro v1.5.2")
        self.root.geometry("450x480")
        self.root.configure(bg="#0B0B0E")
        self.root.resizable(False, False)
        
        self.executando = False
        self.spam_ativo = False
        self.janela_focada = True
        
        self.criar_ui()
        self.checar_foco_janela()

    def abrir_canal(self, event):
        webbrowser.open_new("https://bobdevelopercup.github.io/BobDeveloperCup-Links/")

    def checar_foco_janela(self):
        try:
            id_janela_ativa = ctypes.windll.user32.GetForegroundWindow()
            id_nossa_janela = self.root.winfo_id()
            
            janela_atual_pai = ctypes.windll.user32.GetParent(id_janela_ativa)
            id_real_ativo = janela_atual_pai if janela_atual_pai != 0 else id_janela_ativa

            if id_real_ativo == id_nossa_janela or id_janela_ativa == id_nossa_janela:
                if not self.janela_focada:
                    self.janela_focada = True
                    if self.spam_ativo:
                        self.spam_ativo = False
                        self.lbl_info.config(text="STATUS: PAUSED (WINDOW FOCUSED)", fg="#FFCC00")
            else:
                self.janela_focada = False
        except Exception:
            pass
            
        self.root.after(100, self.checar_foco_janela)

    def criar_ui(self):
        header_frame = tk.Frame(self.root, bg="#111118", height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        try:
            self.logo_img = tk.PhotoImage(file="Icon.png")
            self.logo_img = self.logo_img.subsample(3, 3) 
            lbl_logo = tk.Label(header_frame, image=self.logo_img, bg="#111118")
            lbl_logo.pack(side="left", padx=20, pady=10)
        except Exception:
            pass

        texto_titulo_frame = tk.Frame(header_frame, bg="#111118")
        texto_titulo_frame.pack(side="left", fill="y", pady=15)

        titulo = tk.Label(
            texto_titulo_frame, 
            text="BobMacro", 
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
        container.pack(pady=20, padx=30, fill="both", expand=True)

        def criar_campo_estilizado(row, texto, default_val):
            tk.Label(container, text=texto, font=("Segoe UI Semibold", 9), bg="#0B0B0E", fg="#8E8E9F").grid(row=row, column=0, sticky="w", pady=8)
            
            borda_input = tk.Frame(container, bg="#1E1E2A", padx=1, pady=1)
            borda_input.grid(row=row, column=1, padx=15, pady=8, sticky="we")
            
            input_field = tk.Entry(
                borda_input, 
                font=("Consolas", 11), 
                bg="#13131A", 
                fg="#FFFFFF", 
                insertbackground="#9D4EDD", 
                bd=0,
                highlightthickness=0
            )
            input_field.pack(fill="both", ipadx=8, ipady=6)
            input_field.insert(0, default_val)
            
            input_field.bind("<FocusIn>", lambda e: borda_input.config(bg="#9D4EDD"))
            input_field.bind("<FocusOut>", lambda e: borda_input.config(bg="#1E1E2A"))
            
            return input_field

        self.txt_teclas = criar_campo_estilizado(0, "KEYS TO SPAM", "E, ESPACO")
        self.txt_delay = criar_campo_estilizado(1, "SPAM DELAY (S)", "0.1")
        self.txt_ativacao = criar_campo_estilizado(2, "TOGGLE KEY", "X")

        container.grid_columnconfigure(1, weight=1)

        self.borda_btn = tk.Frame(self.root, bg="#7B2CBF", padx=1, pady=1)
        self.borda_btn.pack(pady=15)

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
            command=self.alternar_estado,
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
        lbl_credito.bind("<Button-1>", self.abrir_canal)

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

    def alternar_estado(self):
        if not self.executando:
            self.executando = True
            self.spam_ativo = False
            self.borda_btn.config(bg="#FF3344")
            self.btn_status.config(text="STOP SERVICE", fg="#FF3344", bg="#181316")
            self.lbl_info.config(text="STATUS: WAITING FOR TOGGLE KEY...", fg="#FFB703")
            threading.Thread(target=self.loop_spam, daemon=True).start()
        else:
            self.executando = False
            self.spam_ativo = False
            self.borda_btn.config(bg="#7B2CBF")
            self.btn_status.config(text="START SERVICE", fg="#7B2CBF", bg="#13131A")
            self.lbl_info.config(text="STATUS: INACTIVE", fg="#555565")

    def loop_spam(self):
        try:
            delay = float(self.txt_delay.get())
        except ValueError:
            delay = 0.1

        teclas_raw = self.txt_teclas.get().upper().replace(" ", "").split(",")
        codigos_spam = [teclas_mapeadas[t] for t in teclas_raw if t in teclas_mapeadas]

        tecla_start_raw = self.txt_ativacao.get().upper().strip()
        codigo_ativacao = teclas_mapeadas.get(tecla_start_raw, None)

        if not codigos_spam or not codigo_ativacao:
            self.root.after(0, self.alternar_estado)
            return

        tuple_pressionada_anterior = False

        while self.executando:
            if not self.janela_focada:
                estado_tecla = (ctypes.windll.user32.GetAsyncKeyState(codigo_ativacao) & 0x8000) != 0

                if estado_tecla:
                    if not tuple_pressionada_anterior:
                        self.spam_ativo = not self.spam_ativo
                        tuple_pressionada_anterior = True
                        if self.spam_ativo:
                            self.lbl_info.config(text="STATUS: ACTIVE (SPAMMING)", fg="#00FFA3")
                        else:
                            self.lbl_info.config(text="STATUS: PAUSED (WAITING)", fg="#FFB703")
                else:
                    tuple_pressionada_anterior = False
            else:
                tuple_pressionada_anterior = False

            if self.spam_ativo and not self.janela_focada:
                for codigo in codigos_spam:
                    if not self.executando or not self.spam_ativo or self.janela_focada:
                        break

                    if (ctypes.windll.user32.GetAsyncKeyState(codigo_ativacao) & 0x8000) != 0:
                        if not tuple_pressionada_anterior:
                            self.spam_ativo = False
                            tuple_pressionada_anterior = True
                            self.lbl_info.config(text="STATUS: PAUSED (WAITING)", fg="#FFB703")
                            break

                    pressionar_tecla(codigo)
                    time.sleep(delay)
            else:
                time.sleep(0.02)

if __name__ == "__main__":
    root = tk.Tk()
    app = BobMacroUI(root)
    root.mainloop()
