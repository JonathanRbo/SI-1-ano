"""
Gera automaticamente a landing page index.html
baseado nos arquivos do projeto SI-1-ano-main.

Uso: python gerar_landing.py

Arquitetura:
- Layout acordeao full-width (disciplina > aula > arquivos)
- Modal unico reutilizavel (codigo populado via JS)
- Conteudo dos arquivos em FILE_DATA (JS object), nao em HTML
- Busca, filtros por disciplina, colapso/expansao
- Escala para 200+ arquivos sem problemas
"""

import os
import json
import html as html_mod
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

# ── Config ──────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
IGNORE = {'.git', '__pycache__', 'node_modules', '.vscode'}
MAX_PREVIEW_LINES = 200
COLLAPSE_THRESHOLD = 4  # auto-expand se total disciplinas <= este valor

DISCIPLINAS = {
    'APPC': {
        'nome': 'Algoritmos de Programacao, Projetos e Computacao',
        'icone': 'iccon-terminal-1',
        'cor': '#a78bfa',
    },
    'ExpBD': {
        'nome': 'Experimentos Praticos de Banco de Dados',
        'icone': 'iccon-database-1',
        'cor': '#34d399',
    },
    'Projetos': {
        'nome': 'Projetos Especiais',
        'icone': 'iccon-rocket-1',
        'cor': '#fb923c',
    },
}

EXT_META = {
    '.py':  ('Python',   '#3b82f6'),
    '.sql': ('SQL',      '#22c55e'),
    '.pdf': ('PDF',      '#ef4444'),
    '.sb3': ('Scratch',  '#f59e0b'),
    '.png': ('Imagem',   '#a855f7'),
    '.jpg': ('Imagem',   '#a855f7'),
    '.md':  ('Markdown', '#6b7280'),
    '.txt': ('Texto',    '#6b7280'),
    '.csv': ('CSV',      '#06b6d4'),
    '.json': ('JSON',    '#f59e0b'),
    '.html': ('HTML',    '#ef4444'),
    '.css': ('CSS',      '#3b82f6'),
    '.js':  ('JS',       '#f59e0b'),
}

READABLE_EXT = {'.py', '.sql', '.md', '.txt', '.csv', '.json', '.html', '.css', '.js'}

# Links externos para arquivos especificos (nome_arquivo_lowercase -> url)
EXTERNAL_LINKS = {
    'cassino.sb3': 'https://scratch.mit.edu/projects/1293177850',
}


# ── Data ────────────────────────────────────────────────

@dataclass
class FileInfo:
    nome: str
    ext: str
    content: Optional[str]
    line_count: int
    truncated: bool


def make_id(*parts):
    raw = '-'.join(parts)
    return ''.join(c if c.isalnum() else '-' for c in raw).strip('-').lower()


def scan_project():
    structure = defaultdict(lambda: defaultdict(list))
    total_files = 0
    total_aulas = set()

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE)
        rel = Path(root).relative_to(BASE_DIR)
        parts = rel.parts

        if not parts or parts[0] in IGNORE:
            continue

        disc = parts[0]
        aula = parts[1] if len(parts) > 1 else '_root'

        for f in sorted(files):
            if f.startswith('.') or f in ('gerar_landing.py', 'index.html'):
                continue

            fp = Path(root) / f
            ext = fp.suffix.lower()
            content = None
            line_count = 0
            truncated = False

            if ext in READABLE_EXT:
                try:
                    raw = fp.read_text(encoding='utf-8', errors='replace')
                    all_lines = raw.split('\n')
                    line_count = len(all_lines)
                    if line_count > MAX_PREVIEW_LINES:
                        content = '\n'.join(all_lines[:MAX_PREVIEW_LINES])
                        truncated = True
                    else:
                        content = raw
                except Exception:
                    pass

            structure[disc][aula].append(FileInfo(
                nome=f, ext=ext, content=content,
                line_count=line_count, truncated=truncated,
            ))
            total_files += 1
            if aula != '_root' and aula.startswith('aula-'):
                total_aulas.add(f"{disc}/{aula}")

    return structure, total_files, len(total_aulas)


def ext_meta(ext):
    return EXT_META.get(ext, ('Arquivo', '#64748b'))


def format_date(aula_folder):
    if not aula_folder.startswith('aula-'):
        return aula_folder
    try:
        p = aula_folder.replace('aula-', '').split('-')
        d, m, y = int(p[0]), int(p[1]), int(p[2])
        meses = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        return f"{d:02d} {meses[m]} {y}"
    except Exception:
        return aula_folder


# ── Builders ────────────────────────────────────────────

