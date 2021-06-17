#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

### Temporary ???
import time
import numpy as np
### No real functionality yet
### ADD: display in window as well as in the terminal
### ADD: Maybe some flair, low on priorties
### TEST: GridLayout might be better rather than manually setting each location

class gui(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Name and size of window
        self.setWindowTitle("DAQCommand Window")
        self.resize(700, 500)

        # Available commands
        self.startButton()
        self.stopButton()
        self.pauseButton()
        self.restartButton()
        self.reconfigureButton()
        self.infoMenu()
        self.quitButton()

        # Display the gui
        self.show()
    
    # Start command, allows for timed and set number of events runs
    def start(self):
        self.timeString = self.timedTextBox.text()
        self.eventsString = self.eventsTextBox.text()
    
        # Addresses potential user input errors
        if not(self.timeString == "") and not(self.eventsString == ""):
            print("Only one or neither box must be filled.")
            return
        
        # Due to errors with empty strings, change them to (hopefully) unused strings
        if self.timeString == "":
            self.timeString += "00.12321"
        if self.eventsString == "":
            self.eventsString += "0012321"
        
        time = float(self.timeString)
        events = int(self.eventsString)

        if time < 0 or events < 0:
            print("Time and events must be greater than 0.")
            return

        # Create separate thread so user can still use GUI while processes run
        self.runThread = QThread()
        self.worker = StartWorker()
        self.worker.moveToThread(self.runThread)

        self.runThread.started.connect(self.worker.startRun)
        self.worker.finished.connect(self.runThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.runThread.finished.connect(self.runThread.deleteLater)
        self.runThread.start()

    def startButton(self):
        # The button to start
        self.startbtn = QPushButton("Start", self)
        self.startbtn.move(25, 75)
        self.startbtn.clicked.connect(self.start)

        # The text boxes for entry of number of seconds or events to run for
        self.timedTextBox = QLineEdit(self)
        self.timedTextBox.move(220, 75)
        self.timedTextBox.setValidator(QDoubleValidator())
        self.eventsTextBox = QLineEdit(self)
        self.eventsTextBox.move(405, 75)
        self.eventsTextBox.setValidator(QIntValidator())

        # Labels for the text boxes
        self.timedLabel = QLabel("Seconds (float):", self)
        self.timedLabel.move(135, 75)
        self.eventsLabel = QLabel("# Events (int):", self)
        self.eventsLabel.move(325, 75)

        # Header for Commands on left
        self.commandTitle = QLabel("Commands: ", self)
        font = self.commandTitle.font()
        font.setBold(True)
        self.commandTitle.setFont(font)
        self.commandTitle.setAlignment(Qt.AlignCenter)
        self.commandTitle.move(25, 25)

    # Stop command, stops current run
    def stop(self):
        print("Stopping current run...")
        
        # Used to terminate process if button has been pressed
        self.stopHasBeenCalled = True

        # Terminate current thread, if started again creates new thread
        self.runThread.terminate()
        self.runThread.wait()
    def stopButton(self):
        self.stopbtn = QPushButton("Stop", self)
        self.stopbtn.move(25, 125)
        self.stopbtn.clicked.connect(self.stop)
        
    # Pause command, pauses and unpauses processes 
    def pause(self):
        # Check if already paused
        if self.pausebtn.isChecked():
            print("Paused")
        else:
            print("Unpaused")
    def unpause(self):
        print("unpausing MilliDAQ processes")
    def pauseButton(self):
        self.pausebtn = QPushButton("Pause", self)
        self.pausebtn.move(25, 175)
        self.pausebtn.setCheckable(True) # Set as toggable, so user can tell if paused
        self.pausebtn.clicked.connect(self.pause)
        self.pausebtn.update()

    # Restart command, stops the cuurent run and starts a new one
    def restart(self):
        self.stop()
        self.start()
    def restartButton(self):
        self.restartbtn = QPushButton("Restart", self)
        self.restartbtn.move(25, 225)
        self.restartbtn.clicked.connect(self.restart)

    ### Check if supposed to also restart.
    # Reconfigure commmand, reconfigures for the run
    def reconfigure(self):
        self.pathToFile = self.pathTextBox.text()

        if self.pathToFile == "":
            print("A path is required.")
            return

        ### FIXME: check if path in correct format (DAQ Code might already check)
        print(self.pathToFile)
        print("reconfiguring...")
        print("reconfigured")
    def reconfigureButton(self):
        # The button to reconfig
        self.reconfigbtn = QPushButton("Reconfigure", self)
        self.reconfigbtn.move(25, 275)
        self.reconfigbtn.clicked.connect(self.reconfigure)

        # The text box for the path
        self.pathTextBox = QLineEdit(self)
        self.pathTextBox.move(220, 275)

        # Label for path box
        self.pathLabel = QLabel("Path to file: ", self)
        self.pathLabel.move(155, 275)

    # Information about runs an equipment
    def status(self):
        print("status")
    def configuration(self):
        print("config")
    def board(self):
        print("board")
    def rates(self):
        print("rates")
    def infoMenu(self):
        # Buttons for each bit of information
        self.statusbtn = QPushButton("Status", self)
        self.statusbtn.move(575, 75)
        self.configbtn = QPushButton("Configuration", self)
        self.configbtn.move(575, 125)
        self.boardbtn = QPushButton("Board", self)
        self.boardbtn.move(575, 175)
        self.ratesbtn = QPushButton("Rates", self)
        self.ratesbtn.move(575, 225)

        # Header for 'menu'
        self.infoTitle = QLabel("Information: ", self)
        font = self.infoTitle.font()
        font.setBold(True)
        self.infoTitle.setFont(font)
        self.infoTitle.setAlignment(Qt.AlignCenter)
        self.infoTitle.move(575, 25)

        # Info buttons need to do something
        self.statusbtn.clicked.connect(self.status)
        self.configbtn.clicked.connect(self.configuration)
        self.boardbtn.clicked.connect(self.board)
        self.ratesbtn.clicked.connect(self.rates)

    # Quit command, stops all processes and closes the gui window
    def quit(self):
        print("Stopping all MilliDAQ processes...")
        print("Doesn't work yet")
    def quitButton(self):
        self.quitbtn = QPushButton("Quit", self)
        self.quitbtn.move(25, 450)
        self.quitbtn.clicked.connect(self.quit)
        self.quitbtn.clicked.connect(self.close)

# Actual processes of the 'start' button
class StartWorker(QObject):
    finished = pyqtSignal()

    def startRun(self):
        # Start MilliDAQ processes
        print("Starting all MilliDAQ processes...")

        w.stopHasBeenCalled = False

        # Able to Pause and stop runs
        if not(w.timeString == "00.12321"):
            for i in np.arange(0, time, 0.01):
                print("second:" + str(i+0.01))
                while w.pausebtn.isChecked():
                    time.sleep(0)
                time.sleep(1)
        elif not(w.eventsString == "0012321"):
            for i in range(0, events, 1):
                print("event: " + str(i+1))
                while w.pausebtn.isChecked():
                    time.sleep(0)
                time.sleep(1)
        else:
            while True:
                print("Kept infinite until actual process can replace. oops")
                while w.pausebtn.isChecked():
                    time.sleep(0)
                if w.stopHasBeenCalled:
                    break
                time.sleep(1)

if __name__=="__main__":
    app = QApplication(sys.argv)
    
    w = gui()

    sys.exit(app.exec_())