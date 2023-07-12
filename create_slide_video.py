import numpy as np
from moviepy.editor import *
import imageio
import os
import numpy as np
from PIL import Image

speaker = "david"
data = np.load(f'./seminars/{speaker}/slide_assignments.npy')
slide_ims_dir = f'seminars/{speaker}/slide_jpgs'

transitions = [[0,0]]
for interval in data:
    if interval[1] == transitions[-1][1]:
        transitions[-1][0] += 25
    else:
        transitions.append([25, interval[1]])

slide_nums = list(sorted(map(lambda x: int(x.split('.')[0][5:]), os.listdir(slide_ims_dir))))

slide_arr = np.zeros((len(slide_nums), 1080, 1920, 3), dtype=np.uint8)

for slide_num in slide_nums :
    file_name = f'./{slide_ims_dir}/Slide{slide_num}.jpeg'
    im = imageio.imread(file_name, pilmode='RGB')
    im = np.array(Image.fromarray(im))#
    slide_arr[slide_num-1] = im

num_transitions = len(transitions)
rows = int(num_transitions ** 0.5)+1
cols = rows

clips = []
for i, (duration, frame_id) in enumerate(transitions):
    if frame_id == 0:
        continue
    else:
        frame_id = frame_id - 1

    clips.append(ImageClip(slide_arr[frame_id], duration=duration//25))

presentation = ()

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile(f"seminars/{speaker}/slide_video_created.mp4", fps=25, threads = 12, audio=False)


# # Try with masking to see if faster
# target_h = int(1080*(371/180))
# target_w = int(1920*(371/180)) # Will need the mask to chop this

# import numpy as np
# duration =  5.0
# mask = np.ones((target_w, target_h), dtype=np.bool)
# mask[-661:, :371] = False
# def make_frame(t):
#     return mask


# src_clip = VideoFileClip("jakob foerster/GMT20220217-123433_Recording_1920x1080.mp4",
#                             audio=True,
#                             target_resolution=((target_w, target_h)))

# src_w, src_h = src_clip.size
# fps, whole_duration = (src_clip.fps, src_clip.duration)

# mask_clip = VideoClip(make_frame, duration=1, ismask=True )

# print(f"mask info {mask_clip.size, mask_clip.duration}, \
#         src  info {src_clip.size, src_clip.duration, src_clip.fps}")
# # src_clip.set_mask(mask_clip)
# # print(1600+(sv_w-w_before_upscale), src_w, sv_h)

# speaker_video = (src_clip
#                     .subclip(0.0, duration)
#                     .set_mask(mask_clip)
# )
