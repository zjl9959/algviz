import os
import re
import sys
import math
import subprocess
import psutil
from gooey import GooeyParser, Gooey

CHROME_PATH = "chrome.exe"
CAPTURA_CLI = "captura-cli.exe"
CHECK_ENV_PROCESS = ['chrome.exe', 'EyesRelax.exe']


def convert_mp4(info, svg_file):
    mp4_file = svg_file.replace('.svg', '.mp4')
    gif_file = svg_file.replace('.svg', '.gif')
    svg_width = math.floor(info['size'][0] * 2.33)
    svg_height = math.floor(info['size'][1] * 2.33)
    duration = info['duration']
    # Start chrome.
    command_list = [CHROME_PATH, '--kiosk', svg_file]
    # print(command_list)
    chrome_process = subprocess.Popen(command_list)
    # Start captura: {--vq Video Quality (1 to 100) (Default is 70)}
    command = """{} start -y --length {} --source {},{},{},{} --file {} --framerate 30 --vq 80""".format(
        CAPTURA_CLI, math.floor(duration), 0, 0, svg_width, svg_height, mp4_file)
    # print(command)
    subprocess.run(command, env=os.environ.copy())
    chrome_process.terminate()
    # Convert to gif.
    command = """ffmpeg -hide_banner -loglevel error -y -i {} {}""".format(mp4_file, gif_file)
    # print('\n{}'.format(command))
    subprocess.run(command, env=os.environ.copy())
    os.remove(mp4_file)


def process_markdown(dir_path):
    svg_path = []
    for file in os.listdir(dir_path):
        if file.endswith(".md"):
            md_path = os.path.join(dir_path, file)
            file_contents = []
            with open(md_path, "r", encoding='utf-8') as f:
                for line in f:
                    match = re.match(r"!\[(.*)\]\((.*)\)", line)
                    if match and match.group(2).endswith('.svg'):
                        svg_path.append(os.path.join(dir_path, match.group(2)))
                        line = line.replace('.svg', '.gif')
                    else:
                        match = re.match(r"<img alt=\"(.*)\" src=\"(.*)\" width=\"(.*)\"></img>", line)
                        if match and match.group(2).endswith('.svg'):
                            svg_path.append(os.path.join(dir_path, match.group(2)))
                            line = line.replace('.svg', '.gif')
                    file_contents.append(line)
            with open(md_path, "w", encoding='utf-8') as f:
                f.writelines(file_contents)
    return list(set(svg_path))


def convert_svgs(svg_files):
    nb_processed = 0
    for file in svg_files:
        nb_processed += 1
        print('Processed {}/{}.'.format(nb_processed, len(svg_files)))
        sys.stdout.flush()
        if not os.path.exists(file):
            continue
        # Parse svg info.
        info = None
        with open(file, 'r') as f:
            for line in f:
                st = line.rfind('<!--{')
                if st != -1:
                    ed = line.rfind('-->')
                    info_str = line[st + 4:ed]
                    info = eval(info_str)
        if info is not None:
            sys.stdout.flush()
            convert_mp4(info, file)


def check_env():
    # Check chrome process.
    processes = psutil.process_iter()
    for process in processes:
        if process.name() in CHECK_ENV_PROCESS:
            return False
    return True


@Gooey(language='chinese')
def main():
    parser = GooeyParser(description="将文件夹下面的 svg 转成 gif 并更新 markdown 链接")
    parser.add_argument("dir_path", help="请选择要处理的文件夹", widget='DirChooser')
    args = parser.parse_args()
    if not check_env():
        print("Please close these processes first: {}".format(CHECK_ENV_PROCESS))
        sys.stdout.flush()
        sys.exit(1)
    svg_files = process_markdown(args.dir_path)
    convert_svgs(svg_files)
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    main()
