"""
MedTech Image Processing Backend API
Provides endpoints for processing medical images with arterial and venous phase filters
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MedTech Image Processing API",
    description="Backend API for processing medical images",
    version="1.0.0"
)

# Configure CORS to allow requests from GitHub Pages and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.github.io",
        "http://localhost:*",
        "http://127.0.0.1:*",
        "*"  # Allow all origins for development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def increase_contrast(img: np.ndarray) -> np.ndarray:
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to enhance contrast
    Used for arterial phase processing

    Args:
        img: Input image as numpy array (BGR format)

    Returns:
        Enhanced image as numpy array
    """
    try:
        # Convert to LAB color space for better contrast enhancement
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE to L channel (lightness)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)

        # Merge channels back and convert to BGR
        enhanced_lab = cv2.merge([l_enhanced, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        logger.info("Contrast enhancement applied successfully")
        return enhanced
    except Exception as e:
        logger.error(f"Error in contrast enhancement: {str(e)}")
        raise


def apply_gaussian_blur(img: np.ndarray) -> np.ndarray:
    """
    Apply Gaussian blur for smoothing
    Used for venous phase processing

    Args:
        img: Input image as numpy array (BGR format)

    Returns:
        Blurred image as numpy array
    """
    try:
        # Apply Gaussian blur with 15x15 kernel
        blurred = cv2.GaussianBlur(img, (15, 15), 0)
        logger.info("Gaussian blur applied successfully")
        return blurred
    except Exception as e:
        logger.error(f"Error in Gaussian blur: {str(e)}")
        raise


def read_image_file(file_bytes: bytes) -> np.ndarray:
    """
    Read image file bytes and convert to OpenCV format

    Args:
        file_bytes: Raw image file bytes

    Returns:
        Image as numpy array in BGR format
    """
    try:
        # Convert bytes to PIL Image
        image = Image.open(BytesIO(file_bytes))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert PIL Image to numpy array
        img_array = np.array(image)

        # Convert RGB to BGR for OpenCV
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        logger.info(f"Image loaded successfully: shape={img_bgr.shape}")
        return img_bgr
    except Exception as e:
        logger.error(f"Error reading image file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")


def encode_image(img: np.ndarray) -> bytes:
    """
    Encode OpenCV image to PNG bytes

    Args:
        img: Image as numpy array (BGR format)

    Returns:
        PNG encoded bytes
    """
    try:
        # Encode image to PNG format
        success, buffer = cv2.imencode('.png', img)
        if not success:
            raise Exception("Failed to encode image")

        return buffer.tobytes()
    except Exception as e:
        logger.error(f"Error encoding image: {str(e)}")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "MedTech Image Processing API",
        "version": "1.0.0",
        "endpoints": {
            "/process": "POST - Process medical images with arterial or venous phase filters"
        }
    }


@app.post("/process")
async def process_image(
    image: UploadFile = File(..., description="Medical image file (JPG/PNG)"),
    phase: str = Form(..., description="Processing phase: 'arterial' or 'venous'")
):
    """
    Process medical image with selected phase filter

    Args:
        image: Uploaded image file (JPG/PNG)
        phase: Processing phase - 'arterial' (contrast enhancement) or 'venous' (blur)

    Returns:
        Processed image as PNG
    """
    logger.info(f"Processing request received - Phase: {phase}")

    # Validate phase parameter
    if phase not in ['arterial', 'venous']:
        raise HTTPException(
            status_code=400,
            detail="Invalid phase. Must be 'arterial' or 'venous'"
        )

    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPG/PNG)"
        )

    try:
        # Read uploaded file
        file_bytes = await image.read()
        logger.info(f"File received: {image.filename}, size: {len(file_bytes)} bytes")

        # Convert to OpenCV format
        img = read_image_file(file_bytes)

        # Apply processing based on phase
        if phase == 'arterial':
            processed_img = increase_contrast(img)
            logger.info("Arterial phase processing completed")
        else:  # venous
            processed_img = apply_gaussian_blur(img)
            logger.info("Venous phase processing completed")

        # Encode processed image
        output_bytes = encode_image(processed_img)

        # Return processed image
        return Response(
            content=output_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=processed_{image.filename}",
                "X-Processing-Phase": phase
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "opencv_version": cv2.__version__,
        "numpy_version": np.__version__
    }


if __name__ == "__main__":
    import uvicorn
    # Run server on port 7860 (Hugging Face Spaces default)
    uvicorn.run(app, host="0.0.0.0", port=7860)
