# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 17:55:17 2017

@author: lenovo
""" 
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

f = plt.figure(figsize=(16,9))
ax = plt.axes(projection=ccrs.Robinson())
ax.stock_img()

plt.show()