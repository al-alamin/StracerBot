#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --mem=1GB
#SBATCH --job-name=alamin_assignment_4_job
##SBATCH --mail-type=END
##SBATCH --mail-user=mdabdullahal.alamin@ucalgary.ca
#SBATCH --output=alamin_assigngment4_job_%j.txt
echo Hello World 1
sleep 2m
echo Hello world 2