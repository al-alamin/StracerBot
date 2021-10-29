#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=15:10:00
#SBATCH --mem=80GB
#SBATCH --job-name=data_extraction
##SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=mdabdullahal.alamin@ucalgary.ca
#SBATCH --output=job_output/Code_segment_extraction_job_%j.txt
set -e
echo Job started
date
echo $1

echo "========================================================================="

source /global/software/anaconda/anaconda3-2019.10-tensorflowgpu/anaconda3/etc/profile.d/conda.sh
conda activate latest

echo "Necessary env loaded"

echo "Ectract Code segment from CSV file"


# python ../Scripts/extract_code_segment.py /work/disa_lab/Alamin/SOTorrent/serverfault/Posts.csv
# python ../Scripts/extract_code_segment.py /work/disa_lab/Alamin/SOTorrent/askubuntu/Posts.csv
# python ../Scripts/extract_code_segment.py /work/disa_lab/Alamin/SOTorrent/unix/Posts.csv
# python ../Scripts/extract_code_segment.py /work/disa_lab/Alamin/SOTorrent/superuser/Posts.csv
python ../Scripts/extract_code_segment.py /work/disa_lab/Alamin/SOTorrent/SO/Posts.csv

echo Job ended
date