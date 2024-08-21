#!/usr/bin/env python3
import BioSimSpace as BSS
import os
import numpy as np
import argparse



 
parser = argparse.ArgumentParser \
    ( formatter_class=argparse.RawDescriptionHelpFormatter,
      description="""
Generate the parameter files for equilibrium simulation for each system. Use Gromacs in Default. The solvation and bound phases are in 0.15 mol/L ions concentration. The default setting for equilibrium is minimization (10000 steps), nvt (5ps restrainting all non-solvent atoms; 50ps restraints backbone for protein system ; another 50ps without restraints ) and npt (200ps restrainting non-solvent heavy atoms and another 200ps without restraints
). 
""" )



parser.add_argument \
    ("-t","--types",
     help="The type of simulations for equlibrium: protein+ligand (com) or ligand only (lig)",
#     nargs='+',
     choices=['com','lig'],
     type=str,
     required=True )

# parser.add_argument \
#     ("-n","--network",
#      help="The network map file for all ligand perturbations, which should the first column be format like 'ligA~ligB'",
#      type=str,
#      required=True )


parser.add_argument \
    ("-w","--water",
     help="The water type for solvation. Default is tip3p. tip4p might have minization issue.",
 #    nargs='+',
     choices=['spc', 'spce', 'tip3p', 'tip4p', 'tip5p'],
     type=str,
     required=False,
     default= 'tip3p',
     )

parser.add_argument \
    ("-f1","--ff1",
     help="The force field for ligands. Default is gaff2.",
 #    nargs='+',
     choices=[
         'gaff',
         'gaff2',
         'openff_unconstrained-2.1.0',
         'openff_unconstrained-1.0.0-RC2',
         'openff_unconstrained-1.0.1',
         'openff_unconstrained-1.2.1',
         'openff_unconstrained-2.1.1',
         'openff_unconstrained-1.3.1',
         'openff_unconstrained-2.0.0-rc.1',
         'openff_unconstrained-1.1.1',
         'openff_unconstrained-2.0.0',
         'openff_unconstrained-1.0.0',
         'openff_unconstrained-1.3.0',
         'openff_unconstrained-1.3.1-alpha.1',
         'openff_unconstrained-1.1.0',
         'openff_unconstrained-2.1.0-rc.1',
         'openff_unconstrained-1.2.0',
         'openff_unconstrained-2.2.0',
         'openff_unconstrained-2.0.0-rc.2',
         'openff_unconstrained-2.2.0-rc1',
         'openff_unconstrained-1.0.0-RC1'
     ],
     type=str,
     required=False,
     default='gaff2'
     )

parser.add_argument \
    ("-f2","--ff2",
     help="The force field for protein. Only require for RBFE or ALL. Default is ff14SB.",
#     nargs='+',
     choices=[
         'ff03',
         'ff99',
         'ff99SB',
         'ff99SBildn',
         'ff14SB'
     ],
     type=str,
     required=False,
     default= 'ff14SB')

parser.add_argument \
    ("-b","--buffers",
     help = "Here we calculate the box size based on the system size and add extra buffer (the distance between the edge of system to the box).Default is 10 A.  Unit is angstrom.",
     type=float,
     required = False,
     default = 10.0,
    )

parser.add_argument \
    ("-s","--boxshape",
     help = "The box shape in the system. Default is cubic.",
     type=str,
#     nargs='+',
     choices=[
         'cubic',
         'rhombicDodecahedronHexagon',
         'rhombicDodecahedronSquare',
         'truncatedOctahedron'
     ],
     required = False,
     default = 'cubic',
    )


parser.add_argument \
    ("-l","--ligs",
     help=("Ligands sdf files"),
     type=str,
     #action='append',
     nargs='*',
     required=True )


parser.add_argument \
    ("-p","--protein",
     help=("Protein pdb file without other things, including water, ions or ligands. Please prepare the pdb by cleaning and adding missing residues beforehand"),
     type=str,
     default=None,
     required=False )


parser.add_argument \
    ("-o","--output",
     help="The output directory.Default is Prep",
     type=str,
     default="Prep",
     required=False )


parser.add_argument \
    ("-ts","--timestep",
     help="The time steps for each equilibrium steps: minimization (10000 steps), nvt (5ps restraint non-solvent), nvt (50ps restraint backbone only for protein system),  nvt (50ps without restraint), npt (200ps restraint non-solvent heavy atoms), npt (200ps without restraint). The unit is picosecond",
     type=int,
     nargs='+',
     default=[10000, 5, 50, 50, 200, 200],
     required=False )

args = parser.parse_args()

#print(args.types)

