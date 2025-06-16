import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    import docx
except ImportError:
    docx = None

class ReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title('My Reader')
        self.text = ''
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.current_voice = self.voices[0].id if self.voices else None
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, bg='#111')
        frame.pack(fill='both', expand=True)

        ctrl = tk.Frame(frame, bg='#111')
        ctrl.pack(pady=5)

        open_btn = tk.Button(ctrl, text='Open File', command=self.open_file)
        open_btn.pack(side='left', padx=2)

        self.voice_var = tk.StringVar(value=self.current_voice)
        voice_menu = tk.OptionMenu(ctrl, self.voice_var, *[v.id for v in self.voices])
        voice_menu.pack(side='left', padx=2)

        play_btn = tk.Button(ctrl, text='Play', command=self.play)
        play_btn.pack(side='left', padx=2)

        stop_btn = tk.Button(ctrl, text='Stop', command=self.stop)
        stop_btn.pack(side='left', padx=2)

        self.textbox = tk.Text(frame, bg='#222', fg='#eee', insertbackground='white')
        self.textbox.pack(fill='both', expand=True, padx=5, pady=5)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('Documents', '*.txt *.pdf *.docx')])
        if not path:
            return
        p = Path(path)
        try:
            if p.suffix == '.txt':
                self.text = Path(path).read_text(encoding='utf-8')
            elif p.suffix == '.pdf' and PyPDF2:
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    self.text = '\n'.join(page.extract_text() or '' for page in reader.pages)
            elif p.suffix == '.docx' and docx:
                document = docx.Document(path)
                self.text = '\n'.join(p.text for p in document.paragraphs)
            else:
                messagebox.showerror('Error', 'Unsupported format or missing dependencies')
                return
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, self.text)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def play(self):
        if not self.text:
            return
        self.engine.stop()
        self.engine.setProperty('voice', self.voice_var.get())
        self.engine.say(self.text)
        self.engine.runAndWait()

    def stop(self):
        self.engine.stop()

if __name__ == '__main__':
    root = tk.Tk()
    app = ReaderApp(root)
    root.mainloop()
