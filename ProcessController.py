from tkinter import *
from tkinter import messagebox
import os
import psutil
import configparser
import sqlite3
import subprocess
import time
import _thread
from Repeater import Repeater

root=Tk()
root.title("Process Controller")
kill_process_dict={}
root.maxsize(300,280)
root.minsize(300,280)
root.after(2000,root.focus_force)
root.iconbitmap('favicon.ico')
dict_process={}
dict_port={}
dict_path={}
dict_command={}
config = configparser.RawConfigParser() 
config.read('config.properties')
dict_port = dict(config.items('Port'))
dict_process = dict(config.items('Process'))
dict_path = dict(config.items('Path'))
dict_command= dict(config.items('Command'))
dict_config=dict(config.items('Config'))
b1_flag=True
b2_flag=True
b3_flag=True
    

def checkifProcessRunning(Port):
    value= os.popen('netstat -aon | find "'+Port+'"').read()
    if len(value)>1:
        return True
    else:
        return False
def turnOn(TomcatName,Path,Port,Command):
    os.chdir(Path) 
    os.system(Command)
    pid=getProcessId(Port)
    pname=TomcatName
    kill_process_dict.update({pname:pid})

    if TomcatName==dict_process['button2']:
        button2['text']=dict_process['button2'].upper()+"("+dict_port[dict_process['button2']]+") STOP"
        button2['command']=lambda:turnOff(TomcatName)
        button2['bg']="pale green"
        if b2_flag== False:
            root.update()
            button2['text']="FAILED"
            button2['bg']="red"
            button2['command']=lambda:turnOn(TomcatName,Path,Port,Command)
    if TomcatName==dict_process['button3']:
        button3['text']=dict_process['button3'].upper()+"("+dict_port[dict_process['button3']]+") STOP"
        button3['command']=lambda:turnOff(TomcatName)
        button3['bg']="pale green"
        if b3_flag== False:
            root.update()
            button3['text']="FAILED"
            button3['bg']="red"
            button3['command']=lambda:turnOn(TomcatName,Path,Port,Command)
    if TomcatName==dict_process['button1']:
        root.update()
        button1['text']=dict_process['button1'].upper()+"("+dict_port[dict_process['button1']]+") STOP"
        button1['command']=lambda:turnOff(TomcatName)
        button1['bg']="pale green" 
        if b1_flag== False:
            button1['text']="FAILED"
            button1['bg']="red"
            button1['command']=lambda:turnOn(TomcatName,Path,Port,Command)
                
def turnOff(Process):
    os.system('taskkill /pid '+kill_process_dict[Process])
    if Process==dict_process['button2']:
        button2['text']=dict_process['button2'].upper()+"("+dict_port[dict_process['button2']]+") START"
        button2['command']=lambda:turnOn(dict_process['button2'],dict_path[dict_process['button2']],dict_port[dict_process['button2']],dict_command[dict_process['button2']])
        button2['bg']='dodger blue'  
    if Process==dict_process['button1']:
        button1['text']=dict_process['button1'].upper()+"("+dict_port[dict_process['button1']]+") START"
        button1['command']=lambda:turnOn(dict_process['button1'],dict_path[dict_process['button1']],dict_port[dict_process['button1']],dict_command[dict_process['button1']])
        button1['bg']='dodger blue'
        print(dict_process['button1'].upper()+"("+dict_port[dict_process['button1']]+") START")
    if Process==dict_process['button3']:
        button3['text']=dict_process['button3'].upper()+"("+dict_port[dict_process['button3']]+") START"
        button3['command']=lambda:turnOn(dict_process['button3'],dict_path[dict_process['button3']],dict_port[dict_process['button3']],dict_command[dict_process['button3']])
        button3['bg']='dodger blue'               


    
def getProcessId(Port):
    final=''
    value = os.popen('netstat -aon | find "'+Port+'"').read()
    #if len(value) <1:
    startTime=time.time()
    endTime=time.time()
    difference_time=(endTime-startTime)
        
    while len(value) <1 and difference_time < int(dict_config['starting_time']):
        running_status(Port)
        root.update()
        value = os.popen('netstat -aon | find "'+Port+'"').read()
        endTime=time.time()
        difference_time=(endTime-startTime)
    try:
        print('trying') 
        pidLen=(len(value)-1)
        if value[pidLen]=="\n":
            pidLen=pidLen-1
        while value[pidLen]!=' ':
            final= final+value[pidLen]
            pidLen=pidLen-1
        final=final[::-1]
        return final
        
    except:
        print('Failed to start')
        failed_status(Port)
        print(b3_flag)    
