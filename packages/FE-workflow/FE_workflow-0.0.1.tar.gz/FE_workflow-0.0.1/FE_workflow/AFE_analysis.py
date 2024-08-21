#!/usr/bin/env python3
import BioSimSpace as BSS
import BioSimSpace.Sandpit.Exscientia as BSE
import os
import argparse
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from collections import defaultdict as ddict
import numpy as np
import glob



parser = argparse.ArgumentParser \
    ( formatter_class=argparse.RawDescriptionHelpFormatter,
      description="""
Analyze the perturbation for each phase, including complex(com), solvation(sol) and vacuum(vac), and it will provide free energy results(csv) and overlap picture for each phase in ABFE or ASFE.
).
""" )



parser.add_argument \
    ("-t","--types",
     help="The type of free energy simulations: absolute solvation free energy (ASFE) or absolute binding free energy (ABFE).",
#     nargs='+',
     choices=['ASFE','ABFE'],
     type=str,
     required=True )






parser.add_argument \
    ("-f","--filepath",
     help="Please provide the folder path for free energy calculations. The default is FreeEnergy, which is created by AFE_fesetup.py. The path organization is like this, i.e. FreeEnergy/{system_name}/{trial}/{phase}, where this python script is trying to locate.",
     type=str,                                                                          
     required=True,
     default="FreeEnergy")


parser.add_argument \
    ("-s","--sys",
     help=("The system names {sys_name}, which is used for searching folder in {filepath} you provided. In default, this script search all systems in the {filepath} you provided. But in the case that you only want to calculate one or several specific system. Here also provide this flag option. You specify the systems such as -s ejm31 ejm55, then this script will just only calculate free energy for these two systems."),
     type=str,
     #action='append',
     nargs='*',
     required=False )

parser.add_argument \
    ("-o","--output",
     help="The output directory. Default is Results, which only contains the free energy results. For the overlap plots, they are generated in input path for teh corresponding phase(com, sol or vac)",
     type=str,
     default="Results",
     required=False )




args = parser.parse_args()
print("type = ", args.types)
print("sysnames = ", args.sys)
print("filepath = ", args.filepath)
print("output = ", args.output)




