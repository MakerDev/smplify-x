'''
output_folder의 png 결과를 video로 merge함
pkl 하나로 합치는것도 해야할 수도. 
pkl -> FBX animation 변환도 해야하긴함. (그냥 obj 모으면 되나? obj는 trimesh기반 파일인듯.)
'''
import os
import subprocess
import pickle
import uuid
import glob
import shutil

if __name__ == '__main__':
    '''
    Usage: 
    smplifyx 폴더에서 python utils/make_video.py로 실행해야함.
    '''
    output_folder = "output_folder"

    '''
    temporal_folder에 다 복사하고 영상 만든 후에 그 폴더 내용 지우기.
    '''
    temp_foldername = f'temp_014bda90-839f-11ed-bf7d-44af28647dd1'
    targets = os.listdir(output_folder)

    for target in targets:
        if len(glob.glob(os.path.join(output_folder, target, "*.mp4"))) > 0:
            continue #If already done, skip.

        if os.path.exists(temp_foldername):
            shutil.rmtree(temp_foldername)
        
        os.makedirs(temp_foldername, exist_ok=False)

        images = glob.glob(f"{output_folder}/{target}/**/*.png", recursive=True)
        for image in images:
            img_idx = image.split('\\')[-3]
            new_img_name = os.path.basename(image.replace('.png', f"_{img_idx}.png"))
            new_image_path = os.path.join(temp_foldername, new_img_name)

            shutil.copy(image, new_image_path)
        cmd = [ 
            f"cd {temp_foldername} &&",
            "ffmpeg -framerate 15 -i output_%05d.png -c:v libx264 output.mp4"
        ]
            
        _ = subprocess.run(' '.join(cmd), shell=True)
        result_file = f"{temp_foldername}/output.mp4"
        shutil.copy(result_file, os.path.join(output_folder, target))

