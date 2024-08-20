"""
Funciones auxiliares para calcular propiedades psicroétricas

--------------------------------------------------------
Escrito por                               José E. Azzaro
--------------------------------------------------------

Las funciones incluidas en este módulos son las siguientes

1.  ICAO        Formulación para calcular la presión atmosférica
2.  PWS_IAPWS97 Formulación de la presión de saturación de agua
3.  TWS_IAPWS97 Formulación de la temperatura de saturación del agua
4.  IAPWS98     Formulación de la presión de sublimación del agua
5.  VIRCOE      Cálculo de los Coeficientes Viriales
6.  ISOTCOMP    Cálculo de la Compresibilidad Isotérmica
7.  HENRYLAW    Cálculo de la Constante de la Ley de Henry
8.  ENHAC       Cálculo del factor de mejoramiento
9.  MSTAIR      Cálculo del Volumen específico y Entalpía
10. DEWPT       Cálculo de la Temperatura de Rocío
11. HW          Cálculo de la Entalpía específica del agua o hielo
12. WETTP       Cálculo de la temperatura de Bulbo Húmedo
13. WETTP2      Cálculo de la temperatura de Bulbo Húmedo
14. HFN2        Cálculo de las fracciones molares, el radio de humedad
                y el volumen específico dadas Tdb, PATM y H
15. VFNITR      Cálculo de las fracciones molares, el radio de humedad
                y la entalpía dadas Tdb, PATM y V
16. HFUNIT      Cálculo de las fracciones molares, el radio de humedad
                dadas Tdb, PATM, XW, HWWB y FUN
17. TDBITb      Cálculo de Tdb dados W y h
18. TDB2ITb     Cálculo de Tdb dados RH y h
19. TDB3ITb     Cálculo de Tdb dados W y v
20. TDB4ITb     Cálculo de Tdb dados RH y v
21. TDB5ITb     Cálculo de Tdb dados W y Twb
22. TDB6ITb     Cálculo de Tdb dados RH y Twb
23. TDB7ITb     Cálculo de Tdb dados W y RH

"""

import math
import numpy as np
from psychrograph.timing import ExecutionTimer
from scipy.optimize import root_scalar


""" Constante Molar gas kJ/kmol.K)
"""
Rm = 8.314472

""" Masa molecular del aire seco - kg/kmol
"""
Ma = 28.966

""" Masa molecular del agua - kg/kmol
"""
Mw = 18.015268

""" Relación de masas moleculares del Gas R = Ra/Rw = Mw/Ma
"""
MR = Mw / Ma

""" Constantes Comunes
"""
Ii = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                     1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0,
                     4.0, 4.0, 5.0, 8.0, 8.0, 21.0, 23.0, 29.0, 30.0, 31.0,
                     32.0])

Ji = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, -9.0, -7.0, -1.0,
                     0.0, 1.0, 3.0, -3.0, 0.0, 1.0, 3.0, 17.0, -4.0, 0.0, 6.0,
                     -5.0, -2.0, 10.0, -8.0, -11.0, -6.0, -29.0, -31.0, -38.0,
                     -39.0, -40.0, -41.0])

ni = np.array([0.14632971213167, -0.84548187169114, -3.756360367204,
                  3.3855169168385, -0.95791963387872, 0.15772038513228,
                  -0.016616417199501, 0.00081214629983568, 0.00028319080123804,
                   -0.00060706301565874, -0.018990068218419, -0.032529748770505,
                   -0.021841717175414, -0.00005283835796993,
                   -0.00047184321073267, -0.00030001780793026,
                   0.000047661393906987, -0.0000044141845330846,
                   -0.00000000000000072694996297594, -0.000031679644845054,
                   -0.0000028270797985312, -0.00000000085205128120103,
                   -0.0000022425281908, -0.00000065171222895601,
                   -0.00000000000014341729937924, -0.00000040516996860117,
                   -0.0000000012734301741641, -0.00000000017424871230634,
                   -6.8762131295531E-19, 1.4478307828521E-20,
                   2.6335781662795E-23, -1.1947622640071E-23,
                   1.8228094581404E-24, -9.3537087292458E-26])

g0 = np.array([-632020.233449497, 0.655022213658955,
                   -0.0000000189369929326131, 0.00000000000000339746123271053,
                   -5.56464869058991E-22])
s0 = -3327.33756492168
t1 = 0.0368017112855051 + 0.0510878114959572j
r1 = 44.7050716285388 + 65.6876847463481j
t2 = 0.337315741065416 + 0.335449415919319j
r20 = -72.597457432922 - 78.100842711287j
r21 = -0.0000557107698030123 + 0.0000464578634580806j
r22 = 0.0000000000234801409215913 - 0.0000000000285651142904972j

"""
-------------------------------------------------------
Funciones Psicrométricas AUXILIARES
--------------------------------------------------------
"""

"""
--------------------------------------------------------
1.  ICAO Formulación para presión atmosférica
    Unidades
    OUTPUT
    PATM  presión barométrica          (kPa)
    INPUT
    H     altitud sobre nivel del mar  (m)
"""


def patm_ICAO(H):
    P0 = 101.325
    P1 = 2.25577
    P2 = 5.2559

    if H > 11000 or H < -5000:
        # Altura fuera de límites
        err = "La Altura no puede ser <-5000 ni >11000"
        return err
    else:
        pbar = P0 * (1 - P1 * 0.00001 * H) ** P2
        return pbar

#-------------------------------------------------------

"""
--------------------------------------------------------
2.  IAPWS97 Formulación de la presión de saturación de agua
    Unidades
    OUTPUT
    PWS_IAPWS97                          (Pa)
    INPUT
    Tdb    temperatura de bulbo seco     (°C)
"""


def PWS_IAPWS97(Tdb):
    paux = 1000000
    # Constantes para la formulación IAPWS97
    n1 = 1167.0521452767
    n2 = -724213.16703206
    n3 = -17.073846940092
    n4 = 12020.82470247
    n5 = -3232555.0322333
    n6 = 14.91510861353
    n7 = -4823.2657361591
    n8 = 405113.40542057
    n9 = -0.23855557567849
    n10 = 650.17534844798

    TDBK = Tdb + 273.15

    if TDBK > 647.096 or TDBK < 273.15:
        err = "Temperatura fuera de rango > 647.096°K o < 273.15°K"
        return err
    else:
        vs = TDBK + n9 / (TDBK - n10)
        A = vs ** 2 + n1 * vs + n2
        B = n3 * vs ** 2 + n4 * vs + n5
        C = n6 * vs ** 2 + n7 * vs + n8
        PWS_97 = paux * (2 * C / (-B + (B ** 2 - 4 * A * C) ** 0.5)) ** 4
        return PWS_97

#-------------------------------------------------------


""" ----------------------------------------------------
2b.  Alternative formulation of Saturation Pressure
Unidades
    OUTPUT
    pws                                     (Pa)
    INPUT
    Tdb    temperatura de bulbo seco        (°C)
"""

def pws_Aprox(Tdb):
    pws = 610.78 * math.exp(17.2694 * Tdb / (Tdb + 237.3))
    return pws


""" ----------------------------------------------------
2c.  Alternative formulation of Derivative of Saturation Pressure
Unidades
    OUTPUT
    pws                                     (Pa)
    INPUT
    patm   barometric pressure              (Pa)
    tsref  saturation reference temperature (°C) 
"""

def dpws_Aprox(patm, tsref):
    aux = math.exp(17.2694 * tsref / (tsref + 237.3))
    dpws = MR * patm * 2.502904E6 * aux / ((tsref + 273.3)**2 * (patm - 610.78 * aux))
    return dpws


"""
--------------------------------------------------------
3.  IAPWS97 Formulación de la temperatura de saturación del agua
    Unidades
    OUTPUT
    TWS_IAPWS97                  (°K)
    INPUT
    ps    presión de saturación  (Pa)
"""


def TWS_IAPWS97(ps):
    paux = 1000000.0

    # Constantes para la formulación
    n1 = 1167.0521452767
    n2 = -724213.16703206
    n3 = -17.073846940092
    n4 = 12020.82470247
    n5 = -3232555.0322333
    n6 = 14.91510861353
    n7 = -4823.2657361591
    n8 = 405113.40542057
    n9 = -0.23855557567849
    n10 = 650.17534844798

    if ps > 22064000.0 or ps < 0.0006112:
        err = "Presión saturada fuera de rango > 22.064 MPa o < 0.0006112 Pa"
        return err
    else:
        beta = (ps / paux) ** 0.25
        E = beta ** 2 + n3 * beta + n6
        F = n1 * beta ** 2 + n4 * beta + n7
        G = n2 * beta ** 2 + n5 * beta + n8
        D = 2 * G / (-F - (F ** 2 - 4 * E * G) ** 0.5)

        TWS_97 = (n10 + D - (((n10 + D) ** 2) - 4 * (n9 + n10 * D)) ** 0.5) / 2
        return TWS_97

#-------------------------------------------------------

"""
--------------------------------------------------------
4.  IAPWS98 Formulación de la presión de sublimación del agua
    Unidades
    OUTPUT
    PWS_IAPWS98                         (Pa)
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
"""


