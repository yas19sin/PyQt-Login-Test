import sys
from PyQt5 import QtWidgets, uic
import MySQLdb as mysql

db = mysql.connect(host="db4free.net", user="code_jammers", passwd="eb1bbafb", db="e_electricians")
# the design
login_form = "designe/login_form.ui"
Home_form = "designe/Home_form.ui"
logged_in = False
user = 'Admin'


class Home(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi(Home_form)
        self.ui.diconnect_btn.clicked.connect(self.disconnect)

    def init_ui(self):
        self.ui.main_title.setText('Home [%s]' % user)
        self.ui.welcome.setText('Welcome to your Home')

    def show_form(self):
        self.show()

    def disconnect(self):
        self.hide()


class Login(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi(login_form)
        self.ui.connect_btn.clicked.connect(self.connect)

    def set_ui(self):
        self.ui.Logging_info.resize(300, 17)
        self.ui.title.resize(100, 10)
        self.ui.Logging_info.setText('Welcome, Please Login')
        self.ui.setFixedSize(470, 230)
        self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

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
        global user
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        if db.open:
            print('successfully connected to database')
            cur = db.cursor()
            # cur.execute("SELECT * FROM Users")
            cur.execute('SELECT * FROM Users WHERE username = %s and password = %s', (username, password))
            data = cur.fetchone()
            # for users in data:
            if data != None:  # users[0] == username and users[1] == password:
                user = username
                print('Hello [%s] You are logging in, successfully' % user)
                QtWidgets.QMessageBox.about(self, 'Logged in', 'Hello [%s] Congrats you just logged in' % user)
            else:
                QtWidgets.QMessageBox.critical(self, 'Error', 'Wrong Username or Password')
                print('wrong username or password')
            # this was just a test to see if how to insert data to database
            # cur.execute("INSERT IGNORE INTO Users(username,password) VALUES ('%s', '%s')" % (ur_username, ur_password))
            # db.commit()
            cur.close()
        else:
            print('error connecting')

    def quit(self):
        raise SystemExit

    def about(self):
        QtWidgets.QMessageBox.about(self, 'About', 'this is just a learning app made by yas19sin to learn from')

    def connected(self):
        return logged_in


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    Login_form = Login()
    Login_form.set_ui()
    Login_form.create_menu_bar()
    Login_form.show_ui()
    home_form = Home()

    sys.exit(app.exec_())
