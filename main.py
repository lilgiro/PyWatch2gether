#! /usr/bin/env python3
#
# PyQt5-based video-sync example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
"""
A VLC python bindings player implemented with PyQt5 that is meant to be utilized
as the "master" player that controls all "slave players".

Author: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
Date: 25 January 2019
"""


import os
import queue
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from network import Server
from client_player import SlavePlayer
from server_player import MasterPlayer

class StartingWindow(QtWidgets.QMainWindow):
    """The starting window that allows the user to select between server and client."""
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Starting Window")
        
        self.mode = None
        
        self.load_default_config()

        self.createui()
    
    def createui(self):
        self.button1 = QtWidgets.QPushButton("Server", self)
        self.button1.move(10, 10)
        self.button1.clicked.connect(self.server)
        self.button2 = QtWidgets.QPushButton("Client", self)
        self.button2.move(10, 50)
        self.button2.clicked.connect(self.client)
    
    def server(self):
        print("Server")
        self.mode = "server"
        self.selectIPandPort()
    
    def client(self):
        print("Client")
        self.mode = "client"
        self.selectIPandPort()
    
    def selectIPandPort(self):
        self.button1.hide()
        self.button2.hide()

        self.textbox1 = QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 20)
        self.textbox1.resize(200, 20)
        self.textbox1.insert(self.default_ip)
        self.textbox1.show()

        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.move(240, 20)
        self.textbox2.resize(75, 20)
        self.textbox2.insert(self.default_port.__str__())
        self.textbox2.show()

        self.button3 = QtWidgets.QPushButton("Submit", self)
        self.button3.move(220, 60)
        self.button3.clicked.connect(self.submit)
        self.button3.show()

        self.button4 = QtWidgets.QPushButton("Set as default", self)
        self.button4.move(20, 60)
        self.button4.clicked.connect(self.save_default_config)
        self.button4.show()

        self.resize(340, 100)

    
    def submit(self):
        # lock all the buttons and textboxes
        self.textbox1.setEnabled(False)
        self.textbox2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)

        # change button text
        self.button3.setText("Loading...")
        self.button3.repaint()

        # Load the player
        if self.mode == "server":
            self.player = MasterPlayer()

        elif self.mode == "client":
            self.player = SlavePlayer()

        else:
            print("Error: mode not selected. How did you get here?")
            return
        
        # Set the IP and port
        self.player.set_ip_and_port(self.textbox1.text(), self.textbox2.text())
        self.player.open_socket()

        # Show the player
        self.player.resize(640, 640)
        self.player.show()
        self.hide()


    def load_default_config(self):
        """Load default config file."""
        if os.path.isfile("config.txt"):
            with open("config.txt", "r") as f:
                self.default_ip = f.readline().strip()
                self.default_port = f.readline().strip()
        else:
            self.default_ip = "localhost"
            self.default_port = 9999
    
    def save_default_config(self):
        """Save default config file."""
        with open("config.txt", "w") as f:
            f.write(self.textbox1.text() + "\n")
            f.write(self.textbox2.text() + "\n")



def main():
    """Selection between server and client, and then run the player."""
    app = QtWidgets.QApplication(sys.argv)
    window = StartingWindow()
    
    window.resize(100, 100)
    window.show()


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
