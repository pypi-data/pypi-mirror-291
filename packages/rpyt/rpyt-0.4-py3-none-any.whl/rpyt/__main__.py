from fire import Fire

from rpyt.crowdin import (
    create_inputs,
    read_common,
    read_dialogue,
)


class PyToolsCrowdin:
    read_common = staticmethod(read_common)
    read_dialogue = staticmethod(read_dialogue)
    create_inputs = staticmethod(create_inputs)


class PyTools:
    crowdin = PyToolsCrowdin


def main():
    Fire(PyTools)


if __name__ == "__main__":
    main()
