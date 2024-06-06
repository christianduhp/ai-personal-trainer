import cv2
import numpy as np
import mediapipe as mp
import threading
import queue
import math

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


class PersonalAI:
    def __init__(
        self,
        file_name,
        model_path,
        resize: bool = False,
        resize_scale: float = 1.0,
        draw: bool = True,
        display: bool = False,
        streamlit: bool = False,
        frame_skip=2,
    ):

        self.file_name = file_name
        self.image_q = queue.Queue()
        self.model_path = model_path
        self.resize = resize
        self.resize_scale = resize_scale
        self.draw = draw
        self.display = display
        self.streamlit = streamlit
        self.frame_skip = frame_skip

        self.BaseOptions = mp.tasks.BaseOptions
        self.PoseLandmarker = mp.tasks.vision.PoseLandmarker
        self.PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        # Create a pose landmarker instance with the video mode:
        self.options = self.PoseLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=self.model_path),
            running_mode=self.VisionRunningMode.VIDEO,
        )

    def find_angle(self, frame, landmarks, p1, p2, p3, draw=True):
        land = landmarks.pose_landmarks[0]
        h, w, _ = frame.shape

        x1, y1, v1 = (land[p1].x, land[p1].y, land[p1].visibility)
        x2, y2, v2 = (land[p2].x, land[p2].y, land[p2].visibility)
        x3, y3, v3 = (land[p3].x, land[p3].y, land[p3].visibility)

        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        )
        position = (int(x2 * w + 10), int(y2 * h + 10))

        if draw:
            frame = cv2.putText(
                frame,
                str(int(angle)),
                position,
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 255, 255),
                2,
            )

        if v1 and v2 and v3 > 0.9:
            is_visible = True
        else:
            is_visible = False

        return frame, angle, is_visible

    def _draw_landmarks_on_image(self, rgb_image, detection_result):
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x, y=landmark.y, z=landmark.z
                    )
                    for landmark in pose_landmarks
                ]
            )
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style(),
            )
        return annotated_image

    def _process_frame(self, frame, landmarker, calc_ts, fps):

        if self.resize:
            height = int(frame.shape[0] * self.resize_scale)
            width = int(frame.shape[1] * self.resize_scale)
            dim = width, height
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

        if self.streamlit:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if self.draw:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            calc_ts.append(int(calc_ts[-1] + 1000 / fps))

            detection_result = landmarker.detect_for_video(mp_image, calc_ts[-1])
            frame = self._draw_landmarks_on_image(frame, detection_result)
            self.image_q.put((frame, detection_result, calc_ts[-1]))

        return frame

    def _process_video(self):
        with self.PoseLandmarker.create_from_options(self.options) as landmarker:
            cap = cv2.VideoCapture(self.file_name)
            fps = cap.get(cv2.CAP_PROP_FPS)
            calc_ts = [0.0]
            current_frame = 0

            while cap.isOpened():
                ret, frame = cap.read()

                if ret:
                    current_frame += 1
                    if current_frame % self.frame_skip != 0:
                        continue

                    frame = self._process_frame(frame, landmarker, calc_ts, fps)

                    if self.display:
                        cv2.imshow("Frame", frame)

                    # Press Q on keyboard to exit
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

                else:
                    break

            self.image_q.put((1, 1, "done"))
            cap.release()
            cv2.destroyAllWindows()

    def run(self):
        t1 = threading.Thread(target=self._process_video)
        t1.start()
