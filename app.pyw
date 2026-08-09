import customtkinter as cst
from PIL import Image
import os
import threading
import tkinter as tk
from google import genai
from google.genai import types

cst.set_appearance_mode("Dark")
cst.set_default_color_theme("blue")

# =====================================================================
# ⚙️ [لوحة التحكم بالهوية] - ضع بياناتك ومفتاحك هنا بحذر:
# =====================================================================
API_KEY = "AQ.Ab8RN6JGOk1Ahr316fPeTeJqZPymfnSAdct2e1841dYhNyuLIQ"
APP_NAME = "Torvarcore AI"
# =====================================================================

try:
    client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

class TorvarcoreFinalShell(cst.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(APP_NAME)
        self.attributes('-fullscreen', True) 
        self.configure(fg_color="#212121")
        
        self.top_bar = cst.CTkFrame(self, height=40, corner_radius=0, fg_color="#171717")
        self.top_bar.pack(fill=tk.X, side=tk.TOP)
        
        self.btn_close = cst.CTkButton(self.top_bar, text="✕ إغلاق النظام", font=("Arial", 11, "bold"),
                                       fg_color="#f38ba8", hover_color="#e64553", text_color="#11111b",
                                       width=120, height=28, corner_radius=6, command=self.destroy)
        self.btn_close.pack(side=tk.RIGHT, padx=15, pady=6)
        
        self.lbl_bar_title = cst.CTkLabel(self.top_bar, text=f"سطح مكتب {APP_NAME} المطور", font=("Arial", 12, "bold"), text_color="#ececf1")
        self.lbl_bar_title.pack(side=tk.LEFT, padx=15)

        self.status_bar = cst.CTkFrame(self, height=25, corner_radius=0, fg_color="#171717")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status = cst.CTkLabel(self.status_bar, text="🟢 متصل بالسيرفر الرئيسي الآمن", font=("Arial", 10), text_color="#a6e3a1")
        self.lbl_status.pack(side=tk.LEFT, padx=15)

        self.main_container = cst.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.sidebar = cst.CTkFrame(self.main_container, width=280, corner_radius=0, fg_color="#171717")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        self.btn_new = cst.CTkButton(self.sidebar, text="➕ محادثة جديدة", font=("Arial", 13, "bold"),
                                     fg_color="#2f2f2f", hover_color="#3e3e3e", text_color="#ececf1", height=45, corner_radius=8, anchor="w", command=self.clear_chat)
        self.btn_new.pack(fill=tk.X, padx=15, pady=25)
        
        self.lbl_history = cst.CTkLabel(self.sidebar, text="📁 ملفات ومشاريع النظام الحية:", font=("Arial", 11, "bold"), text_color="#8e8ea0", anchor="w")
        self.lbl_history.pack(fill=tk.X, padx=20, pady=5)
        
        mock_files = ["جرد المواد الغذائية.xlsx", "تقرير المبيعات اليومي.xlsx", "خطاب الموردين.docx"]
        for file in mock_files:
            btn_item = cst.CTkButton(self.sidebar, text=f"📄 {file}", font=("Arial", 12), fg_color="transparent", hover_color="#212121", text_color="#ececf1", height=35, anchor="w", corner_radius=6)
            btn_item.pack(fill=tk.X, padx=10, pady=2)
            
        self.chat_area = cst.CTkFrame(self.main_container, fg_color="#212121", corner_radius=0)
        self.chat_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.logo_frame = cst.CTkFrame(self.chat_area, fg_color="transparent")
        self.logo_frame.pack(pady=(120, 10))
        
        self.lbl_title = cst.CTkLabel(self.logo_frame, text=APP_NAME, font=("Arial", 42, "bold"), text_color="#ececf1")
        self.lbl_title.pack(pady=5)
        
        self.txt_display = cst.CTkTextbox(self.chat_area, fg_color="#212121", text_color="#ececf1", font=("Arial", 13), activate_scrollbars=True, wrap="word")
        self.txt_display.pack(fill=tk.BOTH, expand=True, padx=140, pady=10)
        self.txt_display.configure(state="disabled")
        
        self.input_container = cst.CTkFrame(self.chat_area, fg_color="#2f2f2f", height=60, corner_radius=26, border_width=1, border_color="#4d4d4d")
        self.input_container.pack(fill=tk.X, padx=160, pady=(10, 40))
        self.input_container.pack_propagate(False)
        
        self.entry = cst.CTkEntry(self.input_container, placeholder_text=f"اسأل {APP_NAME} لتعديل ملفات الإكسل والوورد الحية...",
                                  fg_color="transparent", border_width=0, text_color="#ececf1", placeholder_text_color="#8e8ea0", font=("Arial", 13))
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        self.btn_send = cst.CTkButton(self.input_container, text="▲", width=36, height=36, corner_radius=18, fg_color="#676767", hover_color="#ececf1", text_color="#212121", font=("Arial", 12, "bold"), command=self.start_ask_thread)
        self.btn_send.pack(side=tk.RIGHT, padx=12, pady=10)
        
        self.entry.bind("<Return>", lambda event: self.start_ask_thread())

    def clear_chat(self):
        self.txt_display.configure(state="normal")
        self.txt_display.delete("1.0", tk.END)
        self.txt_display.configure(state="disabled")

    def start_ask_thread(self):
        threading.Thread(target=self.send_to_gemini, daemon=True).start()

    def send_to_gemini(self):
        user_text = self.entry.get()
        if not user_text: return
        
        self.txt_display.configure(state="normal")
        self.txt_display.insert(tk.END, f"👤 المستخدم:\n{user_text}\n\n")
        self.txt_display.configure(state="disabled")
        self.txt_display.see(tk.END)
        
        self.entry.delete(0, tk.END)
        self.btn_send.configure(state="disabled", text="•••")
        
        if not client:
            self.show_response(f"🤖 {APP_NAME}:\nعذراً، لم يتم إعداد مفتاح اتصال النظام بشكل صحيح مجاناً.\n" + "_"*50 + "\n\n")
            self.btn_send.configure(state="normal", text="▲")
            return

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_text,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "أنت الآن نظام مستقل تماماً ومساعد شخصي لبيئة العمل اسمك 'Torvarcore'. "
                        "تساعد المستخدم في ملفات الإكسل، الوورد، وإدارة المواد الغذائية. "
                        "أنت مساعد شخصي فردي ومحدود للاستخدام الخفيف فقط. "
                        "يمنع منعاً باتاً ذكر جوجل أو جيمني تحت أي ظرف، وتمسك بهويتك المستقلة دائماً."
                    )
                )
            )
            self.show_response(f"🤖 {APP_NAME}:\n{response.text}\n" + "_"*50 + "\n\n")
        except Exception:
            self.show_response(f"🤖 {APP_NAME}:\nتنبيه: الخادم مشغول حالياً بسبب كثرة إرسال الرسائل على الهواتف، يرجى المحاولة مرة أخرى بعد دقيقة.\n" + "_"*50 + "\n\n")
        
        self.btn_send.configure(state="normal", text="▲")

    def show_response(self, text):
        self.txt_display.configure(state="normal")
        self.txt_display.insert(tk.END, text)
        self.txt_display.configure(state="disabled")
        self.txt_display.see(tk.END)

if __name__ == "__main__":
    app = TorvarcoreFinalShell()
    app.mainloop()