def PWS_IAPWS98(Tdb):
    paux = 611.657
    Taux = 273.16

    # Constantes para la formulación IAPWS98
    a1 = -21.2144006
    a2 = 27.3203819
    a3 = -6.1059813
    b1 = 0.00333333333
    b2 = 1.20666667
    b3 = 1.70333333

    TDBK = Tdb + 273.15
    aux = TDBK / Taux

    if 130.0 < TDBK <= 273.15:
        PWS_98 = paux * math.exp(aux ** (-1) * (a1 * aux ** b1 +
                                                a2 * aux ** b2 + a3 * aux ** b3))
        return PWS_98
    else:
        err = "Temperatura fuera de rango >= 273.15°K or < 130°K"
        return err

#-------------------------------------------------------

"""
--------------------------------------------------------
5.  VIRCOE Cálculo de los Coeficientes Viriales
    OUTPUT
    B = [Baa Caaa Bww Cwww Baw Caaw Caww,
         dBaadT, dCaaadT, dBwwdT, dCwwwdT, dBawdT, dCaawdT, dCawwdT]
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
"""


def VIRCOE(Tdb):
    D = 0.0000000001         # Densidad reducida - Delta
    Md = 0.0104477           # Maxcondentherm densidad molar (mol/cm3)
    Tj = 132.6312            # Maxcondentherm temperature (°K)
    Tc = 647.096             # Temperatura Crítica (°K)
    Mc = 0.322               # Densidad Crítica (mol/cm3)
    Tred = 100.0             # Temperatura Reducida (°K)

    TDBK = Tdb + 273.15
    Nk = np.array([0.118160747229, 0.713116392079, -1.61824192067,
            0.0714140178971, -0.0865421396646, 0.134211176704,
            0.0112626704218, -0.0420533228842, 0.0349008431982,
            0.000164957183186, -0.101365037912, -0.17381369097,
            -0.0472103183731, -0.0122523554253, -0.146629609713,
            -0.0316055879821, 0.000233594806142, 0.0148287891978,
            -0.00938782884667])

    ik = np.array([1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 6.0, 1.0, 3.0,
            5.0, 6.0, 1.0, 3.0, 11.0, 1.0, 3.0])

    jk = np.array([0.0, 0.33, 1.01, 0.0, 0.0, 0.15, 0.0, 0.2, 0.35, 1.35, 1.6,
            0.8, 0.95, 1.25, 3.6, 6.0, 3.25, 3.5, 15])

    lk = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
            1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0])

    Tau = Tj / TDBK

    """ Baa - Cálculo (cm3/mol)
        dBaa/dT (cm3/mol.°K) """
    F1 = 0.0
    F2 = 0.0
    Y1 = 0.0
    Y2 = 0.0
    for i in range(19):
        if i < 10:
            F1 += ik[i] * Nk[i] * D ** (ik[i] - 1) * Tau ** jk[i]
            Y1 += ik[i] * jk[i] * Nk[i] * D ** (ik[i] - 1) * Tau ** (jk[i] - 1)
        else:
            F2 += Nk[i] * D ** (ik[i] - 1) * Tau ** jk[i] * \
                math.exp(-D ** lk[i]) * (ik[i] - lk[i] * D ** lk[i])
            Y2 += jk[i] * Nk[i] * D ** (ik[i] - 1) * Tau ** (jk[i] - 1) \
                * math.exp(-D ** lk[i]) * (ik[i] - lk[i] * D ** lk[i])

    Baa = (1 / Md) * (F1 + F2)
    dBaadT = -1 / (Md * Tj) * Tau ** 2 * (Y1 + Y2)

    """ Caaa - Cálculo (cm6/mol2) '
    ' dCaaadT (cm6/mol2.°K) """
    F3 = 0.0
    F4 = 0.0
    Y3 = 0.0
    Y4 = 0.0
    for i in range(19):
        if i < 10:
            F3 += ik[i] * (ik[i] - 1) * Nk[i] * D ** (ik[i] - 2) * Tau ** jk[i]
            Y3 += ik[i] * (ik[i] - 1) * jk[i] * Nk[i] * D ** (ik[i] - 2) * \
                Tau ** (jk[i] - 1)
        else:
            F4 += Nk[i] * D ** (ik[i] - 2) * Tau ** jk[i] * \
                math.exp(-D ** lk[i]) * ((ik[i] - lk[i] * D ** lk[i]) *
                (ik[i] - 1 - lk[i] * D ** lk[i]) - lk[i] ** 2 * D ** lk[i])
            Y4 += jk[i] * Nk[i] * D ** (ik[i] - 2) * Tau ** (jk[i] - 1) * \
                math.exp(-D ** lk[i]) * ((ik[i] - lk[i] * D ** lk[i]) *
                (ik[i] - 1 - lk[i] * D ** lk[i]) - lk[i] ** 2 * D ** lk[i])

    Caaa = (1 / Md ** 2) * (F3 + F4)
    dCaaadT = -1 / (Md ** 2 * Tj) * Tau ** 2 * (Y3 + Y4)

    ci = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0,
                   2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
                   2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 4.0, 6.0,
                   6.0, 6.0, 6.0, 0.0, 0.0, 0.0, 3.5, 3.5])

    di = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 4.0, 1.0, 1.0, 1.0, 2.0, 2.0,
                   3.0, 4.0, 4.0, 5.0, 7.0, 9.0, 10.0, 11.0, 13.0, 15.0, 1.0,
                   2.0, 2.0, 2.0, 3.0, 4.0, 4.0, 4.0, 5.0, 6.0, 6.0, 7.0, 9.0,
                   9.0, 9.0, 9.0, 9.0, 10.0, 10.0, 12.0, 3.0, 4.0, 4.0, 5.0,
                   14.0, 3.0, 6.0, 6.0, 6.0, 3.0, 3.0, 3.0, 0.85, 0.95])

    ti = np.array([-0.5, 0.875, 1.0, 0.5, 0.75, 0.375, 1.0, 4.0, 6.0, 12.0,
                   1.0, 5.0, 4.0, 2.0, 13.0, 9.0, 3.0, 4.0, 11.0, 4.0, 13.0,
                   1.0, 7.0, 1.0, 9.0, 10.0, 10.0, 3.0, 7.0, 10.0, 10.0, 6.0,
                   10.0, 10.0, 1.0, 2.0, 3.0, 4.0, 8.0, 6.0, 9.0, 8.0, 16.0,
                   22.0, 23.0, 23.0, 10.0, 50.0, 44.0, 46.0, 50.0, 0.0, 1.0,
                   4.0, 0.2, 0.2])

    ni = np.array([0.012533547935523, 7.8957634722828, -8.7803203303561,
                   0.31802509345418, -0.26145533859358, -0.0078199751687981,
                   0.0088089493102134, -0.66856572307965, 0.20433810950965,
                   -0.000066212605039687, -0.19232721156002, -0.25709043003438,
                   0.16074868486251, -0.040092828925807, 0.00000039343422603254,
                   -0.0000075941377088144, 0.00056250979351888,
                   -0.000015608652257135, 0.0000000011537996422951,
                   0.00000036582165144204, -0.0000000000013251180074668,
                   -0.00000000062639586912454, -0.10793600908921,
                   0.017611491008752, 0.22132295167546, -0.40247669763528,
                   0.58083399985759, 0.0049969146990806, -0.031358700712549,
                   -0.74315929710341, 0.4780732991548, 0.020527940895948,
                   -0.13636435110343, 0.014180634400617, 0.0083326504880713,
                   -0.029052336009585, 0.038615085574206, -0.020393486513704,
                   -0.0016554050063734, 0.0019955571979541, 0.00015870308324157,
                   -0.00001638856834253, 0.043613615723811, 0.034994005463765,
                   -0.076788197844621, 0.022446277332006, -0.000062689710414685,
                   -0.0000000005571111856564, -0.19905718354408,
                   0.3177497330738, -0.11841182425981, -31.306260323435,
                   31.546140237781, -2521.3154341695, -0.14874640856724,
                   0.31806110878444])

    alfai = np.array([20.0, 20.0, 20.0, 28.0, 32.0])
    betai = np.array([150.0, 150.0, 250.0, 700.0, 800.0])
    gammai = np.array([1.21, 1.21, 1.25, 0.32, 0.32])
    etai = np.array([1.0, 1.0, 1.0, 0.3, 0.3])

    Tau = Tc / TDBK
    Mcd = Mc / Mw

    """ Bww - Cálculo (cm3/mol)
        dBwwdT (cm3/mol.°K) """
    F5 = 0.0
    F6 = 0.0
    F7 = 0.0
    F8 = 0.0
    Y5 = 0.0
    Y6 = 0.0
    Y7 = 0.0
    Y8 = 0.0
    for i in range(56):
        if i < 7:
            F5 += ni[i] * di[i] * D ** (di[i] - 1) * Tau ** ti[i]
            Y5 += ni[i] * di[i] * ti[i] * D ** (di[i] - 1) * Tau ** (ti[i] - 1)
        elif i >= 7 and i < 51:
            F6 += ni[i] * math.exp(-D ** ci[i]) * (D ** (di[i] - 1) *
                Tau ** ti[i] * (di[i] - ci[i] * D ** ci[i]))
            Y6 += ni[i] * ti[i] * D ** (di[i] - 1) * Tau ** (ti[i] - 1) * \
                (di[i] - ci[i] * D ** ci[i]) * math.exp(-D ** ci[i])
        elif i >= 51 and i < 54:
            F7 += ni[i] * D ** di[i] * Tau ** ti[i] * math.exp(-alfai[i - 51] *
                (D - etai[i - 51]) ** 2 - betai[i - 51] * (Tau -
                gammai[i - 51]) ** 2) * (di[i] / D - 2 * alfai[i - 51] *
                (D - etai[i - 51]))
            Y7 += ni[i] * D ** di[i] * Tau ** ti[i] * math.exp(-alfai[i - 51] *
                (D - etai[i - 51]) ** 2 - betai[i - 51] * (Tau -
                gammai[i - 51]) ** 2) * (di[i] / D - 2 * alfai[i - 51] *
                (D - etai[i - 51])) * (ti[i] / Tau - 2 * betai[i - 51] *
                (Tau - gammai[i - 51]))
        else:
            titai = (1 - Tau) + gammai[i - 51] * ((D - 1) ** 2) \
                ** (1 / (2 * etai[i - 51]))
            deltai = titai ** 2 + ti[i] * ((D - 1) ** 2) ** ci[i]
            psii = math.exp(-alfai[i - 51] * (D - 1) ** 2 - betai[i - 51] *
                (Tau - 1) ** 2)
            dpsiidD = -2 * alfai[i - 51] * (D - 1) * psii
            dpsiidTau = -2 * betai[i - 51] * (Tau - 1) * psii
            d2psiidDTau = 4 * alfai[i - 51] * betai[i - 51] * (D - 1) * \
                (Tau - 1) * psii
            ddeltaidD = (D - 1) * (gammai[i - 51] * titai * 2 / etai[i - 51] *
                ((D - 1) ** 2) ** (1 / (2 * etai[i - 51]) - 1) + 2 * ti[i] *
                ci[i] * ((D - 1) ** 2) ** (ci[i] - 1))
            ddeltaibidD = di[i] * deltai ** (di[i] - 1) * ddeltaidD
            ddeltaibidTau = -2 * titai * di[i] * deltai ** (di[i] - 1)
            d2deltaibidDTau = -gammai[i - 51] * di[i] * (2 / etai[i - 51]) * \
                (D - 1) * ((D - 1) ** 2) ** (1 / (2 * etai[i - 51]) - 1) - \
                2 * titai * di[i] * (di[i] - 1) * deltai ** (di[i] - 2) * \
                ddeltaidD

            F8 += ni[i] * (deltai ** di[i] * (psii + D * dpsiidD) +
                ddeltaibidD * D * psii)
            Y8 += ni[i] * (deltai ** di[i] * (dpsiidTau + D * d2psiidDTau) +
                D * ddeltaibidD * dpsiidTau + ddeltaibidTau * (psii + D *
                dpsiidD) + d2deltaibidDTau * D * psii)

    Bww = (1 / Mcd) * (F5 + F6 + F7 + F8)
    dBwwdT = -1 / (Mcd * Tc) * Tau ** 2 * (Y5 + Y6 + Y7 + Y8)

    """ Cwww Calculation (cm6/mol2)
        dCwwwdT (cm6/mol2.°K) """
    F9 = 0.0
    F10 = 0.0
    F11 = 0.0
    F12 = 0.0
    Y9 = 0.0
    Y10 = 0.0
    Y11 = 0.0
    Y12 = 0.0
    for i in range(56):
        if i < 7:
            F9 += ni[i] * di[i] * (di[i] - 1) * D ** (di[i] - 2) * Tau ** ti[i]
            Y9 += ni[i] * di[i] * ti[i] * (di[i] - 1) * D ** (di[i] - 2) * \
                Tau ** (ti[i] - 1)
        elif i >= 7 and i < 51:
            F10 += ni[i] * math.exp(-D ** ci[i]) * (D ** (di[i] - 2) *
                Tau ** ti[i] * ((di[i] - ci[i] * D ** ci[i]) * (di[i] - 1 -
                ci[i] * D ** ci[i]) - ci[i] ** 2 * D ** ci[i]))
            Y10 += ni[i] * ti[i] * math.exp(-D ** ci[i]) * D ** (di[i] - 2) * \
                Tau ** (ti[i] - 1) * ((di[i] - ci[i] * D ** ci[i]) * (di[i] -
                1 - ci[i] * D ** ci[i]) - ci[i] ** 2 * D ** ci[i])
        elif i >= 51 and i < 54:
            F11 += ni[i] * Tau ** ti[i] * math.exp(-alfai[i - 51] * (D -
                etai[i - 51]) ** 2 - betai[i - 51] * (Tau - gammai[i - 51])
                ** 2) * (-2 * alfai[i - 51] * D ** di[i] + 4 * alfai[i - 51]
                ** 2 * D ** di[i] * (D - etai[i - 51]) ** 2 - 4 * di[i] *
                alfai[i - 51] * D ** (di[i] - 1) * (D - etai[i - 51]) + di[i]
                * (di[i] - 1) * D ** (di[i] - 2))
            Y11 += ni[i] * Tau ** ti[i] * math.exp(-alfai[i - 51] * (D -
                etai[i - 51]) ** 2 - betai[i - 51] * (Tau - gammai[i - 51])
                ** 2) * (ti[i] / Tau - 2 * betai[i - 51] * (Tau -
                gammai[i - 51])) * (-2 * alfai[i - 51] * D ** di[i] + 4 *
                alfai[i - 51] ** 2 * D ** di[i] * (D - etai[i - 51]) ** 2 -
                4 * di[i] * alfai[i - 51] * D ** (di[i] - 1) * (D -
                etai[i - 51]) + di[i] * (di[i] - 1) * D ** (di[i] - 2))
        else:
            titai = (1 - Tau) + gammai[i - 51] * ((D - 1) ** 2) ** (1 /
                (2 * etai[i - 51]))
            deltai = titai ** 2 + ti[i] * ((D - 1) ** 2) ** ci[i]
            psii = math.exp(-alfai[i - 51] * (D - 1) ** 2 - betai[i - 51] *
                (Tau - 1) ** 2)

            dpsiidD = -2 * alfai[i - 51] * (D - 1) * psii
            dpsiidTau = -2 * betai[i - 51] * (Tau - 1) * psii
            d2psiidDTau = 4 * alfai[i - 51] * betai[i - 51] * (D - 1) * \
                (Tau - 1) * psii
            d2psiidD = (2 * alfai[i - 51] * (D - 1) ** 2 - 1) * 2 * \
                alfai[i - 51] * psii
            d3psiid2DdTau = -2 * (4 * alfai[i - 51] * (D - 1) ** 2 - 2) * \
                alfai[i - 51] * betai[i - 51] * (Tau - 1) * psii

            ddeltaidD = (D - 1) * (gammai[i - 51] * titai * 2 / etai[i - 51] *
                ((D - 1) ** 2) ** (1 / (2 * etai[i - 51]) - 1) + 2 * ti[i] *
                ci[i] * ((D - 1) ** 2) ** (ci[i] - 1))
            ddeltaidTau = -2 * ((1 - Tau) + gammai[i - 51] * ((D - 1) ** 2) **
                (1 / (2 * etai[i - 51])))
            d2deltaidD = (1 / (D - 1)) * ddeltaidD + (D - 1) ** 2 * \
                (gammai[i - 51] ** 2 * (2 / etai[i - 51] ** 2) * (((D - 1)
                ** 2) ** (1 / (2 * etai[i - 51]) - 1)) ** 2 + gammai[i - 51] *
                titai * (4 / etai[i - 51]) * (1 / (2 * etai[i - 51]) - 1) *
                ((D - 1) ** 2) ** (1 / (2 * etai[i - 51]) - 2) + 4 * ti[i] *
                ci[i] * (ci[i] - 1) * ((D - 1) ** 2) ** (ci[i] - 2))
            d2deltaidDdTau = -(D - 1) * gammai[i - 51] * (2 / etai[i - 51]) * \
                ((D - 1) ** 2) ** ((1 / (2 / etai[i - 51])) - 1)
            d3deltaid2DdTau = (1 / (D - 1)) * d2deltaidDdTau - (D - 1) ** 2 * \
                gammai[i - 51] * (4 / etai[i - 51]) * ((1 / (2 / etai[i - 51]))
                - 1) * ((D - 1) ** 2) ** ((1 / (2 / etai[i - 51])) - 2)

            ddeltaibidD = di[i] * deltai ** (di[i] - 1) * ddeltaidD
            ddeltaibidTau = -2 * titai * di[i] * deltai ** (di[i] - 1)
            #ddeltaibiidTau = (di[i] - 1) * deltai ** (di[i] - 2) * \
            #                    ddeltaibidTau
            ddeltaibiiidTau = (di[i] - 2) * deltai ** (di[i] - 3) * ddeltaidTau
            d2deltaibidD = di[i] * (deltai ** (di[i] - 1) * d2deltaidD + (di[i]
                - 1) * deltai ** (di[i] - 2) * ddeltaidD ** 2)
            d2deltaibidDTau = -gammai[i - 51] * di[i] * (2 / etai[i - 51]) * \
                (D - 1) * ((D - 1) ** 2) ** (1 / (2 * etai[i - 51]) - 1) - \
                2 * titai * di[i] * (di[i] - 1) * deltai ** (di[i] - 2) * \
                ddeltaidD
            d3deltaibid2DdTau = di[i] * ((d2deltaibidDTau * d2deltaidD + deltai
                ** (di[i] - 1) * d3deltaid2DdTau) + (di[i] - 1) *
                (ddeltaibiiidTau * ddeltaidD ** 2 + deltai ** (di[i] - 2) * 2
                * d2deltaidDdTau * ddeltaidD))
            F12 += ni[i] * (deltai ** di[i] * (2 * dpsiidD + D * d2psiidD) +
                2 * ddeltaibidD * (psii + D * dpsiidD) + (d2deltaibidD * D *
                psii))
            Y12 += ni[i] * (deltai ** di[i] * (2 * d2psiidDTau + D *
                d3psiid2DdTau) + ddeltaibidTau * (2 * dpsiidD + D * d2psiidD) +
                2 * d2deltaibidDTau * (psii + D * dpsiidD) + 2 * ddeltaibidD *
                (dpsiidTau + D * d2psiidDTau) + d3deltaibid2DdTau * D * psii +
                d2deltaibidD * D * dpsiidTau)

    Cwww = (1 / Mcd ** 2) * (F9 + F10 + F11 + F12)
    dCwwwdT = -(1 / (Mcd ** 2 * Tc)) * Tau ** 2 * (Y9 + Y10 + Y11 + Y12)

    ai = np.array([66.5687, -238.834, -176.755])
    bi = np.array([-0.237, -1.048, -3.183])

    tita = TDBK / Tred

    F13 = 0.0
    Y13 = 0.0

    """ Baw Calculation (cm3/mol)
        dBawdT (cm3/mol.°K) """

    for i in range(3):
        F13 += ai[i] * tita ** bi[i]
        Y13 += ai[i] * bi[i] * tita ** (bi[i] - 1)

    Baw = F13
    dBawdT = 1 / Tred * Y13

    cii = np.array([482.737, 105678.0, -65639400.0, 29444200000.0,
            -3193170000000.0])
    dii = np.array([-10.72887, 3478.04, -383383.0, 33406000.0])

    """ Caaw - Cálculo (cm6/mol2)
        dCaawdT (cm6/mol2.°K) """
    F14 = 0
    Y14 = 0.0

    for i in range(5):
        F14 += cii[i] * TDBK ** (-i)
        Y14 += cii[i] * (-i) * TDBK ** (-i - 1)

    Caaw = F14
    dCaawdT = Y14

    """ Caww Calculation (cm6/mol2)
        dCawwdT (cm6/mol2.°K) """
    F15 = 0.0
    Y15 = 0.0

    for i in range(4):
        F15 += dii[i] * TDBK ** (-i)
        Y15 += dii[i] * (-i) * TDBK ** (-i - 1)

    Caww = -(1 / 0.001 ** 2) * math.exp(F15)
    dCawwdT = Caww * Y15

    B = np.array([Baa, Caaa, Bww, Cwww, Baw, Caaw, Caww, dBaadT, dCaaadT, dBwwdT, dCwwwdT, dBawdT, dCaawdT, dCawwdT])
    return B

