import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("650x550")
        self.root.minsize(600, 450)

        # 1. Предопределённый список цитат
        self.quotes = [
            {"text": "Жизнь — это то, что случается с тобой, пока ты строишь другие планы.", "author": "Джон Леннон", "topic": "жизнь"},
            {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "успех"},
            {"text": "Всё, что вы можете вообразить — реально.", "author": "Пабло Пикассо", "topic": "творчество"},
            {"text": "Простота — высшая форма изысканности.", "author": "Леонардо да Винчи", "topic": "искусство"},
            {"text": "Образование — самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "образование"}
        ]
        self.history = []
        self.json_file = "quotes_history.json"

        self.setup_ui()
        self.load_history()
        self.update_filter_options()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Отображение текущей цитаты
        self.quote_label = ttk.Label(main_frame, text="Нажмите кнопку, чтобы сгенерировать цитату",
                                     wraplength=580, justify=tk.CENTER, font=("Segoe UI", 12, "bold"))
        self.quote_label.pack(pady=10)

        # 2. Кнопка генерации
        self.gen_btn = ttk.Button(main_frame, text="🎲 Сгенерировать цитату", command=self.generate_quote)
        self.gen_btn.pack(pady=5)

        # 4. Фильтрация истории
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтр истории", padding=5)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.author_var = tk.StringVar()
        self.author_combo = ttk.Combobox(filter_frame, textvariable=self.author_var, state="readonly", width=20)
        self.author_combo.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.topic_var = tk.StringVar()
        self.topic_combo = ttk.Combobox(filter_frame, textvariable=self.topic_var, state="readonly", width=20)
        self.topic_combo.grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Применить", command=self.apply_filter).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сброс", command=self.reset_filter).grid(row=0, column=5, padx=5)

        # 3. История сгенерированных цитат
        ttk.Label(main_frame, text="История:").pack(anchor=tk.W, pady=(5, 0))
        self.history_listbox = tk.Listbox(main_frame, height=8, font=("Segoe UI", 10))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Добавление новой цитаты
        add_frame = ttk.LabelFrame(main_frame, text="Добавить новую цитату", padding=5)
        add_frame.pack(fill=tk.X, pady=5)

        ttk.Label(add_frame, text="Текст:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.new_text_entry = ttk.Entry(add_frame, width=45)
        self.new_text_entry.grid(row=0, column=1, padx=5)

        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5, sticky=tk.W)
        self.new_author_entry = ttk.Entry(add_frame, width=20)
        self.new_author_entry.grid(row=1, column=1, padx=5, sticky=tk.W)

        ttk.Label(add_frame, text="Тема:").grid(row=2, column=0, padx=5, sticky=tk.W)
        self.new_topic_entry = ttk.Entry(add_frame, width=20)
        self.new_topic_entry.grid(row=2, column=1, padx=5, sticky=tk.W)

        ttk.Button(add_frame, text="➕ Добавить", command=self.add_new_quote).grid(row=3, column=0, columnspan=2, pady=5)

        # Кнопки сохранения/загрузки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="💾 Сохранить историю", command=self.save_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📂 Загрузить историю", command=self.load_history).pack(side=tk.LEFT, padx=5)

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Внимание", "Список цитат пуст!")
            return
        quote = random.choice(self.quotes)
        self.history.append(quote)
        self.update_display(quote)
        self.update_history_list()
        self.update_filter_options()

    def update_display(self, quote):
        self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]} [{quote["topic"].capitalize()}]')

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for i, q in enumerate(self.history, 1):
            self.history_listbox.insert(tk.END, f"{i}. {q['text'][:60]}{'...' if len(q['text'])>60 else ''} — {q['author']} ({q['topic']})")

    def add_new_quote(self):
        text = self.new_text_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()

        # 6. Проверка корректности ввода (пустые строки)
        if not text or not author or not topic:
            messagebox.showerror("Ошибка ввода", "Все поля (текст, автор, тема) должны быть заполнены!")
            return

        new_quote = {"text": text, "author": author, "topic": topic.lower()}
        self.quotes.append(new_quote)
        messagebox.showinfo("Успех", "Цитата успешно добавлена в коллекцию!")
        self.new_text_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)
        self.update_filter_options()

    def update_filter_options(self):
        authors = sorted(set(q["author"] for q in self.quotes))
        topics = sorted(set(q["topic"] for q in self.quotes))
        self.author_combo["values"] = ["Все"] + authors
        self.topic_combo["values"] = ["Все"] + topics
        self.author_var.set("Все")
        self.topic_var.set("Все")

    def apply_filter(self):
        author_f = self.author_var.get()
        topic_f = self.topic_var.get()

        filtered = self.history
        if author_f != "Все":
            filtered = [q for q in filtered if q["author"] == author_f]
        if topic_f != "Все":
            filtered = [q for q in filtered if q["topic"] == topic_f.lower()]

        self.history_listbox.delete(0, tk.END)
        for i, q in enumerate(filtered, 1):
            self.history_listbox.insert(tk.END, f"{i}. {q['text'][:60]}{'...' if len(q['text'])>60 else ''} — {q['author']} ({q['topic']})")

    def reset_filter(self):
        self.author_var.set("Все")
        self.topic_var.set("Все")
        self.update_history_list()

    # 5. Сохранение и загрузка истории в JSON
    def save_history(self):
        try:
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "История сохранена в quotes_history.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_history(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                self.update_history_list()
                messagebox.showinfo("Успех", "История загружена из файла!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
        else:
            self.history = []
            self.update_history_list()

    def on_closing(self):
        self.save_history()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGeneratorApp(root)
    root.mainloop()