def build_file_data_js(structure):
    data = {}
    for disc, aulas in structure.items():
        for aula, files in aulas.items():
            for f in files:
                if f.content is None:
                    continue
                fid = make_id(disc, aula, f.nome)
                label, color = ext_meta(f.ext)
                data[fid] = {
                    'name': f.nome,
                    'lang': label,
                    'color': color,
                    'lines': f.line_count,
                    'truncated': f.truncated,
                    'content': f.content,
                }
    return f'<script>var FILE_DATA={json.dumps(data, ensure_ascii=False)};</script>'


def build_file_row(disc, aula, f):
    fid = make_id(disc, aula, f.nome)
    label, color = ext_meta(f.ext)
    has_code = f.content is not None
    ext_link = EXTERNAL_LINKS.get(f.nome.lower())
    code_attr = f'data-code-id="{fid}"' if has_code else ''
    cursor = 'file-row cursor-pointer' if (has_code or ext_link) else 'file-row'

    info = ''
    if has_code:
        info = f'<span class="fs-2 xs-d-none" style="color:#484f58;">{f.line_count} linhas</span>'
    elif f.ext == '.pdf':
        info = '<span class="fs-2 xs-d-none" style="color:#484f58;">documento</span>'
    elif f.ext == '.sb3':
        info = '<span class="fs-2 xs-d-none" style="color:#484f58;">projeto interativo</span>'

    action_icon = ''
    if has_code:
        action_icon = '<span class="iccon-eye-1 fs-5 view-icon" style="color:#475569;"></span>'
    elif ext_link:
        action_icon = '<span class="iccon-external-1 fs-5 view-icon" style="color:#475569;"></span>'

    link_attr = f'data-ext-link="{html_mod.escape(ext_link)}"' if ext_link else ''

    return f'''<div class="{cursor} d-flex f-items-center f-gap-10 p-8-tb p-12-lr border-rd-6"
     data-fname="{html_mod.escape(f.nome.lower())}" data-ext="{f.ext}" data-disc="{disc}"
     {code_attr} {link_attr}>
    <span class="dot" style="background:{color};"></span>
    <span class="fs-5 fw-500 f-grow-1 fname-text" style="color:#c9d1d9;">{html_mod.escape(f.nome)}</span>
    {info}
    <span class="fs-2 fw-600 p-2-tb p-8-lr border-rd-4 xs-d-none" style="background:{color}18;color:{color};">{label}</span>
    {action_icon}
</div>'''


def build_aula_block(disc, aula, files, cor):
    date_label = format_date(aula) if aula != '_root' else 'Geral'
    aula_id = make_id(disc, aula, 'body')
    n = len(files)
    code_n = sum(1 for f in files if f.content is not None)

    rows = '\n'.join(build_file_row(disc, aula, f) for f in files)

    code_info = f' &bull; {code_n} com codigo' if code_n > 0 else ''

    return f'''<div class="aula-section m-5-b">
    <div class="aula-header d-flex f-items-center f-gap-10 p-10-tb p-15-lr border-rd-6 cursor-pointer"
         data-toggle="{aula_id}">
        <span class="iccon-calendar-1 fs-5" style="color:{cor};"></span>
        <span class="fs-5 fw-600" style="color:#e2e8f0;">{date_label}</span>
        <span class="fs-2" style="color:#64748b;">{n} arquivo{"s" if n != 1 else ""}{code_info}</span>
        <span class="chevron iccon-chevron-down-1 fs-4 m-auto-l" style="color:#475569;"></span>
    </div>
    <div class="aula-body d-none p-5-l" id="{aula_id}" style="border-left:2px solid {cor}22;">
        {rows}
    </div>
</div>'''


