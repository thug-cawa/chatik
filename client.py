import socket
import threading
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog
from network import *


class Client:
    def __init__(self,host,port):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((host,port))

        app=tkinter.Tk()
        app.withdraw()


        self.nick = simpledialog.askstring("NICK","Choose your nickname",parent = app)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()


    #Настройки окна
    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(width=470, height=550,bg = '#B0C4DE')

        self.chat_label=tkinter.Label(self.window,text = "CHAT",bg = '#778899')
        self.chat_label.config(font=("Arial",15))
        self.chat_label.pack(padx=20,pady=5)

        self.text_area=tkinter.scrolledtext.ScrolledText(self.window,bg='#778899',fg='#FFE4E1')
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled')

        self.message_label=tkinter.Label(self.window,text='Write message',bg='#778899')
        self.message_label.config(font=("Arial",15))
        self.message_label.pack(padx=20,pady=5)

        self.scrollbar = Scrollbar(self.text_area)
        self.scrollbar.configure(command=self.text_area.yview)

        self.input_area=tkinter.Text(self.window,height=3,bg='#778899',fg='#FFE4E1')
        self.input_area.pack(padx=20,pady=5)

        self.send_button=tkinter.Button(self.window,text='send',command = self.write,height=2,bg='#778899')
        self.send_button.config(font=('Arial',12))
        self.send_button.pack(padx=20,pady=5)
        self.gui_done=True


        self.window.mainloop()

    def write(self):
        message = f"{self.nick}: {self.input_area.get('1.0','end')}"
        self.socket.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')


    def stop(self):
        self.running=False
        self.window.destroy()
        self.socket.close()
        exit(0)


    def receive(self):
       while self.running:
           try:
               message = self.socket.recv(1024)
               if message == "NICK":
                   self.socket.send(self.nick.encode('utf-8'))
               else:
                   if self.gui_done:
                       self.text_area.config(state='normal')
                       self.text_area.insert('end', message)
                       self.text_area.yview('end')
                       self.text_area.config(state='disabled')
           except ConnectionAbortedError:
               break
           except:
               print("Error")
               self.socket.close()
               break

client= Client(host,port)