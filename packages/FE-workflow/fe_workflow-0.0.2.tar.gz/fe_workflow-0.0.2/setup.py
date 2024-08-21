from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))

VERSION = '0.0.2' 
DESCRIPTION = 'Free Energy workflow'
LONG_DESCRIPTION = 'Free Energy workflow for Gromacs using BioSimSpace'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="FE_workflow", 
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url="https://github.com/jnutyj/FreeEnergy_workflow",
        license="GNU General Public License v3.0",
        packages=find_packages(),
        #install_requires=["BioSimSpace"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        python_requires=">=3.7, <4", 
        keywords=['python', 'free energy','gromacs'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Physics',            
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    scripts={"FE_workflow/AFE_parameter.py","FE_workflow/AFE_fesetup.py","FE_workflow/AFE_analysis.py","FE_workflow/RFE_network.py","FE_workflow/RFE_parameter.py","FE_workflow/RFE_fesetup.py","FE_workflow/RFE_analysis.py"},

)
