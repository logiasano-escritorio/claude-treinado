# -*- coding: utf-8 -*-
"""
Instalador do claude-treinado — replica o ambiente Claude Code numa maquina nova.

USO
    python3 instalar.py              instala tudo
    python3 instalar.py --dry        mostra o que faria, sem escrever
    python3 instalar.py --skills     so skills/ commands/ agents/
    python3 instalar.py --memoria    so as memorias
    python3 instalar.py --configs    so CLAUDE.md / AGENTS_CATALOG.md / settings.json

O QUE VAI PARA ONDE
    claude/skills/    -> ~/.claude/skills/
    claude/commands/  -> ~/.claude/commands/
    claude/agents/    -> ~/.claude/agents/
    claude/memory/<projeto>/ -> ~/.claude/projects/<projeto-traduzido>/memory/
    claude/CLAUDE.md etc     -> ~/.claude/

Nada e sobrescrito sem backup com timestamp. Rodar duas vezes nao duplica.
Windows, Mac ou Linux. Sem dependencia externa.
"""
import io, os, re, shutil, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(AQUI, "claude")
BASE = os.path.join(os.path.expanduser("~"), ".claude")

DRY = "--dry" in sys.argv or "--dry-run" in sys.argv
FLAGS = [a for a in sys.argv[1:] if a.startswith("--") and a not in ("--dry", "--dry-run")]
def quer(x):
    return not FLAGS or ("--" + x) in FLAGS

IGN = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "*.bak", "*.bak-*")
CARIMBO = time.strftime("%Y%m%d-%H%M%S")


def backup(p):
    """Copia p para p.bak-<timestamp>. Devolve o caminho do backup."""
    b = p + ".bak-" + CARIMBO
    if os.path.isdir(p):
        shutil.copytree(p, b)
    else:
        shutil.copy2(p, b)
    return b


# --------------------------------------------------------------- pastas
def instalar_pasta(nome):
    src = os.path.join(SRC, nome)
    dst = os.path.join(BASE, nome)
    if not os.path.isdir(src):
        return
    n = sum(len(f) for _, _, f in os.walk(src))
    if DRY:
        print("   [dry] %-10s %d arquivos -> %s" % (nome, n, dst))
        return
    if os.path.isdir(dst):
        # preserva o que existe na maquina e nao vem no repo
        b = backup(dst)
        print("   backup: %s" % os.path.basename(b))
        for root, dirs, files in os.walk(src):
            rel = os.path.relpath(root, src)
            alvo = os.path.join(dst, rel) if rel != "." else dst
            os.makedirs(alvo, exist_ok=True)
            for f in files:
                if f.endswith((".pyc",)) or f == ".DS_Store":
                    continue
                shutil.copy2(os.path.join(root, f), os.path.join(alvo, f))
    else:
        shutil.copytree(src, dst, ignore=IGN)
    print("   %-10s %d arquivos" % (nome, n))


# --------------------------------------------------------------- configs
def instalar_configs():
    for f in ["CLAUDE.md", "AGENTS_CATALOG.md", "settings.json", "mcp.json"]:
        src = os.path.join(SRC, f)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(BASE, f)
        if DRY:
            existe = " (ja existe, faria backup)" if os.path.exists(dst) else ""
            print("   [dry] %s%s" % (f, existe))
            continue
        os.makedirs(BASE, exist_ok=True)
        if os.path.exists(dst):
            atual = io.open(dst, encoding="utf-8", errors="replace").read()
            novo = io.open(src, encoding="utf-8", errors="replace").read()
            if atual.strip() == novo.strip():
                print("   = %s ja identico" % f)
                continue
            backup(dst)
            print("   ~ %s atualizado (backup ao lado)" % f)
        else:
            print("   + %s" % f)
        shutil.copy2(src, dst)


# --------------------------------------------------------------- memoria
def traduzir_projeto(nome_original):
    """
    O Claude Code nomeia a pasta pelo caminho do projeto, entao o nome muda
    entre maquinas. Descobre o equivalente NESTA maquina.
    """
    proj = os.path.join(BASE, "projects")
    # sufixo significativo: "...-desktop-sanologia" -> "sanologia"
    cauda = re.split(r"[-_]", nome_original.lower())
    cauda = [c for c in cauda if c and c not in
             ("c", "users", "user", "desktop", "documents", "home", "projetos")]
    alvo = "-".join(cauda[-2:]) if len(cauda) >= 2 else (cauda[-1] if cauda else "")

    if os.path.isdir(proj):
        for d in sorted(os.listdir(proj)):
            dl = d.lower()
            if alvo and dl.endswith(alvo):
                return os.path.join(proj, d, "memory"), d
            if cauda and dl.endswith(cauda[-1]):
                return os.path.join(proj, d, "memory"), d
    # nao existe ainda: deriva do caminho real, se a pasta do projeto existir
    home = os.path.expanduser("~")
    if cauda:
        for raiz in [os.path.join(home, "Desktop"), home, os.path.join(home, "Documents")]:
            if not os.path.isdir(raiz):
                continue
            for x in os.listdir(raiz):
                if x.lower() == cauda[-1]:
                    p = os.path.join(raiz, x)
                    slug = p.replace(":", "-").replace(os.sep, "-").replace("/", "-").lower()
                    return os.path.join(proj, slug, "memory"), slug
    return os.path.join(proj, nome_original, "memory"), nome_original + " (nome original)"