def get_value(Port):
    value = os.popen('netstat -aon | find "'+Port+'"').read()
def running_status(Port):
    if Port==dict_port[dict_process['button2']]:
        button2['text']="STARTING UP"
        button2['bg']="pale green"
        button2['command']=start_up_message
    if Port==dict_port[dict_process['button3']]:
        button3['text']="STARTING UP"
        button3['bg']="pale green"
        button3['command']=start_up_message
    if Port==dict_port[dict_process['button1']]:
        button1['text']="STARTING UP"
        button1['bg']="pale green" 
        button1['command']=start_up_message

def failed_status(Port):
    global b1_flag,b2_flag,b3_flag
    if Port==dict_port[dict_process['button2']]:
        b2_flag=False
    if Port==dict_port[dict_process['button3']]:
        b3_flag=False
    if Port==dict_port[dict_process['button1']]:
        b1_flag=False
def start_up_message():
    messagebox.showinfo("Service Starting Up", "Please wait for Service to Start")   
    
          
#button1
if checkifProcessRunning(dict_port[dict_process['button1']]) == True:
    kill_process_dict.update({dict_process['button1']:getProcessId(dict_port[dict_process['button1']])})
    display_text1=dict_process['button1'].upper()+" AT PORT "+dict_port[dict_process['button1']]+" IS RUNNING"
    button1= Button(root,text=display_text1,padx=40,pady=20,bg="salmon1",command=lambda : turnOff(dict_process['button1']))
    
else:
    display_text1=dict_process['button1'].upper()+"("+dict_port[dict_process['button1']]+") START"    
    button1= Button(root,text=display_text1,command=lambda:turnOn(dict_process['button1'],dict_path[dict_process['button1']],dict_port[dict_process['button1']],dict_command[dict_process['button1']]),
    padx=40,pady=20,bg='dodger blue') 

button1.pack(side="top", fill="x")

#button2
if checkifProcessRunning(dict_port[dict_process['button2']]) == True:
    kill_process_dict.update({dict_process['button2']:getProcessId(dict_port[dict_process['button2']])})
    display_text2=dict_process['button2'].upper()+" AT PORT "+dict_port[dict_process['button2']]+" IS RUNNING"
    button2= Button(root,text=display_text2,padx=40,pady=20,bg="salmon1",command=lambda : turnOff(dict_process['button2']))
else:
    display_text2=dict_process['button2'].upper()+"("+dict_port[dict_process['button2']]+") START"        
    button2= Button(root,text=display_text2,command=lambda:turnOn(dict_process['button2'],dict_path[dict_process['button2']],dict_port[dict_process['button2']],dict_command[dict_process['button2']]),
    bg='dodger blue',padx=40,pady=20)       
button2.pack(side="top", fill="x")

#button3
if checkifProcessRunning(dict_port[dict_process['button3']]) == True:
    kill_process_dict.update({dict_process['button3']:getProcessId(dict_port[dict_process['button3']])})
    display_text3=dict_process['button3'].upper()+" AT PORT "+dict_port[dict_process['button3']]+" IS RUNNING"
    button3= Button(root,text=display_text3,padx=40,pady=20,bg="salmon1",command=lambda : turnOff(dict_process['button3']))
else:
    display_text3=dict_process['button3'].upper()+"("+dict_port[dict_process['button3']]+") START"        
    button3= Button(root,text=display_text3,command=lambda:turnOn(dict_process['button3'],dict_path[dict_process['button3']],dict_port[dict_process['button3']],dict_command[dict_process['button3']]),
    padx=40,pady=20,bg='dodger blue')    
button3.pack(side="top", fill="x")

exitButton=Button(root, text="Exit",command=root.quit,padx=40,pady=20,bg='red').pack(side="bottom")

root.mainloop()