#-------------------------------------------------------


"""
--------------------------------------------------------
6.  ISOTCOMP Cálculo de la Compresibilidad Isotérmica
    OUTPUT
    kT            Compresibilidad Isotérmica (1/Pa)
    vws           Volumen molar del líquido saturado (m3/kmol)
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
    PATM   Presión Barométrica          (kPa)
"""


def ISOTCOMP(Tdb, PATM):
    Taux = 1386.0          # (°K)
    paux = 16530.0         # (kPa)
    p0 = 101.325           # Normal Presure (kPa)
    pt = 0.611657          # Triple point pressure (kPa)
    Tt = 273.16            # Triple point temperature (°K)
    R97 = 0.461526         # Specific gas constant (kJ/kg°K)

    TDBK = Tdb + 273.15
    Tau = Taux / TDBK
    F1 = 0.0
    F2 = 0.0
    g0p = 0.0
    g0pp = 0.0

    if TDBK >= 273.15:
        pi = PATM / paux
        for i in range(34):
            F1 += -ni[i] * Ii[i] * (7.1 - pi) ** (Ii[i] - 1) * (Tau - 1.222) \
                ** Ji[i]
            F2 += ni[i] * Ii[i] * (Ii[i] - 1) * (7.1 - pi) ** (Ii[i] - 2) * \
                (Tau - 1.222) ** Ji[i]
        dgammadpi = F1
        d2gammadpi = F2
        PATM = PATM * 1000.0
        kT = -(1 / PATM) * pi * d2gammadpi * dgammadpi ** (-1)
        vws = Mw * R97 * TDBK * pi * dgammadpi / PATM
    else:
        tita = TDBK / Tt
        pi = PATM / pt
        pi0 = p0 / pt
        pt = pt * 1000
        for i in range(1, 5):
            g0p += g0[i] * (i / pt) * (pi - pi0) ** (i - 1)
        r2p = r21 * (1 / pt) + r22 * (2 / pt) * (pi - pi0)
        aux1 = r2p * ((t2 - tita) * np.log(t2 - tita) + (t2 + tita) *
                np.log(t2 + tita) - 2 * t2 * np.log(t2) - tita ** 2 / t2)
        dgdp = g0p + Tt * aux1.real
        for i in range(2, 5):
            g0pp += g0[i] * i * ((i - 1) / pt ** 2) * (pi - pi0) ** (i - 2)
        r2pp = r22 * 2 / pt ** 2
        aux2 = r2pp * ((t2 - tita) * np.log(t2 - tita) + (t2 + tita) *
                np.log(t2 + tita) - 2 * t2 * np.log(t2) - tita ** 2 / t2)
        d2gdp = g0pp + Tt * aux2.real
        kT = -d2gdp * dgdp ** (-1)
        vws = Mw * dgdp

    IsotComp = np.array([kT, vws])
    return IsotComp

