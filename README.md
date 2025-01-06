<<<<<<< HEAD
# Pexels Image Downloader

## Description
A Python script to download images from Pexels and automatically package them into a ZIP file. The script handles API requests, image downloads, and ZIP creation with progress indicators.

## Installation

### Prerequisites
- Python 3.8 or higher
- Git (optional)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/[repository-name].git
   cd [repository-name]
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # For Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate

   # For Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Create the api.key file:
   ```bash
   echo "your_pexels_api_key_here" > api.key
   ```
   Replace `your_pexels_api_key_here` with your actual Pexels API key

4. Verify installation:
   ```bash
   python test_api.py
   ```
   If the API key is valid, you should see a success message

## Features
- Search and download images from Pexels
- Download images in original quality
- Automatic ZIP packaging of downloaded images
- Progress indicators for download and ZIP creation
- Comprehensive error handling
- Simple API key management using api.key file

## Usage
```bash
python download.py [query] [number_of_photos] [destination_path]
```

### Arguments
| Argument         | Description                                      | Required |
|------------------|--------------------------------------------------|----------|
| query            | Search term for images                           | Yes      |
| number_of_photos | Number of photos to download (max 80 per search) | Yes      |
| destination_path | Directory to save images (default: current dir)  | No       |

## Examples
```bash
# Download 10 cat images
python download.py cat 10

# Download 20 dog images to specific directory
python download.py dog 20 ~/Pictures

# Download 50 landscape images
python download.py landscape 50
```

## Output Structure
- Downloaded images are saved in: `[destination]/[query]/`
- ZIP files are saved in: `downloads/` directory
- ZIP file naming format: `YYYY-MM-DD_HH-MM-SS_query.zip`

## Error Handling
The script handles:
- Missing or invalid API key
- Network errors
- File system errors
- API rate limits
- Invalid responses
- ZIP creation failures

## Requirements
- Python 3.x
- Internet connection
- Valid Pexels API key

## Notes
- The script will create necessary directories automatically
- If no images are downloaded, no ZIP file will be created
- Progress indicators show both download and ZIP creation progress
- API key is read from `api.key` file in the same directory as the script
=======
# Pexels-mass-image-downloader
Mass image downloader and auto compress to the zip file
>>>>>>> 025c9468ecdbedb1f973aba826d606f51cc3db19
