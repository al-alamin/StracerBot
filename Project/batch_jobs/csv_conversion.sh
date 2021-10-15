#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=20:10:00
#SBATCH --mem=16GB
#SBATCH --job-name=data_extraction
##SBATCH --mail-type=END
##SBATCH --mail-user=mdabdullahal.alamin@ucalgary.ca
#SBATCH --output=job_output/CSV_conversion_job_%j.txt
echo Job started
date
echo $1

echo "========================================================================= "

source /global/software/anaconda/anaconda3-2019.10-tensorflowgpu/anaconda3/etc/profile.d/conda.sh
conda activate latest

echo "Necessary env loaded"

python ../Scripts/csv_conversion.py /work/disa_lab/Alamin/SOTorrent/test/Posts.xml
echo "XML converted to CSV"
# python ../Scripts/csv_conversion.py /work/disa_lab/Alamin/SOTorrent/unix/Posts.xml
python ../Scripts/csv_conversion.py /work/disa_lab/Alamin/SOTorrent/superuser/Posts.xml
python ../Scripts/csv_conversion.py /work/disa_lab/Alamin/SOTorrent/serverfault/Posts.xml
python ../Scripts/csv_conversion.py /work/disa_lab/Alamin/SOTorrent/askubuntu/Posts.xml
python ../Scripts/csv_conversion.py /work/disa_lab/Alamin/SOTorrent/SO/Posts.xml


echo Job ended
date