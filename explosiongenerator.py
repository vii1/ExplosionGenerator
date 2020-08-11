import wx
from random import Random
from array import array
import math


def _lerp(x, y, alpha):
    return x + (y - x) * alpha


def _lerp_color(x: wx.Colour, y: wx.Colour, alpha):
    return wx.Colour(
        _lerp(x.red, y.red, alpha),
        _lerp(x.green, y.green, alpha),
        _lerp(x.blue, y.blue, alpha),
        _lerp(x.alpha, y.alpha, alpha)
    )


class ExplosionGenerator:
    class Punto:
        def __init__(self, size: wx.Size, rng: Random):
            cx = size.x / 2
            cy = size.y / 2
            ang = rng.random() * math.pi * 2
            dist = rng.random() * 0.8
            self.ix = math.cos(ang)
            self.iy = math.sin(ang)
            self.x = cx + math.cos(ang) * dist * cx
            self.y = cy + math.sin(ang) * dist * cy
            rx = self.x if self.x < cx else size.x - self.x
            ry = self.y if self.y < cy else size.y - self.y
            self.radio = min(rx, ry)
            self.fuerza = self.radio + (rng.random() * self.radio) * 4

    class Explosion:
        def __init__(self, n_pun, size: wx.Size, rng: Random):
            self.p = [ExplosionGenerator.Punto(size, rng) for _ in range(n_pun)]

    def __init__(self, size: wx.Size, gradient, type, frames, points, seed=None):
        self.size = wx.Size(size)
        self.gradient = gradient
        self.type = type
        self.frames = int(frames)
        self.points = int(points)
        self.seed = seed

        self.bgcolor = gradient[-1][0]

    def _color(self, alpha):
        stops = len(self.gradient)
        for i in range(stops - 1):
            col1, a1 = self.gradient[i]
            col2, a2 = self.gradient[i + 1]
            if a1 <= alpha < a2:
                b = (alpha - a1) / (a2 - a1)
                return _lerp_color(col1, col2, b)
        return self.bgcolor

    def CreateFrames(self, dialog : wx.GenericProgressDialog):
        rng = Random(self.seed)
        buf = array('d', [0] * (self.size.x * self.size.y))
        n_pun = 32
        n_exp = {'A': 4, 'B': 3, 'C': 5, 'D': 1}.get(self.type)
        exp = [ExplosionGenerator.Explosion(n_pun, self.size, rng) for _ in range(n_exp)]
        paso_frame = min(self.size.x, self.size.y) / (self.frames * 2)
        bmps = []
        for n in range(self.frames):
            dialog.Update(n, f"Generando imagen {n + 1} de {self.frames}")
            if dialog.WasCancelled():
                return None
            bmp = self._CreateFrame(n, rng, buf, exp, paso_frame, dialog)
            bmps.append(bmp)
        return bmps

    def _CreateFrame(self, n, rng, buf, exp, paso_frame, dialog: wx.GenericProgressDialog):
        self._PaintExplosion(rng, buf, exp)
        self._AdvancePoints(exp, paso_frame)
        pixels = array('B', [comp for a in buf for comp in self._color(1-a)])
        return wx.Bitmap.FromBufferRGBA(self.size.x, self.size.y, pixels)

    def _PaintExplosion(self, rng: Random, buf: array, exp: Explosion):
        for y in range(self.size.y):
            for x in range(self.size.x):
                coloracum = 0.0
                for m, e in enumerate(exp):
                    color = 0.0
                    for p in e.p:
                        dx = math.fabs(x - p.x)
                        dy = math.fabs(y - p.y)
                        if dx < p.radio and dy < p.radio:
                            dist = math.sqrt(dx * dx + dy * dy)
                            if dist < p.radio:
                                color += (p.radio - dist) * p.fuerza / p.radio / 255
                    color = min(color, 1.0)
                    if self.type in ('A', 'D'):
                        coloracum += color
                    else:
                        coloracum += -color if m % 2 != 0 else color
                if self.type in ('A', 'D'):
                    buf[y * self.size.x + x] = coloracum / len(exp)
                else:
                    coloracum = max(min(coloracum, 1.0), 0.0)
                    buf[y * self.size.x + x] = coloracum
        # Aplicamos el granulado
        for n in range(self.size.x * self.size.y * self.points // 100):
            DEEP = 4 / 255
            x = rng.randrange(1, self.size.x - 1)
            y = rng.randrange(1, self.size.y - 1)
            if buf[y * self.size.x + x] > DEEP * 2:
                buf[y * self.size.x + x] -= DEEP * 2
            if buf[y * self.size.x + x - 1] > DEEP:
                buf[y * self.size.x + x - 1] -= DEEP
            if buf[y * self.size.x + x + 1] > DEEP:
                buf[y * self.size.x + x + 1] -= DEEP
            if buf[(y - 1) * self.size.x + x] > DEEP:
                buf[(y - 1) * self.size.x + x] -= DEEP
            if buf[(y + 1) * self.size.x + x] > DEEP:
                buf[(y + 1) * self.size.x + x] -= DEEP

    def _AdvancePoints(self, exp, paso_frame):
        for e in exp:
            for p in e.p:
                p.x += p.ix * paso_frame
                p.y += p.iy * paso_frame
                if p.fuerza > p.radio:
                    p.fuerza *= 0.86
                p.radio -= paso_frame