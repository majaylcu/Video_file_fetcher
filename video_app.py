import os
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading


from collections import defaultdict

def listDrives():
    dis = str(subprocess.getoutput("wmic logicaldisk get Caption"))
    dis = dis.replace("\n\n", ""); dis = " ".join(dis.split());
    dis = list(dis.split(' ')); dis.pop(0)
    return dis

def removingCdDrive():
    lis = listDrives()
    for i in lis:
        in1 = subprocess.getoutput("%s" % i)
        if in1 == "The device is not ready.":
            no = lis.index(i); lis.pop(no)
    return lis

def findingVideoFiles(list):
    file = os.getcwd() + "\\raw_out.txt"
    print(file)
    for i in list:
        os.chdir("%s\\" % i)
        os.system("dir *.3gp *.avi *.flv *.mkv *.mov *.mpg *.rm *.vob *.wmv *.mp4 /p /s >> %s" % file)
    return file

file = os.getcwd() + "\\raw_out.txt"

def processingProperVideoList(file):
    FH = open(file, 'r')
    # FW = open(os.getcwd() + "\\new.txt", 'w')
    list1 = FH.read().split("\n\n")
    # FW.write(str(list1))
    video_files = []
    for i in list1:
        if i.__contains__("Directory of"):
            dire = i.replace(" Directory of ", "")
            f = list1[list1.index(i)+1]; f = " ".join(f.split()); f = f.split(" ")
            # print(dire)
            for k in f:
                stri = (".3gp", ".avi", ".flv", ".mkv", ".mov", ".mpg", ".rm", ".vob", ".wmv", ".mp4")
                if any(s in k for s in stri):
                    # print(dire)
                    video_files.append(dire+"\\"+k)
    return video_files

    FH.close()
    # FW.close()

# print(processingProperVideoList(file))

class Application:
    def __init__(self, parent):
        self.parent = parent;
        self.frame = Frame(parent)
        # self.scroll = Scrollbar()
        self.topframe()
        self.bottomframe()
        self.listBox()
        self.myImage()

    def topframe(self):
        self.topfr = Frame(self.parent);
        self.topfr.config(bg='#3e7059')
        self.lab = Label(self.topfr, text="Video List :-)", font=("Helvetica", 16, "bold"), bg='#3e7059')
        self.lab.pack()
        self.topfr.grid(row=0, columnspan=10, sticky=(W+E))

    def playvideo(self):
        # threading.Thread(target=os.system("N:/1080p/s01/Lost_S01E01_x265_1080p_BluRay_30nama_30NAMA.mkv")).start()
        # os.system("N:/1080p/s01/Lost_S01E01_x265_1080p_BluRay_30nama_30NAMA.mkv")
        self.videoName = ""
        try:
            self.videoName = self.listb1.selection_get()
        except:
            pass
        if self.videoName == "":
            messagebox.showinfo("Error", "Please Select a video and Hit Play button")
        else :
            # self.button_Bottom.state(['disabled'])
            # print(self.videoName)
            os.system("\"%s\"" % self.videoName)
            # self.button_Bottom.state(['!disabled'])

    def start_thread(self):
        self.thread = threading.Thread(target=self.playvideo)
        self.thread.start()

    def bottomframe(self):
        self.botFrame = Frame(self.parent)
        self.botFrame.config(bg='#3e7059')
        self.foto = PhotoImage(file="C:/Users/ajaydhas/Desktop/python/Succ_apps/play.png").subsample(10,10)
        self.button_Bottom = ttk.Button(self.botFrame, text="  Play", image=self.foto, compound=LEFT, command=self.start_thread)
        self.button_Bottom.image = self.foto
        self.button_Bottom.pack()
        self.botFrame.grid(row=2, sticky=(W+E), columnspan=10)

    def listBox(self):
        self.listFrame = Frame(self.parent)
        self.listFrame.config(bg='#a3eda1')
        self.scroll = ttk.Scrollbar(self.listFrame, orient=VERTICAL)
        self.scroll_bot = ttk.Scrollbar(self.listFrame, orient=HORIZONTAL)
        self.listb1 = Listbox(self.listFrame, selectmode=SINGLE,relief=GROOVE, width=150, height=30, yscrollcommand=self.scroll.set, xscrollcommand=self.scroll_bot.set, bg='#849b84')
        self.scroll.config(command=self.listb1.yview)
        self.scroll_bot.config(command=self.listb1.xview)
        for i in processingProperVideoList(findingVideoFiles(removingCdDrive())):
        # for i in processingProperVideoList(file):
            self.listb1.insert(END, i)
        self.listb1.grid(sticky=W, row=1)
        self.scroll_bot.grid(sticky=(N+E+S+W), columnspan=8)
        self.scroll.grid(sticky=(N+E+W+S), column=8, row=1)
        self.listFrame.grid(row=1,  columnspan=8)

    def myImage(self):
        self.imageF = Frame(self.parent)
        self.imageF.config(bg='green')
        # self.file = 'C:/Users/ajaydhas/Downloads/my.png'; #self.image = Image.open(self.file)
        self.foto1 = PhotoImage(file='C:/Users/ajaydhas/Downloads/my.png').subsample(9,9)
        self.label = Label(self.imageF, image=self.foto1, width=100, height=100, bg='green', relief=GROOVE)
        self.label.image=self.foto
        self.label.pack()
        self.imageF.grid(row=1, column=9, columnspan=10)




# findingVideoFiles(removingCdDrive())

if __name__ == '__main__':
    root = Tk()
    root.title("Video Bank")
    root.config(bg='#3e7059')
    Application(root)
    mainloop()