def build_discipline_section(disc, aulas, total_disc):
    info = DISCIPLINAS.get(disc, {'nome': disc, 'icone': 'iccon-folder-1', 'cor': '#64748b'})
    cor = info['cor']

    total_files = sum(len(f) for f in aulas.values())
    total_aulas_n = sum(1 for a in aulas if a.startswith('aula-'))
    total_code = sum(1 for files in aulas.values() for f in files if f.content is not None)

    body_id = f'disc-{disc}-body'
    # auto-expand se poucas disciplinas
    collapsed = 'd-none' if total_disc > COLLAPSE_THRESHOLD else ''

    # Se so tem _root (sem aulas), mostra arquivos diretamente
    is_flat = list(aulas.keys()) == ['_root']

    sorted_aulas = sorted(aulas.items(), key=lambda x: x[0], reverse=True)

    if is_flat:
        # Mostra arquivos diretamente sem sub-nivel
        flat_rows = '\n'.join(build_file_row(disc, a, f) for a, files in sorted_aulas for f in files)
        body_content = flat_rows
    else:
        aula_blocks = '\n'.join(build_aula_block(disc, a, files, cor) for a, files in sorted_aulas)
        body_content = f'''<div class="d-flex f-items-center f-justify-end f-gap-10 m-10-b p-5-lr">
            <button class="expand-all-btn fs-2 fw-500 cursor-pointer p-4-tb p-10-lr border-rd-4"
                    data-disc-body="{body_id}"
                    style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);color:#64748b;">
                Expandir tudo
            </button>
        </div>
        {aula_blocks}'''

    # Stats line - hide "0 aulas" and "0 codigos" if flat
    if is_flat:
        stats_html = f'<span class="fs-3 fw-500" style="color:#475569;">{total_files} projeto{"s" if total_files != 1 else ""}</span>'
    else:
        stats_html = f'''<span class="fs-3 fw-500" style="color:#475569;">{total_files} arquivo{"s" if total_files != 1 else ""}</span>
                <span class="fs-3 fw-500" style="color:#475569;">{total_aulas_n} aula{"s" if total_aulas_n != 1 else ""}</span>
                <span class="fs-3 fw-500" style="color:#475569;">{total_code} codigo{"s" if total_code != 1 else ""}</span>'''

    return f'''<section class="disc-section" id="disc-{disc}" data-disc="{disc}"
     style="border-bottom:1px solid rgba(255,255,255,0.04);">
    <div class="disc-header d-flex f-items-center f-justify-between f-gap-15 p-20-tb p-25-lr xs-p-15-all cursor-pointer"
         data-toggle="{body_id}">
        <div class="d-flex f-items-center f-gap-15">
            <div class="d-flex f-items-center f-justify-center border-rd-10" style="width:44px;height:44px;background:{cor}15;">
                <span class="{info['icone']} fs-10" style="color:{cor};"></span>
            </div>
            <div>
                <span class="fs-8 fw-700" style="color:#f1f5f9;">{disc}</span>
                <span class="fs-3 d-block xs-d-none" style="color:#64748b;">{info['nome']}</span>
            </div>
        </div>
        <div class="d-flex f-items-center f-gap-15">
            <div class="d-flex f-gap-15 xs-f-gap-10 xs-d-none">
                {stats_html}
            </div>
            <span class="fs-4 fw-600 xs-d-block d-none" style="color:{cor};">{total_files}</span>
            <span class="chevron iccon-chevron-down-1 fs-7" style="color:#475569;"></span>
        </div>
    </div>
    <div class="disc-body {collapsed} p-10-lr p-15-b xs-p-5-lr" id="{body_id}">
        {body_content}
    </div>
</section>'''


def build_nav(structure):
    links = ''
    for disc in sorted(structure.keys()):
        info = DISCIPLINAS.get(disc, {'cor': '#64748b'})
        links += f'<a href="#disc-{disc}" class="nav-disc-link fs-3 fw-600 p-4-tb p-12-lr border-rd-6" data-nav-disc="{disc}" style="color:{info["cor"]};transition:background 0.15s;">{disc}</a>\n'

    pills = '<button class="filter-pill active fs-3 fw-600 p-5-tb p-14-lr border-rd-20 cursor-pointer" data-filter="all">Todas</button>\n'
    for disc in sorted(structure.keys()):
        info = DISCIPLINAS.get(disc, {'cor': '#64748b'})
        pills += f'<button class="filter-pill fs-3 fw-600 p-5-tb p-14-lr border-rd-20 cursor-pointer" data-filter="{disc}" data-pill-color="{info["cor"]}">{disc}</button>\n'

    return f'''<nav class="main-nav ps-sticky d-flex f-items-center f-justify-between f-gap-15 p-12-tb p-25-lr xs-p-10-tb xs-p-15-lr"
     id="main-nav" style="top:0;z-index:100;background:#0a0f1aee;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.04);transform:translateY(-100%);transition:transform 0.3s;">
    <span class="fs-7 fw-700 xs-d-none" style="color:#f1f5f9;">SI 1 Ano</span>
    <div class="d-flex f-gap-8 xs-d-none" id="nav-links">
        {links}
    </div>
    <div class="d-flex f-gap-8 f-wrap xs-f-grow-1" id="filter-pills">
        {pills}
    </div>
    <input type="text" id="search-input" class="fs-5 p-8-tb p-15-lr border-rd-8 xs-w-100"
           placeholder="Buscar arquivo..."
           style="background:#1a2035;border:1px solid #2a3050;color:#e2e8f0;outline:none;width:220px;">
    <span class="kbd-hint xs-d-none">Ctrl+K</span>
</nav>'''


