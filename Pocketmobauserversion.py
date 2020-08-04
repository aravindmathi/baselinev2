from tkinter import *
import csv
import subprocess

root = Tk()
root.title("Pocket Baseline")
root.iconbitmap('logo.ico')
root.geometry("600x300")

bnum=5
jnum=1000

#config files
with open('interface.ini','r') as f:
    conf_dict={}
    for line in f:
        items=line.split('=')
        conf_dict[items[0].strip()] = items[1].strip()

# Processing the CSV file
def csvproc(text):
    with open('baseline.csv', 'r') as csv_file:
        lst = []
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            if line['SID'].strip().upper()  == text or line['Hostname'].strip().upper() ==text or line['IP'].strip() == text:
                lst.append([line['SID'], line['Hostname'], line['IP']])
        return lst

#processing 2nd CSV file for Java urls
def csvJavaUrl(text):
    with open('javaurl.csv', 'r') as csv_file:
        lst = []
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            if line['SID'].strip().upper() == text:
                lst.append([line['SID'], line['url']])
        return lst

# Destroying the text widget if the input is wrong
def desttext():
    try:
        enlst
    except:
        pass
    else:
        for col in enlst:
            # col.delete(1.0,END)
            col.destroy()


# Destroying the Label widget if the input is correct
def destLabel():
    try:
        global labLst
        for lab in labLst:
            lab.destroy()
        labLst = []
    except:
        pass

#To launch Putty moba and SAPGUI
def launch(ip):

    if p.get()=="putty":
        subprocess.Popen(f"putty.exe -ssh {ip}")
    elif p.get() == "win":
        #print(ip)
        subprocess.Popen(f"mstsc /v {ip.strip()}")
    elif p.get() == "moba" :
        #print(usr_text.get("1.0","end"))
        subprocess.Popen(f'{conf_dict["moba"]} -newtab \"waitforX; ssh {usr_text.get("1.0","end").strip()}@{ip}\"')
    elif p.get()=="gui":
        with open('gui.csv', 'r') as gui_file:
            print("Hello")
            lst = []
            csv_reader = csv.DictReader(gui_file)
            for line in csv_reader:
                if line['SID'].strip().upper() == ip:
                    subprocess.Popen(f'{conf_dict["gui"]} {line["command"]}')

def launchg(sid,ip):
    print(sid,ip)
    with open('gui.csv', 'r') as gui_file:
        print("Hello")
        lst = []
        csv_reader = csv.DictReader(gui_file)
        for line in csv_reader:
            if line['SID'].strip().upper() == sid:
                print(f'{conf_dict["gui"]} {line["command"]}')
                subprocess.Popen(f'{conf_dict["gui"]} {line["command"]}')


#Launch Chrome
def urllaunch(url):
    #cmd=r'f"{conf_dict["chrome"]}"'
    print(conf_dict["chrome"])
    subprocess.Popen([{conf_dict["chrome"]}, url])

