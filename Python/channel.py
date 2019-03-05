#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os

src_channel_file = 'src/channel.txt'
f = open(src_channel_file, 'w')
f.close()

f = open('src/config.txt')
channels = f.readlines()
f.close()

src_apks = []
for file in os.listdir('.'):
    if os.path.isfile(file):
        extension = os.path.splitext(file)[1][1:]
        if extension in 'apk':
            src_apks.append(file)

for src_apk in src_apks:
    src_apk_file_name = os.path.basename(src_apk)
    path_arr = os.path.splitext(src_apk_file_name)
    src_apk_name = path_arr[0]
    src_apk_extension = path_arr[1]

    output_dir = 'dst/' + src_apk_name + '/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for channel_name in channels:
        channel_name = channel_name.strip()
        dst_channel_file = "META-INF/channel_{channel}".format(channel=channel_name)
        target_apk = output_dir + src_apk_name + "-" + channel_name + src_apk_extension
        shutil.copy(src_apk, target_apk)
        zf = zipfile.ZipFile(target_apk, 'a', zipfile.ZIP_DEFLATED)
        zf.write(src_channel_file, dst_channel_file)
        zf.close()
