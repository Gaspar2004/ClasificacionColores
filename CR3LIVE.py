import cv2
import numpy as np

def get_predominant_color_from_frame(frame):
    """
    Analyzes an image frame and returns the name of the predominant color,
    excluding white from the predominant calculation if other colors are present.
    Assumes a fixed set of common color ranges for bottle caps.
    """
    if frame is None:
        return None

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_ranges = {
        "red": [([0, 100, 100], [10, 255, 255]), ([170, 100, 100], [179, 255, 255])],
        "green": [([40, 40, 40], [80, 255, 255])],
        "blue": [([100, 100, 100], [130, 255, 255])],
        "yellow": [([20, 100, 100], [35, 255, 255])],
        "orange": [([10, 100, 100], [25, 255, 255])],
        "purple": [([130, 50, 50], [160, 255, 255])],
        "white": [([0, 0, 180], [179, 40, 255])], # Tuned S_max down slightly for better exclusion
        "black": [([0, 0, 0], [179, 50, 50])],
        "gray": [([0, 0, 50], [179, 50, 180])]
    }

    predominant_color = "unknown"
    max_pixels = 0
    color_pixel_counts = {}

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

    # Determine Predominant Color, EXCLUDING White if other colors are significant
    for color_name, count in color_pixel_counts.items():
        if color_name != "white" and count > max_pixels:
            max_pixels = count
            predominant_color = color_name

    frame_area = frame.shape[0] * frame.shape[1] # Use the cropped frame's area
    if max_pixels == 0 and color_pixel_counts.get("white", 0) > (frame_area * 0.5):
        predominant_color = "white (background)" # Clarify it's likely the background
    elif max_pixels < (frame_area * 0.01): # If the "predominant" color is less than 1% of the image, it's probably noise
         predominant_color = "unknown (low confidence)" 

    return predominant_color
"""
if __name__ == "__main__":
    cap = cv2.VideoCapture(0) # 0 is typically the default webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # --- Define the Region of Interest (ROI) for cropping ---
    # These values will need to be adjusted based on your camera's resolution
    # and where the caps appear on your conveyor belt.

    # Get full frame dimensions to help define ROI
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Full Frame Dimensions: {frame_width}x{frame_height}")

    # Example ROI (adjust these values!)
    # roi_x: x-coordinate of the top-left corner of the ROI
    # roi_y: y-coordinate of the top-left corner of the ROI
    # roi_width: width of the ROI
    # roi_height: height of the ROI

    # A good starting point for a central square ROI:
    roi_width = int(frame_width * 0.2) # 40% of the full width
    roi_height = int(frame_height * 0.2) # 40% of the full height
    roi_x = (frame_width - roi_width) // 2   # Center the ROI horizontally
    roi_y = (frame_height - roi_height) // 2 # Center the ROI vertically

    # Or define fixed values if you know your camera's resolution:
    # roi_x, roi_y = 200, 150 # Example: Top-left at (200, 150)
    # roi_width, roi_height = 300, 200 # Example: A 300x200 pixel ROI

    print(f"ROI defined at: x={roi_x}, y={roi_y}, width={roi_width}, height={roi_height}")


    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # --- Crop the frame to the defined ROI ---
        cropped_frame = frame[roi_y : roi_y + roi_height, roi_x : roi_x + roi_width]

        if cropped_frame.shape[0] == 0 or cropped_frame.shape[1] == 0:
            print("Warning: Cropped frame is empty. Adjust ROI coordinates.")
            continue # Skip processing empty frames

        # --- Get predominant color from the cropped frame ---
        pred_color = get_predominant_color_from_frame(cropped_frame)
        print(pred_color)
        #return pred_color
        # --- Display the results ---
        # Draw a rectangle on the original frame to show the ROI
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)
        cv2.putText(frame, f"Detected: {pred_color.upper()}", (roi_x, roi_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Full Live Feed (with ROI)", frame)
        cv2.imshow("Cropped ROI for Analysis", cropped_frame) # Show the actual frame being analyzed

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()"""