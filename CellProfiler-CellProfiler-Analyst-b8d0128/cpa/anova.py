"""
file         anova.py
 
author       Ernesto P. Adorio, Ph.D.
             UPDEPP (UP Clarkfield)
             ernesto.adorio@gmail.com
 
reference    Murray Spiegel, "Probability and statistics",
                  Schaum's Outline Series, 1982.
 
version      0.0.1
 
todos
    june.30.2006 two-way with replication.    *done july.01.2006
    june.30.2006 latin squares.
 
 
revisions
    july.01.2006   pValues computed.
    july.01.2006   two-way with replication done.
"""
 
from scipy import stats   # cdf() of F distribution.
 
 
def anova_oneway(groups):
    """
    Perform one-way anova.
    groups - list of treatments (rows) which may have different lengths.
    """
    a     = len(groups)
    total = 0.0
    lens  = [0]   * a
    avgi  = [0.0] * a
 
    n     = 0
    for i in range(a):
        s       = sum(groups[i])
        total   += s
        lens[i] =  len(groups[i])
        avgi[i] =  s / lens[i]
        n       += lens[i]
    xbar = total / n   # grandmean.
 
    vt = 0.0   # total variations.
    vb = 0.0   # between treatments.
    for i in range(a):
        for j in range(lens[i]):
            d =  groups[i][j] - xbar
            vt += d * d
        d  =  avgi[i] - xbar
        vb += lens[i] * d * d
    vw = vt - vb  # within treatments.
 
    dfb = a - 1
    dfw = n - a
    dft = n - 1
 
    sb = vb / dfb
    sw = vw / dfw
    F  = sb / sw
    pValue = 1.0 - stats.f.cdf(F, dfb, dfw)
 
    return [(vb, dfb, sb, F, pValue),
            (vw, dfw, sw),
            (vt, dft)]
 
 
def anova_twoway(groups):
    """
    Perform two-way anova.
      groups - treatments x blocks data matrix.
 
    Treatments are rows, blocks are columns.
    """
    a     = len(groups)       # number of treatments.
    b     = len(groups[0])    # number of blocks.
 
    # Check for uniform number of columns.
    for i in range(a):
        if len(groups[i]) != b:
            return None
 
    total = 0.0
    avgi  = [0.0] * a         # row averages.
    avgj  = [0.0] * b         # column averages.
 
    # Compute grandmean, row and column averages.
    for i in range(a):
        s       = sum(groups[i])
        total   += s
        avgi[i] =  s / b
        for j in range(b):
            avgj[j] += groups[i][j]
    for j in range(b):
        avgj[j] /= a
    xbar = total / (a * b)   # grandmean.
 
    # Total variation.
    vt  = 0.0   # total variations.
    for i in range(a):
        for j in range(b):
            d = groups[i][j] - xbar
            vt += d * d
    dft = a*b - 1
 
    # Variation between rows (treatments).
    vr = 0.0   
    for i in range(a):
        d = avgi[i] - xbar
        vr += b * d * d
    dfr = a-1
 
    # Variation between columns (blocks).
    vc = 0.0   # variation between blocks.
    for j in range(b):
        d = avgj[j] -  xbar
        vc += a * d * d
    dfc = b-1
 
    # Variation due to errors (residual variations).
    ve = vt - vr - vc
    dfe = (a-1) * (b-1)
 
    sr = vr / (a-1)
    sc = vc / (b-1)
    se = ve / (a - 1) / (b-1)
 
    F1      = sr / se
    pValue1 = 1.0 - stats.f.cdf(F1, a-1,(a-1)*(b-1))
 
    F2      = sc / se
    pValue2 = 1.0 - stats.f.cdf(F2, b-1, (a-1) * (b-1))
 
    return [(vr, dfr,         sr, F1, pValue1),
            (vc, dfc,         sc, F2, pValue2),
            (ve, dfe,        se),
            (vt, dft)]
 
