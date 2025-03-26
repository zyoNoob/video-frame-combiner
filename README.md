# Video Frame Combiner

A Python utility that combines frames from two videos side by side into a single output video. This tool is useful for visual comparison of videos, creating before/after demonstrations, or combining multiple camera angles.

## Features

- Combine two videos horizontally into a single output video
- Handle videos with different heights by resizing while maintaining aspect ratio
- Handle videos with different frame rates with intelligent frame sampling
- Specify the number of frames to process or use the shorter video's length
- User-friendly prompts for choosing which video's dimensions and frame rate to use
- Clear visual output with frames displayed side by side

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

## Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd video-frame-combiner
   ```

2. Install the required dependencies:

   ```bash
   uv sync
   ```

## Usage

Run the script from the command line with the following arguments:

```bash
python main.py video1.mp4 video2.mp4 output.mp4 [num_frames]
```

### Arguments

- `video1`: Path to the first input video file (required)
- `video2`: Path to the second input video file (required)
- `output`: Path to the output video file (required)
- `num_frames`: (Optional) Number of frames to process. If not specified, the script will use the shorter video's length.

### Example

To combine 100 frames from two video files:

```bash
uv run main.py input1.mp4 input2.mp4 combined.mp4 100
```

To combine the entire videos (using the shorter video's length):

```bash
uv run main.py input1.mp4 input2.mp4 combined.mp4
```

## Interactive Features

If the input videos have different heights or frame rates, the script will prompt you to choose which video's properties to use:

- For different heights: Choose which video's height should be used (the other video will be resized with proper aspect ratio)
- For different frame rates: Choose which video's frame rate should be used (frames will be intelligently sampled to maintain synchronization)

## Output

The output is a single video file with frames from both input videos displayed side by side. The quality and format of the output match the input videos.

## Notes

- The script uses the 'mp4v' codec by default, which creates MP4 files
- Videos with extremely different aspect ratios may result in letterboxing
- The frame synchronization works best when the difference in frame rates is not extreme
- The script will stop processing once it reaches the specified number of frames or when either input video ends