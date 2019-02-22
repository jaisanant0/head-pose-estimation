from imutils import face_utils
import cv2
import numpy as np
import dlib
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#capture frames
cap = cv2.VideoCapture(-1)

# output
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') #video codec
out = cv2.VideoWriter(os.getcwd()+'/head_pose.avi',fourcc,5,(int(cap.get(3)), int(cap.get(4))),True)

while True :
      ret, image = cap.read()

      size = image.shape

      faces = detector(image,1)

      for face in faces :
            shape = predictor(image,face)
            shape = face_utils.shape_to_np(shape)

            # taking 5 image points
            nose_tip = shape[30]
            chin = shape[8]
            left_eye_lcorner = shape[45]
            right_eye_rcorner = shape[36]
            left_mouth_corner = shape[54]
            right_mouth_corner = shape[48]

            # 2D points
            image_points = np.array([(nose_tip[0],nose_tip[1]),
                                     (chin[0],chin[1]),
                                     (left_eye_lcorner[0],left_eye_lcorner[1]),
                                     (right_eye_rcorner[0],right_eye_rcorner[1]),
                                     (left_mouth_corner[0],left_mouth_corner[1]),
                                     (right_mouth_corner[0],right_mouth_corner[1])], dtype = "double")

            # 3D points
            world_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -300.0, -65.0),        # Chin
                            (225.0, 170.0, -135.0),     # Left eye left corner
                            (-225.0, 170.0, -135.0),      # Right eye right corne
                            (150.0, -150.0, -125.0),    # Left Mouth corner
                            (-150.0, -150.0, -125.0)      # Right mouth corner
                             ])

            # camera params
            #focal_length = size[1]
            #optic_center = [size[1]/2,size[0]/2]

            cam_mat = np.array([[1.9961704327353971e+03,0,3.1950000000000000e+02],
                                [0,1.9961704327353971e+03,2.3950000000000000e+02],
                                [0,0,1]], dtype = "double")

            #print("Camera Matrix : \n" + str(cam_mat))
            dist_coeffs = np.zeros((5,1))
            (success, rotation_vector, translation_vector) = cv2.solvePnP(world_points, image_points, cam_mat,
                                                                          dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

            #print ("Rotation Vector:\n {0}".format(rotation_vector))
            #print ("Translation Vector:\n {0}".format(translation_vector))
 
 
            
            # draw a line out of the nose 
            (nose_point, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1200.0)]), rotation_vector,
                                                             translation_vector, cam_mat, dist_coeffs)
 
            for pt in image_points:
                  cv2.circle(image, (int(pt[0]), int(pt[1])), 2, (150,100,150), -1)
 
 
            pt1 = (int(image_points[0][0]), int(image_points[0][1]))
            pt2 = (int(nose_point[0][0][0]), int(nose_point[0][0][1]))
 
            cv2.line(image, pt1, pt2, (0,0,200), 2)
 
            # Display image
            cv2.imshow("Output", image)
            #save
            out.write(image)

      if cv2.waitKey(1) & 0xFF == ord('q') :
            break

cap.release()
out.release()
cv2.destroyAllWindows()
