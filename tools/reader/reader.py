import os
import subprocess
import sys
from gooey import GooeyParser, Gooey


SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
MODELS_DIR = os.path.join(os.path.join(SCRIPT_PATH, 'tts_models'))
TTS_MODELS = {
    'zh-CN-tacotron2-DDC-GST': "tts_models/zh-CN/baker/tacotron2-DDC-GST"
}


def load_audio_texts(dir_name):
    audio_texts = list()
    for file in os.listdir(dir_name):
        if file.endswith('.txt'):
            file_real_path = os.path.join(dir_name, file)
            with open(file_real_path, mode='r', encoding='utf-8') as f:
                txt = None
                for line in f.readlines():
                    if txt is None:
                        txt = line.strip('\r\n')
                    else:
                        txt += line.strip('\r\n')
                    if len(txt) > 0 and txt[-1] not in ['。', '？', '！']:
                        txt += '。'
                audio_texts.append((file_real_path.replace('.txt', ''), txt))
    return audio_texts


def process_audios(audio_texts, model):
    for (file, text) in audio_texts:
        command = """tts --text "{}" --model_name "{}" --out_path {}.mp3""".format(
            text, model, file)
        subprocess.run(command, env=os.environ.copy())


@Gooey(language='chinese')
def main():
    parser = GooeyParser(description="将文件夹下面的文本转成音频")
    parser.add_argument("dir_path", help="请选择要处理的文件夹", widget='DirChooser')
    parser.add_argument("tts_model", default='zh-CN-tacotron2-DDC-GST', help="请选择语音模型", choices=list(TTS_MODELS.keys()))
    args = parser.parse_args()
    audio_texts = load_audio_texts(args.dir_path)
    process_audios(audio_texts, TTS_MODELS[args.tts_model])
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    main()
