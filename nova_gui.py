import tkinter as tk
from tkinter import scrolledtext, ttk
import threading

from main import nova_process
from Modules.voice import listen
from nova_settings import load_settings, update_setting


class NOVAApp:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()

        self.root.title("NOVA — AI Desktop Assistant")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#0b1020")

        self.setup_style()
        self.build_header()
        self.build_chat()
        self.build_input()
        self.build_status()

        self.add_message(
            "NOVA",
            "NOVA is online. How can I help you?"
        )

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "NOVA.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(15, 9),
            background="#17213a",
            foreground="white",
            borderwidth=0
        )

        style.map(
            "NOVA.TButton",
            background=[
                ("active", "#243456")
            ]
        )

    def build_header(self):
        header = tk.Frame(
            self.root,
            bg="#11182b",
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(
            header,
            bg="#11182b"
        )
        left.pack(side="left", padx=25)

        title = tk.Label(
            left,
            text="NOVA",
            font=("Segoe UI", 25, "bold"),
            bg="#11182b",
            fg="#62c6ff"
        )
        title.pack(side="left", pady=17)

        subtitle = tk.Label(
            left,
            text="  AI Desktop Assistant",
            font=("Segoe UI", 10),
            bg="#11182b",
            fg="#8c98b3"
        )
        subtitle.pack(side="left", pady=25)

        self.status = tk.Label(
            header,
            text="● Online",
            font=("Segoe UI", 10, "bold"),
            bg="#11182b",
            fg="#55d98b"
        )
        self.status.pack(side="right", padx=20)

        settings_button = ttk.Button(
            header,
            text="⚙ Settings",
            style="NOVA.TButton",
            command=self.open_settings
        )
        settings_button.pack(
            side="right",
            padx=5,
            pady=15
        )

    def build_chat(self):
        chat_frame = tk.Frame(
            self.root,
            bg="#0b1020"
        )
        chat_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(20, 10)
        )

        self.chat = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 12),
            bg="#10182b",
            fg="#e8edf7",
            insertbackground="white",
            selectbackground="#28446d",
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=20,
            state="disabled"
        )

        self.chat.pack(
            fill="both",
            expand=True
        )

        self.chat.tag_config(
            "nova",
            foreground="#62c6ff",
            font=("Segoe UI", 12, "bold")
        )

        self.chat.tag_config(
            "user",
            foreground="#7ee2a8",
            font=("Segoe UI", 12, "bold")
        )

        self.chat.tag_config(
            "message",
            foreground="#e8edf7",
            font=("Segoe UI", 12)
        )

    def build_input(self):
        input_container = tk.Frame(
            self.root,
            bg="#0b1020"
        )
        input_container.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        input_box = tk.Frame(
            input_container,
            bg="#11182b"
        )
        input_box.pack(fill="x")

        self.entry = tk.Entry(
            input_box,
            font=("Segoe UI", 13),
            bg="#11182b",
            fg="white",
            insertbackground="white",
            relief="flat",
            borderwidth=0
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=13
        )

        self.entry.bind("<Return>", self.send)

        ttk.Button(
            input_box,
            text="Send",
            style="NOVA.TButton",
            command=self.send
        ).pack(
            side="right",
            padx=5,
            pady=5
        )

        ttk.Button(
            input_box,
            text="🎤 Voice",
            style="NOVA.TButton",
            command=self.voice
        ).pack(
            side="right",
            padx=5,
            pady=5
        )

    def build_status(self):
        status_bar = tk.Frame(
            self.root,
            bg="#080d19",
            height=28
        )

        status_bar.pack(
            fill="x",
            side="bottom"
        )

        status_bar.pack_propagate(False)

        tk.Label(
            status_bar,
            text="NOVA • OpenJarvis + Ollama • Local AI",
            font=("Segoe UI", 9),
            bg="#080d19",
            fg="#68748d"
        ).pack(
            side="left",
            padx=15
        )

    def add_message(self, sender, message):
        self.chat.config(state="normal")

        if sender == "NOVA":
            self.chat.insert(
                tk.END,
                "NOVA\n",
                "nova"
            )
        else:
            self.chat.insert(
                tk.END,
                "You\n",
                "user"
            )

        self.chat.insert(
            tk.END,
            str(message) + "\n\n",
            "message"
        )

        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def send(self, event=None):
        command = self.entry.get().strip()

        if not command:
            return

        self.entry.delete(0, tk.END)

        self.add_message(
            "You",
            command
        )

        threading.Thread(
            target=self.process,
            args=(command,),
            daemon=True
        ).start()

    def process(self, command):
        self.set_status("● Thinking...")

        try:
            result = nova_process(command)

            self.root.after(
                0,
                lambda: self.add_message(
                    "NOVA",
                    result
                )
            )

        except Exception as error:
            self.root.after(
                0,
                lambda: self.add_message(
                    "NOVA",
                    "Error: " + str(error)
                )
            )

        self.set_status("● Online")

    def voice(self):
        threading.Thread(
            target=self.process_voice,
            daemon=True
        ).start()

    def process_voice(self):
        self.set_status("● Listening...")

        try:
            command = listen()

            if command:
                self.root.after(
                    0,
                    lambda: self.add_message(
                        "You",
                        command
                    )
                )

                self.set_status("● Thinking...")

                result = nova_process(command)

                self.root.after(
                    0,
                    lambda: self.add_message(
                        "NOVA",
                        result
                    )
                )

        except Exception as error:
            self.root.after(
                0,
                lambda: self.add_message(
                    "NOVA",
                    "Voice error: " + str(error)
                )
            )

        self.set_status("● Online")

    def open_settings(self):
        settings = tk.Toplevel(self.root)

        settings.title("NOVA Settings")
        settings.geometry("500x470")
        settings.resizable(False, False)
        settings.configure(bg="#0b1020")

        tk.Label(
            settings,
            text="NOVA Settings",
            font=("Segoe UI", 22, "bold"),
            bg="#0b1020",
            fg="#62c6ff"
        ).pack(pady=(25, 5))

        tk.Label(
            settings,
            text="Assistant Configuration",
            font=("Segoe UI", 10),
            bg="#0b1020",
            fg="#8c98b3"
        ).pack(pady=(0, 20))

        panel = tk.Frame(
            settings,
            bg="#11182b"
        )
        panel.pack(
            fill="x",
            padx=25
        )

        tk.Label(
            panel,
            text="AI Engine",
            font=("Segoe UI", 11, "bold"),
            bg="#11182b",
            fg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 2)
        )

        tk.Label(
            panel,
            text=self.settings["ai_engine"],
            font=("Segoe UI", 10),
            bg="#11182b",
            fg="#62c6ff"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        voice_var = tk.BooleanVar(
            value=self.settings["voice_enabled"]
        )

        memory_var = tk.BooleanVar(
            value=self.settings["memory_enabled"]
        )

        security_var = tk.BooleanVar(
            value=self.settings["security_enabled"]
        )

        tk.Checkbutton(
            panel,
            text="Voice Enabled",
            variable=voice_var,
            font=("Segoe UI", 11),
            bg="#11182b",
            fg="white",
            selectcolor="#17213a",
            activebackground="#11182b",
            activeforeground="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=7
        )

        tk.Checkbutton(
            panel,
            text="Memory Enabled",
            variable=memory_var,
            font=("Segoe UI", 11),
            bg="#11182b",
            fg="white",
            selectcolor="#17213a",
            activebackground="#11182b",
            activeforeground="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=7
        )

        tk.Checkbutton(
            panel,
            text="Owner Security Enabled",
            variable=security_var,
            font=("Segoe UI", 11),
            bg="#11182b",
            fg="white",
            selectcolor="#17213a",
            activebackground="#11182b",
            activeforeground="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=7
        )

        def save():
            update_setting(
                "voice_enabled",
                voice_var.get()
            )

            update_setting(
                "memory_enabled",
                memory_var.get()
            )

            update_setting(
                "security_enabled",
                security_var.get()
            )

            self.settings = load_settings()
            settings.destroy()

        ttk.Button(
            settings,
            text="Save Settings",
            style="NOVA.TButton",
            command=save
        ).pack(pady=(25, 10))

        ttk.Button(
            settings,
            text="Close",
            style="NOVA.TButton",
            command=settings.destroy
        ).pack()

    def set_status(self, text):
        self.root.after(
            0,
            lambda: self.status.config(text=text)
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = NOVAApp(root)
    root.mainloop()