print("types=",args.types)
#print("network=",args.network)
print("water=",args.water)
print("ligand FF=",args.ff1)
print("protein FF=",args.ff2)
print("box buffer=", args.buffers)
print("boxshape=",args.boxshape)
print("ligands file=",args.ligs)
print("protein file=",args.protein)
print("output path=",args.output)
print("time step=", args.timestep)





def PrepLig(ligand_file):
    # take the first molecule as the ligand
    mol = BSS.IO.readMolecules(ligand_file)[0]
    mol_p = BSS.Parameters.parameterise(mol, args.ff1).getMolecule()
    # minimally encloses
    box_min, box_max = mol_p.getAxisAlignedBoundingBox()
    
    # Work out the box size from the difference in the coordinates.
    box_size = [y - x for x, y in zip(box_min, box_max)]

    # How much to pad each side of the protein? (Nonbonded cutoff = 10 A)
    padding = args.buffers * BSS.Units.Length.angstrom
    # Work out an appropriate box. This will used in each dimension to ensure
    # that the cutoff constraints are satisfied if the molecule rotates.
    box_length = max(box_size) + 2 * padding
    
    box, angles = BSS.Box.generateBoxParameters(args.boxshape, box_length)
    
    mol_p_solvated = BSS.Solvent.solvate(args.water, molecule=mol_p, box=box, angles=angles, ion_conc=0.15)
    return mol_p_solvated
    








def PrepProt(ligand_file,prot_p):
    # double check and make sure your protein only one molecules
    
    #prot = BSS.IO.readPDB(protein_file,pdb4amber=False)[0]
    #prot_p = BSS.Parameters.parameterise(prot, args.ff2).getMolecule()

    
    # take the first molecule as the ligand
    mol = BSS.IO.readMolecules(ligand_file)[0]
    mol_p = BSS.Parameters.parameterise(mol, args.ff1).getMolecule()

    com_p = mol_p + prot_p
    
    # minimally encloses
    box_min, box_max = com_p.getAxisAlignedBoundingBox()
    
    # Work out the box size from the difference in the coordinates.
    box_size = [y - x for x, y in zip(box_min, box_max)]

    # How much to pad each side of the protein? (Nonbonded cutoff = 10 A)
    padding = args.buffers * BSS.Units.Length.angstrom
    # Work out an appropriate box. This will used in each dimension to ensure
    # that the cutoff constraints are satisfied if the molecule rotates.
    box_length = max(box_size) + 2 * padding
    
    box, angles = BSS.Box.generateBoxParameters(args.boxshape, box_length)
    
    com_p_solvated = BSS.Solvent.solvate(args.water, molecule=com_p, box=box, angles=angles, ion_conc=0.15)
    return com_p_solvated







    
