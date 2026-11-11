# -*- coding: utf-8 -*-
"""Génère 8 affiches 'Le thème de l'air' (8 images dont 2 intrus) pour enfants de 4 ans."""
import math, os
from PIL import Image, ImageDraw, ImageFont

W, H = 2480, 3508  # A4 @ 300dpi
OUT = "/workspace/affiches-air"
FONT_DIR = os.path.join(OUT, "fonts")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

OUTLINE = (45, 55, 90)

def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

def rot(p, c, deg):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))

class Pen:
    """Dessine dans un repère 0-100 mappé sur un carré cible."""
    def __init__(self, d, cx, cy, size):
        self.d, self.cx, self.cy, self.s = d, cx, cy, size / 100.0

    def p(self, x, y):
        return (self.cx + (x - 50) * self.s, self.cy + (y - 50) * self.s)

    def poly(self, pts, fill=None, w=None, closed=True, outline=None):
        pp = [self.p(x, y) for x, y in pts]
        if fill:
            self.d.polygon(pp, fill=fill)
        if w:
            self.d.line(pp + ([pp[0]] if closed else []), fill=outline or OUTLINE, width=max(1, int(w * self.s)), joint="curve")

    def ell(self, x0, y0, x1, y1, fill=None, w=None, outline=None):
        b = [self.p(x0, y0), self.p(x1, y1)]
        self.d.ellipse(b, fill=fill, outline=(outline or OUTLINE) if w else None, width=max(1, int((w or 0) * self.s)))

    def rrect(self, x0, y0, x1, y1, r, fill=None, w=None, outline=None):
        b = [self.p(x0, y0), self.p(x1, y1)]
        self.d.rounded_rectangle(b, radius=r * self.s, fill=fill, outline=(outline or OUTLINE) if w else None, width=max(1, int((w or 0) * self.s)))

    def line(self, pts, color=OUTLINE, w=3):
        pp = [self.p(x, y) for x, y in pts]
        self.d.line(pp, fill=color, width=max(1, int(w * self.s)), joint="curve")

    def arc(self, x0, y0, x1, y1, a0, a1, color=OUTLINE, w=3):
        b = [self.p(x0, y0), self.p(x1, y1)]
        self.d.arc(b, a0, a1, fill=color, width=max(1, int(w * self.s)))

    def dot(self, x, y, r, color=OUTLINE, fill=None):
        self.ell(x - r, y - r, x + r, y + r, fill=fill or color)

# ---------------------------------------------------------------- icônes AIR
def i_ballon(p, c1=(255, 90, 120)):
    p.ell(24, 6, 76, 72, fill=c1, w=3)
    p.ell(32, 14, 46, 32, fill=(255, 255, 255))
    p.poly([(45, 70), (55, 70), (50, 80)], fill=c1, w=2.5)
    p.line([(50, 80), (44, 87), (56, 93), (50, 99)], w=3)

def i_cerfvolant(p, c1=(70, 170, 255), c2=(255, 200, 60)):
    p.poly([(50, 4), (80, 40), (50, 86), (20, 40)], fill=c1, w=3)
    p.poly([(50, 4), (50, 86)], fill=None, w=2.5)
    p.line([(20, 40), (80, 40)], w=2.5)
    p.poly([(50, 4), (50, 40), (20, 40)], fill=c2)
    p.line([(50, 86), (42, 92), (56, 96), (48, 100)], w=2.5)
    for bx, by in ((44, 93), (54, 97)):
        p.poly([(bx - 5, by - 3), (bx, by), (bx - 5, by + 3)], fill=(255, 90, 120), w=1.5)
        p.poly([(bx + 5, by - 3), (bx, by), (bx + 5, by + 3)], fill=(255, 90, 120), w=1.5)

def i_moulin(p):
    p.line([(50, 52), (50, 97)], color=(150, 100, 60), w=5)
    cols = [(255, 90, 120), (255, 200, 60), (70, 190, 130), (70, 140, 255)]
    blades = [((50, 50), (50, 8), (82, 29)), ((50, 50), (92, 50), (71, 82)),
              ((50, 50), (50, 92), (18, 71)), ((50, 50), (8, 50), (29, 18))]
    for (bl, c) in zip(blades, cols):
        p.poly(list(bl), fill=c, w=2.5)
    p.dot(50, 50, 6)

