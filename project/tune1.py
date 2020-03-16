from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import psycopg2
import time
import datetime
import sys

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
        super().__init__()

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

        #File Menu
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
        super().__init__()

# menu frame

        menu_layout = QtWidgets.QVBoxLayout()
        menu_layout.setAlignment(QtCore.Qt.AlignTop)

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
        self.salesUI()
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
        pass

    def invoices_display(self):
        pass

    def orders_display(self):
        self.stack.setCurrentWidget(self.orders)

    def bills_display(self):
        pass

    def reports_display(self):
        pass

# once dashboard button is clicked (from menu)

    def dashboardUI(self):
        tab_widget = QtWidgets.QTabWidget()

        self.products_tab = QtWidgets.QWidget()
        self.contacts_tab = QtWidgets.QWidget()
        self.order_tab = QtWidgets.QWidget()

        tab_widget.addTab(self.products_tab, "Products")
        tab_widget.addTab(self.contacts_tab, "Contacts")
        tab_widget.addTab(self.order_tab, "Orders")

        self.products_tabUI()
        self.contacts_tabUI()
        self.orders_tabUI()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tab_widget)

        self.dashboard.setLayout(layout)

# dashboard tabs are: products, contacts & orders

# products tab under dashboard

    def products_tabUI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.products_table = Table()
        self.products_table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.products_table.content_groupbox.setTitle('Products')
        self.products_table.table.setColumnCount(12)
        self.products_table.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Quantity', 'Total B.Price',
                                                             'Total S.Price', 'Total Profit', 'Notes'))
        self.products_table.add_button.clicked.connect(self.product_addUI)
        self.products_table.refresh_button.clicked.connect(self.refresh_UI)

        cursor = connection.cursor()
        cursor.execute('select product_id, product_name, product_size, product_category, '
                       'product_buying_price, product_selling_price, product_selling_price - product_buying_price, '
                       'product_quantity, product_pack_bp, product_pack_sp, product_pack_sp - product_pack_bp, '
                       'product_notes from products order by product_name;')

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.products_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.products_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.products_table.table.rowCount()
        self.total_label = QtWidgets.QLabel('Total: ' + str(total))

        self.products_table.content_overall_layout.addWidget(self.total_label)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        search_products_panel = QtWidgets.QLineEdit()
        search_products_panel.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignRight)
        search_layout.addWidget(search_products_panel)
        search_layout.addWidget(search_products_btn)

        layout.addLayout(search_layout)
        layout.addWidget(self.products_table)

        self.products_tab.setLayout(layout)

# add product btn

    def product_addUI(self):
        product_add = ProductAdd()
        product_add.exec_()

# refresh product btn

    def refresh_UI(self):
        self.products_table.table.clear()
        self.products_table.table.setRowCount(0)
        self.products_table.table.setColumnCount(12)
        self.products_table.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                                             'S.Price', 'Profit', 'Quantity', 'Total B.Price',
                                                             'Total S.Price', 'Total Profit', 'Notes'))

        cursor = connection.cursor()
        cursor.execute('select product_id, product_name, product_size, product_category, '
                       'product_buying_price, product_selling_price, product_selling_price - product_buying_price, '
                       'product_quantity, product_pack_bp, product_pack_sp, product_pack_sp - product_pack_bp, '
                       'product_notes from products order by product_name;')

        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            self.products_table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.products_table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = self.products_table.table.rowCount()
        self.total_label.setText('Total: ' + str(total))

    # contacts tab under dashboard

    def contacts_tabUI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        table = Table()
        table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.content_groupbox.setTitle('Contacts')
        table.table.setColumnCount(11)
        table.table.setHorizontalHeaderLabels(('Company', 'Display Name', 'First Name',
                                               'First Name', 'Contact Type', 'Location',
                                               'Phone number', 'E-mail'))
        table.add_button.clicked.connect(self.contact_addUI)

        cursor = connection.cursor()
        cursor.execute('select contact_work_company, contact_display_name, '
                       'contact_first_name, contact_last_name, '
                       'contact_type, contact_location, contact_phone_number, '
                       'contact_email '
                       'from contacts order by contact_work_company;')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = table.table.rowCount()
        total_label = QtWidgets.QLabel('Total: ' + str(total))

        table.content_overall_layout.addWidget(total_label)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        search_products_label = QtWidgets.QLineEdit()
        search_products_label.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignRight)
        search_layout.addWidget(search_products_label)
        search_layout.addWidget(search_products_btn)

        layout.addLayout(search_layout)
        layout.addWidget(table)
        self.contacts_tab.setLayout(layout)

