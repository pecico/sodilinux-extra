#!/usr/bin/env python3.5

'''
@author    Antonio Faccioli <antonio.faccioli@soluzioniopen.com>
@license   http://directory.fsf.org/wiki/License:MPLv2.0
@version   1.0
'''

from tkinter import *
from tkinter import messagebox
import sys, os, subprocess
import urllib.request
from urllib.error import URLError, HTTPError

#inizializza il modulo Tk
tk = Tk()

#variabili d'ambiente
font = "Liberation Sans"
label_text1 = "1. Controllo della connessione"
label_text2 = "2. Aggiornamento indici"
label_text3 = "3. Aggiornamento software"
label_text4 = "4. Rimozione elementi obsoleti"
label_text5 = "5. Procedura completata"
error_step = ".....NON ESEGUITO"
error_text = ".....ERRORE"
pass_step = ".....OK"
url_check = "http://www.google.it"
button_start = "Avvia"
button_exit = "Chiudi"
title_infobox = "Attenzione"
content_infobox = "Per eseguire questo programma devi avere i privilegi di Root!"
logfile = "logfile.txt"

def check_root():
        if os.getuid() != 0:
                messagebox.showinfo(title_infobox, content_infobox)
                sys.exit()

def change_state_button(new_state):
        button1.config(state=new_state)
        button2.config(state=new_state)

def change_label(label, label_text, style, color):
        window.itemconfig(label, font=(font, 12, style), fill=color, text=label_text)
        tk.update()

def update():
        change_label(label2, label_text2, 'bold', '#880c0c')
        try:
                proc = subprocess.Popen('apt-get update', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=None, executable="/bin/bash")
                proc.wait()
                change_label(label2, label_text2+pass_step, 'normal', 'black')
        except subprocess.SubprocessError:
                change_label(label2, label_text2+error_text, 'normal', 'red')
                change_label(label3, label_text3+error_step, 'normal', 'red')
                change_label(label4, label_text4+error_step, 'normal', 'red')
                change_label(label5, label_text5+error_step, 'normal', 'red')
                change_state_button(NORMAL)

def dist_upgrade():
        change_label(label3, label_text3, 'bold', '#880c0c')
        try:
                proc = subprocess.Popen('apt-get --assume-yes dist-upgrade', shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")
                proc.wait()
                change_label(label3, label_text3+pass_step, 'normal', 'black')
        except subprocess.SubprocessError:
                change_label(label3, label_text3+error_text, 'normal', 'red')
                change_label(label4, label_text4+error_step, 'normal', 'red')
                change_label(label5, label_text5+error_step, 'normal', 'red')
                change_state_button(NORMAL)

def autoremove():
        change_label(label4, label_text4, 'bold', '#880c0c')
        try:
                proc = subprocess.Popen('apt-get --assume-yes autoremove', shell=True, stdin=None, stdout=None, stderr=None, executable="/bin/bash")
                proc.wait()
                change_label(label4, label_text4+pass_step, 'normal', 'black')
                change_label(label5, label_text5+pass_step, 'normal', 'black')
                change_state_button(NORMAL)
        except subprocess.SubprocessError:
                change_label(label4, label_text4+error_text, 'normal', 'red')
                change_label(label5, label_text5+error_step, 'normal', 'red')
                change_state_button(NORMAL)

def halt():
        tk.destroy()
	
def check():
        check_root()
        change_state_button(DISABLED)
        change_label(label1, label_text1, 'bold', '#880c0c')
        try:
                urllib.request.urlopen(url_check)
                change_label(label1, label_text1+pass_step, 'normal', 'black')
                update()
                dist_upgrade()
                autoremove()
        except:
                change_label(label1, label_text1+error_text, 'normal', 'red')
                change_label(label2, label_text2+error_step, 'normal', 'red')
                change_label(label3, label_text3+error_step, 'normal', 'red')
                change_label(label4, label_text4+error_step, 'normal', 'red')
                change_label(label5, label_text5+error_step, 'normal', 'red')

def start():
	check()

#costruisce la finestra
window = Canvas(tk, width=550, height=450)
tk.wm_title("Sodilinux Upgrade 1.0")
current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
header = PhotoImage(file=current_dir + '/images/header.gif')
window.create_image(0,0, anchor=NW, image=header)
iconName = "@" + current_dir + "/images/icon_sodi_upgrade.xbm"
tk.iconbitmap(iconName)

#window.call('wm', 'iconphoto', window._w, img)
label1 = window.create_text(50, 150, anchor=W, text=label_text1, font=(font, 12))
label2 = window.create_text(50, 200, anchor=W, text=label_text2, font=(font, 12))
label3 = window.create_text(50, 250, anchor=W, text=label_text3, font=(font, 12))
label4 = window.create_text(50, 300, anchor=W, text=label_text4, font=(font, 12))
label5 = window.create_text(50, 350, anchor=W, text=label_text5, font=(font, 12))

#costruisce e inizializza i pulsanti
button1 = Button(text = button_start, anchor=S, font=(font, 12), command=start)
button1.pack()
button1.place(x=210, y=400)
button2 = Button(text = button_exit, anchor=S, font=(font, 12), command=halt)
button2.pack()
button2.place(x=279, y=400)

#inizializza la finestra
window.pack()
tk.mainloop()
