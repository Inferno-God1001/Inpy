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
    accept="all",
    allowed_chars=None,
    max_chars=None,
    reset_if_exceed=False,
    lock_after_limit=False
):

    texto = ""

    codigo_prompt = _gerar_codigo(message_color)
    codigo_texto = _gerar_codigo(color)

    print(codigo_prompt + prompt + RESET, end="", flush=True)

    while True:
        tecla = _ler_tecla()

        if tecla == "\x03":
            print("^C")
            raise KeyboardInterrupt

        if tecla == "\r":
            break

        if tecla == "\x7f":
            if texto:
                texto = texto[:-1]
                if not hide_full:
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            continue

        if not _permitido(tecla, accept):
            continue

        if allowed_chars and tecla not in allowed_chars:
            continue

        if max_chars and len(texto) >= max_chars:

            if reset_if_exceed:
                while len(texto) > 0:
                    sys.stdout.write("\b \b")
                    texto = texto[:-1]
                sys.stdout.flush()
                continue

            if lock_after_limit:
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



def help_input(language="pt"):

    if language.lower() == "pt":

        print("""
================================
 AJUDA DO INPUT AVANÇADO
================================

Função principal:

input(
    prompt="",
    message_color="white",
    color="white",
    hide=False,
    hide_full=False,
    hide_char="*",
    auto_enter_word=None,
    accept="all",
    allowed_chars=None,
    max_chars=None,
    reset_if_exceed=False,
    lock_after_limit=False
)

--------------------------------
PROMPT
Texto mostrado antes do usuário digitar.

Exemplo:
input(prompt="Nome: ")

--------------------------------
CORES

message_color = cor do prompt
color = cor do texto digitado

Cores disponíveis:

black
red
green
yellow
blue
magenta
cyan
white

Exemplo:

input(
    prompt="Nome: ",
    message_color="cyan",
    color="yellow"
)

--------------------------------
OCULTAR TEXTO

hide=True
Mostra * no lugar dos caracteres.

hide_full=True
Não mostra nada.

--------------------------------
TIPOS DE CARACTERES

accept pode ser:

all
numbers
letters
alphanumeric
chars

--------------------------------
CARACTERES ESPECÍFICOS

allowed_chars="ABC123"

--------------------------------
LIMITE DE CARACTERES

max_chars=5

--------------------------------
RESET AUTOMÁTICO

reset_if_exceed=True

Se passar do limite, o texto é apagado.

--------------------------------
BLOQUEAR APÓS LIMITE

lock_after_limit=True

Usuário precisa apagar manualmente.

--------------------------------
ENTER AUTOMÁTICO

auto_enter_word="exit"

Quando essa palavra aparece, o Enter acontece automaticamente.

================================
""")

    else:

        print("""
================================
 ADVANCED INPUT HELP
================================

Main function:

input(
    prompt="",
    message_color="white",
    color="white",
    hide=False,
    hide_full=False,
    hide_char="*",
    auto_enter_word=None,
    accept="all",
    allowed_chars=None,
    max_chars=None,
    reset_if_exceed=False,
    lock_after_limit=False
)

--------------------------------
PROMPT
Text shown before the user types.

Example:
input(prompt="Name: ")

--------------------------------
COLORS

message_color = prompt color
color = typed text color

Available colors:

black
red
green
yellow
blue
magenta
cyan
white

Example:

input(
    prompt="Name: ",
    message_color="cyan",
    color="yellow"
)

--------------------------------
HIDE TEXT

hide=True
Shows * instead of characters.

hide_full=True
Shows nothing.

--------------------------------
CHARACTER TYPES

accept can be:

all
numbers
letters
alphanumeric
chars

--------------------------------
SPECIFIC CHARACTERS

allowed_chars="ABC123"

--------------------------------
CHARACTER LIMIT

max_chars=5

--------------------------------
AUTO RESET

reset_if_exceed=True

If the limit is exceeded, the text is cleared.

--------------------------------
LOCK AFTER LIMIT

lock_after_limit=True

User must delete characters manually.

--------------------------------
AUTO ENTER

auto_enter_word="exit"

When this word appears, Enter happens automatically.

================================
""")