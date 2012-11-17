import numpy as np
import matplotlib.pyplot as plt
from properties import Properties
from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
import sqltools as sql

p = Properties.getInstance()
p.LoadFile('C:\\Users\\Dalitso\\workspace2\\abhakar\\Properties_README.txt')
db = DBConnect.getInstance()
db.execute('show tables')

class dataSelector:
    def __init__(self, independentVar, dependentVar):
        self.ngroups = 0
        self.groups = []
        self.independentVar = independentVar
        self.dependentVar = dependentVar
    def add(self, group):
        self.ngroups +=1
        self.groups += [group]
    def buildquery(self, table):
        q = 'SELECT ' + self.independentVar + ', '+ self.dependentVar +' FROM ' + table 
        q2= [' WHERE '+ y[1] +' LIKE ' +y[0] for y in group.pairs]
        return q + ''.join(q2)
        
    def Plot (self,n,n2):
        group  =   self.groups[n]
        ind = np.arange(group.npairs)  # the x locations for the groups
        width = 0.35       # the width of the bars
        fig = plt.figure()
        ax = fig.add_subplot(111)
        rects1 = ax.bar(ind, 5, width, color='r')
        rects2 = ax.bar(ind+width,13, width, color='y')
        
        # add some
        ax.set_ylabel(self.independentVar)
        ax.set_title(group.description)
        ax.set_xticks(ind+width)
        ax.set_xticklabels( tuple(self.pairs))
        
        ax.legend( (rects1[0], rects2[0]), (group.pairs[n2], group.pairs[n2+1]))
        
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_ height
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        plt.show()
        
class group:
    def __init__(self,description,plotcolor):
        self.Description= description
        self.PlotColor = plotcolor
        self.pairStr = []
        self.pairs = []
        self.npairs = 0
    def addpair(self, cond1,cond2):
        self.pairStr += [str(cond1) + '=' + str(cond2)]
        self.pairs  += [(cond1,cond2)]
        self.npairs += 1
    
    def __str__(self):
        return self.Description
    
    def __repr__(self):
        return self.Description

    
data = dataSelector('neural count','puncta intensity')
grp = group('wild type','red')
grp.Description
grp.addpair('genotype', 'wto')
data.add(grp)
data.Plot(0,0)

