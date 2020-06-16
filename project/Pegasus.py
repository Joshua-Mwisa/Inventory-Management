from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import qdarkstyle
import psycopg2
import datetime
import time
import sys
import csv
import os

try:
    connection = psycopg2.connect(
        database='inventory',
        port='5432',
        host='localhost',
        password='demo',
        user='postgres'
    )
    connection.commit()

except Exception:
    print('Database is non-existent')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.title = "Pegasus"
        self.iconName = "../images/success (6)"
        self.left = 150
        self.top = 50
        self.width = 1050
        self.height = 600

        pegaus = Application()
        self.setCentralWidget(pegaus)

        self.initWindow()

    def closeEvent(self, event, *args, **kwargs):
        reply = QtWidgets.QMessageBox.question(self, 'Are you sure?', 'Are you sure you want to exit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def initWindow(self):

        self.setWindowTitle(self.title)
        # left, top, width, height
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.iconName))

        pixmap = QtGui.QPixmap("../images/splash_screen")
        pixmap.setDevicePixelRatio(1.5)

        splash_screen = QtWidgets.QSplashScreen(pixmap)
        splash_screen.setGeometry(150, 50, 1050, 600)
        splash_screen.show()

        for i in range(3):
            time.sleep(.2)

        # Tool_bar
        # =============
        toolbar = QtWidgets.QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar_add_action = QtWidgets.QAction(QtGui.QIcon('../images/add_prod'), 'Add', self)
        toolbar_add_action.setStatusTip('Add')

        toolbar_exit_action = QtWidgets.QAction(QtGui.QIcon('../images/close_prod'), 'Exit', self)
        toolbar_exit_action.setStatusTip('Exit')
        toolbar_exit_action.triggered.connect(self.close)

        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")
        system_date = QtWidgets.QLabel()
        system_date.setText(str(date))
        # date = now.strftime("%B %d, %Y %H:%M:%S")

        toolbar.addAction(toolbar_add_action)
        toolbar.addAction(toolbar_exit_action)
        toolbar.addWidget(system_date)

        # Status_bar
        # =============
        statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(statusbar)

        file_menu = self.menuBar().addMenu('File')
        about_menu = self.menuBar().addMenu('About')

        # File Menu
        # ============
        add_action = QtWidgets.QAction(QtGui.QIcon('../images/add_prod'), 'Add', self)
        add_action.setStatusTip('Add')
        file_menu.addAction(add_action)

        file_menu.addSeparator()

        exit_action = QtWidgets.QAction(QtGui.QIcon('../images/close_prod'), 'Exit', self)
        exit_action.setStatusTip('Exit')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # About Menu
        # ============
        about_action = QtWidgets.QAction(QtGui.QIcon('../images/success (6)'), 'About Software', self)
        about_action.setStatusTip('About Software')
        about_action.triggered.connect(self.about)
        about_menu.addAction(about_action)

        self.show()

    def about(self):
        about_action = About_Action()
        about_action.exec_()


