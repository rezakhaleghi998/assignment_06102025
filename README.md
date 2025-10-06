## Tech Stack

### Frontend
- HTML5: Structure and content
- CSS3: Styling and animations
- JavaScript (Vanilla): Client-side logic and API calls
- Fetch API: Backend communication

### Backend
- FastAPI: Modern Python web framework
- OpenCV: Image processing library
- NumPy: Numerical computing
- Pillow: Image I/O operations
- Uvicorn: ASGI server
- Docker: Containerization

### Deployment
- Frontend: GitHub Pages
- Backend: Hugging Face Spaces (Docker)

## Local Development

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git
- Modern web browser

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python app.py
   ```

   Or using uvicorn:
   ```bash
   uvicorn app:app --reload --port 7860
   ```

4. Verify it's running:
   - Open `http://localhost:7860` in browser
   - You should see API information

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the frontend:

   Using Python:
   ```bash
   python -m http.server 8000
   ```

   Using Node.js:
   ```bash
   npx serve
   ```

3. Open browser:
   - Navigate to `http://localhost:8000`
   - Test the application with sample images


## Usage Guide

### Step-by-Step Instructions

1. **Upload Image:**
   - Click the upload area or drag & drop
   - Select a medical image (JPG/PNG)
   - Original image preview appears

2. **Select Phase:**
   - Click "Arterial Phase" for contrast enhancement
   - Click "Venous Phase" for smoothing/blur
   - Selected option highlights

3. **Process:**
   - Click "Process Image" button
   - Wait for processing (usually 1-3 seconds)
   - Processed image appears on right

4. **Compare:**
   - View original (left) vs processed (right)
   - Analyze the differences
   - Upload new image to try again

### Image Processing Details

#### Arterial Phase (Contrast Enhancement)
- **Algorithm**: CLAHE (Contrast Limited Adaptive Histogram Equalization)
- **Color Space**: LAB
- **Parameters**: Clip Limit: 3.0, Tile Grid Size: 8×8
- **Use Case**: Enhance vessel visibility, improve contrast

#### Venous Phase (Gaussian Smoothing)
- **Algorithm**: Gaussian Blur
- **Kernel Size**: 15×15
- **Use Case**: Reduce noise, smooth details

## API Documentation

### Endpoints

#### `GET /`
Health check and API information

**Response:**
```json
{
  "status": "online",
  "service": "MedTech Image Processing API",
  "version": "1.0.0"
}
```

#### `POST /process`
Process medical image with specified phase

**Parameters:**
- `image` (file): Image file (multipart/form-data)
- `phase` (string): Either `"arterial"` or `"venous"`

**Response:**
- Content-Type: `image/png`
- Body: Processed image binary data

**Error Responses:**
- `400`: Invalid file type or phase parameter
- `500`: Processing error

## Project Structure

```
assignment/
├── frontend/
│   └── index.html              # Complete frontend application
│
├── backend/
│   ├── app.py                  # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container configuration
│   └── README.md               # Backend documentation
│
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## Testing

### Manual Testing

**Upload Functionality:**
- Upload JPG image
- Upload PNG image
- Drag and drop image
- Invalid file type shows error

**Phase Selection:**
- Arterial phase selects correctly
- Venous phase selects correctly
- Visual feedback on selection

**Processing:**
- Arterial phase increases contrast
- Venous phase applies blur
- Loading indicator appears
- Success message displays
- Error handling works

**Display:**
- Original image shows on left
- Processed image shows on right
- Responsive on mobile

### API Testing

```bash
# Test arterial phase
curl -X POST "http://localhost:7860/process" \
  -F "image=@test_image.jpg" \
  -F "phase=arterial" \
  --output arterial_result.png

# Test venous phase
curl -X POST "http://localhost:7860/process" \
  -F "image=@test_image.jpg" \
  -F "phase=venous" \
  --output venous_result.png
```

## License

This project is created for educational purposes.

## Troubleshooting

### Common Issues

**Problem**: "Failed to fetch" error
- **Solution**: Ensure backend is running and API_URL is correct

**Problem**: CORS error in browser console
- **Solution**: Backend CORS settings allow your frontend domain

**Problem**: Image not processing
- **Solution**: Check file format (JPG/PNG only), verify backend logs

**Problem**: GitHub Pages not working
- **Solution**: Ensure Pages is enabled, check files are in correct path

**Problem**: Hugging Face Space build fails
- **Solution**: Check Dockerfile syntax, verify all files are pushed
