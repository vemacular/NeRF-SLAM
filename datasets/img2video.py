import cv2
import os
import re
from pathlib import Path 

def extract_number(filename):
    match = re.search(r'\d+',filename.name)
    if match:
        return int(match.group())
    return 0
def img2video(imgfloder:Path, est:bool = True, ref:bool = True):
    est_images = []
    ref_image = []

    for img in imgfloder.iterdir():
        if img.name.startswith('est'):
            est_images.append(imgfloder / img)
        elif img.name.startswith('ref'):
            ref_image.append(imgfloder / img)
    est_images = sorted(est_images,key=extract_number)
    ref_image = sorted(ref_image,key=extract_number)
    h,w = cv2.imread(str(est_images[0])).shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    estvideo = cv2.VideoWriter(str(imgfloder / 'est_video.mp4'), fourcc, 10,(w,h))
    refvideo = cv2.VideoWriter(str(imgfloder / 'ref_video.mp4'), fourcc, 10,(w,h))
    for img in est_images:
        ii = cv2.imread(str(img))
        estvideo.write(ii)
    for img in ref_image:
        ii = cv2.imread(str(img))
        refvideo.write(ii)
    estvideo.release()
    refvideo.release()

p = Path('/home/dzt/data/nerf-slam/0804_fullroom/nerf-slam/0804_fullroom/25000')
img2video(p)