# if user press enter below function will get executed
def ret(event):

    #if radio button is Baseline then execute
    if select.get() == 1:
        ret_lst = csvproc(input_entry.get().strip().upper())
        global myLabel

        # If user input is invalid show invalid on screen
        if ret_lst == []:
            desttext()
            destLabel()
            myLabel = Label(root, text="Invalid Input!!!!")
            myLabel.config(font=("Courier", 20))
            myLabel.grid(row=5, column=2, columnspan=3)
            labLst.append(myLabel)

        # If user input is valid below will be executed
        else:
            destLabel()
            cnt = 0
            global enlst
            global usr_text
            desttext()
            enlst = []
            for res in ret_lst:
                for i in range(len(res)):
                    if len(str(res[i].strip())) == 3:
                        ret_text = Text(root, height=1, width=3)
                    else:
                        ret_text = Text(root, height=1, width=15)


                    ret_text.insert(1.0, res[i])
                    ret_text.grid(row=bnum + cnt, column=2 + i)
                    if i == 2:
                        if p.get() == "moba" and cnt==0:
                            usr_text=Text(root,height=1,width=6)
                            usr_text.grid(row=bnum + cnt, column=3 + i,rowspan=3)
                            usr_text.insert(1.0,res[0].lower().strip()+"adm")
                            labLst.append(usr_text)
                        #else:
                            #usr2_text = Text(root, height=1, width=6,state='disabled',bg='light gray')
                            #usr2_text.grid(row=bnum + cnt, column=3 + i)
                            #labLst.append(usr2_text)

                        if p.get() == "gui":
                            myButton = Button(root, text="Launch", command=lambda opt=res[i-2]: launchg(opt,res[i]))
                        else:
                            myButton = Button(root, text="Launch", command=lambda opt=res[i]: launch(opt))
                        myButton.grid(row=bnum + cnt, column=4 + i)
                        enlst.append(myButton)

                    enlst.append(ret_text)
                cnt += 1

    #Copy of same above if condition, need to trim the code.
    #if the radio button is anything else other than Baseline
    else:
        desttext()
        ret_lst = csvJavaUrl(input_entry.get().strip().upper())
        #(ret_lst)
        if ret_lst == []:
            desttext()
            destLabel()
            myLabel = Label(root, text="Invalid Input!!!!")
            myLabel.config(font=("Courier", 20))
            myLabel.grid(row=jnum, column=2, columnspan=3)
            labLst.append(myLabel)
        else:
            destLabel()
            cnt = 0
            #global enlst
            desttext()
            enlst = []
            for res in ret_lst:
                for i in range(len(res)):
                    if len(str(res[i].strip())) == 3:
                        continue
                        ret_text = Text(root, height=1, width=3)
                    else:
                        ret_text = Text(root, height=1, width=50)

                    ret_text.insert(1.0, res[i])
                    ret_text.grid(row=jnum + cnt, column=1 + i,columnspan=4)
                    if i == 1:
                        myButton = Button(root, text="Launch", command=lambda opt=res[i]: urllaunch(opt))
                        myButton.grid(row=jnum + cnt, column=5 + i)
                        enlst.append(myButton)

                    enlst.append(ret_text)
                cnt += 1


# Default Widgets on screen when launched
name_label = Label(root, text="Search", padx=2, pady=5).grid(row=1, column=0)
name_label = Label(root, text="SID", padx=2, pady=5).grid(row=bnum-1, column=2)
name_label = Label(root, text="Hostname", padx=15, pady=5).grid(row=bnum-1, column=3)
name_label = Label(root, text="IP", padx=10, pady=5).grid(row=bnum-1, column=4)
name_label = Label(root, text="Mobauser", padx=10, pady=5,width=10).grid(row=bnum-1, column=5)
name_label= Label(root, text="url", padx=10, pady=20).grid(row=jnum, column=1)
labLst = []


#selection of Interfaces
#interfaces=[("putty","putty"),("moba","moba"),("win","win"),("gui","gui")]
p=StringVar()
p.set("putty")

frame=Frame(root,borderwidth=10)
my_radio = Radiobutton(frame, text="putty", variable=p, value="putty").grid(row=1,column=3)
my_radio = Radiobutton(frame, text="moba", variable=p, value="moba").grid(row=1,column=4)
my_radio = Radiobutton(frame, text="win", variable=p, value="win").grid(row=1,column=5)
my_radio = Radiobutton(frame, text="gui", variable=p, value="gui").grid(row=1,column=6)

frame.grid(row=1,column=4,columnspan=5,sticky="nsew")


#selection of Radio button
MODES=[("Baseline",1),("JavaUrl",jnum-2)]
select= IntVar()
select.set(1)


for text,mode in MODES:
    my_radio=Radiobutton(root,text=text,variable=select,value=mode)
    my_radio.grid(row =1+mode,column=1)

r = StringVar()
r.set('LP3')
# User Input text Box
input_entry = Entry(root, text="SID", width=15, borderwidth=2, textvariable=r)
input_entry.grid(row=1, column=1)
# When user press enter will go to function ret
input_entry.bind('<Return>', ret)

root.mainloop()