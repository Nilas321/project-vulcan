import cv2

def stitch_frames(cam_id1, cam_id2):
    # Create VideoCapture objects for both cameras
    cap1 = cv2.VideoCapture(cam_id1)
    cap2 = cv2.VideoCapture(cam_id2)
    
    # Check if the cameras are opened successfully
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Error: Cannot open cameras")
        return
    
    # Create stitcher object
    stitcher = cv2.Stitcher.create()
    
    # Capture frames from both cameras
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        #resize both frames to 480x640
        frame1 = cv2.resize(frame1, (480, 640))
        frame2 = cv2.resize(frame2, (480, 640))
        
        #rotate frame1 clockwise
        frame1 = cv2.rotate(frame1, cv2.ROTATE_90_CLOCKWISE)
        
        # rotate frame2 anticlockwise
        frame2 = cv2.rotate(frame2, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # show both frames:
        cv2.imshow("frame1", frame1)
        cv2.imshow("frame2", frame2)
        
        # Check if frames are captured successfully
        if not (ret1 and ret2):
            print("Error: Cannot read frames from cameras")
            break
        
        # Stitch frames
        status, result = stitcher.stitch([frame1, frame2])
        
        # Check if stitching is successful
        if status == cv2.Stitcher_OK:
            cv2.imshow("Stitched Image", result)
        else:
            print("Error during stitching")
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release VideoCapture objects and close windows
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

# Example usage:
stitch_frames(2, 4)  # do `ls /dev/video*` and get camera IDs and pass those here..
