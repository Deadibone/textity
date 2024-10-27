import tkinter as tk
from tkinter import messagebox, font

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Textity")
        self.root.geometry("800x600")

        self.current_file = None

        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        self.format_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)

        self.input_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Input", menu=self.input_menu)

        self.kaomojis_menu = tk.Menu(self.input_menu, tearoff=0)
        self.input_menu.add_cascade(label="Kaomojis", menu=self.kaomojis_menu)

        kaomojis = ["(¬‿¬)", "( ͡° ͜ʖ ͡°)", "(╯°□°）╯︵ ┻━┻", "¯\_(ツ)_/¯", "(づ￣ ³￣)づ", "ಠ_ಠ", "(ง'̀-'́)ง", "ʕ•ᴥ•ʔ", "(⌐■_■)", "( ˶ˆᗜˆ˵ )", "( ｡ •̀ ᴖ •́ ｡)", "⛏", "?"]
        for kaomoji in kaomojis:
            self.kaomojis_menu.add_command(label=kaomoji, command=lambda k=kaomoji: self.insert_kaomoji(k))
           

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path

    def quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def undo(self):
        if self.text_area.edit_modified():
            self.text_area.edit_undo()

    def redo(self):
        if self.text_area.edit_modified():
            self.text_area.edit_redo()

    def find(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x100")

        find_label = tk.Label(find_window, text="Find:")
        find_label.pack()

        find_entry = tk.Entry(find_window)
        find_entry.pack()

        find_button = tk.Button(find_window, text="Find", command=lambda: self.find_text(find_entry.get()))
        find_button.pack()

    def find_text(self, query):
        start = self.text_area.search(query, "1.0", tk.END)
        if start:
            end = f"{start}+{len(query)}c"
            self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
            self.text_area.tag_add(tk.SEL, start, end)
            self.text_area.mark_set(tk.INSERT, end)
            self.text_area.see(tk.INSERT)

    def increase_font_size(self):
        current_font = font.Font(font=self.text_area["font"])
        size = current_font.cget("size")
        current_font.configure(size=size+2)
        self.text_area.configure(font=current_font)

    def decrease_font_size(self):
        current_font = font.Font(font=self.text_area["font"])
        size = current_font.cget("size")
        if size > 2:
            current_font.configure(size=size-2)
            self.text_area.configure(font=current_font)

    def run(self):
        self.root.mainloop()



    def insert_kaomoji(self, kaomoji):
        self.text_area.insert(tk.INSERT, kaomoji)

if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()