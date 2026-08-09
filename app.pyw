import customtkinter as cst
import tkinter as tk
from google import genai
import threading
import sys

if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

cst.set_appearance_mode("Dark")
cst.set_default_color_theme("blue")

APP_NAME = "Torvarcore AI"
# 🔑 اكتب مفتاح الـ API الجديد والنظيف بتاعك هنا بيدك وبدون أي علامات مميزة:
API_KEY = "AQ.Ab8RN6KmFIQu-XUDctxRdMw3qjLszH78Ge92LycGOJLj2ANpFQ"

client = genai.Client(api_key=API_KEY)

class TorvarcoreFinalShell(cst.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("800x600")
        self.configure(fg_color="#212121")
        
        self.txt_display = cst.CTkTextbox(self, fg_color="#171717", text_color="#ececf1", font=("Arial", 13), wrap="word")
        self.txt_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.txt_display.insert(tk.END, "🤖 Torvarcore: النظام جاهز ومستقر بذكاء البرو الصارم.\n\n")
        self.txt_display.configure(state="disabled")
        
        self.entry = cst.CTkEntry(self, placeholder_text="اكتب سؤالك هنا...", fg_color="#2f2f2f", text_color="#ececf1")
        self.entry.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.btn_send = cst.CTkButton(self, text="إرسال الطلب حياً", font=("Arial", 12, "bold"), command=self.start_ask_thread)
        self.btn_send.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.entry.bind("<Return>", lambda event: self.start_ask_thread())

    def start_ask_thread(self):
        threading.Thread(target=self.send_to_gemini, daemon=True).start()

    def send_to_gemini(self):
        user_text = self.entry.get()
        if not user_text: return
        
        self.txt_display.configure(state="normal")
        self.txt_display.insert(tk.END, f"👤 المستخدم: {user_text}\n\n")
        self.txt_display.configure(state="disabled")
        self.txt_display.see(tk.END)
        
        self.entry.delete(0, tk.END)
        self.btn_send.configure(state="disabled", text="جاري المعالجة الحية...")
        
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=user_text,
        )
        self.show_response(f"🤖 Torvarcore:\n{response.text}\n" + "_" * 50 + "\n\n")

    def show_response(self, text):
        self.txt_display.configure(state="normal")
        self.txt_display.insert(tk.END, text)
        self.txt_display.configure(state="disabled")
        self.txt_display.see(tk.END)
        self.btn_send.configure(state="normal", text="إرسال الطلب حياً")

if __name__ == "__main__":
    app = TorvarcoreFinalShell()
    app.mainloop()
