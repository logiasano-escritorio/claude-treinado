# -*- coding: utf-8 -*-
"""
Instalador do repo sano-claude-skills.

USO
    python3 instalar.py            instala tudo (skills + memoria)
    python3 instalar.py --dry      mostra o que faria, sem escrever
    python3 instalar.py --skills   so as skills
    python3 instalar.py --memoria  so a memoria

O QUE FAZ
  1. Copia cada skill para ~/.claude/skills/<nome>/
  2. Registra o gatilho de cada uma no ~/.claude/CLAUDE.md
  3. Instala a memoria do projeto Sanologia em
     ~/.claude/projects/<projeto>/memory/ traduzindo o nome da pasta
     para o caminho DESTA maquina (o nome muda entre Windows e Mac)

Nao sobrescreve nada sem backup. Rodar duas vezes nao duplica.
Windows, Mac ou Linux. Sem dependencia externa.
"""
import io, os, re, shutil, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.expanduser("~"), ".claude")
DRY = "--dry" in sys.argv or "--dry-run" in sys.argv
SO_SKILLS = "--skills" in sys.argv
SO_MEMORIA = "--memoria" in sys.argv

# nome -> descricao curta que vai pro CLAUDE.md
DESCRICOES = {
    "adaptar-longform":
        "pipeline completo de adaptacao de long-form de concorrente estrangeiro",
    "raspar-adlibrary":
        "raspa a Meta Ad Library e vira notas no Obsidian com contagem de variacoes ativas",
}


def log(*a):
    print(*a)


# ------------------------------------------------------------------ skills
def bloco_de(nome):
    desc = DESCRICOES.get(nome, "skill " + nome)
    return ("<!-- %s:inicio -->\n"
            "# %s\n"
            "- **%s** (`~/.claude/skills/%s/SKILL.md`) - %s. Trigger: `/%s`\n"
            "When the user types `/%s`, invoke the Skill tool with "
            '`skill: "%s"` before doing anything else.\n'
            "<!-- %s:fim -->" % (nome, nome, nome, nome, desc, nome, nome, nome, nome))


def instalar_skill(nome):
    src = os.path.join(AQUI, "skills", nome)
    dst = os.path.join(BASE, "skills", nome)
    if not os.path.isdir(src):
        log("   ! nao achei " + src)
        return False
    if DRY:
        log("   [dry] instalaria %s -> %s" % (nome, dst))
        return True
    if os.path.isdir(dst):
        bak = dst + ".bak-" + time.strftime("%Y%m%d-%H%M%S")
        shutil.copytree(dst, bak)
        log("   backup da versao anterior -> " + os.path.basename(bak))
        # preserva um corpus local maior que o do repo
        c_old = os.path.join(bak, "scripts", "corpus-fb.txt")
        c_new = os.path.join(src, "scripts", "corpus-fb.txt")
        guardar = None
        if os.path.exists(c_old) and os.path.exists(c_new):
            a = io.open(c_old, encoding="utf-8", errors="replace").read()
            b = io.open(c_new, encoding="utf-8", errors="replace").read()
            if len(a) > len(b):
                guardar = a
        shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if guardar:
            io.open(os.path.join(dst, "scripts", "corpus-fb.txt"),
                    "w", encoding="utf-8").write(guardar)
            log("   corpus-fb.txt local era maior - mantido")
    else:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    n = sum(len(f) for _, _, f in os.walk(dst))
    log("   %-20s %d arquivos" % (nome, n))
    return True


