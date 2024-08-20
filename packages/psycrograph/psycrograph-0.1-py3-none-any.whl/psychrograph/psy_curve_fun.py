"""
Curve drawing functions

--------------------------------------------------------
Written by                                José E. Azzaro
--------------------------------------------------------

Functions included in this module

1.  f_dib_sat       Drawing function for saturation curve
2.  f_dib_Tdb       Drawing function for Tdb lines
3.  f_dib_W         Drawing function for W lines
4.  f_dib_RH        Drawing function for RH curves
5.  f_dib_v         Drawing function for v curves
6.  f_dib_h         Drawing function for h lines
7.  f_dib_Twb       Drawing function for Twb lines
8.  f_transform     Calculation of texts angles

"""

import math
import psychrograph.psychro_aux as psy
import psychrograph.psychro_aux_diag as psy_d
# from psychrograph.timing import ExecutionTimer
import numpy as np


# @ExecutionTimer
# Function to draw the saturation curve
def f_dib_sat(limits_ext, color_fill, style, patm, ax):
    dp = 1.0
    x_sat = np.arange(limits_ext[0], limits_ext[4], dp, dtype=float)
    x_sat = np.append(x_sat, limits_ext[4])
    y_sat = []
    if x_sat.size > 0:
        y_sat = psy_d.Cur_Sat(x_sat, 100.0, patm, limits_ext, 0)
        ax.plot(x_sat, y_sat, **style)
        x_sat = np.append(x_sat, limits_ext[1])
        y_sat = np.append(y_sat, limits_ext[3])
    ax.fill_between(x_sat, y_sat, color=color_fill)


# Function to draw the Tdb lines
# @ExecutionTimer
def f_dib_tdb(limits_ext, linea_step, style, patm, ax):
    x_tdb = np.arange(limits_ext[0] + linea_step, limits_ext[1], linea_step, dtype=float)
    y_tdb = psy_d.Cur_Sat(x_tdb, 100.0, patm, limits_ext, 0)
    y_tdb = np.where(y_tdb > limits_ext[3], limits_ext[3], y_tdb)
    for x, y in np.nditer([x_tdb, y_tdb]):
        ax.plot([x, x], [limits_ext[2], y], **style, zorder=1)


# Function to draw the W lines
# @ExecutionTimer
def f_dib_w(limits_ext, linea_step, style, patm, ax):
    y_w = np.arange(limits_ext[2] + linea_step, limits_ext[3], linea_step, dtype=float)
    x_w = psy_d.Cur_W(y_w, patm)
    x_w = np.where(x_w < limits_ext[0], limits_ext[0], x_w)
    for x, y in np.nditer([x_w, y_w]):
        ax.plot([x, limits_ext[1]], [y, y], **style, zorder=1)


# Function to draw the RH lines
# @ExecutionTimer
def f_dib_rh(limits_ext, linea_step, text_step, style, patm, ax, figsize, text_prop):
    rh = np.arange(0.0 + linea_step, 100.0, linea_step, dtype=float)
    aux_rh = rh % text_step  # Máscara para extraer valores dónde quiero texto
    ind_aux = rh[aux_rh == 0]
    lcs_rh = psy_d.Cur_Sat(limits_ext[1], rh, patm, limits_ext, 1)
    # Avoid values > 100°C
    lcs_rh = np.where(lcs_rh > 100.0, 100.0, lcs_rh)
    lcs_aux = lcs_rh[aux_rh == 0]

    for ind_RH, ind_LCS in np.nditer([rh, lcs_rh]):
        x_rh = np.arange(limits_ext[0], ind_LCS, 2.0, dtype=float)
        x_rh = np.append(x_rh, ind_LCS)
        if len(x_rh):
            y_rh = psy_d.Cur_Sat(x_rh, ind_RH, patm, limits_ext, 0)
            ax.plot(x_rh, y_rh, **style)

    # Curve text
    fig_x, fig_y = figsize
    dx = 50.0
    x_min, x_max = limits_ext[0], limits_ext[1]
    y_min, y_max = limits_ext[2], limits_ext[3]
    if text_step:
        for ind_aux, lcs_aux in np.nditer([ind_aux, lcs_aux]):
            if limits_ext[1] > limits_ext[4] > limits_ext[0]:
                x_rh_text = limits_ext[4]
            else:
                x_rh_text = (limits_ext[0] + lcs_aux) / 2.0
            y_rh_text = psy_d.Calc_T_RH(x_rh_text, ind_aux, patm)
            if y_rh_text < limits_ext[3] - 0.1:
                dy = psy_d.Calc_T_RH(x_rh_text + dx / 2, ind_aux, patm) - psy_d.Calc_T_RH(x_rh_text - dx / 2, ind_aux,
                                                                                          patm)
                ddx = dx * fig_x / (x_max - x_min)
                ddy = dy * fig_y / (y_max - y_min)
                ang = (180.0 / np.pi) * np.arctan(ddy / ddx)
                ax.text(x_rh_text, y_rh_text, str(ind_aux) + "%", **text_prop, rotation=ang)


