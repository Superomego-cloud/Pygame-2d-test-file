import os
import re
import time
import tkinter

scrip = os.path.dirname(__file__)
fileDir = os.path.join(scrip, "MESSAGE_TEXT.txt")
fileDir2 = os.path.join(scrip, "VALID_KEY.txt")
file = ""
newText = ""
endTrans = False
string = ""
string2 = ""
color = ""


#I didn't borrow this though
def updateText(a):
    
    global newText
    
    print("Text Loading...")
    
    if newText != string:
        msg["text"] = ""
        newText = "\n"
        msg.pack()
        for i in range(int(len(string)/3)):
            newText += string[i*3:(i*3 + 3)]
            msg["text"] = newText
            window.update()
            time.sleep(1/(2*i + 100))
        if newText != string:
            msg["text"] = string
            newText = string
            window.update()
    else:
        msg["text"] = ""
        newText = "\n"
        msg.pack()
        for i in range(int(len(string2)/3)):
            newText += string2[i*3:(i*3 + 3)]
            msg["text"] = newText
            window.update()
            time.sleep(1/(2*i + 100))
        if newText != string2:
            msg["text"] = string2
            newText = string2
            window.update()
        window.unbind("<Return>")
            
# I borrowed this from another website and slightly modified it to return a string instead of a list
def toBinary(a):
  l,m=[],""
  for i in a:
    l.append(ord(i))
  for i in l:
    m += str(int(bin(i)[2:]))
  return m

window = tkinter.Tk()
window.geometry("720x500")
window.bind("<Return>", updateText)
msg = tkinter.LabelFrame(text="", foreground="#ffffff", background="#000000", height=500, width=720, font=("FixedSys", 19), highlightthickness=0, borderwidth=0)

try:
    file = open(fileDir, "x")
except FileExistsError:
    string = "\n  AC - FILE DETECTED... \n"
    msg["foreground"] = "#11ee11"
    msg.pack()
    window.update()
    window.event_generate(sequence="<Return>", when="now")
    file = open(fileDir, "r")
    try:
        file2 = open(fileDir2, "r")
    except FileNotFoundError:
        if file.readline() == "CDD#FGG#A#":
            string2 = "\n AC - VALID KEY, PLEASE RELOAD WINDOW"
            os.system("pause")
            msg["foreground"] = "#11ee11"
            file2 = open(fileDir2, "a")
            file2.write(toBinary(scrip))
            file2.close()
        else:
            string2 = "\n ERROR(WA) - SESSION KEY NOT FOUND \n PLEASE ENTER PASSWORD"
else:
    string = "\n  FILE CREATED - PLEASE CLOSE THE WINDOW \n AND ENTER A VALID PASSKEY TO PROGRESS"
    msg["foreground"] = "#ee1111"
    msg.pack()
    window.update()
    window.event_generate(sequence="<Return>", when="now")
    window.unbind("<Return>")

window.mainloop()