def PlotOverlap(
        overlap, continuous_cbar=False, color_bar_cutoffs=[0.03, 0.1, 0.3]
        ,work_path=f"{os.getcwd()}/overlap.png"):
    """
    Plot the overlap matrix from a free-energy perturbation analysis.

    Parameters
    ----------

    overlap : List of List of float, or 2D numpy array of float
        The overlap matrix.

    continuous_cbar : bool, optional, default=False
        If True, use a continuous colour bar. Otherwise, use a discrete
        set of values defined by the 'color_bar_cutoffs' argument to
        assign a colour to each element in the matrix.

    color_bar_cutoffs : List of float, optional, default=[0.03, 0.1, 0.3]
        The cutoffs to use when assigning a colour to each element in the
        matrix. This is used for both the continuous and discrete color bars.
        Can not contain more than 3 elements.
    work_path : String for the path. The path to generate the picture
    """


    # Validate the input
    if not isinstance(overlap, (list, tuple, np.ndarray)):
        raise TypeError(
            "The 'overlap' matrix must be a list of list types, or a numpy array!"
        )

    # Try converting to a NumPy array.
    try:
        overlap = np.array(overlap)
    except:
        raise TypeError(
            "'overlap' must be of type 'np.matrix',  'np.ndarray', or a list of lists."
        )

    # Store the number of rows.
    num_rows = len(overlap)

    # Check the data in each row.
    for row in overlap:
        if not isinstance(row, (list, tuple, np.ndarray)):
            raise TypeError("The 'overlap' matrix must be a list of list types!")
        if len(row) != num_rows:
            raise ValueError("The 'overlap' matrix must be square!")
        if not all(isinstance(x, float) for x in row):
            raise TypeError("The 'overlap' matrix must contain 'float' types!")

    # Check the colour bar options
    if not isinstance(continuous_cbar, bool):
        raise TypeError("The 'continuous_cbar' option must be a boolean!")
    if not isinstance(color_bar_cutoffs, (list, tuple, np.ndarray)):
        raise TypeError(
            "The 'color_bar_cutoffs' option must be a list of floats "
            " or a numpy array when 'continuous_cbar' is False!"
        )
    if not all(isinstance(x, float) for x in color_bar_cutoffs):
        raise TypeError("The 'color_bar_cutoffs' option must be a list of floats!")
    if len(color_bar_cutoffs) > 3:
        raise ValueError(
            "The 'color_bar_cutoffs' option must contain no more than 3 elements!"
        )

    # Add 0 and 1 to the colour bar cutoffs.
    if color_bar_cutoffs is not None:
        color_bounds = [0] + color_bar_cutoffs + [1]

    # Tuple of colours and associated font colours.
    # The last and first colours are for the top and bottom of the scale
    # for the continuous colour bar, but are ignored for the discrete bar.
    all_colors = (
        ("#FBE8EB", "black"),  # Lighter pink
        ("#FFD3E0", "black"),
        ("#88CCEE", "black"),
        ("#78C592", "black"),
        ("#117733", "white"),
        ("#004D00", "white"),
    )  # Darker green

    # Set the colour map.
    if continuous_cbar:
        # Create a color map using the extended palette and positions
        box_colors = [all_colors[i][0] for i in range(len(color_bounds) + 1)]
        cmap = colors.LinearSegmentedColormap.from_list(
            "CustomMap", list(zip(color_bounds, box_colors))
        )

        # Normalise the same way each time so that plots are always comparable.
        norm = colors.Normalize(vmin=0, vmax=1)
    else:
        # Throw away the first and last colours.
        box_colors = [colors[0] for colors in all_colors[1:-1]]
        cmap = colors.ListedColormap(
            [box_colors[i] for i in range(len(color_bounds) - 1)]
        )
        norm = colors.BoundaryNorm(color_bounds, cmap.N)

    # Create the figure and axis. Use a default size for fewer than 16 windows,
    # otherwise scale the figure size to the number of windows.
    if num_rows < 16:
        fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    else:
        fig, ax = plt.subplots(figsize=(num_rows / 2, num_rows / 2), dpi=300)

    # Create the heatmap. Separate the cells with white lines.
    im = ax.imshow(overlap, cmap=cmap, norm=norm)
    for i in range(num_rows - 1):
        for j in range(num_rows - 1):
            # Make sure these are on the edges of the cells.
            ax.axhline(i + 0.5, color="white", linewidth=0.5)
            ax.axvline(j + 0.5, color="white", linewidth=0.5)

    # Label each cell with the overlap value.
    for i in range(num_rows):
        for j in range(num_rows):
            # Get the text colour based on the overlap value.
            overlap_val = overlap[i][j]
            # Get the index of first color bound greater than the overlap value.
            for idx, bound in enumerate(color_bounds):
                if bound > overlap_val:
                    break
            text_color = all_colors[1:-1][idx - 1][1]
            ax.text(
                j,
                i,
                "{:.2f}".format(overlap[i][j]),
                ha="center",
                va="center",
                fontsize=10,
                color=text_color,
            )

    # Create a colorbar. Reduce the height of the colorbar to match the figure and remove the border.
    if continuous_cbar:
        cbar = ax.figure.colorbar(im, ax=ax, cmap=cmap, norm=norm, shrink=0.7)
    else:
        cbar = ax.figure.colorbar(
            im,
            ax=ax,
            cmap=cmap,
            norm=norm,
            boundaries=color_bounds,
            ticks=color_bounds,
            shrink=0.7,
        )
    cbar.outline.set_visible(False)

    # Set the axis labels.
    # Set the x axis at the top of the plot.
    plt.xlabel(r"$\lambda$ Index")
    ax.xaxis.set_label_position("top")
    plt.ylabel(r"$\lambda$ Index")

    ticks = [x for x in range(0, num_rows)]

    # Set ticks every lambda window.
    plt.xticks(ticks)
    ax.xaxis.tick_top()
    plt.yticks(ticks)

    # Remove the borders.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Create a tight layout to trim whitespace.
    fig.tight_layout()
    return plt.savefig(work_path)




