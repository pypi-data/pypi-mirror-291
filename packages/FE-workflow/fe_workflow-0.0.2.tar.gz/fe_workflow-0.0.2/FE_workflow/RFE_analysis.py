#!/usr/bin/env python3
import BioSimSpace as BSS
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import glob
from collections import defaultdict as ddict
import csv
import pandas as pd
import argparse




parser = argparse.ArgumentParser \
    ( formatter_class=argparse.RawDescriptionHelpFormatter,
      description="""
Analyze the perturbation for each phase, including complex(com), solvation(sol) and vacuum(vac), and it will provide free energy results(csv) and overlap picture for each phase in RBFE or RSFE. 
).
""" )


parser.add_argument \
    ("-t","--types",
     help="The type of free energy simulations: relative solvation free energy (RSFE) or relative binding free energy (RBFE).",
#     nargs='+',
     choices=['RSFE','RBFE'],
     type=str,
     required=True )


parser.add_argument \
    ("-n","--network",
     help="The network map file for all ligand perturbations, in which the first column should be formatted like 'ligA~ligB'. ",
     type=str,
     required=True )



parser.add_argument \
    ("-f","--filepath",
     help="Please provide the folder path for free energy calculations. The default is FreeEnergy, which is created by RFE_fesetup.py. The path organization is like this, i.e. FreeEnergy/{ligA~ligB}/{trial}/{phase}, where this python script is trying to locate.",
     type=str,
     required=True,
     default="FreeEnergy"    )

parser.add_argument \
    ("-o","--output",
     help="The output directory. Default is Results, which only contains the free energy results. For the overlap plots, they are generated in input path for teh corresponding phase(com, sol or vac)",
     type=str,
     default="Results",
     required=False )




args = parser.parse_args()
print("type = ", args.types)
print("network file = ",args.network)
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


def readfile(fname):
    fh=open(fname,"r")
    array=[]

    for line in fh:
        cols=line.split()
        array.append(cols[0])
    fh.close()
    return array





if not os.path.exists(args.network):
    raise Exception(f"{args.network} does not exist!")