def anova_twoway_replicated(groups):
    """
    Perform two-way anova with replication.
      groups   - treatments x blocks data matrix.
 
    Treatments are rows, blocks are columns. Last 
    """
    rows  = len(groups)       # number of rows.
    cols  = len(groups[0])    # number of columns.
    Factor1 = []
    Factor2 = []
 
    # Check for uniform number of columns.
    for i in range(rows):
        if len(groups[i]) != cols:
            return None
 
    total = 0.0
    toti  = [0.0] * rows      # row totals.
    totj  = [0.0] * cols      # column totals.
    tss   = 0.0               # total sum of squares.
 
    # Compute grandmean, row and column totals.
    for i in range(rows):
        label1   = groups[i][0]
        if label1 not in Factor1:
            Factor1.append(label1)
        label2   = groups[i][1]
        if label2 not in Factor2:
            Factor2.append(label2)
 
        s       = sum(groups[i][2:])
        total   += s
        toti[i] += s
        for j in range(2, cols):
            v   = groups[i][j]
            totj[j-2] += v
            tss += v * v
 
    ssmean = total * total / (rows * (cols-2))
    vt  = tss - ssmean
    dft = rows * (cols-2) - 1
 
    redrow = len(Factor1)
    redcol = len(Factor2)
    M = []
    for i in range(redrow):
       M.append([0] * redcol)
 
    for i in range(rows):
        label1 = groups[i][0]
        label2 = groups[i][1]
        ii = Factor1.index(label1)
        jj = Factor2.index(label2)
        M[ii][jj] += sum(groups[i][2:])
 
    # Subtotal variations, row and column sums.
    vs = 0.0
    subRows  = [0] * len(M)
    subCols  = [0] * len(M)
    for i in range(len(M)):
        subRows[i] = sum(M[i])
        for j in range(len(M[i])):
            d  = M[i][j]
            vs += d * d
            subCols[j] += d
    vs  = vs / (cols - 2) - (total*total) / (rows * (cols-2))
    dfs = redrow * redcol - 1
 
 
    # Between row variations.
    vr = 0.0
    for i in range(len(subRows)):
        d = subRows[i]
        vr += d * d
    vr  = vr / ((cols - 2) * redcol) - ssmean
    dfr = redrow - 1
    mr  = vr / dfr
 
    # Between columns variations.
    vc = 0.0
    for j in range(len(subCols)):
        d  =  subCols[j]
        vc += d * d
    vc  = vc / ((cols - 2) * redrow) - ssmean
    dfc = redcol - 1
    mc  = vc / dfc
 
    # Interaction variations.
    vi  = vs  - vr - vc
    dfi = dfs - dfr - dfc
    mi  = vi / dfi
 
    # Error variations.
    ve  = vt - (vr + vc + vi)
    dfe = dft  - dfs
    me  = ve / dfe
 
    Fr      = mr / me
    pValuer = 1.0 - stats.f.cdf(Fr, dfr, dfe)
 
    Fc = mc / me
    pValuec = 1.0 - stats.f.cdf(Fr, dfc, dfe)
 
    Fi = mi / me
    pValuei = 1.0 - stats.f.cdf(Fr, dfi, dfe)
 
    return [(vr,  dfr, mr, Fr, pValuer), 
            (vc,  dfc, mc, Fc, pValuec),
            (vi,  dfi, mi, Fi, pValuei),
            (vs,  dfs),
            (ve,  dfe, me),
            (vt,  dft),
           ]
 
def sumofsquares(dseq):
    """
    Returns sum of squares of a sequence.
    """
    t = 0.0
    for s in dseq:
        t += (s * s)
    return t
 
