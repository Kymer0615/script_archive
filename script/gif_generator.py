import cv2
import imageio
import argparse
import os
from tqdm import tqdm

def create_gif_from_images(folder_path, output_path, duration_ms):
    images = []
    # List all files in the directory and sort them
    files = sorted([os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg'))])
    
    for filename in tqdm(files, desc="Processing images"):
        # Read each image with OpenCV
        img = cv2.imread(filename)
        if img is not None:
            # Convert from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images.append(img)
        else:
            print(f"Failed to load image at {filename}")
    
    # Convert duration from ms to seconds for imageio
    duration_s = duration_ms / 1000.0
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create the GIF using imageio
    imageio.mimsave(output_path, images, duration=duration_s)
    print(f"GIF created successfully and saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GIF from images in a specified directory.")
    parser.add_argument('-dir', '--directory', type=str, help="Directory containing image files")
    parser.add_argument('-out', '--output', type=str, help="Filename for the output GIF")
    parser.add_argument('-outdir', '--outputdir', type=str, default='./', help="Output directory to save the GIF")
    parser.add_argument('-int', '--interval', type=int, help="Time interval between images in milliseconds")
    
    args = parser.parse_args()

    # Directory handling
    if args.directory:
        folder_path = args.directory
    else:
        print("No directory specified")
        folder_path = input("Please enter the image directory: ")

    # Output filename handling
    if args.output:
        if "gif" not in args.output.lower():
            output_filename = args.output + ".gif"
        else:
            output_filename = args.output
    else:
        output_filename = 'output.gif'  # Default filename if not specified
    
    # Combine output directory and filename
    output_path = os.path.join(args.outputdir, output_filename)

    # Interval handling
    if args.interval:
        duration_ms = args.interval
    else:
        duration_ms = int(input("Please specify the time interval between images in milliseconds: "))

    create_gif_from_images(folder_path, output_path, duration_ms)