def build_hero(total_files, total_aulas, total_disc, total_code):
    now = datetime.now().strftime('%d/%m/%Y %H:%M')
    return f'''<section class="p-80-tb xs-p-50-tb f-items-center text-center ps-relative" id="hero">
    <div class="hero-bg"></div>
    <div class="w-800px xs-w-100 xs-p-15-lr">
        <div class="d-flex f-items-center f-justify-center f-gap-8 m-25-b wow fadeIn">
            <div class="live-dot"></div>
            <span class="fs-3 fw-500 text-uppercase ls-3" style="color:#64748b;">{now}</span>
        </div>
        <h1 class="fs-16 xs-fs-14 fw-900 lh-1-1 m-10-b wow fadeInUp hero-title">SI &mdash; 1 Ano</h1>
        <p class="fs-9 xs-fs-7 fw-400 m-40-b wow fadeInUp" data-wow-delay="0.1s" style="color:#64748b;">
            Sistemas de Informacao &mdash; Dashboard de Progresso
        </p>
        <div class="d-flex f-justify-center f-gap-15 xs-f-gap-8 f-wrap wow fadeInUp" data-wow-delay="0.2s">
            <div class="stat-box border-rd-12 p-15-tb p-25-lr xs-p-10-all text-center">
                <span class="fs-13 xs-fs-11 fw-800 d-block lh-1-1" style="color:#a78bfa;">{total_files}</span>
                <span class="fs-2 fw-600 text-uppercase ls-2 m-3-t d-block" style="color:#475569;">Arquivos</span>
            </div>
            <div class="stat-box border-rd-12 p-15-tb p-25-lr xs-p-10-all text-center">
                <span class="fs-13 xs-fs-11 fw-800 d-block lh-1-1" style="color:#38bdf8;">{total_code}</span>
                <span class="fs-2 fw-600 text-uppercase ls-2 m-3-t d-block" style="color:#475569;">Codigos</span>
            </div>
        </div>
        <div class="m-40-t wow fadeIn" data-wow-delay="0.4s">
            <span class="iccon-chevron-down-1 fs-10 animated infinite pulse" style="color:#1e293b;"></span>
        </div>
    </div>
</section>'''


def build_code_modal():
    return '''<div data-modal="code-viewer" class="modal-dialog" aria-hidden="true">
    <div class="dialog-content">
        <div class="dialog-backdrop" data-modal-hide></div>
        <div class="dialog-inline w-900px xs-w-100">
            <button class="dialog-close" data-modal-hide aria-label="Fechar">
                <span class="iccon-close-1"></span>
            </button>
            <div class="modal-popup border-rd-12" style="background:#0d1117;padding:0;overflow:hidden;" id="code-modal-inner">
                <div class="p-40-all text-center" style="color:#484f58;">
                    <span class="iccon-file-1 fs-14 d-block m-10-b"></span>
                    <span class="fs-5">Selecione um arquivo</span>
                </div>
            </div>
        </div>
    </div>
</div>'''


