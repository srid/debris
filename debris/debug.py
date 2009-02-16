# Debug related functions

import sys
import pdb


def SHELL():
    """Break the application and run the PDB shell
    """
    pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__).set_trace(sys._getframe().f_back)


