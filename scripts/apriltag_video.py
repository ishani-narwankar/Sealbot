#!/usr/bin/env python

from argparse import ArgumentParser
import os
import cv2
import apriltag

################################################################################

def apriltag_video(input_streams=['../media/input/arrayvid3.mp4', '../media/input/multiple_tags.mp4'], # For default cam use -> [0]
                   output_stream=False,
                   display_stream=True,
                   detection_window_name='AprilTag',
                  ):

    '''
    Detect AprilTags from video stream.

    Args:   input_streams [list(int/str)]: Camera index or movie name to run detection algorithm on
            output_stream [bool]: Boolean flag to save/not stream annotated with detections
            display_stream [bool]: Boolean flag to display/not stream annotated with detections
            detection_window_name [str]: Title of displayed (output) tag detection window
    '''

    parser = ArgumentParser(description='Detect AprilTags from video stream.')
    apriltag.add_arguments(parser)
    # set default tag family to tag16h5 and tag IDs from 0 to 8
    # parser.set_defaults(families='tag16h5', tag_id_filter=lambda x: x < 9)
    parser.set_defaults(families='tag16h5') # Set the default tag family to tag16h5

    options = parser.parse_args()

    '''
    Set up a reasonable search path for the apriltag DLL.
    Either install the DLL in the appropriate system-wide
    location, or specify your own search paths as needed.
    '''

    detector = apriltag.Detector(options, searchpath=apriltag._get_dll_path())


    for stream in input_streams:

        video = cv2.VideoCapture(stream)

        output = None

        if output_stream:
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(video.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc(*'XVID')
            if type(stream) != int:
                output_path = '../media/output/'+str(os.path.split(stream)[1])
                output_path = output_path.replace(str(os.path.splitext(stream)[1]), '.avi')
            else:
                output_path = '../media/output/'+'camera_'+str(stream)+'.avi'
            output = cv2.VideoWriter(output_path, codec, fps, (width, height))

        while(video.isOpened()):

            success, frame = video.read()
            if not success:
                break


            result, overlay = apriltag.detect_tags(frame,
                                                   detector,
                                                   camera_params=(1037.6, 1028.6, 982.2, 478.8),
                                                    tag_size=0.01,
                                                    vizualization=3,
                                                    verbose=3,
                                                    annotation=True
                                                  )
            if output_stream:
                output.write(overlay)

            if display_stream:
                cv2.imshow(detection_window_name, overlay)
                if cv2.waitKey(1) & 0xFF == ord(' '): # Press space bar to terminate
                    break

################################################################################

if __name__ == '__main__':
    apriltag_video()