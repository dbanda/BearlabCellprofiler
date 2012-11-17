import scipy
import numpy as np
import matplotlib.pyplot as plt
from properties import Properties
from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
import sqltools as sql

p = Properties.getInstance()
p.LoadFile('C:\\Users\\Dalitso\\workspace2\\abhakar\\Properties_README.txt')
db = DBConnect.getInstance()

ans = np.arange(db.execute('select imagenumber from Main_10plates_Synap_v2_Per_PunctaObj'))