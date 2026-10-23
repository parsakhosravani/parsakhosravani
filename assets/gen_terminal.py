import html
def esc(x): return html.escape(x).replace("  ", "\u00a0\u00a0").replace("\u00a0 ", "\u00a0\u00a0")
W, LINE_H, TOP, LEFT = 820, 26, 74, 28
CHAR_W = 9.6          # width of one monospace char at 16px
TYPE_SPEED = 0.055    # seconds per char
PAUSE = 0.55

# (kind, segments). prompt lines are typed, output lines appear at once
script = [
  ("cmd", "whoami"),
  ("out", [("parsa khosravani", "#e6edf3", True)]),
  ("out", [("frontend engineer · I make the web feel fast", "#8b949e", False)]),
  ("cmd", "cat ~/.stack"),
  ("out", [("typescript  ", "#4a9eff", True), ("react  ", "#61dafb", True), ("next.js  ", "#e6edf3", True),
           ("vue  ", "#42b883", True), ("angular  ", "#ff4f6d", True), ("node", "#7ee787", True)]),
  ("cmd", "ls ~/obsessions"),
  ("out", [("real-time-ui/    web-perf/    browser-games/    three.js/", "#79c0ff", False)]),
  ("cmd", "git log -1 --format=%s motto"),
  ("out", [("ship it, then make it faster.", "#d2a8ff", False)]),
  ("cmd", "echo $AFTER_HOURS"),
  ("out", [("dota · counter-strike · coffee", "#ffa657", False)]),
]

lines_svg, defs = [], []
t = 0.8
y = TOP
for i, (kind, content) in enumerate(script):
    if kind == "cmd":
        prompt = [("parsa", "#7ee787", True), ("@", "#8b949e", False), ("github", "#7ee787", True),
                  (":", "#8b949e", False), ("~", "#79c0ff", True), ("$ ", "#e6edf3", False)]
        plen = sum(len(s) for s, *_ in prompt)
        # prompt appears instantly
        spans = "".join(f'<tspan fill="{c}"{" font-weight=\"700\"" if b else ""}>{esc(s)}</tspan>' for s, c, b in prompt)
        lines_svg.append(f'<text x="{LEFT}" y="{y}" opacity="0">{spans}<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>')
        # typed command, revealed char by char with a clip
        n = len(content)
        x0 = LEFT + plen * CHAR_W
        cid = f"c{i}"
        widths = ";".join(f"{k*CHAR_W:.1f}" for k in range(n + 1))
        keyt = ";".join(f"{k/n:.4f}" for k in range(n + 1))
        dur = n * TYPE_SPEED
        defs.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{y-20}" height="28" width="0">'
                    f'<animate attributeName="width" values="{widths}" keyTimes="{keyt}" calcMode="discrete" '
                    f'begin="{t+0.25:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
        lines_svg.append(f'<text x="{x0}" y="{y}" fill="#e6edf3" clip-path="url(#{cid})">{esc(content)}</text>')
        t += 0.25 + dur + 0.3
    else:
        spans = "".join(f'<tspan fill="{c}"{" font-weight=\"700\"" if b else ""}>{esc(s)}</tspan>' for s, c, b in content)
        lines_svg.append(f'<text x="{LEFT}" y="{y}" opacity="0">{spans}<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>')
        nxt = script[i+1][0] if i + 1 < len(script) else None
        t += 0.12 if nxt == "out" else PAUSE
    y += LINE_H
    if kind == "out" and (i + 1 < len(script) and script[i+1][0] == "cmd"):
        y += 8

# final prompt + blinking cursor
y += 8
prompt_final = ('<tspan fill="#7ee787" font-weight="700">parsa</tspan><tspan fill="#8b949e">@</tspan>'
                '<tspan fill="#7ee787" font-weight="700">github</tspan><tspan fill="#8b949e">:</tspan>'
                '<tspan fill="#79c0ff" font-weight="700">~</tspan><tspan fill="#e6edf3">$ </tspan>')
lines_svg.append(f'<text x="{LEFT}" y="{y}" opacity="0">{prompt_final}<tspan fill="#7ee787" fill-opacity="1">\u2588<animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></tspan><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>')

H = y + 34
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: Parsa Khosravani, frontend engineer">
  <defs>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#21262d"/><stop offset="1" stop-color="#161b22"/></linearGradient>
    <radialGradient id="glow" cx="0.15" cy="0" r="1"><stop offset="0" stop-color="#7ee787" stop-opacity="0.07"/><stop offset="1" stop-color="#7ee787" stop-opacity="0"/></radialGradient>
    {"".join(defs)}
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="url(#glow)"/>
  <path d="M13 1h{W-26}a12 12 0 0 1 12 12v23H1V13A12 12 0 0 1 13 1z" fill="url(#bar)"/>
  <line x1="1" y1="36" x2="{W-1}" y2="36" stroke="#30363d"/>
  <circle cx="24" cy="19" r="6.5" fill="#ff5f57"/><circle cx="46" cy="19" r="6.5" fill="#febc2e"/><circle cx="68" cy="19" r="6.5" fill="#28c840"/>
  <text x="{W/2}" y="24" text-anchor="middle" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13">parsa@github: ~ — zsh</text>
  <g font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace" font-size="16" xml:space="preserve">
    {chr(10).join("    " + l for l in lines_svg)}
  </g>
</svg>
'''
open('/home/claude/parsakhosravani/assets/terminal.svg', 'w').write(svg)
print("height", H, "total anim", round(t, 1), "s")
