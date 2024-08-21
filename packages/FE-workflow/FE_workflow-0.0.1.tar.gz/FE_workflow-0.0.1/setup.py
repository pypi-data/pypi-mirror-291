from setuptools import setup, find_packages

VERSION = '0.0.1' 
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
        packages=find_packages(),
        install_requires=["BioSimSpace"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        python_requires=">=3.7, <4", 
        keywords=['python', 'free energy','gromacs'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)
