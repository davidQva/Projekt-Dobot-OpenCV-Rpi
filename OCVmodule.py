import cv2
import numpy as np
#import picamera2 as Picamera2 

# Initialize global variables
camera = cv2.VideoCapture(0)
kernel = np.ones((5,5), np.uint8)

#raspberri pi camera#
""" 
camera = Picamera2()
camera.preview_configuration.main.size = (640, 360)
camera.preview_configuration.main.format = "RGB888"
camera.preview_configuration.align()
camera.configure("preview")
camera.start()
 """
#------------------#

class OCVmodule:
    def __init__(self):
        
        # Initialize global variables
        self.num_cubes = None
        self.colors = {
            'red': (np.array([0, 59, 166]), np.array([10, 229, 255]), np.array([180, 255, 255]), np.array([0, 59, 166])),
            'blue': (np.array([110, 50, 100]), np.array([130, 255, 255]), np.array([180, 255, 255]), np.array([180, 50, 100])),
            'green': (np.array([30, 50, 30]), np.array([80, 255, 255]), np.array([180, 255, 255]), np.array([150, 50, 30])),
            'yellow': (np.array([21, 14, 226]), np.array([37, 61, 255]), np.array([180, 255, 255]), np.array([21, 14, 226]))
        }

    def process_image(self):
        # Resize the image and convert to HSV
        
        image = capture_frame() 

        #raspberri pi camera#
        #image = camera.capture_array()
        #------------------#

        resized_image, hsv_image = imgProcess(image)

        cubes = []  # List to store detected cubes

        for color in self.colors:
            # Create mask for current color
            mask = cv2.inRange(hsv_image, self.colors[color][0], self.colors[color][1])
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv_image, self.colors[color][2], self.colors[color][3]))
            mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            
            contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process each contour
            for cnt in contours:
                if cv2.contourArea(cnt) > 400:  # Filter out small contours->  area>400 pixels
                    
                    # Compute the center and rotation of the contour
                    rect = cv2.minAreaRect(cnt) # Get the minimum area rectangle for the contour
                    box = cv2.boxPoints(rect)# Get the 4 corners of the box
                    box = np.int0(box)# Convert the corners to integers round off the values
                    cX, cY = np.int0(np.mean(box, axis=0))# X-value is calculated as the mean of the X-values of the 4 corners of the box
                    angle = rect[2] # The rotation is the third value in the rectangle tuple
 
                    # Create a Cube object and add it to the list
                    cubes.append(Cube(cX, cY, angle, color))

                    # Draw a rectangle around the cube
                    cv2.drawContours(resized_image, [box], 0, (0, 255, 0), 2)

                    # Overlay text information about the cube
                    text = f"Color: {color}, Position: ({cX}, {cY}), Rotation: {angle:.2f}"
                    cv2.putText(resized_image, text, (cX - 50, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return cubes, resized_image
    
def start_processing(self):
        while True:
            frame = capture_frame()
            if frame is None:
                break

            cubes, result = self.process_image(frame)

            # Visa kubinformation om några detekteras
            if cubes:
                print("\nDetected Cubes:")
                for i, cube in enumerate(cubes, start=1):
                    print(f"  Cube {i}:")
                    print(f"    Color: {cube.color}")
                    print(f"    Position: X={cube.x}, Y={cube.y}")
                    print(f"    Rotation: {cube.rotation} degrees")
            else:
                print("No cubes detected.")

            cv2.imshow('Original', frame)
            cv2.imshow('Processed', result)

            if cv2.waitKey(5) & 0xFF == 27:  # ESC-tangenten
                break

        close_camera()
    
class Cube:
    def __init__(self, x, y, rotation, color):
        self.x = x  # X-coordinate of the cube's center
        self.y = y  # Y-coordinate of the cube's center
        self.rotation = rotation  # Rotation of the cube
        self.color = color  # Color of the cube
       

# This function is called whenever a trackbar moves
def nothing(x):
    pass

def setup_trackbars():
    cv2.namedWindow('HSV Thresholding', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Min_CArea', 'HSV Thresholding', 0, 2000, nothing)

def imgProcess(image):
    scale_percent = 50  # Resize by 50%
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim)   
    # Convert to HSV
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    return resized_image,hsv_image

def capture_frame():
    ret, image = camera.read()
    if not ret:
        print("Failed to grab frame")
        return None
    return image


def close_camera():
    camera.release()
    cv2.destroyAllWindows()

# If OpenCV.py is run directly, this code will execute
# When imported, this code is no run
if __name__ == '__main__':
    ocvModule = OCVmodule()
    
    while True:
        frame = capture_frame()
        if frame is None:
            break
        cubes, result = ocvModule.process_image()

            # Check if cubes are detected and print their details
        if cubes:
            print("\nDetected Cubes:")
            for i, cube in enumerate(cubes, start=1):
                print(f"  Cube {i}:")
                print(f"    Color: {cube.color}")
                print(f"    Position: X={cube.x}, Y={cube.y}")
                print(f"    Rotation: {cube.rotation} degrees")
        else:
            print("No cubes detected.")

        cv2.imshow('Original', frame)
        cv2.imshow('Processed', result)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC key
            break
    close_camera()
