#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=bigmem
#SBATCH --cpus-per-task=16
#SBATCH --time=150:50:00
#SBATCH --mem=500GB
#SBATCH --job-name=code_tdidf
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=mdabdullahal.alamin@ucalgary.ca
#SBATCH --output=job_output/TDIDF_job_%j.txt

set -e
echo Job started
date
echo $1

echo "========================================================================="

source /global/software/anaconda/anaconda3-2019.10-tensorflowgpu/anaconda3/etc/profile.d/conda.sh
conda activate latest

echo "Necessary env loaded"

echo "Going to create TDIFD from the extracted code segment"


# python ../Scripts/create_tdidf_document.py /work/disa_lab/Alamin/SOTorrent/serverfault/
# python ../Scripts/create_tdidf_document.py /work/disa_lab/Alamin/SOTorrent/askubuntu/
# python ../Scripts/create_tdidf_document.py /work/disa_lab/Alamin/SOTorrent/unix/
# python ../Scripts/create_tdidf_document.py /work/disa_lab/Alamin/SOTorrent/superuser/
python ../Scripts/create_tdidf_document.py /work/disa_lab/Alamin/SOTorrent/SO/
# python ../Scripts/create_tdidf_document.py /work/disa_lab/Alamin/SOTorrent/SO2/

echo Job ended
date