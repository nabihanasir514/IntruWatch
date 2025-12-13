import cv2

# Create a VideoCapture object, with 0 for the default camera
# Use 1, 2, etc. for additional cameras
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

print("Camera opened successfully. Press 'q' to exit.")

while True:
    # Read a frame from the video source
    # 'ret' is a boolean (True/False) and 'frame' is the image data (NumPy array)
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the captured frame in a window named 'Camera Feed'
    cv2.imshow('Camera Feed', frame)

    # Wait for 1 millisecond for a key press
    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
