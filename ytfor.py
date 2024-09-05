import tkinter as tk
import subprocess
import sys

root = tk.Tk()
root.title('video downloader for Finette')
root.geometry('1120x300+20+20')
options = {'padx': 5, 'pady': 5}
outpath='/tmp/'
ffmpeg_path='/sbin/ffmpeg'


class TextEx(tk.Text):
    """
    Extended entry widget that includes a context menu
    with Copy, Cut and Paste commands.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Copy", command=self.popup_copy)
        self.menu.add_command(label="Cut", command=self.popup_cut)
        self.menu.add_separator()
        self.menu.add_command(label="Paste", command=self.popup_paste)
        self.bind("<Button-3>", self.display_popup)

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def popup_copy(self):
        self.event_generate("<<Copy>>")

    def popup_cut(self):
        self.event_generate("<<Cut>>")

    def popup_paste(self):
        self.event_generate("<<Paste>>")

frame = tk.Frame(root)

#Boutton to quit the app
quit_button = tk.Button(frame, text="Quit", command=root.destroy)
quit_button.grid(column=2, row=0, sticky='W', **options)

url_label = tk.Label(frame, text='URL')
url_label.grid(column=0, row=1, sticky='W', **options)

# url entry
url = tk.StringVar()
url_entry = tk.Entry(frame, width=128, textvariable=url)
url_entry.grid(column=1, row=1, **options)
url_entry.focus()

#Download function
def download_url(url) -> None:
    """ Download the video given as arg with yt-dlp
    """
    cmd=['yt-dlp', '--ffmpeg-location', f'{ffmpeg_path}', '--force-overwrites', '-P', f'{outpath}',  '-o', '%(title)s.%(ext)s', f'{url}']
    cmd_str=' '.join(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status_text.insert(tk.INSERT, cmd_str)
    while process.poll() is None:
        output=process.stdout.read(32) #read 64 bytes 
        output=output.replace(b'\r',b'\n').decode()
        sys.stdout.write(output)
        status_text.insert(tk.INSERT, output)
        status_text.see(tk.END)
        root.update_idletasks()


# download button click
def download_button_clicked():
    try:
        u = url.get()
        r = download_url(u)
    except ValueError as error:
        showerror(title='Error', message=error)

#clipboard button
def clip_button_clicked():
    try:
        u = root.clipboard_get()
        url.set(u)
        root.update_idletasks()
    except ValueError as error:
        showerror(title='Error', message=error)

# download button
download_button = tk.Button(frame, text='Download')
download_button.grid(column=1, row=0, sticky='W', **options)
download_button.configure(command=download_button_clicked)

# get clipboard button
clip_button = tk.Button(frame, text='Clipboard')
clip_button.grid(column=0, row=0, sticky='W', **options)
clip_button.configure(command=clip_button_clicked)

# status label
#status = tk.StringVar()
#status_label = tk.Entry(frame, textvariable=status, justify=tk.LEFT, state=tk.DISABLED)
status_text = TextEx(frame, heigh=10, width=128, wrap=tk.WORD) #, state=tk.DISABLED)
status_text.grid(row=2, columnspan=10, **options)
#status_label.grid(row=2, **options)



frame.grid(padx=10, pady=10)

root.mainloop()