#-------------------------------------------------------


"""
--------------------------------------------------------
7.  HENRYLAW Cálculo de la Constante de la Ley de Henry
    OUTPUT
    bH            Constante de la Ley de Henry
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
    PATM   Presión Barométrica          (kPa)
"""


def HENRYLAW(Tdb, PATM):
    Tc = 647.096        # Temperatura Crítica (°K)

    psi = np.array([0.7812, 0.2095, 0.0093])
    Ai = np.array([-9.67578, -9.44833, -8.40954])
    Bi = np.array([4.72162, 4.43822, 4.29587])
    Ci = np.array([11.70585, 11.42005, 10.52779])

    TDBK = Tdb + 273.15
    Tr = TDBK / Tc
    Tau = 1 - Tr
    P = PATM * 1000.0
    betai = np.zeros(3)
    aux = 0.0

    if TDBK >= 273.15:
        pws = PWS_IAPWS97(Tdb)
        if pws > P:
            pws = P
        for i in range(3):
            betai[i] = pws * math.exp(Ai[i] / Tr + Bi[i] * Tau ** 0.355 / Tr +
                Ci[i] * Tr ** (-0.41) * math.exp(Tau))
            aux += psi[i] / betai[i]
        betaa = 1 / aux
        bH = 1 / (1.01325 * betaa)
    else:
        bH = 0

    return bH

#-------------------------------------------------------


"""
--------------------------------------------------------
8.  ENHAC Cálculo del factor de mejoramiento
    OUTPUT
    Ef = [f, XAS, XWS, WS, pws] Enhacement factor, fracciones saturadas,
                                radio de humedad saturado y presión de vapor
                                del agua pura (kPa)
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
    PATM   Presión Barométrica          (kPa)
    B      coeficientes viriales
"""


def ENHAC(Tdb, PATM, B):
    R = Rm * 1000000.0
    P = PATM * 1000.0
    TDBK = Tdb + 273.15

    if TDBK >= 273.15:
        pws = PWS_IAPWS97(Tdb)
        if pws > P:
            pws = P
        aux = ISOTCOMP(Tdb, pws / 1000.0)
        vws = aux[1] * 1000000
        aux = ISOTCOMP(Tdb, PATM)
        kT = aux[0]
        if pws > P:
            kT = 0.0
    else:
        pws = PWS_IAPWS98(Tdb)
        aux = ISOTCOMP(Tdb, pws / 1000.0)
        vws = aux[1] * 1000
        aux = ISOTCOMP(Tdb, PATM)
        kT = aux[0]

    bH = HENRYLAW(Tdb, PATM)

    f = 0.0
    X1 = (P - pws) / P
    F0 = 1.0
    err = abs(f - F0)
    j = 1
    while (err > 1e-08) and (j < 50):
        # B = [Baa Caaa Bww Cwww Baw Caaw Caww]
        F1 = (((1 + kT * pws) * (P - pws) - kT * (P ** 2 - pws ** 2) / 2) *
                vws) / (R * TDBK)
        F2 = np.log(1 - bH * X1 * P)
        F3 = (X1 ** 2 * P * B[0]) / (R * TDBK)
        F4 = -(2 * X1 ** 2 * P * B[4]) / (R * TDBK)
        F5 = -(B[2] * (P - pws - (X1 ** 2) * P)) / (R * TDBK)
        F6 = (B[1] * X1 ** 3 * P ** 2) / (R * TDBK) ** 2
        F7 = (B[5] * 3 * X1 ** 2 * (1 - 2 * X1) * P ** 2) / \
                (2 * (R * TDBK) ** 2)
        F8 = -(B[6] * 3 * X1 ** 2 * (1 - X1) * P ** 2) / (R * TDBK) ** 2
        F9 = -(B[3] * ((1 + 2 * X1) * (1 - X1) ** 2 * P ** 2 - pws ** 2)) / \
                (2 * (R * TDBK) ** 2)
        F10 = -(B[0] * B[2] * X1 ** 2 * (1 - 3 * X1) * (1 - X1) * P ** 2) / \
                ((R * TDBK) ** 2)
        F11 = -(B[0] * B[4] * 2 * X1 ** 3 * (2 - 3 * X1) * P ** 2) / \
                ((R * TDBK) ** 2)
        F12 = (B[2] * B[4] * 6 * X1 ** 2 * (1 - X1) ** 2 * P ** 2) / \
                ((R * TDBK) ** 2)
        F13 = -(B[0] ** 2 * 3 * X1 ** 4 * P ** 2) / (2 * (R * TDBK) ** 2)
        F14 = -(B[4] ** 2 * X1 ** 2 * 2 * (1 - X1) * (1 - 3 * X1) * P ** 2) / \
                ((R * TDBK) ** 2)
        F15 = -(B[2] ** 2 * (pws ** 2 - (1 + 3 * X1) * (1 - X1) ** 3 * P **
                2)) / (2 * (R * TDBK) ** 2)
        F16 = F1 + F2 + F3 + F4 + F5 + F6 + F7 + F8 + F9 + F10 + F11 + F12 + \
                F13 + F14 + F15
        f = math.exp(F16)
        X1 = (P - f * pws) / P
        err = abs(f - F0)
        F0 = f
        j = j + 1

    ps = f * pws / 1000.0
    XAS = X1
    XWS = 1.0 - XAS
    if pws == P:
        WS = 1e10
    else:
        WS = MR * (ps / (PATM - ps))
    Ef = np.array([f, XAS, XWS, WS, pws / 1000.0])
    return Ef

