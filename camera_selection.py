import cv2
from cv2_enumerate_cameras import enumerate_cameras


# for camera_info in enumerate_cameras():
#     print(f'{camera_info.index}: {camera_info.name}')


def select_camera_cli():
   """
   Allows the user to select a camera from a list of available cameras.
   
   Returns CameraInfo object
   """


   # Get a list of available cameras
   available_cameras = enumerate_cameras()
   # for i in range(10):  # Try up to 10 cameras
   #     cap = cv2.VideoCapture(i)
   #     if cap.isOpened():
   #         available_cameras.append(cap.getBackendName())
   #         cap.release()


   if not available_cameras:
       print("No cameras found.")
       return None, None


   print("Available cameras:")
   for id, camera_info in enumerate(available_cameras):
       print(f'{id}: {camera_info.name}')


   while True:
       try:
           choice = int(input("Enter camera index: "))
           if choice < len(available_cameras):
                return available_cameras[choice]
           print("Invalid choice. Please try again.")
       except ValueError:
           print("Invalid input. Please enter a number.")



if __name__ == "__main__":
   camera_info = select_camera_cli()
   if camera_info is not None:
       cap = cv2.VideoCapture(camera_info.index, camera_info.backend)


       while True:
           ret, frame = cap.read()
           if not ret:
               break


           cv2.imshow("Selected Camera", frame)


           if cv2.waitKey(1) == ord('q'):
               break


       cap.release()
       cv2.destroyAllWindows()
   pass