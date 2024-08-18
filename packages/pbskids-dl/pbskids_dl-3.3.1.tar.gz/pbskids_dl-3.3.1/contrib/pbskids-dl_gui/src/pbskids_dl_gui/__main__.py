#!/usr/bin/env python3
#   Copyright 2024 The pbskids-dl team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

pbskids_dl_version = '3.3.0'
import sys

try:
    import tkinter, tkinter.messagebox
    from tkinter import ttk
    import threading
    import urllib.request, urllib.error, urllib
    import bs4
    import json
except:
    print("pbskids-dl gui needs these modules:\n\ttkinter, json, threading, urllib (urllib3), and BeautifulSoup4 (bs4)")
    sys.exit(128)

def errorquit(exitmessage, exitcode, errorcode):
    pbskidsdl_errorone = "ERROR: " + str(exitmessage)
    pbskidsdl_errortwo = "Error code: " + str(errorcode)
    pbskidsdl_errorthree = "Possible causes: Bad internet or script killed"
    pbksidsdl_fullerror = str(pbskidsdl_errorone + "\n" + pbskidsdl_errortwo + "\n" + pbskidsdl_errorthree)
    print(pbskidsdl_errorone, file=sys.stderr)
    print(pbskidsdl_errortwo, file=sys.stderr)
    print(pbskidsdl_errorthree, file=sys.stderr)
    tkinter.messagebox.showinfo(title='Error!',message=pbksidsdl_fullerror)
    root.destroy()
    sys.exit(int(exitcode))

def fetch_script(link: str):
    try:
        response = urllib.request.urlopen(link)
        webContent = response.read().decode('UTF-8')
        soup = bs4.BeautifulSoup(webContent, features="lxml")
        check_drm(soup)
        script = soup.find('script', type='application/json').text
    except:
        nofoundurl = str('The \"' + link + '\" link failed to load properly. Is it a PBS KIDS Video link?')
        errorquit(nofoundurl, "1", "1")
    return script

def check_drm(soup):
    isdrm = soup.find('\"drm_enabled\":true')
    if str(isdrm) != "None":
        errorquit("DRM Content is not available in pbskids-dl", "1", "4")

def find_assets(script):
    try:
        data = json.loads(script)
        assets = data['props']['pageProps']['videoData']['mediaManagerAsset']
        videos = assets['videos']
    except:
        message='ERROR: The video was not found! Is the link a PBS KIDS Video link?'
        errorquit(message, "1", "2")
    return assets,videos

def download_status(count, data_size, total_data):
    if count == 0:
        # Set the maximum value for the progress bar.
        progressbar.configure(maximum=total_data)
    else:
        # Increase the progress.
        progressbar.step(data_size)

def download_video(*args):
    global progressbar

    link = url.get()
    script = fetch_script(link)
    assets, videos = find_assets(script)
    vid_title = assets['title'].replace('/','+').replace('\\','+') + '.mp4'
    file_name = ttk.Label(mainframe, text='Video file name: ' + vid_title)
    file_name.grid(column=1, row=3, sticky=tkinter.W)
    for video in videos:
        if (video['profile'] == 'mp4-16x9-baseline'):
            realvid = video['url']
            progressbar = ttk.Progressbar(mainframe)
            progressbar.grid(column=1,row=2, sticky=(tkinter.W, tkinter.E))
            download_button['state']= tkinter.DISABLED
            urllib.request.urlretrieve(realvid, vid_title, download_status)
            urllib.request.urlcleanup()
            progressbar.grid_remove()
            break
    download_button['state']= tkinter.NORMAL
    tkinter.messagebox.showinfo(title='Completed!',message='The operation completed.')
    file_name.grid_remove()
    
def download_button_clicked(*args):
    downloading = threading.Thread(target=download_video)
    downloading.daemon = True
    downloading.start()
    
def main():
    global root
    global mainframe
    global download_button
    global url

    root = tkinter.Tk()
    root.title('pbskids-dl gui ' + pbskids_dl_version)
    
    mainframe = tkinter.ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text='Enter a URL:').grid(column=1, row=1, sticky=tkinter.W)
    url = tkinter.StringVar()
    url_entry = ttk.Entry(mainframe, width=40, textvariable=url)
    url_entry.grid(column=1, row=2, sticky=(tkinter.W, tkinter.E))

    download_button = ttk.Button(mainframe, text='Download', command=download_button_clicked)
    download_button.grid(column=2, row=2, sticky=tkinter.W)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    url_entry.focus()
    root.bind('<Return>', download_button_clicked)

    root.mainloop()

if __name__ == "__main__":
    main()
    sys.exit(0)
