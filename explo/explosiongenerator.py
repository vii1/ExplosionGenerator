from array import array
import wx
import numpy as np
from numpy.random import default_rng

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
    class PointData:
        def __init__(self, size, n_exp, n_pun, rng):
            cx = size.x / 2
            cy = size.y / 2
            self.shape = (n_exp, n_pun)
            ang = rng.random(self.shape) * (np.pi * 2)
            dist = rng.random(self.shape)  # * 0.8
            self.ix = np.cos(ang)
            self.iy = np.sin(ang)
            self.x = self.ix * dist * cx + cx
            self.y = self.iy * dist * cx + cx
            rx = np.where(self.x < cx, self.x, size.x - self.x)
            ry = np.where(self.y < cy, self.y, size.y - self.y)
            self.radio = np.minimum(rx, ry)
            self.fuerza = self.radio + rng.random(self.shape) * self.radio * 4

    def __init__(self, size: wx.Size, gradient, type, frames, points, seed=None):
        self.size = wx.Size(size)
        self.shape = (size.y, size.x)
        self.gradient = gradient
        self.type = type
        self.frames = int(frames)
        self.points = int(points)
        self.seed = seed

        self.satColor = gradient[-1][0]

    def _color(self, alpha):
        alpha = min(max(0, 1 - alpha), 1)
        stops = len(self.gradient)
        for i in range(stops - 1):
            col1, a1 = self.gradient[i]
            col2, a2 = self.gradient[i + 1]
            if a1 <= alpha < a2:
                b = (alpha - a1) / (a2 - a1)
                return tuple(_lerp_color(col1, col2, b))
        return tuple(self.satColor)

    def CreateFrames(self, dialog: wx.GenericProgressDialog):
        rng = default_rng(self.seed)
        buf = np.zeros(self.shape)
        n_pun = 32
        n_exp = {'A': 4, 'B': 3, 'C': 5, 'D': 1}.get(self.type)

        p = ExplosionGenerator.PointData(self.size, n_exp, n_pun, rng)

        paso_frame = min(self.size.x, self.size.y) / (self.frames * 2)
        bmps = []
        for n in range(self.frames):
            dialog.Update(n, _("Generating frame %d of %d") % (n + 1, self.frames))
            if dialog.WasCancelled():
                return None
            bmp = self._CreateFrame(n, rng, buf, p, paso_frame, dialog)
            bmps.append(bmp)
        return bmps

    def _CreateFrame(self, n, rng, buf, p, paso_frame, dialog: wx.GenericProgressDialog):
        self._PaintExplosion(rng, buf, p)
        self._AdvancePoints(p, paso_frame)
        color = np.frompyfunc(self._color, 1, 4)
        pixels = array('B', np.array(color(buf)).flatten('F'))
        return wx.Bitmap.FromBufferRGBA(self.size.x, self.size.y, pixels)

    def _PaintExplosion(self, rng: np.random.Generator, buf: np.ndarray, p):
        for y in range(self.size.y):
            for x in range(self.size.x):
                dist = np.sqrt(np.square(x - p.x) + np.square(y - p.y))
                color = np.sum(np.where(dist < p.radio, (p.radio - dist) * p.fuerza / p.radio / 255, 0), 1)
                color = np.minimum(color, 1.0)
                if self.type in ('A', 'D'):
                    coloracum = np.sum(color)
                else:
                    # resta las filas impares, suma las pares
                    coloracum = np.sum([color[r] for r in range(0, p.shape[0], 2)]) \
                                - np.sum([color[r] for r in range(1, p.shape[0], 2)])
                if self.type in ('A', 'D'):
                    buf[y, x] = coloracum / p.shape[0]
                else:
                    coloracum = max(min(coloracum, 1.0), 0.0)
                    buf[y, x] = coloracum
        # Aplicamos el granulado
        granos = self.size.x * self.size.y * self.points // 100
        X = rng.integers(1, self.size.x - 1, granos)
        Y = rng.integers(1, self.size.y - 1, granos)
        DEEP = 4 / 255
        for x, y in np.transpose(np.stack((X, Y))):
            if buf[y, x] > DEEP * 2:
                buf[y, x] -= DEEP * 2
            if buf[y, x - 1] > DEEP:
                buf[y, x - 1] -= DEEP
            if buf[y, x + 1] > DEEP:
                buf[y, x + 1] -= DEEP
            if buf[y - 1, x] > DEEP:
                buf[y - 1, x] -= DEEP
            if buf[y + 1, x] > DEEP:
                buf[y + 1, x] -= DEEP

    def _AdvancePoints(self, p, paso_frame):
        p.x += p.ix * paso_frame
        p.y += p.iy * paso_frame
        p.fuerza *= np.where(p.fuerza > p.radio, 0.86, 1)
        p.radio -= paso_frame
