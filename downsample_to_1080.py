#!/usr/bin/env python
import os
import argparse

def dir_file_path(string):
    if os.path.isdir(string) or os.path.isfile(string):
        return string
    else:
        raise NotADirectoryError(string)

def parse_config():
    parser = argparse.ArgumentParser(
        description='Downsample MP4 videos to 1080p')
    parser.add_argument('--input', type=dir_file_path,
                        help='File path or directory containing MP4 files')
    parser.add_argument('--output_dir', type=str, default='',
                        help='Output directory  DEFAULT: <input>/downsample/')
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")
    return parser.parse_args()

def downsample_to_1080(input, output, verbose=False):
    # Re-encode to 1080
    if verbose:
        verbose_str = ""
    else:
        verbose_str = "-hide_banner -loglevel error"
    ffmpeg_command = ("ffmpeg -i {input} -copy_unknown -map_metadata 0 "
                      "-crf 20 -preset veryslow -vf scale=1920:1080 -pix_fmt yuv420p "
                      "-c:a copy {verbose_str} -y {output}".format(input=input, 
                      verbose_str=verbose_str, output=output))
    if verbose:
        print('Executing: ' + ffmpeg_command)
    os.system(ffmpeg_command)

    # Update metadata dates to match
    if verbose:
        verbose_str = "-v2"
    else:
        verbose_str = "-q"
    exiftool_command = ('exiftool {verbose_str} -tagsFromFile {input} -extractEmbedded '
                        '-all:all -FileModifyDate -overwrite_original {output}'.format(
                        verbose_str=verbose_str, input=input, output=output))
    if verbose:
        print('Executing: ' + exiftool_command)
    os.system(exiftool_command)

def process(input, output, verbose=False):
    if input.endswith('.mp4') or input.endswith('.MP4'):
        # Get output file name
        if output is '':
            output = os.path.join(os.path.dirname(input), 'downsample', os.path.basename(input))
        else:
            output = os.path.join(output, os.path.basename(input))

        # If output directory doesn't exist, create it
        if not os.path.exists(os.path.dirname(output)):
            os.mkdir(os.path.dirname(output), 777)
            os.chmod(os.path.dirname(output), 0o777)

        # Downsample
        print('Downsampling ' + input)
        downsample_to_1080(input, output, verbose=verbose)
        if verbose:
            print('Output to ' + output)
        return 1
    else:
        return 0


def main():
    args = parse_config()
    input = args.input

    processed = 0
    if os.path.isdir(input):
        print('Downsampling directory: ' + args.input)
        for filename in os.listdir(input):
            processed += process(os.path.join(input, filename), args.output_dir, verbose=args.verbose)
    else:
        processed += process(input, args.output_dir, verbose=args.verbose)

    print('FINISHED')
    print('Successfully downsampled mp4 files: ' + str(processed))

if __name__ == '__main__':
    main()
