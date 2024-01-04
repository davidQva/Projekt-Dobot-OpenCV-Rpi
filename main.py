import threading
import time
from OCVmodule import OCVmodule, capture_frame, close_camera
from modified_server import Server, Observer
import cv2
import json
from threading import Lock

order = [None, None, None, None, None]
oldOrder = [None, None, None, None, None]

# Create a lock object
lock = Lock()

class MessageLogger(Observer):
    
    def update(self, message):     
        global order, oldOrder       
        # Acquire the lock
        lock.acquire()
        try:            
            order = message
            if order != oldOrder:
                print(f"Message from server received: {message}")
                oldOrder = order
        finally:
            # Release the lock
            lock.release()

def opencv_thread_function():
    ocv = OCVmodule()
    global cubes
    # Anta att OCVmodule har en metod för att starta kameraprocessen
    while True:                    
        frame = capture_frame()
        if frame is None:
            break
       
        cubes, result = ocv.process_image()

        cv2.imshow('Original', frame)
        cv2.imshow('Processed', result)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC-tangenten
            break

    close_camera()
 
# Define functions for different scenarios
def handle_scenario_1():
    print("Scenario 1")
    pass

def handle_scenario_2():
    print("Scenario 2")
    pass

def handle_scenario_3():
    global order
    print("Order Received: ", order[1:])
    lookForCubes = order[1:5]

    while True:
        for cube in cubes:
            if cube.color in lookForCubes and cube.x <= 50:
                cubeRemove = cube
                print(f"Matching cube found at X={cube.x}, Y={cube.y}")
                moveRobot(cube.x, cube.y, cube.rotation)               
                lookForCubes.remove(cubeRemove.color)              
                break # Exits the function once a matching cube is found
        if not lookForCubes:
            order = [None, None, None, None]
            print("All cubes found, Order Finished")
            return # Exits the function once all cubes are found
        time.sleep(0.1) # Sleeps for 100ms          

def moveRobot(x, y, angle):
    time.sleep(3)
    print(f"Moving robot to X={x}, Y={y}, Angle={angle}")
    time.sleep(3) 
    print(f"Done!")
    return True

def main():
    
    server = Server()  
    opencv_thread = threading.Thread(target=opencv_thread_function)
    opencv_thread.start()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    logger = MessageLogger()
    server.register_observer(logger)

    # Dispatch dictionary
    scenario_actions = {
        'start': handle_scenario_1,
        'stop': handle_scenario_2,
        'order': handle_scenario_3        
    }

    oldOrder = None

    try:
        while True:
            # Assuming 'order' is updated by the message receiver
            if order is not None and order!= oldOrder:
                oldOrder = order
                scenario = order[0]
                if scenario in scenario_actions:
                    scenario_actions[scenario]()
                else:                    
                    default_scenario()
            time.sleep(1)

    finally:
        # Make sure to join threads and clean up resources
        opencv_thread.join()
        server_thread.join()

  
if __name__ == "__main__":
    main()