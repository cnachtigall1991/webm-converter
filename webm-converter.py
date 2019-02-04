#!/usr/bin/python3

import getopt
import sys
import os
import re
import shutil

files = []
path = os.getcwd() + '/webm'


def usage():
    print('''
webm-converter -h / --help
  Usage: ''' + os.path.basename(__file__) + ''' [OUTPUT_FORMAT]
  Encode all (mkv|mp4|avi|mov|flv|MOV) files in the current folder to webm using ffmpeg with vp9 and opus.
  All encoded files will be moved to a folder called 'webm'.

  Output formats:
    --240p     320x240   (24/25/30 fps)
    --360p     640x360   (24/25/30 fps)
    --480p     640x480   (24/25/30 fps)
    --720p30   1280x720  (24/25/30 fps)
    --720p60   1280x720  (50/60    fps)
    --1080p30  1920x1080 (24/25/30 fps)
    --1080p60  1920x1080 (50/60    fps)
    --1440p30  2560x1440 (24/25/30 fps)
    --1440p60  2560x1440 (50/60    fps)
    --2160p30  3840x2160 (24/25/30 fps)
    --2160p60  3840x2160 (50/60    fps)
    -o / --original [keeps scale, aspect ratio and framerate | encoding on average bitrate 3000k]

   Version: 0.1-stable
   Developer: Christian Nachtigall
   Bugreports: https://github.com/cnachtigall1991/webm-converter/issues
   Github: https://github.com/cnachtigall1991/webm-converter
    ''')


def ffmpeg_orig(files):
    with os.scandir('.') as scan:
        for entry in scan:
            if not entry.name.startswith('.') and entry.is_file():
                if entry.name.endswith(('.mkv', '.mp4', '.avi', '.mov', '.flv', '.MOV')):
                    files.append(entry.name)

    for file in files:
        basename = re.sub('\.mkv|mp4|avi|mov|flv|MOV$', '', file)

        os.system('ffmpeg -i "' + file + '" -b:v 3000k -minrate 1500k -maxrate 4350k -tile-columns 2'
                            ' -g 240 -threads 8 -quality good -crf 30 -c:v libvpx-vp9 -c:a libopus -b:a 96k'
                            ' -ac 2 -af "pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR"'
                            ' -af "aresample=async=1:first_pts=0" -pass 1 -speed 4 -hide_banner "'
                            + basename + '.webm"')
        os.system('ffmpeg -i "' + file + '" -b:v 3000k -minrate 1500k -maxrate 4350k -tile-columns 4'
                            ' -g 240 -threads 8 -quality good -crf 30 -c:v libvpx-vp9 -c:a libopus -b:a 96k'
                            ' -ac 2 -af "pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR"'
                            ' -af "aresample=async=1:first_pts=0" -pass 2 -speed 2 -hide_banner -y "'
                            + basename + '.webm"')
        os.unlink('ffmpeg2pass-0.log')

        shutil.move(basename + '.webm', path)


def ffmpeg(files, width, height, avg, min, max, tile1, tile2, threads, crf, speed):
    with os.scandir('.') as scan:
        for entry in scan:
            if not entry.name.startswith('.') and entry.is_file():
                if entry.name.endswith(('.mkv', '.mp4', '.avi', '.mov', '.flv', '.MOV')):
                    files.append(entry.name)

    for file in files:
        basename = re.sub('\.mkv|mp4|avi|mov|flv|MOV$', '', file)

        os.system('ffmpeg -i "' + file + '" -vf scale=' + width + 'x' + height + ' -b:v ' + avg + 'k'
                            ' -minrate ' + min + 'k -maxrate ' + max + 'k -tile-columns ' + tile1 +
                            ' -g 240 -threads ' + threads + ' -quality good -crf ' + crf +
                            ' -c:v libvpx-vp9 -c:a libopus -ac 2'
                            ' -af "pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR"'
                            ' -af "aresample=async=1:first_pts=0" -pass 1 -speed 4 -hide_banner "'
                            + basename + '.webm"')
        os.system('ffmpeg -i "' + file + '" -vf scale=' + width + 'x' + height + ' -b:v ' + avg + 'k'
                            ' -minrate ' + min + 'k -maxrate ' + max + 'k -tile-columns ' + tile2 +
                            ' -g 240 -threads ' + threads + ' -quality good -crf ' + crf +
                            ' -c:v libvpx-vp9 -c:a libopus -ac 2'
                            ' -af "pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR" -y'
                            ' -af "aresample=async=1:first_pts=0" -pass 2 -speed ' + speed + ' -hide_banner "'
                            + basename + '.webm"')
        os.unlink('ffmpeg2pass-0.log')

        shutil.move(basename + '.webm', path)


def main():
    if not os.path.exists(path):
        os.mkdir(path)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ho', ['help', 'original', '240p', '360p', '480p', '720p30',
                                                         '720p60', '1080p30', '1080p60', '1440p30', '1440p60',
                                                         '2160p30', '2160p60'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-o', '--original'):
            ffmpeg_orig(files)
        elif opt in ('--240p'):
            ffmpeg(files, '320', '240', '150', '75', '218', '0', '1', '2', '37', '1')
        elif opt in ('--360p'):
            ffmpeg(files, '640', '360', '276', '138', '400', '1', '2', '4', '36', '1')
        elif opt in ('--480p'):
            ffmpeg(files, '640', '480', '750', '375', '1088', '1', '2', '4', '33', '1')
        elif opt in ('--720p30'):
            ffmpeg(files, '1280', '720', '1024', '512', '1485', '2', '4', '8', '32', '2')
        elif opt in ('--720p60'):
            ffmpeg(files, '1280', '720', '1800', '900', '2610', '2', '4', '8', '32', '2')
        elif opt in ('--1080p30'):
            ffmpeg(files, '1920', '1080', '1800', '900', '2610', '2', '4', '8', '31', '2')
        elif opt in ('--1080p60'):
            ffmpeg(files, '1920', '1080', '3000', '1500', '4350', '2', '4', '8', '31', '2')
        elif opt in ('--1440p30'):
            ffmpeg(files, '2560', '1440', '6000', '3000', '8700', '3', '8', '16', '24', '2')
        elif opt in ('--1440p60'):
            ffmpeg(files, '2560', '1440', '9000', '4500', '13050', '3', '8', '16', '24', '2')
        elif opt in ('--2160p30'):
            ffmpeg(files, '3840', '2160', '12000', '6000', '17400', '4', '16', '24', '15', '2')
        elif opt in ('--2160p60'):
            ffmpeg(files, '3840', '2160', '18000', '9000', '26100', '4', '16', '24', '15', '2')
        else:
            usage()
            sys.exit(2)


if __name__ == "__main__":
    main()
