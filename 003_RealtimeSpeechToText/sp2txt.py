import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer

# パラメータ設定
samplerate = 16000  # 16kHz
block_duration = 0.5  # 0.5秒ごとにチェック
pause_threshold_sec = 3.0  # 無音が1秒以上で終了
# model_path = "vosk-model-small-ja-0.22"  # モデルパス(簡易版)
model_path = "vosk-model-ja-0.22"  # モデルパス(本命)

# 音声データを格納するキュー
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    # モデル読み込み
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(True)

    print("マイク待機中...（発話で録音開始）")

    with sd.RawInputStream(samplerate=samplerate, blocksize=int(samplerate * block_duration),
                           dtype='int16', channels=1, callback=callback):

        started = False
        silence_duration = 0.0
        result_text = ""

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    if not started:
                        print("発話検出 → 録音開始")
                        started = True
                    result_text += text + " "
                    silence_duration = 0.0  # 音があったのでリセット
                else:
                    if started:
                        silence_duration += block_duration
            else:
                if started:
                    silence_duration += block_duration

            if started and silence_duration >= pause_threshold_sec:
                print("無音検出 → 録音終了")
                break

        # 最終出力
        final_result = json.loads(recognizer.FinalResult())
        result_text += final_result.get("text", "")
        print("\n認識結果：")
        print(result_text.strip())

if __name__ == '__main__':
    main()
