# Script archive 

## Wechat sticker download (MAC)

## Image to GIF/Video Converter

This script allows you to create either a GIF or an MP4 video from a series of images in a specified directory.

### Prerequisites

Before running the script, ensure you have the following libraries installed:

```
pip install opencv-python imageio tqdm
```

### Usage

Run the script from the command line with various arguments to control its behavior.

#### Basic Syntax

```
python script/moving_image_generator.py [arguments]
```

#### Arguments

- `-dir` or `--directory`: Directory containing the image files (required)
- `-out` or `--output`: Filename for the output GIF or video (optional, default: 'output.gif' or 'output.mp4')
- `-outdir` or `--outputdir`: Output directory to save the GIF or video (optional, default: current directory)
- `-int` or `--interval`: Time interval between images in milliseconds (optional, will prompt if not provided)
- `-sort` or `--sortby`: Sort images by 'name' or 'time' (optional, default: 'name')
- `-type` or `--outputtype`: Output type: 'gif' or 'video' (optional, default: 'gif')

#### Examples

1. Create a GIF from images in a directory:

   ```
   python script/moving_image_generator.py -dir /path/to/images -out my_animation.gif -int 100
   ```

2. Create an MP4 video from images:

   ```
   python script/moving_image_generator.py -dir /path/to/images -out my_video.mp4 -type video -int 50
   ```

3. Sort images by modification time and create a GIF:

   ```
   python script/moving_image_generator.py -dir /path/to/images -sort time -int 200
   ```

4. Specify an output directory:

   ```
   python script/moving_image_generator.py -dir /path/to/images -outdir /path/to/output -out animation.gif
   ```

#### Notes

- If you don't provide the output filename, the script will use 'output.gif' for GIFs or 'output.mp4' for videos.
- The script will automatically add the correct file extension (.gif or .mp4) if it's not included in the output filename.
- If you don't specify the interval, the script will prompt you to enter it.
- The script supports PNG, JPG, and JPEG image formats.
- Progress bars will show the status of image processing and video creation.

### Troubleshooting

- Ensure all required libraries are installed.
- Check that the specified image directory exists and contains supported image files.
- Verify that you have write permissions in the output directory.
- If creating a video, make sure your system has the necessary codecs installed.