else:
    trans=readfile(args.network)
    print(trans)
    if len(trans) == 0:
        raise Exception(f"{args.network} does not contain any information in the first column. Please double check your file!")
    else:
        rsfe_data=ddict(lambda: ddict(list))
        rbfe_data=ddict(lambda: ddict(list))
        for i,tran in enumerate(trans):
            if "~" not in tran:
                raise Exception(f"{tran} is not formatted with 'ligA~ligB'. Please provide 'ligA~ligB' formatted text in the first colunm in network file!")
            else:
                ligA=tran.split("~")[0]
                ligB=tran.split("~")[1]


    
                if args.types == "RSFE":

                    fl=sorted(glob.glob(f"{args.filepath}/{tran}/t0*"))
                    if len(fl) > 0:
                        for ipath in fl:
                            if os.path.exists(ipath):
                                sol_path=f"{ipath}/sol/pro"
                                vac_path=f"{ipath}/vac/pro"
                                if os.path.exists(sol_path) and os.path.exists(vac_path):
                                    pmf_sol, overlap_matrix_sol = BSS.FreeEnergy.Relative.analyse(sol_path)
                                    pmf_vac, overlap_matrix_vac = BSS.FreeEnergy.Relative.analyse(vac_path)
                                    rsfe = BSS.FreeEnergy.Relative.difference(pmf_sol, pmf_vac)
                                    itrial=ipath[-3:] # assume that trial name is "t01" , only two digits.
                                    rsfe_data[tran][itrial].append(pmf_sol[-1][1].value())
                                    rsfe_data[tran][itrial].append(pmf_sol[-1][2].value())
                                    rsfe_data[tran][itrial].append(pmf_vac[-1][1].value())
                                    rsfe_data[tran][itrial].append(pmf_vac[-1][2].value())
                                    rsfe_data[tran][itrial].append(rsfe[0].value())
                                    rsfe_data[tran][itrial].append(rsfe[1].value())
                                    PlotOverlap(overlap_matrix_sol,work_path=f"{sol_path}/overlap.png")
                                    PlotOverlap(overlap_matrix_vac,work_path=f"{vac_path}/overlap.png")
                                else:
                                    raise Exception(f"{sol_path} or {vac_path} does not exist!")    



                                
                            else:
                                raise Exception(f"{args.filepath}/{tran}/t0* path does not exists!")    
                    else:
                        raise Exception(f"{args.filepath}/{tran}/t0* path does not exists!")    
                    


                    
                elif args.types == "RBFE":
                    fl=sorted(glob.glob(f"{args.filepath}/{tran}/t0*"))
                    if len(fl) > 0:
                        for ipath in fl:
                            if os.path.exists(ipath):
                                sol_path=f"{ipath}/sol/pro"
                                com_path=f"{ipath}/com/pro"
                                if os.path.exists(sol_path) and os.path.exists(com_path):
                                    pmf_sol, overlap_matrix_sol = BSS.FreeEnergy.Relative.analyse(sol_path)
                                    pmf_com, overlap_matrix_com = BSS.FreeEnergy.Relative.analyse(com_path)
                                    rbfe = BSS.FreeEnergy.Relative.difference(pmf_com, pmf_sol)
                                    itrial=ipath[-3:] # assume that trial name is "t01" , only two digits.
                                    rbfe_data[tran][itrial].append(pmf_com[-1][1].value())
                                    rbfe_data[tran][itrial].append(pmf_com[-1][2].value())
                                    rbfe_data[tran][itrial].append(pmf_sol[-1][1].value())
                                    rbfe_data[tran][itrial].append(pmf_sol[-1][2].value())
                                    rbfe_data[tran][itrial].append(rbfe[0].value())
                                    rbfe_data[tran][itrial].append(rbfe[1].value())
                                    PlotOverlap(overlap_matrix_sol,work_path=f"{sol_path}/overlap.png")
                                    PlotOverlap(overlap_matrix_com,work_path=f"{com_path}/overlap.png")
                                else:
                                    raise Exception(f"{sol_path} or {com_path} does not exist!")    



                                
                            else:
                                raise Exception(f"{args.filepath}/{tran}/t0* path does not exists!")    
                    else:
                        raise Exception(f"{args.filepath}/{tran}/t0* path does not exists!")                        
        




        if args.types == "RSFE":
            if len(rsfe_data[trans[0]]["t01"]) != 0:
                if not os.path.exists(args.output):
                    os.makedirs(args.output)
                data_file=open(f"{args.output}/rsfe.csv","w")
                writer=csv.writer(data_file,delimiter=",")
                writer.writerow(["ligA", "ligB","trial","dG_sol(kcal/mol)", "error_sol","dG_vac(kcal/mol)","error_vac","ddG(kcal/mol)", "error"])

                for pert in rsfe_data:
                    lig_0 = pert.split("~")[0]
                    lig_1 = pert.split("~")[1]
                    for t in rsfe_data[pert]:
                        dG_sol   =rsfe_data[pert][t][0]
                        dG_sol_er=rsfe_data[pert][t][1]
                        dG_vac   =rsfe_data[pert][t][2]
                        dG_vac_er=rsfe_data[pert][t][3]
                        ddG      =rsfe_data[pert][t][4]
                        ddG_er   =rsfe_data[pert][t][5]
                        writer.writerow([lig_0, lig_1, t, dG_sol, dG_sol_er, dG_vac, dG_vac_er, ddG, ddG_er])
                        
                data_file.close()
            else:
                raise Exception(f"The data from {trans[0]} t01 for rsfe is empty!")
            
        elif args.types == "RBFE":
            if len(rbfe_data[trans[0]]["t01"]) != 0:
                if not os.path.exists(args.output):
                    os.makedirs(args.output)
                data_file=open(f"{args.output}/rbfe.csv","w")
                writer=csv.writer(data_file,delimiter=",")
                writer.writerow(["ligA", "ligB","trial","dG_com(kcal/mol)", "error_com","dG_sol(kcal/mol)","error_sol","ddG(kcal/mol)", "error"])

                for pert in rbfe_data:
                    lig_0 = pert.split("~")[0]
                    lig_1 = pert.split("~")[1]
                    for t in rbfe_data[pert]:
                        dG_com   =rbfe_data[pert][t][0]
                        dG_com_er=rbfe_data[pert][t][1]
                        dG_sol   =rbfe_data[pert][t][2]
                        dG_sol_er=rbfe_data[pert][t][3]
                        ddG      =rbfe_data[pert][t][4]
                        ddG_er   =rbfe_data[pert][t][5]
                        writer.writerow([lig_0, lig_1, t, dG_com, dG_com_er, dG_sol, dG_sol_er, ddG, ddG_er])
                        
                data_file.close()                
            else:
                raise Exception(f"The data from {trans[0]} t01 for rbfe is empty!")                