def build_js():
    return '''<script>
(function(){
    var nav = document.getElementById('main-nav');
    var hero = document.getElementById('hero');

    // ── Collapse toggle ──
    document.addEventListener('click', function(e){
        var toggler = e.target.closest('[data-toggle]');
        if(!toggler) return;
        var id = toggler.getAttribute('data-toggle');
        var el = document.getElementById(id);
        if(!el) return;
        el.classList.toggle('d-none');
        var ch = toggler.querySelector('.chevron');
        if(ch) ch.style.transform = el.classList.contains('d-none') ? '' : 'rotate(180deg)';
    });

    // ── Expand all within a discipline ──
    document.addEventListener('click', function(e){
        var btn = e.target.closest('.expand-all-btn');
        if(!btn) return;
        e.stopPropagation();
        var bodyId = btn.getAttribute('data-disc-body');
        var body = document.getElementById(bodyId);
        if(!body) return;
        var allBodies = body.querySelectorAll('.aula-body');
        var allHidden = Array.from(allBodies).every(function(b){ return b.classList.contains('d-none'); });
        allBodies.forEach(function(b){
            if(allHidden) b.classList.remove('d-none');
            else b.classList.add('d-none');
        });
        body.querySelectorAll('.aula-header .chevron').forEach(function(ch){
            ch.style.transform = allHidden ? 'rotate(180deg)' : '';
        });
        btn.textContent = allHidden ? 'Colapsar tudo' : 'Expandir tudo';
    });

    // ── Filter pills ──
    var pills = document.querySelectorAll('.filter-pill');
    var sections = document.querySelectorAll('.disc-section');
    pills.forEach(function(pill){
        pill.addEventListener('click', function(){
            pills.forEach(function(p){ p.classList.remove('active'); });
            pill.classList.add('active');
            var filter = pill.getAttribute('data-filter');
            sections.forEach(function(s){
                if(filter === 'all' || s.getAttribute('data-disc') === filter){
                    s.classList.remove('d-none');
                } else {
                    s.classList.add('d-none');
                }
            });
        });
    });

    // ── Nav disc links (scroll + expand with offset) ──
    document.querySelectorAll('.nav-disc-link').forEach(function(link){
        link.addEventListener('click', function(e){
            e.preventDefault();
            var disc = link.getAttribute('data-nav-disc');
            var sec = document.getElementById('disc-' + disc);
            if(!sec) return;
            sec.classList.remove('d-none');
            var body = document.getElementById('disc-' + disc + '-body');
            if(body) body.classList.remove('d-none');
            var ch = sec.querySelector('.disc-header .chevron');
            if(ch) ch.style.transform = 'rotate(180deg)';
            var offset = nav ? nav.offsetHeight + 10 : 0;
            var top = sec.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({top: top, behavior:'smooth'});
        });
    });

    // ── Search ──
    var searchInput = document.getElementById('search-input');
    var fileRows = document.querySelectorAll('.file-row');
    var debounceTimer;
    searchInput.addEventListener('input', function(){
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(doSearch, 200);
    });

    function doSearch(){
        var q = searchInput.value.trim().toLowerCase();
        if(!q){
            // restore: show all rows, collapse aulas
            fileRows.forEach(function(r){ r.classList.remove('d-none','search-match'); });
            document.querySelectorAll('.aula-body').forEach(function(b){ b.classList.add('d-none'); });
            document.querySelectorAll('.aula-header .chevron').forEach(function(c){ c.style.transform=''; });
            document.querySelectorAll('.disc-section').forEach(function(s){ s.classList.remove('d-none'); });
            // re-apply pill filter
            var activePill = document.querySelector('.filter-pill.active');
            if(activePill){
                var f = activePill.getAttribute('data-filter');
                if(f !== 'all'){
                    sections.forEach(function(s){
                        if(s.getAttribute('data-disc') !== f) s.classList.add('d-none');
                    });
                }
            }
            return;
        }
        // show all sections during search
        sections.forEach(function(s){ s.classList.remove('d-none'); });
        // expand all disc bodies
        document.querySelectorAll('.disc-body').forEach(function(b){
            b.classList.remove('d-none');
        });
        document.querySelectorAll('.disc-header .chevron').forEach(function(c){ c.style.transform='rotate(180deg)'; });

        fileRows.forEach(function(r){
            var fname = r.getAttribute('data-fname') || '';
            if(fname.indexOf(q) !== -1){
                r.classList.remove('d-none');
                r.classList.add('search-match');
            } else {
                r.classList.add('d-none');
                r.classList.remove('search-match');
            }
        });
        // show/hide aula bodies based on visible rows
        document.querySelectorAll('.aula-section').forEach(function(as){
            var body = as.querySelector('.aula-body');
            var hasVisible = body && body.querySelector('.file-row:not(.d-none)');
            if(hasVisible){
                body.classList.remove('d-none');
                var ch = as.querySelector('.aula-header .chevron');
                if(ch) ch.style.transform = 'rotate(180deg)';
            } else if(body){
                body.classList.add('d-none');
            }
        });
        // hide disc sections with no results
        sections.forEach(function(s){
            var visibleRow = s.querySelector('.file-row:not(.d-none)');
            if(!visibleRow) s.classList.add('d-none');
        });
    }

    // ── Ctrl+K shortcut ──
    document.addEventListener('keydown', function(e){
        if((e.ctrlKey || e.metaKey) && e.key === 'k'){
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
        if(e.key === 'Escape' && document.activeElement === searchInput){
            searchInput.blur();
            searchInput.value = '';
            doSearch();
        }
    });

    // ── Scroll to top ──
    var scrollBtn = document.getElementById('scroll-top-btn');
    if(scrollBtn){
        window.addEventListener('scroll', function(){
            scrollBtn.classList.toggle('visible', window.scrollY > 400);
        });
        scrollBtn.addEventListener('click', function(){
            window.scrollTo({top:0, behavior:'smooth'});
        });
    }

    // ── External links (e.g. Scratch projects) ──
    document.addEventListener('click', function(e){
        var row = e.target.closest('.file-row[data-ext-link]');
        if(!row) return;
        if(row.getAttribute('data-code-id')) return; // code viewer takes priority
        window.open(row.getAttribute('data-ext-link'), '_blank', 'noopener');
    });

    // ── Code modal ──
    var modalEl = document.querySelector('[data-modal="code-viewer"]');
    var modalInner = document.getElementById('code-modal-inner');

    function escHtml(s){
        var d = document.createElement('div');
        d.appendChild(document.createTextNode(s));
        return d.innerHTML;
    }

    document.addEventListener('click', function(e){
        var row = e.target.closest('.file-row[data-code-id]');
        if(!row) return;
        var id = row.getAttribute('data-code-id');
        if(!FILE_DATA || !FILE_DATA[id]) return;
        var f = FILE_DATA[id];

        var lines = f.content.split('\\n');
        var lineNums = '';
        for(var i = 1; i <= lines.length; i++) lineNums += '<span>' + i + '</span>';

        var truncBanner = '';
        if(f.truncated){
            truncBanner = '<div class="truncation-banner">Mostrando ' + lines.length + ' de ' + f.lines + ' linhas &bull; Abra o arquivo original para ver tudo</div>';
        }

        modalInner.innerHTML =
            '<div class="d-flex f-items-center f-gap-10 p-12-tb p-20-lr xs-p-10-all" style="background:#161b22;border-bottom:1px solid #21262d;">' +
                '<div class="d-flex f-gap-6">' +
                    '<span id="modal-close-dot" style="width:12px;height:12px;border-radius:50%;background:#ff5f57;display:inline-block;cursor:pointer;" title="Fechar"></span>' +
                    '<span style="width:12px;height:12px;border-radius:50%;background:#febc2e;display:inline-block;"></span>' +
                    '<span style="width:12px;height:12px;border-radius:50%;background:#28c840;display:inline-block;"></span>' +
                '</div>' +
                '<span class="fs-4 fw-500 m-auto-lr" style="color:#8b949e;">' + escHtml(f.name) + '</span>' +
                '<span class="fs-2 fw-600 p-3-tb p-8-lr border-rd-4" style="background:' + f.color + '22;color:' + f.color + ';">' + escHtml(f.lang) + '</span>' +
                '<button class="copy-btn" id="copy-code-btn" data-code-id="' + id + '">Copiar</button>' +
            '</div>' +
            '<div class="code-viewer" style="overflow:auto;max-height:70vh;padding:16px 0;">' +
                '<table style="border-collapse:collapse;width:100%;font-family:\\\'JetBrains Mono\\\',\\\'Fira Code\\\',\\\'Cascadia Code\\\',Consolas,monospace;font-size:13px;line-height:1.6;">' +
                    '<tr>' +
                        '<td class="line-nums" style="padding:0 12px 0 16px;text-align:right;user-select:none;vertical-align:top;color:#484f58;border-right:1px solid #21262d;white-space:pre;">' + lineNums + '</td>' +
                        '<td style="padding:0 16px;vertical-align:top;"><pre style="margin:0;color:#e6edf3;white-space:pre;overflow-x:auto;tab-size:4;">' + escHtml(f.content) + '</pre></td>' +
                    '</tr>' +
                '</table>' +
            '</div>' +
            truncBanner +
            '<div class="d-flex f-items-center f-justify-between p-8-tb p-20-lr" style="background:#161b22;border-top:1px solid #21262d;">' +
                '<span class="fs-2" style="color:#484f58;">' + escHtml(f.lang) + ' &bull; ' + f.lines + ' linhas</span>' +
                '<span class="fs-2" style="color:#484f58;">UTF-8</span>' +
            '</div>';

        // Open modal
        if(modalEl && modalEl._a11yDialog){
            modalEl._a11yDialog.show();
        } else {
            // fallback: dispatch click on a hidden trigger
            var tmpBtn = document.createElement('button');
            tmpBtn.setAttribute('data-modal-show','code-viewer');
            tmpBtn.style.display = 'none';
            document.body.appendChild(tmpBtn);
            tmpBtn.click();
            document.body.removeChild(tmpBtn);
        }
    });

    // ── Close modal via red dot ──
    document.addEventListener('click', function(e){
        if(e.target.id === 'modal-close-dot'){
            if(modalEl && modalEl._a11yDialog) modalEl._a11yDialog.hide();
        }
    });

    // ── Copy code button ──
    document.addEventListener('click', function(e){
        var btn = e.target.closest('#copy-code-btn');
        if(!btn) return;
        var cid = btn.getAttribute('data-code-id');
        if(!FILE_DATA || !FILE_DATA[cid]) return;
        navigator.clipboard.writeText(FILE_DATA[cid].content).then(function(){
            btn.textContent = 'Copiado!';
            btn.classList.add('copied');
            setTimeout(function(){ btn.textContent = 'Copiar'; btn.classList.remove('copied'); }, 2000);
        });
    });

    // ── Dynamic pill color ──
    pills.forEach(function(pill){
        var c = pill.getAttribute('data-pill-color');
        if(c){
            pill.style.setProperty('--pill-color', c);
            pill.style.setProperty('--pill-bg', c + '20');
        }
    });

    // ── Sticky nav (show after hero) ──
    if(nav && hero){
        var observer = new IntersectionObserver(function(entries){
            entries.forEach(function(entry){
                nav.style.transform = entry.isIntersecting ? 'translateY(-100%)' : 'translateY(0)';
            });
        }, { threshold: 0.1 });
        observer.observe(hero);
    }
})();
</script>'''


