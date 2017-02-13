'''Find all the mp4 in folder and transform them into WAV'''

import glob
import subprocess
import os

# Get all mp4 files
mp4_list = glob.glob("*.mp4")

# Create a folder to keep wave files
os.mkdir('wav')

# Create command for transformation
for i in mp4_list:
	command = ('ffmpeg -i '+ i + ' -ac 1 -ar 11025 -vn ' +'wav/'+ i[:-3] + 'wav')
	subprocess.call(command, shell=True)
