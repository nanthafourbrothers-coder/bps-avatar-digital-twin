import subprocess, os, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
from pptx import Presentation
SL = "../slides/"
prs = Presentation(SL + "AVATAR-Twin_Slides.pptx")
scripts = [s.notes_slide.notes_text_frame.text for s in prs.slides]
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
os.makedirs("work", exist_ok=True)
PAD_START, PAD_END = 0.4, 0.7
durs, wavs = [], []
for i, t in enumerate(scripts, 1):
    a, sr = k.create(t, voice="am_michael", speed=1.0, lang="en-us")
    a = np.concatenate([np.zeros(int(PAD_START*sr)), a, np.zeros(int(PAD_END*sr))])
    p = f"work/a{i}.wav"; sf.write(p, a, sr); wavs.append(p); durs.append(len(a)/sr)
    print(i, round(durs[-1], 1), "s", len(t.split()), "words")
print("total", round(sum(durs), 1), "s")
# scenes: one encoded file per slide, same settings
for i, d in enumerate(durs, 1):
    out = f"work/s{i}.tmp.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",f"{SL}slide-{i}.png",
        "-vf",f"scale=1920:1080,format=yuv420p,loop=-1:1,trim=duration={d:.3f},fade=t=in:st=0:d=0.3",
        "-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-r","30",out], check=True)
    os.rename(out, f"work/s{i}.mp4")
open("work/list.txt","w").write("".join(f"file 's{i}.mp4'\n" for i in range(1, len(durs)+1)))
open("work/alist.txt","w").write("".join(f"file 'a{i}.wav'\n" for i in range(1, len(durs)+1)))
subprocess.run("cd work && ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy video_only.tmp.mp4 && mv video_only.tmp.mp4 video_only.mp4", shell=True, check=True)
subprocess.run("cd work && ffmpeg -y -loglevel error -f concat -safe 0 -i alist.txt -c copy audio.wav", shell=True, check=True)
subprocess.run("ffmpeg -y -loglevel error -i work/video_only.mp4 -i work/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest AVATAR-Twin_Pitch_Video.tmp.mp4 && mv AVATAR-Twin_Pitch_Video.tmp.mp4 AVATAR-Twin_Pitch_Video.mp4", shell=True, check=True)
# subtitles (SRT) from the script, timed per slide
def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s-int(s))*1000):03d}"
t0, srt = 0.0, []
for i,(t,d) in enumerate(zip(scripts,durs),1):
    srt.append(f"{i}\n{ts(t0+PAD_START)} --> {ts(t0+d-0.3)}\n{t}\n"); t0 += d
open("AVATAR-Twin_Narration.srt","w").write("\n".join(srt))
open("AVATAR-Twin_Narration_Script.txt","w").write("\n\n".join(f"[Slide {i}]\n{t}" for i,t in enumerate(scripts,1)))
