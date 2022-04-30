#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=7:10:00
#SBATCH --mem=4GB
#SBATCH --job-name=data_extraction
##SBATCH --mail-type=END
##SBATCH --mail-user=mdabdullahal.alamin@ucalgary.ca
#SBATCH --output=job_output/Data_extraction_job_%j.txt
echo Job started
date
echo $1
echo $2
echo "========================================================================= "

7zz x $1 -o$2
echo Job ended
date

