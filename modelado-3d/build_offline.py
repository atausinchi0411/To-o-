"""Genera las versiones distribuibles del visor QSM11.

  python modelado-3d/build_offline.py

Salidas:
  modelado-3d/QSM11_Visor_Tablet_Offline.html  -> un solo archivo, funciona SIN Internet
                                                 (librería 3D, modelo y páginas del manual incluidos)
  modelado-3d/artifact/                         -> versión web: HTML + carpeta manual/ con las páginas
Requisitos: poppler-utils (pdftoppm) e ImageMagick (convert).
"""
import base64, os, re, subprocess, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'Cummins_QSM11_Interactive_3D.html')
PDF = os.path.join(ROOT, 'Cummins QSM-11 Operation and Maintenance Manual.pdf')
PAGES_DIR = os.path.join(HERE, 'manual_paginas')
# Páginas del PDF incluidas: identificación, operación, mantenimiento, reparación, diagnóstico y especificaciones
PAGES = [25, *range(29, 40), *range(43, 61), *range(89, 94), *range(97, 109), *range(111, 123), *range(125, 131),
         *range(133, 143), *range(145, 155), *range(157, 193), *range(197, 199), *range(303, 358), *range(361, 382)]

def render_pages():
    os.makedirs(PAGES_DIR, exist_ok=True)
    for n in PAGES:
        out = os.path.join(PAGES_DIR, f'{n}.png')
        if os.path.exists(out): continue
        tmp = os.path.join(PAGES_DIR, '_t')
        subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '110', '-gray', '-png', PDF, tmp], check=True)
        f = [x for x in os.listdir(PAGES_DIR) if x.startswith('_t')][0]
        subprocess.run(['convert', os.path.join(PAGES_DIR, f), '-trim', '+repage', '-resize', '1000x', '-level', '22%,78%',
                        '-colors', '8', '-depth', '4', out], check=True)
        os.remove(os.path.join(PAGES_DIR, f))

def inline_libs(html):
    def rep(m):
        name = m.group(1).split('/')[-1]
        code = open(os.path.join(HERE, 'vendor', name), encoding='utf-8').read()
        return '<script>/* ' + name + ' (three.js r147, MIT) */\n' + code + '\n</script>'
    return re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/three@0\.147\.0/[^"]*?/([^"/]+\.js)"></script>',
                  lambda m: rep(m), html)

def strip_wrapper(html):
    for pat in [r'<!DOCTYPE html>\n', r'<html lang="es">\n', r'<head>\n', r'</head>\n', r'<body>\n', r'</body>\n', r'</html>\n?',
                r'<meta charset="UTF-8">\n', r'<meta name="viewport"[^>]*>\n']:
        html = re.sub(pat, '', html, count=1)
    return html

if __name__ == '__main__':
    render_pages()
    html = inline_libs(open(SRC, encoding='utf-8').read())
    # versión offline: páginas embebidas
    pages = {n: 'data:image/png;base64,' + base64.b64encode(open(os.path.join(PAGES_DIR, f'{n}.png'), 'rb').read()).decode() for n in PAGES}
    offline = html.replace('<div id="tour" hidden></div>', '<div id="tour" hidden></div>\n<script>window.MANUAL_PAGES=' + json.dumps(pages) + ';</script>', 1)
    out = os.path.join(HERE, 'QSM11_Visor_Tablet_Offline.html'); open(out, 'w', encoding='utf-8').write(offline)
    print('offline:', out, round(os.path.getsize(out) / 1e6, 1), 'MB')
    # versión web (artifact): páginas como archivos aparte
    adir = os.path.join(HERE, 'artifact'); os.makedirs(adir, exist_ok=True)
    open(os.path.join(adir, 'qsm11-visor.html'), 'w', encoding='utf-8').write(strip_wrapper(html))
    print('artifact:', round(os.path.getsize(os.path.join(adir, 'qsm11-visor.html')) / 1e6, 1), 'MB +', len(PAGES), 'páginas')