#-------------------------------------------------------


"""
--------------------------------------------------------
9.  MSTAIR Cálculo del Volumen específico y Entalpía
    OUTPUT
    VA     Volumen específico           (m3/kg)
    HS     Entalpía                     (kJ/kgda)
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
    PATM   Presión Barométrica          (kPa)
    pws    Presión saturada de agua pura(kPa)
    XA, XW Fracciones molares de aire y agua
    W      Radio de Humedad             (gw/gda)
    B      Coeficientes viriales
"""


def MSTAIR(Tdb, PATM, pws, XA, XW, W, B):
    R = Rm * 1000000.0
    TDBK = Tdb + 273.15
    Bm = XA ** 2 * B[0] + 2 * XA * XW * B[4] + XW ** 2 * B[2]
    Cm = XA ** 3 * B[1] + 3 * XA ** 2 * XW * B[5] + 3 * XA * XW ** 2 * B[6] + \
        XW ** 3 * B[3]
    dBmdT = XA ** 2 * B[7] + 2 * XA * XW * B[11] + XW ** 2 * B[9]
    dCmdT = XA ** 3 * B[8] + 3 * XA ** 2 * XW * B[12] + \
        3 * XA * XW ** 2 * B[13] + XW ** 3 * B[10]

    # Volumen específico
    V9 = R * TDBK / (PATM * 1000)

    maxiter = 50
    err = 0.01
    j = 1
    while (err > 0.0000001) and (j <= maxiter):
        V = (R * TDBK / (PATM * 1000)) * (1 + Bm / V9 + Cm / V9 ** 2)
        err = abs((V - V9) / V)
        V9 = V
        j = j + 1

    if XA < 0.0000001:
        VS = V / 1000
    else:
        VS = V / (1000 * (Ma * XA))

    # Entalpía Específica
    h0 = 0.000002924425468
    Rlem = 8.31451          # Constante de gas específica-Lemmon (kJ/kmol.°K)
    #Md = 0.0104477          # Maxcondentherm densidad molar      (mol/cm3)
    Tj = 132.6312           # Maxcondentherm temperatura         (°K)
    Tred = 540.0            # Temperatura Reducida               (°K)
    Tc = 647.096
    R97 = 8.31451           # Constante de gas específica (kJ/kmol°K)
    R95 = 8.314371          # Constante de gas Universal-IAPWS-95(kJ/kmol.°K)

    # Formulación de Lemmon
    Ni0 = np.array([0.00000006057194, -0.0000210274769, -0.000158860716,
                    -13.841928076, 17.275266575, -0.00019536342, 2.490888032,
                    0.791309509, 0.212236768, -0.197938904, 25.36365, 16.90741,
                    87.31279])
    Tau = Tj / TDBK
    F1 = 0.0
    for i in range(5):
        F1 += (i - 3) * Ni0[i] * Tau ** (i - 4)
    dalfadTau = F1 + 1.5 * Ni0[5] * Tau ** 0.5 + Ni0[6] * Tau ** -1 + Ni0[7] \
                * Ni0[10] / (math.exp(Ni0[10] * Tau) - 1) + Ni0[8] * Ni0[11] \
                / ((math.exp(Ni0[11] * Tau)) - 1) + Ni0[9] * Ni0[12] / \
                (((2 / 3) * math.exp(-Ni0[12] * Tau)) + 1)
    h0lem = -7914.149298
    H1 = h0lem + Rlem * TDBK * (1 + Tau * dalfadTau)

    if TDBK >= 273.15:
        # IAPWS-97
        Ji0 = np.array([0.0, 1.0, -5.0, -4.0, -3.0, -2.0, -1.0, 2.0, 3.0])
        ni097 = np.array([-9.6927686500217, 10.086655968018,
                          -0.005608791128302, 0.071452738081455,
                          -0.40710498223928, 1.4240819171444, -4.383951131945,
                          -0.28408632460772, 0.021268463753307])
        Tau = Tred / TDBK
        #pi = PATM / 1000
        dgammadTau = 0.0
        for i in range(9):
            dgammadTau += ni097[i] * Ji0[i] * Tau ** (Ji0[i] - 1)
        h097 = -0.01102142797
        H2 = h097 + R97 * TDBK * Tau * dgammadTau
    else:
        # IAPWS-95
        ni095 = np.array([-8.3204464837497, 6.6832105275932, 3.00632, 0.012436,
                          0.97315, 1.2795, 0.96956, 0.24873])
        gammai0 = np.array([0.0, 0.0, 0.0, 1.28728967, 3.53734222, 7.74073708,
                            9.24437796, 27.5075105])
        Tau = Tc / TDBK
        F2 = 0.0
        for i in range(3, 8):
            F2 += ni095[i] * gammai0[i] * (math.exp(gammai0[i] * Tau) - 1) ** -1
        dalfa95dTau = ni095[1] + ni095[2] * Tau ** -1 + F2
        h095 = -0.01102303806
        H2 = h095 + R95 * TDBK * (1 + Tau * dalfa95dTau)

    HS = h0 + XA * H1 + XW * H2 + Rm * TDBK * ((Bm - TDBK * dBmdT) / V +
         (Cm - 0.5 * TDBK * dCmdT) / V ** 2)

    if XA > 0.0000001:
        HS = HS / (Ma * XA)

    if j == maxiter:
        print("MSTAIR - Máximo número de iteraciones alcanzada")

    MSTAIR = np.array([VS, HS])
    return MSTAIR

#-------------------------------------------------------


"""
--------------------------------------------------------
10. DEWPT Cálculo de la Temperatura de Rocío
    OUTPUT
    TDP           Temperatura de Rocío  (°C)
    INPUT
    W      Radio de Humedad             (gw/gda)
    PATM   Presión Barométrica          (kPa)
"""

#@ExecutionTimer
def DEWPT(W, PATM):
    CONV = 0.00001 * W
    if W < 0.001:
        CONV = 0.000001

    # Inicialmente estimo TDP con la formulación de Peppers
    if W == 0.0:
        TDPi = 0.0
        # print("TDP se ha fijado en 0.0 dado que W = 0.0")
    else:
        pw1 = PATM * W / (MR + W)
        A = np.log(pw1)
        TDPi = 6.54 + 14.526 * A + 0.7389 * A ** 2 + 0.09486 * A ** 3 + 0.4569 * pw1 ** 0.1984
        if TDPi < 0:
            TDPi = 6.09 + 12.608 * A + 0.4959 * A ** 2
    TDP = TDPi

    maxiter = 50
    err = 0
    j = 1
    while (err < 1) and (j <= maxiter):
        if TDP > 100.0 or TDP < -200.0:
            err = 1
        B = VIRCOE(TDP)
        # B = [Baa Caaa Bww Cwww Baw Caaw Caww
        #      dBaadT dCaaadT dBwwdT dCwwwdT dBawdT dCaawdT dCawwdT]
        Ef = ENHAC(TDP, PATM, B)
        # Ef = {f, XAS, XWS, WS, pws}
        WS = Ef[3]
        DELW = WS - W
        if abs(DELW) < CONV:
            break
        H = 0.01 * TDP + 0.0001
        TDPU = TDP + H
        TDPD = TDP - H

        B = VIRCOE(TDPU)
        Ef = ENHAC(TDPU, PATM, B)
        WSU = Ef[3]
        DELWU = WSU - W
        if abs(DELWU) < CONV:
            err = 2

        B = VIRCOE(TDPD)
        Ef = ENHAC(TDPD, PATM, B)
        WSD = Ef[3]
        DELWD = WSD - W
        if abs(DELWD) < CONV:
            err = 3

        DWDT = (WSU - WSD) / (2 * H)
        DELT = DELW / DWDT

        j = j + 1
        TDP = TDP - 0.5 * DELT

    if err == 1:
        TDP = TDPi
    elif err == 2:
        TDP = TDPU
    elif err == 3:
        TDP = TDPD

    if j == maxiter:
        TDP = TDPi
        print("DEWPT - Máximo número de iteraciones alcanzada")

    DEWPT = TDP
    return DEWPT

