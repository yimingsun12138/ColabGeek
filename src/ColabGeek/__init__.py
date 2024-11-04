import os
import warnings

###########################
## define setup function ##
###########################

# root user check
def _root_user_check():
    """Check if the current user is root."""

    if (os.geteuid() != 0):
        warnings.warn(message = "The current user is not root, some features may not work properly!",category = UserWarning)

################################
## action upon package import ##
################################

# root user check
_root_user_check()

# import from ColabGeek
from .ColabGeek import *
