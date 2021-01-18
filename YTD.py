from tkinter import * # GUIS
from PIL import Image, ImageTk # Images and positons ... etc
from tkinter import messagebox # Messageboxes
from tkinter.filedialog import askdirectory # Get the path of the file
#from tkinter.ttk import Progressbar
import pytube # Download the vidoes
import pyperclip # Copy the https link
import re # Find patters
import threading # Threads
import webbrowser # Open to github
import os # Checking directories and files
#import time # Waiting a bit


download_link = None # Our download link
path = None # Our path to download to

root = Tk()
root.title('YtD')
root.iconbitmap('youtube-icon.ico')
root.geometry('600x400')
root.resizable(0,0)

# Make a function to detect if the clipboard has found a link
def link():
	global download_link

	link_re = re.compile(r'(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?')
	while True:
		clipboard = pyperclip.paste()
		if not link_entry.get():
			if link_re.findall(clipboard):
				link_entry.insert(0, clipboard)
				download_link = clipboard

# Start the thread of the link function
def start_link_thread():
	t = threading.Thread(target=link)
	t.setDaemon(True)
	t.start()


# Download the link
def download():
	global link_entry
	global download_link
	global path
	global video

	if download_link != None:
		if path != None:
			youtube = pytube.YouTube(download_link)
			video = youtube.streams.get_highest_resolution()

			pyperclip.copy('') # Get rid of the clipboard so the thread doesn't detect it

			link_entry.place_forget()
			link_entry = Entry(root, width=30, font=(None, 15), fg='purple')
			link_entry.place(x=180, y=240)

			download_link = None
			path = None
			tick_label.place_forget()

			# Download the video
			video.download()

			# When finished show a messagebox saying it's finished
			messagebox.showinfo('Done', 'The video has finished downloading!')
		else:
			messagebox.showerror('Invalid', 'No path specified')

	else:
		messagebox.showerror('Invalid', 'No link specified!')


# Save the path to where the user wants to save the file
def save_path():
	global path
	path = askdirectory()

	if not os.path.exists(path):
		path = None
		return

	os.chdir(path)
	tick_label.place(x=370, y=290)


# Start a download thread so it doesn't interrupt the GUI's mainloop which can causes glitches
def download_thread():
	t = threading.Thread(target=download)
	t.setDaemon(True)
	t.start()




# Set to the default background color
default_bg = '#%02x%02x%02x' % (240, 240, 237) # RGB Color
root.configure(bg=default_bg)


# Add the youtube picture
yt_img = Image.open('youtube.png')
yt_img = yt_img.resize((250,250), Image.ANTIALIAS)
yt_img = ImageTk.PhotoImage(yt_img)


# Add the version number / display it onto the screen
version_num = Label(root, text='V1.0', fg='purple', font=(None, 20))
version_num.place(x=60, y=105)


# Create the label and pack
yt_label = Label(root, image=yt_img)
yt_label.pack()


# Create the link label
link_label = Label(root, text='Link:', fg='blue', font=(None, 20))
link_label.place(x=100, y=230)


# Create the link entry
link_entry = Entry(root, width=30, font=(None, 15), fg='purple')
link_entry.place(x=180, y=240)


# Create save folder label
save_label = Label(root, text='Save:', fg='orange', font=(None, 20))
save_label.place(x=100, y=285)


# Create choose file button
save_button = Button(root, text='Choose Where To Save', fg='green', padx=10, pady=5, command=save_path)
save_button.place(x=180, y=290)


# Add the file image
file_img = Image.open('file.png')
file_img = file_img.resize((30,30), Image.ANTIALIAS)
file_img = ImageTk.PhotoImage(file_img)


# Create the file image label
file_label = Label(root, image=file_img)
file_label.place(x=335, y=290)


# Create a download button
download_button = Button(root, text='Download', fg='dark green', bg='lime', padx=118, font=(None, 15), command=download_thread)
download_button.place(x=180, y=340)


# Add the download image
download_img = Image.open('download.png')
download_img = download_img.resize((30,35), Image.ANTIALIAS)
download_img = ImageTk.PhotoImage(download_img)


# Create the label for download_img (must be in the download_button)
download_label = Label(root, image=download_img)
download_label.place(x=180, y=340)


# Add the tick mark image
tick_img = Image.open('tickmark.png')
tick_img = tick_img.resize((30,30), Image.ANTIALIAS)
tick_img = ImageTk.PhotoImage(tick_img)


# Create tick label
tick_label = Label(root, image=tick_img)


# Github button
github_url = 'https://www.github.com/m3r4j'
support_button = Button(root, text='GITHUB', fg='red', bg='black', padx=20, command=lambda: webbrowser.open(github_url), font=(None, 10))
support_button.place(x=480, y=20)


# Exit button
exit_button = Button(root, text='EXIT', fg='red', bg='black', padx=31, command=root.destroy, font=(None, 10))
exit_button.place(x=480, y=49)


# Top left youtube logo
logo_img = Image.open('youtube-icon.ico')
logo_img = logo_img.resize((60,60), Image.ANTIALIAS)
logo_img = ImageTk.PhotoImage(logo_img)


# Add to the screen
logo_label = Label(root, image=logo_img)
logo_label.place(x=50, y=20)


# Start the link thread which detects if your clipboard has a valid youtube link
start_link_thread()



root.mainloop()
