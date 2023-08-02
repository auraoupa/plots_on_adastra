#!/bin/bash
#SBATCH -J plotse36
#SBATCH --nodes=1
#SBATCH --ntasks=15
#SBATCH --time=00:30:00
#SBATCH -e plotse36.e%j
#SBATCH -o plotse36.o%j
#SBATCH --constraint=HPDA
#SBATCH --account=gda2307
#SBATCH --exclusive

source /lus/home/NAT/gda2307/aalbert/.bashrc
load_conda

conda activate plots

cd /lus/work/NAT/gda2307/aalbert/DEV/git/plots_on_adastra
python init_abort_eORCA36_temp-salt_sections.py
