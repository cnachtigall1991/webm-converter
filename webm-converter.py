#!/usr/bin/python3

import argparse
import textwrap
import sys
import os
import re
import shutil

version = '0.2-stable'
files = []
path = os.getcwd() + '/webm'


def scan_folder():
    with os.scandir(os.getcwd()) as scan:
        for entry in scan:
            if not entry.name.startswith('.') and entry.is_file():
                if entry.name.endswith(('.mkv', '.mp4', '.avi', '.mov', '.flv', '.MOV')):
                    files.append(entry.name)


def ffmpeg_orig(files):
    scan_folder()

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
    scan_folder()

    for file in files:
        basename = re.sub('\.mkv|mp4|avi|mov|flv|MOV$', '', file)

        os.system('ffmpeg -i "' + file + '" -vf scale=' + width + 'x' + height + ' -b:v ' + avg + 'k'
                    ' -minrate ' + min + 'k -maxrate ' + max + 'k -tile-columns ' + tile1 +
                    ' -g 240 -threads ' + threads + ' -quality good -crf ' + crf + ' -c:v libvpx-vp9 -c:a libopus'
                    ' -ac 2 -af "pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR"'
                    ' -af "aresample=async=1:first_pts=0" -pass 1 -speed 4 -hide_banner "'
                    + basename + '.webm"')
        os.system('ffmpeg -i "' + file + '" -vf scale=' + width + 'x' + height + ' -b:v ' + avg + 'k'
                    ' -minrate ' + min + 'k -maxrate ' + max + 'k -tile-columns ' + tile2 +
                    ' -g 240 -threads ' + threads + ' -quality good -crf ' + crf + ' -c:v libvpx-vp9 -c:a libopus'
                    ' -ac 2 -af "pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR" -y'
                    ' -af "aresample=async=1:first_pts=0" -pass 2 -speed ' + speed + ' -hide_banner "'
                    + basename + '.webm"')
        os.unlink('ffmpeg2pass-0.log')

        shutil.move(basename + '.webm', path)


def options():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                Encode (mkv|mp4|avi|mov|flv|MOV) files in the current folder to webm (vp9 + opus) using ffmpeg.
                All encoded files will be moved to a folder called "webm".
            '''),
        epilog=textwrap.dedent('''\
                Version:    ''' + version + '''
                Developer:  Christian Nachtigall
                Bugreports: https://github.com/cnachtigall1991/webm-converter/issues
                Github:     https://github.com/cnachtigall1991/webm-converter
            '''),
        allow_abbrev=False)
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)
    group = parser.add_argument_group('encoding')
    group.add_argument('-o', '--original', action='store_true', dest='original', help='keeps scale, aspect ratio and framerate | encoding on average bitrate 3000k')
    group.add_argument('--240p', action='store_true', dest='enc240p', help='320x240 (24/25/30 fps)')
    group.add_argument('--360p', action='store_true', dest='enc360p', help='640x360 (24/25/30 fps)')
    group.add_argument('--480p', action='store_true', dest='enc480p', help='640x480 (24/25/30 fps)')
    group.add_argument('--720p30', action='store_true', dest='enc720p30', help='1280x720 (24/25/30 fps)')
    group.add_argument('--720p60', action='store_true', dest='enc720p60', help='1280x720 (50/60 fps)')
    group.add_argument('--1080p30', action='store_true', dest='enc1080p30', help='1920x1080 (24/25/30 fps)')
    group.add_argument('--1080p60', action='store_true', dest='enc1080p60', help='1920x1080 (50/60 fps)')
    group.add_argument('--1440p30', action='store_true', dest='enc1440p30', help='2560x1440 (24/25/30 fps)')
    group.add_argument('--1440p60', action='store_true', dest='enc1440p60', help='2560x1440 (50/60 fps)')
    group.add_argument('--2160p30', action='store_true', dest='enc2160p30', help='3840x2160 (24/25/30 fps)')
    group.add_argument('--2160p60', action='store_true', dest='enc2160p60', help='3840x2160 (50/60 fps)')

    args = parser.parse_args()
    if args is not None:
        if not os.path.exists(path):
            os.mkdir(path)

        if args.original:
            ffmpeg_orig(files)
        elif args.enc240p:
            ffmpeg(files, '320', '240', '150', '75', '218', '0', '1', '2', '37', '1')
        elif args.enc360p:
            ffmpeg(files, '640', '360', '276', '138', '400', '1', '2', '4', '36', '1')
        elif args.enc480p:
            ffmpeg(files, '640', '480', '750', '375', '1088', '1', '2', '4', '33', '1')
        elif args.enc720p30:
            ffmpeg(files, '1280', '720', '1024', '512', '1485', '2', '4', '8', '32', '2')
        elif args.enc720p60:
            ffmpeg(files, '1280', '720', '1800', '900', '2610', '2', '4', '8', '32', '2')
        elif args.enc1080p30:
            ffmpeg(files, '1920', '1080', '1800', '900', '2610', '2', '4', '8', '31', '2')
        elif args.enc1080p60:
            ffmpeg(files, '1920', '1080', '3000', '1500', '4350', '2', '4', '8', '31', '2')
        elif args.enc1440p30:
            ffmpeg(files, '2560', '1440', '6000', '3000', '8700', '3', '8', '16', '24', '2')
        elif args.enc1440p60:
            ffmpeg(files, '2560', '1440', '9000', '4500', '13050', '3', '8', '16', '24', '2')
        elif args.enc2160p30:
            ffmpeg(files, '3840', '2160', '12000', '6000', '17400', '4', '16', '24', '15', '2')
        elif args.enc2160p60:
            ffmpeg(files, '3840', '2160', '18000', '9000', '26100', '4', '16', '24', '15', '2')
    else:
        parser.print_help()
        sys.exit(2)


def main():
    options()


if __name__ == "__main__":
    main()
