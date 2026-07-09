#!/usr/bin/env python3
"""Touch-friendly window switcher with close buttons."""
import subprocess, re, os, sys
import tkinter as tk

DISPLAY = os.environ.get('DISPLAY', ':0')
XAUTH   = os.environ.get('XAUTHORITY', os.path.expanduser('~/.Xauthority'))

ENV = {**os.environ, 'DISPLAY': DISPLAY, 'XAUTHORITY': XAUTH}

BG        = '#111827'
TILE_BG   = '#1f2937'
TILE_HOV  = '#374151'
ACC       = '#14b8a6'   # teal accent
CLOSE_FG  = '#ef4444'
CLOSE_HOV = '#b91c1c'
TEXT      = '#f3f4f6'
SUB       = '#9ca3af'

TILE_H    = 90          # px per tile
FONT_APP  = ('Sans', 11, 'bold')
FONT_TTL  = ('Sans', 14)
FONT_X    = ('Sans', 22, 'bold')
X_W       = 72          # width of X button column


def wmctrl(*args):
    return subprocess.run(['wmctrl', *args], capture_output=True, text=True, env=ENV)


def get_windows():
    r = wmctrl('-lx')
    wins = []
    for line in r.stdout.strip().split('\n'):
        if not line:
            continue
        m = re.match(r'^(0x\w+)\s+(-?\d+)\s+(\S+)\s+\S+\s*(.*)', line)
        if not m:
            continue
        wid, desk, wclass, title = m.group(1), m.group(2), m.group(3), m.group(4)
        if desk == '-1':          # skip desktop/docks
            continue
        app = wclass.split('.')[-1] if '.' in wclass else wclass
        # skip the switcher itself
        if 'win-switcher' in title.lower() or app.lower() == 'python3':
            continue
        wins.append({'id': wid, 'title': title, 'app': app})
    return wins


def close_win(wid, rebuild_fn):
    wmctrl('-ic', wid)
    import time; time.sleep(0.35)
    rebuild_fn()


def focus_win(wid, root):
    wmctrl('-ia', wid)
    root.destroy()


def main():
    root = tk.Tk()
    root.title('win-switcher')
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg=BG)
    root.focus_force()
    root.bind('<Escape>', lambda e: root.destroy())

    # ── header ──────────────────────────────────────────────────────────
    hdr = tk.Frame(root, bg=BG)
    hdr.pack(fill='x', padx=24, pady=(22, 8))
    tk.Label(hdr, text='WINDOWS', font=('Sans', 12, 'bold'),
             fg=SUB, bg=BG).pack(side='left')
    tk.Label(hdr, text='TAP TO SWITCH  •  ✕ TO CLOSE',
             font=('Sans', 10), fg='#4b5563', bg=BG).pack(side='right')

    # ── scrollable area ─────────────────────────────────────────────────
    outer = tk.Frame(root, bg=BG)
    outer.pack(fill='both', expand=True, padx=16, pady=(0, 16))

    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0,
                       bd=0, relief='flat')
    scrollbar = tk.Scrollbar(outer, orient='vertical',
                             command=canvas.yview, width=6)
    inner = tk.Frame(canvas, bg=BG)

    inner.bind('<Configure>',
               lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    win_id = canvas.create_window((0, 0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # keep inner frame width = canvas width
    canvas.bind('<Configure>',
                lambda e: canvas.itemconfig(win_id, width=e.width))

    # ── tile builder ─────────────────────────────────────────────────────
    def build_tiles():
        for w in inner.winfo_children():
            w.destroy()

        wins = get_windows()
        if not wins:
            tk.Label(inner, text='No windows open.',
                     font=('Sans', 16), fg=SUB, bg=BG).pack(pady=60)
            return

        for win in wins:
            wid   = win['id']
            app   = win['app']
            title = win['title']
            short = (title[:52] + '…') if len(title) > 53 else title

            # outer tile frame
            tile = tk.Frame(inner, bg=TILE_BG, height=TILE_H)
            tile.pack(fill='x', pady=3)
            tile.pack_propagate(False)

            # left colour accent bar
            bar = tk.Frame(tile, bg=ACC, width=4)
            bar.pack(side='left', fill='y')

            # text section
            info = tk.Frame(tile, bg=TILE_BG)
            info.pack(side='left', fill='both', expand=True, padx=(14, 0))

            app_lbl = tk.Label(info, text=app.upper(),
                               font=FONT_APP, fg=ACC, bg=TILE_BG, anchor='w')
            app_lbl.pack(fill='x', pady=(18, 0))

            ttl_lbl = tk.Label(info, text=short,
                               font=FONT_TTL, fg=TEXT, bg=TILE_BG, anchor='w')
            ttl_lbl.pack(fill='x')

            # X close button
            x_frame = tk.Frame(tile, bg=TILE_BG, width=X_W)
            x_frame.pack(side='right', fill='y')
            x_frame.pack_propagate(False)

            x_btn = tk.Label(x_frame, text='✕', font=FONT_X,
                             fg=CLOSE_FG, bg=TILE_BG,
                             anchor='center', cursor='hand2')
            x_btn.place(relx=0.5, rely=0.5, anchor='center')

            # ── hover / tap visual feedback ─────────────────────────────
            focus_parts = [tile, bar, info, app_lbl, ttl_lbl]

            def on_enter(e, parts=focus_parts, xf=x_frame, xb=x_btn):
                for p in parts: p.configure(bg=TILE_HOV)
                xf.configure(bg=TILE_HOV); xb.configure(bg=TILE_HOV)
            def on_leave(e, parts=focus_parts, xf=x_frame, xb=x_btn):
                for p in parts: p.configure(bg=TILE_BG)
                xf.configure(bg=TILE_BG); xb.configure(bg=TILE_BG)

            def on_x_enter(e, xb=x_btn): xb.configure(fg=CLOSE_HOV)
            def on_x_leave(e, xb=x_btn): xb.configure(fg=CLOSE_FG)

            for w in focus_parts:
                w.bind('<Enter>', on_enter)
                w.bind('<Leave>', on_leave)
                w.bind('<Button-1>', lambda e, i=wid: focus_win(i, root))

            x_frame.bind('<Enter>', on_enter)
            x_frame.bind('<Leave>', on_leave)
            x_btn.bind('<Enter>', on_x_enter)
            x_btn.bind('<Leave>', on_x_leave)
            x_btn.bind('<Button-1>', lambda e, i=wid: close_win(i, build_tiles))
            x_frame.bind('<Button-1>', lambda e, i=wid: close_win(i, build_tiles))

    build_tiles()
    root.mainloop()


if __name__ == '__main__':
    main()
