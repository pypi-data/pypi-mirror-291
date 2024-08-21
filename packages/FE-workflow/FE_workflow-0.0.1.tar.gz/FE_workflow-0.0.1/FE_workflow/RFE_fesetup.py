#!/usr/bin/env python3
import BioSimSpace as BSS
import os
import numpy as np
import argparse
import shutil



parser = argparse.ArgumentParser \
    ( formatter_class=argparse.RawDescriptionHelpFormatter,
      description="""
Generate the merged parameter files for relative free energy simulation, including relative solvation free energy(RSFE) and relative binding free energy(RBFE). Use Gromacs in Default. This free energy wordflow does not include features for replica exchance sampling. 
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
     help="The network map file for all ligand perturbations, in which the first column should be formatted like 'ligA~ligB', and the secondcolumn is the lomap scores which calculated by RFE_network.py. ",
     type=str,
     required=True )



parser.add_argument \
    ("-f","--filepath",
     help="Please provide the folder path for pre-equilirbium system. The default is Prep, which is created by RFE_parameter.py. The path organization is like this, i.e. Prep/{lig_name}/lig/05_npt_relax, where this python script is trying to locate.",
     type=str,
     required=True,
     default="Prep"
        
    )

parser.add_argument \
    ("-ts","--timestep",
     help="Each of the lambda window will run with minization, NVT, NPT and Production, except that no NPT in vacuum phase. The time step here is just for production, and the unit is nanosecond. Default is 5.0 ns.",
     type=float,
     required=False,
     default=5.0,
        
    )


parser.add_argument \
    ("-s","--score",
     help="The threshold of lomap score for each pair of perturbation. Here it reads the second column of network file to identify the lomap score for each perturbation, if it is less than this threshold, then the number of lambda window will be increased to 21, or else the number of lambda window will be defined as 11. The default threshold is 0.4",
     type=float,
     required=False,
     default=0.4,
        
    )



parser.add_argument \
    ("-tl","--trials",
     help="The number of trials for repeating the simulation for each of them. Default is 1.",
     type=int,
     required=False,
     default=1,
        
    )


parser.add_argument \
    ("-o","--output",
     help="The output directory. Default is FreeEnergy",
     type=str,
     default="FreeEnergy",
     required=False )


args = parser.parse_args()
print("type = ", args.types)
print("network file = ",args.network)
print("filepath = ", args.filepath)
print(f"time step = {args.timestep} ns")
print("lomap threshold = ", args.score)
print("trials = ", args.trials)
print("output = ", args.output)


def readfile(fname):
    fh=open(fname,"r")
    array=[]
    lscores=[]
    for line in fh:
        cols=line.split()
        array.append(cols[0])
        if len(cols) > 1:
            lscore=float(cols[1])
            
            lscores.append(lscore)
        else:
            lscores.append(0.1) #define the lomap score with low one, if the network file does not provide with this information. 
    fh.close()   
    return array, lscores



if not os.path.exists(args.network):
    raise Exception(f"{args.network} does not exist!")
else:
    trans,scores=readfile(args.network)
    print(trans)
    if len(trans) == 0:
        raise Exception(f"{args.network} does not contain any information in the first column. Please double check your file!")
    else:
        for i,tran in enumerate(trans):
            if "~" not in tran:
                raise Exception(f"{tran} is not formatted with 'ligA~ligB'. Please provide 'ligA~ligB' formatted text in the first colunm in network file!")
            else:
                ligA=tran.split("~")[0]
                ligB=tran.split("~")[1]

                ligA_gro=f"{args.filepath}/{ligA}/lig/05_npt_relax/05_npt_relax_out.gro"
                ligA_top=f"{args.filepath}/{ligA}/lig/05_npt_relax/05_npt_relax.top"
                ligB_gro=f"{args.filepath}/{ligB}/lig/05_npt_relax/05_npt_relax_out.gro"
                ligB_top=f"{args.filepath}/{ligB}/lig/05_npt_relax/05_npt_relax.top"
                
                comA_gro=f"{args.filepath}/{ligA}/com/05_npt_relax/05_npt_relax_out.gro"
                comA_top=f"{args.filepath}/{ligA}/com/05_npt_relax/05_npt_relax.top"
                comB_gro=f"{args.filepath}/{ligB}/com/05_npt_relax/05_npt_relax_out.gro"
                comB_top=f"{args.filepath}/{ligB}/com/05_npt_relax/05_npt_relax.top"                
                
                
                
                if os.path.exists(ligA_top) and os.path.exists(ligA_gro) and os.path.exists(ligB_top) and os.path.exists(ligB_gro):
                    ligA_sys = BSS.IO.readMolecules([ligA_gro,ligA_top])
                    ligB_sys = BSS.IO.readMolecules([ligB_gro,ligB_top])

                    ligA_mol=ligA_sys.getMolecule(0)
                    ligB_mol=ligB_sys.getMolecule(0)
                    
                    print(f"Mapping and aligning {ligA} and {ligB} for solvation...")
                    
                    mapping = BSS.Align.matchAtoms(ligA_mol, ligB_mol, complete_rings_only=True)
                    inv_mapping = {v: k for k, v in mapping.items()}
                    
                    ligB_a = BSS.Align.rmsdAlign(ligB_mol, ligA_mol, inv_mapping)
                    
                    # Generate merged molecule.
                    print("Merging..")
                    merged_ligs = BSS.Align.merge(ligA_mol, ligB_a, mapping)
                    #### Get equilibrated waters and waterbox information for both bound and free. Get all information from lambda==0
                    # Following is work around because setBox() doesn't validate correctly boxes with lengths and angles

                    ligA_sys.removeMolecules(ligA_mol)
                    ligA_sys.addMolecules(merged_ligs)
                    sol_sys = ligA_sys

                    if scores[i] >= args.score:
                        num_lambda=11
                    else:
                        num_lambda=21
                        
                    
                    sol_path=f"{args.output}/{tran}/template/sol"
                    if not os.path.exists(sol_path):
                        os.makedirs(sol_path)
                    

                    runtime_query = args.timestep
                    runtime_unit = BSS.Units.Time.nanosecond
                    min_protocol = BSS.Protocol.FreeEnergyMinimisation(num_lam=num_lambda)
                    nvt_protocol = BSS.Protocol.FreeEnergyEquilibration(num_lam=num_lambda, pressure=None)
                    npt_protocol = BSS.Protocol.FreeEnergyEquilibration(num_lam=num_lambda, pressure=1 * BSS.Units.Pressure.atm)
                    pro_protocol = BSS.Protocol.FreeEnergy(num_lam=num_lambda, runtime=runtime_query * runtime_unit)
                    pro2_protocol= BSS.Protocol.FreeEnergy(num_lam=num_lambda, runtime=runtime_query * runtime_unit, pressure=None)
                    

                    
                    if args.types == "RSFE":
                        # for RSFE, because in vacuum, we cannot use NPT for production, so to make everything consistent, solvation phase is also NVT for production.
                        if not os.path.exists(f"{sol_path}/min"):
                            BSS.FreeEnergy.Relative(sol_sys, min_protocol, engine="gromacs", work_dir=sol_path + "/min")

                        if not os.path.exists(f"{sol_path}/nvt"):
                            BSS.FreeEnergy.Relative(sol_sys, nvt_protocol, engine="gromacs", work_dir=sol_path + "/nvt")
                        if not os.path.exists(f"{sol_path}/npt"):
                            BSS.FreeEnergy.Relative(sol_sys, npt_protocol, engine="gromacs", work_dir=sol_path + "/npt")
                        if not os.path.exists(f"{sol_path}/pro"):
                            BSS.FreeEnergy.Relative(sol_sys, pro2_protocol, engine="gromacs", work_dir=sol_path + "/pro")
                    
                        if not os.path.exists(f"{sol_path}/submit_slurm.sh"):
                            fh = open(f"{sol_path}/submit_slurm.sh","w")
                            fh.write(
                            """#!/bin/bash 
#SBATCH --job-name=SOL%s
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

NLAM=%i
"""%(tran,num_lambda))
                            fh.write(
                            """
DLAM=$(bc -l <<< "1./(${NLAM}-1)")
FLAM=$(printf "%.4f" ${DLAM})
LAMS=($( for i in $(seq ${NLAM}); do printf " %.4f" $(bc -l <<< "($i-1.)/(${NLAM}-1.)"); done))
steps=(min nvt npt pro)



for i in $(seq 0 $((${#steps[@]}-1)));do
    for ilam in ${LAMS[@]};do
        lam=$(printf "lambda_%s" ${ilam})
        if [ ! -e "${steps[$i]}/${lam}/gromacs.log" ];then
            echo "${steps[$i]}/${lam}/gromacs.log not exist and start running..."
            if [ $i == 0 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            elif [ $i == 1 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            else
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            fi
        else 
            value=$(tail -n 2 ${steps[$i]}/${lam}/gromacs.log | head -n 1 |  awk '{print $1}')
            if [[ ${value} != "Finished" ]];then
                echo "${steps[$i]}/${lam}/gromacs.log not finished and start running..."
                if [ $i == 0 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                elif [ $i == 1 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                else
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                fi
            else
                echo "${steps[$i]}/${lam} finished"
            fi
            
        fi
    done
    

done



                            """)
                            fh.close()
                    
                    

                        vac_path=f"{args.output}/{tran}/template/vac"
                        if not os.path.exists(vac_path):
                            os.makedirs(vac_path)
                        print("Creating vacuum phases...")
                        vac_sys = merged_ligs.toSystem()
                        if not os.path.exists(f"{vac_path}/min"):
                            BSS.FreeEnergy.Relative(vac_sys, min_protocol, engine="gromacs", work_dir=vac_path + "/min")
                        if not os.path.exists(f"{vac_path}/nvt"):
                            BSS.FreeEnergy.Relative(vac_sys, nvt_protocol, engine="gromacs", work_dir=vac_path + "/nvt")
                        if not os.path.exists(f"{vac_path}/pro"):
                            BSS.FreeEnergy.Relative(vac_sys, pro_protocol, engine="gromacs", work_dir=vac_path + "/pro")
                        if not os.path.exists(f"{vac_path}/submit_slurm.sh"):
                            fh = open(f"{vac_path}/submit_slurm.sh","w")
                            fh.write(
                            """#!/bin/bash 
#SBATCH --job-name=VAC%s
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

NLAM=%i
"""%(tran,num_lambda))
                            fh.write(
                            """
DLAM=$(bc -l <<< "1./(${NLAM}-1)")
FLAM=$(printf "%.4f" ${DLAM})
LAMS=($( for i in $(seq ${NLAM}); do printf " %.4f" $(bc -l <<< "($i-1.)/(${NLAM}-1.)"); done))
steps=(min nvt pro)



for i in $(seq 0 $((${#steps[@]}-1)));do
    for ilam in ${LAMS[@]};do
        lam=$(printf "lambda_%s" ${ilam})
        if [ ! -e "${steps[$i]}/${lam}/gromacs.log" ];then
            echo "${steps[$i]}/${lam}/gromacs.log not exist and start running..."
            if [ $i == 0 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            elif [ $i == 1 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            else
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            fi
        else 
            value=$(tail -n 2 ${steps[$i]}/${lam}/gromacs.log | head -n 1 |  awk '{print $1}')
            if [[ ${value} != "Finished" ]];then
                echo "${steps[$i]}/${lam}/gromacs.log not finished and start running..."
                if [ $i == 0 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                elif [ $i == 1 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                else
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 10 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                fi
            else
                echo "${steps[$i]}/${lam} finished"
            fi
            
        fi
    done
    

done



                            """)
                            fh.close()
                    
                    
                    elif args.types == "RBFE":
                        if not os.path.exists(f"{sol_path}/min"):
                            BSS.FreeEnergy.Relative(sol_sys, min_protocol, engine="gromacs", work_dir=sol_path + "/min")
                        if not os.path.exists(f"{sol_path}/nvt"):
                            BSS.FreeEnergy.Relative(sol_sys, nvt_protocol, engine="gromacs", work_dir=sol_path + "/nvt")
                        if not os.path.exists(f"{sol_path}/npt"):
                            BSS.FreeEnergy.Relative(sol_sys, npt_protocol, engine="gromacs", work_dir=sol_path + "/npt")
                        if not os.path.exists(f"{sol_path}/pro"):
                            BSS.FreeEnergy.Relative(sol_sys, pro_protocol, engine="gromacs", work_dir=sol_path + "/pro")
                    
                        if not os.path.exists(f"{sol_path}/submit_slurm.sh"):
                            fh = open(f"{sol_path}/submit_slurm.sh","w")
                            fh.write(
                            """#!/bin/bash 
#SBATCH --job-name=SOL%s
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

NLAM=%i
"""%(tran,num_lambda))
                            fh.write(
                            """
DLAM=$(bc -l <<< "1./(${NLAM}-1)")
FLAM=$(printf "%.4f" ${DLAM})
LAMS=($( for i in $(seq ${NLAM}); do printf " %.4f" $(bc -l <<< "($i-1.)/(${NLAM}-1.)"); done))
steps=(min nvt npt pro)



for i in $(seq 0 $((${#steps[@]}-1)));do
    for ilam in ${LAMS[@]};do
        lam=$(printf "lambda_%s" ${ilam})
        if [ ! -e "${steps[$i]}/${lam}/gromacs.log" ];then
            echo "${steps[$i]}/${lam}/gromacs.log not exist and start running..."
            if [ $i == 0 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            elif [ $i == 1 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            else
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            fi
        else 
            value=$(tail -n 2 ${steps[$i]}/${lam}/gromacs.log | head -n 1 |  awk '{print $1}')
            if [[ ${value} != "Finished" ]];then
                echo "${steps[$i]}/${lam}/gromacs.log not finished and start running..."
                if [ $i == 0 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                elif [ $i == 1 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                else
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                fi
            else
                echo "${steps[$i]}/${lam} finished"
            fi
            
        fi
    done
    

done



                            """)
                            fh.close()
                    
                    

                        
                        if os.path.exists(comA_top) and os.path.exists(comA_gro) and os.path.exists(comB_top) and os.path.exists(comB_gro):
                            system_A = BSS.IO.readMolecules([comA_gro,comA_top])
                            system_B = BSS.IO.readMolecules([comB_gro,comB_top])
                            # Extract ligands and protein. Do this based on nAtoms and nResidues, as sometimes
                            # the order of molecules is switched, so we can't use index alone.
                            # bugfix in BSS makes the below redundant but keeping this in to be 100% sure we're getting the correct structures.
                            mol_ligA = None
                            protein = None
                            n_residues = [mol.nResidues() for mol in system_A]
                            n_atoms = [mol.nAtoms() for mol in system_A]
                            for k, (n_resi, n_at) in enumerate(zip(n_residues[:20], n_atoms[:20])):
                                if n_resi == 1 and n_at > 5:
                                    mol_ligA = system_A.getMolecule(k)
                                elif n_resi > 1:
                                    protein = system_A.getMolecule(k)
                                else:
                                    pass


                            # loop over molecules in system to extract the ligand
                            mol_ligB = None

                            n_residues = [mol.nResidues() for mol in system_B]
                            n_atoms = [mol.nAtoms() for mol in system_B]
                            for k, (n_resi, n_at) in enumerate(zip(n_residues, n_atoms)):
                                # grab the system's ligand and the protein. ignore the waters.
                                if n_resi == 1 and n_at > 5:
                                    mol_ligB = system_B.getMolecule(k)
                                else:
                                    pass
                            
                            # Align ligand2 on ligand1
                            print(f"Mapping and aligning {ligA} and {ligB} for complex...")
                            com_mapping = BSS.Align.matchAtoms(mol_ligA, mol_ligB, complete_rings_only=True)
                            inv_com_mapping = {v: k for k, v in com_mapping.items()}
                            
                            
                            mol_ligB_a = BSS.Align.rmsdAlign(mol_ligB, mol_ligA, inv_com_mapping)
                            
                            # Generate merged molecule.
                            print("Merging..")
                            mol_merged_ligs = BSS.Align.merge(mol_ligA, mol_ligB_a, com_mapping)

                            system_A.removeMolecules(mol_ligA)
                            system_A.addMolecules(mol_merged_ligs)
                            com_sys = system_A
                            com_path=f"{args.output}/{tran}/template/com"
                            if not os.path.exists(com_path):
                                os.makedirs(com_path)
                            
                            if not os.path.exists(f"{com_path}/min"):
                                BSS.FreeEnergy.Relative(com_sys, min_protocol, engine="gromacs", work_dir=com_path + "/min")
                            if not os.path.exists(f"{com_path}/nvt"):
                                BSS.FreeEnergy.Relative(com_sys, nvt_protocol, engine="gromacs", work_dir=com_path + "/nvt")
                            if not os.path.exists(f"{com_path}/npt"):
                                BSS.FreeEnergy.Relative(com_sys, npt_protocol, engine="gromacs", work_dir=com_path + "/npt")
                            if not os.path.exists(f"{com_path}/pro"):
                                BSS.FreeEnergy.Relative(com_sys, pro_protocol, engine="gromacs", work_dir=com_path + "/pro")
                                
                            if not os.path.exists(f"{com_path}/submit_slurm.sh"):
                                fh = open(f"{com_path}/submit_slurm.sh","w")
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

NLAM=%i
"""%(tran,num_lambda))
                                fh.write(
                            """
DLAM=$(bc -l <<< "1./(${NLAM}-1)")
FLAM=$(printf "%.4f" ${DLAM})
LAMS=($( for i in $(seq ${NLAM}); do printf " %.4f" $(bc -l <<< "($i-1.)/(${NLAM}-1.)"); done))
steps=(min nvt npt pro)



for i in $(seq 0 $((${#steps[@]}-1)));do
    for ilam in ${LAMS[@]};do
        lam=$(printf "lambda_%s" ${ilam})
        if [ ! -e "${steps[$i]}/${lam}/gromacs.log" ];then
            echo "${steps[$i]}/${lam}/gromacs.log not exist and start running..."
            if [ $i == 0 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            elif [ $i == 1 ];then
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            else
                echo "Running ${steps[$i]}/${lam}"
                ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
            fi
        else 
            value=$(tail -n 2 ${steps[$i]}/${lam}/gromacs.log | head -n 1 |  awk '{print $1}')
            if [[ ${value} != "Finished" ]];then
                echo "${steps[$i]}/${lam}/gromacs.log not finished and start running..."
                if [ $i == 0 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$i]}/${lam}/gromacs.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                elif [ $i == 1 ];then
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                else
                    echo "Running ${steps[$i]}/${lam}"
                    ${LAUNCH} ${GMX} grompp -f ${steps[$i]}/${lam}/gromacs.mdp -c ${steps[$(($i-1))]}/${lam}/gromacs_out.gro -p ${steps[$i]}/${lam}/gromacs.top  -t ${steps[$(($i-1))]}/${lam}/gromacs.cpt -o ${steps[$i]}/${lam}/gromacs.tpr
                    ${LAUNCH} ${GMX} mdrun -ntomp 1 -deffnm ${steps[$i]}/${lam}/gromacs -c ${steps[$i]}/${lam}/gromacs_out.gro
                fi
            else
                echo "${steps[$i]}/${lam} finished"
            fi
            
        fi
    done
    

done



                                """)
                                fh.close()
                    
                    
                            
                        else:
                            raise Exception(f"Either {comA_top} or {comA_gro} or {comB_top} or {comB_gro} not exists!")
                        
                else:
                    raise Exception(f"Either {ligA_top} or {ligA_gro} or {ligB_top} or {ligB_gro} not exists!")    
                    
                if os.path.exists(f"{args.output}/{tran}/template/"):
                    for itrial in range(args.trials):
                        trial_name="t%02d"%(itrial+1)
                        if not os.path.exists(f"{args.output}/{tran}/{trial_name}/"):                        
                            shutil.copytree(f"{args.output}/{tran}/template/", f"{args.output}/{tran}/{trial_name}/")
                        else:
                            
                            if args.types == "RSFE":
                                if not os.path.exists(f"{args.output}/{tran}/{trial_name}/vac"):
                                    shutil.copytree(f"{args.output}/{tran}/template/vac", f"{args.output}/{tran}/{trial_name}/vac")
                                    
                            elif args.types == "RBFE":
                                if not os.path.exists(f"{args.output}/{tran}/{trial_name}/com"):
                                    shutil.copytree(f"{args.output}/{tran}/template/com", f"{args.output}/{tran}/{trial_name}/com")
                
                    
            
    
