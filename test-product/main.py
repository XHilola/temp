import math
from math import ceil


from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QComboBox, \
    QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
import pymysql


def back_change():
    change_oyna.hide()
    oyna.show()
def back_delete():
    delete_oyna.hide()
    oyna.show()
def back_add():
    add_oyna.hide()
    oyna.show()
def add():
    oyna.hide()
    add_oyna.show()
def delete():
    oyna.hide()
    delete_oyna.show()
def change():
    oyna.hide()
    change_oyna.show()


class Mahsulotlar(QWidget):
    def __init__(self, connection, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.cursor = cursor

        self.CURRENT_PAGE = current_page


        self.resize(800, 500)
        self.setWindowTitle("Mahsulotlar bazasi")

        layout = QVBoxLayout()
        layout.setContentsMargins(20,30,20,30)
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Mahsulot qidirish...")
        self.search.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout1.addWidget(self.search)


        self.word1 = QLabel("Kategoriya:")
        self.word1.setStyleSheet("font-size: 18px")
        hlayout1.addWidget(self.word1)

        self.box1 = QComboBox()
        self.box1.setStyleSheet("font-size: 18px; padding: 8px")
        # self.box1.addItems()
        self.load_category()
        hlayout1.addWidget(self.box1)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nomi", "Narxi", "Kategoriya"])
        self.show_data()

        self.button1 = QPushButton(" ➕ Qo'shish")
        self.button1.setStyleSheet("font-size: 18px; padding: 8px")
        self.button1.clicked.connect(add)
        hlayout2.addWidget(self.button1)

        self.button2 = QPushButton(" 🖊 Tahrirlash")
        self.button2.setStyleSheet("font-size: 18px; padding: 8px")
        self.button2.clicked.connect(change)
        hlayout2.addWidget(self.button2)

        self.button3 = QPushButton(" 🗑 O'chirish")
        self.button3.setStyleSheet("font-size: 18px; padding: 8px")
        self.button3.clicked.connect(delete)
        hlayout2.addWidget(self.button3)
        hlayout2.addStretch()

        self.word2 = QLabel("Sahifa: 0")
        self.word2.setStyleSheet("font-size: 18px")
        hlayout2.addWidget(self.word2)

        self.word2_1 = QLabel(" 🔼\n"
                              " 🔽")
        hlayout2.addWidget(self.word2_1)

        hlayout3.addStretch()

        self.button4 = QPushButton(" ◀ Orqaga")
        self.button4.setStyleSheet("font-size: 18px; padding: 8px")
        self.button4.clicked.connect(self.orqaga)
        hlayout3.addWidget(self.button4)

        self.button5 = QPushButton("Keyingi ▶")
        self.button5.setStyleSheet("font-size: 18px; padding: 8px")
        self.button5.clicked.connect(self.oldinga)
        hlayout3.addWidget(self.button5)

        layout.addLayout(hlayout1)
        layout.addWidget(self.table)
        layout.addLayout(hlayout2)
        layout.addLayout(hlayout3)
        self.setLayout(layout)

        self.search.textChanged.connect(self.show_data)
        self.box1.currentIndexChanged.connect(self.show_data)

    def load_category(self):


        sql = "select id, name from categories"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            self.box1.addItem(row[1])

    def oldinga(self):
        if self.CURRENT_PAGE < self.MAX_PAGE:# self.page_size()-1:
            self.CURRENT_PAGE +=1
            self.show_data()
            self.word2.setText(f"Sahifa: {self.CURRENT_PAGE}")

    def orqaga(self):
        if self.CURRENT_PAGE >0:
            self.CURRENT_PAGE -= 1
            self.show_data()
            self.word2.setText(f"Sahifa: {self.CURRENT_PAGE}")

    def page_size(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        rows = cursor.fetchall()
        return ceil(len(rows) / PAGE_SIZE)
    def check(self):
        if self.search.text() == "":
            self.show_data()
    def show_data(self):
        sql = f"""select p.id,p.name, p.price , c.name
                    from products p
                    left join categories c  on p.category_id=c.id
                    where 1=1         
                  
                    """

        params = []

        # search
        if self.search.text().strip():
            sql += f" and p.name like %s "
            params.append(f"{self.search.text().strip()}%")

                   # "# and c.id=%s
                    # and p.name like %s
        # category
        category = self.box1.currentText()
        sql += " and c.name=%s "
        params.append(category)


        # sonini aniqlash
        self.cursor.execute(sql, params)
        rows = self.cursor.fetchall()
        self.MAX_PAGE = math.ceil(len(rows)/PAGE_SIZE)


        # pagination
        sql += f""" limit {PAGE_SIZE} offset {PAGE_SIZE*self.CURRENT_PAGE}"""

        print(sql)
        print(params)
        self.cursor.execute(sql, params)
        rows = self.cursor.fetchall()



        self.table.setRowCount(len(rows))
        for i,row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(row[3])))

    # def show_data_(self):
    #     sql = f"Select * from products where  limit {PAGE_SIZE} offset {PAGE_SIZE*self.CURRENT_PAGE}"
    #     self.cursor.execute(sql)
    #     rows = self.cursor.fetchall()
    #
    #     self.table.setRowCount(len(rows))
    #     for i,row in enumerate(rows):
    #         self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
    #         self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
    #         self.table.setItem(i, 2, QTableWidgetItem(str(row[5])))
    def search_data(self):
        a = self.search.text()
        sql = f"Select * from products where name like \"%{a}%\" "
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            if self.search.text().lower() in row[1].lower():
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row[5])))
    def category_(self):
        if self.box1.currentIndex()!=0:
            sql = f"Select * from products where category_id = {self.box1.currentIndex()}"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                if self.search.text().lower() in row[1].lower():
                    self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                    self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
                    self.table.setItem(i, 2, QTableWidgetItem(str(row[5])))
        else:
            self.show_data()

