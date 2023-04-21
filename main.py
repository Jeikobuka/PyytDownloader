from pytube import YouTube
from datetime import datetime

import threading, subprocess, time
from moviepy.editor import *

import tkinter as tk
import customtkinter as ctk

DOWNLOADS_FOLDER = "Downloads\\"
downloadStartTime = datetime.now()

def timeToSeconds(t):
    tSplit = t.split(":")
    minutesToSeconds = float(tSplit[0]) * 60.0
    totalSeconds = float(tSplit[1]) + minutesToSeconds
    return totalSeconds

def downloadCallback(stream, chunk, bytesRemaining):
    global downloadStartTime
    secondsSinceDownloadStart = (datetime.now()-downloadStartTime).total_seconds()
    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytesRemaining
    percentCompleted = round(bytesDownloaded / totalSize * 100)
    speed = round(((bytesDownloaded / 1024) / 1024) / secondsSinceDownloadStart, 2)    
    secondsLeft = round(round(((bytesRemaining / 1024) / 1024) / float(speed), 2))
    percentCompletedBar.set(percentCompleted/100)
    secondsLeftLabel.configure(text=f"Seconds Left: {secondsLeft}")

def download(link):
    global downloadStartTime, t
    if link.strip() == "":
        return print("Nothing to download.")
    print("Downloading...")
    percentCompletedBar.set(0)
    secondsLeftLabel.configure(text="Seconds Left: 0")
    yt = YouTube(link)
    stream = yt.streams.filter(only_audio=False, only_video=False, progressive=True, res="720p").first()
    print(stream)
    yt.register_on_progress_callback(downloadCallback)
    downloadStartTime = datetime.now()
    title = yt.title.replace('|', "")
    download = stream.download(DOWNLOADS_FOLDER, f"{title}.mp4")
    print(download)
    print("Download Complete.")
    startFrom = 0
    endAt = yt.length
    if startFromEntry.get().strip() == "" and endAtEntry.get().strip() == "":
        return
    if endAtEntry.get().strip() != "":
        endAt = timeToSeconds(endAtEntry.get().strip())
    if startFromEntry.get().strip != "":
        startFrom = timeToSeconds(startFromEntry.get().strip())
    vPath = DOWNLOADS_FOLDER+f"{title}.mp4"
    p = subprocess.Popen('./main.py',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, errors = p.communicate()
    print(output)
    v = VideoFileClip(vPath).subclip(startFrom, endAt)
    v.write_videofile(f"{vPath}-.mp4", fps=60)
    v.close()
    os.remove(f"{vPath}.mp4")
    os.rename(f"{vPath}-.mp4", f"{vPath}.mp4")

def getDownload(link):
    global t
    t = threading.Thread(target=download, args=(link, ))
    t.start()

def openThis():
    print("done")
    cwd = os.getcwd()
    subprocess.Popen(rf'explorer /select,"'+cwd+'\\Downloads\\"')

global root, themeDropdown
ctk.set_default_color_theme("themes/Redline.json")
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("500x275")
root.title("YT Vid Downloader")
tabview = ctk.CTkTabview(root)

downloaderTab = tabview.add("Downloader")
tabview.pack()

downloaderFrame = ctk.CTkFrame(master=downloaderTab)
downloaderFrame.pack(pady=20,padx=20, fill="both", expand=True)

downloadLinkEntry = ctk.CTkEntry(master=downloaderFrame, font=("Roboto", 16, "bold"), width=200,height=25,corner_radius=10)
downloadLinkEntry.grid(row=1, column=1, padx=10, pady=10, stick="W")

downloadButton = ctk.CTkButton(master=downloaderFrame, text="Download", font=("Roboto", 16, "bold"), width=40, command = lambda : getDownload(downloadLinkEntry.get().strip()))
downloadButton.grid(row=1, column=2, padx=10, pady=10, columnspan=2)

percentCompletedBar = ctk.CTkProgressBar(master=downloaderFrame, width=150)
percentCompletedBar.grid(row=2, column=1, padx=10, pady=5)
percentCompletedBar.set(0)

openDownloadsButton = ctk.CTkButton(master=downloaderFrame, text="Open Downloads", font=("Roboto", 16, "bold"), width=100, command = openThis)
openDownloadsButton.grid(row=3, column=1, padx=10, pady=5)

secondsLeftLabel = ctk.CTkLabel(master=downloaderFrame, text="Seconds Left: ", font=("Roboto", 16, "bold"))
secondsLeftLabel.grid(row=4, column=1, padx=10, pady=5)
secondsLeftLabel.configure(text="")

startFromLabel = ctk.CTkLabel(master=downloaderFrame, text="Start from: ", font=("Roboto", 16, "bold"))
startFromLabel.grid(row=2, column=2, padx=5, pady=5)
startFromEntry = ctk.CTkEntry(master=downloaderFrame, width=40)
startFromEntry.grid(row=2, column=3, padx=10, pady=5)

endAtLabel = ctk.CTkLabel(master=downloaderFrame, text="End at: ", font=("Roboto", 16, "bold"))
endAtLabel.grid(row=3, column=2, padx=5, pady=5)
endAtEntry = ctk.CTkEntry(master=downloaderFrame, width=40)
endAtEntry.grid(row=3, column=3, padx=10, pady=5)

root.mainloop()