import os
import glob


if __name__ == '__main__':
    FPS = 15

    VIDEO_DIR = 'D:\\IWIP\\mocap_test_dataset'
    FRAMES_DIR = os.path.join(VIDEO_DIR, 'images')
    KEYPOINTS_DIR = os.path.join(VIDEO_DIR, 'keypoints')
    OPENPOSE_IMAGES_DIR = os.path.join(VIDEO_DIR, 'openpose_images')

    os.makedirs(KEYPOINTS_DIR, exist_ok=True)
    os.makedirs(OPENPOSE_IMAGES_DIR, exist_ok=True)

    videos = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))

    for video_path in videos:
        # Extract frames using ffmpeg.
        video_name = os.path.basename(video_path).split('.')[0]
        output_dir = os.path.join(FRAMES_DIR, video_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            os.system(f"ffmpeg -i {video_path} -vf fps={FPS}  -qscale:v 2 {output_dir}/%05d.png")

        #Run openpose
        openpose_keypoint_dir = os.path.join(KEYPOINTS_DIR, video_name)
        openpose_image_dir = os.path.join(OPENPOSE_IMAGES_DIR, video_name)
        os.makedirs(openpose_keypoint_dir, exist_ok=True)
        os.makedirs(openpose_image_dir, exist_ok=True)
        
        # If already done, skip.
        if len(os.listdir(openpose_keypoint_dir)) != 0:
            continue

        # If you want to use hands and face tracking features, append '--hands --face' in command.
        os.system(f"cd ..\\openpose && .\\bin\\OpenPoseDemo.exe --image_dir {output_dir} --write_json {openpose_keypoint_dir} --display 0 --write_images {openpose_image_dir}")