def build_css():
    return '''<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    body { background:#0a0f1a; color:#e2e8f0; font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; }

    /* Hero */
    .hero-title {
        background:linear-gradient(135deg,#a78bfa 0%,#34d399 50%,#fb923c 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    }
    .hero-bg { position:absolute; inset:0; z-index:-1; overflow:hidden; }
    .hero-bg::before {
        content:''; position:absolute; width:600px; height:600px; top:-200px; left:-100px;
        background:radial-gradient(circle,rgba(167,139,250,0.07) 0%,transparent 70%);
    }
    .hero-bg::after {
        content:''; position:absolute; width:500px; height:500px; bottom:-150px; right:-100px;
        background:radial-gradient(circle,rgba(52,211,153,0.05) 0%,transparent 70%);
    }

    /* Stats */
    .stat-box {
        background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05);
        transition:transform 0.2s,border-color 0.2s;
    }
    .stat-box:hover { transform:translateY(-2px); border-color:rgba(255,255,255,0.1); }

    /* Pulse dot */
    .live-dot {
        width:6px; height:6px; border-radius:50%; background:#34d399;
        animation:dot-pulse 2s infinite;
    }
    @keyframes dot-pulse {
        0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(52,211,153,0.4); }
        50% { opacity:.7; box-shadow:0 0 0 6px rgba(52,211,153,0); }
    }

    /* Disc/Aula headers */
    .disc-header, .aula-header { user-select:none; transition:background 0.15s; }
    .disc-header:hover { background:rgba(255,255,255,0.02); }
    .aula-header:hover { background:rgba(255,255,255,0.03); }
    .chevron { transition:transform 0.2s; }

    /* File rows */
    .file-row { border:1px solid transparent; transition:all 0.12s; }
    .file-row.cursor-pointer:hover { background:rgba(255,255,255,0.03)!important; border-color:rgba(255,255,255,0.06)!important; }
    .file-row.cursor-pointer:hover .view-icon { color:#a78bfa!important; }
    .file-row.search-match { background:rgba(167,139,250,0.04)!important; }
    .dot { width:8px; height:8px; border-radius:50%; display:inline-block; flex-shrink:0; }

    /* Filter pills */
    .filter-pill {
        background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
        color:#64748b; transition:all 0.15s;
    }
    .filter-pill:hover { border-color:rgba(255,255,255,0.15); color:#94a3b8; }
    .filter-pill.active { background:rgba(167,139,250,0.15); border-color:#a78bfa; color:#a78bfa; }

    /* Nav disc links */
    .nav-disc-link:hover { background:rgba(255,255,255,0.04); text-decoration:none; }

    /* Code viewer */
    .code-viewer::-webkit-scrollbar { width:6px; height:6px; }
    .code-viewer::-webkit-scrollbar-track { background:#0d1117; }
    .code-viewer::-webkit-scrollbar-thumb { background:#21262d; border-radius:3px; }
    .code-viewer::-webkit-scrollbar-thumb:hover { background:#30363d; }
    .line-nums span { display:block; }

    /* Truncation */
    .truncation-banner {
        text-align:center; padding:12px; background:#161b22;
        color:#8b949e; border-top:1px solid #21262d; font-size:12px;
    }

    /* Modal override */
    .modal-popup { background:transparent!important; }
    [data-modal="code-viewer"] .dialog-close { display:none; }

    /* Search */
    #search-input::placeholder { color:#475569; }
    #search-input:focus { border-color:#a78bfa; }

    /* Scroll to top */
    .scroll-top {
        position:fixed; bottom:30px; right:30px; z-index:99;
        width:44px; height:44px; border-radius:50%;
        background:rgba(167,139,250,0.15); border:1px solid rgba(167,139,250,0.3);
        color:#a78bfa; cursor:pointer; font-size:20px;
        opacity:0; transform:translateY(10px); transition:all 0.3s;
        display:flex; align-items:center; justify-content:center;
        backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px);
    }
    .scroll-top.visible { opacity:1; transform:translateY(0); }
    .scroll-top:hover { background:rgba(167,139,250,0.25); border-color:#a78bfa; }

    /* Copy button */
    .copy-btn {
        background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);
        color:#8b949e; cursor:pointer; padding:4px 12px; border-radius:6px;
        font-size:12px; transition:all 0.15s;
    }
    .copy-btn:hover { background:rgba(255,255,255,0.1); color:#e6edf3; }
    .copy-btn.copied { background:rgba(52,211,153,0.15); border-color:#34d399; color:#34d399; }

    /* Kbd hint */
    .kbd-hint {
        font-size:10px; color:#475569; background:rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.08); border-radius:4px;
        padding:1px 6px; font-family:'JetBrains Mono',monospace;
    }

    /* Active pill dynamic color */
    .filter-pill.active[data-pill-color] { background:var(--pill-bg); border-color:var(--pill-color); color:var(--pill-color); }
</style>'''


