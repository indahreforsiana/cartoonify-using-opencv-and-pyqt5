#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 12:01:11 2021

@author: indahreforsiana
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys
import numpy as np
import cv2 
from PIL import Image
from PIL.ImageQt import ImageQt

form_class = uic.loadUiType("cartoon.ui")[0]  # Load the UI

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
    def choose_file_clicked(self):
        options = QFileDialog.Options()
        fileName = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Image Files ()", options=options)
        if fileName:
            print(fileName[0])
            global pic_path
            pic_path = fileName[0]
            self.path_file.setText(fileName[0])
            pixmap=QtGui.QPixmap(fileName[0])
            self.prev_img.setPixmap(pixmap.scaled(291,341,transformMode=QtCore.Qt.SmoothTransformation))
    
    def process_clicked(self):
        def color_quantization(img, k):
        # Transform the image
          data = np.float32(img).reshape((-1, 3))
        
        # Determine criteria
          criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        
        # Implementing K-Means
          ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
          center = np.uint8(center)
          result = center[label.flatten()]
          result = result.reshape(img.shape)
          return result
        img = cv2.imread(pic_path)
        
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        median_filt = cv2.medianBlur(gray_img, 5)
       
        edges = cv2.adaptiveThreshold(median_filt, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9,5)
        color = cv2.bilateralFilter(img, d=9, sigmaColor= 200, sigmaSpace=200)
        #
        result = color_quantization(color,9)
        result = cv2.medianBlur(result, 5)
        cartoon = cv2.bitwise_and(result, result, mask=edges)
        cv2.imwrite("edited.jpg", cartoon)
        edited = Image.open("edited.jpg")
        qgray= ImageQt(edited)
        pixmap=QtGui.QPixmap.fromImage(qgray)
        self.result_img.setPixmap(pixmap.scaled(291,341,transformMode=QtCore.Qt.SmoothTransformation))
        
        
app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
sys.exit(app.exec_())