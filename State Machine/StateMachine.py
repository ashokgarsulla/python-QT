import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QStateMachine,QState,QFinalState
# from PyQt5.QtCore import SIGNAL,Signal

class CalibrationControlPanel(QMainWindow):
    imageOrPoseDataAcquisitionCompleted = pyqtSignal(name="imageOrPoseDataAcquisitionCompleted")
    daqStartResumeClicked = pyqtSignal(name="daqStartResumeClicked")
    daqCompleted = pyqtSignal(name="daqCompleted")
    dataUpdateCompleted = pyqtSignal(name="dataUpdateCompleted")
    recoverableDAQErrorOccurred = pyqtSignal(name="recoverableDAQErrorOccurred")
    daqPaused = pyqtSignal(name="daqPaused")
    windowClosed = pyqtSignal(name="windowClosed")
    
    
    Expand (9 lines)

@pyqtSlot()
def on_stateImageOrPoseDataAcquisitionEntered(self):
    print("[CalibrationControlPanel.py] Started image acquisition")
    self.isCollectingImageOrPoseData =False
    self.isCollectingImageOrPoseDataTimedOut = False        
    self.trackingSystem.tsInteractive.RefreshBlobClassification()


@pyqtSlot(str)
def on_ComputationErrorOccurred(self,errorStr):
if self.computationRunning:
    QMessageBox(QMessageBox.Icon.Critical,"Error",errorStr,parent=self).show()
    self.ui.pbStartComputation.setEnabled(True)
    self.ui.pbStopComputation.setEnabled(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        def __setupAndStartDAQFSM(self):
            self.daqFSM = QStateMachine()
            #state definitions        self.stateSystemReadyWait = QState()
            self.stateDAQRunning = QState()
            self.stateDAQComplete = QState()
            self.stateServoOnWait = QState(parent=self.stateDAQRunning)
            self.stateRobotMotion = QState(parent=self.stateDAQRunning)
            self.stateImageOrPoseDataAcquisition = QState(parent=self.stateDAQRunning)
            self.stateDataUpdateWait = QState(parent=self.stateDAQRunning)
            self.daqFSM.addState(self.stateSystemReadyWait)
            self.daqFSM.addState(self.stateDAQRunning)
            self.daqFSM.addState(self.stateDAQComplete)
            self.daqFSM.setInitialState(self.stateSystemReadyWait)
            self.stateDAQRunning.setInitialState(self.stateServoOnWait)
            #setup transitions        self.stateSystemReadyWait.addTransition(self.daqStartResumeClicked,self.stateDAQRunning)
            self.stateServoOnWait.addTransition(self.ui.robotInterface.robotServoTurnedOn, self.stateRobotMotion)
            self.stateRobotMotion.addTransition(self.ui.robotInterface.robotMotionStopped, self.stateImageOrPoseDataAcquisition)
            self.stateImageOrPoseDataAcquisition.addTransition(self.imageOrPoseDataAcquisitionCompleted, self.stateDataUpdateWait)
            self.stateDataUpdateWait.addTransition(self.dataUpdateCompleted, self.stateRobotMotion)
            self.stateDataUpdateWait.addTransition(self.daqCompleted, self.stateDAQComplete)
            self.stateDAQRunning.addTransition(self.recoverableDAQErrorOccurred, self.stateSystemReadyWait)
            self.stateDAQRunning.addTransition(self.daqPaused, self.stateSystemReadyWait)
            self.stateDAQRunning.addTransition(self.ui.pbStopCalibDAQ.clicked, self.stateSystemReadyWait)
            #connect signals for on_entry and on_exit        self.stateDAQRunning.entered.connect(self.ui.robotInterface.servoOn)
            self.stateDAQRunning.exited.connect(self.ui.robotInterface.servoOff)
            self.stateRobotMotion.entered.connect(self.__beginRobotMotion)
            self.stateImageOrPoseDataAcquisition.entered.connect(self.on_stateImageOrPoseDataAcquisitionEntered)
            self.stateDataUpdateWait.entered.connect(self.on_stateDataUpdateWaitEntered)
            self.stateSystemReadyWait.entered.connect(self.on_stateSystemReadyWaitEntered)
            self.stateDAQComplete.entered.connect(self.on_stateDAQCompleteEntered)
            self.daqFSM.start()

        button = QPushButton("working")

        machine = QStateMachine()
        s1 = QState()
        s1.assignProperty(button, "text", "Click me")

        s2 = QFinalState()
        # s1.addTransition(button, SIGNAL('clicked()'), s2)
        s1.addTransition(button.clicked, s2)

        machine.addState(s1)
        machine.addState(s2)
        machine.setInitialState(s1)
        machine.start()

        self.setCentralWidget(button)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()