# Function to draw the v lines
# @ExecutionTimer
def f_dib_v(limits_ext, linea_step, text_step, style, patm, ax, figsize, text_prop, text_v):
    # v limits
    aux1 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[2], patm, 1)[0]
    aux2 = psy_d.Calc_T_HUM(limits_ext[0], 100, patm, 0)[0]
    aux3 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[2], patm, 1)[0]
    aux4 = psy_d.Calc_T_HUM(limits_ext[4], 100.0, patm, 0)[0]
    aux5 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[3], patm, 1)[0]
    # text auxiliar
    aux_textv_x = []
    aux_textv_y = []
    aux_textv_p = []
    # Move the init value of the text
    add = 0

    # Draw the v curves
    v_lim = [aux1, aux2, aux3, aux4, aux5]
    if v_lim[3] < v_lim[2]:
        v_lim[3], v_lim[2] = v_lim[2], v_lim[3]
    if v_lim[1] > v_lim[2]:
        del v_lim[1]
        aux6 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[3], patm, 1)
        v_lim[1] = aux6[0]
    v_aux = np.arange(round(v_lim[0], 2), v_lim[-1], linea_step, dtype=float)
    fig_x, fig_y = figsize

    for v in np.nditer([v_aux]):
        if v < v_lim[0]:
            add += 1
            continue
        if v < v_lim[1]:
            x1 = limits_ext[0]
            y1 = psy_d.Calc_T_v(x1, v, patm)
            x2 = psy.TDB3ITb(limits_ext[2] / 1000.0, v, patm)
            y2 = limits_ext[2]
        elif v < v_lim[3]:
            x1 = psy.TDB4ITb(100.0, v, patm)
            y1 = psy_d.Calc_T_v(x1, v, patm)
            if y1 > limits_ext[3]:
                x1 = psy.TDB3ITb(limits_ext[3] / 1000.0, v, patm)
                y1 = limits_ext[3]
            x2 = psy.TDB3ITb(limits_ext[2] / 1000.0, v, patm)
            y2 = limits_ext[2]
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_v(x2, v, patm)
        else:
            x1 = psy.TDB3ITb(limits_ext[3] / 1000.0, v, patm)
            y1 = limits_ext[3]
            x2 = limits_ext[1]
            y2 = psy_d.Calc_T_v(limits_ext[1], v, patm)
        ax.plot([x1, x2], [y1, y2], **style)

        aux_textv_x.append(x2)
        aux_textv_y.append(y2)
        aux_textv_p.append(
            f_transform(x1, y1, x2, y2, fig_x, fig_y, limits_ext[0], limits_ext[1], limits_ext[2], limits_ext[3]))

    # Curve text
    ind_aux = np.arange(round(v_aux[0 + add], 2), v_aux[-1], text_step, dtype=float)
    x_aux = aux_textv_x[::int(text_step / linea_step)]
    y_scale = limits_ext[3] - limits_ext[2]
    y_aux = aux_textv_y[::int(text_step / linea_step)]
    p_aux = aux_textv_p[::int(text_step / linea_step)]
    middle_index = len(x_aux) // 2
    for x_entry, y_entry, ang, ind in zip(x_aux, y_aux, p_aux, ind_aux):
        if x_entry < limits_ext[1]:
            ax.text(x_entry - 0.06 * y_scale, y_entry + 0.02 * y_scale, r'{:.2f}'.format(float(ind)),
                    text_prop, rotation=ang)
        else:
            ax.text(x_entry - 0.05 * y_scale, y_entry, r'{:.2f}'.format(float(ind)), text_prop, rotation=ang)

    if text_v:
        ax.text(x_aux[middle_index] - y_scale * 0.3, y_aux[middle_index] + y_scale * 0.1,
                text_v,
                text_prop, rotation=p_aux[middle_index], picker=True, gid=id)


