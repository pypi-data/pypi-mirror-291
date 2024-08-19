# shit ass code

import typing

class Colors:
    colors: typing.Dict[str, typing.Tuple[tuple, tuple]] = {
        'purple_to_white': ((127, 0, 255), (255, 255, 255)),
        'red_to_blue': ((255, 0, 0), (0, 0, 255)),
        'green_to_yellow': ((0, 255, 0), (255, 255, 0)),
        'black_to_white': ((0, 0, 0), (255, 255, 255)),
        'blue_to_cyan': ((0, 0, 255), (0, 255, 255)),
        'orange_to_pink': ((255, 165, 0), (255, 192, 203)),
        'mint': ((194, 255, 182), (255, 255, 255)),
        'red_to_yellow': ((255, 0, 0), (255, 255, 0)),
        'blue_to_green': ((0, 0, 255), (0, 255, 0)),
        'purple_to_blue': ((128, 0, 128), (0, 0, 255)),
        'pink_to_white': ((255, 192, 203), (255, 255, 255)),
        'cyan_to_magenta': ((0, 255, 255), (255, 0, 255)),
        'gray_to_black': ((169, 169, 169), (0, 0, 0)),
        'blue_to_white': ((0, 0, 255), (255, 255, 255)),
        'red_to_green': ((255, 0, 0), (0, 255, 0)),
        'green_to_blue': ((0, 255, 0), (0, 0, 255)),
        'blue_to_yellow': ((0, 0, 255), (255, 255, 0)),
        'yellow_to_cyan': ((255, 255, 0), (0, 255, 255)),
        'magenta_to_red': ((255, 0, 255), (255, 0, 0)),
        'white_to_black': ((255, 255, 255), (0, 0, 0)),
        'rainbow': None,
    }

    def __init__(self, start: str, end: str) -> None:
        if start not in Colors.colors or end not in Colors.colors:
            raise ValueError(f'Color gradient not found')
        self.start = start
        self.end = end

    def _inter(self, t: float, s: tuple[int, int, int], e: tuple[int, int, int]) -> tuple[int, int, int]:
        return tuple(int(s[i] + t * (e[i] - s[i])) for i in range(3))

    def _applyg(self, text: str) -> typing.List[tuple[int, int, int]]:
        gradient = []
        if self.start == 'rainbow':
            rbc = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (127, 0, 255)]
            num_colors = len(rbc)
            for i in range(len(text)):
                t = i / (len(text) - 1) * (num_colors - 1)
                ss = int(t)
                ee = min(ss + 1, num_colors - 1)
                blend = t - ss
                color = self._inter(blend, rbc[ss], rbc[ee])
                gradient.append(color)
        else:
            for i in range(len(text)):
                t = i / (len(text) - 1)
                color = self._inter(t, Colors.colors[self.start][0], Colors.colors[self.end][1])
                gradient.append(color)
        return gradient

    def __call__(self, text: str) -> str:
        gc = self._applyg(text)
        return ''.join(
            f'\033[38;2;{color[0]};{color[1]};{color[2]}m{char}\033[0m'
            for char, color in zip(text, gc)
        )

    @classmethod
    def gg(cls, name: str) -> typing.Callable[[str], str]:
        if name not in cls.colors:
            raise AttributeError(f'gradient not found {name}')
        return cls(name, name)

for grad in Colors.colors:
    if Colors.colors[grad] is not None:
        setattr(Colors, grad, Colors.gg(grad))
