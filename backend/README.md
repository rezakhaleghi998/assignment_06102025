# MedTech Image Processing Backend

FastAPI-based backend service for processing medical images with arterial and venous phase filters.

## Features

- **Arterial Phase Processing**: CLAHE-based contrast enhancement for improved visibility
- **Venous Phase Processing**: Gaussian smoothing/blur for noise reduction
- **RESTful API**: Simple POST endpoint for image processing
- **CORS Enabled**: Works with frontend hosted on GitHub Pages
- **Docker Ready**: Containerized for easy deployment on Hugging Face Spaces

## API Endpoints

### `POST /process`

Process a medical image with specified phase filter.

**Parameters:**
- `image` (file): Medical image file (JPG/PNG)
- `phase` (form): Processing phase - `"arterial"` or `"venous"`

**Response:**
- Processed image as PNG

**Example using curl:**
```bash
curl -X POST "http://localhost:7860/process" \
  -F "image=@sample.jpg" \
  -F "phase=arterial" \
  --output processed.png
```

### `GET /`

Health check and API information.

### `GET /health`

Detailed health check with library versions.

## Local Development

### Prerequisites
- Python 3.10+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The API will be available at `http://localhost:7860`

### Using uvicorn directly:
```bash
uvicorn app:app --reload --port 7860
```

## Docker Deployment

### Build locally:
```bash
docker build -t medtech-backend .
docker run -p 7860:7860 medtech-backend
```

## Hugging Face Spaces Deployment

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Docker** as the SDK
3. Clone the Space repository:
```bash
git clone https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME
```

4. Copy backend files:
```bash
cp app.py Dockerfile requirements.txt YOUR-SPACE-NAME/
cd YOUR-SPACE-NAME
```

5. Commit and push:
```bash
git add .
git commit -m "Initial commit"
git push
```

6. Your Space will automatically build and deploy at:
   `https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space`

## Image Processing Details

### Arterial Phase (Contrast Enhancement)
- Uses CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Operates in LAB color space for better results
- Parameters: `clipLimit=3.0`, `tileGridSize=(8,8)`

### Venous Phase (Gaussian Smoothing)
- Applies Gaussian blur with 15x15 kernel
- Reduces noise and smooths fine details
- Simulates venous phase imaging characteristics

## Tech Stack

- **FastAPI**: Modern Python web framework
- **OpenCV**: Image processing library
- **NumPy**: Numerical computing
- **Pillow**: Image I/O
- **Uvicorn**: ASGI server

## Error Handling

The API includes comprehensive error handling:
- Invalid file types → 400 Bad Request
- Invalid phase parameter → 400 Bad Request
- Processing errors → 500 Internal Server Error

## CORS Configuration

CORS is configured to accept requests from:
- GitHub Pages (`*.github.io`)
- Localhost (development)
- All origins (can be restricted for production)

## Testing

Test the API with sample medical images:

```python
import requests

url = "http://localhost:7860/process"
files = {"image": open("sample.jpg", "rb")}
data = {"phase": "arterial"}

response = requests.post(url, files=files, data=data)

with open("output.png", "wb") as f:
    f.write(response.content)
```

## License

This project is created for educational purposes.
