#!/usr/bin/env bash

input_file="/home/chase/Downloads/mk_test/C0120.MP4"
output_file="/home/chase/Downloads/mk_test/downsample/C0120.MP4"

# Re-encode to 1080
ffmpeg -i ${input_file} -copy_unknown -map_metadata 0 \
    -crf 20 -preset veryslow -vf scale=1920:1080 -pix_fmt yuv420p -c:a copy ${output_file}

# Update metadata dates to match
exiftool -tagsFromFile ${input_file} -extractEmbedded \
    -all:all -FileModifyDate -overwrite_original ${output_file}
    