from groupDefs import *
from RgbColor import *
def createGrpPairs(dataSelector,pairs,descriptions,mode):
    pairskeys = pairs.keys()[:]
    keyslength = len(pairs.keys())
##    if mode == 'noalternate':
##        WTColors = ('black','light slate gray','light slate gray','dim gray','dim gray','dim gray','dim gray','dim gray','dim gray','dim gray')
##        KOColors = ('red','salmon','salmon','Firebrick','Firebrick','Firebrick','Coral','Coral','Coral','Coral')
##        WTColors = ('black','light slate gray','black','light slate gray','black','light slate gray','black','light slate gray','black','light slate gray','black','light slate gray','black','light slate gray','black','light slate gray')
##        KOColors = ('red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon')
##        Colors = (WTColors,KOColors)
    if mode == 'noalternate':
        WTColors = ('black','gray','gray','gray','gray','gray','gray','gray','gray','gray')
        KOColors = ('red','red','red','firebrick','firebrick','firebrick') #,'Coral','Coral','Coral','Coral')
        WTColors = ('black','gray','black','gray','black','gray','black','gray','black','gray','black','gray','black','gray','black','gray')
        KOColors = ('red','red','red','red','red')


        #,'salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon','red','salmon')
        Colors = (WTColors,KOColors)
    else:
        Colors = (('black','black','black','black','black'),('red','red','red','red','red'))
    for ii in range(len(pairskeys)):
        maxLength = max(1,len(pairs[pairskeys[ii]]))
        if maxLength == len(pairs[pairskeys[ii]]):
            iteratePair = pairskeys[ii]

    nGroups =0
    pkeys =0
    keyIndex = [0] * keyslength
    for numberofkeys in range(keyslength):
        keyIndex[numberofkeys] = 1

    while nGroups < len(descriptions):
        print descriptions[nGroups] , 'group'
        print descriptions, 'note the number'
        for ii in [0,1]:
            if mode == 'alternate':
                new_ii = ii;
            elif mode  == 'noalternate':
                print 'noalternate'
                if nGroups <= (len(descriptions)/2)-1:
                    #print (len(descriptions)/2)
                    new_ii=0
                else:
                    new_ii = 1

            grp = groupDef()
            grp.setDescription(descriptions[nGroups])
            for pkeys in range(keyslength):
                values = pairs[pairskeys[pkeys]]
                #print pkeys; print 'pkeys'; print nGroups
                while keyIndex[pkeys] < len(values):
                    print pkeys, ' pkeys',values, 'values'
                    if 'WT' in values:
#                        print pairskeys[pkeys]
#                        print values[new_ii]
#                        print 'wt pkey'
                        grp.addPair(pairskeys[pkeys],values[new_ii])
                    else:
                        print pairskeys[pkeys]
                        print values[new_ii]
                        print 'ko pkey'
                        grp.addPair(pairskeys[pkeys],values[keyIndex[pkeys]])

                    if pairskeys[pkeys] == iteratePair:
                        grp.setPlotColor((Colors[new_ii][keyIndex[pkeys]]))
                    if mode == 'alternate':
                        if new_ii == 1:
                            keyIndex[pkeys] = keyIndex[pkeys]+1
                    else:
                        keyIndex[pkeys] = keyIndex[pkeys]+1
                    if keyIndex[pkeys] == len(values):
                        keyIndex[pkeys] = 0
                    break
            nGroups = nGroups+1
            dataSelector.addGroupDef(grp);

    return dataSelector, iteratePair
