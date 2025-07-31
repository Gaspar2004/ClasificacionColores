import cv2
import numpy as np

def get_predominant_color(image_path):
    """
    Analyzes an image and returns the name of the predominant color.
    Assumes a fixed set of common color ranges for bottle caps.
    """
    # 1. Load the Image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return None

    # Resize for faster processing if images are very large (optional)
    # image = cv2.resize(image, (600, 400))

    # 2. Convert to HSV Color Space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 3. Define Color Ranges (in HSV)
    # These ranges are approximate and might need tuning based on your specific caps and lighting.
    # Hue (H): 0-179 (OpenCV's H range)
    # Saturation (S): 0-255 (how vivid the color is)
    # Value (V): 0-255 (how bright the color is)

    color_ranges = {
        "red": [
            ([0, 100, 100], [10, 255, 255]),      # Lower red
            ([170, 100, 100], [179, 255, 255])    # Upper red
        ],
        "green": [
            ([40, 40, 40], [80, 255, 255])
        ],
        "blue": [
            ([100, 100, 100], [130, 255, 255])
        ],
        "yellow": [
            ([20, 100, 100], [35, 255, 255])
        ],
        "orange": [
            ([10, 100, 100], [25, 255, 255])
        ],
        "purple": [
            ([130, 50, 50], [160, 255, 255])
        ],
        "white": [
            ([0, 0, 180], [179, 50, 255]) # Low Saturation, High Value
        ],
        "black": [
            ([0, 0, 0], [179, 50, 50]) # Low Saturation, Low Value
        ]
    }

    predominant_color = "unknown"
    max_pixels = 0
    debug_masks = {} # For visualization

    # 4. Masking and Counting Pixels for each color
    for color_name, ranges in color_ranges.items():
        total_pixels_for_color = 0
        current_mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8) # Start with a black mask

        for lower_bound, upper_bound in ranges:
            lower = np.array(lower_bound, dtype=np.uint8)
            upper = np.array(upper_bound, dtype=np.uint8)

            # Create mask for the current sub-range
            mask_segment = cv2.inRange(hsv_image, lower, upper)
            current_mask = cv2.bitwise_or(current_mask, mask_segment) # Combine masks if multiple ranges

        # Count non-zero (white) pixels in the combined mask
        count = cv2.countNonZero(current_mask)
        total_pixels_for_color += count
        debug_masks[color_name] = current_mask # Store for debugging

        # 5. Determine Predominant Color
        if total_pixels_for_color > max_pixels:
            max_pixels = total_pixels_for_color
            predominant_color = color_name

    # Optional: Display the original image and the masks for debugging
    # cv2.imshow("Original Image", image)
    # for color_name, mask in debug_masks.items():
    #     cv2.imshow(f"Mask for {color_name}", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    return predominant_color

if __name__ == "__main__":
    # Test with some example images
    test_images = [
        "red.jpg",   # Make sure these images exist in the same directory
        "blue.jpg",
        "yellow.jpg",
        "green.jpg",
        "orange.jpg",
        "white.jpg",
        "black.jpg"
    ]

    print("--- Predominant Color Detection ---")
    for img_path in test_images:
        pred_color = get_predominant_color(img_path)
        if pred_color:
            print(f"Image: {img_path} -> Predominant Color: {pred_color.upper()}")
        print("-" * 30)

    print("\nTip: Adjust HSV color ranges in the script for better accuracy with your specific bottle caps and lighting.")