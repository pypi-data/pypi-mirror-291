
from MethnaniSahbi.MethnaniSahbi import Employee
from PyQt5.QtWidgets import QApplication
import sys 
"""class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.window=Employee()
        self.window.show()
        self.close()"""
if __name__=="__main__":
    app= QApplication(sys.argv)
    window=Employee()
    window.show()
    sys.exit(app.exec())




    