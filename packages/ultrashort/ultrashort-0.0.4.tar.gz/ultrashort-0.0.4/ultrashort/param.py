"""Routines for dealing with parameters"""

def get_param_from_eq_sep_file(param_file_path, param_name):
    """
    Parse a parameter files with a list of lines in a form: 
    'param_name=param_value'
    """
    with open(param_file_path) as f: _param_file_str = f.read()
    _matched_list = [line.split('=')[1] 
            for line in _param_file_str.split('\n') 
            if line.split('=')[0] == param_name]
    _matched_num = len(_matched_list)
    if _matched_num == 0: raise Exception("No match")
    elif _matched_num == 1: return _matched_list[0]
    elif _matched_num > 1: Exception("Multiple matches")
    else: raise Exception("Unexpected exception")

