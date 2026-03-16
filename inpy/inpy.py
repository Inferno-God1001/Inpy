import sys
import termios
import tty
import string

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


def _gerar_codigo(style):
    partes = style.lower().split()
    codigos = []

    for p in partes:
        if p in CORES:
            codigos.append(CORES[p])
        elif p in ESTILOS:
            codigos.append(ESTILOS[p])

    if not codigos:
        return ""

    return "\033[" + ";".join(codigos) + "m"


def _permitido(tecla, modo):

    if modo == "all":
        return True

    if modo == "numbers":
        return tecla.isdigit()

    if modo == "letters":
        return tecla.isalpha()

    if modo == "alphanumeric":
        return tecla.isalnum()

    if modo == "chars":
        return tecla in string.punctuation

    return True


def input(
    prompt="",
    message_color="white",
    color="white",
    hide=False,
    hide_full=False,
    hide_char="*",
    auto_enter_word=None,
    accept="all"
):

    texto = ""

    codigo_prompt = _gerar_codigo(message_color)
    codigo_texto = _gerar_codigo(color)

    print(codigo_prompt + prompt + RESET, end="", flush=True)

    while True:
        tecla = _ler_tecla()

        if tecla == "\x03":  # Ctrl+C
            print("^C")
            raise KeyboardInterrupt

        if tecla == "\r":  # Enter
            break

        if tecla == "\x7f":  # Backspace
            if texto:
                texto = texto[:-1]
                if not hide_full:
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            continue

        if not _permitido(tecla, accept):
            continue

        texto += tecla

        if auto_enter_word and texto.endswith(auto_enter_word):
            break

        if hide_full:
            pass
        elif hide:
            sys.stdout.write(hide_char)
        else:
            sys.stdout.write(codigo_texto + tecla + RESET)

        sys.stdout.flush()

    print()
    return texto