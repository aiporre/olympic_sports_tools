import numpy as np
import os
from olympic_sports import read_seq
from skvideo import io
import argparse
import os


def convert(path_dataset, path_output=None):
    # video_list = 'video_Olympic.list'
    # original list of files
    video_list = os.path.join(os.path.split(__file__)[0], "..", "resources", "video_Olympic.list")

    # path_dataset = '/home/datasets/Olympic'
    # path_output = '/home/datasets/Olympic_converted'
    if path_output is None:
        path_output = path_dataset + '_converted'

    print('Creating new folder for converted dataset: ', path_output)
    os.makedirs(path_output, exist_ok=True)

    cnt = 0
    file = open(video_list, 'r')
    for line_raw in file:
        video_name = line_raw.rstrip('\n')
        video_class = video_name.split('/')[0]
        video_filename = video_name.split('/')[-1]
        video_path = os.path.join(path_dataset, video_name)
        if not os.path.exists(video_path):
            print('Video: ', video_path, ' doesn\'t exists')
            continue
        video_name_wo_ext = os.path.join(*video_name.split('.')[:-1])
        converted_video_path = os.path.join(path_output, video_name_wo_ext + '_converted.avi')

        dest_class_folder = os.path.join(path_output, video_class)
        if not os.path.exists(dest_class_folder):
            os.mkdir(dest_class_folder)

        print('#{:04d} \t| Reading video {}'.format(cnt + 1, video_name))
        image_npy_list = read_seq(video_path)
        print('Found {:04d} images'.format(len(image_npy_list)))
        sample_img = image_npy_list[0]

        video = np.array(image_npy_list, dtype=np.float32)
        video = (255.0 * video).astype(np.uint8)
        writer = io.FFmpegWriter(converted_video_path, outputdict={'-r': '25', '-vcodec': 'mpeg4'}, verbosity=1)
        for img in video:
            writer.writeFrame(img)
        writer.close()
        print('')
        cnt += 1


def main():
    parser = argparse.ArgumentParser(
        description='Converts a directory containing seq files into avi for the Olympic Sports Dataset')
    parser.add_argument('path', metavar='path-to-olympic-dataset', type=str,
                        help='Path to the olympic dataset.')
    parser.add_argument('-o', '--output-path', type=str, default=None,
                        help='Path to output directory. Defaults to the directory with the suffix \'_converted\' of the olympic dataset.')
    args = parser.parse_args()

    print(' args: ', args)
    convert(args.path, args.output_path)


if __name__ == '__main__':
    main()
