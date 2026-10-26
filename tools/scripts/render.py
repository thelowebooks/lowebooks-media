"""Render brand templates to images or videos.

still:  render.py still <html> <w> <h> <out_prefix> <arg> [<arg> ...]   -> <out_prefix>_<arg>.png
video:  render.py video <html> <w> <h> <out.mp4> [fps]
The page must define render(t). Videos also define DURATION and EVENTS ([[sound, time], ...]).
"""
import sys, os, shutil, subprocess, tempfile, wave
import numpy as np
from playwright.sync_api import sync_playwright

SR = 44100

def tone(freqs, dur, decay, amp, sweep=None):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for f in freqs:
        if sweep:
            f_t = f + (sweep - f) * (t / dur)
            out += np.sin(2 * np.pi * np.cumsum(f_t) / SR)
        else:
            out += np.sin(2 * np.pi * f * t)
    env = np.exp(-t / decay) * np.minimum(1, t / 0.003)
    return amp * out / len(freqs) * env

SOUNDS = {
    'tick': lambda: tone([1800], 0.05, 0.012, 0.18),
    'tickhi': lambda: tone([2400], 0.07, 0.02, 0.28),
    'pop': lambda: tone([620], 0.12, 0.04, 0.45, sweep=220),
    'ding': lambda: tone([880, 1320, 1760], 1.2, 0.35, 0.32),
}

def make_audio(events, duration, path):
    buf = np.zeros(int(SR * (duration + 1.5)))
    for name, at in events:
        s = SOUNDS[name]()
        i = int(SR * at)
        buf[i:i + len(s)] += s[:len(buf) - i]
    buf = np.clip(buf, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())

def open_page(p, html, w, h):
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    page.goto('file://' + os.path.abspath(html))
    page.evaluate('window.__ready')
    return b, page

def still(html, w, h, prefix, args):
    with sync_playwright() as p:
        b, page = open_page(p, html, w, h)
        for a in args:
            page.evaluate(f'render({a})')
            page.screenshot(path=f'{prefix}_{a}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            print('wrote', f'{prefix}_{a}.png')
        b.close()

def video(html, w, h, out, fps=30):
    tmp = tempfile.mkdtemp()
    with sync_playwright() as p:
        b, page = open_page(p, html, w, h)
        dur = page.evaluate('window.DURATION'); events = page.evaluate('window.EVENTS')
        n = int(round(dur * fps))
        for i in range(n):
            page.evaluate(f'render({i / fps})')
            page.screenshot(path=f'{tmp}/f{i:05d}.jpg', type='jpeg', quality=92, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        b.close()
    make_audio(events, dur, f'{tmp}/a.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/f%05d.jpg', '-i', f'{tmp}/a.wav',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    shutil.rmtree(tmp)
    print('wrote', out, f'{dur:.1f}s', n, 'frames')

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        still(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6:])
    else:
        video(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6]) if len(sys.argv) > 6 else 30)
