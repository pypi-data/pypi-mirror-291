import psychrograph.psychro_aux as psy

"""
--------------------------------------------------------
1.  check Verify the diagram limits
    OUTPUT
    limits - corrected and extended with LCS if it's necessary
    INPUT
    limits - dictionary with the limits fixed by the user
             = {"LIT": xx, "LST": xx, "LIW": xx, "LSW": xx}
    patm   - Barometric Pressure          (kPa)
"""


def check_lim(limits, patm):
    # limits = [LIT, LST, LIW, LSW]
    # Calculate the dew point og LSW
    dplsw = psy.DEWPT(limits[3] / 1000.0, patm)

    # if LIW > 0
    if limits[2] > 0:
        # Calculate the pws of LIW
        pws = (limits[2] / 1000) * (patm * 1000) / (limits[2] / 1000 + psy.MR)
        # Calculate the saturation temperature of LIW
        aux_lit = psy.TWS_IAPWS97(pws) - 273.15
        # if aux_LIT > LIT make a correction
        if aux_lit > limits[0]:
            limits[0] = psy.TWS_IAPWS97(pws) - 273.15

    # Verify if LST >= dplsw
    if limits[1] >= dplsw:
        limits[4] = dplsw
    # if not, redefine the diagram limit
    else:
        limits[4] = limits[1]
        b = psy.VIRCOE(limits[4])
        ef = psy.ENHAC(limits[4], patm, b)
        xw = ef[2]
        xa = 1.0 - xw
        if xa == 0:
            xa = 1e-5
        w = psy.MR * xw / xa
        limits[3] = w * 1000.0

    # print(limits)
    return limits

# -------------------------------------------------------