# add contact btn command

    def contact_addUI(self):
        contact_add = ContactAdd()
        contact_add.exec_()

# orders tab under dashboard

    def orders_tabUI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        make_oder_btn = QtWidgets.QPushButton('Make order')
        make_oder_btn.clicked.connect(self.make_orderUI)
        make_oder_btn.setFixedWidth(300)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        search_products_panel = QtWidgets.QLineEdit()
        search_products_panel.setFixedWidth(200)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignRight)
        search_layout.addWidget(search_products_panel)
        search_layout.addWidget(search_products_btn)

        layout.addLayout(search_layout)
        layout.addWidget(make_oder_btn)
        self.order_tab.setLayout(layout)

# Make order btn command

    def make_orderUI(self):
        order = MakeOrder()
        order.exec_()

# once contacts button is clicked (from menu)

    def contactsUI(self):

        layout = QtWidgets.QHBoxLayout()
        tab = QtWidgets.QTabWidget()

        self.contactstab1 = QtWidgets.QWidget()
        self.contactstab2 = QtWidgets.QWidget()
        self.contactstab3 = QtWidgets.QWidget()

        tab.addTab(self.contactstab1, 'View Contacts')
        tab.addTab(self.contactstab2, 'Add Contacts')
        tab.addTab(self.contactstab3, 'Remove Contact(s)')

        self.contactstab1UI()
        self.contactstab2UI()
        self.contactstab3UI()

        layout.addWidget(tab)
        self.suppliers.setLayout(layout)

# Contacts tabs

    def contactstab1UI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        table = Table()
        table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.content_groupbox.setTitle('contacts')
        table.table.setColumnCount(11)
        table.table.setHorizontalHeaderLabels(('Company', 'Display Name', 'First Name',
                                               'First Name', 'Contact Type', 'Location',
                                               'Phone number', 'E-mail'))
        table.add_button.hide()
        table.edit_button.hide()
        table.refresh_button.hide()
        table.remove_button.hide()

        cursor = connection.cursor()
        cursor.execute('select contact_work_company, contact_display_name, '
                       'contact_first_name, contact_last_name, '
                       'contact_type, contact_location, contact_phone_number, '
                       'contact_email '
                       'from contacts order by contact_work_company;')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = table.table.rowCount()
        total_label = QtWidgets.QLabel('Total: ' + str(total))

        table.content_overall_layout.addWidget(total_label)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        search_products_panel = QtWidgets.QLineEdit()
        search_products_panel.setFixedWidth(200)

        contact_type_label = QtWidgets.QLabel('Select contact type. ')
        contact_type = QtWidgets.QComboBox()
        contact_type.addItem('All')
        contact_type.addItem('Suppliers')
        contact_type.addItem('Customers')
        contact_type.addItem('Allies')

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignLeft)
        search_layout.addWidget(search_products_btn)
        search_layout.addWidget(search_products_panel)
        search_layout.addWidget(contact_type_label, alignment=QtCore.Qt.AlignRight)
        search_layout.addWidget(contact_type)

        layout.addLayout(search_layout)
        layout.addWidget(table)

        self.contactstab1.setLayout(layout)

    def contactstab2UI(self):
            layout = QtWidgets.QFormLayout()

            self.add_btn = QtWidgets.QPushButton('Add', self)
            cancel_btn = QtWidgets.QPushButton('Cancel', self)

            self.name = QtWidgets.QLineEdit()
            layout.addRow('Name', self.name)

            self.quanity = QtWidgets.QLineEdit()
            layout.addRow('Quantity', self.quanity)

            layout.addWidget(self.add_btn)
            layout.addWidget(cancel_btn)

            cancel_btn.clicked.connect(self.name.clear)
            cancel_btn.clicked.connect(self.quanity.clear)

            self.contactstab2.setLayout(layout)

    def contactstab3UI(self):
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

            self.contactstab3.setLayout(layout)

# once products button is clicked (from menu)

    def productsUI(self):

        layout = QtWidgets.QHBoxLayout()
        tab = QtWidgets.QTabWidget()

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()

        tab.addTab(self.tab1, 'View Products')
        tab.addTab(self.tab2, 'Add Products')
        tab.addTab(self.tab3, 'Reduce Products')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        layout.addWidget(tab)
        self.products.setLayout(layout)

