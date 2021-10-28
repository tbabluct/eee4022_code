#!/bin/sh

# This example submission script contains several important directives, please examine it thoroughly

# Do not put spaces between the start of the line and #SBATCH, the line must start exactly with #SBATCH, no spaces.
# Do not put spaces between the # and SBATCH

# The line below indicates which accounting group to log your job against
#SBATCH --account=aru

# The line below selects the group of nodes you require
#SBATCH --partition=a100

# The line below reserves 1 worker node and 40 cores
#SBATCH --nodes=1 --ntasks=4

# The line below indicates the wall time your job will need, 10 hours for example. NB, this is a mandatory directive!
#SBATCH --time=6:00:00

# A sensible name for your job, try to keep it short
#SBATCH --job-name="georg_p2p_2"

#Modify the lines below for email alerts. Valid type values are NONE, BEGIN, END, FAIL, REQUEUE, ALL 
#SBATCH --mail-user=bbltor001@myuct.ac.za
#SBATCH --mail-type=BEGIN,END,FAIL

# The cluster is configured primarily for OpenMPI and PMI. Use srun to launch parallel jobs if your code is parallel aware.
# To protect the cluster from code that uses shared memory and grabs all available cores the cluster has the following 
# environment variable set by default: OMP_NUM_THREADS=1
# If you feel compelled to use OMP then uncomment the following line:
# export OMP_NUM_THREADS=$SLURM_NTASKS

# NB, for more information read https://computing.llnl.gov/linux/slurm/sbatch.html

# Use module to gain easy access to software, typing module avail lists all packages.
# Example:
# module load python/anaconda-python-3.7

# If your code is capable of running in parallel and requires a command line argument for the number of cores or threads such as -n 30 or -t 30 then you can link the reserved cores to this with the $SLURM_NTASKS variable for example -n $SLURM_NTASKS instead of -n 30

# GPU Stuff
#SBATCH --gres=gpu:a100-2g-10gb:1

#Last line after all #SBATCH directives !!!
CUDA_VISIBLE_DEVICES=$(ncvd)

# Your science stuff goes here...

# Change path
PATH=$PATH:/home/bbltor001/.local/bin
#load python executables
module load python/anaconda-python-3.7
source activate pytorch3
export PYTHONPATH=/home/bbltor001/.conda/envs/pytorch3/lib/python3.9/site-packages/
# Run python training script
python /home/bbltor001/pytorch-CycleGAN-and-pix2pix/train.py --display_id -1 --model pix2pix --checkpoints_dir /scratch/bbltor001/checkpoints --dataroot /home/bbltor001/datasets/georg/ --name georg_pix2pix_1