# ── Assembler ───────────────────────────────────────────

def assemble_html(structure, total_files, total_aulas):
    total_disc = len([d for d in structure if d in DISCIPLINAS and d != 'Projetos'])
    total_code = sum(1 for d in structure.values() for a in d.values() for f in a if f.content is not None)

    disc_count = len(structure)
    sections_html = '\n'.join(
        build_discipline_section(d, a, disc_count)
        for d, a in sorted(structure.items())
    )

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Dashboard de progresso do curso Sistemas de Informacao - 1 Ano. {total_files} arquivos, {total_code} com codigo.">
    <meta name="theme-color" content="#0a0f1a">
    <meta property="og:title" content="SI - 1 Ano | Dashboard">
    <meta property="og:description" content="Sistemas de Informacao - Dashboard de Progresso com {total_files} arquivos organizados por disciplina e aula.">
    <meta property="og:type" content="website">
    <title>SI - 1 Ano | Dashboard</title>
    <link rel="stylesheet" href="https://cdn.squeleton.dev/squeleton.v4.min.css">
    <script src="https://cdn.squeleton.dev/squeleton-main.v4.min.js"></script>
    {build_css()}
</head>
<body>

{build_nav(structure)}

{build_hero(total_files, total_aulas, total_disc, total_code)}

