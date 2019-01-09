import argparse
import math
import requests
import os
from file_utils import make_dir

def shot_info_parser(file_path):
    serialID_ls, keyframeName_ls, videoID_ls, videoName_ls = [], [], [], []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.split('\t')
            serialID_ls.append(row[0])
            keyframeName_ls.append(row[1])
            videoID_ls.append(row[2])
            videoName_ls.append(row[3])
    return serialID_ls, keyframeName_ls, videoID_ls, videoName_ls


def download_cc_web_video_keyframes(shot_info_path, output_path):
    server_videoPath = 'http://vireo.cs.cityu.edu.hk/webvideo/Keyframes/'
    serialID, keyframeName, videoID, videoName = shot_info_parser(shot_info_path)
    for i in range(len(videoID)):
        KID = str(int(math.floor(int(videoID[i])/100)))
        make_dir(os.path.join(output_path, KID))
        file_path = os.path.join(output_path, KID, keyframeName[i]+'.jpg')
        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            r = requests.get(os.path.join(server_videoPath, KID, keyframeName[i] + '.jpg'))
            with open(file_path, 'wb') as f:
                print('Write %s' % (keyframeName[i] + '.jpg'))
                f.write(r.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download cc video key frames")
    parser.add_argument('--shot_info', default='/home/eugene/Dev/Download-CCWebVideo-py/Shot_Info.txt')
    parser.add_argument('--outpath', default='/home/eugene/_DATASET/cc_web_video/Keyframes')
    args = parser.parse_args()

    download_cc_web_video_keyframes(args.shot_info, args.outpath)
