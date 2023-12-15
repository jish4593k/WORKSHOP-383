import argparse
import os
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog

def trim_video(input_path, output_path, fps, speed):
    cap = cv2.VideoCapture(input_path)
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculate new frame count based on speed
    new_frame_count = int(frame_count / speed)

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Read and write frames with adjusted speed
    for _ in range(new_frame_count):
        ret, frame = cap.read()
        if ret:
            
           
            tensor_frame = transforms.ToTensor()(frame)
            
          
            tensor_frame = torch.flip(tensor_frame, [0])  # Flip vertically

          
            processed_frame = (tensor_frame.numpy() * 255).astype(np.uint8)

            out.write(processed_frame)
        else:
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    args = collect_args()
    input_path = args['path']
    fps = args['fps']
    speed = args['speed'] if args['speed'] else 1.0

    output_directory = os.path.join(os.path.dirname(input_path), f"{fps}_output")
    output_path = os.path.join(output_directory, os.path.basename(input_path))

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    trim_video(input_path, output_path, fps, speed)

def collect_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--speed", type=int)
    return vars(parser.parse_args())

class VideoProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Video Processor")

        self.choose_directory_button = tk.Button(master, text="Choose Directory", command=self.choose_directory)
        self.choose_directory_button.pack()

        self.process_button = tk.Button(master, text="Process Videos", command=self.process_videos)
        self.process_button.pack()

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.process_directory(directory)

    def process_videos(self):
        directory = filedialog.askdirectory()
        if directory:
            self.process_directory(directory)

    def process_directory(self, directory):
        processor = VideoProcessor(directory, ".mp4", 30, 2.0)
        processor.process_files()

if __name__ == "__main__":
    main()