if args.types == "lig":
    p01_min=BSS.Protocol.Minimisation(steps=args.timestep[0])
    p02_nvt_all = BSS.Protocol.Equilibration(
        runtime=args.timestep[1] * BSS.Units.Time.picosecond,
        temperature_start=0 * BSS.Units.Temperature.kelvin,
        temperature_end=300 * BSS.Units.Temperature.kelvin,
        restraint="all")
    p03_nvt_relax = BSS.Protocol.Equilibration(
        runtime=args.timestep[3] * BSS.Units.Time.picosecond,
        temperature=300 * BSS.Units.Temperature.kelvin)
    
    p04_npt_heavy = BSS.Protocol.Equilibration(
        runtime=args.timestep[4] * BSS.Units.Time.picosecond,
        pressure=1 * BSS.Units.Pressure.atm,
        temperature=300 * BSS.Units.Temperature.kelvin,
        restraint="heavy")
    
    p05_npt_relax =  BSS.Protocol.Equilibration(
        runtime=args.timestep[5] * BSS.Units.Time.picosecond,
        pressure=1 * BSS.Units.Pressure.atm,
        temperature=300 * BSS.Units.Temperature.kelvin)
    

    
    for lig_file in args.ligs:
        lig_name = lig_file.split("/")[-1].replace(".sdf","")
        print(f"Creating solvation system for {lig_name}")
        path_name=f"{args.output}/{lig_name}/lig"
        lig_sol = PrepLig(lig_file)
        if not os.path.exists(path_name):
            os.makedirs(path_name)
        if os.path.exists(f"{path_name}/system.gro") or os.path.exists(f"{path_name}/system.top"):
            print(f"{path_name}/system.gro or {path_name}/system.top exists. It won't regenerate the files for this system." )
            continue
        else:
            BSS.IO.saveMolecules(f"{path_name}/system", lig_sol, ["gro87", "grotop","prm7","rst7"])
        
        
        BSS.Process.Gromacs(lig_sol, p01_min, name="01_min",work_dir=f"{path_name}/01_min")
        BSS.Process.Gromacs(lig_sol, p02_nvt_all, name="02_nvt_all",work_dir=f"{path_name}/02_nvt_all")
        BSS.Process.Gromacs(lig_sol, p03_nvt_relax, name="03_nvt_relax",work_dir=f"{path_name}/03_nvt_relax")
        BSS.Process.Gromacs(lig_sol, p04_npt_heavy, name="04_npt_heavy",work_dir=f"{path_name}/04_npt_heavy")
        BSS.Process.Gromacs(lig_sol, p05_npt_relax, name="05_npt_relax",work_dir=f"{path_name}/05_npt_relax")

        ## TODO: maybe think about how to optimize the running cpu based on the system ligands
        ## TODO: check previous step finished or not
        
        if not os.path.exists(f"{path_name}/submit_slurm.sh"):
            fh = open(f"{path_name}/submit_slurm.sh","w")
            fh.write(
                """#!/bin/bash
#SBATCH --job-name=LIG%s
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=1GB
#SBATCH --partition=bsc120c
#SBATCH --exclude=bsc120c-pg0-[1-3],bsc120c-pg0-[5-30]
#SBATCH --no-requeue

source /anfhome/.profile
module load gromacs
export GMX="gmx_mpi"
export LAUNCH="mpirun -np 1"
steps=(01_min 02_nvt_all 03_nvt_relax 04_npt_heavy 05_npt_relax)




for i in $(seq 0 $((${#steps[@]}-1)));do
    if [ ! -e ${steps[$i]}/${steps[$i]}.log ];then
        echo "${steps[$i]}/${steps[$i]}.log not exist and start running..."
        if [ $i == 0 ];then                
           echo "Running ${steps[$i]}"
           ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c system.gro -p system.top -r system.gro -o ${steps[$i]}/${steps[$i]}.tpr
           ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        elif [ $i == 1 ];then
           echo "Running ${steps[$i]}"
           ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -o ${steps[$i]}/${steps[$i]}.tpr
           ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        else
           echo "Running ${steps[$i]}"
           ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -t ${steps[$(($i-1))]}/${steps[$(($i-1))]}.cpt -o ${steps[$i]}/${steps[$i]}.tpr
           ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        
        fi
    else
        value=$(tail -n 2 ${steps[$i]}/${steps[$i]}.log | head -n 1 |  awk '{print $1}')
        if [[ ${value} != "Finished" ]];then
           echo "${steps[$i]}/${steps[$i]}.log not finished and start running..."
           if [ $i == 0 ];then                
              echo "Running ${steps[$i]}"
              ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c system.gro -p system.top -r system.gro -o ${steps[$i]}/${steps[$i]}.tpr
              ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
           elif [ $i == 1 ];then
              echo "Running ${steps[$i]}"
              ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -o ${steps[$i]}/${steps[$i]}.tpr
              ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
           else
              echo "Running ${steps[$i]}"
              ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -t ${steps[$(($i-1))]}/${steps[$(($i-1))]}.cpt -o ${steps[$i]}/${steps[$i]}.tpr
              ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        
           fi
        else 
           echo "${steps[$i]}/${steps[$i]} finished"
        fi
        
    fi
done




"""%(lig_name))
            fh.close() 
        
    
    
