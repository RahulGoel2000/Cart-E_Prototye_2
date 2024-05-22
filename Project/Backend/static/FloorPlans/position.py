import cv2

# Function to handle mouse events
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Coordinates: ({x}, {y})')

# Read an image
image = cv2.imread('Floor3.png')

# Display the image
cv2.imshow('Image', image)

# Set mouse callback function
cv2.setMouseCallback('Image', click_event)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