def anova_graecolatin(latin1, latin2, data):
    """
    Computes totals for analysing graeco-latin square.
    Reference. Statistics 2nd Ed. p.362-363.
    """
 
    # Row, column, latin1, latin2, total sum of squares.
    n           = len(data[0])
    row_sums    = []
    col_sums    = [0] * n
    tss         = 0.0
 
    for row in data:
        tot = 0.0
    j   = 0
    for col in row:
        tss += (col * col)
        tot += col
        col_sums[j] += col
        j += 1
    row_sums.append(tot)
 
    grand_total = sum(row_sums)
    gt = grand_total * grand_total / (n*n)
 
    v1 = [0] * n  # first latin square
    v2 = [0] * n  # second latin square
 
    for i in range(n):
       for j in range(n):
 
           idx1 = int(latin1[i][j]) - 1
           v1[idx1] += data[i][j]
 
           idx2 = int(latin2[i][j]) - 1
           v2[idx2] += data[i][j]
 
    return row_sums, col_sums, v1, v2, tss
 
 
def anova_graecolatin_summary(latin1, latin2, data):
    """
    Returns anova summary data.
    """
    row_sums, col_sums, lat1, lat2, tss = anova_graecolatin(latin1, latin2, data)
 
    n  = len(lat1)
    gt = sum(row_sums)**2 /(n*n)
 
    # Vriations.
    vr  = sumofsquares(row_sums) / n - gt
    vc  = sumofsquares(col_sums) / n - gt
    v1  = sumofsquares(lat1) / n - gt
    v2  = sumofsquares(lat2) / n - gt
    vt  = tss - gt
    ve  = vt - (vr + vc + v1 + v2)
 
    # Degrees of freedom.
    dfr = dfc = df1 = df2 = dfe = n - 1
    dft = (n*n) - 1
 
    # Mean squares.
    mr = vr / dfr
    mc = vc / dfc
    m1 = v1 / df1
    m2 = v2 / df2
    me = ve / dfe
 
    # F-ratios.
    fr = mr / me
    fc = mc / me
    f1 = m1 / me
    f2 = m2 / me
 
    # Probabilities.
    pvaluer = 1.0 - stats.f.cdf(fr, dfr, dfe)
    pvaluec = 1.0 - stats.f.cdf(fc, dfc, dfe)
    pvalue1 = 1.0 - stats.f.cdf(f1, df1, dfe)
    pvalue2 = 1.0 - stats.f.cdf(f2, df2, dfe)   
 
    return [ (vr, dfr, mr, fr, pvaluer),
             (vc, dfc, mc, fc, pvaluec),
         (v1, df1, m1, f1, pvalue1),
         (v2, df2, m2, f2, pvalue2),
         (ve, dfe, me),
         (vt, dft)
           ]             
 
 
 
if __name__ == "__main__":
    print "One-way anova example #1"
    groups = [[48, 49, 50, 49],
              [47, 49, 48, 48],
              [49, 51, 50, 50]]
    output = anova_oneway(groups)
    for out in output:
        print out
    print
 
    print "One-way anova example #2"
    groups = [ [68, 72, 75, 42, 53],
               [72, 52, 63, 55, 48],
               [60, 82, 65, 77, 75],
               [48, 61, 57, 64, 50],
               [64, 65, 70, 68, 53]]
 
    output = anova_oneway(groups)
    for out in output:
        print out
    print
 
    print "One-way anova example with unequal number of observations"
    groups = [[407, 411, 409],
              [404, 406, 408, 405, 402],
              [410, 408, 406, 408]]
 
    output = anova_oneway(groups)
    for out in output:
        print out
    print
 
    print "Two-way anova example"
    groups = [[4.5, 6.4, 7.2, 6.7],
              [8.8, 7.8, 9.6, 7.0],
              [5.9, 6.8, 5.7, 5.2]]
    output = anova_twoway(groups)
    for out in output:
        print out
    print
 
    print "Two-way anova with replication"
    groups = [[1,1,      6,4,5,5,4],
              [1,2,      5,7,4,6,8],
              [2,1,     10,8,7,7,9],
              [2,2,      7,9,12,8,8],
              [3,1,      7,5,6,5,9],
              [3,2,      9,7,5,4,6],
              [4,1,      8,4,6,5,5],
              [4,2,      5,7,9,7,10]]
    output = anova_twoway_replicated(groups)
    for out in output:
        print out
    print
