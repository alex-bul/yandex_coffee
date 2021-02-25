import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

COLUMNS = ["ID", 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки']


class Example(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()
        self.pushButton.clicked.connect(self.openDialog)

    def initUI(self):
        # Зададим тип базы данных
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('coffee.sqlite3')
        # И откроем подключение
        db.open()
        # QTableView - виджет для отображения данных из базы
        view = self.tableView
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()

        for i, name in enumerate(COLUMNS):
            model.setHeaderData(i, Qt.Horizontal, name)

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)

    def openDialog(self):
        dialog = PreDialog(self)
        dialog.show()

    def update_sql(self):
        self.initUI()


class PreDialog(QDialog):
    def __init__(self, parent=None):  # + parent
        super(PreDialog, self).__init__(parent)  #
        self.parent = parent  #
        uic.loadUi('addEditCoffeeForm.ui', self)
        conn = sqlite3.connect('coffee.sqlite3')
        conn.cursor().execute(self.textEdit.toPlainText())
        conn.commit()
        self.pushButton.clicked.connect(self.close_d)

    def close_d(self):
        self.close()

    def closeEvent(self, event):  # +++
        self.parent.update_sql()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