# Function to for the h curves
# @ExecutionTimer
def f_dib_h(limits_ext, linea_step, text_step, style, patm, ax, figsize, text_prop, text_h):
    # h curve limits
    aux1 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[2], patm, 1)[1]
    aux2 = psy_d.Calc_T_HUM(limits_ext[0], 100, patm, 0)[1]
    aux3 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[2], patm, 1)[1]
    aux4 = psy_d.Calc_T_HUM(limits_ext[4], 100.0, patm, 0)[1]
    aux5 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[3], patm, 1)[1]
    h_lim = [aux1, aux2, aux3, aux4, aux5]
    if h_lim[3] < h_lim[2]:
        h_lim[3], h_lim[2] = h_lim[2], h_lim[3]
    if h_lim[1] > h_lim[2]:
        del h_lim[1]
        aux6 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[3], patm, 1)
        h_lim[1] = aux6[1]
    h_aux = np.arange(math.ceil(h_lim[0]), h_lim[-1], linea_step, dtype=float)
    fig_x, fig_y = figsize
    # text auxiliar
    aux_texth_x = []
    aux_texth_y = []
    aux_texth_p = []

    # Draw the h lines
    for h in np.nditer([h_aux]):
        if h < h_lim[1]:
            x1 = limits_ext[0]
            y1 = psy_d.Calc_T_h(x1, h, patm)
            x2 = psy.TDBITb(limits_ext[2] / 1000.0, h, patm)
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_h(x2, h, patm)
            else:
                y2 = limits_ext[2]
        elif h < h_lim[3]:
            x1 = psy.TDB2ITb(100.0, h, patm)
            y1 = psy_d.Calc_T_h(x1, h, patm)
            if y1 > limits_ext[3]:
                x1 = psy.TDBITb(limits_ext[3] / 1000.0, h, patm)
                y1 = limits_ext[3]
            x2 = psy.TDB2ITb(limits_ext[2] / 1000.0, h, patm)
            y2 = limits_ext[2]
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_h(x2, h, patm)
        else:
            x1 = psy.TDBITb(limits_ext[3] / 1000.0, h, patm)
            y1 = limits_ext[3]
            x2 = limits_ext[1]
            y2 = psy_d.Calc_T_h(limits_ext[1], h, patm)

        ax.plot([x1, x2], [y1, y2], **style)
        aux_texth_x.append(x1)
        aux_texth_y.append(y1)
        aux_texth_p.append(
            f_transform(x1, y1, x2, y2, fig_x, fig_y, limits_ext[0], limits_ext[1], limits_ext[2], limits_ext[3]))

    # Lines text
    ind_aux = np.arange(round(h_lim[0], 1), h_lim[-1], text_step, dtype=float)
    x_aux = aux_texth_x[::int(text_step / linea_step)]
    y_scale = limits_ext[3] - limits_ext[2]
    y_aux = aux_texth_y[::int(text_step / linea_step)]
    p_aux = aux_texth_p[::int(text_step / linea_step)]
    middle_index = len(x_aux) // 2
    for x_entry, y_entry, ang, ind in zip(x_aux, y_aux, p_aux, ind_aux):
        ax.text(x_entry - 0.05 * y_scale, y_entry + 0.01 * y_scale, r'{:.1f}'.format(float(ind)), text_prop,
                rotation=ang)

    if text_h:
        ax.text(x_aux[middle_index] + 0.6 * y_scale, y_aux[middle_index] - 0.09 * y_scale,
                text_h,
                text_prop, rotation=p_aux[middle_index], picker=True, gid=id)


