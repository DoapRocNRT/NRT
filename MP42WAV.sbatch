#!/bin/sh
#SBATCH --partition=gpu --gres=gpu:1 --mem-per-cpu=6000 --time=01:0:00 --output=m2w.out
 
module load ffmpeg/2.2.1/b1

python MP42WAV.py