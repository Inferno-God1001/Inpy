import sys
import termios
import tty

CORES = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37"
}

ESTILOS = {
    "bold": "1",
    "underline": "4",
    "reverse": "7"
}

RESET = "\033[0m"


def _ler_tecla():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        tecla = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    return tecla


def _gerar_codigo(estilo):
    partes = estilo.lower().split()
    codigos = []

    for p in partes:
        if p in CORES:
            codigos.append(CORES[p])
        elif p in ESTILOS:
            codigos.append(ESTILOS[p])

    return "\033[" + ";".join(codigos) + "m"


def input_color(prompt="", style="white"):
    texto = ""
    codigo = _gerar_codigo(style)

    print(prompt, end="", flush=True)

    while True:
        tecla = _ler_tecla()

        if tecla == "\x03":  # Ctrl + C
            print("^C")
            raise KeyboardInterrupt

        if tecla == "\r":  # Enter
            break

        if tecla == "\x7f":  # Backspace
            if texto:
                texto = texto[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue

        texto += tecla
        sys.stdout.write(codigo + tecla + RESET)
        sys.stdout.flush()

    print()
    return texto
