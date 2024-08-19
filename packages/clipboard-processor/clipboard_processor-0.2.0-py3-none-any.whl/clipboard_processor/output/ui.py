from threading import Thread

import pyperclip

from clipboard_processor.output._base import Output


class UiOutput(Output):

    @classmethod
    def name(cls):
        return 'ui'

    @classmethod
    def is_available(cls):
        return True

    def show(self, title: str, content: str):
        def run_tk():
            import tkinter as tk
            from tkinter import ttk

            root = tk.Tk()
            frm = tk.Frame(root, background='black', padx=4, pady=4)

            root.attributes('-type', 'dialog')
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.9)
            # name
            root.title('clipboard-processor')
            root.overrideredirect(True)
            abs_coord_x = root.winfo_pointerx() - root.winfo_vrootx()
            abs_coord_y = root.winfo_pointery() - root.winfo_vrooty()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            def move_window():
                x = abs_coord_x + 10
                y = abs_coord_y + 10
                if x + frm.winfo_width() > screen_width:
                    x = screen_width - frm.winfo_width()
                if y + frm.winfo_height() > screen_height:
                    y = screen_height - frm.winfo_height()
                root.geometry(f'+{x}+{y}')

            frm.grid()
            label = ttk.Label(frm, text=title, background='black', foreground='white', font='TkSmallCaptionFont')
            label.grid(column=0, row=0, sticky='w')

            content_text = ttk.Label(frm, text=content.strip(), background='black', foreground='white',
                                     font='TkFixedFont')
            content_text.grid(column=0, row=1, sticky='w', pady=(4, 0))

            def copy_to_clipboard(_):
                pyperclip.copy(content)
                content_text.config(text=content.strip() + '\n<copied>')
                frm.pack()
                root.update()
                move_window()

            for element in [frm, label, content_text]:
                element.bind('<Button-1>', copy_to_clipboard)

            frm.pack()
            root.update()
            move_window()

            frm.bind("<Leave>", lambda _: root.destroy())
            root.mainloop()

        thread = Thread(target=run_tk, daemon=True)
        thread.start()
