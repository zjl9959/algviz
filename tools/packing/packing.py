import os
import re
import sys
import datetime
import shutil
from gooey import GooeyParser, Gooey


IMAGE_SUFFIX = ['gif', 'png', 'jpg', 'bmp']
ZIP_PROGRAM = r'C:\Program Files\7-Zip\7z.exe'


def check_file_suffix(file_name, suffix):
    for suff in suffix:
        if file_name.endswith(suff):
            return True
    return False


def process_markdown(dir_path):
    files = []
    for file in os.listdir(dir_path):
        if file.endswith(".md"):
            md_path = os.path.join(dir_path, file)
            with open(md_path, "r", encoding='utf-8') as f:
                for line in f:
                    match = re.match(r"!\[(.*)\]\((.*)\)", line)
                    if match and check_file_suffix(match.group(2), IMAGE_SUFFIX):
                        files.append(os.path.join(dir_path, match.group(2)))
                    else:
                        match = re.match(r"<img alt=\"(.*)\" src=\"(.*)\" width=\"(.*)\"></img>", line)
                        if match and check_file_suffix(match.group(2), IMAGE_SUFFIX):
                            files.append(os.path.join(dir_path, match.group(2)))
            files.append(os.path.join(dir_path, file))
    return list(set(files))


def packing_files(files, dir_path):
    if len(files) == 0:
        return
    date_now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    packing_dir = os.path.join(dir_path, '{}_{}'.format(
        os.path.basename(dir_path), date_now))
    os.mkdir(packing_dir)
    for file in files:
        target_file = os.path.join(packing_dir, os.path.basename(file))
        shutil.copy(file, target_file)
    zip_name = '{}.{}'.format(os.path.basename(dir_path), date_now)
    os.system('"{}" a -r -mhe=on {}.7z {}'.format(ZIP_PROGRAM,
              os.path.join(dir_path, zip_name), packing_dir))
    shutil.rmtree(packing_dir)


@Gooey(language='chinese')
def main():
    parser = GooeyParser(description="自动打包 markdown 和依赖的图片资源")
    parser.add_argument("dir_path", help="请选择要处理的文件夹", widget='DirChooser')
    args = parser.parse_args()
    files = process_markdown(args.dir_path)
    packing_files(files, args.dir_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
