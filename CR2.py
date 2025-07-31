import cv2
import numpy as np

def get_predominant_color(image_path):
    """
    Analyzes an image and returns the name of the predominant color,
    excluding white from the predominant calculation if other colors are present.
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

    # IMPORTANT: Tune these ranges carefully for YOUR specific setup!
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
            # A common range for white/light colors: low saturation, high value
            ([0, 0, 180], [179, 40, 255]) # Tuned S_max down slightly for better exclusion
        ],
        "black": [
            # A common range for black/dark colors: low saturation, low value
            ([0, 0, 0], [179, 50, 50])
        ],
        "gray": [
            # Gray: low saturation, mid-range value
            ([0, 0, 50], [179, 50, 180]) # Make sure it doesn't overlap too much with black/white
        ]
    }

    predominant_color = "unknown"
    max_pixels = 0
    # Store counts for all colors, including white, for later comparison
    color_pixel_counts = {}

    # 4. Masking and Counting Pixels for each color
    for color_name, ranges in color_ranges.items():
        total_pixels_for_color = 0
        current_mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)

        for lower_bound, upper_bound in ranges:
            lower = np.array(lower_bound, dtype=np.uint8)
            upper = np.array(upper_bound, dtype=np.uint8)
            mask_segment = cv2.inRange(hsv_image, lower, upper)
            current_mask = cv2.bitwise_or(current_mask, mask_segment)

        count = cv2.countNonZero(current_mask)
        color_pixel_counts[color_name] = count

    # 5. Determine Predominant Color, EXCLUDING White if other colors are significant
    # First, find the max among non-white colors
    for color_name, count in color_pixel_counts.items():
        if color_name != "white" and count > max_pixels:
            max_pixels = count
            predominant_color = color_name

    # If no significant non-white color was found, and white itself is predominant
    # (i.e., the white background dominates and no colored object is clearly detected),
    # then report white. Otherwise, stick with the detected color or 'unknown'.
    # A threshold (e.g., 500 pixels) can prevent small specks from being classified.
    if max_pixels == 0 and color_pixel_counts.get("white", 0) > (image.shape[0] * image.shape[1] * 0.5): # If white covers >50% of image
        predominant_color = "white"
    elif max_pixels < (image.shape[0] * image.shape[1] * 0.01): # If the "predominant" color is less than 1% of the image, it's probably noise
         predominant_color = "unknown (low confidence)"


    # Optional: Display the original image and the masks for debugging
    # cv2.imshow("Original Image", image)
    # for color_name, mask in debug_masks.items():
    #     cv2.imshow(f"Mask for {color_name}", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    return predominant_color

if __name__ == "__main__":
   
    test_images = [
        "red.jpg",
        "blue.jpg",
        "white.jpg", # Test with a pure white image
        "yellow.jpg",
        "green.jpg",
        "black.jpg",    
    ]

    print("--- Predominant Color Detection (Excluding White) ---")
    for img_path in test_images:
        pred_color = get_predominant_color(img_path)
        if pred_color:
            print(f"Image: {img_path} -> Predominant Color: {pred_color.upper()}")
        print("-" * 30)

    print("\nTip: Adjust HSV color ranges in the script for better accuracy with your specific bottle caps and lighting.")
    print("Especially tune the 'white' range to accurately capture your background.")