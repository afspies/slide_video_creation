import moviepy.editor as mpe
import imageio
import os
import numpy as np
from PIL import Image
from tqdm import tqdm

# ----------------------------
# Configuration
speaker = 'david'

# The Recording containing the slides somewhere
filename = f"./seminars/{speaker}/talk.mp4"
# Pixel region in the recording where the slides are visible
video_region = ((428,641),(9,388))
# The directory containing JPGs of the slides (e.g. exported from .ppt)
slide_ims_dir = f'./seminars/{speaker}/slide_jpgs'
# ----------------------------

video = mpe.VideoFileClip(filename)
total_frames = video.duration*video.fps

w = video_region[0][1] - video_region[0][0]
h = video_region[1][1] - video_region[1][0]

slide_nums = list(sorted(map(lambda x: int(x.split('.')[0][5:]), os.listdir(slide_ims_dir))))

slide_arr = np.zeros((len(slide_nums), w, h, 3), dtype=np.uint8)
# slide_arr = np.zeros((len(slide_nums), 1080, 1920, 3), dtype=np.uint8)
for slide_num in slide_nums :
    file_name = f'./{slide_ims_dir}/Slide{slide_num}.jpeg'
    # file_name = f'./{slide_ims_dir}/{slide_num:0004}.jpg'
    im = imageio.imread(file_name, pilmode='RGB')
    im = np.array(Image.fromarray(im).resize((h, w), resample=Image.NEAREST))
    # im = np.array(Image.fromarray(im).resize((1920, 1080), resample=Image.NEAREST))
    slide_arr[slide_num-1] = im
slide_arr = slide_arr #[:, 00:800, 00:800]


def find_matching_slide(curr_frame, prev_slide, slide_arr, neighbors):
    curr_frame = curr_frame[video_region[0][0]:video_region[0][1],video_region[1][0]:video_region[1][1]] #[000:800, 000:800]
    prev_slide = prev_slide - 1
    best_match_val = -10
    best_match = 0
    for offset in sorted(np.arange(-neighbors, neighbors+1), key=lambda x: abs(x)):
        if not (0 <= prev_slide+offset < len(slide_arr)):
            continue
        slide = slide_arr[prev_slide + offset]
        dist = np.sum((slide - np.mean(slide)) * (curr_frame - np.mean(curr_frame)) ) / ((slide.size - 1) * np.std(slide) * np.std(curr_frame))
        if dist > best_match_val:
            best_match = prev_slide + offset + 1
            best_match_val = dist
    return best_match


matched_slide = 1
slide_assignments = np.zeros((int(video.duration)+100, 2), dtype=np.uint32)
frame = 0
pbar = tqdm(total=total_frames//video.fps)
for frame_num, frame in enumerate(video.iter_frames()):
    if frame_num % video.fps != 0:
        continue
    second = int(frame_num / video.fps)
    matched_slide  = find_matching_slide(frame, matched_slide, slide_arr, 8)
    slide_assignments[second] = [frame_num, matched_slide]
    # if int(second) % 60 == 0:
    #     print(int(second)//60, " minutes passed")
    pbar.update(1)
np.save(f'./seminars/{speaker}/slide_assignments.npy', slide_assignments)
