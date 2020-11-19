#!/usr/bin/python3

import sys
import os
import re
import xlrd
import time
import csv
from fpdf import FPDF
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

from csv_excel import CsvToExcel
from water_mark import WaterMark
import config as cfg

file_location = ""


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOCIAL SNAPPER Version-1.0.0")
        self.setGeometry(450, 150, 750, 750)
        self.UI()
        self.show()

    def UI(self):

        self.maindesign()
        self.layout()

    def maindesign(self):

        self.setStyleSheet(
            "background-color:#F0FFF0;font-size:14pt;font-family:Times")
        self.setStyleSheet("QComboBox { background-color: #D3D3D3 }\
            " "QListView { color: black; }")

    def layout(self):
        """
        Create a basic layout.
        """
        self.mainlayout = QHBoxLayout()
        self.toplayout = QHBoxLayout()
        self.mainlayout.addLayout(self.toplayout)

        # Adding content to layout
        self.option = QLabel("Select the option and click 'OK'", self)
        self.option.setStyleSheet("font: 20pt Times")
        self.image = QLabel(self)
        self.image2 = QLabel(self)
        self.image3 = QLabel(self)
        self.image4 = QLabel(self)
        self.combobox = QComboBox(self)
        self.combobox.setStyleSheet("width:50px")
        mainbutton = QPushButton("OK", self)
        self.toplayout.addWidget(self.option)
        self.toplayout.addWidget(self.image)
        self.toplayout.addWidget(self.image2)
        self.toplayout.addWidget(self.image3)
        self.toplayout.addWidget(self.image4)
        self.toplayout.addWidget(mainbutton)
        self.image.setPixmap(QPixmap("icons/facebook-3.png"))
        self.image2.setPixmap(QPixmap("icons/instagram-2.png"))
        self.image3.setPixmap(QPixmap("icons/twitter-2.png"))
        self.image4.setPixmap(QPixmap("icons/youtube-2.png"))
        self.image.move(50, 50)
        self.image2.move(300, 50)
        self.image3.move(550, 50)
        self.image4.move(300, 250)
        self.option.move(210, 450)
        self.combobox.move(310, 520)
        mainbutton.move(310, 580)
        mainbutton.clicked.connect(self.select_option)
        self.toplayout.addWidget(self.combobox)
        list = ["Facebook", "Twitter", "Instagram", "Youtube", "Linkedin"]
        for name in list:
            self.combobox.addItem(name)

    def select_option(self):
        """
        This method will call classes of selected option.
        """
        value = self.combobox.currentText()
        print(value)
        if value == "Facebook":
            self.facebookWindow = FacebookSnap()
            self.close()
        if value == "Twitter":
            self.twitterWindow = TwitterSnap()
            self.close()
        if value == "Youtube":
            self.youtubeWindow = YoutubeSnap()
            self.close()
        if value =="Instagram":
            self.instagram_window = InstagramSnap()
            self.close()