class Application(QtWidgets.QWidget):
    def __init__(self):
        super(Application, self).__init__()

        # menu frame

        menu_layout = QtWidgets.QVBoxLayout()

        menu_frame = QtWidgets.QFrame()
        menu_frame.setLayout(menu_layout)

        menu_scroll = QtWidgets.QScrollArea()
        menu_scroll.setWidget(menu_frame)
        menu_scroll.setWidgetResizable(True)
        menu_scroll.setFixedWidth(205)
        menu_scroll.setMaximumHeight(640)

        menu_content = MenuAction()
        menu_layout.addWidget(menu_content)

        # Content widget (Stacked Widget)

        self.dashboard = QtWidgets.QWidget()
        menu_content.dashboard.clicked.connect(self.dashboard_display)

        self.suppliers = QtWidgets.QWidget()
        menu_content.contacts.clicked.connect(self.suppliers_display)

        self.products = QtWidgets.QWidget()
        menu_content.products.clicked.connect(self.products_display)

        self.sales = QtWidgets.QWidget()
        menu_content.sales.clicked.connect(self.sales_display)

        self.invoices = QtWidgets.QWidget()
        menu_content.invoices.clicked.connect(self.invoices_display)

        self.orders = QtWidgets.QWidget()
        menu_content.orders.clicked.connect(self.orders_display)

        self.bills = QtWidgets.QWidget()
        menu_content.bills.clicked.connect(self.bills_display)

        self.reports = QtWidgets.QWidget()
        menu_content.reports.clicked.connect(self.reports_display)

        self.dashboardUI()
        self.contactsUI()
        self.productsUI()
        self.sales_ui()
        self.invoicesUI()
        self.ordersUI()
        self.billsUI()
        self.reportsUI()

        self.stack = QtWidgets.QStackedWidget(self)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.suppliers)
        self.stack.addWidget(self.products)
        self.stack.addWidget(self.sales)
        self.stack.addWidget(self.invoices)
        self.stack.addWidget(self.orders)
        self.stack.addWidget(self.bills)
        self.stack.addWidget(self.reports)
        self.stack.setCurrentWidget(self.dashboard)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(menu_scroll)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    # menu button actions

    def dashboard_display(self):
        self.stack.setCurrentWidget(self.dashboard)

    def suppliers_display(self):
        self.stack.setCurrentWidget(self.suppliers)

    def products_display(self):
        self.stack.setCurrentWidget(self.products)

    def sales_display(self):
        self.stack.setCurrentWidget(self.sales)

    def invoices_display(self):
        pass

    def orders_display(self):
        self.stack.setCurrentWidget(self.orders)

    def bills_display(self):
        pass

    def reports_display(self):
        self.stack.setCurrentWidget(self.reports)

    # once dashboard button is clicked (from menu)

    def dashboardUI(self):
        tab_widget = QtWidgets.QTabWidget()

        self.products_tab = QtWidgets.QWidget()
        self.contacts_tab = QtWidgets.QWidget()
        self.order_tab = QtWidgets.QWidget()

        tab_widget.addTab(self.products_tab, "Products")
        tab_widget.addTab(self.contacts_tab, "Contacts")
        tab_widget.addTab(self.order_tab, "Orders")

        self.view_products_UI()
        self.view_contacts_tab_UI()
        self.view_orders_tab_ui()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tab_widget)

        self.dashboard.setLayout(layout)

    # products tab under dashboard

    def view_products_UI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.products_table = Table()
        self.products_table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.products_table.content_groupbox.setTitle('Products')
        self.products_table.table.setColumnCount(12)
        self.products_table.table.setHorizontalHeaderLabels(('Product_id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Product quantity', 'Product quantifier', 'Total B.Price',
                                                             'Total S.Price', 'Total Profit', 'Notes'))
        self.products_table.add_button.clicked.connect(self.add_products_UI)
        self.products_table.refresh_button.clicked.connect(self.refresh_products_UI)

        cursor = connection.cursor()
        cursor.execute('select product_id, product_name, product_size, product_category, '
                       'product_buying_price, product_selling_price, product_selling_price - product_buying_price, '
                       'product_quantity, product_quantifier, product_pack_bp, product_pack_sp, product_pack_sp - product_pack_bp, '
                       'product_notes from products order by product_name;')

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.products_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.products_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.products_table.table.rowCount()
        self.prod_total_label = QtWidgets.QLabel('Total: ' + str(total))

        self.products_table.content_overall_layout.addWidget(self.prod_total_label)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        self.search_products_panel_ = QtWidgets.QLineEdit()
        self.search_products_panel_.textChanged.connect(self.search_products_action)
        self.search_products_panel_.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignRight)
        search_layout.addWidget(self.search_products_panel_)
        search_layout.addWidget(search_products_btn)

        layout.addLayout(search_layout)
        layout.addWidget(self.products_table)

        self.products_tab.setLayout(layout)

    def search_products_action(self):
        self.products_table.table.clear()
        self.products_table.table.setRowCount(0)
        self.products_table.table.setHorizontalHeaderLabels(('Product_id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Product quantity', 'Product quantifier',
                                                             'Total B.Price', 'Total S.Price', 'Total Profit', 'Notes'))
        product_name = self.search_products_panel_.text() + "%"

        cursor = connection.cursor()
        cursor.execute("select product_id, product_name, product_size, product_category, "
                       "product_buying_price, product_selling_price, product_selling_price - product_buying_price, "
                       "product_quantity, product_quantifier, product_pack_bp, product_pack_sp, product_pack_sp - product_pack_bp, "
                       "product_notes from products where product_name ilike '%s' order by product_name" % product_name)

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.products_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.products_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.products_table.table.rowCount()
        self.prod_total_label.setText('Total: ' + str(total))

    # add product btn

    def add_products_UI(self):
        product_add = ProductAdd()
        product_add.exec_()

    # refresh product btn

    def refresh_products_UI(self):
        self.products_table.table.clear()
        self.products_table.table.setRowCount(0)
        self.products_table.table.setColumnCount(12)
        self.products_table.table.setHorizontalHeaderLabels(('Product_id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Product quantity', 'Product quantifier', 'Total B.Price',
                                                             'Total S.Price', 'Total Profit', 'Notes'))

        cursor = connection.cursor()
        cursor.execute('select product_id, product_name, product_size, product_category, '
                       'product_buying_price, product_selling_price, product_selling_price - product_buying_price, '
                       'product_quantity, product_quantifier, product_pack_bp, product_pack_sp, product_pack_sp - product_pack_bp, '
                       'product_notes from products order by product_name;')

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.products_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.products_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.products_table.table.rowCount()
        self.prod_total_label.setText('Total: ' + str(total))

    # contacts tab under dashboard

    def view_contacts_tab_UI(self):
        self.contact_table = Table()
        self.contact_table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.contact_table.content_groupbox.setTitle('Contacts')
        self.contact_table.table.setColumnCount(11)
        self.contact_table.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                            'Last Name', 'Contact Type', 'Location',
                                                            'Phone number', 'E-mail'))
        self.contact_table.add_button.clicked.connect(self.contact_add_UI)
        self.contact_table.refresh_button.clicked.connect(self.contact_refresh_ui)

        cursor = connection.cursor()
        cursor.execute('select contact_id, contact_work_company, contact_display_name, '
                       'contact_first_name, contact_last_name, '
                       'contact_type, contact_location, contact_phone_number, '
                       'contact_email '
                       'from contacts order by contact_work_company;')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.contact_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.contact_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.contact_table.table.rowCount()
        self.contact_total_label = QtWidgets.QLabel('Total: ' + str(total))

        self.contact_table.content_overall_layout.addWidget(self.contact_total_label)

        search_contact_btn = QtWidgets.QPushButton('Search')
        search_contact_btn.setFixedWidth(100)
        self.search_contact_label = QtWidgets.QLineEdit()
        self.search_contact_label.textChanged.connect(self.search_contact_action)
        self.search_contact_label.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignRight)
        search_layout.addWidget(self.search_contact_label)
        search_layout.addWidget(search_contact_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(search_layout)
        layout.addWidget(self.contact_table)
        self.contacts_tab.setLayout(layout)

    def search_contact_action(self):
        self.contact_table.table.clear()
        self.contact_table.table.setRowCount(0)
        self.contact_table.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                            'Last Name', 'Contact Type', 'Location',
                                                            'Phone number', 'E-mail'))
        contact_first_name = self.search_contact_label.text() + "%"

        cursor = connection.cursor()
        cursor.execute("select contact_id, contact_work_company, contact_display_name, "
                       "contact_first_name, contact_last_name, "
                       "contact_type, contact_location, contact_phone_number, "
                       "contact_email from contacts where contact_first_name ilike '%s' order by contact_work_company" % contact_first_name)

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.contact_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.contact_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.contact_table.table.rowCount()
        self.contact_total_label.setText('Total: ' + str(total))

    # add contact btn

    def contact_add_UI(self):
        contact_add = ContactAdd()
        contact_add.exec_()

    # refresh contact btn

    def contact_refresh_ui(self):
        self.contact_table.table.clear()
        self.contact_table.table.setRowCount(0)
        self.contact_table.table.setColumnCount(11)
        self.contact_table.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                            'First Name', 'Contact Type', 'Location',
                                                            'Phone number', 'E-mail'))

        cursor = connection.cursor()
        cursor.execute('select contact_id, contact_work_company, contact_display_name, '
                       'contact_first_name, contact_last_name, '
                       'contact_type, contact_location, contact_phone_number, '
                       'contact_email '
                       'from contacts order by contact_work_company;')

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.contact_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.contact_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.contact_table.table.rowCount()
        self.total_label.setText('Total: ' + str(total))

    # orders tab under dashboard

    def view_orders_tab_ui(self):
        self.orders_table = Table()
        self.orders_table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.orders_table.content_groupbox.setTitle('Orders')
        self.orders_table.table.setColumnCount(12)
        self.orders_table.table.setHorizontalHeaderLabels(('Order id', 'Order title', 'Order urgency', 'product name',
                                                           'Product buying price', 'Product selling price',
                                                           'Product quantity', 'Product quantifier', 'Product size', 'Supplier name',
                                                           'Supplier phone number', 'Supplier email', 'Order notes'))
        self.orders_table.edit_button.hide()
        self.orders_table.refresh_button.hide()
        self.orders_table.remove_button.hide()

        cursor = connection.cursor()
        cursor.execute('''select order_id, order_title, order_urgency, product_name, 
                               product_buying_price, product_selling_price,
                               product_quantity, product_quantifier, product_size, supplier_name, 
                               supplier_phone_number, supplier_email, order_notes 
                               from orders order by order_title;''')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.orders_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.orders_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        self.orders_table.add_button.setText('Order')
        self.orders_table.add_button.clicked.connect(self.make_order_ui)
        total = self.orders_table.table.rowCount()

        self.orders_total_label = QtWidgets.QLabel('Total: ' + str(total))
        self.orders_table.content_overall_layout.addWidget(self.orders_total_label)

        make_oder_btn = QtWidgets.QPushButton('Make order')
        make_oder_btn.clicked.connect(self.make_order_ui)
        make_oder_btn.setFixedWidth(300)

        search_orders_btn = QtWidgets.QPushButton('Search')
        search_orders_btn.setFixedWidth(100)
        self.search_orders_panel = QtWidgets.QLineEdit()
        self.search_orders_panel.textChanged.connect(self.search_orders_action)
        self.search_orders_panel.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignRight)
        search_layout.addWidget(self.search_orders_panel)
        search_layout.addWidget(search_orders_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(search_layout)
        layout.addWidget(self.orders_table)
        # layout.addWidget(make_oder_btn)
        self.order_tab.setLayout(layout)

    def search_orders_action(self):
        self.orders_table.table.clear()
        self.orders_table.table.setRowCount(0)
        self.orders_table.table.setHorizontalHeaderLabels(('Order id', 'Order title', 'Order urgency', 'product name',
                                                           'Product buying price', 'Product selling price',
                                                           'Product quantity', 'Product quantifier', 'Product size', 'Supplier name',
                                                           'Supplier phone number', 'Supplier email', 'Order notes'))
        product_name = self.search_orders_panel.text() + "%"

        cursor = connection.cursor()
        cursor.execute('''select order_id, order_title, order_urgency, product_name, 
                               product_buying_price, product_selling_price,
                               product_quantity, product_quantifier, product_size, supplier_name, 
                               supplier_phone_number, supplier_email, order_notes 
                               from orders where product_name ilike '%s' order by order_title''' % product_name)

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.orders_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.orders_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.orders_table.table.rowCount()
        self.orders_total_label.setText('Total: ' + str(total))
    # Make order btn command

    def make_order_ui(self):
        order = MakeOrder()
        order.exec_()

    # once contacts button is clicked (from menu)

    def contactsUI(self):

        layout = QtWidgets.QHBoxLayout()
        tab = QtWidgets.QTabWidget()

        self.view_contacts_tab = QtWidgets.QWidget()
        self.add_contacts_tab = QtWidgets.QWidget()
        self.remove_contact_tab = QtWidgets.QWidget()

        tab.addTab(self.view_contacts_tab, 'View Contacts')
        tab.addTab(self.add_contacts_tab, 'Add Contacts')
        tab.addTab(self.remove_contact_tab, 'Remove Contacts')

        self.view_contacts_ui()
        self.add_contacts_ui()
        self.remove_contact_ui()

        layout.addWidget(tab)
        self.suppliers.setLayout(layout)

    # Contacts tabs

    def view_contacts_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.contact_table_ = Table()
        self.contact_table_.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.contact_table_.content_groupbox.setTitle('contacts')
        self.contact_table_.table.setColumnCount(11)
        self.contact_table_.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                             'First Name', 'Contact Type', 'Location',
                                                             'Phone number', 'E-mail'))
        self.contact_table_.add_button.hide()
        self.contact_table_.edit_button.hide()
        self.contact_table_.refresh_button.hide()
        self.contact_table_.remove_button.hide()

        cursor = connection.cursor()
        cursor.execute('select contact_id, contact_work_company, contact_display_name, '
                       'contact_first_name, contact_last_name, '
                       'contact_type, contact_location, contact_phone_number, '
                       'contact_email '
                       'from contacts order by contact_work_company;')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.contact_table_.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.contact_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.contact_table_.table.rowCount()
        self.total_contact_label = QtWidgets.QLabel('Total: ' + str(total))

        self.contact_table_.content_overall_layout.addWidget(self.total_contact_label)

        search_contacts_btn = QtWidgets.QPushButton('Search')
        search_contacts_btn.setFixedWidth(100)
        self.search_contacts_panel = QtWidgets.QLineEdit()
        self.search_contacts_panel.setPlaceholderText('Search contacts')
        self.search_contacts_panel.setFixedWidth(200)
        self.search_contacts_panel.textChanged.connect(self.contact_text_change_action)

        contact_type_label = QtWidgets.QLabel('Select contact type. ')
        self.contact_type = QtWidgets.QComboBox()
        self.contact_type.addItem('All')
        self.contact_type.addItem('Suppliers')
        self.contact_type.addItem('Customers')
        self.contact_type.addItem('Support')
        self.contact_type.currentTextChanged.connect(self.contact_type_change_action)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignLeft)
        search_layout.addWidget(search_contacts_btn)
        search_layout.addWidget(self.search_contacts_panel)
        search_layout.addWidget(contact_type_label, alignment=QtCore.Qt.AlignRight)
        search_layout.addWidget(self.contact_type)

        layout.addLayout(search_layout)
        layout.addWidget(self.contact_table_)

        self.view_contacts_tab.setLayout(layout)

    def contact_type_change_action(self):
        contact_type_selected = self.contact_type.currentText()
        if contact_type_selected == 'All':
            self.contact_table_.table.clear()
            self.contact_table_.table.setRowCount(0)
            self.contact_table_.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                                 'Last Name', 'Contact Type', 'Location',
                                                                 'Phone number', 'E-mail'))
            cursor = connection.cursor()
            cursor.execute("select contact_id, contact_work_company, contact_display_name, "
                           "contact_first_name, contact_last_name, "
                           "contact_type, contact_location, contact_phone_number, "
                           "contact_email "
                           "from contacts order by contact_work_company;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.contact_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.contact_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.contact_table_.table.rowCount()
            self.total_contact_label.setText('Total: ' + str(total))
        elif contact_type_selected == 'Suppliers':
            self.contact_table_.table.clear()
            self.contact_table_.table.setRowCount(0)
            self.contact_table_.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                                 'Last Name', 'Contact Type', 'Location',
                                                                 'Phone number', 'E-mail'))
            cursor = connection.cursor()
            cursor.execute("select contact_id, contact_work_company, contact_display_name, "
                           "contact_first_name, contact_last_name, "
                           "contact_type, contact_location, contact_phone_number, "
                           "contact_email "
                           "from contacts where contact_type = 'Supplier' order by contact_work_company;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.contact_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.contact_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.contact_table_.table.rowCount()
            self.total_contact_label.setText('Total: ' + str(total))

            print('suppliers')
        elif contact_type_selected == 'Customers':
            self.contact_table_.table.clear()
            self.contact_table_.table.setRowCount(0)
            self.contact_table_.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                                 'Last Name', 'Contact Type', 'Location',
                                                                 'Phone number', 'E-mail'))
            cursor = connection.cursor()
            cursor.execute("select contact_id, contact_work_company, contact_display_name, "
                           "contact_first_name, contact_last_name, "
                           "contact_type, contact_location, contact_phone_number, "
                           "contact_email "
                           "from contacts where contact_type = 'Customer' order by contact_work_company;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.contact_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.contact_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.contact_table_.table.rowCount()
            self.total_contact_label.setText('Total: ' + str(total))

            print('Customers')
        elif contact_type_selected == 'Support':
            self.contact_table_.table.clear()
            self.contact_table_.table.setRowCount(0)
            self.contact_table_.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                                 'Last Name', 'Contact Type', 'Location',
                                                                 'Phone number', 'E-mail'))
            cursor = connection.cursor()
            cursor.execute("select contact_id, contact_work_company, contact_display_name, "
                           "contact_first_name, contact_last_name, "
                           "contact_type, contact_location, contact_phone_number, "
                           "contact_email "
                           "from contacts where contact_type = 'Support' order by contact_work_company;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.contact_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.contact_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.contact_table_.table.rowCount()
            self.total_contact_label.setText('Total: ' + str(total))

            print('Support')

    def contact_text_change_action(self):
        self.contact_table_.table.clear()
        self.contact_table_.table.setRowCount(0)
        self.contact_table_.table.setHorizontalHeaderLabels(('Contact_id', 'Company', 'Display Name', 'First Name',
                                                             'Last Name', 'Contact Type', 'Location',
                                                             'Phone number', 'E-mail'))
        contact_name = self.search_contacts_panel.text() + "%"

        cursor = connection.cursor()
        cursor.execute("select contact_id, contact_work_company, contact_display_name, "
                       "contact_first_name, contact_last_name, "
                       "contact_type, contact_location, contact_phone_number, "
                       "contact_email "
                       "from contacts where contact_first_name ilike '%s' order by contact_first_name;" % contact_name)

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.contact_table_.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.contact_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.contact_table_.table.rowCount()
        self.total_contact_label.setText('Total: ' + str(total))

    def add_contacts_ui(self):

        contact_add = ContactAdd()
        contact_add.cancel_btn.hide()

        layout = QtWidgets.QFormLayout()
        layout.addWidget(contact_add)
        self.add_contacts_tab.setLayout(layout)

    def remove_contact_ui(self):
        layout = QtWidgets.QFormLayout()

        self.reduce_btn = QtWidgets.QPushButton('Reduce', self)
        cancel_btn = QtWidgets.QPushButton('Cancel', self)

        name = QtWidgets.QLineEdit()
        layout.addRow('Name', name)

        quanity = QtWidgets.QLineEdit()
        layout.addRow('Quantity', quanity)

        layout.addWidget(self.reduce_btn)
        layout.addWidget(cancel_btn)

        cancel_btn.clicked.connect(name.clear)
        cancel_btn.clicked.connect(quanity.clear)

        self.remove_contact_tab.setLayout(layout)

    # once products button is clicked (from menu)

    def productsUI(self):

        layout = QtWidgets.QHBoxLayout()
        tab = QtWidgets.QTabWidget()

        self.view_products = QtWidgets.QWidget()
        self.add_products = QtWidgets.QWidget()
        self.reduce_products = QtWidgets.QWidget()

        tab.addTab(self.view_products, 'View Products')
        tab.addTab(self.add_products, 'Add Products')
        tab.addTab(self.reduce_products, 'Reduce Products')

        self.view_products_ui()
        self.add_products_ui()
        self.reduce_products_ui()

        layout.addWidget(tab)
        self.products.setLayout(layout)

    # tab actions for products, for the menu buttons.

    def view_products_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.product_table_ = Table()
        self.product_table_.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.product_table_.content_groupbox.setTitle('Products')
        self.product_table_.table.setColumnCount(12)
        self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                             'Product quantity', 'Product quantifier', 'Notes'))
        self.product_table_.add_button.hide()
        self.product_table_.edit_button.hide()
        self.product_table_.refresh_button.hide()
        self.product_table_.remove_button.hide()

        cursor = connection.cursor()
        cursor.execute('select product_id, product_name, product_size, product_category, '
                       'product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,'
                       'product_pack_sp, product_quantity, product_quantifier, product_notes from products order by product_name;')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.product_table_.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.product_table_.table.rowCount()
        self.total_label = QtWidgets.QLabel('Total: ' + str(total))

        self.product_table_.content_overall_layout.addWidget(self.total_label)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        self.search_products_panel = QtWidgets.QLineEdit()
        self.search_products_panel.setPlaceholderText('Search all products')
        self.search_products_panel.textChanged.connect(self.product_text_change_action)
        self.search_products_panel.setFixedWidth(200)

        product_type_label = QtWidgets.QLabel('Select product category. ')
        self.product_type = QtWidgets.QComboBox()
        self.product_type.addItem('All')
        self.product_type.addItem('Food stuff & snacks')
        self.product_type.addItem('Beverages')
        self.product_type.addItem('Medicine')
        self.product_type.addItem('Cleaning accessories')
        self.product_type.addItem('Stationeries')
        self.product_type.currentTextChanged.connect(self.product_type_change_action)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignLeft)
        search_layout.addWidget(search_products_btn)
        search_layout.addWidget(self.search_products_panel)
        search_layout.addWidget(product_type_label, alignment=QtCore.Qt.AlignRight)
        search_layout.addWidget(self.product_type)

        layout.addLayout(search_layout)
        layout.addWidget(self.product_table_)

        self.view_products.setLayout(layout)

    def product_text_change_action(self):
        self.product_table_.table.clear()
        self.product_table_.table.setRowCount(0)
        self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                             'Product quantity', 'Product quantifier', 'Notes'))
        product_name = self.search_products_panel.text() + "%"

        cursor = connection.cursor()
        cursor.execute("select product_id, product_name, product_size, product_category,"
                       "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                       "product_pack_sp, product_quantity, product_quantifier, product_notes from products where product_name ilike '%s' order by product_name" % product_name)

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.product_table_.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.product_table_.table.rowCount()
        self.total_label.setText('Total: ' + str(total))

    def product_type_change_action(self):
        product_type_selected = self.product_type.currentText()
        if product_type_selected == 'All':
            self.product_table_.table.clear()
            self.product_table_.table.setRowCount(0)
            self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                                 'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                                 'Product quantity', 'Product quantifier', 'Notes'))
            cursor = connection.cursor()
            cursor.execute("select product_id, product_name, product_size, product_category,"
                           "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                           "product_pack_sp, product_quantity, product_quantifier, product_notes from products order by product_name;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.product_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.product_table_.table.rowCount()
            self.total_label.setText('Total: ' + str(total))
        elif product_type_selected == 'Food stuff & snacks':
            self.product_table_.table.clear()
            self.product_table_.table.setRowCount(0)
            self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                                 'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                                 'Product quantity', 'Product quantifier', 'Notes'))
            cursor = connection.cursor()
            cursor.execute("select product_id, product_name, product_size, product_category,"
                           "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                           "product_pack_sp, product_quantity, product_quantifier, product_notes from products where product_category = 'Food stuff & snacks' "
                           "order by product_name;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.product_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.product_table_.table.rowCount()
            self.total_label.setText('Total: ' + str(total))

            print('Food stuff & snacks')
        elif product_type_selected == 'Beverages':
            self.product_table_.table.clear()
            self.product_table_.table.setRowCount(0)
            self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                                 'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                                 'Product quantity', 'Product quantifier', 'Notes'))
            cursor = connection.cursor()
            cursor.execute("select product_id, product_name, product_size, product_category,"
                           "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                           "product_pack_sp, product_quantity, product_quantifier, product_notes from products where product_category = 'Beverages' "
                           "order by product_name;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.product_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.product_table_.table.rowCount()
            self.total_label.setText('Total: ' + str(total))

            print('beverages')
        elif product_type_selected == 'Medicine':
            self.product_table_.table.clear()
            self.product_table_.table.setRowCount(0)
            self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                                 'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                                 'Product quantity', 'Product quantifier', 'Notes'))
            cursor = connection.cursor()
            cursor.execute("select product_id, product_name, product_size, product_category,"
                           "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                           "product_pack_sp, product_quantity, product_quantifier, product_notes from products where product_category = 'Medicine' order by product_name;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.product_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.product_table_.table.rowCount()
            self.total_label.setText('Total: ' + str(total))

            print('Medicine')
        elif product_type_selected == 'Cleaning accessories':
            self.product_table_.table.clear()
            self.product_table_.table.setRowCount(0)
            self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                                 'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                                 'Product quantity', 'Product quantifier', 'Notes'))
            cursor = connection.cursor()
            cursor.execute("select product_id, product_name, product_size, product_category,"
                           "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                           "product_pack_sp, product_quantity, product_quantifier, product_notes from products where product_category = 'Cleaning accessories' "
                           "order by product_name;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.product_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.product_table_.table.rowCount()
            self.total_label.setText('Total: ' + str(total))

            print('cleaning accessories')
        elif product_type_selected == 'Stationeries':
            self.product_table_.table.clear()
            self.product_table_.table.setRowCount(0)
            self.product_table_.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                                 'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                                                 'Product quantity', 'Product quantifier', 'Notes'))
            cursor = connection.cursor()
            cursor.execute("select product_id, product_name, product_size, product_category,"
                           "product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,"
                           "product_pack_sp, product_quantity, product_quantifier, product_notes from products where product_category = 'Stationeries' "
                           "order by product_name;")
            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.product_table_.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.product_table_.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            total = self.product_table_.table.rowCount()
            self.total_label.setText('Total: ' + str(total))

            print('stationeries')

    def add_products_ui(self):

        # Product Add

        add_interface = ProductAdd()
        add_interface.cancel_btn.hide()

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(add_interface)
        self.add_products.setLayout(layout)

    def reduce_products_ui(self):

        layout = QtWidgets.QFormLayout()
        self.reduce_btn = QtWidgets.QPushButton('Reduce', self)
        cancel_btn = QtWidgets.QPushButton('Cancel', self)

        name = QtWidgets.QLineEdit()
        layout.addRow('Name', name)

        quantity = QtWidgets.QLineEdit()
        layout.addRow('Quantity', quantity)

        layout.addWidget(self.reduce_btn)
        layout.addWidget(cancel_btn)

        cancel_btn.clicked.connect(name.clear)
        cancel_btn.clicked.connect(quantity.clear)

        self.reduce_products.setLayout(layout)

    # once sales button is clicked (from menu)

    def sales_ui(self):

        sales_ui = SalesUi()

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(sales_ui)
        # layout.addLayout(table_btn_layout)
        # layout.addLayout(summary_sale_layout)

        self.sales.setLayout(layout)

    def add_product(self):
        pass

    # once invoices button is clicked (from menu)

    def invoicesUI(self):
        pass

    # once orders button is clicked (from menu)

    def ordersUI(self):
        layout = QtWidgets.QHBoxLayout()
        tab = QtWidgets.QTabWidget()

        self.view_orders = QtWidgets.QWidget()
        self.add_orders = QtWidgets.QWidget()
        self.remove_orders = QtWidgets.QWidget()

        tab.addTab(self.view_orders, 'View Orders')
        tab.addTab(self.add_orders, 'Add Orders')
        tab.addTab(self.remove_orders, 'Remove Orders')

        self.view_orders_ui()
        self.add_orders_ui()
        self.remove_orders_ui()

        layout.addWidget(tab)
        self.orders.setLayout(layout)

    def view_orders_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.table = Table()
        self.table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.content_groupbox.setTitle('Orders')
        self.table.table.setColumnCount(12)
        self.table.table.setHorizontalHeaderLabels(('Order id', 'Order title', 'Order urgency', 'product name',
                                                    'Product buying price', 'Product selling price',
                                                    'Product quantity', 'Product quantifier', 'Product size', 'Supplier name',
                                                    'Supplier phone number', 'Supplier email', 'Order notes'))
        self.table.add_button.hide()
        self.table.edit_button.hide()
        self.table.refresh_button.hide()
        self.table.remove_button.hide()

        cursor = connection.cursor()
        cursor.execute('''select order_id, order_title, order_urgency, product_name, 
                       product_buying_price, product_selling_price,
                       product_quantity, product_quantifier, product_size, supplier_name, 
                       supplier_phone_number, supplier_email, order_notes 
                       from orders order by order_title;''')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.table.table.rowCount()
        self.order_total_label = QtWidgets.QLabel('Total: ' + str(total))
        refresh = QtWidgets.QPushButton('Refresh')
        refresh.clicked.connect(self.refresh_order)

        self.table.content_overall_layout.addWidget(self.order_total_label)
        self.table.content_groupbox_layout.addWidget(refresh, alignment=QtCore.Qt.AlignTop)
        # table.content_overall_layout.addWidget(refresh, alignment=QtCore.Qt.AlignRight)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        search_products_panel = QtWidgets.QLineEdit()
        search_products_panel.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignLeft)
        search_layout.addWidget(search_products_btn)
        search_layout.addWidget(search_products_panel)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        self.view_orders.setLayout(layout)

    def refresh_order(self):
        self.table.table.clear()
        self.table.table.setRowCount(0)
        self.table.table.setColumnCount(12)
        self.table.table.setHorizontalHeaderLabels(('Order id', 'Order title', 'Order urgency', 'product name',
                                                    'Product buying price', 'Product selling price',
                                                    'Product quantity', 'Product quantifier', 'Product size', 'Supplier name',
                                                    'Supplier phone number', 'Supplier email', 'Order notes'))

        cursor = connection.cursor()
        cursor.execute('''select order_id, order_title, order_urgency, product_name, 
                       product_buying_price, product_selling_price,
                       product_quantity, product_quantifier, product_size, supplier_name, 
                       supplier_phone_number, supplier_email, order_notes 
                       from orders_demo order by order_title;''')

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.table.table.rowCount()
        self.order_total_label.setText('Total: ' + str(total))

    def add_orders_ui(self):

        # make order interface

        make_order = MakeOrder()
        make_order.cancel_btn.hide()

        # main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(make_order)
        self.add_orders.setLayout(layout)

    def remove_orders_ui(self):
        pass

    # once bills button is clicked (from menu)

    def billsUI(self):
        pass

    # once reports button is clicked (from menu)

    def reportsUI(self):

        # tab creation

        tab = QtWidgets.QTabWidget()

        self.reporting = QtWidgets.QWidget()
        self.pdf_reporting = QtWidgets.QWidget()

        tab.addTab(self.reporting, 'Report Generation')
        tab.addTab(self.pdf_reporting, 'Report Writing')

        self.reporting_ui()
        self.pdf_reporting_ui()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tab)

        self.reports.setLayout(layout)

    def reporting_ui(self):

        # products csv

        product_groupbox = QtWidgets.QGroupBox('Products.')
        product_groupbox_layout = QtWidgets.QHBoxLayout()
        product_groupbox.setLayout(product_groupbox_layout)
        product_label = QtWidgets.QLabel('Generate a CSV file for your products\n'
                                         'CSV - (Comma Separated Values)')

        product_button = QtWidgets.QPushButton('Generate CSV file')
        product_button.clicked.connect(self.product_report)

        product_groupbox_layout.addWidget(product_label)
        product_groupbox_layout.addWidget(product_button)

        # contacts csv

        contact_groupbox = QtWidgets.QGroupBox('Contacts.')
        contact_groupbox_layout = QtWidgets.QHBoxLayout()
        contact_groupbox.setLayout(contact_groupbox_layout)
        contact_label = QtWidgets.QLabel('Generate a CSV file for your contacts\n'
                                         'CSV - (Comma Separated Values)')

        contact_button = QtWidgets.QPushButton('Generate CSV file')
        contact_button.clicked.connect(self.contact_report)

        contact_groupbox_layout.addWidget(contact_label)
        contact_groupbox_layout.addWidget(contact_button)

        # orders csv

        order_groupbox = QtWidgets.QGroupBox('Orders.')
        order_groupbox_layout = QtWidgets.QHBoxLayout()
        order_groupbox.setLayout(order_groupbox_layout)
        order_label = QtWidgets.QLabel('Generate a CSV file for your orders\n'
                                       'CSV - (Comma Separated Values)')

        order_button = QtWidgets.QPushButton('Generate CSV file')
        order_button.clicked.connect(self.order_report)
        order_groupbox_layout.addWidget(order_label)
        order_groupbox_layout.addWidget(order_button)

        # report opening, editing and saving

        report_frame_layout = QtWidgets.QHBoxLayout()
        report_frame = QtWidgets.QFrame()
        report_frame.setLayout(report_frame_layout)

        self.report_workspace = ReportTable()

        open_btn = QtWidgets.QPushButton('Open csv')
        open_btn.clicked.connect(self.report_workspace.open_sheet)
        save_btn = QtWidgets.QPushButton('Save csv')
        save_btn.clicked.connect(self.report_workspace.save_sheet)
        clear_btn = QtWidgets.QPushButton('Clear')

        clear_btn.clicked.connect(self.report_clear)

        btn_layout = QtWidgets.QVBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignTop)
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(clear_btn)

        report_frame_layout.addWidget(self.report_workspace)
        report_frame_layout.addLayout(btn_layout)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(product_groupbox)
        layout.addWidget(contact_groupbox)
        layout.addWidget(order_groupbox)
        layout.addWidget(report_frame)
        self.reporting.setLayout(layout)

    def report_clear(self):
        self.report_workspace.clear()
        self.report_workspace.setColumnCount(10)
        self.report_workspace.setRowCount(6)
        col_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        self.report_workspace.setHorizontalHeaderLabels(col_headers)
        self.report_workspace.setAlternatingRowColors(True)

    def pdf_reporting_ui(self):

        # tool bar
        tool_bar = QtWidgets.QToolBar()
        tool_bar.setMovable(True)

        brows_action = QtWidgets.QAction(QtGui.QIcon('../images/folder.ico'), 'Brows for file', self)
        brows_action.setStatusTip('Brows for file')
        brows_action.triggered.connect(self.brows_action)

        font_color_action = QtWidgets.QAction(QtGui.QIcon('../images/draw.ico'), 'Font Color', self)
        font_color_action.setStatusTip('Change font color')
        font_color_action.triggered.connect(self.color_dialog)

        text_font_action = QtWidgets.QAction(QtGui.QIcon('../images/edit.ico'), 'Font', self)
        text_font_action.setStatusTip('Change text font')
        text_font_action.triggered.connect(self.font_dialog)

        preview_pdf_action = QtWidgets.QAction(QtGui.QIcon('../images/general_document(2).ico'), 'Preview PDF', self)
        preview_pdf_action.setStatusTip('Preview PDF')
        preview_pdf_action.triggered.connect(self.preview_pdf_action)

        generate_pdf = QtWidgets.QAction(QtGui.QIcon('../images/general_document(1).ico'), 'Generate PDF', self)
        generate_pdf.setStatusTip('Generate PDF')
        generate_pdf.triggered.connect(self.pdf_action)

        print_action = QtWidgets.QAction(QtGui.QIcon('../images/print.ico'), 'Print', self)
        print_action.setStatusTip('Print')
        print_action.triggered.connect(self.print_action)

        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")
        system_date = QtWidgets.QLabel()
        system_date.setText(str(date))
        # date = now.strftime("%B %d, %Y %H:%M:%S")

        tool_bar.addAction(brows_action)
        tool_bar.addAction(font_color_action)
        tool_bar.addAction(text_font_action)
        tool_bar.addAction(preview_pdf_action)
        tool_bar.addAction(generate_pdf)
        tool_bar.addAction(print_action)
        # tool_bar.addWidget(system_date)

        # text area

        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setToolTip('Type your report here and generate PDF when done')
        self.text_area.setAlignment(QtCore.Qt.AlignTop)
        clear_btn = QtWidgets.QPushButton('Clear text area')
        clear_btn.clicked.connect(self.clear_action)
        text_area_layout = QtWidgets.QVBoxLayout()
        text_area_layout.addWidget(self.text_area)
        text_area_layout.addWidget(clear_btn)
        text_area_groupbox = QtWidgets.QGroupBox('Text Area')
        text_area_groupbox.setLayout(text_area_layout)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(tool_bar)
        # layout.addLayout(buttons_layout)
        layout.addWidget(text_area_groupbox)
        self.pdf_reporting.setLayout(layout)

    def clear_action(self):
        self.text_area.clear()

    def brows_action(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), "", "All(*)")
        if path[0] != "":
            with open(path[0], newline="") as file:
                text = file.read()
                self.text_area.setText(text)

    def color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        self.text_area.setTextColor(color)

    def font_dialog(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.text_area.setFont(font)

    def pdf_action(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Generate PDF', None, 'PDF files (.pdf);;All Files()')

        if fn != '':

            if QtCore.QFileInfo(fn).suffix() == '':
                fn += '.pdf'

            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.text_area.document().print_(printer)

    def preview_pdf_action(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        preview_dialog = QtPrintSupport.QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.paint_preview)
        preview_dialog.exec_()

    def paint_preview(self, printer):
        self.text_area.print_(printer)

    def print_action(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        dialog = QtPrintSupport.QPrintDialog(printer, self)
        if dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
            self.text_area.print_(printer)

    def product_report(self):
        cursor = connection.cursor()

        sql = "COPY (select * from products) TO STDOUT WITH CSV DELIMITER ',' HEADER"
        with open('c:/users/josh/desktop/products_file2.csv', 'w') as file:
            cursor.copy_expert(sql, file)

    def contact_report(self):
        cursor = connection.cursor()

        sql = "COPY (select * from contacts) TO STDOUT WITH CSV DELIMITER ',' HEADER"
        with open('c:/users/josh/desktop/contacts_file2.csv', 'w') as file:
            cursor.copy_expert(sql, file)

    def order_report(self):
        cursor = connection.cursor()

        sql = "COPY (select * from orders) TO STDOUT WITH CSV DELIMITER ',' HEADER"
        with open('c:/users/josh/desktop/orders_file.csv', 'w') as file:
            cursor.copy_expert(sql, file)


class SalesUi(QtWidgets.QWidget):
    def __init__(self):
        super(SalesUi, self).__init__()

        # table

        self.table = Table()
        self.table.content_groupbox.setTitle('Selected Items')
        self.table.table.setRowCount(0)
        self.table.table.setColumnCount(0)
        self.table.table.setColumnCount(7)
        self.table.remove_button.hide()
        self.table.refresh_button.hide()
        self.table.edit_button.hide()
        self.table.add_button.hide()

        column_labels = ['Id', 'Name', 'Size', 'Category', 'Selling price', 'Quantity', 'Quantifier']
        self.table.table.setHorizontalHeaderLabels(column_labels)

        cursor = connection.cursor()
        cursor.execute('''select product_id, product_name, product_size, product_category, product_selling_price, product_quantity, 
                                product_quantifier from sales''')

        result = cursor.fetchall()
        cursor.close()

        for row_number, row_data in enumerate(result):
            self.table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        # brows button and action

        brows_button = QtWidgets.QPushButton('Brows')
        brows_button.clicked.connect(self.sales_brows_button)

        edit_button = QtWidgets.QPushButton('Edit')
        remove_button = QtWidgets.QPushButton('Remove')
        remove_button.clicked.connect(self.sales_remove_button)

        # refresh button and action

        refresh_button = QtWidgets.QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_btn)

        # button_layout

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(brows_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(refresh_button)

        # table button layout

        table_btn_layout = QtWidgets.QHBoxLayout()
        table_btn_layout.addWidget(self.table)
        table_btn_layout.addLayout(button_layout)

        # Summary group box

        cursor = connection.cursor()
        cursor.execute("select name from admin_log order by id desc limit(1);")
        my_admin = cursor.fetchone()[0]
        cursor.close()
        # print(my_admin)

        cursor = connection.cursor()
        cursor.execute("select sum(product_selling_price) from sales")
        my_total = cursor.fetchone()[0]
        cursor.close()

        total_products = QtWidgets.QLabel('Total number of products: ')
        self.total_items = QtWidgets.QLabel('Total number of items: ' + str(self.table.table.rowCount()))
        self.total_sp = QtWidgets.QLabel('Total selling price: ' + str(my_total))
        sold_by = QtWidgets.QLabel('Sold by: ' + my_admin)

        summary_groupbox = QtWidgets.QGroupBox('Summary')
        summary_groupbox.setFixedWidth(350)
        self.summary_groupbox_layout = QtWidgets.QVBoxLayout()
        summary_groupbox.setLayout(self.summary_groupbox_layout)

        self.summary_groupbox_layout.addWidget(total_products)
        self.summary_groupbox_layout.addWidget(self.total_items)
        self.summary_groupbox_layout.addWidget(self.total_sp)
        self.summary_groupbox_layout.addWidget(sold_by)

        # sell_group box

        cash_label = QtWidgets.QLabel('Cash')
        sp_label = QtWidgets.QLabel('Selling price')
        change_label = QtWidgets.QLabel('Change')

        self.cash_input = QtWidgets.QLineEdit()
        self.cash_input.textChanged.connect(self.cash_input_)
        self.sp_input = QtWidgets.QLineEdit()
        self.sp_input.setText(str(my_total))
        self.sp_input.setEnabled(False)
        self.change_display = QtWidgets.QLCDNumber()
        self.change_display.setStyleSheet('background-color:transparent')

        complete_button = QtWidgets.QPushButton('Complete Sale')
        complete_button.clicked.connect(self.complete_sales_action)

        sale_groupbox = QtWidgets.QGroupBox('Sell')
        sale_groupbox_layout = QtWidgets.QFormLayout()
        sale_groupbox.setLayout(sale_groupbox_layout)

        sale_groupbox_layout.addRow(cash_label, self.cash_input)
        sale_groupbox_layout.addRow(sp_label, self.sp_input)
        sale_groupbox_layout.addRow(change_label, self.change_display)
        sale_groupbox_layout.addRow("", complete_button)

        # summary and sale layout

        summary_sale_layout = QtWidgets.QHBoxLayout()
        summary_sale_layout.addWidget(summary_groupbox)
        summary_sale_layout.addWidget(sale_groupbox)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(table_btn_layout)
        layout.addLayout(summary_sale_layout)

        self.setLayout(layout)

    def cash_input_(self):
        cursor = connection.cursor()
        cursor.execute("select sum(product_selling_price) from sales")
        my_total = cursor.fetchone()[0]
        cursor.close()

        cash_input = int(self.cash_input.text())
        total_price = my_total
        if cash_input > total_price:
            change = cash_input - total_price
            self.change_display.display(change)
        elif total_price > cash_input:
            less_change = 0
            self.change_display.display(less_change)
        elif cash_input < 1:
            null_change = 0
            self.change_display.display(null_change)

    def sales_remove_button(self):
        remove_dialog = RemoveDialog()
        remove_dialog.exec()

    def sales_brows_button(self):
        sales_dialog = SalesDialog()
        sales_dialog.exec()

    def refresh_btn(self):
        self.table.table.clear()
        self.table.table.setRowCount(0)
        self.table.table.setColumnCount(7)

        cursor = connection.cursor()
        cursor.execute('''select product_id, product_name, product_size, product_category, product_selling_price, product_quantity, 
                                product_quantifier from sales''')
        result = cursor.fetchall()

        column_labels = ['Id', 'Name', 'Size', 'Category', 'Selling price', 'Quantity', 'Quantifier']
        self.table.table.setHorizontalHeaderLabels(column_labels)

        for row_number, row_data in enumerate(result):
            self.table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        print('refreshed')

        # total price of products

        cursor = connection.cursor()
        cursor.execute("select sum(product_selling_price) from sales")
        my_total = cursor.fetchone()[0]
        cursor.close()

        self.total_sp.setText('Total selling price: ' + str(my_total))
        self.sp_input.setText(str(my_total))

        # total number of products

        total_items = 'Total number of items: ' + str(self.table.table.rowCount())
        self.total_items.setText(total_items)

    def complete_sales_action(self):

        reply = QtWidgets.QMessageBox.question(self, 'Are you sure?', 'Are you sure you want to complete this sale?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.confirmed_complete()
            self.refresh_btn()
        else:
            pass

    def confirmed_complete(self):
        cursor = connection.cursor()

        try:
            cursor.execute('''
                    INSERT INTO sales_log (product_id, product_name, product_size, product_category, product_buying_price, product_selling_price, 
                                product_pack_bp, product_pack_sp, product_quantity, product_quantifier)
                    SELECT product_id, product_name, product_size, product_category, product_buying_price, product_selling_price, 
                                product_pack_bp, product_pack_sp, product_quantity, product_quantifier
                    FROM sales where true;
                    ''')
            print('added!')

            cursor.execute('DROP TABLE sales;')
            cursor.execute('CREATE TABLE sales AS TABLE sales_log WITH NO DATA;')
            connection.commit()

        except Exception:
            print('nothing was added to sales_log, check your list...')


class RemoveDialog(QtWidgets.QDialog):
    def __init__(self):
        super(RemoveDialog, self).__init__()

        self.setWindowTitle('Remove product')
        self.setWindowIcon(QtGui.QIcon('../images/success (13).png'))
        self.setFixedWidth(700)
        self.setFixedHeight(350)

        remove_widget = RemoveWidget()

        cancel_button = QtWidgets.QPushButton('Close')
        cancel_button.clicked.connect(self.close)

        remove_widget.remove_layout.addRow("", cancel_button)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(remove_widget)
        self.setLayout(layout)


class SalesDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SalesDialog, self).__init__()

        self.setWindowTitle('Select product')
        self.setWindowIcon(QtGui.QIcon('../images/success (12).png'))
        self.setFixedWidth(700)
        self.setFixedHeight(350)

        sales_widget = SalesWidget()

        cancel_button = QtWidgets.QPushButton('Close')
        cancel_button.clicked.connect(self.close)

        sales_widget.brows_layout.addRow("", cancel_button)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(sales_widget)
        self.setLayout(layout)


class RemoveWidget(QtWidgets.QWidget):
    def __init__(self):
        super(RemoveWidget, self).__init__()

        self.remove_table = QtWidgets.QTableWidget()
        self.remove_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.remove_table.setColumnCount(5)
        self.remove_table.setRowCount(0)
        self.remove_table.setAlternatingRowColors(True)
        col_headers = ['id', 'name', 'selling price', 'size', 'category', 'F']
        self.remove_table.setHorizontalHeaderLabels(col_headers)

        cursor = connection.cursor()
        cursor.execute('''SELECT product_id, product_name, product_selling_price,
         product_size, product_category FROM sales ORDER BY product_name
        ''')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.remove_table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.remove_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        row_count = self.remove_table.rowCount()
        self.brows_label = QtWidgets.QLabel('Total: ' + str(row_count))

        table_frame = QtWidgets.QFrame()
        table_frame_layout = QtWidgets.QVBoxLayout()
        table_frame_layout.addWidget(self.remove_table)
        table_frame_layout.addWidget(self.brows_label)
        table_frame.setLayout(table_frame_layout)

        # brows_items

        search_label = QtWidgets.QLabel('Search by:')

        self.search_creteria = QtWidgets.QComboBox()
        self.search_creteria.addItem('All')
        self.search_creteria.addItem('Name')
        self.search_creteria.addItem('Size')
        self.search_creteria.addItem('Category')

        self.product_name_label = QtWidgets.QLabel('Name')
        self.product_name_text = QtWidgets.QLineEdit()
        self.product_name_text.textChanged.connect(self.product_change_action)
        self.search_creteria.currentTextChanged.connect(self.combo_changed)

        self.remove_product_button = QtWidgets.QPushButton('Remove product')
        self.remove_product_button.clicked.connect(self.remove_product)

        product_id_label = QtWidgets.QLabel('ID')
        self.product_id_text = QtWidgets.QLineEdit()
        # self.product_id_text.textChanged.connect(self.id_change_action)

        # brows_layout

        self.remove_layout = QtWidgets.QFormLayout()
        self.remove_layout.addRow(search_label, self.search_creteria)
        self.remove_layout.addRow(self.product_name_label, self.product_name_text)
        self.remove_layout.addRow(product_id_label, self.product_id_text)
        self.remove_layout.addRow("", self.remove_product_button)
        # self.brows_layout.addRow("", cancel_button)

        # frame

        brows_frame = QtWidgets.QFrame()
        brows_frame.setFixedWidth(200)
        brows_frame.setLayout(self.remove_layout)

        # main layout

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(table_frame)
        layout.addWidget(brows_frame)
        self.setLayout(layout)

    def combo_changed(self):
        combo = self.search_creteria.currentText()
        if combo == 'All':
            pass
        else:
            self.product_name_label.setText(combo)

    def product_change_action(self):
        self.refresh_table()

        product_name = self.product_name_text.text() + "%"
        search_creteria = self.search_creteria.currentText()

        try:
            cursor = connection.cursor()
            # cursor.execute("select product_id, product_name, product_selling_price, product_size, "
            #                "product_category from products where product_name ilike '%s' " % product_name)

            if search_creteria == 'All':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, product_category from sales order by product_name;")

            elif search_creteria == 'Name':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, "
                               "product_category from sales where product_name ilike '%s' order by product_name" % product_name)

            # elif search_creteria == 'Selling Price':
            #     cursor.execute("select product_id, product_name, product_selling_price, product_size, "
            #                    "product_category from products where product_selling_price ilike '%s' " % product_name)

            elif search_creteria == 'Size':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, "
                               "product_category from sales where product_size ilike '%s' order by product_name" % product_name)

            elif search_creteria == 'Category':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, "
                               "product_category from sales where product_category ilike '%s' order by product_name" % product_name)

            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.remove_table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.remove_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            row_count = self.remove_table.rowCount()
            self.brows_label.setText('Total: ' + str(row_count))

        except Exception:
            print('Could not find product')

    def remove_product(self):
        recovered_id = self.product_id_text.text()

        try:
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM sales where product_id = '%s'; ''' % recovered_id)

            connection.commit()
            self.product_id_text.clear()

            # self.result = cursor.fetchall()
            print(recovered_id)

        except Exception:
            print('Tough luck!!')

    def refresh_table(self):
        self.remove_table.clear()
        self.remove_table.setColumnCount(5)
        self.remove_table.setRowCount(0)
        self.remove_table.setAlternatingRowColors(True)
        col_headers = ['id', 'name', 'selling price', 'size', 'category', 'F']
        self.remove_table.setHorizontalHeaderLabels(col_headers)
        total = self.remove_table.rowCount()
        self.brows_label.setText(str(total))


class SalesWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SalesWidget, self).__init__()

        # brows_table

        self.table = QtWidgets.QTableWidget()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(6)
        self.table.setRowCount(0)
        self.table.setAlternatingRowColors(True)
        col_headers = ['id', 'name', 'selling price', 'size', 'category', 'Quantity']
        self.table.setHorizontalHeaderLabels(col_headers)

        cursor = connection.cursor()
        cursor.execute('''SELECT product_id, product_name, product_selling_price,
         product_size, product_category, product_quantity FROM products ORDER BY product_name
        ''')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        row_count = self.table.rowCount()
        self.brows_label = QtWidgets.QLabel('Total: ' + str(row_count))

        table_frame = QtWidgets.QFrame()
        table_frame_layout = QtWidgets.QVBoxLayout()
        table_frame_layout.addWidget(self.table)
        table_frame_layout.addWidget(self.brows_label)
        table_frame.setLayout(table_frame_layout)

        # brows_items

        search_label = QtWidgets.QLabel('Search by:')

        self.search_creteria = QtWidgets.QComboBox()
        self.search_creteria.addItem('All')
        self.search_creteria.addItem('Name')
        # self.search_creteria.addItem('Selling Price')
        self.search_creteria.addItem('Size')
        self.search_creteria.addItem('Category')

        self.product_name_label = QtWidgets.QLabel('Name')
        self.product_name_text = QtWidgets.QLineEdit()
        # self.product_name_text.returnPressed.connect(self.product_enter_action)
        self.product_name_text.textChanged.connect(self.product_change_action)
        self.search_creteria.currentTextChanged.connect(self.combo_changed)

        product_quantity_label = QtWidgets.QLabel('Quantity')
        self.product_quantity_spinbox = QtWidgets.QSpinBox()
        self.add_product_button = QtWidgets.QPushButton('Add product')
        self.add_product_button.clicked.connect(self.add_product)

        product_id_label = QtWidgets.QLabel('ID')
        self.product_id_text = QtWidgets.QLineEdit()
        # self.product_id_text.textChanged.connect(self.id_change_action)

        # brows_layout

        self.brows_layout = QtWidgets.QFormLayout()
        self.brows_layout.addRow(search_label, self.search_creteria)
        self.brows_layout.addRow(self.product_name_label, self.product_name_text)
        self.brows_layout.addRow(product_id_label, self.product_id_text)
        self.brows_layout.addRow(product_quantity_label, self.product_quantity_spinbox)
        self.brows_layout.addRow("", self.add_product_button)
        # self.brows_layout.addRow("", cancel_button)

        # frame

        brows_frame = QtWidgets.QFrame()
        brows_frame.setFixedWidth(200)
        brows_frame.setLayout(self.brows_layout)

        # main layout

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(table_frame)
        layout.addWidget(brows_frame)
        self.setLayout(layout)

    # def add_product(self):
    #     add_product = AddProduct()
    #     add_product.exec_()

    def combo_changed(self):
        combo = self.search_creteria.currentText()
        if combo == 'All':
            pass
        else:
            self.product_name_label.setText(combo)

    def product_change_action(self):
        self.refresh_table()

        product_name = self.product_name_text.text() + "%"
        search_creteria = self.search_creteria.currentText()

        try:
            cursor = connection.cursor()
            # cursor.execute("select product_id, product_name, product_selling_price, product_size, "
            #                "product_category from products where product_name ilike '%s' " % product_name)

            if search_creteria == 'All':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, product_category from products order by product_name;")

            elif search_creteria == 'Name':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, "
                               "product_category from products where product_name ilike '%s' order by product_name" % product_name)

            # elif search_creteria == 'Selling Price':
            #     cursor.execute("select product_id, product_name, product_selling_price, product_size, "
            #                    "product_category from products where product_selling_price ilike '%s' " % product_name)

            elif search_creteria == 'Size':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, "
                               "product_category from products where product_size ilike '%s' order by product_name" % product_name)

            elif search_creteria == 'Category':
                cursor.execute("select product_id, product_name, product_selling_price, product_size, "
                               "product_category from products where product_category ilike '%s' order by product_name" % product_name)

            results = cursor.fetchall()

            for row_number, row_data in enumerate(results):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            row_count = self.table.rowCount()
            self.brows_label.setText('Total: ' + str(row_count))

        except Exception:
            print('Could not find product')

    def add_product(self):
        sales_ui_table = SalesUi()
        recovered_id = self.product_id_text.text()
        recovered_quantity = self.product_quantity_spinbox.value()

        try:
            cursor = connection.cursor()
            # cursor.execute("select * from products where product_id = '%s' " % recovered_id)
            cursor.execute('''INSERT INTO sales (product_id, product_name, product_size, product_category, product_buying_price, product_selling_price, 
                                product_pack_bp, product_pack_sp, product_quantity, product_quantifier)
                                SELECT product_id, product_name, product_size, product_category, product_buying_price, product_selling_price, 
                                product_pack_bp, product_pack_sp, product_quantity, product_quantifier 
                                FROM products where product_id = '%s'; ''' % recovered_id)
            cursor.execute("UPDATE sales SET product_quantity = %s WHERE product_id = '%s';" % (recovered_quantity, recovered_id))
            cursor.execute("select product_selling_price from sales where product_id = '%s';" % recovered_id)
            selling_price = cursor.fetchone()
            for i in selling_price:
                final_selling_price = i * recovered_quantity
                cursor.execute("UPDATE sales SET product_selling_price = '%s' WHERE product_id = '%s';" % (final_selling_price, recovered_id))

            connection.commit()
            self.product_id_text.clear()

            # self.result = cursor.fetchall()
            print(recovered_id)

        except Exception:
            print('Tough luck!!')

    def refresh_table(self):
        self.table.clear()
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.setAlternatingRowColors(True)
        col_headers = ['id', 'name', 'selling price', 'size', 'category', 'F']
        self.table.setHorizontalHeaderLabels(col_headers)
        total = self.table.rowCount()
        self.brows_label.setText(str(total))


class AddProduct(QtWidgets.QDialog):
    def __init__(self):
        super(AddProduct, self).__init__()

        self.setWindowTitle('Sale')
        self.setWindowIcon(QtGui.QIcon('../images/success (1)'))

        sales_widget = SalesWidget()
        recover_id = sales_widget.product_id_text.text()
        print(recover_id)

        # cursor = connection.cursor()
        # cursor.execute("SELECT * FROM products where product_id '%s' " % id)
        # result = cursor.fetchall()
        #
        # sales_table = Application()
        #
        # for row_number, row_data in enumerate(result):
        #     sales_table.sales_table.insertRow(row_number)
        #     for column_number, column_data in enumerate(row_data):
        #         sales_table.sales_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        message = QtWidgets.QLabel('Successfully added \nadd more? Yes | No')

        # buttons

        yes_btn = QtWidgets.QPushButton('Yes')
        no_btn = QtWidgets.QPushButton('No')

        # buttons layout

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(message)
        layout.addLayout(btn_layout)

        self.setLayout(layout)


class MenuAction(QtWidgets.QWidget):
    def __init__(self):
        super(MenuAction, self).__init__()

        self.dashboard = QtWidgets.QCommandLinkButton('Dashboard')
        self.dashboard.setIcon(QtGui.QIcon('../images/office/dashboard'))
        self.dashboard.setIconSize(QtCore.QSize(40, 40))
        self.dashboard.setFixedWidth(150)

        self.contacts = QtWidgets.QCommandLinkButton('Contacts')
        self.contacts.setIcon(QtGui.QIcon('../images/office/contacts'))
        self.contacts.setIconSize(QtCore.QSize(30, 30))
        self.contacts.setFixedWidth(150)

        self.products = QtWidgets.QCommandLinkButton('Products')
        self.products.setIcon(QtGui.QIcon('../images/office/products'))
        self.products.setIconSize(QtCore.QSize(40, 40))
        self.products.setFixedWidth(150)

        self.sales = QtWidgets.QCommandLinkButton('Sales')
        self.sales.setIcon(QtGui.QIcon('../images/office/sales'))
        self.sales.setIconSize(QtCore.QSize(40, 40))
        self.sales.setFixedWidth(150)

        self.invoices = QtWidgets.QCommandLinkButton('Invoices')
        self.invoices.setIcon(QtGui.QIcon('../images/office/invoice'))
        self.invoices.setIconSize(QtCore.QSize(40, 40))
        self.invoices.setFixedWidth(150)

        self.orders = QtWidgets.QCommandLinkButton('Orders')
        self.orders.setIcon(QtGui.QIcon('../images/office/order'))
        self.orders.setIconSize(QtCore.QSize(40, 40))
        self.orders.setFixedWidth(150)

        self.bills = QtWidgets.QCommandLinkButton('Bills')
        self.bills.setIcon(QtGui.QIcon('../images/office/bill'))
        self.bills.setIconSize(QtCore.QSize(40, 40))
        self.bills.setFixedWidth(150)

        self.reports = QtWidgets.QCommandLinkButton('Reports')
        self.reports.setIcon(QtGui.QIcon('../images/office/report'))
        self.reports.setIconSize(QtCore.QSize(40, 40))
        self.reports.setFixedWidth(150)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self.dashboard, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.contacts, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.products, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.sales, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.invoices, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.orders, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.bills, alignment=QtCore.Qt.AlignTop)
        main_layout.addWidget(self.reports, alignment=QtCore.Qt.AlignTop)

        self.setLayout(main_layout)


class Table(QtWidgets.QWidget):
    def __init__(self):
        super(Table, self).__init__()

        self.content_groupbox = QtWidgets.QGroupBox('Table')
        self.content_overall_layout = QtWidgets.QVBoxLayout()
        self.content_groupbox.setLayout(self.content_overall_layout)
        # self.content_groupbox.setFixedHeight(300)

        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(7)
        self.table.setGridStyle(4)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        # total = self.table.rowCount()
        # self.total_label = QtWidgets.QLabel('Total: ' + str(total))

        self.add_button = QtWidgets.QPushButton('Add')
        self.edit_button = QtWidgets.QPushButton('Edit')
        self.refresh_button = QtWidgets.QPushButton('Refresh')
        self.remove_button = QtWidgets.QPushButton('Remove')

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignTop)
        button_layout.addWidget(self.edit_button, alignment=QtCore.Qt.AlignTop)
        button_layout.addWidget(self.refresh_button, alignment=QtCore.Qt.AlignTop)
        button_layout.addWidget(self.remove_button, alignment=QtCore.Qt.AlignTop)

        self.content_groupbox_layout = QtWidgets.QHBoxLayout()
        self.content_groupbox_layout.setAlignment(QtCore.Qt.AlignTop)
        self.content_groupbox_layout.addWidget(self.table)
        self.content_groupbox_layout.addLayout(button_layout)

        self.content_overall_layout.addLayout(self.content_groupbox_layout)
        # content_overall_layout.addWidget(self.total_label)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addWidget(self.content_groupbox)
        content_layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(content_layout)


# This is the reports interactive table

class ReportTable(QtWidgets.QTableWidget):
    def __init__(self):
        super(ReportTable, self).__init__()
        self.check_change = True
        self.setColumnCount(10)
        self.setRowCount(6)
        col_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        self.setHorizontalHeaderLabels(col_headers)
        self.setAlternatingRowColors(True)
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)

    def c_current(self):
        if self.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            print('The current cell is ', row, ", ", col)
            print("In the cell, we have:", value)

    def open_sheet(self):

        self.check_change = False
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), "", "CSV(*.csv)")
        if path[0] != "":
            with open(path[0], newline="") as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(stuff)
                        self.setItem(row, column, item)

        self.check_change = True

    def save_sheet(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), "", 'CSV(*.csv)')
        if path[0] != "":
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)


# once add button is clicked under dashboard's product table


class ProductAdd(QtWidgets.QDialog):
    def __init__(self):
        super(ProductAdd, self).__init__()

        self.setWindowTitle('Add product')
        self.setWindowIcon(QtGui.QIcon('../images/success (8)'))

        # name

        self.name_field = QtWidgets.QLineEdit()
        self.name_field.setFixedWidth(200)
        self.name_field.setPlaceholderText('Product name')

        name_layout = QtWidgets.QHBoxLayout()
        name_layout.setAlignment(QtCore.Qt.AlignLeft)
        name_layout.addWidget(self.name_field)

        # category

        self.category = QtWidgets.QComboBox()
        self.category.setFixedWidth(200)
        self.category.setFrame(False)
        # self.category.addItem('Select category')
        self.category.addItem('Food stuff & snacks')
        self.category.addItem('Beverages')
        self.category.addItem('Medicine')
        self.category.addItem('Cleaning accessories')
        self.category.addItem('Stationeries')
        self.category.setMaxCount(10)
        # category.setEditable(True)
        self.category.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)

        # unit prices

        self.unit_buying_price = QtWidgets.QLineEdit()
        self.unit_buying_price.setPlaceholderText('Unit Buying price')

        self.unit_selling_price = QtWidgets.QLineEdit()
        self.unit_selling_price.setPlaceholderText('Unit Selling price')

        prices_layout = QtWidgets.QHBoxLayout()
        prices_layout.addWidget(self.unit_buying_price)
        prices_layout.addWidget(self.unit_selling_price)

        # quantity

        self.quantity = QtWidgets.QLineEdit()
        self.quantity.setPlaceholderText('Product quantity.')

        self.quantifier = QtWidgets.QComboBox()
        self.quantifier.addItem(' Piece(s)')
        self.quantifier.addItem(' Box(es)')
        self.quantifier.insertSeparator(3)
        self.quantifier.addItem(' Bundle(s)')
        self.quantifier.addItem(' Sack(s)')
        # quantifier.addItem('dozen')

        # quantity spin box

        self.quantity_spinbox = QtWidgets.QSpinBox()
        self.quantity_spinbox.setToolTip("Select quantity in box or bundle.")
        self.quantity_spinbox.setRange(0, 10)

        # finding out the number of items in a sealed product full of there products.

        # size
        self.size = QtWidgets.QLineEdit()
        self.size.setPlaceholderText('Product size')

        self.measuring_unit = QtWidgets.QComboBox()
        self.measuring_unit.addItem(' (g) Grams')
        self.measuring_unit.addItem(' (kg) Kilograms')
        self.measuring_unit.insertSeparator(3)
        self.measuring_unit.addItem(' (l) Litres')
        self.measuring_unit.addItem(' (ml) Milliliter')

        size_quantity_layout = QtWidgets.QHBoxLayout()
        size_quantity_layout.addWidget(self.quantity, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(self.quantifier, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(self.quantity_spinbox, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(self.size, alignment=QtCore.Qt.AlignRight)
        size_quantity_layout.addWidget(self.measuring_unit, alignment=QtCore.Qt.AlignRight)

        # pack prices

        self.total_buying_price = QtWidgets.QLineEdit()
        self.total_buying_price.setPlaceholderText('Total Buying price')

        # product quanity * product unit buying price

        self.total_selling_price = QtWidgets.QLineEdit()
        self.total_selling_price.setPlaceholderText('Total Selling price')
        # product quantity * product unit selling price

        pack_prices_layout = QtWidgets.QHBoxLayout()
        pack_prices_layout.addWidget(self.total_buying_price)
        pack_prices_layout.addWidget(self.total_selling_price)

        # notes

        self.notes = QtWidgets.QLineEdit()
        self.notes.setToolTip('This is not mandatory')
        self.notes.setPlaceholderText('Enter describing notes')
        self.notes.setFixedHeight(100)

        notes_groupbox = QtWidgets.QGroupBox('Description')
        notes_label = QtWidgets.QLabel('Enter short notes concerning product')
        notes_layout = QtWidgets.QVBoxLayout()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes)
        notes_groupbox.setLayout(notes_layout)

        # buttons

        submit_btn = QtWidgets.QPushButton('Submit')
        submit_btn.setStyleSheet('background-color:green')
        submit_btn.clicked.connect(self.product_submit_btn)

        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.product_reset_btn)

        self.cancel_btn = QtWidgets.QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(self.cancel_btn)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(name_layout)
        layout.addWidget(self.category)
        layout.addLayout(prices_layout)
        layout.addLayout(size_quantity_layout)
        layout.addLayout(pack_prices_layout)
        layout.addWidget(notes_groupbox)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def product_submit_btn(self):
        print(self.name_field.text())
        print(self.category.currentText())
        print(self.unit_buying_price.text())
        print(self.unit_selling_price.text())

        print(self.quantity.text(), self.quantifier.currentText())
        # print(self.quantifier.currentText())
        print(self.quantity_spinbox.value())
        print(self.size.text(), self.measuring_unit.currentText())
        # print(self.measuring_unit.currentText())

        print(self.total_buying_price.text())
        print(self.total_selling_price.text())
        print(self.notes.text())

        p_name = self.name_field.text()
        p_size = self.size.text()
        p_category = self.category.currentText()
        p_bp = self.unit_buying_price.text()
        p_sp = self.unit_selling_price.text()
        p_quantity = self.quantity.text()
        quantifier = self.quantifier.currentText()
        measure_units = self.measuring_unit.currentText()
        size = p_size + measure_units
        # quantity = p_quantity + quantifier
        p_total_bp = self.total_buying_price.text()
        p_total_sp = self.total_selling_price.text()
        p_notes = self.notes.text()

        try:
            cursor = connection.cursor()

            query = ''' INSERT INTO products
            (product_id, product_name, product_size, 
            product_category, product_buying_price, 
            product_selling_price, product_quantity, product_quantifier,
            product_pack_bp, product_pack_sp, product_notes)
            VALUES (uuid_generate_v4(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            data = (p_name, size, p_category, p_bp, p_sp, p_quantity, quantifier,
                    p_total_bp, p_total_sp, p_notes)

            cursor.execute(query, data)

            if data:
                print('Submission was successful')
                submit_action = SubmitAction()
                submit_action.exec_()

            connection.commit()

        except Exception:
            print('Submission  was futile')
            fatal_action = FatalAction()
            fatal_action.exec_()

    def product_reset_btn(self):
        self.name_field.clear()
        self.unit_buying_price.clear()
        self.unit_selling_price.clear()
        self.total_buying_price.clear()
        self.total_selling_price.clear()
        self.quantity.clear()
        self.size.clear()
        self.notes.clear()


# when submit btn is clicked across all tabs add action under the dashboard


class SubmitAction(QtWidgets.QDialog):
    def __init__(self):
        super(SubmitAction, self).__init__()

        self.setWindowTitle('Success')
        self.setWindowIcon(QtGui.QIcon('../images/db (2)'))

        # submission label

        submission_label = QtWidgets.QLabel('Successfully added')

        # date and time

        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")
        system_date = QtWidgets.QLabel()
        system_date.setText(str(date))

        # button

        submit_btn = QtWidgets.QPushButton('OK')
        submit_btn.clicked.connect(self.close)

        # main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(submission_label)
        main_layout.addWidget(system_date)
        main_layout.addWidget(submit_btn)

        self.setLayout(main_layout)


class FatalAction(QtWidgets.QDialog):
    def __init__(self):
        super(FatalAction, self).__init__()

        self.setWindowTitle('Futile')
        self.setWindowIcon(QtGui.QIcon('../images/db (6)'))
        self.setFixedWidth(170)

        # submission label

        submission_label = QtWidgets.QLabel('Submission was futile, \nCheck details')

        # date and time

        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")
        system_date = QtWidgets.QLabel()
        system_date.setText(str(date))

        # button

        submit_btn = QtWidgets.QPushButton('OK')
        submit_btn.clicked.connect(self.close)

        # main layout

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(submission_label)
        main_layout.addWidget(system_date)
        main_layout.addWidget(submit_btn)

        self.setLayout(main_layout)


# once add_conntacts button is clicked under dashboard's contact table


class ContactAdd(QtWidgets.QDialog):
    def __init__(self):
        super(ContactAdd, self).__init__()

        self.setWindowTitle('Add contact')
        self.setWindowIcon(QtGui.QIcon('../images/success (9)'))

        # contact name and salutation

        self.contact_salutation = QtWidgets.QComboBox()
        self.contact_salutation.addItem('Mr.')
        self.contact_salutation.addItem('Mrs.')
        self.contact_salutation.addItem('Sir')
        self.contact_salutation.addItem('Madam')

        self.contact_first_name = QtWidgets.QLineEdit()
        self.contact_first_name.setPlaceholderText('First name')
        self.contact_last_name = QtWidgets.QLineEdit()
        self.contact_last_name.setPlaceholderText('Last name')

        contact_layout = QtWidgets.QHBoxLayout()
        contact_layout.addWidget(self.contact_salutation)
        contact_layout.addWidget(self.contact_first_name)
        contact_layout.addWidget(self.contact_last_name)

        # display and contact type

        self.contact_display_name = QtWidgets.QLineEdit()
        self.contact_display_name.setFixedWidth(300)
        self.contact_display_name.setPlaceholderText("Display name")

        self.contact_type = QtWidgets.QComboBox()
        self.contact_type.addItem('Supplier')
        self.contact_type.addItem('Customer')
        self.contact_type.addItem('Support')

        display_contact_type_layout = QtWidgets.QHBoxLayout()
        display_contact_type_layout.addWidget(self.contact_display_name)
        display_contact_type_layout.addWidget(self.contact_type)

        # phone and email

        self.contact_phone_number = QtWidgets.QLineEdit()
        self.contact_phone_number.setPlaceholderText('Phone number')

        self.contact_email = QtWidgets.QLineEdit()
        self.contact_email.setPlaceholderText('E-mail')

        self.phone_email_layout = QtWidgets.QHBoxLayout()
        self.phone_email_layout.addWidget(self.contact_phone_number)
        self.phone_email_layout.addWidget(self.contact_email)

        # company name & locatipn

        self.contact_company_name = QtWidgets.QLineEdit()
        self.contact_company_name.setPlaceholderText("Company name")

        self.contact_company_location = QtWidgets.QLineEdit()
        self.contact_company_location.setPlaceholderText("Enter Location")

        company_location_layout = QtWidgets.QHBoxLayout()
        company_location_layout.addWidget(self.contact_company_name)
        company_location_layout.addWidget(self.contact_company_location)

        # notes

        self.notes = QtWidgets.QLineEdit()
        self.notes.setPlaceholderText('Enter describing notes')
        self.notes.setFixedHeight(100)

        notes_groupbox = QtWidgets.QGroupBox('Description')
        notes_label = QtWidgets.QLabel('Enter short notes concerning contact')

        notes_layout = QtWidgets.QVBoxLayout()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes)
        notes_groupbox.setLayout(notes_layout)

        # buttons

        submit_btn = QtWidgets.QPushButton('Submit')
        submit_btn.setStyleSheet('background-color:green')
        submit_btn.clicked.connect(self.contact_submit_btn)

        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.contact_reset_btn)

        self.cancel_btn = QtWidgets.QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(self.cancel_btn)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(contact_layout)
        layout.addLayout(display_contact_type_layout)
        layout.addLayout(self.phone_email_layout)
        layout.addLayout(company_location_layout)
        layout.addWidget(notes_groupbox)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def contact_submit_btn(self):

        print(self.contact_salutation.currentText())
        print(self.contact_first_name.text())
        print(self.contact_last_name.text())
        print(self.contact_display_name.text())
        print(self.contact_type.currentText())
        print(self.contact_phone_number.text())
        print(self.contact_email.text())
        print(self.contact_company_name.text())
        print(self.contact_company_location.text())
        print(self.notes.text())

        c_salutation = self.contact_salutation.currentText()
        c_first_name = self.contact_first_name.text()
        c_last_name = self.contact_last_name.text()
        c_display_name = self.contact_display_name.text()
        c_company_name = self.contact_company_name.text()
        c_location = self.contact_company_location.text()
        c_type = self.contact_type.currentText()
        c_phone_number = self.contact_phone_number.text()
        c_email = self.contact_email.text()
        c_notes = self.notes.text()

        try:
            cursor = connection.cursor()

            query = ''' INSERT INTO contacts_demo
            (contact_id, contact_salutation, contact_first_name, 
            contact_last_name, contact_display_name, 
            contact_work_company, contact_location,
            contact_type, contact_phone_number, contact_email, contact_notes)
            VALUES (uuid_generate_v4(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            data = (c_salutation, c_first_name, c_last_name, c_display_name,
                    c_company_name, c_location, c_type, c_phone_number, c_email,
                    c_notes)

            cursor.execute(query, data)

            if data:
                print('Submission was successful')
                submit_action = SubmitAction()
                submit_action.exec_()

            connection.commit()

        except Exception:
            print('Submission was futile.')
            fatal_action = FatalAction()
            fatal_action.exec_()
            # QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), 'Fatal', 'Addition failed, \n Check details.')

    def contact_reset_btn(self):
        self.contact_first_name.clear()
        self.contact_last_name.clear()
        self.contact_display_name.clear()
        self.contact_phone_number.clear()
        self.contact_email.clear()
        self.contact_company_name.clear()
        self.contact_company_location.clear()
        self.notes.clear()


# once make_order button is clicked under dashboard's product table


class MakeOrder(QtWidgets.QDialog):
    def __init__(self):
        super(MakeOrder, self).__init__()

        self.setWindowTitle('Order')
        self.setWindowIcon(QtGui.QIcon('../images/success (9)'))

        # order title, priority and the date

        self.order_title = QtWidgets.QLineEdit()
        self.order_title.setPlaceholderText('Order Title')

        self.order_urgency = QtWidgets.QComboBox()
        self.order_urgency.setToolTip("Select the order's urgency")
        self.order_urgency.addItem('High')
        self.order_urgency.addItem('Moderate')
        self.order_urgency.addItem('Low')

        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")
        system_date = QtWidgets.QLabel()
        system_date.setText(str(date))

        title_urgency_layout = QtWidgets.QHBoxLayout()
        title_urgency_layout.addWidget(self.order_title)
        title_urgency_layout.addWidget(self.order_urgency)
        title_urgency_layout.addWidget(system_date)

        # product name

        self.product_name = QtWidgets.QLineEdit()
        self.product_name.setPlaceholderText('Product name')

        # product buying price and selling price

        self.product_buying_price = QtWidgets.QLineEdit()
        self.product_buying_price.setPlaceholderText('product buying price')

        self.product_selling_price = QtWidgets.QLineEdit()
        self.product_selling_price.setPlaceholderText('product selling price')

        price_layout = QtWidgets.QHBoxLayout()
        price_layout.addWidget(self.product_buying_price)
        price_layout.addWidget(self.product_selling_price)

        # quantity & size

        self.quantity = QtWidgets.QLineEdit()
        self.quantity.setPlaceholderText('Product quantity.')

        self.quantifier = QtWidgets.QComboBox()
        self.quantifier.addItem(' Pieces')
        self.quantifier.addItem(' Pack')
        self.quantifier.addItem(' dozen')
        self.quantifier.addItem(' Bundle')
        self.quantifier.addItem(' Sack')

        # size
        self.size = QtWidgets.QLineEdit()
        self.size.setPlaceholderText('Product size')

        self.measuring_unit = QtWidgets.QComboBox()
        self.measuring_unit.addItem(' Grams (g)')
        self.measuring_unit.addItem(' Kilograms (kg)')
        self.measuring_unit.addItem(' Litres (l)')
        self.measuring_unit.addItem(' Milliliter (ml)')

        size_quantity_layout = QtWidgets.QHBoxLayout()
        size_quantity_layout.addWidget(self.quantity, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(self.quantifier, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(self.size, alignment=QtCore.Qt.AlignRight)
        size_quantity_layout.addWidget(self.measuring_unit, alignment=QtCore.Qt.AlignRight)

        # supplier selection

        # self.supplier_selection = QtWidgets.QPushButton('supplier selection')
        self.supplier_selection = QtWidgets.QComboBox()
        self.supplier_selection.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        # self.supplier_selection.setEditable(True)
        names = ['John', 'Sarah', 'Andrew', 'Faith', 'James']
        completer = QtWidgets.QCompleter(names)
        completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.supplier_selection.setCompleter(completer)

        self.supplier_selection.setToolTip('Select Supplier')
        self.supplier_selection.addItem('John')
        self.supplier_selection.addItem('Sarah')
        self.supplier_selection.addItem('Andrew')
        self.supplier_selection.addItem('Faith')
        self.supplier_selection.addItem('James')

        # phone and email

        self.phone_number = QtWidgets.QLineEdit()
        self.phone_number.setPlaceholderText('Supplier phone number')
        # self.phone_number.setDisabled(True)

        self.email = QtWidgets.QLineEdit()
        self.email.setPlaceholderText('E-mail')
        # self.email.setDisabled(True)

        phone_email_layout = QtWidgets.QHBoxLayout()
        phone_email_layout.addWidget(self.phone_number)
        phone_email_layout.addWidget(self.email)

        # notes

        self.order_notes = QtWidgets.QLineEdit()
        self.order_notes.setPlaceholderText('Enter describing notes')
        self.order_notes.setFixedHeight(100)

        notes_groupbox = QtWidgets.QGroupBox('Description')
        notes_label = QtWidgets.QLabel('Enter short notes concerning order')

        notes_layout = QtWidgets.QVBoxLayout()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.order_notes)
        notes_groupbox.setLayout(notes_layout)

        # buttons

        submit_btn = QtWidgets.QPushButton('Submit')
        submit_btn.setStyleSheet('background-color:green')
        submit_btn.clicked.connect(self.order_submit_btn)

        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.order_reset_btn)

        self.cancel_btn = QtWidgets.QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(self.cancel_btn)

        # main layout

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(title_urgency_layout)
        layout.addWidget(self.product_name)
        layout.addLayout(size_quantity_layout)
        layout.addLayout(price_layout)
        layout.addWidget(self.supplier_selection)
        layout.addLayout(phone_email_layout)
        layout.addWidget(notes_groupbox)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def order_submit_btn(self):
        o_title = self.order_title.text()
        o_urgency = self.order_urgency.currentText()
        p_name = self.product_name.text()
        p_buying_price = self.product_buying_price.text()
        p_selling_price = self.product_selling_price.text()

        quantity = self.quantity.text()
        quantifier = self.quantifier.currentText()
        # p_quantity = quantity + quantifier

        size = self.size.text()
        measuring_unit = self.measuring_unit.currentText()
        p_size = size + measuring_unit

        s_name = self.supplier_selection.currentText()
        s_phone_number = self.phone_number.text()
        s_email = self.email.text()
        o_notes = self.order_notes.text()

        print(o_title)
        print(o_urgency)
        print(p_name)
        print(p_buying_price)
        print(p_selling_price)
        # print(p_quantity)
        print(p_size)
        print(s_name)
        print(s_phone_number)
        print(s_email)
        print(o_notes)

        try:
            cursor = connection.cursor()

            query = '''INSERT INTO orders_demo
            (order_id, order_title, order_urgency, product_name,
            product_buying_price, product_selling_price, product_quantity, product_quantifier,
            product_size, supplier_name, supplier_phone_number, 
            supplier_email, order_notes)
            VALUES (uuid_generate_v4(), %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            data = (o_title, o_urgency, p_name, p_buying_price, p_selling_price,
                    quantity, quantifier, p_size, s_name, int(s_phone_number), s_email, o_notes)

            cursor.execute(query, data)

            if data:
                print('Submission was successful')
                submit_action = SubmitAction()
                submit_action.exec_()

            connection.commit()

        except Exception:
            print('Submission was futile')
            fatal_action = FatalAction()
            fatal_action.exec_()

    def order_reset_btn(self):
        self.order_title.clear()
        self.product_name.clear()
        self.product_buying_price.clear()
        self.product_selling_price.clear()
        self.quantity.clear()
        self.size.clear()
        self.phone_number.clear()
        self.email.clear()
        self.order_notes.clear()


class About_Action(QtWidgets.QDialog):
    def __init__(self):
        super(About_Action, self).__init__()

        self.setWindowTitle('About Software')
        self.setWindowIcon(QtGui.QIcon('../images/success (6)'))
        self.setFixedWidth(500)
        self.setFixedHeight(300)

        vbox = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel('Pegasus IMS (Inventory Management System)')
        title.setFont(QtGui.QFont('Cambria', 15))
        description = QtWidgets.QLabel('This is a product of Pegasus Foundation \n Pegasus V1.0, 2020')
        description.setFont(QtGui.QFont('Cambria', 10))
        label_image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('../images/systembone.jpg')
        pixmap = pixmap.scaledToWidth(500)
        label_image.setPixmap(pixmap)

        accept_btn = QtWidgets.QDialogButtonBox.Ok
        button_box = QtWidgets.QDialogButtonBox(accept_btn)
        button_box.accepted.connect(self.accept)

        vbox.addWidget(title, alignment=QtCore.Qt.AlignLeft)
        vbox.addWidget(description, alignment=QtCore.Qt.AlignLeft)
        vbox.addWidget(label_image, alignment=QtCore.Qt.AlignLeft)
        vbox.addWidget(button_box, alignment=QtCore.Qt.AlignRight)

        self.setLayout(vbox)


# before actual application starts, this is triggered


class Login(QtWidgets.QDialog):
    def __init__(self):
        super(Login, self).__init__()

        self.setWindowTitle('Login')
        self.setWindowIcon(QtGui.QIcon('../images/success (6)'))

        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setPlaceholderText('User')

        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.textPass.setPlaceholderText('Password')
        self.textPass.setMaxLength(4)

        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        # self.buttonLogin.clicked.connect(self.captured_name)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    # def captured_name(self):
    #     captured_name = self.textName.text()
    #     sale_ui = SalesUi()
    #     sale_ui.summary_groupbox_layout.addWidget(QtWidgets.QLabel('Sold by: ' + captured_name))
    #     print(captured_name)

    def handleLogin(self):
        if self.textName.text() == 'Josh' and self.textPass.text() == '1234':

            try:
                cursor = connection.cursor()
                now = datetime.datetime.now()
                date = now.strftime("%B %d, %Y")
                str_date = str(date)

                query = '''INSERT INTO admin_log (name, date) VALUES (%s, %s)'''
                name = self.textName.text()
                data = (name, str_date)
                cursor.execute(query, data)

                connection.commit()

            except Exception:
                print('futile')

            self.accept()

        elif self.textName.text() == 'Dee' and self.textPass.text() == '5678':

            try:
                cursor = connection.cursor()
                now = datetime.datetime.now()
                date = now.strftime("%B %d, %Y")
                str_date = str(date)

                query = '''INSERT INTO admin_log (name, date) VALUES (%s, %s)'''
                name = self.textName.text()
                data = (name, str_date)
                cursor.execute(query, data)

                connection.commit()

            except Exception:
                print('futile')

            self.accept()
        elif self.textName.text() == 'David' and self.textPass.text() == '9123':

            try:
                cursor = connection.cursor()
                now = datetime.datetime.now()
                date = now.strftime("%B %d, %Y")
                str_date = str(date)

                query = '''INSERT INTO admin_log (name, date) VALUES (%s, %s)'''
                name = self.textName.text()
                data = (name, str_date)
                cursor.execute(query, data)

                connection.commit()

            except Exception:
                print('futile')

            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Check your details')


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
# app.setStyle('Fusion')
login = Login()

if login.exec_() == QtWidgets.QDialog.Accepted:
    window = MainWindow()
    sys.exit(app.exec())