def i_voilier(p, c1=(255, 120, 80)):
    p.poly([(20, 68), (80, 68), (68, 84), (32, 84)], fill=c1, w=3)
    p.line([(50, 66), (50, 12)], w=4)
    p.poly([(55, 16), (55, 62), (82, 62)], fill=(255, 255, 255), w=2.5)
    p.poly([(45, 22), (45, 62), (22, 62)], fill=(120, 220, 255), w=2.5)
    p.poly([(50, 12), (62, 16), (50, 20)], fill=(255, 200, 60), w=2)
    p.arc(8, 78, 34, 96, 200, 340, color=(90, 170, 230), w=4)
    p.arc(40, 80, 66, 98, 200, 340, color=(90, 170, 230), w=4)
    p.arc(72, 78, 98, 96, 200, 340, color=(90, 170, 230), w=4)

def i_bulles(p, c=(120, 200, 250)):
    p.line([(16, 82), (30, 62)], color=(255, 120, 150), w=5)
    p.ell(24, 44, 44, 64, w=4, outline=(255, 120, 150))
    for (x, y, r) in ((64, 26, 15), (82, 52, 10), (58, 58, 7), (38, 22, 9)):
        p.ell(x - r, y - r, x + r, y + r, fill=(235, 248, 255), w=2.5, outline=c)
        p.arc(x - r + 2, y - r + 2, x + r - 2, y + r - 2, 200, 300, color=(255, 255, 255), w=2.5)

def i_eolienne(p):
    p.poly([(46, 42), (54, 42), (58, 96), (42, 96)], fill=(160, 170, 190), w=3)
    hub = (50, 40)
    for a in (90, 210, 330):
        pts = [rot(pt, hub, a - 90) for pt in [(50, 40), (46, 8), (58, 10)]]
        p.poly(pts, fill=(210, 235, 252), w=2.5)
    p.dot(50, 40, 5.5)

def i_parachute(p, c1=(255, 90, 120), c2=(255, 210, 70)):
    p.ell(14, 4, 86, 74, fill=c1, w=3)
    p.poly([(50, 4), (50, 44)], fill=None, w=0)
    p.poly([(32, 6), (32, 44)], fill=c2)
    p.poly([(68, 6), (68, 44)], fill=c2)
    p.poly([(14, 39), (86, 39)], fill=(255, 255, 255))
    for x in (18, 38, 62, 82):
        p.line([(x, 41), (43 if x < 50 else 57, 72)], w=2.5)
    p.rrect(41, 70, 59, 86, 4, fill=(180, 120, 70), w=2.5)

def i_avion(p, c1=(255, 255, 255), c2=(255, 120, 80)):
    p.ell(10, 30, 30, 46, fill=(230, 242, 252), w=2.5)
    p.ell(16, 40, 90, 68, fill=c1, w=3)
    p.poly([(44, 54), (66, 54), (58, 78), (38, 78)], fill=c2, w=2.5)
    p.poly([(30, 44), (42, 44), (36, 26), (26, 26)], fill=c2, w=2.5)
    for x in (56, 66, 76):
        p.ell(x - 4, 48, x + 4, 58, fill=(140, 210, 250), w=2)
    p.poly([(16, 40), (16, 68)], fill=None, w=0)

def i_montgolfiere(p, c1=(255, 90, 120), c2=(255, 200, 60)):
    p.ell(20, 4, 80, 62, fill=c1, w=3)
    p.poly([(40, 5), (36, 61)], fill=c2)
    p.poly([(60, 5), (64, 61)], fill=c2)
    p.ell(44, 8, 56, 58, fill=c2)
    p.line([(32, 55), (42, 76)], w=2.5)
    p.line([(68, 55), (58, 76)], w=2.5)
    p.line([(50, 60), (50, 76)], w=2.5)
    p.rrect(40, 74, 60, 90, 5, fill=(180, 120, 70), w=2.5)

def i_ventilateur(p, c1=(90, 170, 255)):
    p.ell(24, 6, 76, 58, fill=(240, 246, 252), w=3)
    hub = (50, 32)
    for a in (0, 120, 240):
        pts = [rot(pt, hub, a) for pt in [(50, 32), (50, 10), (62, 16), (56, 30)]]
        p.poly(pts, fill=c1, w=2)
    p.dot(50, 32, 5)
    p.line([(50, 58), (50, 84)], w=6)
    p.ell(34, 82, 66, 96, fill=(120, 130, 160), w=2.5)

