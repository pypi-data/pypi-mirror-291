import psychrograph.psychro_aux as psy
# from psychrograph.timing import ExecutionTimer
import numpy as np


"""
FUNCIONES AUXILIARES PARA LA CONSTRUCCIÓN DEL DIAGRAMA
--------------------------------------------------------
Escrito por                               José E. Azzaro
--------------------------------------------------------
1. Cur_Sat - Calcula W de acuerdo a Tdb y RH
        aux == 0
        - Tdb es una matrix, RH un valor determninado
        aux <> 0
        - Tdb es un valor, RH es una matrix
        - calcula la temperatura límite para las curvas de RH

2. Cur_W - Calcula del punto de rocío de una matrix de valores de W
3. Calc_T_HUM - Calcula h (entalpía) conociendo Tdb y RH o W
        aux == 0
        - se conoce RH
        aux <> 0
        - se conoce W

4. Calc_T_h - Calcula W en función de Tdb y h
5. Calc_T_v - Calcula W en función de Tdb y v
6. Calc_T_RH - Calcula W en función de Tdb y RH
7. Calc_T_h_HUM - Calcula Twb en función de Tdb, h y RH o W
8. Calc_T_Twb - Calcula W en función de Tdb y Twb
"""


# @ExecutionTimer
def Cur_Sat(tdb, rh, patm, limits, aux):
    if aux == 0:
        with np.nditer([tdb, None]) as it:
            for x, y in it:
                XW = psy.ENHAC(x, patm, psy.VIRCOE(x))[2] * rh / 100.0
                XA = 1.0 - XW
                if XA == 0:
                    XA = 1e-05
                y[...] = 1000.0 * psy.MR * XW / XA
            return it.operands[1]
    else:
        with np.nditer([rh, None]) as it:
            for x, y in it:
                XW = psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[2] * x / 100.0
                XA = 1.0 - XW
                if XA == 0:
                    XA = 1e-05
                W = 1000.0 * psy.MR * XW / XA
                if W > limits[3]:
                    T_lim = psy.TDB7ITb(limits[3] / 1000.0, x, patm)
                else:
                    T_lim = limits[1]
                y[...] = T_lim
            return it.operands[1]


# @ExecutionTimer
def Cur_W(w, patm):
    with np.nditer([w, None]) as it:
        for x, y in it:
            y[...] = psy.DEWPTb(x / 1000.0, patm)
        return it.operands[1]


def Calc_T_HUM(tdb, hum, patm, aux):
    # if HUM = RH
    if aux == 0:
        XW = psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[2] * hum / 100.0
        XA = 1.0 - XW
        if XA == 0:
            XA = 1e-05
        W = psy.MR * XW / XA
        res = psy.MSTAIR(tdb, patm, psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[4], XA, XW, W, psy.VIRCOE(tdb))
    # if HUM = W
    else:
        XW = (hum / 1000.0) / (hum / 1000.0 + psy.MR)
        res = psy.MSTAIR(tdb, patm, psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[4], 1.0 - XW, XW, hum, psy.VIRCOE(tdb))
    v = res[0]
    h = res[1]
    VH = np.array([v, h])
    return VH


def Calc_T_h(tdb, h, patm):
    aux = psy.HFN2(tdb, patm, h, psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[2])
    W = aux[2] * 1000
    return W


def Calc_T_v(tdb, v, patm):
    XW = psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[2]
    W = psy.VFNITR(tdb, patm, v, XW)[2] * 1000.0
    return W


# @ExecutionTimer
def Calc_T_RH(tdb, rh, patm):
    B = psy.VIRCOE(tdb)
    XW = psy.ENHAC(tdb, patm, B)[2] * rh / 100.0
    XA = 1.0 - XW
    if XA == 0:
        XA = 1e-05
    W = 1000 * (psy.MR * XW / XA)
    return W


def Calc_T_h_HUM(tdb, h, hum, patm, aux):
    # if HUM = RH
    if aux == 0:
        XW = psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))[2] * hum / 100.0
        XA = 1.0 - XW
        if XA == 0:
            XA = 1e-05
        W = psy.MR * XW / XA
    # if HUM = W
    else:
        W = hum / 1000.0

    Tdp = psy.DEWPTb(W, patm)
    Twb = psy.WETTP(tdb, Tdp, h, W, patm)
    return Twb


def Calc_T_Twb(tdb, twb, patm):
    Efdb = psy.ENHAC(tdb, patm, psy.VIRCOE(tdb))
    Efwb = psy.ENHAC(twb, patm, psy.VIRCOE(twb))
    if twb >= 0:
        PSAT = psy.PWS_IAPWS97(twb) / 1000.0
    else:
        PSAT = psy.PWS_IAPWS98(tdb) / 1000.0
    WS = psy.MR * Efwb[0] * PSAT / (patm - Efwb[0] * PSAT)
    HWWB = psy.HW(twb, Efwb[4])
    FUN = psy.MSTAIR(twb, patm, Efwb[4], Efwb[1], Efwb[2], WS, psy.VIRCOE(twb))[1] - WS * HWWB
    W = 1000.0 * psy.HFUNIT(tdb, patm, FUN, HWWB, (Efdb[2] + Efwb[2]) / 2)[2]
    return W
