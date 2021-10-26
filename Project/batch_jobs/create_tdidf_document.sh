#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=23:10:00
#SBATCH --mem=80GB
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

echo Job ended
date