class Add(QWidget):
    def __init__(self, connection, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.cursor = cursor

        self.resize(500, 400)
        self.setWindowTitle("Mahsulot qo'shish")

        layout = QVBoxLayout()
        layout.setContentsMargins(50,30,50,30)
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()
        hlayout4 = QHBoxLayout()

        self.word1 = QLabel("Mahsulot qo'shish uchun quydagilarni to'ldiring!")
        self.word1.setStyleSheet("font-size: 27px; color: green")
        hlayout1.addWidget(self.word1)

        self.word2 = QLabel("Mahsulot nomi:")
        self.word2.setStyleSheet("font-size: 18px")
        hlayout2.addWidget(self.word2)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Mahsulot nomini kiriting...")
        self.name.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout2.addWidget(self.name)

        self.word3 = QLabel("Mahsulot narxi:")
        self.word3.setStyleSheet("font-size: 18px")
        hlayout3.addWidget(self.word3)

        self.price = QLineEdit()
        self.price.setPlaceholderText("Mahsulot narxini kiriting...")
        self.price.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout3.addWidget(self.price)

        hlayout4.addStretch()

        self.button1 = QPushButton("Orqaga")
        self.button1.setStyleSheet("font-size: 18px; padding: 8px; background-color: blue; color: white")
        self.button1.clicked.connect(back_add)
        hlayout4.addWidget(self.button1)

        self.button2 = QPushButton("Qo'shish")
        self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: lightblue; color: white")
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.add_date)
        hlayout4.addWidget(self.button2)

        layout.addLayout(hlayout1)
        layout.addLayout(hlayout2)
        layout.addLayout(hlayout3)
        layout.addLayout(hlayout4)
        self.setLayout(layout)

        self.name.textChanged.connect(self.check)
        self.price.textChanged.connect(self.check)

    def check(self):
        if self.name.text() == "" or self.price.text() == "":
            self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: lightblue; color: white")
            self.button2.setEnabled(False)
        else:
            self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: blue; color: white")
            self.button2.setEnabled(True)
    def add_date(self):
        sql = "insert into products(name,price) values(%s, %s)"
        params = (self.name.text(), self.price.text())
        self.cursor.execute(sql, params)
        self.connection.commit()

        oyna.show_data()

        self.name.setText("")
        self.price.setText("")
        QMessageBox.information(self,"Qo'shish", "Muvaffaqiyatli qo'shildi!")