def registrar_gatilhos(nomes):
    md = os.path.join(BASE, "CLAUDE.md")
    blocos = [bloco_de(n) for n in nomes]

    if not os.path.exists(md):
        if DRY:
            log("   [dry] criaria o CLAUDE.md com %d gatilhos" % len(blocos))
            return
        os.makedirs(BASE, exist_ok=True)
        io.open(md, "w", encoding="utf-8").write("\n\n".join(blocos) + "\n")
        log("   CLAUDE.md criado com %d gatilhos" % len(blocos))
        return

    txt = io.open(md, encoding="utf-8", errors="replace").read()
    original = txt
    novos, atualizados, mantidos = [], [], []

    for nome, bloco in zip(nomes, blocos):
        ini, fim = "<!-- %s:inicio -->" % nome, "<!-- %s:fim -->" % nome
        if ini in txt and fim in txt:
            atual = txt[txt.index(ini):txt.index(fim) + len(fim)]
            if atual.strip() == bloco.strip():
                mantidos.append(nome)
            else:
                txt = txt.replace(atual, bloco)
                atualizados.append(nome)
        elif ('skill: "%s"' % nome) in txt:
            mantidos.append(nome + " (registrado a mao, nao mexi)")
        else:
            sep = "" if txt.endswith("\n\n") else ("\n" if txt.endswith("\n") else "\n\n")
            txt = txt + sep + bloco + "\n"
            novos.append(nome)

    if DRY:
        log("   [dry] CLAUDE.md: %d novos, %d atualizados, %d ja ok"
            % (len(novos), len(atualizados), len(mantidos)))
        return
    if txt != original:
        shutil.copy2(md, md + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
        io.open(md, "w", encoding="utf-8").write(txt)
    for n in novos:
        log("   + gatilho: " + n)
    for n in atualizados:
        log("   ~ atualizado: " + n)
    for n in mantidos:
        log("   = ja estava ok: " + n)


# ----------------------------------------------------------------- memoria
def achar_pasta_memoria():
    """
    O Claude Code nomeia a pasta pelo caminho do projeto, e esse caminho muda
    entre maquinas. Descobre o nome correto NESTA maquina.
    """
    proj = os.path.join(BASE, "projects")
    if os.path.isdir(proj):
        for d in sorted(os.listdir(proj)):
            if d.lower().endswith("sanologia"):
                return os.path.join(proj, d, "memory"), d
    home = os.path.expanduser("~")
    for cand in [os.path.join(home, "Desktop", "Sanologia"),
                 os.path.join(home, "Sanologia"),
                 os.path.join(home, "Documents", "Sanologia")]:
        if os.path.isdir(cand):
            slug = cand.replace(":", "-").replace(os.sep, "-").replace("/", "-").lower()
            return os.path.join(proj, slug, "memory"), slug
    cand = os.path.join(home, "Desktop", "Sanologia")
    slug = cand.replace(":", "-").replace(os.sep, "-").replace("/", "-").lower()
    return os.path.join(proj, slug, "memory"), slug


def instalar_memoria():
    src = os.path.join(AQUI, "memory")
    if not os.path.isdir(src):
        log("   ! pasta memory/ nao encontrada no repo")
        return
    destino, slug = achar_pasta_memoria()
    arquivos = sorted(f for f in os.listdir(src) if f.endswith(".md"))
    ja = set()
    if os.path.isdir(destino):
        ja = set(f for f in os.listdir(destino) if f.endswith(".md"))

    novos = [f for f in arquivos if f not in ja and f != "MEMORY.md"]
    conf = [f for f in arquivos if f in ja and f != "MEMORY.md"]

    log("   projeto: " + slug)
    log("   destino: " + destino)
    log("   %d no repo | %d ja existem | %d novas | %d sobrescritas (com backup)"
        % (len(arquivos), len(ja), len(novos), len(conf)))

    if DRY:
        log("   [dry] nada escrito")
        return

    os.makedirs(destino, exist_ok=True)
    if conf:
        bak = destino + ".bak-" + time.strftime("%Y%m%d-%H%M%S")
        os.makedirs(bak, exist_ok=True)
        for f in conf:
            shutil.copy2(os.path.join(destino, f), os.path.join(bak, f))
        log("   backup das %d anteriores -> %s" % (len(conf), os.path.basename(bak)))

    for f in arquivos:
        if f != "MEMORY.md":
            shutil.copy2(os.path.join(src, f), os.path.join(destino, f))

    # o indice e MESCLADO, nunca sobrescrito
    idx = os.path.join(destino, "MEMORY.md")
    novo_idx = ""
    if os.path.exists(os.path.join(src, "MEMORY.md")):
        novo_idx = io.open(os.path.join(src, "MEMORY.md"),
                           encoding="utf-8", errors="replace").read()
    if os.path.exists(idx):
        atual = io.open(idx, encoding="utf-8", errors="replace").read()
        shutil.copy2(idx, idx + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
        linhas = [l.rstrip() for l in atual.split("\n")]
        tem = set(m.group(1) for m in
                  (re.search(r"\(([^)]+\.md)\)", l) for l in linhas) if m)
        add = []
        for l in novo_idx.split("\n"):
            m = re.search(r"\(([^)]+\.md)\)", l)
            if m and m.group(1) not in tem:
                add.append(l.rstrip())
        if add:
            io.open(idx, "w", encoding="utf-8").write(
                "\n".join(linhas + [""] + add).strip() + "\n")
            log("   MEMORY.md: %d linhas novas mescladas" % len(add))
        else:
            log("   MEMORY.md: nada novo a mesclar")
    elif novo_idx:
        io.open(idx, "w", encoding="utf-8").write(novo_idx)
        log("   MEMORY.md criado")

    log("   OK: %d memorias em %s"
        % (len([f for f in os.listdir(destino) if f.endswith(".md")]), destino))


# -------------------------------------------------------------------- main
def main():
    if DRY:
        log(">>> DRY RUN - nada sera escrito\n")

    skills = []
    d = os.path.join(AQUI, "skills")
    if os.path.isdir(d):
        skills = sorted(x for x in os.listdir(d)
                        if os.path.isfile(os.path.join(d, x, "SKILL.md")))

    if not SO_MEMORIA and skills:
        log("SKILLS")
        for s in skills:
            instalar_skill(s)
        log("")
        log("GATILHOS no CLAUDE.md")
        registrar_gatilhos(skills)
        log("")

    if not SO_SKILLS:
        log("MEMORIA (projeto Sanologia)")
        instalar_memoria()
        log("")

    if DRY:
        log("[dry] rode sem --dry pra aplicar.")
        return

    log("-" * 60)
    log("CONFERINDO")
    log("-" * 60)
    ok = True
    for s in skills:
        p = os.path.join(BASE, "skills", s, "SKILL.md")
        log(("  OK   " if os.path.exists(p) else "  FALHA  ") + s)
        ok = ok and os.path.exists(p)
    md = os.path.join(BASE, "CLAUDE.md")
    t = io.open(md, encoding="utf-8", errors="replace").read() if os.path.exists(md) else ""
    for s in skills:
        g = ('skill: "%s"' % s) in t
        log(("  OK   " if g else "  FALHA  ") + "gatilho " + s)
        ok = ok and g
    log("")
    log("Tudo pronto. Reinicie o Claude Code." if ok else "Algo falhou acima.")
    if skills:
        log("Skills: " + "  ".join("/" + s for s in skills))
    log("")
    log("Dependencias (so quando for usar cada uma):")
    log("   pip3 install DrissionPage                        # /raspar-adlibrary")
    log("   pip3 install google-genai pillow python-dotenv   # /adaptar-longform (imagens)")


if __name__ == "__main__":
    main()