#-------------------------------------------------------


#@ExecutionTimer
def DEWPTb(W, PATM):
    CONV = 1E-4
    # Inicialmente estimo TDP con la formulación de Peppers
    if W == 0.0:
        TDPi = 0.0
        #print("TDP se ha fijado en 0.0 dado que W = 0.0")
        return TDPi
    else:
        pw1 = PATM * W / (MR + W)
        A = np.log(pw1)
        TDPi = 6.54 + 14.526 * A + 0.7389 * A ** 2 + 0.09486 * A ** 3 + 0.4569 * pw1 ** 0.1984
        if TDPi < 0:
            TDPi = 6.09 + 12.608 * A + 0.4959 * A ** 2


        def f(x, PATM):
            if x > 0.0:
                eqs = PWS_IAPWS97(x) / 1000.0 * ENHAC(x, PATM, VIRCOE(x))[0] - PATM * W / (MR + W)
            else:
                eqs = PWS_IAPWS98(x) / 1000.0 * ENHAC(x, PATM, VIRCOE(x))[0] - PATM * W / (MR + W)

            return eqs

        ini_guess = TDPi
        root = root_scalar(f, args=(PATM), method='secant', x0=ini_guess, bracket=None).root
        return root

"""
--------------------------------------------------------
11. HW Cálculo de la Entalpía específica del agua o hielo
    OUTPUT
    HW     Entalpía Específica          (kJ/kg)
    INPUT
    Tdb    temperatura de bulbo seco    (°C)
    PATM   Presión Barométrica          (kPa)
"""


def HW(Tdb, PATM):

    Taux = 1386.0             # (°K)
    paux = 16530.0            # (kPa)
    p0 = 101.325              # Presión normal               (kPa)
    pt = 0.611657             # Presión del punto triple     (kPa)
    Tt = 273.16               # Temperatura del punto triple (°K)
    R97 = 0.461526            # Constante de gas específica  (kJ/kg°K)

    TDBK = Tdb + 273.15

    dgammadTau = 0.0
    g0p = 0.0

    if TDBK >= 273.15:
        Tau = Taux / TDBK
        pi = PATM / paux
        for i in range(34):
            dgammadTau += ni[i] * (7.1 - pi) ** Ii[i] * Ji[i] * (Tau - 1.222) \
                            ** (Ji[i] - 1)
        HW = R97 * TDBK * Tau * dgammadTau
    else:
        tita = TDBK / Tt
        pi = PATM / pt
        pi0 = p0 / pt
        pt = pt * 1000.0
        for i in range(5):
            g0p += g0[i] * (pi - pi0) ** i
        r2p = r20 + r21 * (pi - pi0) + r22 * (pi - pi0) ** 2
        F1 = r1 * ((t1 - tita) * np.log(t1 - tita) + (t1 + tita) *
                np.log(t1 + tita) - 2 * t1 * np.log(t1) - tita ** 2 / t1)
        F2 = r2p * ((t2 - tita) * np.log(t2 - tita) + (t2 + tita) *
                np.log(t2 + tita) - 2 * t2 * np.log(t2) - tita ** 2 / t2)
        aux1 = F1 + F2
        g = g0p - s0 * Tt * tita + Tt * aux1.real
        r2p = r21 * (1 / pt) + r22 * (2 / pt) * (pi - pi0)
        F3 = r1 * (-np.log(t1 - tita) + np.log(t1 + tita) - 2 * tita / t1)
        F4 = r2p * (-np.log(t2 - tita) + np.log(t2 + tita) - 2 * tita / t2)
        aux2 = F3 + F4
        dgdT = -s0 + aux2.real
        HW = (g - TDBK * dgdT) / 1000.0

    return HW

#-------------------------------------------------------


"""
--------------------------------------------------------
12. WETTP Cálculo de la temperatura de Bulbo Húmedo
    OUTPUT
    TWB    Temperatura de Bulbo Húmedo  (°C)
    INPUT
    Tdb    Temperatura de bulbo seco    (°C)
    Tdp    Temperatura de Rocío         (°C)
    H      Entalpía                     (kJ/kgda)
    W      Radio de Humedad             (gw/gda)
    PATM   Presión Barométrica          (kPa)
"""


def WETTP(Tdb, Tdp, H, W, PATM):
    CONV = 0.0001 * abs(H)

    # Inicilamnete estimo TWB como el promedio de Tdb y Tdp
    TWB = (Tdb + Tdp) / 2

    err = 0
    j = 1
    maxiter = 50

    while (err < 1) and (j < maxiter):
        B = VIRCOE(TWB)
        # B = [Baa Caaa Bww Cwww Baw Caaw Caww
        # dBaadT dCaaadT dBwwdT dCwwwdT dBawdT dCaawdT dCawwdT]
        Ef = ENHAC(TWB, PATM, B)
        # Ef = {f, XAS, XWS, WS, pws}
        WS = Ef[3]
        aux = MSTAIR(TWB, PATM, Ef[4], Ef[1], Ef[2], WS, B)
        HS = aux[1]
        HWWB = HW(TWB, PATM)
        FUN = HS - (WS - W) * HWWB
        if H < FUN:
            II = 1
        else:
            II = 0
        DELH = FUN - H
        if abs(DELH) < CONV:
            break

        HP = 0.01 * TWB + 0.00001
        TWBU = TWB + HP
        TWBD = TWB - HP

        B = VIRCOE(TWBU)
        Ef = ENHAC(TWBU, PATM, B)
        WS = Ef[3]
        aux = MSTAIR(TWBU, PATM, Ef[4], Ef[1], Ef[2], WS, B)
        HS = aux[1]
        HWWB = HW(TWBU, PATM)
        FUNU = HS - (WS - W) * HWWB
        DELFU = FUNU - H
        if abs(DELFU) < CONV:
            err = 2

        B = VIRCOE(TWBD)
        Ef = ENHAC(TWBD, PATM, B)
        aux = MSTAIR(TWBD, PATM, Ef[4], Ef[1], Ef[2], WS, B)
        HS = aux[1]
        HWWB = HW(TWBD, PATM)
        FUND = HS - (WS - W) * HWWB
        DELFD = FUND - H
        if abs(DELFD) < CONV:
            err = 3

        DHDT = (FUNU - FUND) / (2 * HP)
        DELT = abs(DELH) / DHDT
        if II == 1:
            DELT = -DELT

        j = j + 1
        TWB = TWB + DELT

    if err == 2:
        TWB = TWBU
    elif err == 3:
        TWB = TWBD

    WETTP = TWB

    if j == maxiter:
        print("WETTP - Máximo número de iteraciones alcanzada")

    return WETTP

#-------------------------------------------------------


def WETTPb(Tdb, Tdp, H, W, PATM):
    CONV = 1E-7
    # Inicilamnete estimo TWB como el promedio de Tdb y Tdp
    TWB = (Tdb + Tdp) / 2


    def f(x, PATM, H):
        Ef = ENHAC(x, PATM, VIRCOE(x))
        # Ef = {f, XAS, XWS, WS, pws}
        WS = Ef[3]
        HS = MSTAIR(x, PATM, Ef[4], Ef[1], Ef[2], WS, VIRCOE(x))[1]
        #eqs = (H + (WS - W) * HW(x, PATM) - HS) / HS
        eqs = H - HS - (W - WS) * HW(x, PATM)
        return eqs


    ini_guess = TWB
    root = root_scalar(f, args=(PATM, H), method='secant', x0=ini_guess, xtol=CONV, bracket=None).root
    return root

"""
--------------------------------------------------------
13. WETTP2 Cálculo de la temperatura de Bulbo Húmedo
    OUTPUT
    TWB    Temperatura de Bulbo Húmedo  (°C)
    INPUT
    Tdb    Temperatura de bulbo seco    (°C)
    H      Entalpía                     (kJ/kgda)
    W      Radio de Humedad             (gw/gda)
    PATM   Presión Barométrica          (kPa)
"""


def WETTP2(Tdb, H, W, PATM):
    TWB = TWS_IAPWS97(PATM * 1000.0) - 273.15 - 1
    i = 0
    j = 0
    DELT = 10
    maxiter = 50
    maxiter2 = 10
    err2 = 0

    while (err2 < 1) and (j < maxiter2):
        err = 0
        while (err < 1) and (i < maxiter):
            B = VIRCOE(TWB)
            Ef = ENHAC(TWB, PATM, B)
            if TWB >= 0:
                PSAT = PWS_IAPWS97(TWB) / 1000.0
            else:
                PSAT = PWS_IAPWS98(TWB) / 1000.0
            WW = Ef[0] * PSAT
            if WW < PATM:
                err = 1
            else:
                TWB = TWB - DELT
            i = i + 1
        WS = MR * WW / (PATM - WW)
        HWWB = HW(TWB, PATM)
        aux = MSTAIR(TWB, PATM, Ef[4], Ef[1], Ef[2], WS, B)
        HS = aux[1]
        FUN = (H + (WS - W) * HWWB - HS) / HS
        if abs(FUN) < 0.000001:
            err2 = 1
            DELT = 0
        if FUN >= 0:
            j = j + 1
            TWB = TWB + DELT
            DELT = DELT / 10.0
            TWB = TWB - DELT
        else:
            TWB = TWB - DELT

    WETTP2 = TWB
    return WETTP2