class FacebookSnap(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOCIAL SNAPPER Version-1.0.0")
        self.setGeometry(450, 150, 400, 550)
        self.UI()
        self.show()

    def UI(self):
        self.maindesign()
        self.layout()

    def maindesign(self):
        """
        Main design for UI.
        """
        self.setStyleSheet(
            "background-color:#6495ED;font-size:14pt;font-family:Times")

    def layout(self):
        """
        Create a basic layout.
        """
        ###########Layout###########
        self.mainlayout = QHBoxLayout()
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)

        #########Button################
        self.button = QPushButton("Back", self)
        self.toplayout.addWidget(self.button)
        self.button.clicked.connect(self.fb_menu)
        self.button.setStyleSheet("background-color:#A9A9A9")
        self.button.move(10, 5)
        self.selectfile = QPushButton("Browse", self)
        self.toplayout.addWidget(self.selectfile)
        self.selectfile.clicked.connect(self.open_file)
        self.selectfile.setStyleSheet("background-color:#A9A9A9")
        self.selectfile.move(120, 310)
        self.start_btn = QPushButton("Start", self)
        self.toplayout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_process)
        self.start_btn.setStyleSheet("background-color:#696969;width:100px")
        self.start_btn.move(215, 310)

        ###############Image################
        self.image = QLabel(self)
        self.toplayout.addWidget(self.image)
        self.image.setPixmap(QPixmap("icons/facebook-logo.png"))
        self.image.move(145, 50)
        self.user_img = QLabel(self)
        self.toplayout.addWidget(self.user_img)
        self.user_img.setPixmap(QPixmap("icons/man-user-2.png"))
        self.user_img.move(80, 220)
        self.pass_img = QLabel(self)
        self.toplayout.addWidget(self.pass_img)
        self.pass_img.setPixmap(QPixmap("icons/lock-2.png"))
        self.pass_img.move(80, 250)
        self.file_img = QLabel(self)
        self.toplayout.addWidget(self.file_img)
        self.file_img.setPixmap(QPixmap("icons/file-2.png"))
        self.file_img.move(80, 280)

        ###########User Input###########
        self.nameTextBox = QLineEdit(self)
        self.toplayout.addWidget(self.nameTextBox)
        self.nameTextBox.setPlaceholderText("Please enter your email")
        self.nameTextBox.setStyleSheet("width:200px")
        self.nameTextBox.move(120, 220)
        self.passTextBox = QLineEdit(self)
        self.toplayout.addWidget(self.passTextBox)
        self.passTextBox.setPlaceholderText("Please enter your password")
        self.passTextBox.setEchoMode(QLineEdit.Password)
        self.passTextBox.setStyleSheet("width:200px")
        self.passTextBox.move(120, 250)
        self.filename = QLineEdit(self)
        self.filename.setStyleSheet("width:200px")
        self.filename.setReadOnly(True)
        self.toplayout.addWidget(self.filename)
        self.filename.setPlaceholderText("Please select the file")
        self.filename.move(120, 280)

        # Check Box
        self.default_credetails = QCheckBox("    Default Account", self)
        self.default_credetails.move(85, 190)

    def fb_menu(self):
        """
        Method to go back to main menu.
        """
        self.updateWindow = Main()
        self.close()

    def open_file(self):
        """
        Method to select file.
        """
        global file_location
        file_location = QFileDialog.getOpenFileName(
            self, "Open a file", "", "All files(*);;*txt")
        self.filename.setText(os.path.basename(file_location[0]))

    def create_folder(self):

        today = datetime.now()
        _time = time.strftime("%H-%M-%S")
        _date = today.strftime('%Y-%m-%d')
        folder = _date + "|" + _time
        os.mkdir("screenshots/Facebook/{}".format(folder))
        os.mkdir("screenshots/Facebook/{}/Active".format(folder))
        os.mkdir("screenshots/Facebook/{}/Closed".format(folder))
        return(folder)

    def start_process(self):

        try:
            global file_location
            if file_location == "":
                self.empty()
            else:
                folder_name = self.create_folder()
                username = self.nameTextBox.text()
                password = self.passTextBox.text()
                browser = webdriver.Firefox(executable_path = cfg.PATH)
                browser.set_window_position(0, 0)
                browser.set_window_size(1000, 800)
                wait = WebDriverWait(browser, 10)
                browser.get('https://www.facebook.com/')
                if (self.default_credetails.isChecked()):
                    username = cfg.USERNAME
                    password = cfg.PASSWORD
                wait.until(EC.visibility_of_element_located((By.ID, "email")))
                username_box = browser.find_element_by_id('email')
                username_box.send_keys(username)
                password_box = browser.find_element_by_id('pass')
                password_box.send_keys(password)
                password_box.send_keys(Keys.RETURN)
                time.sleep(4)
                online = 0
                blocked = 0
                page_not_found = 0
                loc = file_location[0]
                wb = xlrd.open_workbook(loc)
                sheet = wb.sheet_by_index(0)
                sheet.cell_value(0, 0)
                rows = sheet.nrows
                self.create_csv(folder_name)
                for i in range(rows):
                    url = sheet.cell_value(i, 1)
                    ref_id = sheet.cell_value(i, 0)
                    new_ref = ref_id.replace("/",".")
                    try:
                        browser.get(url)
                        time.sleep(5.5)
                        if re.search("This Content Isn't Available Right Now", browser.page_source) is not None:
                            status = "blocked"
                            blocked = blocked + 1
                            print(">>>" + os.path.basename(url) + " is blocked ")
                            s_no = i + 1
                            self.append_csv(s_no, ref_id, url, os.path.basename(
                                url), status, folder_name)
                            browser.save_screenshot(
                                "screenshots/Facebook/{}/Closed/{}.png".format(folder_name, new_ref))
                            image_path = "screenshots/Facebook/{}/Closed/{}.png".format(folder_name, new_ref)
                            WaterMark.water_mark(image_path, url, ref_id)
                        elif re.search("Sorry, this content isn't available at this time", browser.page_source) is not None:
                            status = "blocked"
                            blocked = blocked + 1
                            print(">>>" + os.path.basename(url) + "blocked")
                            s_no = i + 1
                            self.append_csv(s_no, ref_id, url, os.path.basename(
                                url), status, folder_name)
                            browser.save_screenshot(
                                "screenshots/Facebook/{}/Closed/{}.png".format(folder_name, new_ref))
                            image_path = "screenshots/Facebook/{}/Closed/{}.png".format(folder_name, new_ref)
                            WaterMark.water_mark(image_path, url, ref_id)
                        elif re.search("This Page Isn't Available", browser.page_source) is not None:
                            status = "page not found"
                            print(">>>" + os.path.basename(url) + "Page not found")
                            page_not_found = page_not_found + 1
                            s_no = i + 1
                            self.append_csv(s_no, ref_id, url, os.path.basename(
                                url), status, folder_name)
                            browser.save_screenshot(
                                "screenshots/Facebook/{}/Closed/{}.png".format(folder_name, new_ref))
                            image_path = "screenshots/Facebook/{}/Closed/{}.png".format(folder_name, new_ref)
                            WaterMark.water_mark(image_path, url, ref_id)
                        else:
                            status = "online"
                            online = online + 1
                            s_no = i + 1
                            self.append_csv(s_no,ref_id ,url , os.path.basename(
                                url), status, folder_name)
                            print(">>>" + os.path.basename(url) + " is online ")
                            browser.save_screenshot(
                                "screenshots/Facebook/{}/Active/{}.png".format(folder_name, new_ref))
                            image_path = "screenshots/Facebook/{}/Active/{}.png".format(folder_name, new_ref)
                            WaterMark.water_mark(image_path, url, ref_id)
                    except Exception as e:
                        pass
                print(">>> Total links = " + str(rows))
                print(">>> Online = " + str(online))
                print(">>> Blocked = " + str(blocked))
                print(">>> Page not found = " + str(page_not_found))
                browser.quit()
                folder_name_2 = "Facebook"
                CsvToExcel.csv2excel(folder_name, folder_name_2)
                self.message = QMessageBox.information(
                    self, "Done", "Task completed!")

        except Exception as e:
            print(e)


    def empty(self):
        self.message = QMessageBox.information(
                self, "Empty", "Please Select File!")
        
    def create_csv(self, folder):
        """Method to create csv file"""

        with open('screenshots/Facebook/{}/report.csv'.format(folder), mode='w') as csv_file:
            fieldnames = ['S.NO','Ref_ID', 'FACEBOOK URL', 'FACEBOOK NAME/ID',
                          'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def append_csv(self, s_no, ref_id, url, name_id, status, folder):
        """ Method to create csv file"""
        with open('screenshots/Facebook/{}/report.csv'.format(folder), 'a') as filename:
            _fields = ['S.NO', 'Ref_ID', 'FACEBOOK URL', 'FACEBOOK NAME/ID',
                       'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(filename, _fields)
            writer.writerow({'S.NO': s_no, 'Ref_ID':ref_id, 'FACEBOOK URL': url, 'FACEBOOK NAME/ID': name_id,
                             'ACTIVE/CLOSED': status, 'DATE/TIME': datetime.now().time()})


class TwitterSnap(QWidget):
    """
    This class will handel all links related to twitter
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOCIAL SNAPPER Version-1.0.0")
        self.setGeometry(450, 150, 400, 550)
        self.UI()
        self.show()

    def UI(self):
        self.maindesign()
        self.layout()

    def maindesign(self):
        """
        Main design for UI.
        """
        self.setStyleSheet(
            "background-color:#6495ED;font-size:14pt;font-family:Times")

        ###Layouts###
        self.mainlayout = QHBoxLayout()
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)

        ###Button###
        self.button = QPushButton("Back", self)
        self.toplayout.addWidget(self.button)
        self.button.clicked.connect(self.tw_menu)
        self.button.setStyleSheet("background-color:#A9A9A9")
        self.button.move(10, 5)
        self.selectfile = QPushButton("Browse", self)
        self.toplayout.addWidget(self.selectfile)
        self.selectfile.clicked.connect(self.open_file)
        self.selectfile.setStyleSheet("background-color:#A9A9A9")
        self.selectfile.move(120, 310)
        self.start_btn = QPushButton("Start", self)
        self.toplayout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_process)
        self.start_btn.setStyleSheet("background-color:#696969;width:100px")
        self.start_btn.move(215, 310)

        ###Images###
        self.image = QLabel(self)
        self.toplayout.addWidget(self.image)
        self.image.setPixmap(QPixmap("icons/twitter-3.png"))
        self.image.move(145, 50)
        self.file_img = QLabel(self)
        self.toplayout.addWidget(self.file_img)
        self.file_img.setPixmap(QPixmap("icons/file-2.png"))
        self.file_img.move(80, 280)

        ###User Input###
        self.filename = QLineEdit(self)
        self.filename.setStyleSheet("width:200px")
        self.filename.setReadOnly(True)
        self.toplayout.addWidget(self.filename)
        self.filename.setPlaceholderText("Please select the file")
        self.filename.move(120, 280)

    def open_file(self):
        """
        Method to select file.
        """
        global file_location
        file_location = QFileDialog.getOpenFileName(
            self, "Open a file", "", "All files(*);;*txt")
        self.filename.setText(os.path.basename(file_location[0]))

    def create_folder(self):
        today = datetime.now()
        _time = time.strftime("%H-%M-%S")
        _date = today.strftime('%Y-%m-%d')
        folder = _date + "|" + _time
        os.mkdir("screenshots/Twitter/{}".format(folder))
        os.mkdir("screenshots/Twitter/{}/Active".format(folder))
        os.mkdir("screenshots/Twitter/{}/Closed".format(folder))
        return(folder)   

    def create_csv(self, folder):
        """Method to create csv file"""

        with open('screenshots/Twitter/{}/report.csv'.format(folder), mode='w') as csv_file:
            fieldnames = ['S.NO','Ref_ID', 'Twitter URL', 'Twitter NAME/ID',
                          'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def append_csv(self, s_no, ref_id, url, name_id, status, folder):
        """ Method to create csv file"""
        with open('screenshots/Twitter/{}/report.csv'.format(folder), 'a') as filename:
            _fields = ['S.NO', 'Ref_ID', 'Twitter URL', 'Twitter NAME/ID',
                       'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(filename, _fields)
            writer.writerow({'S.NO': s_no, 'Ref_ID':ref_id, 'Twitter URL': url, 'Twitter NAME/ID': name_id,
                             'ACTIVE/CLOSED': status, 'DATE/TIME': datetime.now().time()})        

    def start_process(self):
        folder_name = self.create_folder()
        global file_location
        browser = webdriver.Firefox(executable_path = cfg.PATH)
        browser.set_window_position(0, 0)
        browser.set_window_size(1000, 800)
        wb = xlrd.open_workbook(file_location[0])
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        rows = sheet.nrows
        self.create_csv(folder_name)
        for i in range(rows):
            ref_id = sheet.cell_value(i, 0)
            new_ref = ref_id.replace("/", ".")
            url = sheet.cell_value(i, 1)
            browser.get(url)
            time.sleep(5.5)
            if re.search("Sorry, that page doesn’t exist!", browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Twitter/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Twitter/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            elif re.search("This Tweet is unavailable", browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Twitter/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Twitter/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            else:
                status = "online"
                s_no = i + 1
                self.append_csv(s_no,ref_id ,url , os.path.basename(
                    url), status, folder_name)
                print(">>>" + os.path.basename(url) + " is online ")
                browser.save_screenshot(
                    "screenshots/Twitter/{}/Active/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Twitter/{}/Active/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
        browser.quit()
        folder_name_2 = "Twitter"
        CsvToExcel.csv2excel(folder_name, folder_name_2)
        self.message = QMessageBox.information(self, "Done", "Task completed!")

    def tw_menu(self):
        """
        Method to go back to main menu.
        """
        self.mainWindow = Main()
        self.close()


class YoutubeSnap(QWidget):
    "This class will handle all snap related to youtube"


    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOCIAL SNAPPER Version-1.0.0")
        self.setGeometry(450, 150, 400, 550)
        self.UI()
        self.show()

    def UI(self):
        self.maindesign()
        self.layout()

    def maindesign(self):
        """
        Main design for UI.
        """
        self.setStyleSheet(
            "background-color:#E9F0F9;font-size:14pt;font-family:Times")

        ###Layouts###
        self.mainlayout = QHBoxLayout()
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)

        ###Button###
        self.button = QPushButton("Back", self)
        self.toplayout.addWidget(self.button)
        self.button.clicked.connect(self.tw_menu)
        self.button.setStyleSheet("background-color:#A9A9A9")
        self.button.move(10, 5)
        self.selectfile = QPushButton("Browse", self)
        self.toplayout.addWidget(self.selectfile)
        self.selectfile.clicked.connect(self.open_file)
        self.selectfile.setStyleSheet("background-color:#A9A9A9")
        self.selectfile.move(120, 310)
        self.start_btn = QPushButton("Start", self)
        self.toplayout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_process)
        self.start_btn.setStyleSheet("background-color:#696969;width:100px")
        self.start_btn.move(215, 310)

        ###Images###
        self.image = QLabel(self)
        self.toplayout.addWidget(self.image)
        self.image.setPixmap(QPixmap("icons/youtube-2.png"))
        self.image.move(145, 50)
        self.file_img = QLabel(self)
        self.toplayout.addWidget(self.file_img)
        self.file_img.setPixmap(QPixmap("icons/file-2.png"))
        self.file_img.move(80, 280)

        ###User Input###
        self.filename = QLineEdit(self)
        self.filename.setStyleSheet("width:200px")
        self.filename.setReadOnly(True)
        self.toplayout.addWidget(self.filename)
        self.filename.setPlaceholderText("Please select the file")
        self.filename.move(120, 280)

    def open_file(self):
        """
        Method to select file.
        """
        global file_location
        file_location = QFileDialog.getOpenFileName(
            self, "Open a file", "", "All files(*);;*txt")
        self.filename.setText(os.path.basename(file_location[0]))

    def create_folder(self):
        today = datetime.now()
        _time = time.strftime("%H-%M-%S")
        _date = today.strftime('%Y-%m-%d')
        folder = _date + "|" + _time
        os.mkdir("screenshots/Youtube/{}".format(folder))
        os.mkdir("screenshots/Youtube/{}/Active".format(folder))
        os.mkdir("screenshots/Youtube/{}/Closed".format(folder))
        return(folder)   

    def create_csv(self, folder):
        """Method to create csv file"""

        with open('screenshots/Youtube/{}/report.csv'.format(folder), mode='w') as csv_file:
            fieldnames = ['S.NO','Ref_ID', 'Youtube URL', 'Youtube NAME/ID',
                          'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def append_csv(self, s_no, ref_id, url, name_id, status, folder):
        """ Method to create csv file"""
        with open('screenshots/Youtube/{}/report.csv'.format(folder), 'a') as filename:
            _fields = ['S.NO', 'Ref_ID', 'Youtube URL', 'Youtube NAME/ID',
                       'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(filename, _fields)
            writer.writerow({'S.NO': s_no, 'Ref_ID':ref_id, 'Youtube URL': url, 'Youtube NAME/ID': name_id,
                             'ACTIVE/CLOSED': status, 'DATE/TIME': datetime.now().time()})        

    def start_process(self):
        folder_name = self.create_folder()
        global file_location
        browser = webdriver.Firefox(executable_path = cfg.PATH)
        browser.set_window_position(0, 0)
        browser.set_window_size(1000, 800)
        wb = xlrd.open_workbook(file_location[0])
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        rows = sheet.nrows
        self.create_csv(folder_name)
        for i in range(rows):
            ref_id = sheet.cell_value(i, 0)
            new_ref = ref_id.replace("/", ".")
            url = sheet.cell_value(i, 1)
            browser.get(url)
            time.sleep(5.5)
            youtube_pattern = "This content is not available on this country domain due to a legal complaint from the government."
            if re.search("This channel is not available in your country.", browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Youtube/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Youtube/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            elif re.search("Video unavailable", browser.page_source) and re.search(youtube_pattern, browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Youtube/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Youtube/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            else:
                status = "online"
                s_no = i + 1
                self.append_csv(s_no,ref_id ,url , os.path.basename(
                    url), status, folder_name)
                print(">>>" + os.path.basename(url) + " is online ")
                browser.save_screenshot(
                    "screenshots/Youtube/{}/Active/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Youtube/{}/Active/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
        browser.quit()
        folder_name_2 = "Youtube"
        CsvToExcel.csv2excel(folder_name, folder_name_2)
        self.message = QMessageBox.information(self, "Done", "Task completed!")

    def tw_menu(self):
        """
        Method to go back to main menu.
        """
        self.mainWindow = Main()
        self.close()

class InstagramSnap(QWidget):
    "This class will handle all snap related to instagram"


    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOCIAL SNAPPER Version-1.0.0")
        self.setGeometry(450, 150, 400, 550)
        self.UI()
        self.show()

    def UI(self):
        self.maindesign()
        self.layout()

    def maindesign(self):
        """
        Main design for UI.
        """
        self.setStyleSheet(
            "background-color:#E9F0F9;font-size:14pt;font-family:Times")

        ###Layouts###
        self.mainlayout = QHBoxLayout()
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.toplayout)
        self.mainlayout.addLayout(self.bottomlayout)

        ###Button###
        self.button = QPushButton("Back", self)
        self.toplayout.addWidget(self.button)
        self.button.clicked.connect(self.tw_menu)
        self.button.setStyleSheet("background-color:#A9A9A9")
        self.button.move(10, 5)
        self.selectfile = QPushButton("Browse", self)
        self.toplayout.addWidget(self.selectfile)
        self.selectfile.clicked.connect(self.open_file)
        self.selectfile.setStyleSheet("background-color:#A9A9A9")
        self.selectfile.move(120, 310)
        self.start_btn = QPushButton("Start", self)
        self.toplayout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_process)
        self.start_btn.setStyleSheet("background-color:#696969;width:100px")
        self.start_btn.move(215, 310)

        ###Images###
        self.image = QLabel(self)
        self.toplayout.addWidget(self.image)
        self.image.setPixmap(QPixmap("icons/instagram-2.png"))
        self.image.move(145, 50)
        self.file_img = QLabel(self)
        self.toplayout.addWidget(self.file_img)
        self.file_img.setPixmap(QPixmap("icons/file-2.png"))
        self.file_img.move(80, 280)

        ###User Input###
        self.filename = QLineEdit(self)
        self.filename.setStyleSheet("width:200px")
        self.filename.setReadOnly(True)
        self.toplayout.addWidget(self.filename)
        self.filename.setPlaceholderText("Please select the file")
        self.filename.move(120, 280)

    def open_file(self):
        """
        Method to select file.
        """
        global file_location
        file_location = QFileDialog.getOpenFileName(
            self, "Open a file", "", "All files(*);;*txt")
        self.filename.setText(os.path.basename(file_location[0]))

    def create_folder(self):
        today = datetime.now()
        _time = time.strftime("%H-%M-%S")
        _date = today.strftime('%Y-%m-%d')
        folder = _date + "|" + _time
        os.mkdir("screenshots/Instagram/{}".format(folder))
        os.mkdir("screenshots/Instagram/{}/Active".format(folder))
        os.mkdir("screenshots/Instagram/{}/Closed".format(folder))
        return(folder)   

    def create_csv(self, folder):
        """Method to create csv file"""

        with open('screenshots/Instagram/{}/report.csv'.format(folder), mode='w') as csv_file:
            fieldnames = ['S.NO','Ref_ID', 'Instagram URL', 'Instagram NAME/ID',
                          'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def append_csv(self, s_no, ref_id, url, name_id, status, folder):
        """ Method to create csv file"""
        with open('screenshots/Instagram/{}/report.csv'.format(folder), 'a') as filename:
            _fields = ['S.NO', 'Ref_ID', 'Instagram URL', 'Instagram NAME/ID',
                       'ACTIVE/CLOSED', 'DATE/TIME', 'REMARKS']
            writer = csv.DictWriter(filename, _fields)
            writer.writerow({'S.NO': s_no, 'Ref_ID':ref_id, 'Instagram URL': url, 'Instagram NAME/ID': name_id,
                             'ACTIVE/CLOSED': status, 'DATE/TIME': datetime.now().time()})        

    def start_process(self):
        folder_name = self.create_folder()
        global file_location
        browser = webdriver.Firefox(executable_path = cfg.PATH)
        browser.set_window_position(0, 0)
        browser.set_window_size(1000, 800)
        wb = xlrd.open_workbook(file_location[0])
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        rows = sheet.nrows
        self.create_csv(folder_name)
        for i in range(rows):
            ref_id = sheet.cell_value(i, 0)
            new_ref = ref_id.replace("/", ".")
            url = sheet.cell_value(i, 1)
            print(">>>" + os.path.basename(url) )
            browser.get(url)
            time.sleep(5.5)
            photo_pattern = "Restricted Photo"
            video_pattern = "Restricted Video"
            page_pattern = "The link you followed may be broken, or the page may have been removed."
            post_not = "This post is not available in your country."
            if re.search("This photo is not available in your country.", browser.page_source) and re.search(photo_pattern, browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            elif re.search("This video is not available in your country.", browser.page_source) and re.search(video_pattern, browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            elif re.search(post_not, browser.page_source) and re.search("Restricted Post", browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            elif re.search("Sorry, this page isn't available.", browser.page_source) and re.search(page_pattern, browser.page_source) is not None:
                status = "blocked"
                print(">>>" + os.path.basename(url) + " is blocked ")
                s_no = i + 1
                self.append_csv(s_no, ref_id, url, os.path.basename(
                    url), status, folder_name)
                browser.save_screenshot(
                    "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Instagram/{}/Closed/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
            else:
                status = "online"
                s_no = i + 1
                self.append_csv(s_no,ref_id ,url , os.path.basename(
                    url), status, folder_name)
                print(">>>" + os.path.basename(url) + " is online ")
                browser.save_screenshot(
                    "screenshots/Instagram/{}/Active/{}.png".format(folder_name, new_ref))
                image_path = "screenshots/Instagram/{}/Active/{}.png".format(folder_name, new_ref)
                WaterMark.water_mark(image_path, url, ref_id)
        browser.quit()
        folder_name_2 = "Instagram"
        CsvToExcel.csv2excel(folder_name, folder_name_2)
        self.message = QMessageBox.information(self, "Done", "Task completed!")

    def tw_menu(self):
        """
        Method to go back to main menu.
        """
        self.mainWindow = Main()
        self.close()


def main():
    APP = QApplication(sys.argv)
    window = Main()
    sys.exit(APP.exec_())


if __name__ == '__main__':
    main()











