#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import os
import platform
import random

class AkilliTahtaSayac:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Sınıf Sayacı 🎓")
        self.pencere.geometry("600x500")
        
        self.renkler = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF"]
        self.arkaplan = random.choice(self.renkler)
        self.pencere.configure(bg=self.arkaplan)
        
        self.kalan_sure = 0
        self.calisiyor = False

        frame = tk.Frame(pencere, bg=self.arkaplan)
        frame.pack(pady=30)

        font_ayar = ("Arial", 14, "bold")
        
        spin_ayar = {"font": ("Arial", 25), "width": 3, "from_": 0, "justify": "center"}

        tk.Label(frame, text="Saat", bg=self.arkaplan, font=font_ayar).grid(row=0, column=0)
        self.saat_spin = tk.Spinbox(frame, **spin_ayar, to=23) 
        self.saat_spin.grid(row=1, column=0, padx=15)

        tk.Label(frame, text="Dak", bg=self.arkaplan, font=font_ayar).grid(row=0, column=1)
        self.dak_spin = tk.Spinbox(frame, **spin_ayar, to=59) 
        self.dak_spin.grid(row=1, column=1, padx=15)

        tk.Label(frame, text="San", bg=self.arkaplan, font=font_ayar).grid(row=0, column=2)
        self.san_spin = tk.Spinbox(frame, **spin_ayar, to=59) 
        self.san_spin.grid(row=1, column=2, padx=15)

        self.zaman_gosterge = tk.Label(pencere, text="00:00:00", font=("Arial", 80, "bold"), bg=self.arkaplan, fg="#333")
        self.zaman_gosterge.pack(pady=20)

        btn_stil = {"font": ("Arial", 18, "bold"), "width": 15, "bd": 5}
        
        self.baslat_buton = tk.Button(pencere, text="BAŞLAT", command=self.baslat, bg="#4CAF50", fg="white", **btn_stil)
        self.baslat_buton.pack(pady=10)

        self.durdur_buton = tk.Button(pencere, text="DURDUR", command=self.durdur_devam, bg="#f44336", fg="white", **btn_stil)
        self.durdur_buton.pack(pady=10)

    def ses_cikar(self):
        sistem = platform.system()
        if sistem == "Windows":
            import winsound
            winsound.Beep(1000, 1500)
        elif sistem == "Darwin":
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif sistem == "Linux":
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga || aplay /usr/share/sounds/alsa/Front_Center.wav')

    def bildirim_gonder(self, baslik, mesaj):
        self.pencere.attributes("-topmost", True)
        sistem = platform.system()
        if sistem == "Windows":
            os.system(f'msg * {baslik}: {mesaj}')
        elif sistem == "Darwin":
            os.system(f"osascript -e 'display notification \"{mesaj}\" with title \"{baslik}\"'")
        elif sistem == "Linux":
            os.system(f'notify-send "{baslik}" "{mesaj}"')
        self.ses_cikar()
        self.pencere.attributes("-topmost", False)

    def guncelle(self):
        if self.calisiyor and self.kalan_sure > 0:
            saat, artan = divmod(self.kalan_sure, 3600)
            dk, sn = divmod(artan, 60)
            self.zaman_gosterge.config(text=f"{saat:02d}:{dk:02d}:{sn:02d}")
            self.kalan_sure -= 1
            self.pencere.after(1000, self.guncelle)
        elif self.kalan_sure == 0 and self.calisiyor:
            self.zaman_gosterge.config(text="00:00:00")
            self.calisiyor = False
            self.bildirim_gonder("SÜRE BİTTİ!", "GEÇMİŞ OLSUN!")

    def baslat(self):
        try:
            s = int(self.saat_spin.get())
            d = int(self.dak_spin.get())
            sn = int(self.san_spin.get())
            self.kalan_sure = (s * 3600) + (d * 60) + sn
            if self.kalan_sure > 0:
                self.calisiyor = True
                self.durdur_buton.config(text="DURDUR", bg="#f44336")
                self.guncelle()
        except ValueError:
            messagebox.showerror("Hata", "Sayı girin!")

    def durdur_devam(self):
        if self.kalan_sure > 0:
            self.calisiyor = not self.calisiyor
            if self.calisiyor:
                self.durdur_buton.config(text="DURDUR", bg="#f44336")
                self.guncelle()
            else:
                self.durdur_buton.config(text="DEVAM ET", bg="#2196F3")

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = AkilliTahtaSayac(root)
    root.mainloop()