#-------------------------------------------------------


def WETTP2b(Tdb, H, W, PATM):
    CONV = 1E-6
    # Estimo TWB
    #TWB = Tdb
    TWB = TWS_IAPWS97(PATM * 1000.0) - 273.15 - 1.0
    print(TWB)

    def f(x, PATM, H):
        Ef = ENHAC(x, PATM, VIRCOE(x))
        # Ef = {f, XAS, XWS, WS, pws}
        if TWB >= 0:
            PSAT = PWS_IAPWS97(x) / 1000.0
        else:
            PSAT = PWS_IAPWS98(x) / 1000.0
        WW = Ef[0] * PSAT
        WS = MR * WW / (PATM - WW)
        HWWB = HW(x, PATM)
        HS = MSTAIR(x, PATM, Ef[4], Ef[1], Ef[2], WS, VIRCOE(x))[1]
        eqs = (H + (WS - W) * HWWB - HS) / HS
        return eqs


    ini_guess = TWB
    root = root_scalar(f, args=(PATM, H), method='secant', x0=ini_guess, xtol=CONV, bracket=None).root
    return root

"""
--------------------------------------------------------
14. HFN2 Cálculo de las fracciones molares, el radio de humedad
    y el volumen específico dadas Tdb, PATM y H
    OUTPUT
    XA, XW fracciones molares
    W      Radio de Humedad             (gw/gda)
    V      Volumen específico           (m3(kg)
    INPUT
    Tdb    Temperatura de bulbo seco    (°C)
    H      Entalpía                     (kJ/kgda)
    PATM   Presión Barométrica          (kPa)
    XW     Estimación inicial de XW
"""


def HFN2(Tdb, PATM, H, XW):

    def iter_hfn(Tdb, PATM, pws, XA, XW, W, B):
        aux = MSTAIR(Tdb, PATM, pws, XA, XW, W, B)
        V = aux[0]
        H = aux[1]
        W = MR * XW / (1.0 - XW)
        ret_iter = np.array([W, V, H])
        return ret_iter

    if XW == 1:
        XW = 0.9

    XA = 1.0 - XW
    W = MR * XW / (1.0 - XW)
    if H == 0:
        CONV = 0.0001
    else:
        CONV = 0.001 * H
    B = VIRCOE(Tdb)
    P = PATM * 1000.0
    TDBK = Tdb + 273.15

    if TDBK >= 273.15:
        pws = PWS_IAPWS97(Tdb)
        if pws > P:
            pws = P
    else:
        pws = PWS_IAPWS98(Tdb)

    maxiter = 50
    j = 1
    while j < maxiter:
        FV = iter_hfn(Tdb, PATM, pws, XA, XW, W, B)
        W0 = FV[0]
        V0 = FV[1]
        H0 = FV[2]
        DELH = H0 - H
        if abs(DELH) <= abs(CONV):
            HFN2 = np.array([XW, XA, W0, V0])
            return HFN2
            break

        D = 0.001 * XW
        XWU = XW + D
        XWD = XW - D
        XAU = 1.0 - XWU
        XAD = 1.0 - XWD
        WU = MR * XWU / (1.0 - XWU)
        WD = MR * XWD / (1.0 - XWD)

        FVU = iter_hfn(Tdb, PATM, pws, XAU, XWU, WU, B)
        WU = FVU[0]
        VU = FVU[1]
        HU = FVU[2]
        DELHU = HU - H
        if abs(DELHU) <= abs(CONV):
            HFN2 = np.array([XWU, XAU, WU, VU])
            return HFN2
            break
        FVD = iter_hfn(Tdb, PATM, pws, XAD, XWD, WD, B)
        WD = FVD[0]
        VD = FVD[1]
        HD = FVD[2]
        DELHD = FVD[2] - H
        if abs(DELHD) <= abs(CONV):
            HFN2 = np.array([XWD, XAD, WD, VD])
            return HFN2
            break

        j = j + 1
        DHDX = (HU - HD) / (2.0 * D)
        DELX = DELH / DHDX
        XW = XW - DELX
        XA = 1 - XW

    if j == maxiter:
        print("HFN2 - Máximo número de iteraciones alcanzada")

#-------------------------------------------------------


"""
--------------------------------------------------------
15. VFNITR Cálculo de las fracciones molares, el radio de humedad
    y la entalpía dadas Tdb, PATM y V
    OUTPUT
    XA, XW fracciones molares
    W      Radio de Humedad             (gw/gda)
    H      Entalpía                     (kJ/kgda)
    INPUT
    Tdb    Temperatura de bulbo seco    (°C)
    V      Volumen específico           (m3/kg)
    PATM   Presión Barométrica          (kPa)
    XW     Estimación inicial de XW
"""


def VFNITR(Tdb, PATM, V, XW):

    def iter_vfun(XA, XW, W, Tdb, pws, PATM, B):
        aux = MSTAIR(Tdb, PATM, pws, XA, XW, W, B)
        V = aux[0]
        H = aux[1]
        W = MR * XW / (1.0 - XW)
        ret_iter = np.array([W, V, H])
        return ret_iter

    if XW == 1:
        XW = 0.9

    XA = 1.0 - XW
    W = MR * XW / (1.0 - XW)
    CONV = 0.00001 * V
    P = PATM * 1000.0
    TDBK = Tdb + 273.15
    B = VIRCOE(Tdb)

    if TDBK >= 273.15:
        pws = PWS_IAPWS97(Tdb)
        if pws > P:
            pws = P
    else:
        pws = PWS_IAPWS98(Tdb)

    maxiter = 50
    j = 1

    while j < maxiter:
        FV = iter_vfun(XA, XW, W, Tdb, pws, PATM, B)
        DELV = FV[1] - V
        W0 = FV[0]
        H0 = FV[2]
        if abs(DELV) < CONV:
            VFNITR = np.array([XW, XA, W0, H0])
            return VFNITR
            break

        D = 0.001 * XW
        XWU = XW + D
        XWD = XW - D
        XAU = 1.0 - XWU
        XAD = 1.0 - XWD
        WU = MR * XWU / (1.0 - XWU)
        WD = MR * XWD / (1.0 - XWD)

        FVU = iter_vfun(XAU, XWU, W, Tdb, pws, PATM, B)
        DELVU = FVU[1] - V
        WU = FVU[0]
        VU = FVU[1]
        HU = FVU[2]
        if abs(DELVU) < CONV:
            VFNITR = np.array([XWU, XAU, WU, HU])
            return VFNITR
            break
        FVD = iter_vfun(XAD, XWD, W, Tdb, pws, PATM, B)
        DELVD = FVD[1] - V
        WD = FVD[0]
        VD = FVD[1]
        HD = FVD[2]
        if abs(DELVD) < CONV:
            VFNITR = np.array([XWD, XAD, WD, HD])
            return VFNITR
            break
        j = j + 1
        DVDX = (VU - VD) / (2.0 * D)
        DELX = DELV / DVDX
        XW = XW - DELX
        XA = 1.0 - XW

    if j == maxiter:
        print("VFNITR - Máximo número de iteraciones alcanzada")

#-------------------------------------------------------


"""
--------------------------------------------------------
16. HFUNIT Cálculo de las fracciones molares, el radio de humedad
    dadas Tdb, PATM, XW, HWWB y FUN
    OUTPUT
    XA, XW fracciones molares
    W      Radio de Humedad             (gw/gda)
    INPUT
    Tdb    Temperatura de bulbo seco    (°C)
    PATM   Presión Barométrica          (kPa)
    XW     Estomación inicial de XW
    HW     Entalpía Específica del agua (kJ/kg)
    FUN    Valor nuimérico de of H-W*H  (kJ/kg)
"""


def HFUNIT(Tdb, PATM, FUN, HW, XW):

    def iter_hfun(XA, XW, Tdb, pws, PATM, HW):
        B = VIRCOE(Tdb)
        W = MR * XW / (1.0 - XW)
        aux = MSTAIR(Tdb, PATM, pws, XA, XW, W, B)
        V = aux[0]
        H = aux[1]
        FC = H - W * HW
        ret_iter = np.array([W, V, H, FC])
        return ret_iter

    if XW == 1:
        XW = 0.99

    XA = 1.0 - XW
    CONV = abs(0.0001 * FUN)
    P = PATM * 1000.0
    TDBK = Tdb + 273.15

    if TDBK >= 273.15:
        pws = PWS_IAPWS97(Tdb)
        if pws > P:
            pws = P
    else:
        pws = PWS_IAPWS98(Tdb)

    maxiter = 50
    j = 1

    while j < maxiter:
        FC = iter_hfun(XA, XW, Tdb, pws, PATM, HW)
        DELF = FC[3] - FUN
        if abs(DELF) < CONV:
            W = FC[0]
            V = FC[1]
            H = FC[2]
            HFUNIT = np.array([XW, XA, W, H, V])
            return HFUNIT
            break
        D = 0.1 * XW
        XWU = XW + D
        XAU = 1.0 - XWU
        FU = iter_hfun(XAU, XWU, Tdb, pws, PATM, HW)
        DELFU = FU[3] - FUN
        if abs(DELFU) < CONV:
            W = FU[0]
            V = FU[1]
            H = FU[2]
            HFUNIT = np.array([XWU, XAU, W, H, V])
            return HFUNIT
            break
        XWD = XW - D
        XAD = 1.0 - XWD
        FD = iter_hfun(XAD, XWD, Tdb, pws, PATM, HW)
        DELFD = FD[3] - FUN
        if abs(DELFD) < CONV:
            W = FD[0]
            V = FD[1]
            H = FD[2]
            HFUNIT = np.array([XWD, XAD, W, H, V])
            return HFUNIT
            break

        j = j + 1
        DFDW = (FU[3] - FD[3]) / (2.0 * D)
        DELW = DELF / DFDW
        XW = XW - DELW
        XA = 1 - XW

    if j == maxiter:
        print("HFUNIT - Máximo número de iteraciones alcanzada")