# tab actions for products, contacts and orders. for the menu buttons.

    def tab1UI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        table = Table()
        table.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.content_groupbox.setTitle('Products')
        table.table.setColumnCount(12)
        table.table.setHorizontalHeaderLabels(('Id', 'Name', 'Size', 'Category', 'B.Price',
                                               'S.Price', 'Profit', 'Pack B.Price', 'Pack S.Price',
                                               'Quantity', 'Notes'))
        table.add_button.hide()
        table.edit_button.hide()
        table.refresh_button.hide()
        table.remove_button.hide()

        cursor = connection.cursor()
        cursor.execute('select product_id, product_name, product_size, product_category, '
                       'product_buying_price, product_selling_price, product_selling_price - product_buying_price, product_pack_bp,'
                       'product_pack_sp, product_quantity, product_notes from products order by product_name;')
        results = cursor.fetchall()

        for row_number, row_data in enumerate(results):
            table.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                table.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

        total = table.table.rowCount()
        total_label = QtWidgets.QLabel('Total: ' + str(total))

        table.content_overall_layout.addWidget(total_label)

        search_products_btn = QtWidgets.QPushButton('Search')
        search_products_btn.setFixedWidth(100)
        search_products_panel = QtWidgets.QLineEdit()
        search_products_panel.setFixedWidth(200)

        contact_type_label = QtWidgets.QLabel('Select contact type. ')
        contact_type = QtWidgets.QComboBox()
        contact_type.addItem('Select category')
        contact_type.addItem('Food stuff & snacks')
        contact_type.addItem('Beverages')
        contact_type.addItem('Medicine')
        contact_type.addItem('Cleaning accessories')
        contact_type.addItem('Stationeries')

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setAlignment(QtCore.Qt.AlignLeft)
        search_layout.addWidget(search_products_btn)
        search_layout.addWidget(search_products_panel)
        search_layout.addWidget(contact_type_label, alignment=QtCore.Qt.AlignRight)
        search_layout.addWidget(contact_type)

        layout.addLayout(search_layout)
        layout.addWidget(table)

        self.tab1.setLayout(layout)

    def tab2UI(self):
            layout = QtWidgets.QFormLayout()

            self.add_btn = QtWidgets.QPushButton('Add', self)
            cancel_btn = QtWidgets.QPushButton('Cancel', self)

            self.name = QtWidgets.QLineEdit()
            layout.addRow('Name', self.name)

            self.quanity = QtWidgets.QLineEdit()
            layout.addRow('Quantity', self.quanity)

            layout.addWidget(self.add_btn)
            layout.addWidget(cancel_btn)

            cancel_btn.clicked.connect(self.name.clear)
            cancel_btn.clicked.connect(self.quanity.clear)

            self.tab2.setLayout(layout)

    def tab3UI(self):
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

            self.tab3.setLayout(layout)

# once sales button is clicked (from menu)

    def salesUI(self):
       pass

# once invoices button is clicked (from menu)

    def invoicesUI(self):
       pass

# once orders button is clicked (from menu)

    def ordersUI(self):
       pass

# once bills button is clicked (from menu)

    def billsUI(self):
       pass

# once reports button is clicked (from menu)

    def reportsUI(self):
        layout = QtWidgets.QHBoxLayout()
        tab = QtWidgets.QTabWidget()

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()

        tab.addTab(self.tab1, 'View Orders')
        tab.addTab(self.tab2, 'Add Orders')
        tab.addTab(self.tab3, 'Reduce Orders')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        layout.addWidget(tab)
        self.orders.setLayout(layout)


