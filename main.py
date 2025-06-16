import tkinter as tk
from tkinter import filedialog, ttk
import threading
import pyttsx3
from pathlib import Path
from PyPDF2 import PdfReader
import docx

class ReaderApp:
    def __init__(self, root):
        self.root = root
        root.title("My Reader")
        root.geometry("800x600")

        self.engine = pyttsx3.init()
        self.engine.connect('started-word', self.on_started_word)

        self.text_content = ''
        self.voice_map = {v.name: v.id for v in self.engine.getProperty('voices')}

        controls = tk.Frame(root)
        controls.pack(fill='x')

        tk.Button(controls, text="Open File", command=self.open_file).pack(side='left')

        self.voice_var = tk.StringVar()
        voice_names = list(self.voice_map.keys())
        ttk.Combobox(controls, textvariable=self.voice_var, values=voice_names, width=20).pack(side='left')
        if voice_names:
            self.voice_var.set(voice_names[0])

        self.rate_var = tk.IntVar(value=self.engine.getProperty('rate'))
        tk.Scale(controls, from_=100, to=300, orient='horizontal', label='Rate',
                 variable=self.rate_var).pack(side='left')

        tk.Button(controls, text="Play", command=self.play).pack(side='left')
        tk.Button(controls, text="Stop", command=self.stop).pack(side='left')

        self.text = tk.Text(root, wrap='word', state='disabled')
        self.text.pack(fill='both', expand=True)
        self.text.tag_config('highlight', background='yellow')

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('Documents', '*.txt *.pdf *.docx')])
        if not path:
            return
        path = Path(path)
        if path.suffix == '.txt':
            text = path.read_text(encoding='utf-8')
        elif path.suffix == '.pdf':
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or '' for page in reader.pages)
        elif path.suffix == '.docx':
            doc = docx.Document(str(path))
            text = "\n".join(p.text for p in doc.paragraphs)
        else:
            text = ''
        self.text_content = text
        self.text.configure(state='normal')
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', text)
        self.text.configure(state='disabled')
        self.clear_highlight()

    def play(self):
        if not self.text_content:
            return
        self.stop()
        self.engine.setProperty('voice', self.voice_map.get(self.voice_var.get()))
        self.engine.setProperty('rate', self.rate_var.get())
        self.engine.say(self.text_content)
        threading.Thread(target=self.engine.runAndWait, daemon=True).start()

    def stop(self):
        self.engine.stop()
        self.clear_highlight()

    def on_started_word(self, name, location, length):
        def highlight():
            self.text.configure(state='normal')
            self.clear_highlight()
            start = f'1.0+{location}c'
            end = f'1.0+{location+length}c'
            self.text.tag_add('highlight', start, end)
            self.text.see(start)
            self.text.configure(state='disabled')
        self.root.after(0, highlight)

    def clear_highlight(self):
        self.text.tag_remove('highlight', '1.0', 'end')

if __name__ == '__main__':
    root = tk.Tk()
    ReaderApp(root)
    root.mainloop()