<main class="container p-30-tb xs-p-15-tb" id="content">
    <div class="text-center m-40-b xs-m-20-b">
        <h2 class="fs-12 xs-fs-10 fw-800 m-8-b wow fadeInUp" style="color:#f1f5f9;">Disciplinas & Arquivos</h2>
        <p class="fs-7 xs-fs-5 wow fadeInUp" data-wow-delay="0.1s" style="color:#475569;">Clique em qualquer arquivo de codigo para visualizar</p>
    </div>
    <div class="border-rd-14" style="background:#0f1525;border:1px solid rgba(255,255,255,0.04);overflow:hidden;">
        {sections_html}
    </div>
</main>

<button class="scroll-top" id="scroll-top-btn" aria-label="Voltar ao topo">
    <span class="iccon-chevron-up-1"></span>
</button>

<footer class="p-25-tb text-center" style="border-top:1px solid rgba(255,255,255,0.04);">
    <p class="fs-3" style="color:#334155;">
        <strong>{total_files}</strong> arquivos &bull; <strong>{total_code}</strong> com codigo &bull;
        <code style="background:#1e293b;padding:2px 8px;border-radius:4px;font-size:11px;">python gerar_landing.py</code>
    </p>
</footer>

{build_code_modal()}
{build_file_data_js(structure)}
<script src="https://cdn.squeleton.dev/squeleton-scripts.v4.min.js"></script>
{build_js()}
</body>
</html>'''


# ── Main ────────────────────────────────────────────────

def main():
    structure, total_files, total_aulas = scan_project()
    output = BASE_DIR / 'index.html'
    output.write_text(assemble_html(structure, total_files, total_aulas), encoding='utf-8')

    total_code = sum(1 for d in structure.values() for a in d.values() for f in a if f.content is not None)
    print(f"Landing page gerada: {output}")
    print(f"  {total_files} arquivos | {total_aulas} aulas | {total_code} com codigo visivel")


if __name__ == '__main__':
    main()