elif args.types == "com":
    if args.protein == None:
        raise Exception(f"Please provide protein pdb file, because you selected 'com'")
    else:
        # double check and make sure your protein only one molecules
    
        prot = BSS.IO.readPDB(args.protein, pdb4amber=False)[0]
        protein_p = BSS.Parameters.parameterise(prot, args.ff2).getMolecule()

        
        p01_min=BSS.Protocol.Minimisation(steps=args.timestep[0])
        
        p02_nvt_all = BSS.Protocol.Equilibration(
            runtime=args.timestep[1] * BSS.Units.Time.picosecond,
            temperature_start=0 * BSS.Units.Temperature.kelvin,
            temperature_end=300 * BSS.Units.Temperature.kelvin,
            restraint="all")

        p03_nvt_backbone = BSS.Protocol.Equilibration(
            runtime=args.timestep[2] * BSS.Units.Time.picosecond,
            temperature=300 * BSS.Units.Temperature.kelvin,
            restraint="backbone")

        
        p03_nvt_relax = BSS.Protocol.Equilibration(
            runtime=args.timestep[3] * BSS.Units.Time.picosecond,
            temperature=300 * BSS.Units.Temperature.kelvin)
    
        p04_npt_heavy = BSS.Protocol.Equilibration(
            runtime=args.timestep[4] * BSS.Units.Time.picosecond,
            pressure=1 * BSS.Units.Pressure.atm,
            temperature=300 * BSS.Units.Temperature.kelvin,
            restraint="heavy")
        
        p05_npt_relax =  BSS.Protocol.Equilibration(
            runtime=args.timestep[5] * BSS.Units.Time.picosecond,
            pressure=1 * BSS.Units.Pressure.atm,
            temperature=300 * BSS.Units.Temperature.kelvin)
        
        for lig_file in args.ligs:
            lig_name = lig_file.split("/")[-1].replace(".sdf","")
            path_name=f"{args.output}/{lig_name}/com"
            com_sol = PrepProt(lig_file,protein_p)
            print(f"Creating complex system for {lig_name}")
            
            if not os.path.exists(path_name):
                os.makedirs(path_name)
            if os.path.exists(f"{path_name}/system.gro") or os.path.exists(f"{path_name}/system.top"):
                print(f"{path_name}/system.gro or {path_name}/system.top exists. It won't regenerate the files for this system." )
                continue
            else:
                BSS.IO.saveMolecules(f"{path_name}/system", com_sol, ["gro87", "grotop","prm7","rst7"])
        
        
    
            BSS.Process.Gromacs(com_sol, p01_min, name="01_min",work_dir=f"{path_name}/01_min")
            BSS.Process.Gromacs(com_sol, p02_nvt_all, name="02_nvt_all",work_dir=f"{path_name}/02_nvt_all")
            BSS.Process.Gromacs(com_sol, p03_nvt_backbone, name="03_nvt_backbone",work_dir=f"{path_name}/03_nvt_backbone")
            BSS.Process.Gromacs(com_sol, p03_nvt_relax, name="03_nvt_relax",work_dir=f"{path_name}/03_nvt_relax")
            BSS.Process.Gromacs(com_sol, p04_npt_heavy, name="04_npt_heavy",work_dir=f"{path_name}/04_npt_heavy")
            BSS.Process.Gromacs(com_sol, p05_npt_relax, name="05_npt_relax",work_dir=f"{path_name}/05_npt_relax")



            if not os.path.exists(f"{path_name}/submit_slurm.sh"):
                fh = open(f"{path_name}/submit_slurm.sh","w")
                fh.write(
                    """#!/bin/bash
#SBATCH --job-name=COM%s
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=1GB
#SBATCH --partition=bsc120c
#SBATCH --exclude=bsc120c-pg0-[1-3],bsc120c-pg0-[5-30]
#SBATCH --no-requeue

source /anfhome/.profile
module load gromacs
export GMX="gmx_mpi"
export LAUNCH="mpirun -np 10"
steps=(01_min 02_nvt_all 03_nvt_backbone 03_nvt_relax 04_npt_heavy 05_npt_relax)




for i in $(seq 0 $((${#steps[@]}-1)));do
    if [ ! -e ${steps[$i]}/${steps[$i]}.log ];then
        echo "${steps[$i]}/${steps[$i]}.log not exist and start running..."
        if [ $i == 0 ];then                
           echo "Running ${steps[$i]}"
           ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c system.gro -p system.top -r system.gro -o ${steps[$i]}/${steps[$i]}.tpr
           ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        elif [ $i == 1 ];then
           echo "Running ${steps[$i]}"
           ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -o ${steps[$i]}/${steps[$i]}.tpr
           ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        else
           echo "Running ${steps[$i]}"
           ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -t ${steps[$(($i-1))]}/${steps[$(($i-1))]}.cpt -o ${steps[$i]}/${steps[$i]}.tpr
           ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        
        fi
    else
        value=$(tail -n 2 ${steps[$i]}/${steps[$i]}.log | head -n 1 |  awk '{print $1}')
        if [[ ${value} != "Finished" ]];then
           echo "${steps[$i]}/${steps[$i]}.log not finished and start running..."
           if [ $i == 0 ];then                
              echo "Running ${steps[$i]}"
              ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c system.gro -p system.top -r system.gro -o ${steps[$i]}/${steps[$i]}.tpr
              ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
           elif [ $i == 1 ];then
              echo "Running ${steps[$i]}"
              ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -o ${steps[$i]}/${steps[$i]}.tpr
              ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
           else
              echo "Running ${steps[$i]}"
              ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${steps[$i]}.mdp -c ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -p ${steps[$i]}/${steps[$i]}.top -r ${steps[$(($i-1))]}/${steps[$(($i-1))]}_out.gro -t ${steps[$(($i-1))]}/${steps[$(($i-1))]}.cpt -o ${steps[$i]}/${steps[$i]}.tpr
              ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${steps[$i]} -c ${steps[$i]}/${steps[$i]}_out.gro
        
           fi
        else 
           echo "${steps[$i]}/${steps[$i]} finished"
        fi
        
    fi
done




"""%(lig_name) )
                fh.close() 
