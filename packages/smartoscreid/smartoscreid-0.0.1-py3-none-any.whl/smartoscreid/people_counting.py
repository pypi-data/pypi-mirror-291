import warnings
warnings.filterwarnings("ignore")

import os
import cv2
import glob
import torch
import operator
import numpy as np
import pandas as pd
import datetime as dt
from PIL import Image
from ultralytics import YOLO
from smartoscreid.reid import REID
from smartoscreid.utils import cv2_addBox, get_FrameLabels, get_name
from smartoscreid.load_video import LoadVideo
from smartoscreid.config import *

class PeopleCounting:
    def __init__(self, model=None, reid_threshold=0.4) -> None: 
        """
        Input:
        - model: The path to the YOLO model file (default is "yolov8m.pt").
        - reid_threshold: A float value representing the threshold for the ReID (Re-identification) process (default is 0.4).

        Output:
        - Initializes the PeopleCounting class with the YOLO model, ReID model, and threshold.
        - Creates an output folder if it doesn't exist.
        """

        if model == None:
            raise Exception("You model path is invalid! Try your path")
        self.model = YOLO(model)
        self.reid = REID()
        self.threshold = reid_threshold
        self.folder_initialize()

    def folder_initialize(self)->None:
        """
        Input:
        - None

        Output:
        - Checks if the 'output' folder exists; if not, creates it.
        - No return value.
        """

        if not os.path.exists("output"):
            os.mkdir("output")


    def run(self, videos=[], export_video=False) -> None:
        """
        Input:
        - videos: A list of video file paths to process.

        Output:
        - Processes each video to detect and track people.
        - Outputs a CSV file with the ID mapping and person-minute data for each video in the 'output' folder.
        - No return value.
        """

        all_frames = []
        video_capture, frame_rate, w, h = None, None, None, None
        nof = [(0,0,0)]
        video_names = []
        for i, video in enumerate(videos):
            vname = get_name(video)
            if vname in video_names:
                video_names.append(vname + '_' + str(i))
            else:     
                video_names.append(vname)
            loadvideo = LoadVideo(video)
            video_capture, frame_rate, w, h, vn = loadvideo.get_VideoLabels()
            nof.append((vn, w, h, frame_rate))
            while True:
                ret, frame = video_capture.read()
                if ret is not True:
                    video_capture.release()
                    break
                all_frames.append(frame)

        track_cnt = dict()
        images_by_id = dict()
        ids_per_frame = []
        id_mapping = {}

        all_track_id = {}

        for fdx, frame in enumerate(all_frames):
            results = self.model.track(frame, persist=True, classes=0,  verbose=False)
            
            try:
                track_id = [int(x.item()) for x in results[0].boxes.id] 
                boxes = results[0].boxes.xyxy.tolist()

                for idx, tid in enumerate(track_id):
                    if tid not in all_track_id.keys():
                        all_track_id[tid] = [fdx, 0]
                    else:
                        all_track_id[tid][1] = fdx

                    if tid not in track_cnt:
                        track_cnt[tid] = [
                            [fdx, int(boxes[idx][0]), int(boxes[idx][1]), int(boxes[idx][2]), int(boxes[idx][3])]
                        ]
                        images_by_id[tid] = [frame[int(boxes[idx][1]):int(boxes[idx][3]), int(boxes[idx][0]):int(boxes[idx][2])]]
                    else:
                        track_cnt[tid].append([
                            fdx,
                            int(boxes[idx][0]), int(boxes[idx][1]), int(boxes[idx][2]), int(boxes[idx][3]),
                        ])
                        images_by_id[tid].append(frame[int(boxes[idx][1]):int(boxes[idx][3]), int(boxes[idx][0]):int(boxes[idx][2])])

                ids_per_frame.append(set(track_id))
            except:
                continue

        exist_ids = set()
        final_fuse_id = dict()

        feats = dict()
        for i in images_by_id:
            feats[i] = self.reid._features(images_by_id[i])

        for f in ids_per_frame:
            if f:
                if len(exist_ids) == 0:
                    for i in f:
                        final_fuse_id[i] = [i]
                        id_mapping[i] = i
                    exist_ids = exist_ids or f
                else:
                    new_ids = f - exist_ids
                    for nid in new_ids:
                        dis = []
                        # if len(images_by_id[nid]) < 10:
                        #     exist_ids.add(nid)
                        #     continue
                        unpickable = []
                        for i in f:
                            for key, item in final_fuse_id.items():
                                if i in item:
                                    unpickable += final_fuse_id[key]
                        for oid in (exist_ids - set(unpickable)) & set(final_fuse_id.keys()):
                            tmp = np.mean(self.reid.compute_distance(feats[nid], feats[oid]))
                            dis.append([oid, tmp])
                        exist_ids.add(nid)
                        if not dis:
                            final_fuse_id[nid] = [nid]
                            id_mapping[nid] = nid
                            continue
                        dis.sort(key=operator.itemgetter(1))
                        if dis[0][1] < self.threshold:
                            combined_id = dis[0][0]
                            images_by_id[combined_id] += images_by_id[nid]
                            final_fuse_id[combined_id].append(nid)
                            id_mapping[nid] = combined_id
                        else:
                            final_fuse_id[nid] = [nid]
                            id_mapping[nid] = nid

        export_data = []
        sum_person_minute = 0
        for idx, final_id in enumerate(final_fuse_id.keys()):
            min_frame = len(all_frames)
            max_frame = 0
            for idd in final_fuse_id[final_id]:
                min_frame = min(min_frame, all_track_id[idd][0])
                max_frame = max(max_frame, all_track_id[idd][1])    

            person_minute = round((max_frame-min_frame)/frame_rate/60, 2)
            sum_person_minute += person_minute
            export_data.append([idx+1, final_id, person_minute])

        export_data.append(["", "", sum_person_minute])
        df_export = pd.DataFrame(export_data, columns=["ID", "ID Mapping","Person_minute"])
        current_dt = dt.datetime.now()
        current_dt = current_dt.strftime('%Y-%m-%d_%H:%M:%S')

        if not os.path.exists(f'output/{current_dt}'):
            os.mkdir(f'output/{current_dt}')

        df_export.to_csv(f'output/{current_dt}/result.csv', index=False)

        if export_video:
            final_id_frame = []
            for frame in range(len(all_frames)):
                frame2 = all_frames[frame]
                for idx in final_fuse_id:
                    for i in final_fuse_id[idx]:
                        for f in track_cnt[i]:
                            if frame == f[0]:
                                text_scale, text_thickness, line_thickness = get_FrameLabels(frame2)
                                frame2 = cv2_addBox(idx, frame2, f[1], f[2], f[3], f[4], line_thickness, text_thickness, text_scale)
                final_id_frame.append(frame2)

            for idx in range(len(nof)-1):
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                
                if not os.path.exists(f'output/{current_dt}/tracks'):
                    os.mkdir(f'output/{current_dt}/tracks')

                output_path = f'output/{current_dt}/tracks/{video_names[idx]}_tracking.avi'
                out = cv2.VideoWriter(output_path, fourcc, nof[idx+1][3], (nof[idx+1][1], nof[idx+1][2]))
                for idframe in range(nof[idx][0], nof[idx][0] + nof[idx+1][0]):
                    out.write(final_id_frame[idframe])
            
                out.release()