def i_drapeau(p, c1=(70, 190, 130)):
    p.line([(28, 6), (28, 96)], color=(130, 100, 70), w=5)
    p.dot(28, 6, 3.5, color=(255, 200, 60))
    p.poly([(31, 12), (58, 8), (80, 16), (72, 28), (80, 42), (54, 48), (31, 42)], fill=c1, w=2.5)

def i_feuilles_vent(p):
    for pts in ([(8, 30), (40, 22), (66, 30), (80, 24)],
                [(14, 56), (44, 48), (70, 56), (88, 50)],
                [(10, 82), (38, 74), (62, 82), (78, 76)]):
        p.line(pts, color=(90, 170, 230), w=4)
        x, y = pts[-1]
        p.arc(x - 6, y - 7, x + 8, y + 7, 290, 80, color=(90, 170, 230), w=4)
    for (x, y, a, c) in ((40, 38, -30, (110, 200, 90)), (66, 66, 20, (255, 170, 60)), (30, 68, -15, (255, 120, 150))):
        leaf = [(x, y - 10), (x + 8, y - 4), (x, y + 10), (x - 8, y + 4)]
        p.poly([rot(pt, (x, y), a) for pt in leaf], fill=c, w=2.5)

def i_plume(p, c1=(200, 230, 250)):
    p.poly([(36, 92), (40, 60), (52, 28), (66, 12), (64, 34), (56, 62), (44, 90)], fill=c1, w=2.5)
    p.line([(38, 90), (66, 12)], w=2.5)
    for i, (x0, y0, x1, y1) in enumerate(((46, 62, 58, 58), (50, 46, 62, 42), (55, 32, 66, 28))):
        p.line([(x0, y0), (x1, y1)], w=2)
    p.line([(36, 92), (30, 99)], w=2.5)

def i_seche_cheveux(p, c1=(255, 150, 60)):
    p.ell(14, 30, 58, 62, fill=c1, w=3)
    p.rrect(54, 38, 76, 54, 6, fill=(150, 160, 180), w=2.5)
    p.rrect(26, 58, 40, 92, 6, fill=c1, w=2.5)
    p.dot(36, 66, 3, color=(255, 255, 255))
    for i, y in enumerate((36, 46, 56)):
        p.line([(82, y), (94, y)], color=(90, 170, 230), w=3.5)
    p.dot(30, 40, 5, color=(255, 255, 255))

def i_pompe(p, c1=(70, 140, 255)):
    p.rrect(30, 34, 56, 84, 5, fill=c1, w=2.5)
    p.line([(43, 34), (43, 20)], w=5)
    p.rrect(28, 12, 58, 22, 4, fill=(255, 90, 120), w=2.5)
    p.line([(56, 50), (72, 62), (80, 74)], w=3.5)
    p.rrect(76, 72, 88, 82, 3, fill=(120, 130, 160), w=2)
    p.ell(84, 30, 98, 44, fill=(150, 220, 250), w=2)
    p.ell(92, 14, 100, 24, fill=(150, 220, 250), w=2)

def i_linge(p):
    p.line([(6, 26), (94, 26)], color=(130, 100, 70), w=3.5)
    p.poly([(24, 30), (40, 30), (46, 38), (38, 42), (38, 68), (26, 68), (26, 42), (18, 38)], fill=(255, 120, 150), w=2.5)
    p.rrect(56, 30, 78, 66, 3, fill=(110, 200, 250), w=2.5)
    p.line([(56, 42), (78, 42)], color=(255, 255, 255), w=3)
    p.line([(56, 54), (78, 54)], color=(255, 255, 255), w=3)
    p.dot(26, 28, 2.5, color=(90, 90, 110)); p.dot(38, 28, 2.5, color=(90, 90, 110))
    p.dot(62, 28, 2.5, color=(90, 90, 110)); p.dot(72, 28, 2.5, color=(90, 90, 110))

