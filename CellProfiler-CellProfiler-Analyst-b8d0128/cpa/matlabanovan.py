def matlabanovan(y,group,**args):
    from pymatlab.matlab import MatlabSession
    session = MatlabSession()
    session.close()
    session = MatlabSession('matlab -nojvm -nodisplay')
    session.PutValue('y',y)
    session.PutValue('group', group)
    session.PutValue('varargin' **args)
    session.run('anovan(y, group, varargin)')
    