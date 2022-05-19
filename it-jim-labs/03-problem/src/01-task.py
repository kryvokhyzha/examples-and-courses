import cv2
import numpy as np
from config import opt


def find_homography(kp1, desc1, kp2, desc2, h1, w1, matcher='knn'):
    if matcher == 'bf':
        ## match descriptors
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desc1, desc2)
        
        min_match_dist = min([m.distance for m in matches])
        dmatches = [m for m in matches if m.distance <= opt.cutoff_coef * min_match_dist]

        ## extract the matched keypoints
        src_pts  = np.float32([kp1[m.queryIdx].pt for m in dmatches])
        dst_pts  = np.float32([kp2[m.trainIdx].pt for m in dmatches])
    elif matcher == 'knn':
        ## match descriptors
        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
        nn_matches = matcher.knnMatch(desc1, desc2, k=2)
        
        ## extract the matched keypoints
        src_pts  = np.float32([kp1[m.queryIdx].pt for m, n in nn_matches if m.distance < opt.nn_match_ratio * n.distance])
        dst_pts  = np.float32([kp2[m.trainIdx].pt for m, n in nn_matches if m.distance < opt.nn_match_ratio * n.distance])
        
    if len(src_pts) < opt.min_match_cnt:
        return []

    ## find homography matrix and do perspective transform
    H, status = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)
    status = status.ravel() != 0
    if status.sum() < opt.min_match_cnt:
        return []
    
    src_pts, dst_pts = src_pts[status], dst_pts[status]
    planar = np.float32([[0,0], [0, h1-1], [w1-1, h1-1], [w1-1, 0]])
    planar = cv2.perspectiveTransform(np.expand_dims(planar, axis=0), H).squeeze(axis=0)
    
    return planar


def detect_features(detector, image):
    keypoints, descrs = detector.detectAndCompute(image, None)
    if descrs is None:
        descrs = []
    return keypoints, descrs


def main():
    orb = cv2.ORB_create(opt.n_features)
    
    marker_img = cv2.cvtColor(cv2.imread(str(opt.path_to_data / opt.input_marker_img_name)), cv2.COLOR_BGR2GRAY)
    h_marker, w_marker = marker_img.shape[:2]
    key_points_marker, descriptors_marker = detect_features(orb, marker_img)
    
    cap = cv2.VideoCapture(str(opt.path_to_data / opt.input_video_name))
    assert cap.isOpened(), "Error opening video stream or file"

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(str(opt.path_to_predictions / '01-task-solution.avi'), cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))

    while(True):
        ret, frame = cap.read()

        if ret:
            frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            key_points_frame, descriptors_frame = detect_features(orb, frame_grey)
            
            polygon = find_homography(key_points_marker, descriptors_marker, key_points_frame, descriptors_frame, h_marker, w_marker)
            frame = cv2.polylines(frame, [np.int32(polygon)], True, (0, 255, 0), 1, cv2.LINE_AA)
            out.write(frame)
        else:
            break  

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
