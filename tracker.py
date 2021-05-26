import cv2
import sys
import nexstarAPI

def main():

    #port = "/dev/ttyS0"
    port = "/dev/ttyUSB0"

    # for arg in sys.argv:
    #     if arg.startswith("--port="):
    #         port = arg[7:]

    if port is None:
        print("specify serial port using --port=<device> argument.")
        return

    controller = nexstarAPI.NexstarHandController(port)

    if True:

        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
        tracker_type = tracker_types[5]

        if int(major_ver) < 4 and int(minor_ver) < 3:
            tracker = cv2.face.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'CSRT':
                tracker = cv2.TrackerCSRT_create()
            if tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()

        # Read video
        video = cv2.VideoCapture("Ben.mp4")
        #video = cv2.VideoCapture(0) // should be from camera

        # Exit if video not opened.
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        # Read first frame.
        ok, frame = video.read()
        if not ok:
            print('Cannot read video file')
            sys.exit()

        bbox = (200, 150, 200, 300)

        xCenter = (int(bbox[0] + int(bbox[2]))) / 2
        yCenter = (int(bbox[1]+int(bbox[3]))) / 2

        # Uncomment the line below to select a different bounding box
        bbox = cv2.selectROI(frame, False)

        # Initialize tracker with first frame and bounding box
        ok = tracker.init(frame, bbox)

        while True:
            # Read a new frame
            ok, frame = video.read()
            if not ok:
                break

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok, bbox = tracker.update(frame)
            x (int(bbox[0] + int(bbox[2]))) / 2
            y = (int(bbox[1]+int(bbox[3]))) / 2

            if(x > xCenter * 1.1): # move scope right
                
                xCenter = x
                # should be in a function and getting paramters of where to move
                pos = controller.getPosition()
                controller.gotoPosition(pos[0] * 1.1, pos[1])
                gotoInProgress = True
                while gotoInProgress:
                    pos = controller.getPosition()
                    print(pos)
                    gotoInProgress = getGotoInProgress()

            if(x < xCenter  * 1.1): # move scope left

                    # should be in a function and getting paramters of where to move
                xCenter = x
                pos = controller.getPosition()
                controller.gotoPosition(pos[0] * 0.9, pos[1])
                gotoInProgress = True
                while gotoInProgress:
                    pos = controller.getPosition()
                    print(pos)
                    gotoInProgress = getGotoInProgress()

            if(y < yCenter * 1.1):# move scope up
                yCenter = y
                    # should be in a function and getting paramters of where to move
                pos = controller.getPosition()
                controller.gotoPosition(pos[0], pos[1] * 1.1)
                gotoInProgress = True
                while gotoInProgress:
                    pos = controller.getPosition()
                    print(pos)
                    gotoInProgress = getGotoInProgress()


            if(y > xCenter * 1.1):# move scope down
                yCenter = y
                    # should be in a function and getting paramters of where to move
                pos = controller.getPosition()
                controller.gotoPosition(pos[0], pos[1] * 0.9)
                gotoInProgress = True
                while gotoInProgress:
                    pos = controller.getPosition()
                    print(pos)
                    gotoInProgress = getGotoInProgress()
                


            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 3)
            else :
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,130), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

            # Display tracker type on frame
            cv2.putText(frame, tracker_type + " Tracker", (100,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,0,50),2);
            cv2.putText(frame,  "X = " +str(int(xCenter)), (100,90), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,0,50),2);
            cv2.putText(frame,  "Y = " +str(int(yCenter)), (220,90), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,0,50),2);

            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100,60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,0,50), 2);
            print("X ", xCenter)
            print("Y ",yCenter)
            # Display result
            cv2.imshow("Tracking", frame)

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break

    if False:

        while True:
            for deviceId in [NexstarDeviceId.AZM_RA_MOTOR, NexstarDeviceId.ALT_DEC_MOTOR]:
                try:
                    (versionMajor, versionMinor) = controller.getDeviceVersion(deviceId)
                    status = "version = {}.{}".format(versionMajor, versionMinor)
                except NexstarPassthroughError as exception:
                    status = "error: {}".format(exception)

                print("device {} {} : {}".format(deviceId.name, "." * (27 - len(str(deviceId.name))), status))

                time.sleep(1)

    controller.close()

if __name__ == "__main__":
    main()
