#!/usr/bin/env python3
import BioSimSpace as BSS
import os
import glob
import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser \
    ( formatter_class=argparse.RawDescriptionHelpFormatter,
      description="""
Generate the lomap for pertubations based on ligands sdf files provided
""" )

# parser.add_argument \
#     ("-l","--ligs",
#      help="The path for ligand sdf files",
#      type=str,
#      required=True )


parser.add_argument \
    ("-l","--ligs",
     help=("Ligands sdf files"),
     type=str,
     #action='append',
     nargs='*',
     required=True )

parser.add_argument \
    ("-o","--output",
     help="The output directory",
     type=str,
     default="output",
     required=False )




args = parser.parse_args()
#path_to_ligands=args.ligs


if not os.path.exists(args.output):
    os.mkdir(args.output)

#ligand_files=sorted(glob.glob(f"{path_to_ligands}/*.sdf"))
ligs=args.ligs
ligand_files=sorted(ligs)


if len(ligand_files) == 0:
    raise NameError(
        #f"Cannot find the ligands in {path_to_ligands} with extension of sdf."
        f"Cannot find the ligands {ligs}."
    )

ligands=[]
ligand_names=[]

for filepath in ligand_files:
    ligands.append(BSS.IO.readMolecules(filepath)[0])
    if filepath[-3:].lower() != "sdf":
        raise NameError(f"{filepath} is not ended with .sdf")
    else:
        ligand_names.append(filepath.split("/")[-1].replace(".sdf",""))


transformations,lomap_scores = BSS.Align.generateNetwork(ligands, plot_network=True, names=ligand_names,work_dir=args.output)


pert_network_dict={}

transformations_named = [
    (ligand_names[transf[0]], ligand_names[transf[1]]) for transf in transformations
]


fh=open("%s/network.dat"%(args.output), "w")
writer = csv.writer(fh,delimiter=" ")
for score, transf in sorted(zip(lomap_scores, transformations_named)):
    pert_network_dict[transf] = score
    writer.writerow([f"{transf[0]}~{transf[1]}",score])

## another way to see the network without the chamdraw structures

# Generate the graph.
graph = nx.Graph()

# Loop over the nligands and add as nodes to the graph.
for lig in ligand_names:
    graph.add_node(lig, label=lig, labelloc="t")

# Loop over the edges in the dictionary and add to the graph.
for edge in pert_network_dict:
    graph.add_edge(edge[0], edge[1], label=(pert_network_dict[edge]))

# Plot the networkX graph.
pos = nx.kamada_kawai_layout(graph)
plt.figure()
nx.draw(
    graph,
    pos,
    edge_color="black",
    width=1,
    linewidths=1,
    node_size=1000,
    node_color="skyblue",
    font_size=10,
    labels={node: node for node in graph.nodes()},
)


edge_label=dict([(pert, "%.2f"%(lomap_score)) for pert, lomap_score in pert_network_dict.items()])
nx.draw_networkx_edge_labels(
    graph, pos, edge_labels=edge_label, font_color="purple", font_size=8
)

plt.savefig(f"{args.output}/network_graph.png", dpi=300)

