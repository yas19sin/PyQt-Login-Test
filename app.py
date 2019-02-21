import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox as MBox
import MySQLdb as mysql

# TODO: next up add sign up funcionality

db = mysql.connect(host="db4free.net", user="code_jammers",
                   passwd="eb1bbafb", db="e_electricians")
# the design
login_form = "designe/login_form.ui"
Home_form = "designe/Home_form.ui"
logged_in = False
# user = 'Admin'


class Home(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        self.home = uic.loadUi(Home_form)
        self.home.diconnect_btn.clicked.connect(self.disconnect)

    def setHome(self, user):
        bar = self.home.menubar
        File = bar.addMenu('File')
        disconnect_action = QtWidgets.QAction('Disconnect', self)
        disconnect_action.setShortcut('Ctrl+D')
        File.addAction(disconnect_action)
        disconnect_action.triggered.connect(self.disconnect)

        self.home.setFixedSize(350, 300)
        self.home.diconnect_btn.setText('Disconnect')
        self.home.main_title.setText('Home [%s]' % user)
        self.home.main_title.resize(100, 20)
        self.home.welcome.setText('Welcome %s to your Home' % user)
        self.home.welcome.resize(150, 20)

    def show_ui(self):
        self.home.show()

    def disconnect(self):
        self.home.hide()
        self.login = Login()
        self.login.set_ui()
        self.login.show_ui()


class Login(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.ui = uic.loadUi(login_form)
        self.ui.connect_btn.clicked.connect(self.connect)

    def set_ui(self):
        self.ui.Logging_info.resize(300, 17)
        self.ui.title.resize(100, 10)
        self.ui.title.setText('PyQt5 MySQL Test')
        self.ui.Logging_info.setText('Welcome, Please Login')
        self.ui.setFixedSize(470, 230)
        self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_menu_bar()

    def create_menu_bar(self):
        bar = self.ui.menuBar

        File = bar.addMenu('File')
        Help = bar.addMenu('Help')

        connect_action = QtWidgets.QAction('Connect', self)
        connect_action.setShortcut('Ctrl+C')

        quit_action = QtWidgets.QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')

        about_action = QtWidgets.QAction('About', self)
        about_action.setShortcut('Ctrl+H')

        File.addAction(connect_action)
        File.addAction(quit_action)
        Help.addAction(about_action)

        connect_action.triggered.connect(self.connect)
        quit_action.triggered.connect(self.quit)
        about_action.triggered.connect(self.about)

    def show_ui(self):
        self.ui.show()

    # just a check for now nothing too important
    def connect(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        if db.open:
            print('successfully connected to database')
            cur = db.cursor()
            cur.execute('SELECT * FROM Users WHERE username = %s '
                        'and password = %s', (username, password))
            data = cur.fetchone()
            # for users in data:
            if data is not None:
                user = username
                print('Hello [%s] You are logging in, successfully' % user)
                MBox.about(self, 'Log in', 'Hello %s, you logged in' % user)
                self.ui.password_input.setText('')
                self.ui.username_input.setText('')
                self.home = Home()
                self.home.setHome(user=user)
                self.home.show_ui()
                self.ui.hide()
            else:
                MBox.critical(self, 'Error', 'Wrong Username or Password')
                print('wrong username or password')
            # this was just a test to see if how to insert data to database
            # cur.execute("INSERT IGNORE INTO Users(username,password)
            # VALUES ('%s', '%s')" % (ur_username, ur_password))
            # db.commit()
            cur.close()
        else:
            MBox.critical(self, 'Error', 'Couldn\'t connect to database')
            print('error connecting to database')

    def quit(self):
        raise SystemExit

    def about(self):
        MBox.about(self, 'About', 'this is app was made to train and learn')

    def connected(self):
        return logged_in


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    Login_form = Login()
    Login_form.set_ui()
    # Login_form.create_menu_bar()
    Login_form.show_ui()

    sys.exit(app.exec_())