class MenuAction(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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
        super().__init__()

        self.content_groupbox = QtWidgets.QGroupBox('Table')
        self.content_overall_layout = QtWidgets.QVBoxLayout()
        self.content_groupbox.setLayout(self.content_overall_layout)
        self.content_groupbox.setFixedHeight(300)

        content_groupbox_layout = QtWidgets.QHBoxLayout()
        content_groupbox_layout.setAlignment(QtCore.Qt.AlignTop)

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
        button_layout.addWidget(self.refresh_button, alignment=QtCore.Qt.AlignBottom)
        button_layout.addWidget(self.remove_button, alignment=QtCore.Qt.AlignBottom)

        content_groupbox_layout.addWidget(self.table)
        content_groupbox_layout.addLayout(button_layout)

        self.content_overall_layout.addLayout(content_groupbox_layout)
        # content_overall_layout.addWidget(self.total_label)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addWidget(self.content_groupbox)
        content_layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(content_layout)

# once add button is clicked under dashboard's product table


class ProductAdd(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

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
        submit_btn.clicked.connect(self.product_submit_btn)

        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.product_reset_btn)

        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)

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
        measure_units = self.measuring_unit.currentText()
        size = p_size + measure_units

        p_category = self.category.currentText()
        p_bp = self.unit_buying_price.text()
        p_sp = self.unit_selling_price.text()

        p_quantity = self.quantity.text()
        quantifier = self.quantifier.currentText()
        quantity = p_quantity + quantifier

        p_total_bp = self.total_buying_price.text()
        p_total_sp = self.total_selling_price.text()
        p_notes = self.notes.text()

        try:
            cursor = connection.cursor()

            query = ''' INSERT INTO products
            (product_name, product_size, 
            product_category, product_buying_price, 
            product_selling_price, product_quantity,
            product_pack_bp, product_pack_sp, product_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            data = (p_name, size, p_category, p_bp, p_sp, quantity,
                    p_total_bp, p_total_sp, p_notes)

            cursor.execute(query, data)

            if data:
                print('successfully added')
                submit_btn = ProductSubmitAction()
                submit_btn.exec_()

            connection.commit()

        except Exception:
            QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), 'Fatal', 'Product was not added')

    def product_reset_btn(self):
        self.name_field.clear()
        self.unit_buying_price.clear()
        self.unit_selling_price.clear()
        self.total_buying_price.clear()
        self.total_selling_price.clear()
        self.quantity.clear()
        self.quantity_spinbox.clear()
        self.size.clear()
        self.notes.clear()

    # when submit btn is clicked across all tabs' add action under the dashboard


class ProductSubmitAction(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Success')
        self.setWindowIcon(QtGui.QIcon('../images/success (8)'))

# submission label

        submission_label = QtWidgets.QLabel('Product was successfully added')

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
        super().__init__()

        self.setWindowTitle('Add contact')
        self.setWindowIcon(QtGui.QIcon('../images/success (9)'))

# contact name and salutation

        contact_salutation = QtWidgets.QComboBox()
        contact_salutation.addItem('Mr.')
        contact_salutation.addItem('Mrs.')
        contact_salutation.addItem('Sir')
        contact_salutation.addItem('Madam')

        contact_first_name = QtWidgets.QLineEdit()
        contact_first_name.setPlaceholderText('First name')
        contact_last_name = QtWidgets.QLineEdit()
        contact_last_name.setPlaceholderText('Last name')

        contact_layout = QtWidgets.QHBoxLayout()
        contact_layout.addWidget(contact_salutation)
        contact_layout.addWidget(contact_first_name)
        contact_layout.addWidget(contact_last_name)

# display and contact type

        contact_display_name = QtWidgets.QLineEdit()
        contact_display_name.setFixedWidth(300)
        contact_display_name.setPlaceholderText("Display name")

        contact_type = QtWidgets.QComboBox()
        contact_type.addItem('Supplier')
        contact_type.addItem('Customer')
        contact_type.addItem('Support')

        display_contact_type_layout = QtWidgets.QHBoxLayout()
        display_contact_type_layout.addWidget(contact_display_name)
        display_contact_type_layout.addWidget(contact_type)

# phone and email

        phone_number = QtWidgets.QLineEdit()
        phone_number.setPlaceholderText('Phone number')

        email = QtWidgets.QLineEdit()
        email.setPlaceholderText('E-mail')

        phone_email_layout = QtWidgets.QHBoxLayout()
        phone_email_layout.addWidget(phone_number)
        phone_email_layout.addWidget(email)

# company name & locatipn

        contact_company_name = QtWidgets.QLineEdit()
        contact_company_name.setPlaceholderText("Company name")

        contact_company_location = QtWidgets.QLineEdit()
        contact_company_location.setPlaceholderText("Enter Location")

        company_location_layout = QtWidgets.QHBoxLayout()
        company_location_layout.addWidget(contact_company_name)
        company_location_layout.addWidget(contact_company_location)

# notes

        notes = QtWidgets.QLineEdit()
        notes.setPlaceholderText('Enter describing notes')
        notes.setFixedHeight(100)

        notes_groupbox = QtWidgets.QGroupBox('Description')
        notes_label = QtWidgets.QLabel('Enter short notes concerning contact')

        notes_layout = QtWidgets.QVBoxLayout()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(notes)
        notes_groupbox.setLayout(notes_layout)

# buttons

        submit_btn = QtWidgets.QPushButton('Submit')
        submit_btn.clicked.connect(self.contact_submit_btn)

        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.contact_reset_btn)

        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)


# main layout

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(contact_layout)
        layout.addLayout(display_contact_type_layout)
        layout.addLayout(phone_email_layout)
        layout.addLayout(company_location_layout)
        layout.addWidget(notes_groupbox)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def contact_submit_btn(self):
        pass

    def contact_reset_btn(self):
        pass

# once make_order button is clicked under dashboard's product table


class MakeOrder(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Order')
        self.setWindowIcon(QtGui.QIcon('../images/success (9)'))

# date and time

# product name

        product_name = QtWidgets.QLineEdit()
        product_name.setPlaceholderText('Product name')

        product_urgency = QtWidgets.QComboBox()
        product_urgency.addItem('High')
        product_urgency.addItem('Moderate')
        product_urgency.addItem('Low')

        product_urgency_layout = QtWidgets.QHBoxLayout()
        product_urgency_layout.addWidget(product_name)
        product_urgency_layout.addWidget(product_urgency)

# quantity & size

        quantity = QtWidgets.QLineEdit()
        quantity.setPlaceholderText('Product quantity.')

        quantifier = QtWidgets.QComboBox()
        quantifier.addItem('Piece')
        quantifier.addItem('Pack')
        quantifier.addItem('dozen')
        quantifier.addItem('Bundle')
        quantifier.addItem('Sack')
# size
        size = QtWidgets.QLineEdit()
        size.setPlaceholderText('Product size')

        measuring_unit = QtWidgets.QComboBox()
        measuring_unit.addItem('Grams (g)')
        measuring_unit.addItem('Kilograms (kg)')
        measuring_unit.addItem('Litres (l)')
        measuring_unit.addItem('Milliliter (ml)')

        size_quantity_layout = QtWidgets.QHBoxLayout()
        size_quantity_layout.addWidget(quantity, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(quantifier, alignment=QtCore.Qt.AlignLeft)
        size_quantity_layout.addWidget(size, alignment=QtCore.Qt.AlignRight)
        size_quantity_layout.addWidget(measuring_unit, alignment=QtCore.Qt.AlignRight)
# product buying price and selling price

        product_buying_price = QtWidgets.QLineEdit()
        product_buying_price.setPlaceholderText('product buying price')

        product_selling_price = QtWidgets.QLineEdit()
        product_selling_price.setPlaceholderText('product selling price')

        price_layout = QtWidgets.QHBoxLayout()
        price_layout.addWidget(product_buying_price)
        price_layout.addWidget(product_selling_price)
# phone and email

        phone_number = QtWidgets.QLineEdit()
        phone_number.setPlaceholderText('Supplier phone number')

        email = QtWidgets.QLineEdit()
        email.setPlaceholderText('E-mail')

        phone_email_layout = QtWidgets.QHBoxLayout()
        phone_email_layout.addWidget(phone_number)
        phone_email_layout.addWidget(email)

# notes

        notes = QtWidgets.QLineEdit()
        notes.setPlaceholderText('Enter describing notes')
        notes.setFixedHeight(100)

        notes_groupbox = QtWidgets.QGroupBox('Description')
        notes_label = QtWidgets.QLabel('Enter short notes concerning contact')

        notes_layout = QtWidgets.QVBoxLayout()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(notes)
        notes_groupbox.setLayout(notes_layout)

# buttons

        submit_btn = QtWidgets.QPushButton('Submit')
        submit_btn.clicked.connect(self.order_submit_btn)

        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.order_reset_btn)

        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)

# main layout

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(product_urgency_layout)
        layout.addLayout(size_quantity_layout)
        layout.addLayout(price_layout)
        layout.addLayout(phone_email_layout)
        layout.addWidget(notes_groupbox)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def order_submit_btn(self):
        pass

    def order_reset_btn(self):
        pass


class About_Action(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

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
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

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

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if self.textName.text() == 'Josh' and self.textPass.text() == '1234':
            self.accept()
        elif self.textName.text() == 'Dee' and self.textPass.text() == '5678':
            self.accept()
        elif self.textName.text() == 'David' and self.textPass.text() == '9123':
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Check your user name or password')


App = QtWidgets.QApplication(sys.argv)
login = Login()

if login.exec_() == QtWidgets.QDialog.Accepted:
    window = MainWindow()
    sys.exit(App.exec())