# Function to for the Twb curves
# @ExecutionTimer
def f_dib_twb(limits_ext, linea_step, text_step, style, patm, ax, figsize, text_prop, text_twb):
    # Twb curve limits
    aux1 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[2], patm, 1)[1]
    aux2 = psy_d.Calc_T_HUM(limits_ext[0], 100, patm, 0)[1]
    aux3 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[2], patm, 1)[1]
    aux4 = psy_d.Calc_T_HUM(limits_ext[4], 100.0, patm, 0)[1]
    aux5 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[3], patm, 1)[1]

    twb_aux1 = psy_d.Calc_T_h_HUM(limits_ext[0], aux1, limits_ext[2], patm, 1)
    twb_aux2 = psy_d.Calc_T_h_HUM(limits_ext[0], aux2, 100.0, patm, 0)
    twb_aux3 = psy_d.Calc_T_h_HUM(limits_ext[1], aux3, limits_ext[2], patm, 1)
    twb_aux4 = psy_d.Calc_T_h_HUM(limits_ext[4], aux4, 100.0, patm, 0)
    twb_aux5 = psy_d.Calc_T_h_HUM(limits_ext[1], aux5, limits_ext[3], patm, 1)
    twb_lim = [twb_aux1, twb_aux2, twb_aux3, twb_aux4, twb_aux5]
    if twb_lim[3] < twb_lim[2]:
        twb_lim[3], twb_lim[2] = twb_lim[2], twb_lim[3]
    if twb_lim[1] > twb_lim[2]:
        del twb_lim[1]
        aux6 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[3], patm, 1)
        twb_lim[1] = psy_d.Calc_T_h_HUM(limits_ext[0], aux6[1], limits_ext[3], patm, 1)
    fig_x, fig_y = figsize
    twb_lim_d = twb_lim[-1]
    twb_lim_i = twb_lim[0]
    if (limits_ext[3] - twb_lim[-1]) < 0.5:
        twb_lim_d = twb_lim[-1] - 0.5
    if (twb_lim[0] - limits_ext[0]) < 0.5:
        twb_lim_i = twb_lim[0] + 0.5
    twb_aux = np.arange(math.ceil(twb_lim_i), twb_lim_d, linea_step, dtype=float)
    # Text auxiliar
    aux_textt_x = []
    aux_textt_y = []
    aux_textt_p = []
    for twb in np.nditer([twb_aux]):
        # At high temperatures LCS < LIT
        if twb < twb_lim[1]:
            x1 = limits_ext[0]
            y1 = psy_d.Calc_T_Twb(x1, twb, patm)
            x2 = psy.TDB5ITb(limits_ext[2] / 1000.0, twb, patm)
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_Twb(x2, twb, patm)
            else:
                y2 = limits_ext[2]
        elif twb < twb_lim[3]:
            x1 = psy.TDB6ITb(100.0, twb, patm)
            y1 = psy_d.Calc_T_Twb(x1, twb, patm)
            if y1 > limits_ext[3]:
                x1 = psy.TDB5ITb(limits_ext[3] / 1000.0, twb, patm)
                y1 = limits_ext[3]
            x2 = psy.TDB5ITb(limits_ext[2] / 1000.0, twb, patm)
            y2 = limits_ext[2]
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_Twb(x2, twb, patm)
        else:
            x1 = psy.TDB5ITb(limits_ext[3] / 1000.0, twb, patm)
            y1 = limits_ext[3]
            x2 = limits_ext[1]
            y2 = psy_d.Calc_T_Twb(x2, twb, patm)

        ax.plot([x1, x2], [y1, y2], **style)
        aux_textt_x.append((x1 + x2) / 2)
        aux_textt_y.append((y1 + y2) / 2)
        aux_textt_p.append(
            f_transform(x1, y1, x2, y2, fig_x, fig_y, limits_ext[0], limits_ext[1], limits_ext[2], limits_ext[3]))

    # Lines text
    ind_aux = np.arange(round(twb_aux[0], 1), twb_aux[-1], text_step, dtype=float)
    x_aux = aux_textt_x[::int(text_step / linea_step)]
    y_scale = limits_ext[3] - limits_ext[2]
    y_aux = aux_textt_y[::int(text_step / linea_step)]
    p_aux = aux_textt_p[::int(text_step / linea_step)]
    middle_index = len(x_aux) // 2
    for x_entry, y_entry, ang, ind in zip(x_aux, y_aux, p_aux, ind_aux):
        ax.text(x_entry, y_entry, r'{:.1f}'.format(float(ind)) + " °C", text_prop, rotation=ang)

    ax.text(x_aux[middle_index] + 0.45 * y_scale, y_aux[middle_index] + 0.4 * y_scale,
            text_twb,
            text_prop, rotation=p_aux[middle_index], picker=True, gid=id)


# Angles of the texts calculation
def f_transform(x1, y1, x2, y2, fig_x, fig_y, x_min, x_max, y_min, y_max):
    dx = x2 - x1
    dy = y2 - y1
    ddx = dx * fig_x / (x_max - x_min)
    ddy = dy * fig_y / (y_max - y_min)
    ang = (180.0 / np.pi) * np.arctan(ddy / ddx)
    return ang
