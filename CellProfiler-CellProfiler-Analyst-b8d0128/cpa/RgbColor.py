def RgbColor(colorStr):
    if colorStr ==  'Snow':
        triplet = [1.000000, 0.980392, 0.980392];
    if colorStr ==  'Snow 2':
        triplet = [0.933333, 0.913725, 0.913725];
    
    else:
        #print('unknown colorStr ''%s''',colorStr);
        triplet = [0, 0, 0];
    return triplet