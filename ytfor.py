import tkinter as tk
import subprocess

root = tk.Tk()
root.title('video downloader for Finette')
root.geometry('1280x150+20+20')
options = {'padx': 5, 'pady': 5}
outpath='/tmp/'
ffmpeg_path='/sbin/ffmpeg'

def download_url(url, status_label) -> None:
    """ Download the video given as arg with yt-dlp
    """
    cmd=['yt-dlp', '--ffmpeg-location', f'{ffmpeg_path}', '--force-overwrites', '-P', f'{outpath}',  '-o', '%(title)s.%(ext)s', f'{url}']
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output=process.stdout.readline()
    status_label.config(text=output)
    process.wait()

frame = tk.Frame(root)

#Boutton to quit the app
quit_button = tk.Button(frame, text="Quit", command=root.destroy)
quit_button.grid(column=0, row=0, sticky='W', **options)

url_label = tk.Label(frame, text='URL')
url_label.grid(column=0, row=1, sticky='W', **options)

# url entry
url = tk.StringVar()
url_entry = tk.Entry(frame, width=128, textvariable=url)
url_entry.grid(column=1, row=1, **options)
url_entry.focus()

# download button click
def download_button_clicked():
    try:
        u = url.get()
        r = download_url(u, status_label)        
    except ValueError as error:
        showerror(title='Error', message=error)

# download button
download_button = tk.Button(frame, text='Download')
download_button.grid(column=2, row=1, sticky='W', **options)
download_button.configure(command=download_button_clicked)

# status label
status_label = tk.Label(frame)
status_label.grid(row=2, columnspan=10, **options)

frame.grid(padx=10, pady=10)

root.mainloop()

