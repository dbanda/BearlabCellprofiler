# TODO: add hooks to change point size, alpha, numsides etc.
from cpatool import CPATool
import tableviewer
from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
import sqltools as sql
import multiclasssql
from properties import Properties
from wx.combo import OwnerDrawnComboBox as ComboBox
import guiutils as ui
from gating import GatingHelper
import imagetools
import icons
import logging
import numpy as np
from bisect import bisect
import os
import sys
import re
from time import time
import wx
import wx.combo
from matplotlib.widgets import Lasso
from matplotlib.nxutils import points_inside_poly
from matplotlib.colors import colorConverter
from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
p = Properties.getInstance()
p.LoadFile('../Properties_README.txt')
db2 = DBConnect.getInstance()


        

            
            