def mesclar_indice(idx, novo_idx):
    """MEMORY.md e mesclado linha a linha: memoria local nunca some."""
    atual = io.open(idx, encoding="utf-8", errors="replace").read()
    backup(idx)
    linhas = [l.rstrip() for l in atual.split("\n")]
    tem = set(m.group(1) for m in
              (re.search(r"\(([^)]+\.md)\)", l) for l in linhas) if m)
    add = [l.rstrip() for l in novo_idx.split("\n")
           if re.search(r"\(([^)]+\.md)\)", l)
           and re.search(r"\(([^)]+\.md)\)", l).group(1) not in tem]
    if add:
        io.open(idx, "w", encoding="utf-8").write(
            "\n".join(linhas + [""] + add).strip() + "\n")
    return len(add)


def instalar_memoria():
    raiz = os.path.join(SRC, "memory")
    if not os.path.isdir(raiz):
        return
    for p in sorted(os.listdir(raiz)):
        origem = os.path.join(raiz, p)
        if not os.path.isdir(origem):
            continue
        arqs = sorted(f for f in os.listdir(origem) if f.endswith(".md"))
        if not arqs:
            continue
        destino, slug = traduzir_projeto(p)
        ja = set(f for f in os.listdir(destino)
                 if f.endswith(".md")) if os.path.isdir(destino) else set()
        novos = [f for f in arqs if f not in ja and f != "MEMORY.md"]
        conf = [f for f in arqs if f in ja and f != "MEMORY.md"]

        print("   %s" % slug)
        print("      %d no repo | %d ja la | %d novas | %d sobrescritas"
              % (len(arqs), len(ja), len(novos), len(conf)))
        if DRY:
            continue

        os.makedirs(destino, exist_ok=True)
        if conf:
            b = destino + ".bak-" + CARIMBO
            os.makedirs(b, exist_ok=True)
            for f in conf:
                shutil.copy2(os.path.join(destino, f), os.path.join(b, f))
        for f in arqs:
            if f != "MEMORY.md":
                shutil.copy2(os.path.join(origem, f), os.path.join(destino, f))

        idx = os.path.join(destino, "MEMORY.md")
        src_idx = os.path.join(origem, "MEMORY.md")
        if os.path.exists(src_idx):
            novo_idx = io.open(src_idx, encoding="utf-8", errors="replace").read()
            if os.path.exists(idx):
                n = mesclar_indice(idx, novo_idx)
                print("      MEMORY.md: %d linhas mescladas" % n)
            else:
                io.open(idx, "w", encoding="utf-8").write(novo_idx)
                print("      MEMORY.md criado")


# ------------------------------------------------------------------ main
def main():
    if not os.path.isdir(SRC):
        print("ERRO: nao achei a pasta claude/ ao lado do instalador.")
        print("Rode de dentro do repo clonado.")
        sys.exit(1)

    if DRY:
        print(">>> DRY RUN - nada sera escrito\n")

    if quer("skills"):
        print("SKILLS, COMMANDS E AGENTES")
        for d in ["skills", "commands", "agents"]:
            instalar_pasta(d)
        print("")

    if quer("configs"):
        print("CONFIGURACOES")
        instalar_configs()
        print("")

    if quer("memoria"):
        print("MEMORIAS")
        instalar_memoria()
        print("")

    if DRY:
        print("[dry] rode sem --dry pra aplicar.")
        return

    print("-" * 62)
    print("CONFERINDO")
    print("-" * 62)
    ok = True
    for d in ["skills", "commands", "agents"]:
        p = os.path.join(BASE, d)
        n = sum(len(f) for _, _, f in os.walk(p)) if os.path.isdir(p) else 0
        print("  %-8s %s %d arquivos" % (d, "OK  " if n else "FALHA", n))
        ok = ok and bool(n)
    for f in ["CLAUDE.md", "AGENTS_CATALOG.md"]:
        e = os.path.exists(os.path.join(BASE, f))
        print("  %-8s %s %s" % ("config", "OK  " if e else "FALHA", f))
        ok = ok and e
    proj = os.path.join(BASE, "projects")
    tot = 0
    if os.path.isdir(proj):
        for d in os.listdir(proj):
            m = os.path.join(proj, d, "memory")
            if os.path.isdir(m):
                tot += len([f for f in os.listdir(m) if f.endswith(".md")])
    print("  %-8s %s %d memorias" % ("memory", "OK  " if tot else "FALHA", tot))

    print("")
    print("Tudo pronto. Reinicie o Claude Code." if ok else "Algo falhou acima.")
    print("")
    print("Dependencias (so quando for usar cada skill):")
    print("   pip3 install DrissionPage                        # /raspar-adlibrary")
    print("   pip3 install google-genai pillow python-dotenv   # imagens")
    print("")
    print("As chaves de API NAO vem no repo. Crie o .env local quando alguma skill pedir.")


if __name__ == "__main__":
    main()