def i_sifflet(p, c1=(255, 200, 60)):
    p.rrect(26, 40, 78, 66, 12, fill=c1, w=3)
    p.rrect(12, 44, 34, 56, 4, fill=(255, 150, 60), w=2.5)
    p.dot(62, 53, 6, fill=(255, 255, 255))
    p.line([(26, 40), (26, 66)], w=0)
    for i, r in enumerate((8, 14, 20)):
        p.arc(80 - r // 2, 53 - r, 80 + r, 53 + r, -55, 55, color=(90, 170, 230), w=3.5)

def i_nuage_vent(p):
    p.ell(16, 26, 48, 52, fill=(255, 255, 255), w=3)
    p.ell(34, 14, 66, 42, fill=(255, 255, 255), w=3)
    p.ell(52, 26, 84, 52, fill=(255, 255, 255), w=3)
    p.rrect(20, 38, 80, 52, 8, fill=(255, 255, 255), w=3)
    for y, x2 in ((68, 74), (84, 62)):
        p.line([(20, y), (x2, y)], color=(90, 170, 230), w=4)
        p.arc(x2 - 8, y - 8, x2 + 8, y + 8, 270, 90, color=(90, 170, 230), w=4)

AIR = {
    "ballon": (i_ballon, "le ballon"),
    "cerf-volant": (i_cerfvolant, "le cerf-volant"),
    "moulin": (i_moulin, "le moulin à vent"),
    "voilier": (i_voilier, "le bateau à voile"),
    "bulles": (i_bulles, "les bulles de savon"),
    "eolienne": (i_eolienne, "l'éolienne"),
    "parachute": (i_parachute, "le parachute"),
    "avion": (i_avion, "l'avion"),
    "montgolfiere": (i_montgolfiere, "la montgolfière"),
    "ventilateur": (i_ventilateur, "le ventilateur"),
    "drapeau": (i_drapeau, "le drapeau"),
    "feuilles": (i_feuilles_vent, "les feuilles et le vent"),
    "plume": (i_plume, "la plume"),
    "seche-cheveux": (i_seche_cheveux, "le sèche-cheveux"),
    "pompe": (i_pompe, "la pompe à vélo"),
    "linge": (i_linge, "le fil à linge"),
    "sifflet": (i_sifflet, "le sifflet"),
    "nuage": (i_nuage_vent, "le nuage et le vent"),
}

# ------------------------------------------------------------- icônes INTRUS
def i_caillou(p):
    p.poly([(22, 72), (32, 42), (52, 28), (72, 40), (80, 72)], fill=(160, 165, 175), w=3)
    p.poly([(32, 42), (52, 28), (50, 52)], fill=(190, 195, 205))
    p.poly([(22, 72), (50, 52), (80, 72)], fill=(135, 140, 150))
    p.poly([(22, 72), (32, 42), (50, 52), (80, 72)], fill=None, w=2.5)

def i_banane(p):
    outer = [(math.cos(math.radians(a)) * 34 + 50, math.sin(math.radians(a)) * 34 + 34) for a in range(200, 341, 10)]
    inner = [(math.cos(math.radians(a)) * 22 + 50, math.sin(math.radians(a)) * 22 + 38) for a in range(340, 199, -10)]
    p.poly(outer + inner, fill=(255, 210, 60), w=3)
    p.line([(20, 45), (26, 40)], color=(120, 90, 40), w=5)

def i_nounours(p):
    c = (170, 115, 70)
    p.ell(24, 8, 44, 28, fill=c, w=2.5)
    p.ell(56, 8, 76, 28, fill=c, w=2.5)
    p.ell(30, 46, 70, 90, fill=c, w=3)
    p.ell(30, 14, 70, 54, fill=c, w=3)
    p.ell(39, 34, 61, 52, fill=(225, 195, 160), w=2)
    p.dot(40, 28, 2.5); p.dot(60, 28, 2.5)
    p.dot(50, 40, 3.5)
    p.line([(50, 44), (50, 47)], w=2)
    p.ell(22, 52, 36, 68, fill=c, w=2.5)
    p.ell(64, 52, 78, 68, fill=c, w=2.5)

def i_gateau(p):
    p.ell(18, 80, 82, 92, fill=(230, 240, 250), w=2.5)
    p.rrect(28, 56, 72, 82, 5, fill=(255, 150, 180), w=2.5)
    p.rrect(34, 42, 66, 58, 5, fill=(255, 230, 180), w=2.5)
    p.rrect(47, 24, 53, 44, 2, fill=(120, 200, 250), w=2)
    p.line([(50, 24), (50, 21)], w=0)
    p.ell(46, 12, 54, 22, fill=(255, 170, 60), w=2)
    for x in (36, 50, 64):
        p.dot(x, 68, 3, color=(255, 255, 255))

def i_tortue(p):
    p.ell(70, 44, 90, 62, fill=(120, 200, 110), w=2.5)
    p.ell(22, 28, 74, 74, fill=(90, 170, 80), w=3)
    p.ell(30, 34, 66, 62, fill=(150, 210, 90), w=2.5)
    p.ell(26, 66, 42, 80, fill=(120, 200, 110), w=2.5)
    p.ell(56, 66, 72, 80, fill=(120, 200, 110), w=2.5)
    p.dot(82, 50, 2.5)

def i_escargot(p):
    p.ell(14, 52, 84, 76, fill=(255, 190, 120), w=3)
    p.ell(58, 40, 84, 68, fill=(255, 190, 120), w=3)
    p.ell(26, 22, 66, 62, fill=(255, 140, 100), w=3)
    p.arc(32, 28, 60, 56, 0, 360, color=(200, 90, 60), w=2.5)
    p.arc(38, 34, 54, 50, 0, 360, color=(200, 90, 60), w=2.5)
    p.dot(46, 42, 3, color=(200, 90, 60))
    p.line([(66, 44), (62, 30)], w=2.5); p.dot(62, 28, 2.5)
    p.line([(74, 44), (78, 30)], w=2.5); p.dot(78, 28, 2.5)

def i_pomme(p):
    p.ell(26, 32, 74, 82, fill=(240, 70, 80), w=3)
    p.line([(50, 32), (48, 16)], color=(120, 80, 40), w=4)
    p.poly([(52, 22), (70, 12), (72, 26), (56, 32)], fill=(110, 190, 90), w=2.5)
    p.ell(34, 42, 44, 56, fill=(255, 160, 160))

def i_chaise(p):
    c = (190, 130, 80)
    p.rrect(32, 10, 68, 56, 6, fill=c, w=3)
    p.rrect(26, 52, 74, 66, 4, fill=(210, 155, 105), w=3)
    p.line([(32, 66), (30, 94)], w=5)
    p.line([(68, 66), (70, 94)], w=5)
    p.line([(40, 66), (39, 90)], w=5)
    p.line([(60, 66), (61, 90)], w=5)

def i_lapin(p):
    c = (215, 215, 225)
    p.ell(34, 4, 47, 40, fill=c, w=2.5)
    p.ell(53, 4, 66, 40, fill=c, w=2.5)
    p.ell(37, 10, 44, 34, fill=(255, 180, 200))
    p.ell(56, 10, 63, 34, fill=(255, 180, 200))
    p.ell(30, 32, 70, 72, fill=c, w=3)
    p.dot(40, 48, 2.5); p.dot(60, 48, 2.5)
    p.poly([(46, 56), (54, 56), (50, 62)], fill=(255, 140, 170), w=2)
    p.line([(50, 62), (50, 66)], w=2)
    p.ell(36, 68, 64, 94, fill=c, w=3)

def i_poisson(p, c1=(255, 150, 60)):
    p.ell(14, 36, 72, 70, fill=c1, w=3)
    p.poly([(68, 53), (90, 36), (90, 70)], fill=(255, 120, 40), w=2.5)
    p.poly([(40, 38), (52, 24), (58, 40)], fill=(255, 120, 40), w=2.5)
    p.dot(30, 50, 3.5, fill=(255, 255, 255))
    p.dot(31, 50, 1.8)
    p.arc(40, 46, 60, 62, 300, 90, color=(255, 120, 40), w=2.5)

INTR = {
    "caillou": (i_caillou, "le caillou"),
    "banane": (i_banane, "la banane"),
    "nounours": (i_nounours, "le nounours"),
    "gateau": (i_gateau, "le gâteau"),
    "tortue": (i_tortue, "la tortue"),
    "escargot": (i_escargot, "l'escargot"),
    "pomme": (i_pomme, "la pomme"),
    "chaise": (i_chaise, "la chaise"),
    "lapin": (i_lapin, "le lapin"),
    "poisson": (i_poisson, "le poisson"),
}

# ------------------------------------------------------------------- affiches
POSTERS = [
    ("Le vent", ["moulin", "drapeau", "feuilles", "cerf-volant", "eolienne", "nuage"], ["banane", "tortue"], (255, 214, 120), (120, 200, 250)),
    ("Ça vole !", ["avion", "montgolfiere", "parachute", "ballon", "plume", "cerf-volant"], ["escargot", "chaise"], (170, 220, 255), (255, 150, 170)),
    ("On souffle !", ["bulles", "sifflet", "seche-cheveux", "pompe", "ventilateur", "ballon"], ["gateau", "caillou"], (255, 190, 140), (140, 210, 250)),
    ("Dehors, dehors !", ["voilier", "nuage", "cerf-volant", "moulin", "parachute", "feuilles"], ["nounours", "pomme"], (180, 235, 180), (255, 200, 90)),
    ("L'air et l'eau", ["voilier", "bulles", "parachute", "nuage", "moulin", "ballon"], ["lapin", "banane"], (150, 215, 250), (170, 225, 160)),
    ("L'énergie du vent", ["eolienne", "moulin", "drapeau", "ventilateur", "cerf-volant", "nuage"], ["tortue", "gateau"], (200, 200, 250), (120, 210, 200)),
    ("Tout s'envole !", ["plume", "feuilles", "ballon", "avion", "montgolfiere", "parachute"], ["poisson", "caillou"], (255, 220, 160), (160, 200, 250)),
    ("L'air partout", ["bulles", "seche-cheveux", "sifflet", "voilier", "drapeau", "pompe"], ["escargot", "nounours"], (250, 180, 200), (150, 220, 240)),
]

def rounded_bg(d, box, r, fill, outline, w):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w)

