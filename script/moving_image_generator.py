import cv2
import imageio
import argparse
import os
from tqdm import tqdm

def create_media_from_images(folder_path, output_path, duration_ms, sort_by, output_type):
    images = []
    # List all files in the directory and sort them
    if sort_by == "name":
        image_files = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        files = sorted(
            image_files,
            key=lambda x: int(os.path.splitext(os.path.basename(x))[0])
        )
    elif sort_by == "time":
        files = sorted(
            [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg'))],
            key=os.path.getmtime
        )
    
    for filename in tqdm(files, desc="Processing images"):
        # Read each image with OpenCV
        img = cv2.imread(filename)
        if img is not None:
            # Convert from BGR to RGB for GIF, keep as BGR for video
            if output_type == 'gif':
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images.append(img)
        else:
            print(f"Failed to load image at {filename}")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if output_type == 'gif':
        # Convert duration from ms to seconds for imageio
        duration_s = duration_ms / 1000.0
        # Create the GIF using imageio
        imageio.mimsave(output_path, images, duration=duration_s)
        print(f"GIF created successfully and saved to {output_path}")
    elif output_type == 'video':
        # Get the dimensions of the first image
        height, width, layers = images[0].shape
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 1000.0/duration_ms, (width, height))
        
        for image in tqdm(images, desc="Writing video frames"):
            out.write(image)
        
        out.release()
        print(f"Video created successfully and saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GIF or video from images in a specified directory.")
    parser.add_argument('-dir', '--directory', type=str, help="Directory containing image files")
    parser.add_argument('-out', '--output', type=str, help="Filename for the output GIF or video")
    parser.add_argument('-outdir', '--outputdir', type=str, default='./', help="Output directory to save the GIF or video")
    parser.add_argument('-int', '--interval', type=int, help="Time interval between images in milliseconds")
    parser.add_argument('-sort', '--sortby', type=str, choices=['name', 'time'], default='name', help="Sort images by 'name' or 'time'")
    parser.add_argument('-type', '--outputtype', type=str, choices=['gif', 'video'], default='gif', help="Output type: 'gif' or 'video'")
    
    args = parser.parse_args()

    # Directory handling
    if args.directory:
        folder_path = args.directory
    else:
        print("No directory specified")
        folder_path = input("Please enter the image directory: ")

    # Output filename handling
    if args.output:
        output_filename = args.output
    else:
        output_filename = 'output.gif' if args.outputtype == 'gif' else 'output.mp4'
    
    # Ensure correct file extension
    if args.outputtype == 'gif' and not output_filename.lower().endswith('.gif'):
        output_filename += '.gif'
    elif args.outputtype == 'video' and not output_filename.lower().endswith('.mp4'):
        output_filename += '.mp4'
    
    # Combine output directory and filename
    output_path = os.path.join(args.outputdir, output_filename)

    # Interval handling
    if args.interval:
        duration_ms = args.interval
    else:
        duration_ms = int(input("Please specify the time interval between images in milliseconds: "))

    # Sort argument handling
    sort_by = args.sortby

    create_media_from_images(folder_path, output_path, duration_ms, sort_by, args.outputtype)