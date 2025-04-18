import sounddevice as sd
import numpy as np
import queue
import sys
import json
import threading
import keyboard
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel

# VOSK API ログレベル設定(出力オフ)
SetLogLevel(-1)

# 設定
samplerate = 16000
block_duration = 0.5  # 秒
model_path = "vosk-model-ja-0.22"
output_wav = "recorded.wav"
output_txt = "result.txt"

# 音声データ用キュー
audio_data = []
q = queue.Queue()

# 終了フラグ
stop_flag = False

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # wav出力のためnumpy形式で保存
    # audio = np.frombuffer(indata, dtype=np.float32).reshape(-1,1)
    audio = np.frombuffer(indata, dtype=np.int16).copy().reshape(-1,1)
    q.put(audio)

def listen_for_esc():
    global stop_flag
    keyboard.wait('esc')
    stop_flag = True
    print("\n録音終了")

def save_wav(filename, audio_data, samplerate):
    data = np.concatenate(audio_data)
    # data_int16 = (data * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(data.astype(np.int16).tobytes())
        # wf.writeframes(data_int16.tobytes())

def main():
    global stop_flag

    # モデル読み込み
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(True)

    print("音声入力開始:\n")

    # Escキー検知スレッド開始
    threading.Thread(target=listen_for_esc, daemon=True).start()

    with sd.RawInputStream(samplerate=samplerate, blocksize=int(samplerate * block_duration),
                           dtype='int16', channels=1, callback=callback):
                           # dtype='float32', channels=1, callback=callback):
        result_text = ""

        while not stop_flag:
            indata = q.get()
            audio_data.append(indata)

            # vosk_data = (indata * 32767).astype(np.int16).tobytes()
            vosk_data = indata.tobytes()
            if recognizer.AcceptWaveform(vosk_data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(f"{text}")
                    result_text += text + "\n"

        # 終了後の最終結果
        final_result = json.loads(recognizer.FinalResult())
        text = final_result.get("text", "")
        if text:
            print(f"\n最終結果：{text}")
            result_text += text

        # wav保存
        save_wav(output_wav, audio_data, samplerate)
        print(f"録音データを{output_wav}に保存")

        # txt保存
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(result_text.strip())
        print(f"テキストデータを{output_txt}に保存")

    print("\n処理完了")

if __name__ == '__main__':
    main()