## Let user to specify the systems, or else we search them by ourself.
if args.sys == None:
    paths=sorted(glob.glob(f"{args.filepath}/*"))
else:
    paths=[]
    for i in args.sys:
        paths.append(f"{args.filepath}/{i}")


asfe_data=ddict(lambda: ddict(list))
abfe_data=ddict(lambda: ddict(list))
sys_names=[]
if len(paths) == 0:
    raise Exception(f"{args.filepath} is empty! Please double check!")
else:
    for i, filepath in enumerate(paths):
        sysname = filepath.split("/")[-1]
        sys_names.append(sysname)
        
        fl=sorted(glob.glob(f"{filepath}/t0*"))
        if len(fl) == 0:
            raise Exception(f"{filepath} does not exist any trial, i.e.'t01'. ")
        else:
            if args.types == "ASFE":
                for ipath in fl:
                    if os.path.exists(ipath):
                        sol_path=f"{ipath}/sol/pro"
                        vac_path=f"{ipath}/vac/pro"
                        if not os.path.exists(sol_path) or not os.path.exists(vac_path):
                            raise Exception(f"Either {sol_path} or {vac_path} does not exist!")
                            
                        else:
                            pmf_sol, overlap_matrix_sol = BSE.FreeEnergy.AlchemicalFreeEnergy.analyse(sol_path,temperature=300 * BSE.Units.Temperature.kelvin)
                            pmf_vac, overlap_matrix_vac = BSE.FreeEnergy.AlchemicalFreeEnergy.analyse(vac_path,temperature=300 * BSE.Units.Temperature.kelvin)
                            ### the direction is very important here! Please double check the thermodynamic cycles.
                            asfe = BSE.FreeEnergy.AlchemicalFreeEnergy.difference(pmf_vac, pmf_sol)
                            itrial=ipath[-3:] # assume that trial name is "t01" , only two digits.
                            asfe_data[sysname][itrial].append(pmf_vac[-1][1].value())
                            asfe_data[sysname][itrial].append(pmf_vac[-1][2].value())
                            asfe_data[sysname][itrial].append(pmf_sol[-1][1].value())
                            asfe_data[sysname][itrial].append(pmf_sol[-1][2].value())
                            asfe_data[sysname][itrial].append(asfe[0].value())
                            asfe_data[sysname][itrial].append(asfe[1].value())
                            PlotOverlap(overlap_matrix_sol,work_path=f"{sol_path}/overlap.png")
                            PlotOverlap(overlap_matrix_vac,work_path=f"{vac_path}/overlap.png")   
            elif args.types == "ABFE":
                for ipath in fl:
                    if os.path.exists(ipath):
                        sol_path=f"{ipath}/sol/pro"
                        com_path=f"{ipath}/com/pro"
                        if not os.path.exists(sol_path) or not os.path.exists(com_path):
                            raise Exception(f"Either {sol_path} or {com_path} does not exist!")
                            
                        else:
                            pmf_sol, overlap_matrix_sol = BSE.FreeEnergy.AlchemicalFreeEnergy.analyse(sol_path,temperature=300 * BSE.Units.Temperature.kelvin)
                            pmf_com, overlap_matrix_com = BSE.FreeEnergy.AlchemicalFreeEnergy.analyse(com_path,temperature=300 * BSE.Units.Temperature.kelvin)
                            ### the direction is very important here! Please double check the thermodynamic cycles. 
                            abfe_tmp = BSE.FreeEnergy.AlchemicalFreeEnergy.difference(pmf_sol, pmf_com)
                            ### need to get the release free energy, which is storaged in restraint.dat when ran with AFE_fesetup.py . 

                            rest_file=f"{ipath}/com/restraint.dat"
                            if not os.path.exists(rest_file):
                                raise Exception(f"{rest_file} does not exist!")
                            else:
                                fh=open(rest_file,"r")
                                content = fh.readlines()
                                text=content[-1].replace('\n','').split()
                                check=content[-2].replace('\n','')
                                fh.close()
                                if "FREE ENERGY" in check:
                                    if text[-1] == "kcal/mol":
                                        dG_release = float(text[0])
                                        
                                    else:
                                        raise Exception(f"Please make sure the release free energy has the correct unit(kcal/mol) in the last line of {rest_file}")
                                else:
                                    raise Exception(f"Please double check {rest_file} has the key words 'FREE ENERGY'!")
                                        
                                
                            ### Be carefule for the sign here(Please see https://github.com/OpenBioSim/biosimspace_tutorials/04_fep/03_ABFE for more info)
                            abfe = abfe_tmp[0].value() - dG_release
                            
                            itrial=ipath[-3:] ## assume that trial name is "t01" , only two digits.
                            abfe_data[sysname][itrial].append(pmf_sol[-1][1].value())
                            abfe_data[sysname][itrial].append(pmf_sol[-1][2].value())
                            abfe_data[sysname][itrial].append(pmf_com[-1][1].value())
                            abfe_data[sysname][itrial].append(pmf_com[-1][2].value())
                            abfe_data[sysname][itrial].append(dG_release)
                            abfe_data[sysname][itrial].append(abfe)
                            abfe_data[sysname][itrial].append(abfe_tmp[1].value())
                            PlotOverlap(overlap_matrix_sol,work_path=f"{sol_path}/overlap.png")
                            PlotOverlap(overlap_matrix_com,work_path=f"{com_path}/overlap.png")    
 



    if args.types == "ASFE":
        if len(asfe_data[sys_names[0]]["t01"]) == 0:
            raise Exception(f"The data from {sys_names[0]} t01 for asfe is empty!")
        else:
            if not os.path.exists(args.output):
                os.makedirs(args.output)
            data_file=open(f"{args.output}/asfe.csv","w")
            writer=csv.writer(data_file,delimiter=",")
            writer.writerow(["system","trial","dG_vac(kcal/mol)", "error_vac","dG_sol(kcal/mol)","error_sol","ddG(kcal/mol)", "error"])

            for pert in asfe_data:
                
                for t in asfe_data[pert]:
                    dG_vac   =asfe_data[pert][t][0]
                    dG_vac_er=asfe_data[pert][t][1]
                    dG_sol   =asfe_data[pert][t][2]
                    dG_sol_er=asfe_data[pert][t][3]
                    ddG      =asfe_data[pert][t][4]
                    ddG_er   =asfe_data[pert][t][5]
                    writer.writerow([pert, t, dG_vac, dG_vac_er, dG_sol, dG_sol_er, ddG, ddG_er])

            data_file.close()
            
    elif args.types == "ABFE":
        if len(abfe_data[sys_names[0]]["t01"]) == 0:
            raise Exception(f"The data from {sys_names[0]} t01 for abfe is empty!")
        else:
            if not os.path.exists(args.output):
                os.makedirs(args.output)
            data_file=open(f"{args.output}/abfe.csv","w")
            writer=csv.writer(data_file,delimiter=",")
            writer.writerow(["system","trial","dG_sol(kcal/mol)", "error_sol", "dG_com(kcal/mol)","error_com","dG_release(kcal/mol)","ddG(kcal/mol)", "error"])

            for pert in abfe_data:
                
                for t in abfe_data[pert]:
                    dG_sol   =abfe_data[pert][t][0]
                    dG_sol_er=abfe_data[pert][t][1]
                    dG_com   =abfe_data[pert][t][2]
                    dG_com_er=abfe_data[pert][t][3]
                    dG_re    =abfe_data[pert][t][4]
                    ddG      =abfe_data[pert][t][5]
                    ddG_er   =abfe_data[pert][t][6]
                    writer.writerow([pert, t, dG_sol, dG_sol_er, dG_com, dG_com_er, dG_re, ddG, ddG_er])

            data_file.close()        
         
                
