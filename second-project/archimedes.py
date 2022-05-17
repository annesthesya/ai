import copy

import pygame
import sys
import math
import time
import statistics

class Joc:
    JMIN = None
    JMAX = None
    GOL = '#'

    # coordonatele nodurilor ()
    @classmethod
    def initializeaza(cls, display, scalare = 100):
        '''
            Se încarcă toate imaginile și atributele necesare pentru a putea desena tabla de joc.
        '''
        cls.display = display
        cls.scalare = scalare
        cls.culoare_ecran = (166, 163, 182)
        cls.culoare_linii = (20, 6, 38)
        cls.translatie = 35
        cls.raza_punct = 15
        cls.raza_piesa = 25
        cls.piesa_alba = pygame.image.load('alb.png')
        diametru_piesa = 2 * cls.raza_piesa
        cls.piesa_alba = pygame.transform.scale(cls.piesa_alba, (diametru_piesa, diametru_piesa))
        cls.piesa_neagra = pygame.image.load('negru.png')
        cls.piesa_neagra = pygame.transform.scale(cls.piesa_neagra, (diametru_piesa, diametru_piesa))
        cls.piesa_alba_ocupata = pygame.image.load('alb-ocupat.png')
        cls.piesa_alba_ocupata = pygame.transform.scale(cls.piesa_alba_ocupata, (diametru_piesa, diametru_piesa))
        cls.piesa_neagra_ocupata = pygame.image.load('negru-ocupat.png')
        cls.piesa_neagra_ocupata = pygame.transform.scale(cls.piesa_neagra_ocupata, (diametru_piesa, diametru_piesa))
        cls.piesa_alba_selectata = pygame.image.load('alb-selectat.png')
        cls.piesa_alba_selectata = pygame.transform.scale(cls.piesa_alba_selectata, (diametru_piesa, diametru_piesa))
        cls.piesa_neagra_selectata = pygame.image.load('negru-selectat.png')
        cls.piesa_neagra_selectata = pygame.transform.scale(cls.piesa_neagra_selectata, (diametru_piesa, diametru_piesa))

    def deseneaza_ecran_joc(self):
        '''
        Metoda care desenează/actualizează starea curentă.
        '''
        Joc.display = pygame.display.set_mode(size=(600, 600))
        fundal = pygame.transform.scale(pygame.image.load("fundal.png"), (600, 600))
        Joc.display.blit(fundal, (0, 0))
        for muchie in self.muchii:
            a = self.coordonate_noduri[muchie[0]]
            b = self.coordonate_noduri[muchie[1]]
            pygame.draw.line(surface=Joc.display, color=Joc.culoare_linii, start_pos=a, end_pos=b, width=5)
        for nod in self.piese_albe:
            Joc.display.blit(self.piesa_alba, (nod[0] - self.raza_piesa, nod[1] - self.raza_piesa))
        for nod in self.piese_negre:
            Joc.display.blit(self.piesa_neagra, (nod[0] - self.raza_piesa, nod[1] - self.raza_piesa))
        if self.nod_piesa_selectata in self.piese_albe:
            Joc.display.blit(Joc.piesa_alba_selectata, (self.nod_piesa_selectata[0] - self.raza_piesa,
                                                    self.nod_piesa_selectata[1] - self.raza_piesa))
        if self.nod_piesa_selectata in self.piese_negre:
            Joc.display.blit(Joc.piesa_neagra_selectata, (self.nod_piesa_selectata[0] - self.raza_piesa,
                                                    self.nod_piesa_selectata[1] - self.raza_piesa))
        if self.nod_piesa_ocupata in self.piese_albe:
            Joc.display.blit(Joc.piesa_alba_ocupata, (self.nod_piesa_ocupata[0] - self.raza_piesa,
                                                    self.nod_piesa_ocupata[1] - self.raza_piesa))
        if self.nod_piesa_ocupata in self.piese_negre:
            Joc.display.blit(Joc.piesa_neagra_ocupata, (self.nod_piesa_ocupata[0] - self.raza_piesa,
                                                       self.nod_piesa_ocupata[1] - self.raza_piesa))
        pygame.display.update()
               
    def __init__(self, noduri = None, muchii = None, piese_albe = None, piese_negre = None, pozitii_albe = None,
                 pozitii_negre = None):
        '''
        Inițializează jocul cu piesele aranjate conform cerinței.
        '''
        if not noduri:
            self.noduri = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                          (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
                          (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
                          (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
                          (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
                          (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
                          (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                          (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)
                          ]
        if not muchii:
            self.muchii = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
                          (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15),
                          (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23),
                          (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31),
                          (32, 33), (33, 34), (34, 35), (35, 36), (36, 37), (37, 38), (38, 39),
                          (40, 41), (41, 42), (42, 43), (43, 44), (44, 45), (45, 46), (46, 47),
                          (48, 49), (49, 50), (50, 51), (51, 52), (52, 53), (53, 54), (54, 55),
                          (56, 57), (57, 58), (58, 59), (59, 60), (60, 61), (61, 62), (62, 63),  # linii
                          (0, 8), (8, 16), (16, 24), (24, 32), (32, 40), (40, 48), (48, 56),
                          (1, 9), (9, 17), (17, 25), (25, 33), (33, 41), (41, 49), (49, 57),
                          (2, 10), (10, 18), (18, 26), (26, 34), (34, 42), (42, 50), (50, 58),
                          (3, 11), (11, 19), (19, 27), (27, 35), (35, 43), (43, 51), (51, 59),
                          (4, 12), (12, 20), (20, 28), (28, 36), (36, 44), (44, 52), (52, 60),
                          (5, 13), (13, 21), (21, 29), (29, 37), (37, 45), (45, 53), (53, 61),
                          (6, 14), (14, 22), (22, 30), (30, 38), (38, 46), (46, 54), (54, 62),
                          (7, 15), (15, 23), (23, 31), (31, 39), (39, 47), (47, 55), (55, 63)  # coloane
                          ]
        self.coordonate_noduri = [[self.translatie + self.scalare * x for x in nod] for nod in self.noduri]
        if not piese_albe:
            self.piese_albe = [self.coordonate_noduri[4], self.coordonate_noduri[5], self.coordonate_noduri[6],
                               self.coordonate_noduri[12],
                               self.coordonate_noduri[13], self.coordonate_noduri[14], self.coordonate_noduri[15],
                               self.coordonate_noduri[21],
                               self.coordonate_noduri[22], self.coordonate_noduri[23], self.coordonate_noduri[30],
                               self.coordonate_noduri[31]
                               ]
        if not piese_negre:
            self.piese_negre = [self.coordonate_noduri[32], self.coordonate_noduri[33], self.coordonate_noduri[40],
                                self.coordonate_noduri[41],
                                self.coordonate_noduri[42], self.coordonate_noduri[48], self.coordonate_noduri[49],
                                self.coordonate_noduri[50],
                                self.coordonate_noduri[51], self.coordonate_noduri[57], self.coordonate_noduri[58],
                                self.coordonate_noduri[59]
                                ]
        self.nod_piesa_selectata = False
        self.nod_piesa_ocupata = False
        self.m_r_alb = []
        self.m_r_negru = []


    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def mutare_posibila(self, start, final):
        '''
        Verifică dacă mutarea din poziția start în poziția finală este posibilă, asigurându-se de aliniamentul
        direcției, de faptul că destinația nu are deja o piesă care să o ocupe și că piesa nu va sări peste
        vreun alt pion.
        '''
        if final in self.piese_negre + self.piese_albe:
            return False
        a = ((start[1] - Joc.translatie)//Joc.scalare, (start[0] - Joc.translatie)//Joc.scalare)
        b = ((final[1] - Joc.translatie)//Joc.scalare, (final[0] - Joc.translatie)//Joc.scalare)
        if a[0] == b[0] or a[1] == b[1] or abs(b[0] - a[0]) == abs(b[1]-a[1]):
            if b[0] - a[0] < 0:
                i = -1
            elif b[0] - a[0] == 0:
                i = 0
            else:
                i = 1
            if b[1] - a[1] < 0:
                j = -1
            elif b[1] - a[1] == 0:
                j = 0
            else:
                j = 1
            while a != b:
                a = (a[0] + i, a[1] + j)
                if [Joc.translatie + Joc.scalare * x for x in a] in self.piese_albe + self.piese_negre:
                    return False
            return True
        return False

    def calculeaza_matrici_risc(self):
        '''
        Calculează cele două matrici de risc pentru fiecare jucător, care reprezintă nivelul de risc al mutării
        unui pion pe fiecare poziție în funcție de câte piese adversare pot ajunge în acea poziție.
        '''
        self.m_r_alb = [[0] * 8] * 8
        self.m_r_negru = [[0] * 8] * 8
        albe = [((nod[1] - Joc.translatie)//Joc.scalare, (nod[0] - Joc.translatie)//Joc.scalare)
                for nod in self.piese_albe]
        negre = [((nod[1] - Joc.translatie)//Joc.scalare, (nod[0] - Joc.translatie)//Joc.scalare)
                for nod in self.piese_negre]
        for i in self.noduri:
            for j in albe:
                if self.mutare_posibila(i, j) == True:
                    self.m_r_negru[i[0]][i[1]] += 1
        for i in self.noduri:
            for j in negre:
                if self.mutare_posibila(i, j):
                    self.m_r_alb[i[0]][i[1]] += 1

    def captura(self):
        self.calculeaza_matrici_risc()
        for i in self.piese_albe:
            cop_i = [(x - Joc.translatie)//Joc.scalare for x in i]
            if self.m_r_alb[cop_i[0]][cop_i[1]] >= 3:
                self.piese_albe.remove(i)
        for i in self.piese_albe:
            cop_i = [(x - Joc.translatie)//Joc.scalare for x in i]
            if self.m_r_alb[cop_i[0]][cop_i[1]] >= 3:
                self.piese_albe.remove(i)
        self.deseneaza_ecran_joc()

    def mutari(self, jucator):
        '''
        Trece prin fiecare poziție a tablei de joc, verificând posibilitatea ca vreun pion al jucătorului să
        poată efectua mutarea respectivă. Dacă este posibil, starea cu mutarea efectuată se adaugă în lista
        de mutări posibile.
        '''
        l_mutari = []
        for i in self.coordonate_noduri:
            if [Joc.translatie + Joc.scalare * x for x in i] not in self.piese_negre + self.piese_albe:
                if jucator == "negru":
                    for j in self.piese_negre:
                        if self.mutare_posibila(i, j):
                            cop = copy.deepcopy(self)
                            cop.piese_negre.remove(j)
                            cop.piese_negre.append(i)
                            l_mutari.append(cop)
                else:
                    for j in self.piese_albe:
                        if self.mutare_posibila(j, i):
                            cop = copy.deepcopy(self)
                            cop.piese_albe.remove(j)
                            cop.piese_albe.append(i)
                            l_mutari.append(cop)
        return l_mutari

    def estimeaza_scor(self, adancime):
        '''
        Prima modalitate de a calcula scorul posibil al mutării, se adaugă numărul de poziții de risc
        crescut al adversarului și numărul de piese deținute, scăzând numărul de pioni ai adversarului
        și numărul de poziții apărate ale acestuia.
        '''
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return (self.__class__.scor_maxim + adancime)
        elif t_final == self.__class__.JMIN:
            return (-self.__class__.scor_maxim - adancime)
        else:
            sa = 0
            sn = 0
            for i in self.m_r_negru:
                for x in i:
                    if x >= 2:
                        sa += x
            for j in self.m_r_alb:
                for x in j:
                    if x >= 2:
                        sn += x
            if Joc.JMAX == "negru":
                return sa - sn - len(self.piese_albe) + len(self.piese_negre)
            return sn - sa + len(self.piese_albe) - len(self.piese_negre)

    def estimeaza_scor2(self):
        '''
        A doua modalitate de a estima scorul, se scade din distanța medie a pieselor adversarului
        distanța medie a pieselor calculatorului.
        '''
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return (self.__class__.scor_maxim + adancime)
        elif t_final == self.__class__.JMIN:
            return (-self.__class__.scor_maxim - adancime)
        else:
            a = mean([dist_euclid([Joc.translatie + Joc.scalare * x for x in (0, 7)], x) for x in piese_negre])
            b = mean([dist_euclid([Joc.translatie + Joc.scalare * x for x in (7, 0)], x) for x in piese_albe])
            if Joc.JMAX == "negru":
                return b - a
            else:
                return a - b

    def estimeaza_scor3(self):
        '''
        A treia modalitate de a estima scorul, se scade din numărul de poziții apărate și care au piese pe ele ale
        calculatorului cele ale adversarului.
        '''
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return (self.__class__.scor_maxim + adancime)
        elif t_final == self.__class__.JMIN:
            return (-self.__class__.scor_maxim - adancime)
        else:
            for i in self.m_r_alb:
                if i >= 3:
                    sa += i
                    if [Joc.translatie + Joc.scalare * x for x in i] in self.piese_albe:
                        sa += 5
            for j in self.m_r_negru:
                if j >= 3:
                    sn += i
                    if [Joc.translatie + Joc.scalare * x for x in i] in self.piese_negre:
                        sn += 5
            if Joc.JMAX == "negru":
                return sn - sa
            return sa - sn

    def final(self):
        '''
        Se verifică dacă s-a ajuns într-o stare finală, dacă există o piesă albă în portul negru sau vice versa, sau
        dacă vreun jucător a rămas fără piese.
        '''
        if len(self.piese_negre) == 0:
            return "alb"
        if len(self.piese_albe) == 0:
            return "negru"
        port_alb = (7, 0)
        port_negru = (0, 7)
        if [Joc.translatie + Joc.scalare * x for x in port_alb] in self.piese_negre:
            return "alb"
        if [Joc.translatie + Joc.scalare * x for x in port_negru] in self.piese_albe:
            return "negru"
        return False

    def __str__(self):
        matr = ['*' * 8] * 8
        for nod in self.piese_albe:
            nod = ((nod[1] - Joc.translatie)//Joc.scalare, (nod[0] - Joc.translatie)//Joc.scalare)
            matr[nod[0]] = matr[nod[0]][:nod[1]] + 'a' + matr[nod[0]][nod[1] + 1:]
        for nod in self.piese_negre:
            nod = ((nod[1] - Joc.translatie)//Joc.scalare, (nod[0] - Joc.translatie)//Joc.scalare)
            matr[nod[0]] = matr[nod[0]][:nod[1]] + 'n' + matr[nod[0]][nod[1] + 1:]
        return "\n".join(matr)+"\n"

class Stare():
    def __init__(self, tabla_joc, jucator_curent, adancime, parinte = None, scor = None):
        self.tabla_joc = tabla_joc
        self.jucator_curent = jucator_curent
        self.adancime = adancime
        self.mutari_posibile = []
        self.stare_aleasa = None
        self.scor = scor

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.jucator_curent)
        juc_opus = Joc.jucator_opus(self.jucator_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, int(self.adancime) - 1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Jucător curent:" + self.jucator_curent + ")\n"
        return sir

    def __repr__(self):
        sir = str(self.tabla_joc) + "(Jucător curent:" + self.jucator_curent + ")\n"
        return sir

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(145, 80, 199),
                 culoareFundalSel=(192, 125, 219), text="", font="courier-new", fontDimensiune=16, culoareText=(0, 0, 0),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteaza_dupa_coord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def update_dreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.update_dreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteaza_dupa_coord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteaza_dupa_coord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        for b in self.listaButoane:
            b.deseneaza()

    def get_valoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    fundal = pygame.transform.scale(pygame.image.load("fundal-meniu.png"), (600, 600))
    display.blit(fundal, (0, 0))
    font = pygame.font.SysFont('courier-new', 20)
    text = font.render('Neagu Anastasia - Archimedes', True, (0, 0, 0), (192, 125, 219))
    textRect = text.get_rect()
    textRect.center = (300, 175)
    display.blit(text, textRect)

    btn_alg = GrupButoane(
        top=225,
        left=190,
        listaButoane=[
            Buton(display=display, w=100, h=30, text="mini-max", valoare="minimax"),
            Buton(display=display, w=120, h=30, text="alpha-beta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=275,
        left=245,
        listaButoane=[
            Buton(display=display, w=60, h=30, text="negru", valoare="negru"),
            Buton(display=display, w=45, h=30, text="alb", valoare="alb")
        ],
        indiceSelectat=0)
    btn_dif = GrupButoane(
        top=325,
        left=195,
        listaButoane=[
            Buton(display=display, w=50, h=30, text="ușor", valoare="1"),
            Buton(display=display, w=70, h=30, text="mediu", valoare="2"),
            Buton(display=display, w=80, h=30, text="dificil", valoare="4")
        ],
        indiceSelectat=0)
    btn_mod = GrupButoane(
        top=375,
        left=0,
        listaButoane=[
            Buton(display=display, w=200, h=30, text="jucător vs jucător", valoare="pvp"),
            Buton(display=display, w=225, h=30, text="jucător vs calculator", valoare="pve"),
            Buton(display=display, w=140, h=30, text="calc vs calc", valoare="eve")
        ],
        indiceSelectat=1)
    ok = Buton(display=display, top=425, left=280, w=40, h=30, text="ok", culoareFundal = (235, 52, 177))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    btn_mod.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteaza_dupa_coord(pos):
                    if not btn_juc.selecteaza_dupa_coord(pos):
                        if not btn_dif.selecteaza_dupa_coord(pos):
                            if not btn_mod.selecteaza_dupa_coord(pos):
                                if ok.selecteaza_dupa_coord(pos):
                                    display.fill((0, 0, 0))  # stergere ecran
                                    tabla_curenta.deseneaza_ecran_joc
                                    return btn_juc.get_valoare(), btn_alg.get_valoare(), \
                                           btn_dif.get_valoare(), btn_mod.get_valoare()
        pygame.display.update()

def dist_euclid(a, b):
    (x0, y0) = a
    (x1, y1) = b
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    stare.mutari_posibile = stare.mutari()

    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.jucator_curent == Joc.JMAX:
        stare.stare_aleasa = max(mutari_scor, key = lambda x: x.scor)
    else:
        stare.stare_aleasa = min(mutari_scor, key = lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare

    stare.mutari_posibile = stare.mutari()

    for mp in stare.mutari_posibile:
        mp.scor = mp.tabla_joc.estimeaza_scor(mp.adancime-1)

    if stare.jucator_curent == Joc.JMAX:
        stare.mutari_posibile.sort(key = lambda x: x.scor, reverse=True)
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)
            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.jucator_curent == Joc.JMIN:
        stare.mutari_posibile.sort(key = lambda x: x.scor)
        scor_curent = float('inf')
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)
            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor
    return stare

def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        print("A castigat " + final)
        return True
    return False

def stop():
    pass

def pvp(stare_curenta, adancime_max):
    tabla_curenta = stare_curenta.tabla_joc
    # ============================================         PvP         =============================================
    while True:
        t_inainte = int(round(time.time() * 1000))

        if (stare_curenta.jucator_curent == Joc.JMIN):
            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        stop()
                        pygame.quit()
                        sys.exit()
                    elif ev.key == pygame.K_r:
                        pve(Stare(Joc(), 'negru', adancime_max), adancime_max)

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for nod in tabla_curenta.coordonate_noduri:

                        if dist_euclid(pos, nod) <= tabla_curenta.raza_punct:

                            if Joc.JMIN == 'negru':
                                piesa = tabla_curenta.piesa_neagra
                                piese_curente = tabla_curenta.piese_negre
                            else:
                                piesa = tabla_curenta.piesa_alba
                                piese_curente = tabla_curenta.piese_albe

                            if nod == tabla_curenta.nod_piesa_ocupata:
                                tabla_curenta.nod_piesa_ocupata = False

                            if nod == tabla_curenta.nod_piesa_selectata:
                                tabla_curenta.nod_piesa_selectata = False

                            if tabla_curenta.nod_piesa_selectata in piese_curente:

                                if nod not in tabla_curenta.piese_albe + tabla_curenta.piese_negre:
                                    if tabla_curenta.mutare_posibila(tabla_curenta.nod_piesa_selectata, nod):
                                        piese_curente.remove(tabla_curenta.nod_piesa_selectata)
                                        piese_curente.append(nod)
                                        tabla_curenta.nod_piesa_selectata = False
                                        tabla_curenta.nod_piesa_ocupata = False
                                        stare_curenta.jucator_curent = Joc.jucator_opus(stare_curenta.jucator_curent)
                                        t_dupa = int(round(time.time() * 1000))
                                        print("Jucatorul 1 a \"gandit\" timp de " + str(
                                            t_dupa - t_inainte) + " milisecunde.")
                                        tabla_curenta.captura()

                            else:
                                tabla_curenta.nod_piesa_selectata = False

                            if nod in piese_curente:
                                if not tabla_curenta.nod_piesa_selectata:
                                    tabla_curenta.nod_piesa_selectata = nod
                                    tabla_curenta.nod_piesa_ocupata = False
                            else:
                                tabla_curenta.nod_piesa_ocupata = nod

                            print(str(tabla_curenta))
                            tabla_curenta.deseneaza_ecran_joc()
                            break
        else:

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        stop()
                        pygame.quit()
                        sys.exit()
                    elif ev.key == pygame.K_r:
                        pve(Stare(Joc(), 'negru', adancime_max), adancime_max)

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for nod in tabla_curenta.coordonate_noduri:

                        if dist_euclid(pos, nod) <= tabla_curenta.raza_punct:

                            if Joc.JMAX == 'negru':
                                piesa = tabla_curenta.piesa_neagra
                                piese_curente = tabla_curenta.piese_negre
                            else:
                                piesa = tabla_curenta.piesa_alba
                                piese_curente = tabla_curenta.piese_albe

                            if nod == tabla_curenta.nod_piesa_ocupata:
                                tabla_curenta.nod_piesa_ocupata = False

                            if nod == tabla_curenta.nod_piesa_selectata:
                                tabla_curenta.nod_piesa_selectata = False

                            if tabla_curenta.nod_piesa_selectata in piese_curente:

                                if nod not in tabla_curenta.piese_albe + tabla_curenta.piese_negre:
                                    if tabla_curenta.mutare_posibila(tabla_curenta.nod_piesa_selectata, nod):
                                        piese_curente.remove(tabla_curenta.nod_piesa_selectata)
                                        piese_curente.append(nod)
                                        tabla_curenta.nod_piesa_selectata = False
                                        tabla_curenta.nod_piesa_ocupata = False
                                        stare_curenta.jucator_curent = Joc.jucator_opus(stare_curenta.jucator_curent)
                                        t_dupa = int(round(time.time() * 1000))
                                        print("Jucatorul 2 a \"gandit\" timp de " + str(
                                            t_dupa - t_inainte) + " milisecunde.")
                                        tabla_curenta.captura()

                            else:
                                tabla_curenta.nod_piesa_selectata = False

                            if nod in piese_curente:
                                if not tabla_curenta.nod_piesa_selectata:
                                    tabla_curenta.nod_piesa_selectata = nod
                                    tabla_curenta.nod_piesa_ocupata = False
                            else:
                                tabla_curenta.nod_piesa_ocupata = nod

                            print(str(tabla_curenta))
                            tabla_curenta.deseneaza_ecran_joc()
                            break

def pve(stare_curenta, adancime_max):
    lista_t = []
    t_start = int(round(time.time() * 1000))
    tabla_curenta = stare_curenta.tabla_joc
    while True:

        if (stare_curenta.jucator_curent == Joc.JMIN):
            t_inainte = int(round(time.time() * 1000))

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        stop()
                        pygame.quit()
                        sys.exit()
                    elif ev.key == pygame.K_r:
                        pve(Stare(Joc(), 'negru', adancime_max), adancime_max)

                if ev.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()

                    for nod in tabla_curenta.coordonate_noduri:

                        if dist_euclid(pos, nod) <= tabla_curenta.raza_punct:

                            if Joc.JMIN == 'negru':
                                piesa = tabla_curenta.piesa_neagra
                                piese_curente = tabla_curenta.piese_negre
                            else:
                                piesa = tabla_curenta.piesa_alba
                                piese_curente = tabla_curenta.piese_albe

                            if nod == tabla_curenta.nod_piesa_ocupata:
                                tabla_curenta.nod_piesa_ocupata = False

                            if nod == tabla_curenta.nod_piesa_selectata:
                                tabla_curenta.nod_piesa_selectata = False

                            if tabla_curenta.nod_piesa_selectata in piese_curente:

                                if nod not in tabla_curenta.piese_albe + tabla_curenta.piese_negre:
                                    if tabla_curenta.mutare_posibila(tabla_curenta.nod_piesa_selectata, nod):
                                        piese_curente.remove(tabla_curenta.nod_piesa_selectata)
                                        piese_curente.append(nod)
                                        tabla_curenta.nod_piesa_selectata = False
                                        tabla_curenta.nod_piesa_ocupata = False
                                        stare_curenta.jucator_curent = Joc.jucator_opus(stare_curenta.jucator_curent)
                                        t_dupa = int(round(time.time() * 1000))
                                        print("Jucatorul a \"gandit\" timp de " + str(
                                            t_dupa - t_inainte) + " milisecunde.")
                                        stare_curenta.tabla_joc = tabla_curenta
                                        tabla_curenta.captura()
                            else:
                                tabla_curenta.nod_piesa_selectata = False

                            if nod in piese_curente:
                                tabla_curenta.nod_piesa_selectata = nod
                                tabla_curenta.nod_piesa_ocupata = False
                            else:
                                tabla_curenta.nod_piesa_ocupata = nod
                                tabla_curenta.nod_piesa_selectata = False

                            print(str(tabla_curenta))
                            tabla_curenta.deseneaza_ecran_joc()
                            break

                if (afis_daca_final(stare_curenta)):
                    print("Timp \"gândire\" minim: ", min(lista_t))
                    print("Timp \"gândire\" maxim: ", max(lista_t))
                    print("Timp \"gândire\" mediu: ", statistics.mean(lista_t))
                    print("Mediana timpului de \"gândire\": ", statistics.median(lista_t))
                    t_stop = int(round(time.time() * 1000))
                    print("Timp total joc: ", t_stop - t_start)
                    break
        else:
            # print("Muta " + Joc.JMAX)
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("tabla_curenta dupa mutarea calculatorului\n" + str(stare_curenta))
            t_dupa = int(round(time.time() * 1000))
            lista_t.append(t_dupa-t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            stare_curenta.tabla_joc.deseneaza_ecran_joc()
            tabla_curenta.captura()
            if (afis_daca_final(stare_curenta)):
                print("Timp \"gândire\" minim: ", min(lista_t))
                print("Timp \"gândire\" maxim: ", max(lista_t))
                print("Timp \"gândire\" mediu: ", statistics.mean(lista_t))
                print("Mediana timpului de \"gândire\": ", statistics.median(lista_t))
                t_stop = int(round(time.time() * 1000))
                print("Timp total joc: ", t_stop-t_start)
                break
            stare_curenta.jucator_curent = Joc.jucator_opus(stare_curenta.jucator_curent)

def eve(stare_curenta):
    pass

def main():
    pygame.init()
    pygame.display.set_caption("Neagu Anastasia - Archimedes")
    ecran = pygame.display.set_mode(size=(600, 600))
    Joc.initializeaza(ecran, 75)

    tabla_curenta = Joc()

    Joc.JMIN, tip_algoritm, adancime_max, mod = deseneaza_alegeri(ecran, tabla_curenta)
    print(Joc.JMIN, tip_algoritm)
    stare_curenta = Stare(tabla_curenta, 'negru', adancime_max)

    Joc.JMAX = 'alb' if Joc.JMIN == 'negru' else 'negru'

    tabla_curenta = stare_curenta.tabla_joc
    tabla_curenta.calculeaza_matrici_risc()

    print("tabla_curenta initiala")
    print(str(tabla_curenta))

    tabla_curenta.deseneaza_ecran_joc()

    print(mod)

    if mod == "pvp":
        print("da")
        pvp(stare_curenta, adancime_max)
    elif mod == "pve":
        pve(stare_curenta, adancime_max)
    else:
        eve(stare_curenta, adancime_max)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
