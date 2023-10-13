import os
import re
import sys
import subprocess
from gooey import GooeyParser, Gooey

TIME_CUT_PATH = "D:\\SoftWares\\timecut"
CHROME_PATH = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'


def convert_mp4(info, svg_file):
    mp4_file = svg_file.replace('.svg', '.mp4')
    gif_file = svg_file.replace('.svg', '.gif')
    svg_width = info['size'][0] / 3 * 4
    svg_height = info['size'][1] / 3 * 4
    duration = info['duration']
    os.chdir(TIME_CUT_PATH)
    command = """node cli.js {} --viewport="{}, {}" --duration={} -q --executable-path={} --no-headless --screenshot-type=jpeg --screenshot-quality=1 --pix-fmt=yuv420p --output={}""".format(
        svg_file, svg_width + 1, svg_height + 1, duration, CHROME_PATH, mp4_file)
    print(command)
    subprocess.run(command, env=os.environ.copy())
    # Convert to gif.
    command = """ffmpeg -y -i {} {}""".format(mp4_file, gif_file)
    print(command)
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
        print('正在转换文件【{}/{}】：{}'.format(nb_processed, len(svg_files), file))
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


@Gooey(language='chinese',
       progress_regex=r"^正在转换文件【(?P<current>\d+)/(?P<total>\d+)】：.*$",
       progress_expr="current / total * 100")
def main():
    parser = GooeyParser(description="将文件夹下面的 svg 转成 gif 并更新 markdown 链接")
    parser.add_argument("dir_path", help="请选择要处理的文件夹", widget='DirChooser')
    args = parser.parse_args()
    if not os.path.exists(args.dir_path):
        print("文件夹不存在")
        exit(1)
    svg_files = process_markdown(args.dir_path)
    convert_svgs(svg_files)


def test():
    dir_path = 'D:\\code\\algviz\\副业\\example'
    svg_files = process_markdown(dir_path)
    convert_svgs(svg_files)


if __name__ == "__main__":
    main()
