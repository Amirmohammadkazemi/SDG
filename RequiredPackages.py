import subprocess
import subprocess
import pkg_resources
import sys
from pkg_resources import DistributionNotFound, VersionConflict


__requirement_list  = {'pip', 'numpy', 'matplotlib', 'urllib3', 'requests'}

def should_install_requirement(requirement):
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install

def install_requirements():
    try:
        requirements = [
            requirement
            for requirement in __requirement_list
            if should_install_requirement(requirement)
        ]
        if len(requirements) > 0:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
        else:
            print("Requirements already satisfied.")

    except Exception as e:
        print(e)