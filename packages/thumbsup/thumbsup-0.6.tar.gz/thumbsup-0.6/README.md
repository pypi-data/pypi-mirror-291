# Thumbnail Generator CLI Tool

A command-line interface (CLI) tool for generating thumbnails from video files. The tool allows you to list files in a directory, generate thumbnails for video files, and specify custom frame extraction points.

## Features

- **List Directory Contents**: View detailed information about files and directories.
- **Generate Thumbnails**: Automatically extract frames from video files at specified intervals.
- **Supported Formats**: `.mp4`, `.mov`, `.mkv`.

## Requirements

- Python 3.11+
- OpenCV (cv2) library

## Installation

First, make sure you have Python 3.11+ installed on your system. Then, install the required dependencies:

```bash
pip install thumbsup
```

## Usage

The CLI tool provides several options:

### 1. Listing Directory Contents

You can list the contents of a directory using the `--ls` option:

```bash
thumbsup --ls /path/to/directory
```

### 2. Generating Thumbnails for a Directory of Videos

To generate thumbnails for all supported video files in a directory:

```bash
thumbsup --dir /path/to/videos --format .mp4 .mkv --dest /path/to/output --at 0.25 0.5 0.75
```

- `--dir`: Directory containing video files.
- `--format`: (Optional) Specify file formats to include. Default is `.mp4`.
- `--dest`: (Optional) Output directory where thumbnails will be saved. Default is the current directory.
- `--at`: (Optional) Frame capture points as a percentage of video duration (e.g., 0.25 for 25%).

### 3. Generating Thumbnails for a Single Video File

To generate thumbnails for a specific video file:

```bash
thumbsup --file /path/to/video.mp4 --dest /path/to/output --at 0.1 0.5 0.9
```

- `--file`: Path to the video file.
- `--dest`: (Optional) Output directory where thumbnails will be saved. Default is the current directory.
- `--at`: (Optional) Frame capture points as a percentage of video duration.

### Example Commands

#### List directory contents:

```bash
thumbsup --ls /path/to/directory
```

#### Generate thumbnails for all `.mp4` files in a directory:

```bash
thumbsup --dir /path/to/videos --format .mp4 --dest /path/to/output
```

#### Generate thumbnails for a single video file:

```bash
thumbsup --file /path/to/video.mp4 --dest /path/to/output --at 0.1 0.5 0.9
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
