#!/usr/bin/python
import sys

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal
from PyQt4 import QtCore, QtGui

class WorkerSignals(QObject):
    result = pyqtSignal(int)

class Worker(QRunnable):
    def __init__(self, task):
        super(Worker, self).__init__()

        self.task = task
        self.signals = WorkerSignals()

    def run(self):
        print 'Sending', self.task
        self.signals.result.emit(self.task)

class Tasks(QObject):
    def __init__(self):
        super(Tasks, self).__init__()

        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(10)
        self.pool.setExpiryTimeout(1)
    
    def process_result(self, task):
        print 'Receiving', task

    def start(self):
        for task in range(10):
            worker = Worker(task)
            worker.setAutoDelete(True)
            worker.signals.result.connect(self.process_result)

            self.pool.start(worker)

        #self.pool.waitForDone()
        QtCore.QCoreApplication.instance().quit()
    
        

if __name__ == "__main__":
    import  sys

    app = QApplication(sys.argv)
    main = Tasks()
    main.start()
    sys.exit(app.exec_())