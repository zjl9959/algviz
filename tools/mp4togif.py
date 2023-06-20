import os
import sys
import subprocess


def convert_file(file_path):
    if file_path.endswith('.mp4'):
        out_path = file_path.replace('.mp4', '.gif')
        command = """ffmpeg -y -i {} {}""".format(file_path, out_path)
        print(command)
        subprocess.run(command, env=os.environ.copy())


def main():
    if len(sys.argv) < 2:
        print("Usage: python mp4togif.py <file/folder>")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        print('Path {} not exists!'.format(sys.argv[1]))
        exit(1)
    if os.path.isdir(sys.argv[1]):
        for file in os.listdir(sys.argv[1]):
            convert_file(os.path.join(sys.argv[1], file))
    else:
        convert_file(os.path.join(os.curdir, sys.argv[1]))


if __name__ == "__main__":
    main()