#-------------------------------------------------------


"""
--------------------------------------------------------
17. TDBIT Cálculo de Tdb dados W y h
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    W      Radio de Humedad             (gw/gda)
    H      Entalpía Específica del aire (kJ/kg)
    PATM   Presión Barométrica          (kPa)
"""


def TDBITb(W, H, PATM):
    # Estimo una Tdb
    Tdb = H - 2501.0 * W / (1.006 + 1.86 * W)
    CONV = 1E-4


    def f(x, PATM, W, H):
        XW = W / (W + MR)
        XA = 1.0 - XW
        eqs = H - MSTAIR(x, PATM, ENHAC(x, PATM, VIRCOE(x))[4], XA, XW, W, VIRCOE(x))[1]
        return eqs


    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, W, H), method='secant', x0=ini_guess, bracket=None).root
    return root


"""
--------------------------------------------------------
18. TDB2IT Cálculo de Tdb dados RH y h
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    RH     Humedad Relativa             (%)
    H      Entalpía Específica del aire (kJ/kg)
    PATM   Presión Barométrica          (kPa)
"""


def TDB2ITb(RH, H, PATM):
    # Estimo una Tdb
    Tdb = 20.0
    CONV = 1E-6

    def f(x, PATM, RH, H):
        XW = ENHAC(x, PATM, VIRCOE(x))[2] * RH / 100.0
        XA = 1.0 - XW
        W = MR * XW / XA
        eqs = H - MSTAIR(x, PATM, ENHAC(Tdb, PATM, VIRCOE(x))[4], XA, XW, W, VIRCOE(x))[1]
        return eqs

    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, RH, H), method='secant', x0=ini_guess, bracket=None).root
    return root


"""
--------------------------------------------------------
19. TDB3IT Cálculo de Tdb dados W y V
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    W      Radio de Humedad             (gw/gda)
    V      Volumen específico           (m3/kg)
    PATM   Presión Barométrica          (kPa)
"""


def TDB3ITb(W, V, PATM):
    # Estimo una Tdb
    Tdb = PATM * 1000.0 * V / (287.055 * (1 + 1.608 * W)) - 273.15
    CONV = 1E-6

    #B = [Baa Caaa Bww Cwww Baw Caaw Caww, dBaadT, dCaaadT, dBwwdT, dCwwwdT, dBawdT, dCaawdT, dCawwdT]
    XW = W / (MR + W)
    M = (1 - XW) * Ma + XW * Mw
    Vm = 1E6 * V * M / (1 + W)


    def f(x, PATM, W, V):
        eqs = PATM - 1E6 * Rm * (x + 273.15) / Vm * (1 + VIRCOE(x)[2] / Vm + VIRCOE(x)[3] / Vm ** 2)
        return eqs


    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, W, V), method='secant', x0=ini_guess, bracket=None).root
    return root



"""
--------------------------------------------------------
20. TDB4IT Cálculo de Tdb dados RH y V
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    RH     Humedad Relativa             (%a)
    V      Volumen específico           (m3/kg)
    PATM   Presión Barométrica          (kPa)
"""


def TDB4ITb(RH, V, PATM):
    # Estimo una Tdb
    #Tdb = MR * RH * pws / 100.0 / (PATM - RH * pws / 100.0)
    Tdb = 20.0
    CONV = 1E-4
    # Estimo XW
    XW = ENHAC(Tdb, PATM, VIRCOE(Tdb))[2]


    def f(x, PATM, RH, V, XW):
        XW = ENHAC(x, PATM, VIRCOE(x))[2] * RH / 100.0
        XA = 1.0 - XW
        if XA == 0:
            XA = 1e-05
        W = MR * XW / XA
        eqs = V - MSTAIR(x, PATM, ENHAC(x, PATM, VIRCOE(x))[4], XA, XW, W, VIRCOE(x))[0]
        return eqs


    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, RH, V, XW), method='secant', x0=ini_guess, bracket=None).root
    return root


"""
--------------------------------------------------------
21. TDB5IT Cálculo de Tdb dados W y Twb
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    W      Radio de Humedad             (gw/gda)
    Twb    Temperatura de bulbo húmedo  (°C)
    PATM   Presión Barométrica          (kPa)
"""


def TDB5ITb(W, Twb, PATM):
    # Estimo una Tdb
    Tdb = Twb
    CONV = 1E-6


    def f(x, PATM, W, Twb):
        Ef = ENHAC(x, PATM, VIRCOE(x))
        XW = W / (W + MR)
        XA = 1.0 - XW
        if XA == 0.0:
            XA = 1e-05
        h = MSTAIR(x, PATM, Ef[4], XA, XW, W, VIRCOE(x))[1]
        Tdp = DEWPTb(W, PATM)
        eqs = Twb - WETTPb(x, Tdp, h, W, PATM)
        return eqs


    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, W, Twb), method='secant', x0=ini_guess, xtol=CONV, bracket=None).root
    return root


"""
--------------------------------------------------------
22. TDB6IT Cálculo de Tdb dados RH y Twb
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    RH     Humedad Relativa             (%)
    Twb    Temperatura de bulbo húmedo  (°C)
    PATM   Presión Barométrica          (kPa)
"""


def TDB6ITb(RH, Twb, PATM):
    # Estimo una Tdb
    Tdb = Twb
    CONV = 1E-6


    def f(x, PATM, RH, Twb):
        Ef = ENHAC(x, PATM, VIRCOE(x))
        XW = Ef[2] * RH / 100.0
        XA = 1.0 - XW
        if XA == 0:
            XA = 1e-05
        W = MR * XW / XA
        h = MSTAIR(x, PATM, Ef[4], XA, XW, W, VIRCOE(x))[1]
        Tdp = DEWPTb(W, PATM)
        eqs = Twb - WETTPb(x, Tdp, h, W, PATM)
        return eqs


    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, RH, Twb), method='secant', x0=ini_guess, xtol=CONV, bracket=None).root
    return root


"""
--------------------------------------------------------
23. TDB7IT Cálculo de Tdb dados W y RH
    OUTPUT
    Tdb    Temperatura de bulbo seco    (°C)
    INPUT
    W      Radio de Humedad             (gw/gda)
    RH     Humedad Relativa             (%)
    Twb    Temperatura de bulbo húmedo  (°C)
    PATM   Presión Barométrica          (kPa)
"""

#@ExecutionTimer
def TDB7ITb(W, RH, PATM):
    CONV = 1E-4
    # Estimo una Tdb
    pws = 1000.0 * W * PATM / ((RH / 100.0) * (MR + W))
    Tdb = TWS_IAPWS97(pws) - 273.15


    def f(x, PATM, W, RH):
        if x > 0.0:
            eqs = PWS_IAPWS97(x) / 1000.0 * ENHAC(x, PATM, VIRCOE(x))[0] - W * PATM / ((RH / 100.0) * (MR + W))
        else:
            eqs = PWS_IAPWS98(x) / 1000.0 * ENHAC(x, PATM, VIRCOE(x))[0] - W * PATM / ((RH / 100.0) * (MR + W))
        return eqs


    ini_guess = Tdb
    root = root_scalar(f, args=(PATM, W, RH), method='secant', x0=ini_guess, bracket=None).root
    return root


if __name__ == '__main__':

    #print(patm_ICAO(10120))
    #print(PWS_IAPWS98(0.0))
    #print(TWS_IAPWS97(100000.0) - 273.15)
    #print(PWS_IAPWS98(-30))
    #print(VIRCOE(-15))
    #print(ISOTCOMP(0, 101.325))
    #print(ISOTCOMP(120, 200))
    #print(HENRYLAW(0, 101.325))
    #print(HENRYLAW(80, 1000))
    #aux = ENHAC(350, 500, VIRCOE(350))
    #print(aux[0])
    #print(aux[1] + aux[2])
    #print(HW(-0.0, 101.325))
    #print(DEWPT(105 / 1000, 101.325))
    #print(WETTP(200, DEWPT(1.0 / 1000, 101.325), 3442.54, 1.0, 101.325))
    #print(WETTP(320, DEWPT(1.0 / 1000, 1000), 3429.10, 1.0, 1000))
    #print(TDB2IT(100.0, 81.579, 93.14863))
    #print(TDBIT(0.0 / 1000, 0.0, 101.325))
    #print(TDB3IT(50 / 1000, 1.1, 101.325))
    #print(TDB4IT(100, 1.11, 101.325))
    #print(TDB5IT(4.0/1000.0, 23.2, 101.325))
    print(TDB7ITb(14.2/1000.0, 40.0, 101.325))