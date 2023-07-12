# ICARL Slide Video Creation Scripts
For a few ICARL talks the recordings of the slides were of low resolution. These scripts can be used to generate a video of the slides, provided that one has:
 1. A video of a talk in which the slides are visible (at a fixed location)
 2. A set of images corresponding to the slides (powerpoint allows easy export), named "Slide1.jpg", "Slide2.jpg", etc.


## Usage
### Scripts
There are two key scripts. The first ```(parse_video.py)``` matches each frame of the video to the corresponding slide image. The second ```(create_slide_video.py)``` creates a video of the slides, using the matched frames and the images of the slides.

For the sake of identifying the relevant pixel region for the slides, the notebook "match_slides.ipynb" exists.

As I am too lazy to use argparse, the speaker names in the scripts need to be changed manually.

### Run Time
For a 1 hour long 1080p video, the run times are approximately:
| Script | Run Time |
| --- | --- |
| parse_video.py | 15 minutes |
| create_slide_video.py | 45 minutes |

### Folder structure
The expected folder structure for use of the directory is:

```
- seminars
    - speaker_name
        - slide_jpgs
            - Slide1.jpg
            - Slide2.jpg
            - ...
        - talk.mp4
- create_slide_video.py
- parse_video.py
- match_slides.ipynb
```