def draw_cloud(d, cx, cy, s, color=(255, 255, 255)):
    for (dx, dy, r) in ((-30, 6, 22), (0, -8, 28), (30, 6, 22), (0, 10, 26)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=color)

def make_poster(idx, titre, air_keys, intr_keys, col_top, col_accent):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # fond dégradé ciel
    for y in range(H):
        t = y / H
        c = tuple(int(col_top[i] * (1 - t) + 255 * t * 0.9 + 255 * 0.1 * (1 - t)) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # décor : soleil, nuages, oiseaux
    d.ellipse([W - 420, 90, W - 160, 350], fill=(255, 210, 80), outline=(255, 170, 50), width=10)
    for a in range(0, 360, 45):
        x0 = W - 290 + math.cos(math.radians(a)) * 190
        y0 = 220 + math.sin(math.radians(a)) * 190
        x1 = W - 290 + math.cos(math.radians(a)) * 250
        y1 = 220 + math.sin(math.radians(a)) * 250
        d.line([(x0, y0), (x1, y1)], fill=(255, 190, 60), width=16)
    draw_cloud(d, 330, 260, 2.2)
    draw_cloud(d, 900, 180, 1.5)
    draw_cloud(d, 1700, 300, 1.8)
    for (bx, by, s) in ((1250, 260, 1.4), (1420, 320, 1.0)):
        for sgn in (-1, 1):
            d.arc([bx - 40 * s * (1 if sgn < 0 else 0) + (0 if sgn < 0 else 0), by - 20 * s, bx + 40 * s, by + 20 * s], 200, 340, fill=(90, 110, 150), width=8)
    # titre
    f_title = ImageFont.truetype(BOLD, 210)
    f_sub = ImageFont.truetype(BOLD, 92)
    f_instr = ImageFont.truetype(BOLD, 74)
    f_label = ImageFont.truetype(BOLD, 56)
    f_small = ImageFont.truetype(BOLD, 44)
    title = "L'AIR"
    tw = d.textlength(title, font=f_title)
    tx, ty = 140, 110
    d.text((tx + 10, ty + 12), title, font=f_title, fill=(60, 70, 110))
    d.text((tx, ty), title, font=f_title, fill=(255, 255, 255), stroke_width=14, stroke_fill=col_accent)
    # badge numéro
    bx0, by0 = tx + tw + 90, ty + 30
    d.rounded_rectangle([bx0, by0, bx0 + 260, by0 + 170], radius=60, fill=col_accent, outline=(255, 255, 255), width=10)
    bf = ImageFont.truetype(BOLD, 96)
    nb = f"{idx}/8"
    d.text((bx0 + 130 - d.textlength(nb, font=bf) / 2, by0 + 26), nb, font=bf, fill=(255, 255, 255))
    # sous-titre
    d.text((tx, ty + 250), titre, font=f_sub, fill=(60, 70, 110))
    # consigne
    instr = "Trouve les 2 intrus et entoure-les !"
    iw = d.textlength(instr, font=f_instr)
    d.rounded_rectangle([tx - 20, ty + 380, tx + iw + 40, ty + 500], radius=60, fill=(255, 255, 255), outline=col_accent, width=8)
    d.text((tx + 10, ty + 396), instr, font=f_instr, fill=(230, 90, 110))

    # grille 2 x 4
    gx, gy = 140, ty + 560
    gw, gh = W - 280, H - gy - 260
    cw = (gw - 70) / 2
    ch = (gh - 3 * 50) / 4
    tile_cols = [(255, 255, 255), (255, 250, 235), (245, 250, 255), (250, 255, 245)]
    items = [(k, True) for k in air_keys] + [(k, False) for k in intr_keys]
    # Mélange déterministe différent par affiche
    order = [0, 4, 1, 7, 2, 5, 3, 6] if idx % 2 else [6, 1, 7, 0, 4, 2, 5, 3]
    items = [items[i] for i in order]
    for i, (key, is_air) in enumerate(items):
        r, c = divmod(i, 2)
        x0 = gx + c * (cw + 70)
        y0 = gy + r * (ch + 50)
        src, label = (AIR if is_air else INTR)[key]
        bgc = tile_cols[(i + idx) % 4]
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=60, fill=bgc, outline=col_accent if is_air else (200, 200, 210), width=10)
        pen = Pen(d, x0 + cw / 2, y0 + (ch - 110) / 2, min(cw - 120, ch - 220))
        src(pen)
        lw = d.textlength(label, font=f_label)
        d.text((x0 + cw / 2 - lw / 2, y0 + ch - 118), label, font=f_label, fill=(60, 70, 110))

    # corrigé en bas, à l'envers
    names = [INTR[k][1] for k in intr_keys]
    ans = f"Corrigé (affiche {idx}) : les intrus sont {names[0]} et {names[1]}."
    fs = ImageFont.truetype(BOLD, 40)
    tmp = Image.new("RGBA", (int(d.textlength(ans, font=fs)) + 20, 70), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((10, 5), ans, font=fs, fill=(130, 140, 160))
    tmp = tmp.rotate(180)
    img.paste(tmp, (W - tmp.width - 60, H - 110), tmp)
    return img

def make_corrige():
    img = Image.new("RGB", (W, H), (255, 252, 245))
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(BOLD, 150)
    f_h = ImageFont.truetype(BOLD, 78)
    f_t = ImageFont.truetype(BOLD, 62)
    d.text((W / 2 - d.textlength("Corrigé - L'AIR", font=f_title) / 2, 160), "Corrigé - L'AIR", font=f_title, fill=(60, 70, 110))
    y = 480
    for idx, (titre, airs, intrs, ct, ca) in enumerate(POSTERS, 1):
        names = [INTR[k][1] for k in intrs]
        d.rounded_rectangle([160, y, W - 160, y + 220], radius=50, fill=(255, 255, 255), outline=ca, width=8)
        d.text((220, y + 30), f"Affiche {idx} - {titre}", font=f_h, fill=(230, 90, 110))
        d.text((220, y + 130), f"Les intrus : {names[0]}  •  {names[1]}", font=f_t, fill=(60, 70, 110))
        y += 280
    d.text((W / 2 - d.textlength("Pour les grands : on entoure les 2 intrus de chaque affiche !", font=ImageFont.truetype(BOLD, 54)) / 2, H - 160),
           "Pour les grands : on entoure les 2 intrus de chaque affiche !", font=ImageFont.truetype(BOLD, 54), fill=(130, 140, 160))
    return img

def main():
    os.makedirs(OUT, exist_ok=True)
    pages = []
    for idx, (titre, airs, intrs, ct, ca) in enumerate(POSTERS, 1):
        img = make_poster(idx, titre, airs, intrs, ct, ca)
        p = os.path.join(OUT, f"affiche-{idx}.png")
        img.save(p, dpi=(300, 300))
        pages.append(img)
        print("ok", p)
    corr = make_corrige()
    corr.save(os.path.join(OUT, "corrige.png"), dpi=(300, 300))
    # PDF : affiches en 150 dpi + corrigé
    small = [im.resize((W // 2, H // 2), Image.LANCZOS).convert("RGB") for im in pages] + [corr.resize((W // 2, H // 2), Image.LANCZOS).convert("RGB")]
    small[0].save(os.path.join(OUT, "affiches-air.pdf"), save_all=True, append_images=small[1:], resolution=150)
    print("PDF ok")

if __name__ == "__main__":
    main()