class Delete(QWidget):
    def __init__(self, connection, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.cursor = cursor

        self.resize(500, 400)
        self.setWindowTitle("Mahsulot o'chirish")

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()

        self.word1 = QLabel("Mahsulot o'chirish uchun quydagilarni to'ldiring!")
        self.word1.setStyleSheet("font-size: 27px; color: green")
        hlayout1.addWidget(self.word1)

        self.word2 = QLabel("Mahsulot Idsi:")
        self.word2.setStyleSheet("font-size: 18px")
        hlayout2.addWidget(self.word2)

        self.Id = QLineEdit()
        self.Id.setPlaceholderText("Mahsulot Idini kiriting...")
        self.Id.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout2.addWidget(self.Id)

        hlayout3.addStretch()

        self.button1 = QPushButton("Orqaga")
        self.button1.setStyleSheet("font-size: 18px; padding: 8px; background-color: blue; color: white")
        self.button1.clicked.connect(back_delete)
        hlayout3.addWidget(self.button1)

        self.button2 = QPushButton("O'chirish")
        self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: lightblue; color: white")
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.delete_data)
        hlayout3.addWidget(self.button2)

        layout.addLayout(hlayout1)
        layout.addLayout(hlayout2)
        layout.addLayout(hlayout3)
        self.setLayout(layout)

        self.Id.textChanged.connect(self.check)

    def check(self):
        if self.Id.text() == "":
            self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: lightblue; color: white")
            self.button2.setEnabled(False)
        else:
            self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: blue; color: white")
            self.button2.setEnabled(True)

    def delete_data(self):
        sql = "delete from products where id = %s"
        params = (self.Id.text(),)
        self.cursor.execute(sql, params)
        self.connection.commit()

        oyna.show_data()

        self.Id.setText("")
        QMessageBox.information(self, "O'chirish", "Muvaffaqiyatli o'chirildi!")

class Change(QWidget):
    def __init__(self, connection, cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.cursor = cursor

        self.resize(500, 400)
        self.setWindowTitle("Mahsulot qo'shish")

        layout = QVBoxLayout()
        layout.setContentsMargins(50,30,50,30)
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()
        hlayout4 = QHBoxLayout()
        hlayout5 = QHBoxLayout()

        self.word1 = QLabel("Mahsulot qo'shish uchun quydagilarni to'ldiring!")
        self.word1.setStyleSheet("font-size: 27px; color: green")
        hlayout1.addWidget(self.word1)

        self.word2 = QLabel("Mahsulot Idsi:")
        self.word2.setStyleSheet("font-size: 18px")
        hlayout2.addWidget(self.word2)

        self.Id = QLineEdit()
        self.Id.setPlaceholderText("Mahsulot Idsini kiriting...")
        self.Id.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout2.addWidget(self.Id)

        self.word3 = QLabel("Mahsulot yangi nomi:")
        self.word3.setStyleSheet("font-size: 18px")
        hlayout3.addWidget(self.word3)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Mahsulot yangi nomini kiriting...")
        self.name.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout3.addWidget(self.name)

        self.word4 = QLabel("Mahsulotning yangi narxi:")
        self.word4.setStyleSheet("font-size: 18px")
        hlayout4.addWidget(self.word4)

        self.price = QLineEdit()
        self.price.setPlaceholderText("Mahsulotning yangi narxini kiriting...")
        self.price.setStyleSheet("font-size: 18px; padding: 8px")
        hlayout4.addWidget(self.price)

        hlayout5.addStretch()

        self.button1 = QPushButton("Orqaga")
        self.button1.setStyleSheet("font-size: 18px; padding: 8px; background-color: blue; color: white")
        self.button1.clicked.connect(back_change)
        hlayout5.addWidget(self.button1)

        self.button2 = QPushButton("O'zgartirish")
        self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: lightblue; color: white")
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.change_date)
        hlayout5.addWidget(self.button2)

        layout.addLayout(hlayout1)
        layout.addLayout(hlayout2)
        layout.addLayout(hlayout3)
        layout.addLayout(hlayout4)
        layout.addLayout(hlayout5)
        self.setLayout(layout)

        self.Id.textChanged.connect(self.check)
        self.name.textChanged.connect(self.check)
        self.price.textChanged.connect(self.check)

    def check(self):
        if self.name.text() == "" or self.price.text() == "" or self.Id.text() == "":
            self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: lightblue; color: white")
            self.button2.setEnabled(False)
        else:
            self.button2.setStyleSheet("font-size: 18px; padding: 8px; background-color: blue; color: white")
            self.button2.setEnabled(True)
    def change_date(self):
        sql = "update products set name = %s, price = %s where id = %s"
        params = (self.name.text(), self.price.text(), self.Id.text())
        self.cursor.execute(sql, params)
        self.connection.commit()

        oyna.show_data()

        self.Id.setText("")
        self.name.setText("")
        self.price.setText("")
        QMessageBox.information(self,"O'zgartirish", "Muvaffaqiyatli o'zgartirildi!")


try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='organization_db'
    )
    print("Baza ulandi")
except Exception as e:
    print("Xato:", e)

cursor = connection.cursor()

app = QApplication([])

PAGE_SIZE = 5
current_page = 0
a=0

oyna = Mahsulotlar(connection,cursor)
add_oyna = Add(connection,cursor)
delete_oyna = Delete(connection, cursor)
change_oyna = Change(connection, cursor)
oyna.show()

app.exec_()