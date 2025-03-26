import cv2
import numpy as np
import sys

# Check if at least the required arguments are provided
if len(sys.argv) < 4:
    print("Usage: python script.py video1 video2 output [num_frames]")
    sys.exit(1)

# Assign input and output paths
video1_path = sys.argv[1]
video2_path = sys.argv[2]
output_path = sys.argv[3]

# Open the video files
cap1 = cv2.VideoCapture(video1_path)
cap2 = cv2.VideoCapture(video2_path)

# Verify that both videos opened successfully
if not cap1.isOpened() or not cap2.isOpened():
    print("Error: Could not open videos")
    sys.exit(1)

# Get frame counts from both videos
frame_count1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
frame_count2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))

# Determine num_frames based on arguments
if len(sys.argv) == 5:
    try:
        num_frames = int(sys.argv[4])
    except ValueError:
        print("Error: num_frames must be an integer")
        sys.exit(1)
else:
    # Use the smaller video's frame count if num_frames is not provided
    num_frames = min(frame_count1, frame_count2)

# Get properties of the first video
width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps1 = cap1.get(cv2.CAP_PROP_FPS)

# Get properties of the second video
width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps2 = cap2.get(cv2.CAP_PROP_FPS)

# Check if heights are different and ask user for preference
if height1 != height2:
    print(f"Videos have different heights: Video 1 = {height1}px, Video 2 = {height2}px")
    choice = input("Which video's height should be used? (1/2): ")
    
    if choice == "1":
        target_height = height1
        # Calculate new width for video 2 to maintain aspect ratio
        new_width2 = int(width2 * (height1 / height2))
        width2 = new_width2
        print(f"Resizing video 2 to height {height1}px (new width: {new_width2}px)")
    elif choice == "2":
        target_height = height2
        # Calculate new width for video 1 to maintain aspect ratio
        new_width1 = int(width1 * (height2 / height1))
        width1 = new_width1
        height1 = height2  # Update height1 to match height2
        print(f"Resizing video 1 to height {height2}px (new width: {new_width1}px)")
    else:
        print("Invalid choice. Using video 1's height as default.")
        target_height = height1
        new_width2 = int(width2 * (height1 / height2))
        width2 = new_width2
else:
    target_height = height1  # Both heights are the same

# Check if the fps values are very different
if abs(fps1 - fps2) > 1.0:
    print(f"Videos have different frame rates: Video 1 = {fps1}fps, Video 2 = {fps2}fps")
    fps_choice = input("Which video's frame rate should be used? (1/2): ")
    
    if fps_choice == "1":
        output_fps = fps1
        fps_ratio = fps2 / fps1  # How many frames of video 2 per frame of video 1
        print(f"Using video 1's frame rate ({fps1}fps) for output")
    elif fps_choice == "2":
        output_fps = fps2
        fps_ratio = fps1 / fps2  # How many frames of video 1 per frame of video 2
        print(f"Using video 2's frame rate ({fps2}fps) for output")
    else:
        print(f"Invalid choice. Using video 1's frame rate ({fps1}fps) as default")
        output_fps = fps1
        fps_ratio = fps2 / fps1
else:
    output_fps = fps1  # Both fps values are close enough
    fps_ratio = 1.0

# Define output video properties
output_width = width1 + width2
output_height = target_height

# Set up the video writer with 'mp4v' codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, output_fps, (output_width, output_height))

# Process frames up to num_frames or until one video ends
i = 0
frame_count1 = 0
frame_count2 = 0
while i < num_frames:
    # Determine which frames to read based on fps ratio
    if abs(fps1 - fps2) > 1.0:
        if output_fps == fps1:
            # Using video 1's frame rate
            ret1, frame1 = cap1.read()
            frame_count1 += 1
            
            # Calculate how many frames of video 2 we should have read by now
            target_frame2 = int(frame_count1 * fps_ratio)
            
            # Skip or reread frames from video 2 to maintain sync
            if target_frame2 > frame_count2:
                # Need to read more frames from video 2 to catch up
                frames_to_read = target_frame2 - frame_count2
                for _ in range(frames_to_read - 1):
                    cap2.read()  # Read and discard frames to catch up
                    frame_count2 += 1
                
                ret2, frame2 = cap2.read()
                frame_count2 += 1
            else:
                # We're ahead on video 2, reuse the last frame
                ret2 = True
        else:
            # Using video 2's frame rate
            ret2, frame2 = cap2.read()
            frame_count2 += 1
            
            # Calculate how many frames of video 1 we should have read by now
            target_frame1 = int(frame_count2 * fps_ratio)
            
            # Skip or reread frames from video 1 to maintain sync
            if target_frame1 > frame_count1:
                # Need to read more frames from video 1 to catch up
                frames_to_read = target_frame1 - frame_count1
                for _ in range(frames_to_read - 1):
                    cap1.read()  # Read and discard frames to catch up
                    frame_count1 += 1
                
                ret1, frame1 = cap1.read()
                frame_count1 += 1
            else:
                # We're ahead on video 1, reuse the last frame
                ret1 = True
    else:
        # Frame rates are similar, read normally
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
    
    # Break if either video ends
    if not ret1 or not ret2:
        break
    
    # Resize frames if necessary
    if height1 != height2:
        if target_height == height1 and frame2.shape[0] != target_height:
            # Resize video 2 to match video 1's height
            frame2 = cv2.resize(frame2, (width2, target_height))
        elif target_height == height2 and frame1.shape[0] != target_height:
            # Resize video 1 to match video 2's height
            frame1 = cv2.resize(frame1, (width1, target_height))
    
    # Concatenate frames horizontally
    concatenated_frame = np.hstack([frame1, frame2])
    out.write(concatenated_frame)
    i += 1

# Release resources
out.release()
cap1.release()
cap2.release()