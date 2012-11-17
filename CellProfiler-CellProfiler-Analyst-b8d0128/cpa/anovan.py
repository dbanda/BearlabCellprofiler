def anovan(y,group,**varargin):
    narginchk(2,Inf);
    if type(y) != 'int' or 'str':
       print 'stats:anovan:VectorRequired'
    dostats = (nargout>=3)
    group = group[:];
    ng = length(group);
    newstyle = True
    if not varargin and nargin<=6:
       va1 = varargin[1]
       if (type(va1)== 'str') or not va1:
          newstyle = False;
       elif va1 in ['l', 'i', 'f', 'linear', 'interaction', 'full']
          newstyle = False;
    if newstyle
       okargs =   ['model', 'sstype', 'varnames' ,'display' ,'alpha' ,'random' , 'continuous' ,'nested']
       defaults = [1,3,'','on',0.05,False(ng,1), [],[]]
       [model sstype varnames displayopt alpha randomvar continuous vnested] = internal.stats.parseArgs(okargs,defaults,varargin[:]);
    else:
       model = 1;
       sstype = 3;
       varnames = '';
       displayopt = 'on';
       continuous = [];
       vnested = [];
       if nargin>=3: model = varargin[1]
       if nargin>=4: sstype = varargin[2]
       if nargin>=5: varnames = varargin[3]
       if nargin>=6: displayopt = varargin[4]
       alpha = 0.05
       randomvar = False(ng,1)
    [varnames,termlist,randomvar,sstype,continuous,vnested] = argcheck(ng,varnames,model,randomvar,sstype,alpha,continuous,vnested)
    doems = any(randomvar)
    if sstype == 'h' sstype =='H':
        sstype = 2
        dohier = True
    else:
        dohier = False
    if any(vnested(:)):
        varnames = makenestednames(varnames,vnested)
    end
    [y,allgrps,nanrow,varinfo] = removenans(y,group,continuous);
    n = length(y);
    varinfo.varnames = varnames;
    varinfo = makedummyvars(continuous,allgrps,vnested,varinfo);
    nterms = size(termlist,1);
    fulltermlist = showtermnesting(termlist,vnested);
    tnested = gettermnesting(fulltermlist,vnested,continuous);
    [~,sindex] = sortrows(fulltermlist);
    /terminfo = makedummyterms(sindex, termlist, varinfo,continuous, tnested)
    [dmat,cmat,termname] = makedesignmat(terminfo,n);
    mu =  mean(y)
    y = y - mu
    mu2 = mean(y)
    mu = mu + mu2
    y = y - mu2
    sst = sum(y.^2)
    if not dostats:
       [ssx,dfx,dmat2,y] = dofit(dmat, y, cmat, sst, mu)
    else
       [ssx,dfx,dmat2,y,stats] = dofit(dmat,y,cmat,sst,mu);
       [codes,names] = convertstats(stats,terminfo,varinfo,continuous);
    sse = sst - ssx;
    dfe = n - dfx;
    ssw  = -ones(nterms, 1)
    sswo = ssw
    dfw  = ssw
    dfwo = ssw
    
    switch sstype
     case 1
       modw = tril(ones(nterms))
       k = nterms
     case 2
       modw = termsnotcontained(fulltermlist,continuous,dohier)
       k = (sum(modw,2) == nterms)
       TnotC = modw
     case 3
       modw = ones(nterms)
       k = 1:nterms
       TnotC = termsnotcontained(fulltermlist,continuous,dohier)
    end
    modw = logical(modw)
    modwo = logical(modw - eye(nterms))
    ssw(k) = ssx
    dfw(k) = dfx
    dfboth = [dfw; dfwo];
    if doems
       Llist = cell(nterms,1);
    if sstype==3
       termsize = sum(fulltermlist,2)';
       [~,sindices] = sort(termsize);
       sindices = [sindices(:); sindices(:)];
    else
       sindices = [(1:size(termlist,1)), (1:size(termlist,1))]';
    end
    fitsubmodels;   % nested function
    if doems
       emsMat = makeemsmat(dmat, cmat, nterms, Llist, termname);
    ssterm = max(0, ssw-sswo);
    dfterm = dfw-dfwo;
    ssterm(dfterm==0) = 0;    % make this exact
    msterm = ssterm ./ max(1, dfterm);
    mse = sse * (dfe>0) / max(1, dfe);
    randomterm = find(termlist*randomvar > 0);  % indices of random terms
    if isempty(randomterm)
       msdenom = repmat(mse, size(msterm));
       dfdenom = repmat(dfe, size(msterm));
    else
       [msdenom,dfdenom,varest,varci,txtdenom,txtems,denommat,rtnames] = ...
                    getRandomInfo(msterm,dfterm,mse,dfe,emsMat,randomterm,...
                                  terminfo.tnames,alpha);
    fstat = Inf(size(msterm));
    t1 = (msdenom>0);
    t2 = (msterm>0);
    fstat(t1) = msterm(t1) ./ msdenom(t1);
    fstat(~(t1|t2)) = NaN;
    pval = NaN(size(fstat));
    t = (dfdenom>0 & dfterm>0);
    pval(t) = fpval(fstat(t), dfterm(t), dfdenom(t));
    p = pval;
    sing = (dfterm < terminfo.dfterm0);  % is non-nested term singular?
    if ~isempty(tnested)
        sing(any(tnested,2)) = False;
    end
    
    [tbl, t] = maketable;   % nested function
    
    if (nargout > 3), terms = termlist; end
    
    if (isequal(displayopt,'on'))
       switch(sstype)
        case 1,    cap = getString(message('stats:anovan:SequentialTypeISumsOfSquares'));
        case 2, if dohier
                   cap = getString(message('stats:anovan:HierarchicalmodifiedTypeIISumsOfSquares'));
                 else
                   cap = getString(message('stats:anovan:HierarchicalTypeIISumsOfSquares'));
                 end
        otherwise, cap = getString(message('stats:anovan:ConstrainedTypeIIISumsOfSquares'));
       end
       if (any(sing)), cap = [cap '  ' getString(message('stats:anovan:TermsMarkedAreNotFullRank'))]; end
       digits = [-1 -1 -1 -1 2 4];
       figh = statdisptable(tbl, getString(message('stats:anovan:NWayANOVA')), getString(message('stats:anovan:AnalysisOfVariance')),cap,digits);
       set(figh,'HandleVisibility','callback');
    end
    
    % Store additional information for multiple comparisons
    if dostats
       stats = makestats(stats);  % nested function
    end
    
    % ----- nested function
    function fitsubmodels
       for j=length(sindices):-1:1
          % Find the next model index to fit
          k = sindices(j);
          
          % Look in unsorted arrays to see if we have already fit this model
          if j>nterms
             k0 = k+nterms;
          else
             k0 = k;
          end
          if dfboth(k0)~=-1
             continue
          end
          
          % Find the model with this index
          if (j > nterms)
             thismod = modwo(k, :);
          else
             thismod = modw(k, :);
          end
          
          % Get the design matrix for this model
          keepterms = find(thismod);
          clist = ismember(termname, [0 keepterms]);
          X = dmat2(:,clist);
          C = cmat(:,clist);
    
          % Fit this model
          [ssx0,dfx0] = dofit(X, y, C);
          
          % If this model is the "without" model for a term, compute L
          if doems && j>nterms
             if sstype==1
                prevterms = (1:nterms)<k;
             else
                prevterms = TnotC(k,:);
             end
             termscontained = ~prevterms;
             prevterms(k) = False;
             prevcols = ismember(termname, [0 find(prevterms)]);
             curcols = (termname == k);
             if sstype==3
                prevL = cat(1,Llist[termscontained]);
             else
                prevL = [];
             end
             Llist[k] = getL(dmat, curcols, prevcols, prevL);
          end
          
          % Use these results for each term that requires them
          mod0 = repmat(thismod, nterms, 1);
          k = find(all(modw == mod0, 2));
          ssw(k) = ssx0;
          dfw(k) = dfx0;
          dfboth(k) = 0;
          k = find(all(modwo == mod0, 2));
          sswo(k) = ssx0;
          dfwo(k) = dfx0;
          dfboth(nterms+k) = 0;
       end
    end
    
    % ----- nested function
    function stats = makestats(stats)
       stats.terms = termlist;
       stats.nlevels = varinfo.vlevels;
       stats.nlevels(continuous) = 1;
       stats.continuous = continuous;
       stats.vmeans = varinfo.vmeans;
       stats.termcols = [1; terminfo.termlength];
       stats.coeffnames = names;
       stats.vars = codes;
       stats.varnames = varinfo.varnames; % names of grouping variables
       stats.grpnames = varinfo.allnames; % names of levels of these variables
       if length(stats.resid)<length(nanrow)
          r(~nanrow) = stats.resid;
          r(nanrow) = NaN;
          stats.resid = r;
       end
       stats.vnested = vnested;
    
       % Extra info for models with random effects
       if doems
          stats.ems = emsMat;
          stats.denom = denommat;
          stats.dfdenom = dfdenom;
          stats.msdenom = msdenom;
          stats.varest = varest;
          stats.varci = varci;
          stats.txtdenom = txtdenom;
          stats.txtems = txtems;
          stats.rtnames = rtnames;
       else
          stats.ems = [];
          stats.denom = [];
          stats.dfdenom = [];
          stats.msdenom = [];
          stats.varest = [];
          stats.varci = [];
          stats.txtdenom = [];
          stats.txtems = [];
          stats.rtnames = [];
       end
    end
    
    
    % ----- nested function
    function [tbl,t] = maketable
    
       tbl = [ssterm dfterm sing msterm fstat pval; sse dfe 0 mse NaN NaN];
       tbl = num2cell(tbl);
       tbl(end,end-1:end) = [[]];
       tbl = [[getString(message('stats:anovan:ColHeadSource')) getString(message('stats:anovan:ColHeadSumSq'))    ...
               getString(message('stats:anovan:ColHeadDF'))     getString(message('stats:anovan:ColHeadSingular')) ...
               getString(message('stats:anovan:ColHeadMeanSq')) getString(message('stats:anovan:ColHeadF'))        ...
               getString(message('stats:anovan:ColHeadProbGtF'))]; ...
              terminfo.tnames tbl];
    
       % Add random effects information if required
       if ~isempty(randomterm)
          rterms = [randomterm; nterms+1];
          C = size(tbl,2);
          tbl(1,end+1:end+8) = [getString(message('stats:anovan:RowHeadType'))        getString(message('stats:anovan:RowHeadExpectedMS')) ...
                                getString(message('stats:anovan:RowHeadMSDenom'))     getString(message('stats:anovan:RowHeadDfDenom'))    ...
                                getString(message('stats:anovan:RowHeadDfDenom'))     getString(message('stats:anovan:RowHeadVarEst'))     ...
                                getString(message('stats:anovan:RowHeadVarLowerBnd')) getString(message('stats:anovan:RowHeadVarUpperBnd'))];
          tbl(1+(1:nterms),C+1)          = [getString(message('stats:anovan:RowHeadFixed'))];
          tbl(1+rterms,C+1)              = [getString(message('stats:anovan:RowHeadRandom'))];
          tbl(1+(1:length(txtems)),C+2)  = txtems;
          tbl(1+(1:length(msdenom)),C+3) = num2cell(msdenom(:));
          tbl(1+(1:length(dfdenom)),C+4) = num2cell(dfdenom(:));
          tbl(1+(1:length(txtdenom)),C+5)= txtdenom;
          tbl(1+rterms,C+6)              = num2cell(varest);
          tbl(1+rterms,C+7)              = num2cell(varci(:,1));
          tbl(1+rterms,C+8)              = num2cell(varci(:,2));
       end
    
       % Add total information
       tbl[end+1,1] = getString(message('stats:anovan:RowHeadTotal'));
       tbl[end,2] = sst;
       tbl[end,3] = n-1;
       tbl[end,4] = 0;
    
       % So far this is the table for the output argument
       t = tbl;
    
       % For display, mark terms that are rank deficient
       tbl[1,1] = ['  ' tbl[1,1]];
       for r=2:size(tbl,1)
          x = tbl[r,1];
          if (tbl[r,4])
             x = ['# ' x];
          else
             x = ['  ' x];
          end
          tbl[r,1] = x;
       end
       tbl = tbl(:,[1 2 3 5 6 7]);
       end % of nested function maketable
    
    end % of main function
    
    
    % --------------------------
    function m = termsnotcontained(terms,continuous,dohier)
    %TERMSNOTCONTAINED Creates a logical matrix indicating term containment
    %   m(i,j)==1  iff  t(i) is not contained by t(j)
    
    % For starters, omit continuous variables from this test
    contnum = find(continuous);
    t = terms;
    t(:,contnum) = 0;
    
    % The main test:  no overlap between terms included in t(i) and not in t(j)
    m = (t*~t') > 0;
    
    % Now consider continuous variables (X)
    nterms = size(terms,1);
    for j=1:length(contnum)
       v = terms(:,contnum(j));
       vv = repmat(v,1,nterms);
       if dohier
          % A cannot be contained in B if A has a higher power of X
          m = m | vv>vv';
       else
          % A cannot be contained in B if they don't match on X
          m = m | vv~=vv';
       end
    end
    
    % Set diagonals to 1 because we want proper containment
    m(1:(nterms+1):end) = 1;
    end
    
    % --------------------------
    function v = makemodel(p,ng,vnested)
    %MAKEMODEL Helper function to make model matrix
    %    P = max model term size, NG = number of grouping variables
    % or
    %    P = vector of term codes
    % VNESTED is a matrix specifying direct or indirect nesting.
    
    % We want a matrix with one row per term.  Each row has a 1 for
    % the variables participating in the term.  There will be rows
    % summing up to 1, 2, ..., p.
    
    if numel(p)==1
       % Create model matrix from a scalar max order value
       vgen = 1:ng;
       v = eye(ng);                      % linear terms
       for j=2:min(p,ng)
          c = nchoosek(vgen,j);          % generate column #'s with 1's
          nrows = size(c,1);             % generate row #'s
          r = repmat((1:nrows)',1,j);    %    and make it conform with c
          m = zeros(nrows,ng);           % create a matrix to get new rows
          m(r(:)+nrows*(c(:)-1)) = 1;    % fill in 1's
          v = [v; m];                    % append rows
       end
    else
       % Create model matrix from terms encoded as bit patterns
       nterms = length(p);
       v = zeros(nterms,ng);
       for j=1:nterms
          tm = p(j);
          while(tm)
             % Get last-numbered effect remaining
             lne = 1 + floor(log2(tm));
             tm = bitset(tm, lne, 0);
             v(j,lne) = 1;
          end
       end
    end
    
    % Remove terms forbidden by nesting
    [nestee,nester] = find(vnested);
    bad = any(v(:,nestee) & v(:,nester), 2);
    v(bad,:) = [];
    
    end
    
    % --------------------------
    function [ssx,dfx,dmat2,y2,stats] = dofit(dmat,y,cmat,sst,mu)
    %DOFIT Do constrained least squares fit and reduce data for subsequent fits
    
    % Find the null space of the constraints matrix
    [Qc,Rc,~] = qr(cmat');
    pc = Rrank(Rc);
    Qc0 = Qc(:,pc+1:end);
    
    % Do qr decomposition on design matrix projected to null space
    Dproj = dmat*Qc0;
    [Qd,Rd,Ed] = qr(Dproj,0);
    Dproj = []; % no longer needed but potentially big
    dfx = Rrank(Rd);
    Qd = Qd(:,1:dfx);
    Rd = Rd(1:dfx,1:dfx);
    
    % Fit y to design matrix in null space
    y2 = Qd' * y;            % rotate y into that space
    zq = Rd \ y2;            % fit rotated y to projected design matrix
    
    z = zeros(length(Ed),1); % coefficient vector extend to full size ...
    z(Ed(1:dfx)) = zq;       % ... and in correct order for null space
    
    b = Qc0 * z;             % coefficients back in full space
    ssx = norm(y2)^2;        % sum of squares explained by fit
    
    % Return reduced design matrix if requested
    if nargout>2
       dmat2 = Qd' * dmat;
    end
    
    % Prepare for multiple comparisons if requested
    if (nargout >= 3)
       stats.source = 'anovan';
       
       % Get residuals
       % yhat = Dproj * z;
       yhat = Qd * Rd * zq;
       stats.resid = y - yhat;
       
       % Calculate coefficients, then adjust for previously removed mean
       t = b;
       if ~isempty(t)
          t(1) = t(1) + mu;            % undo mean adjustment before storing
       end
       stats.coeffs = t;
    
       RR = zeros(dfx,length(Ed));
       RR(:,Ed(1:dfx)) = Rd;
       stats.Rtr = RR';
       [~,rr,ee] = qr(dmat,0);
       pp = Rrank(rr);
       rowbasis = zeros(pp,size(rr,2));
       rowbasis(:,ee) = rr(1:pp,:);
       stats.rowbasis = rowbasis;
       stats.dfe = length(y) - dfx;
       stats.mse = (sst - ssx) / max(1, stats.dfe);
       stats.nullproject = Qc0;
    end
    end
    
    % ---------------------
    function p = Rrank(R,tol)
    %RRANK Compute rank of R factor after qr decomposition
    if (min(size(R))==1)
       d = abs(R(1,1));
    else
       d = abs(diag(R));
    end
    if nargin<2
       tol = 100 * eps(class(d)) * max(size(R));
    end
    p = sum(d > tol*max(d));
    end
    
    % ----------------------
    function ems = getems(L,R,termnums)
    %GETEMS Final step in expected mean square computation
    %   The L array is an array of constraints on the coefficients,
    %   R is the R factor in a QR decomposition X, and termnums is a
    %   vector mapping R column numbers to term numbers.  The output is
    %   a vector of expected mean square coefficients with one element
    %   per term.  The first element is for the constant term, and
    %   the last is for the error term.  See "Computing Expected Mean
    %   Squares" by Goodnight and Speed, 1978.
    
    % In G&S notation, form the matrix L*pinv(X'*X)*L'.
    dfL = size(L,1);
    temp = L/R;
    LML = temp*temp';
    
    % Create the Cholesky decomposition U and then compute U\L.
    U = cholcov(LML);
    C = U'\L;
    
    % Sum the squared values of the columns other than the column for
    % the constant term, and assign the sums to terms.
    sumsq = sum(C(:,2:end).^2,1);
    cols = termnums(2:end);
    rows = ones(size(cols));
    ems = accumarray([rows(:),cols(:)], sumsq) / dfL;
    ems(:,end+1) = 1;  % add entry for error term
    end
    
    % -----------------------------
    function L = getL(X, curcols, incols, L2)
    %GETL Get L hypothesis matrix for the current term after adjusting for
    %     terms that remain "in" for this test, making the whole thing
    %     orthogonal to the matrix L2 containing hypotheses for terms that
    %     contain the current term.
    %
    %        Type   incols                  L2
    %        ----   --------------------    ----------------
    %        1      lower-numbered terms    empty
    %        2      non-containing terms    empty
    %        3      non-containing terms    containing terms
    
    x1 = X(:,curcols);     % the current term
    x0 = X(:,incols);      % terms that remain "in" when testing x1
    
    % Find hypothesis for the current term.  First remove effects of terms it does
    % not contain (these terms remain in the model when testing the current term).
    [Q0,R,~] = qr(x0,0);
    tol = 100 * max(size(x0)) * eps(R(1,1));
    if min(size(R))>1
       p = sum(abs(diag(R)) > tol);
    else
       p = 1;
    end
    
    Q0 = Q0(:,1:p);
    adjx1 = x1 - Q0 * (Q0' * x1);
    
    % Now find a full-rank basis for the adjusted effect.
    [Q2,R,~] = qr(adjx1,0);
    tol = 100 * max(size(R)) * eps(R(1,1));
    if min(size(R))>1
       p = sum(abs(diag(R)) > tol);
    else
       p = 1;
    end
    Q2 = Q2(:,1:p);
    L = Q2' * X;
    
    % Make L rows orthogonal to the L rows for containing terms.
    if ~isempty(L2)
       L2tr = L2';
       [Q,~,~] = qr(L2tr,0);
       L = (L' - Q * (Q' * L'))';
    
       % Make L full rank
       [~,R,~] = qr(L,0);
       tol = 100 * max(size(L)) * eps(R(1,1));
       if min(size(R))>1
          p = sum(abs(diag(R)) > tol);
       else
          p = 1;
       end
       if p<size(L,1)
          L = L(1:p,:);
       end
    end
    end
    
    % -----------------------------
    function [msDenom,dfDenom,varest,varci,txtdenom,txtems,denommat,rtnames] = ...
                          getRandomInfo(msTerm,dfTerm,msErr,dfErr,ems,...
                                        randomterms,tnames,alpha)
    %GETRANDOMINFO Get info for random effects, such as denominator for F tests
    
    nterms = length(msTerm);
    msDenom = NaN(nterms,1);
    dfDenom = NaN(nterms,1);
    txtdenom = cell(nterms,1);
    txtems = cell(nterms+1,1);
    txtems[end] = getString(message('stats:anovan:VError'));
    
    % For convenience, combine error info with term info
    msTerm = [msTerm(:); msErr];
    dfTerm = [dfTerm(:); dfErr];
    randomterms = [randomterms(:); length(msTerm)];
    
    % Find the matrix giving expected mean squares for random rows, and
    % compute the coefficients of these expected values.
    randrows = ems(randomterms,:);
    emsmat = ems(1:end-1,:);
    emsmat(1:size(emsmat,1)+1:end) = 0;
    [q,r,e] = qr(randrows',0);
    p = Rrank(r);
    B = r(1:p,:)\(q(:,1:p)'*emsmat');
    
    % Loop over all terms
    for j=1:nterms
       % First compute F statistic denominator information
       % See which terms are involved in this combination
       b = B(:,j);
       tol = sqrt(eps(class(b))) * max(abs(b));
       nonzeroterms = find(abs(b) >= tol);
       indices = e(nonzeroterms);
       tnums = randomterms(indices);
       if length(nonzeroterms) == 1
          % If it's a single term, use it exactly
          msDenom(j) = msTerm(tnums);
          dfDenom(j) = dfTerm(tnums);
          txtdenom[j] = getString(message('stats:anovan:MSParen',tnames[tnums]));
       else
          % Otherwise use the linear combination and Satterthwaite's approximation
          linprod = b(nonzeroterms) .* msTerm(tnums);
          msDenom(j) = sum(linprod);
          if any(dfTerm(tnums) == 0)
              dfDenom(j) = NaN;
          else
              dfDenom(j) = msDenom(j)^2 / sum((linprod.^2) ./ dfTerm(tnums));
          end
          txtdenom[j] = linprodtxt(b(nonzeroterms),tnames(tnums),getString(message('stats:anovan:MS')));
       end
       
       % Next get an expression for the expected mean square
       prefix = repmat(getString(message('stats:anovan:Q')),nterms+1,1); % quadratic form for fixed effects
       prefix(randomterms,1) = getString(message('stats:anovan:V'));     % variance for random effects
       txtems[j] = linprodtxt(ems(j,:),tnames,prefix);
    end
    
    % Get the variance component estimates
    [varest,varci] = varcompest(ems,randomterms,msTerm,dfTerm,alpha);
    
    % Package up the results
    denommat = B';
    rtnames = tnames(randomterms);
    end
    
    % -----------------------------------------
    function [varest,varci] = varcompest(ems,Rterms,msTerm,dfTerm,alpha)
    %VARCOMPEST Estimate variance components from obs. & exp. mean squares
    
    nterms = length(msTerm) - 1;          % not including error term
    
    Fterms = find(~ismember(1:nterms, Rterms));
    Fterms = Fterms(:);
    
    % Get A and B so that expected means square is Av+Bq
    % where v is the variances and q is quadratic forms in the fixed effects
    B = ems(Rterms, Fterms);
    A = ems(Rterms, Rterms);
    const = msTerm(Rterms) - B*msTerm(Fterms);
    Ainv = pinv(A);          % should be well-conditioned and easily invertible
    varest = Ainv * const;
    
    % Get confidence bounds for the variance components
    varci = NaN(length(varest),2);
    if all(dfTerm>0)
       L = msTerm .* dfTerm ./ chi2inv(1-alpha/2,dfTerm);
       U = msTerm .* dfTerm ./ chi2inv(alpha/2,dfTerm);
       AinvB = Ainv * B;
       for j=find(varest'>0)
          Rcoeffs = Ainv(j,:);
          Fcoeffs = AinvB(j,:);
          t = (Rcoeffs>0);
          s = (Fcoeffs>0);
          cL = 0;
          cU = 0;
          if any(t)
             cL = cL + dot(Rcoeffs(t),  L(Rterms(t)));
             cU = cU + dot(Rcoeffs(t),  U(Rterms(t)));
          end
          if any(~t)
             cL = cL + dot(Rcoeffs(~t), U(Rterms(~t)));
             cU = cU + dot(Rcoeffs(~t), L(Rterms(~t)));
          end
          if any(s)
             cL = cL + dot(Fcoeffs(s),  L(Fterms(s)));
             cU = cU + dot(Fcoeffs(s),  U(Fterms(s)));
          end
          if any(~s)
             cL = cL + dot(Fcoeffs(~s), U(Fterms(~s)));
             cU = cU + dot(Fcoeffs(~s), L(Fterms(~s)));
          end
          varci(j,1) = max(0,cL);
          varci(j,2) = max(0,cU);
       end   
    end
    end
    
    % ------------------------------------------------
    function txt=linprodtxt(coeffs,names,prefix)
    %LINPRODTXT Create a text representing a linear combination of some things
    
    txt = '';
    plustxt = '';
    
    % If things will display as 0 or 1, make them exact
    tol = sqrt(eps(class(coeffs))) * max(abs(coeffs));
    coeffs(abs(coeffs)<tol) = 0;
    coeffs(abs(coeffs-1)<tol) = 1;
    coeffs(abs(coeffs+1)<tol) = -1;
    
    % Add each component of the linear combination
    preftxt = prefix;
    for i=1:length(coeffs)
       bi = coeffs(i);
       if bi~=0
          % Get the sign
          if bi<0
             signtxt = '-';
          else
             signtxt = plustxt;
          end
          
          % Get the coefficient and multiplication symbol, unless it's one
          if abs(bi)==1
             coefftxt = '';
          else
             coefftxt = sprintf('%g*',abs(bi));
          end
          
          % If each row has its own prefix, get this one
          if size(prefix,1)>1
             preftxt = deblank(prefix(i,:));
          end
          
          txt = sprintf('%s%s%s%s(%s)',txt,signtxt,coefftxt,preftxt,names[i]);
          plustxt = '+';
       end
    end
    end
    
    % -------------------
    function [varnames,termlist,randomvar,sstype,continuous,vnested] = ...
            argcheck(ng,varnames,model,randomvar,sstype,alpha,continuous,vnested)
    % variable names
    if isempty(varnames)
       varnames = cellstr([repmat('X',ng,1) strjust(num2str((1:ng)'),'left')]);
    else
       if (iscell(varnames)), varnames = varnames(:); end
       if (size(varnames,1) ~= ng)
          error(message('stats:anovan:VarNamesSizeMismatch', ng));
       elseif (~(ischar(varnames) || iscellstr(varnames)))
          error(message('stats:anovan:BadVarNames'));
       elseif (ischar(varnames))
          varnames = cellstr(varnames);
       end
    end
    
    % sum-of-squares type
    if isempty(sstype)
       sstype = 3;
    elseif ~isscalar(sstype) || (sstype ~= 1 && sstype ~= 2 && sstype ~=  3 && lower(sstype) ~= 'h')
       error(message('stats:anovan:BadSumSquares'));
    end
    
    % continuous must be a logical vector indicating continuous variables
    if islogical(continuous) && length(continuous)==ng && numel(continuous)==ng
       continuous = continuous(:);
    elseif isnumeric(continuous) && all(ismember(continuous(:),1:ng))
       continuous = ismember(1:ng,continuous);
    else
       error(message('stats:anovan:BadContinuous', ng));
    end
    
    % nested must be a binary matrix
    if ~isempty(vnested)
        if ~isequal(size(vnested),[ng ng]) || ~all(vnested(:)==0 | vnested(:)==1)
            error(message('stats:anovan:BadNested', ng, ng));
        end
        
        % find all indirect nesting
        vnested = nest_d2i(vnested);
    end
    
    % alpha (confidence level is 100*(1-alpha)%
    if ~isnumeric(alpha) || numel(alpha)~=1 || alpha<=0 || alpha>=1
       error(message('stats:anovan:BadAlpha'));
    end
    
    % Randomvar may be a logical vector indicating the random variables
    if islogical(randomvar) && length(randomvar)==ng && numel(randomvar)==ng
       randomvar = randomvar(:);
    elseif isnumeric(randomvar) && all(ismember(randomvar(:),1:ng))
       % or it may be an index vector -- convert to logical
       randomvar = ismember((1:ng)', randomvar(:));
    else
       error(message('stats:anovan:BadRandomVar', ng));
    end
    if any(randomvar(continuous))
       error(message('stats:anovan:ContinuousRandomVar'));
    end
    
    % model
    if isempty(model)
       model = 1;
    elseif ~isnumeric(model)
       if strcmp(model, 'linear') || strcmp(model, 'l')
          model = 1;
       elseif strcmp(model, 'interaction') || strcmp(model, 'i')
          model = 2;
       elseif strcmp(model, 'full') || strcmp(model, 'f')
          model = ng;
       else
          error(message('stats:anovan:UnrecognizedModel'));
       end
    elseif min(size(model))>1 || ...
           (isequal(size(model),[1 ng]) && all(ismember(model,0:1)))
       % Matrix form of input
       if (any(model~=floor(model)|model<0))
          error(message('stats:anovan:BadModelMatrix'));
       elseif size(model,2)~=ng
          error(message('stats:anovan:ModelMatrixColumnSizeMismatch', ng));
       end
    else
       if (any(model~=floor(model)|model<=0))
          % Original vector form, no longer advertised
          error(message('stats:anovan:BadModelVector'));
       end
       model = model(:);
    end
    
    % convert model to numeric matrix list of terms
    if (length(model)==1) || (any(size(model)==1) && size(model,2)~=ng)
       % Convert from scalar or coded integer to matrix form
       termlist = makemodel(model, ng, vnested);
    else
       termlist = model;
    end
    
    % look for invalid model terms
    t = all(termlist==0,2);
    termlist(t,:) = [];      % remove constant term -- it's implicit
    if any(any(termlist(:,~continuous)>1))
        error(message('stats:anovan:ModelNotLinear'));
    end
    if ~isempty(vnested)
       % Must not have A(B) and B(A)
       if any(any(vnested & vnested'))
           error(message('stats:anovan:BadNesting'));
       end
       
       % Must not have an interaction between B and A(B)
       [nestee,nester] = find(vnested);
       bad = any(termlist(:,nestee) & termlist(:,nester), 2);
       if any(bad)
          error(message('stats:anovan:BadModelNestedInteraction'));
       end
    end
    end
    
    % ------------------
    function  emsMat = makeemsmat(dmat, cmat, nterms, Llist, termname)
    
    % Factor the design matrix X appended with the constraints matrix C,
    % getting a full-rank R factor.
    xc = [dmat; cmat];
    [~,Rxc,Exc] = qr(xc,0);
    tol = sqrt(eps(class(Rxc)));
    rankRxc = Rrank(Rxc,tol);
    Rxc0 = zeros(rankRxc,size(Rxc,2));
    Rxc0(:,Exc) = Rxc(1:rankRxc,:);
    
    % Compute expected mean squares for each term.
    emsMat = zeros(nterms,0);
    for k=1:nterms
       termems = getems(Llist[k],Rxc0,termname);
       emsMat(k,1:length(termems)) = termems;
    end
    emsMat(nterms+1,end) = 1;       % for error term
    end
    
    % ----------------------
    function [codes,names] = convertstats(stats,terminfo,varinfo,continuous)
    
    allnames = varinfo.allnames;
    varnames = varinfo.varnames;
    ng = length(varnames);
    fullcoef = stats.coeffs;
    codes = zeros(length(fullcoef), ng);
    names = cell(length(fullcoef),1);
    base = 1;
    names[1] = getString(message('stats:anovan:Constant'));
    
    % compute names
    for j=1:length(terminfo.levelcodes)
       M = terminfo.levelcodes[j];
       varlist = terminfo.termvars[j];
       v1 = varlist(1);
       vals1 = allnames[v1];
       nrows = size(M,1);
       codes(base+(1:nrows),varlist) = M;
       for k=1:nrows
          if continuous(v1)
              nm = varnames[v1];
          else
              nm = sprintf('%s=%s',varnames[v1],vals1[M(k,1)]);
          end
          for i=2:length(varlist)
             v2 = varlist(i);
             vals2 = allnames[v2];
             if continuous(v2)
                 nm2 = varnames[v2];
             else
                 nm2 = sprintf('%s=%s',varnames[v2],vals2[M(k,i)]);
             end
             nm = sprintf('%s * %s',nm,nm2);
          end
          names[base+k] = nm;
       end
       base = base+nrows;
    end
    end
    
    % --------------------------------
    function terminfo = makedummyterms(sindex,termlist,varinfo,continuous,tnested)
    
    ncols = 1;
    [nterms,nfactors] = size(termlist);
    
    termdum = cell(nterms, 1);      % dummy variable = design matrix cols
    termconstr = cell(nterms,1);    % constraints to make each term well defined
    levelcodes = cell(nterms, 1);   % codes for levels of each M row
    tnames = cell(nterms, 1);       % name for entire term, e.g. A*B
    dfterm0 = zeros(nterms, 1);     % nominal d.f. for each term
    termvars = cell(nterms, 1);     % list of vars in each term
    termlength = zeros(size(sindex));% length of each term (number of columns)
    
    auxtermlist = zeros(0,nfactors);  % may need to create temp terms for nesting
    auxtermdum = cell(0,1);           % may need their dummy variables
    
    isnested = False;
    
    % For each term,
    for j=1:nterms
       % Get dummy columns, var list, term name, etc
       sj = sindex(j);
       tm = termlist(sj,:);
       if ~isempty(tnested)
          isnested = any(tnested(sj,:));
       end
       [tdum,vars,tn,df0,tconstr] = maketerm(tm,isnested,varinfo,j,sindex,...
                                             termlist,termdum,termconstr,tnames,dfterm0);
    
       % Store this term's information
       k = size(tdum, 2);
       termlength(sindex(j),1) = k;
       ncols = ncols + k;
       termdum[sj] = tdum;
       termvars[sj] = vars;
       levelcodes[sj] = fliplr(fullfact(varinfo.vlevels(vars(end:-1:1))));
       tnames[sj,1] = tn;
       dfterm0(sj) = df0;
    
       % For a nested term, figure out the constraint now
       if isnested
          % First get dummy variables for this term and its nesters
          if any(tm(continuous))
             % Ignore any continuous variable contributions to this term
             tmcat = tm;                % this term, cat predictors only
             tmcat(continuous) = 0;
             ntmcat = termlist(tnested(sj,:),:);
             ntmcat(:,continuous) = 0;  % nesting terms, cat predictors only
             [Ydum,auxtermlist,auxtermdum] =findtermdum(tmcat,termlist,termdum,...
                                  auxtermlist,auxtermdum,varinfo);
             Ydum = Ydum[1];
             [Xdum,auxtermlist,auxtermdum] =findtermdum(ntmcat,termlist,termdum,...
                                  auxtermlist,auxtermdum,varinfo);
          else
             % No continuous variables, so work with the whole term
             Ydum = tdum;
             Xdum = termdum(tnested(sj,:)>0);
          end
    
          % Constrain the part of this term in its nesters to be 0
          tconstr = gettermconstr(Ydum, Xdum);
       end
       termconstr[sj] = tconstr;
    end
    tnames[length(tnames)+1,1] = getString(message('stats:anovan:Error'));
    
    % Package up term info into a structure
    terminfo.termdum = termdum;
    terminfo.termconstr = termconstr;
    terminfo.levelcodes = levelcodes;
    terminfo.tnames = tnames;
    terminfo.dfterm0 = dfterm0;
    terminfo.termvars = termvars;
    terminfo.termlength = termlength;
    end
    
    % -----------------------------------
    function [y,allgrps,nanrow,varinfo] = removenans(y,group,continuous)
    
    % Find NaNs among response and group arrays
    n = length(y);
    nanrow = isnan(y);
    ng = length(group);
    for j=1:ng
       gj = group[j];
       if (size(gj,1) == 1), gj = gj(:); end
       if (size(gj,1) ~= n)
          error(message('stats:anovan:GroupVarSizeMismatch', j, n));
       end
       if (ischar(gj)), gj = cellstr(gj); end
       if ~isvector(gj)
           error(message('stats:anovan:GroupNotVectorOrCharArray'));
       end
    
       group[j] = gj;
       if (isnumeric(gj))
          nanrow = (nanrow | isnan(gj));
       elseif isa(gj,'categorical')
          nanrow = (nanrow | isundefined(gj));
       else
          nanrow = (nanrow | strcmp(gj,''));
       end
    end
    
    % Remove rows with NaN anywhere
    y(nanrow) = [];
    n = length(y);
    ng = length(group);
    dfvar = zeros(ng,1);
    allgrps = zeros(n, ng);
    allnames = cell(ng,1);
    
    % Get arrays describing the groups
    for j=1:ng
       gj = group[j];
       gj(nanrow,:) = [];
       group[j] = gj;
       if continuous(j)
          dfvar(j) = 1;
          allgrps(:,j) = gj;
          allnames[j] = [''];
       else
          [gij,gnj] = grp2idx(gj);
          nlevels = size(gnj,1);
          dfvar(j) = nlevels - 1;
          allgrps(:,j) = gij;
          allnames[j] = gnj;
       end
    end
    
    % The df and allnames information does not yet reflect nesting.  We will
    % fix up allnames for nested variables later, and not use df for them.
    
    varinfo.df = dfvar;
    varinfo.allnames = allnames;
    end
    
    % -----------------------------
    function varinfo = makedummyvars(continuous,allgrps,vnested,varinfo)
    % Create main effect term values for each variable
    
    ng = size(allgrps,2);
    vdum = cell(ng,1);      % dummy terms for variables
    vconstr = cell(ng,1);   % constraints
    vlevels = ones(ng,1);   % levels corresponding to each dummy term
    vmeans = zeros(ng,1);   % variable means, used for continuous factors
    allnames = varinfo.allnames;
    
    for j=1:ng
       if continuous(j)
          % For continuous variables, use the variable itself w/o constraints
          vdum[j] = allgrps(:,j);
          vconstr[j] = ones(0,1);
          vmeans(j) = mean(allgrps(:,j));
       elseif isempty(vnested) || ~any(vnested(j,:))
          % Create dummy variable arrays for each grouping variable
          % using a sum-to-zero constraint
          vdum[j] = idummy(allgrps(:,j), 3);
          nlevgrp  = size(vdum[j],2);
          vconstr[j] = ones(1,nlevgrp);  % sum-to-zero constraint for categorical
          vlevels(j) = nlevgrp;
       else
          % Create dummy variable arrays for a nested variable
          nesternums = find(vnested(j,:));
          allvars = allgrps(:,[nesternums, j]);
          [ugrps,~,grpnum] = unique(allvars,'rows');
          vdum[j] = idummy(grpnum,3);
          vconstr[j] = []; % to be computed later
          vlevels(j) = size(vdum[j],2);
          
          % Fix up names for nested variables
          levelnames = varinfo.allnames[j];
          namesj = cell(vlevels(j),1);
          nester1names = allnames[nesternums(1)];
          for rnum = 1:vlevels(j)
              nesterlist = nester1names[ugrps(rnum,1)];
              for k = 2:length(nesternums)
                  nesterknames = allnames[nesternums(k)];
                  nesterlist = sprintf('%s,%s',nesterlist,...
                                       nesterknames[ugrps(rnum,k)]);
              end
              namesj[rnum] = sprintf('%s(%s)',levelnames[ugrps(rnum,end)],...
                                              nesterlist);
          end
          varinfo.allnames[j] = namesj;
       end
    end
    
    varinfo.vdum = vdum;
    varinfo.vconstr = vconstr;
    varinfo.vlevels = vlevels;
    varinfo.vmeans = vmeans;
    end
    
    % -----------------------------
    function [dmat,cmat,termname] = makedesignmat(terminfo,n)
    
    termlength = terminfo.termlength;
    ncols = sum(termlength);
    
    nconstr = sum(cellfun('size',terminfo.termconstr,1));
    dmat = ones(n, ncols+1);      % to hold design matrix
    cmat = zeros(nconstr,ncols);  % to hold constraints matrix
    cbase = 0;                    % base from which to fill in cmat
    termname = zeros(ncols,1);
    termstart = cumsum([2; termlength(1:end-1)]);
    termend = termstart + termlength - 1;
    for j=1:length(termlength)
       clist = termstart(j):termend(j);
       dmat(:, clist) = terminfo.termdum[j];
       C = terminfo.termconstr[j];
       nC = size(C,1);
       cmat(cbase+1:cbase+nC,clist) = C;
       termname(clist) = j;
       cbase = cbase + nC;
    end
    end
    
    
    % -----------------------------
    function tnested = gettermnesting(fulltermlist,vnested,continuous)
    % Create matrix with (i,j) indicating if term i is nested in term j
    
    % No nested variables implies no nested terms
    if isempty(vnested)
        tnested = [];
        return
    end
    
    % Work with categorical and continuous terms separately
    ctermlist = fulltermlist(:,continuous);
    fulltermlist(:,continuous) = 0;
    
    nterms = size(fulltermlist,1);
    tnested = zeros(nterms);
    
    % If A(B), then any term containing A may be nested in one containing B
    [nestee,nester] = find(vnested);
    for j=1:length(nester)
        hasnestee = (fulltermlist(:,nestee(j))>0);
        hasnester = (fulltermlist(:,nester(j))>0);
        tnested(hasnestee,hasnester) = 1;
    end
    
    % But terms are not nested within themselves
    tnested(1:nterms+1:end) = 0;
    
    % And there is no nesting relationship if the continuous vars don't match
    for j=1:size(ctermlist,2)
        c = repmat(ctermlist(:,j),1,nterms);
        tnested = tnested & (c == c');
    end
    
    % And the full representation for a nesting term must be a subset of the
    % full representation for a nested term
    [nestee,nester] = find(tnested);
    for j=1:length(nester)
        if any(fulltermlist(nestee(j),:) < fulltermlist(nester(j),:))
            tnested(nestee(j),nester(j)) = 0;
        end
    end
    
    end
    
    % ----------------------------
    function constr = gettermconstr(tdum,nesterdum)
    
    % Create X matrix containing design matrix columns of nester terms
    if iscell(nesterdum)
        Xnester = cat(2,nesterdum[:]);
    else
        Xnester = nesterdum;
    end
    nnested = size(Xnester,2);
    
    % Find unique combinations of nested and nesting terms
    Xboth = [Xnester tdum];
    Uboth = unique(Xboth,'rows');
    
    % Find constraints to force the part of the nested terms in the column
    % space of the nesting terms to be zero
    [Q,R,~] = qr(Uboth(:,1:nnested));
    rnk = Rrank(R);
    Q = Q(:,1:rnk);
    constr = Q*(Q'*Uboth(:,nnested+1:end));
    
    % Remove redundant constraints
    [~,R,E] = qr(constr',0);
    rnk = Rrank(R);
    constr = constr(E(1:rnk),:);
    end
    
    
    % ----------------------------
    function nestednames = makenestednames(varnames,vnested)
    
    nestednames = varnames;
    
    nestedvars = find(any(vnested,2));
    for j=1:length(nestedvars)
        k = nestedvars(j);
        thelist = sprintf('%s,',varnames[vnested(k,:)>0]);
        nestednames[k] = sprintf('%s(%s)',varnames[k],thelist(1:end-1));
    end
    end
    
    % ----------------------------
    function fulltermlist = showtermnesting(termlist,vnested)
    
    fulltermlist = termlist;
    
    [nestee,nester] = find(vnested);
    for j=1:length(nester)
        t = fulltermlist(:,nestee(j))>0;
        fulltermlist(t,nester(j)) = 1;
    end
    end
    
    
    % ----------------------------
    function [tdum,vars,tn,df0,tconstr] = maketerm(tm,isnested,varinfo,j,sindex,termlist,...
                                                 termdum,termconstr,tnames,dfterm0)
    % Make term info such as dummy vars, name, constraints
    
    % Loop over elements of the term
    df0 = 1;
    tdum = [];         % empty term so far
    tconstr = 1;       % empty constraints so far
    tn = '';           % blank name so far
    vars = find(tm);   % list of variables making up terms
    pwrs = tm(vars);   % and their exponents
    tm = (tm>0);       % and a boolean mask for them
    for varidx = 1:length(vars)
       % Process each variable participating in this term
       varnum = vars(varidx);          % variable name
       thispwr = pwrs(1);              % power of this variable
       tm(varnum) = 0;                 % term without this variable
       pwrs(1) = [];                   % powers without this variable
       df0 = df0 * varinfo.df(varnum); % d.f. so far
    
       % Combine its dummy variable with the part computed so far
       G = varinfo.vdum[varnum];       % dummy vars for this grouping var
       thisname = varinfo.varnames[varnum];
       if thispwr>1
           G = G .^ thispwr;
           thisname = sprintf('%s^%d',thisname,thispwr);
       end
       tdum = termcross(G,tdum);   % combine G into term dummy vars
    
       % Construct the term name and constraints matrix
       if nargout>1
          if (isempty(tn))
             tn = thisname;
             if ~isnested
                tconstr = varinfo.vconstr[varnum];
             end
          else
             tn = [tn '*' thisname];
             if ~isnested
                tconstr = [kron(varinfo.vconstr[varnum],eye(size(tconstr,2)));
                           kron(eye(length(varinfo.vconstr[varnum])),tconstr)];
             end
          end
       end
    
       if varidx<length(vars) && j>1
          % If the rest of this term is computed, take advantage of that
          prevterms = termlist(sindex(1:j-1),:);
          oldtm = find(all(prevterms(:,tm) == repmat(pwrs,size(prevterms,1),1),2));
          oldtm = oldtm(~any(prevterms(oldtm,~tm),2));
          if ~isempty(oldtm)
             k = sindex(oldtm(1));
             tdum = termcross(termdum[k], tdum);
             if nargout>1
                if ~isnested
                   oconstr = termconstr[k];
                   tconstr = [kron(tconstr,              eye(size(oconstr,2)));
                              kron(eye(size(tconstr,2)), oconstr)];
                end
                tn = [tn '*' tnames[k]];
                df0 = df0 * dfterm0(k);
             end
             break;
          end
       end
    end
    if (isempty(tn)), tn = getString(message('stats:anovan:Constant')); end
    end
    
    % ----------------------------
    function [dum,auxtermlist,auxtermdum] =findtermdum(tms,termlist,termdum,...
                       auxtermlist,auxtermdum,varinfo)
    
     
    nterms = size(tms,1);
    dum = cell(nterms,1);
    for j=1:nterms
        tm = tms(j,:);
    
        % Try to find this term among the terms in the model
        oldtm = find(all(termlist == repmat(tm,size(termlist,1),1),2));
        if ~isempty(oldtm)
            dum[j] = termdum[oldtm(1)];
            continue
        end
            
        % Try to find this term among the auxiliary terms
        oldtm = find(all(auxtermlist == repmat(tm,size(auxtermlist,1),1),2));
        if ~isempty(oldtm)
            dum[j] = auxtermdum[oldtm(1)];
            continue
        end
        
        % Create an auxiliary term
        dum[j] = maketerm(tm,[],varinfo,0);
    
        auxtermdum[end+1] = dum[j];
        auxtermlist(end+1,:) = tm;
    end
    end
    
    % ---------------------------
    function m = nest_d2i(nested)
    % Take matrix specifying at least direct nesting relationships, and
    % return matrix that includes all indirect nesting relationships
    m = nested;
    n = size(m,1);
    m0 = zeros(n);
    while(~isequal(m,m0))
       m0 = m;
       m = double(m | ((m*m) > 0));
    return [p,t,stats,terms]
