import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)
import psychrograph.psy_verify_lim as psy_f
import psychrograph.psychro_aux as psy
import psychrograph.psychro_aux_diag as psy_d
from psychrograph.timing import ExecutionTimer
from psychrograph.drag import DragHandler
import numpy as np

#https://stackoverflow.com/questions/55779944/how-to-remove-toolbar-buttons-from-matplotlib
from matplotlib import backend_bases


backend_bases.NavigationToolbar2.toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to  previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
      )

#@ExecutionTimer
def f_diagrama_tW(limits, lineas, lineas_step, lineas_text, lineas_text_step, lineas_color, alt, color_text,
                  color_fill, figsize):
    """
        LÍMITES
        ------------------------------------------------------------------------
        LIT - límite inferior de Temperatura         index 0
        LST - límite superior de Temperatura         index 1
        LIW - límite inferior de Radio de Humedad    index 2
        LSW - límite superior de Radio de Humedad    index 3

        LÍNEAS
        ------------------------------------------------------------------------
        Indica qué lineas quiero ver en el diagrama
        [Tdb, Twb, RH, W , v, h]
        cada índice adopta un valor de 0 o 1 con 1 indicando
        que se dibuje la línea

        lineas_step indica el paso entre líneas
        [Tdb, Twb, RH, W , v, h]

        INPUT
        alt - altura s.n.m. (m)

    """

    f = plt.figure('Diagrama Psicrométrico', figsize=figsize, dpi=100)
    ax = f.add_subplot(111)
    #https: // stackoverflow.com / questions / 43916834 / matplotlib - dynamically - change - text - position
    #https: // matplotlib.org / stable / users / explain / figure / event_handling.html
    #https: // scipy - cookbook.readthedocs.io / items / Matplotlib_Drag_n_Drop_Text_Example.html

    # Creo una figura
    fig_x, fig_y = figsize
    bck = plt.get_backend()
    mng = plt.get_current_fig_manager()
    mng.window.resizable(False, False)


    # Establezo los colores de los ejes y quito los que no quiero ver
    ax.spines['right'].set_color(color_pre)
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color(color_pre)

    # Escalas de los ticks y formatos
    if lineas_text[0] == 1: # Texto eje Tdb
        locator_T = lineas_text_step[0]
    else:
        locator_T = 10.0
    if lineas_text[1] == 1: # Texto eje W
        locator_W = lineas_text_step[3]
    else:
        locator_W = 2.0

    ax.xaxis.set_major_locator(MultipleLocator(locator_T))
    ax.xaxis.set_minor_locator(MultipleLocator(locator_T/2))
    ax.yaxis.set_major_locator(MultipleLocator(locator_W))
    ax.yaxis.set_minor_locator(MultipleLocator(locator_W/2))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

    # Posiciones y propiedades de los ticks y labels
    ax.tick_params(axis='x', which='major', labelsize=7, labelcolor=color_pre, color=color_pre)
    ax.tick_params(axis='y', which='both', labelsize=7, labelcolor=color_pre, color=color_pre,
                   labelleft=False, left=False, right=True, labelright=True, direction='in')
    # Apago la grilla
    ax.grid(False)

    # Apago títulos de ejes
    ax.set_xlabel('Temperatura de Bulbo Seco (°C)', fontsize=8, color=color_pre)
    ax.set_ylabel('Radio de Humedad (g/kg)', fontsize=8, color=color_pre)
    ax.yaxis.set_label_position('right')

    # Calculo la PATM
    PATM = psy.patm_ICAO(alt)

    # Propiedades del texto dentro del diagrama
    dx = 50.0
    props = {'ha': 'center', 'va': 'baseline', 'alpha': 0.5, 'zorder': 15}
    props_1 = {'ha': 'left', 'va': 'center', 'alpha': 0.5, 'zorder': 15}
    limits_ext = psy_f.check_lim(limits, PATM)
    ax.axis([limits_ext[0], limits_ext[1], limits_ext[2], limits_ext[3]])
    x_min, x_max = limits_ext[0], limits_ext[1]
    y_min, y_max = limits_ext[2], limits_ext[3]

    if limits_ext[4] < limits_ext[1]:
        ax.plot([limits_ext[4], limits_ext[1]], [limits_ext[3], limits_ext[3]], linewidth=0.5, color=color_pre)

    yt = psy_d.Calc_T_RH(limits_ext[0], 100.0, PATM)
    ax.plot([limits_ext[0], limits_ext[0]], [limits_ext[2], yt], linewidth=0.5, color=color_pre)

    # Dibujo la curva de saturación
    dp = 1
    x_sat = np.arange(limits_ext[0], limits_ext[4], dp, dtype=float)
    x_sat = np.append(x_sat, limits_ext[4])
    if x_sat.size > 0:
        y_sat = psy_d.Cur_Sat(x_sat, 100.0, PATM, limits, 0)
        ax.plot(x_sat, y_sat, linewidth=0.5, color=color_pre)
        x_fill = np.append(x_sat, limits[1])
        y_fill = np.append(y_sat, limits[3])
    ax.fill_between(x_fill, y_fill, color=color_fill, zorder=1)

    # Dibujo las líneas de Tdb
    if lineas[0] == 1:
        f_dib_T(limits_ext, lineas_step, lineas_color, PATM, ax)

    # Dibujo las curvas de RH
    if lineas[2] == 1:
        f_dib_RH(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, dx, props, fig_x, fig_y, x_min, x_max, y_min, y_max)

    # Dibujo las líneas de W
    if lineas[3] == 1:
        f_dib_W(limits_ext, lineas_step, lineas_color, PATM, ax)

    # Límites para curvas de v
    aux1 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[2], PATM, 1)
    aux2 = psy_d.Calc_T_HUM(limits_ext[0], 100, PATM, 0)
    aux3 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[2], PATM, 1)
    aux4 = psy_d.Calc_T_HUM(limits_ext[4], 100.0, PATM, 0)
    aux5 = psy_d.Calc_T_HUM(limits_ext[1], limits_ext[3], PATM, 1)

    # Dibujo las líneas de v
    if lineas[4] == 1:
        f_dib_v(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, props, fig_x, fig_y, x_min, x_max, y_min, y_max,
                aux1, aux2, aux3, aux4, aux5)

    # Dibujo las líneas de h
    if lineas[5] == 1:
        f_dib_h(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, props, props_1, fig_x, fig_y, x_min, x_max, y_min, y_max,
                aux1, aux2, aux3, aux4, aux5)

    # Dibujo las líneas de Twb
    if lineas[1] == 1:
        f_dib_Tw(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, props, fig_x, fig_y, x_min, x_max, y_min, y_max,
                 aux1, aux2, aux3, aux4, aux5)

    D = 15 * fig_y / (y_max - y_min)
    ax.text(0.0, 1.0, 'Carta Psicrométrica', fontsize=10, color=color_text, horizontalalignment='left',
            verticalalignment='bottom', transform=ax.transAxes)
    ax.text(0.0, 0.97, "a.s.n.m. " + r'{:.2f}'.format(float(alt)) + " m", fontsize=8, color=color_text,
            horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes)
    ax.text(0.0, 0.94, "Presión barométrica " + r'{:.2f}'.format(float(PATM)) + " kPa", fontsize=8, color=color_text,
            horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes)

    # Create the event handler
    dragh = DragHandler()

    plt.show()
    return f


#@ExecutionTimer
def f_dib_T(limits_ext, lineas_step, lineas_color, PATM, ax):
    x_Tdb = np.arange(limits_ext[0] + lineas_step[0], limits_ext[1], lineas_step[0], dtype=float)
    y_Tdb = psy_d.Cur_Sat(x_Tdb, 100.0, PATM, limits_ext, 0)
    y_Tdb = np.where(y_Tdb > limits[3], limits[3], y_Tdb)
    for x, y in np.nditer([x_Tdb, y_Tdb]):
        ax.plot([x, x], [limits_ext[2], y], linewidth=0.2, color=lineas_color[0], zorder=1)


#@ExecutionTimer
def f_dib_W(limits_ext, lineas_step, lineas_color, PATM, ax):
    y_W = np.arange(limits_ext[2] + lineas_step[3], limits_ext[3], lineas_step[3], dtype=float)
    x_W = psy_d.Cur_W(y_W, PATM)
    x_W = np.where(x_W < limits[0], limits[0], x_W)
    for x, y in np.nditer([x_W, y_W]):
        ax.plot([x, limits[1]], [y, y], linewidth=0.2, color=lineas_color[3], zorder=1)


#@ExecutionTimer
def f_dib_RH(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, dx, props, fig_x, fig_y, x_min, x_max, y_min, y_max):
    RH = np.arange(0 + lineas_step[2], 100.0, lineas_step[2], dtype=float)
    #print("RH", RH)
    aux_RH = RH % lineas_text_step[2]  # Máscara para extraer valores dónde quiero texto
    #print("aux_RH", aux_RH)
    ind_aux = RH[aux_RH == 0]
    #print("ind_aux", ind_aux)
    LCSrh = psy_d.Cur_Sat(limits_ext[1], RH, PATM, limits_ext, 1)
    # Evito valores mayores a 100°C
    LCSrh = np.where(LCSrh > 100.0, 100.0, LCSrh)
    #print("LCSrh", LCSrh)
    LCS_aux = LCSrh[aux_RH == 0]
    #print("LCSrh_aux", LCS_aux)

    for ind_RH, ind_LCS in np.nditer([RH, LCSrh]):
        x_RH = np.arange(limits_ext[0], ind_LCS, 2.0, dtype=float)
        x_RH = np.append(x_RH, ind_LCS)
        if len(x_RH):
            y_RH = psy_d.Cur_Sat(x_RH, ind_RH, PATM, limits, 0)
            ax.plot(x_RH, y_RH, linewidth=0.5, color=lineas_color[2])

    # Texto de las curvas
    if lineas_text[2] != 0:
        for ind_aux, LCS_aux in np.nditer([ind_aux, LCS_aux]):
            if limits_ext[1] > limits_ext[4] > limits_ext[0]:
                x_rh_text = limits_ext[4]
            else:
                x_rh_text = (limits_ext[0] + LCS_aux) / 2.0
            y_rh_text = psy_d.Calc_T_RH(x_rh_text, ind_aux, PATM)
            if y_rh_text < limits_ext[3] - 0.1:
                dy = psy_d.Calc_T_RH(x_rh_text + dx / 2, ind_aux, PATM)
                Dx = dx * fig_x / (x_max - x_min)
                Dy = dy * fig_y / (y_max - y_min)
                ang = (180.0 / np.pi) * np.arctan(Dy / Dx)
                ax.text(x_rh_text, y_rh_text, str(ind_aux) + "%", props, rotation=ang, fontsize=7, color=lineas_color[2])
    # https: // matplotlib.org / 3.1.1 / gallery / text_labels_and_annotations / text_rotation.html
    # https: // scipy - cookbook.readthedocs.io / items / Matplotlib_Drag_n_Drop_Text_Example.html
    # https: // stackoverflow.com / questions / 51028431 / calculating - matplotlib - text - rotation
    # https: // stackoverflow.com / questions / 5605167 / matplotlib - how - to - set - text - below - other - objects - when - they - overlap?rq = 4


#@ExecutionTimer
def f_dib_v(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, props, fig_x, fig_y, x_min, x_max, y_min, y_max,
            aux1, aux2, aux3, aux4, aux5):
    # auxiliar para texto
    aux_textv_x = []
    aux_textv_y = []
    aux_textv_p = []

    # Dibujo las líneas de v
    v_lim = [aux1[0], aux2[0], aux3[0], aux4[0], aux5[0]]
    if v_lim[3] < v_lim[2]:
        v_lim[3], v_lim[2] = v_lim[2], v_lim[3]
    if v_lim[1] > v_lim[2]:
        del v_lim[1]
        aux6 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[3], PATM, 1)
        v_lim[1] = aux6[0]
    v_aux = np.arange(round(v_lim[0], 2), v_lim[-1], lineas_step[4], dtype=float)

    for v in np.nditer([v_aux]):
        if v < v_lim[0]:
            continue
        if v < v_lim[1]:
            x1 = limits_ext[0]
            y1 = psy_d.Calc_T_v(x1, v, PATM)
            x2 = psy.TDB3ITb(limits_ext[2] / 1000.0, v, PATM)
            y2 = limits_ext[2]
        elif v < v_lim[3]:
            x1 = psy.TDB4ITb(100.0, v, PATM)
            y1 = psy_d.Calc_T_v(x1, v, PATM)
            if y1 > limits_ext[3]:
                x1 = psy.TDB3ITb(limits_ext[3] / 1000.0, v, PATM)
                y1 = limits_ext[3]
            x2 = psy.TDB3ITb(limits_ext[2] / 1000.0, v, PATM)
            y2 = limits_ext[2]
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_v(x2, v, PATM)
        else:
            x1 = psy.TDB3ITb(limits_ext[3] / 1000.0, v, PATM)
            y1 = limits_ext[3]
            x2 = limits_ext[1]
            y2 = psy_d.Calc_T_v(limits_ext[1], v, PATM)
        ax.plot([x1, x2], [y1, y2], dashes=[40, 15], linewidth=0.2, color=lineas_color[4])

        aux_textv_x.append(x2)
        aux_textv_y.append(y2)
        aux_textv_p.append(ftransform(x1, y1, x2, y2, fig_x, fig_y, x_min, x_max, y_min, y_max))

    # Texto de las líneas
    if lineas_text[4] != 0:
        ind_aux = np.arange(round(v_lim[0], 2), v_lim[-1], lineas_text_step[4], dtype=float)
        x_aux = aux_textv_x[::int(lineas_text_step[4] / lineas_step[4])]
        y_scale = limits_ext[3] - limits_ext[2]
        y_aux = aux_textv_y[::int(lineas_text_step[4] / lineas_step[4])]
        p_aux = aux_textv_p[::int(lineas_text_step[4] / lineas_step[4])]
        middle_index = len(x_aux) // 2
        for x_entry, y_entry, ang, ind in zip(x_aux, y_aux, p_aux, ind_aux):
           if x_entry < limits_ext[1]:
                ax.text(x_entry - 0.06 * y_scale, y_entry + 0.02 * y_scale, r'{:.2f}'.format(float(ind)), props, rotation=ang, fontsize=7,
                        color=lineas_color[4])
           else:
                ax.text(x_entry - 0.05 * y_scale, y_entry, r'{:.2f}'.format(float(ind)), props, rotation=ang, fontsize=7,
                        color=lineas_color[4])

        ax.text(x_entry - 0.25 * y_scale, y_entry - 0.1 * y_scale,
                        " Volumen específico (m3/kg)",
                        props, rotation=p_aux[middle_index], fontsize=7, color=lineas_color[4], picker=True, gid=id)


#@ExecutionTimer
def f_dib_h(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, props, props_1, fig_x, fig_y, x_min, x_max, y_min, y_max,
            aux1, aux2, aux3, aux4, aux5):
    # Límites para curvas de h
    h_lim = [aux1[1], aux2[1], aux3[1], aux4[1], aux5[1]]
    if h_lim[3] < h_lim[2]:
        h_lim[3], h_lim[2] = h_lim[2], h_lim[3]
    if h_lim[1] > h_lim[2]:
        del h_lim[1]
        aux6 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[3], PATM, 1)
        h_lim[1] = aux6[1]
    h_aux = np.arange(math.ceil(h_lim[0]), h_lim[-1], lineas_step[5], dtype=float)
    # auxiliar para texto
    aux_texth_x = []
    aux_texth_y = []
    aux_texth_p = []

    # Dibujo las líneas de h
    for h in np.nditer([h_aux]):
        if h < h_lim[1]:
            x1 = limits_ext[0]
            y1 = psy_d.Calc_T_h(x1, h, PATM)
            x2 = psy.TDBITb(limits_ext[2] / 1000.0, h, PATM)
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_h(x2, h, PATM)
            else:
                y2 = limits_ext[2]
        elif h < h_lim[3]:
            x1 = psy.TDB2ITb(100.0, h, PATM)
            y1 = psy_d.Calc_T_h(x1, h, PATM)
            if y1 > limits_ext[3]:
                x1 = psy.TDBITb(limits_ext[3] / 1000.0, h, PATM)
                y1 = limits_ext[3]
            x2 = psy.TDB2ITb(limits_ext[2] / 1000.0, h, PATM)
            y2 = limits_ext[2]
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_h(x2, h, PATM)
        else:
            x1 = psy.TDBITb(limits_ext[3] / 1000.0, h, PATM)
            y1 = limits_ext[3]
            x2 = limits_ext[1]
            y2 = psy_d.Calc_T_h(limits_ext[1], h, PATM)

        ax.plot([x1, x2], [y1, y2], linewidth=0.2, color=lineas_color[5])
        aux_texth_x.append(x1)
        aux_texth_y.append(y1)
        aux_texth_p.append(ftransform(x1, y1, x2, y2, fig_x, fig_y, x_min, x_max, y_min, y_max))


    # Texto de las líneas
    if lineas_text[5] != 0:
        ind_aux = np.arange(round(h_lim[0], 1), h_lim[-1], lineas_text_step[5], dtype=float)
        x_aux = aux_texth_x[::int(lineas_text_step[5] / lineas_step[5])]
        y_scale = limits_ext[3] - limits_ext[2]
        y_aux = aux_texth_y[::int(lineas_text_step[5] / lineas_step[5])]
        p_aux = aux_texth_p[::int(lineas_text_step[5] / lineas_step[5])]
        middle_index = len(x_aux) // 2
        for x_entry, y_entry, ang, ind in zip(x_aux, y_aux, p_aux, ind_aux):
            ax.text(x_entry - 0.05 * y_scale, y_entry + 0.01 * y_scale, r'{:.1f}'.format(float(ind)), props,
                rotation=ang, fontsize=7, color=lineas_color[5])

        ax.text(x_aux[middle_index] + 0.25 * y_scale, y_aux[middle_index] - 0.01 * y_scale,
            " Entalpía específica (kJ/kg)",
            props, rotation=p_aux[middle_index], fontsize=7, color=lineas_color[5], picker=True, gid=id)


#@ExecutionTimer
def f_dib_Tw(limits_ext, lineas_step, lineas_color, lineas_text, PATM, ax, props, fig_x, fig_y, x_min, x_max, y_min, y_max,
             aux1, aux2, aux3, aux4, aux5):
    twb_aux1 = psy_d.Calc_T_h_HUM(limits_ext[0], aux1[1], limits_ext[2], PATM, 1)
    twb_aux2 = psy_d.Calc_T_h_HUM(limits_ext[0], aux2[1], 100.0, PATM, 0)
    twb_aux3 = psy_d.Calc_T_h_HUM(limits_ext[1], aux3[1], limits_ext[2], PATM, 1)
    twb_aux4 = psy_d.Calc_T_h_HUM(limits_ext[4], aux4[1], 100.0, PATM, 0)
    twb_aux5 = psy_d.Calc_T_h_HUM(limits_ext[1], aux5[1], limits_ext[3], PATM, 1)
    twb_lim = [twb_aux1, twb_aux2, twb_aux3, twb_aux4, twb_aux5]
    if twb_lim[3] < twb_lim[2]:
        twb_lim[3], twb_lim[2] = twb_lim[2], twb_lim[3]
    if twb_lim[1] > twb_lim[2]:
        del twb_lim[1]
        aux6 = psy_d.Calc_T_HUM(limits_ext[0], limits_ext[3], PATM, 1)
        twb_lim[1] = psy_d.Calc_T_h_HUM(limits_ext[0], aux6[1], limits_ext[3], PATM, 1)

    twb_lim_d = twb_lim[-1]
    twb_lim_i = twb_lim[0]
    if (limits_ext[3] - twb_lim[-1]) < 0.5:
        twb_lim_d = twb_lim[-1] - 0.5
    if (twb_lim[0] - limits_ext[0]) < 0.5:
        twb_lim_i = twb_lim[0] + 0.5
    twb_aux = np.arange(math.ceil(twb_lim_i), twb_lim_d, lineas_step[1], dtype=float)
    # auxiliar para texto
    aux_textt_x = []
    aux_textt_y = []
    aux_textt_p = []

    for twb in np.nditer([twb_aux]):
        # A altas temperaturas LCS < LIT
        if twb < twb_lim[1]:
            x1 = limits_ext[0]
            y1 = psy_d.Calc_T_Twb(x1, twb, PATM)
            x2 = psy.TDB5ITb(limits_ext[2] / 1000.0, twb, PATM)
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_Twb(x2, twb, PATM)
            else:
                y2 = limits_ext[2]
        elif twb < twb_lim[3]:
            x1 = psy.TDB6ITb(100.0, twb, PATM)
            y1 = psy_d.Calc_T_Twb(x1, twb, PATM)
            if y1 > limits_ext[3]:
                x1 = psy.TDB5ITb(limits_ext[3] / 1000.0, twb, PATM)
                y1 = limits_ext[3]
            x2 = psy.TDB5ITb(limits_ext[2] / 1000.0, twb, PATM)
            y2 = limits_ext[2]
            if x2 > limits_ext[1]:
                x2 = limits_ext[1]
                y2 = psy_d.Calc_T_Twb(x2, twb, PATM)
        else:
            x1 = psy.TDB5ITb(limits_ext[3] / 1000.0, twb, PATM)
            y1 = limits_ext[3]
            x2 = limits_ext[1]
            y2 = psy_d.Calc_T_Twb(x2, twb, PATM)

        ax.plot([x1, x2], [y1, y2], linewidth=0.2, color=lineas_color[1], dashes=[20, 20, 40, 20])
        aux_textt_x.append((x1 + x2) / 2)
        aux_textt_y.append((y1 + y2) / 2)
        aux_textt_p.append(ftransform(x1, y1, x2, y2, fig_x, fig_y, x_min, x_max, y_min, y_max))

    # Texto de las líneas
    if lineas_text[1] != 0:
        ind_aux = np.arange(round(twb_lim[0], 1), twb_lim[-1], lineas_text_step[1], dtype=float)
        x_aux = aux_textt_x[::int(lineas_text_step[1] / lineas_step[1])]
        y_scale = limits_ext[3] - limits_ext[2]
        y_aux = aux_textt_y[::int(lineas_text_step[1] / lineas_step[1])]
        p_aux = aux_textt_p[::int(lineas_text_step[1] / lineas_step[1])]
        middle_index = len(x_aux) // 2
        for x_entry, y_entry, ang, ind in zip(x_aux, y_aux, p_aux, ind_aux):
            ax.text(x_entry, y_entry, r'{:.1f}'.format(float(ind)) + " °C", props, rotation=ang, fontsize=7, color=lineas_color[1])

        ax.text(x_aux[middle_index] + 0.1 * y_scale, y_aux[middle_index] + 0.1 * y_scale,
                    "Temp bulbo húmedo (°C)",
                    props, rotation=p_aux[middle_index], fontsize=7, color=lineas_color[1], picker=True, gid=id)


def ftransform(x1, y1, x2, y2, fig_x, fig_y, x_min, x_max, y_min, y_max):
    dx = x2 - x1
    dy = y2 - y1
    Dx = dx * fig_x / (x_max - x_min)
    Dy = dy * fig_y / (y_max - y_min)
    ang = (180.0 / np.pi) * np.arctan(Dy / Dx)
    return ang

# Speed up Matplotlib
# https://stackoverflow.com/questions/71686545/how-can-i-generate-matplotlib-graphs-faster
# https://matplotlib.org/stable/users/explain/artists/performance.html


if __name__ == '__main__':
    # [Tdb, Twb, RH, W , v, h]
    color_pre = 'black'
    # (0.9, 0.1, 0.1, 0.05)
    color_fill = 'whitesmoke'
    limits = [0.0, 50.0, 0.0, 30.0, 0.0]
    lineas = [1, 0, 1, 1, 1, 1]
    lineas_step = [1, 2, 10, 2, 0.02, 5]
    lineas_text = [1, 1, 1, 1, 1, 1]
    lineas_text_step = [10, 4, 20, 5, 0.04, 10]
    lineas_color = [color_pre, color_pre, color_pre, color_pre, color_pre, color_pre]
    figsize = (9, 7)
    #f = plt.figure('Diagrama Psicrométrico', figsize=figsize, dpi=100)
    #ax = f.add_subplot(111, picker=True)
    f_diagrama_tW(limits, lineas, lineas_step, lineas_text, lineas_text_step, lineas_color, 0.0, color_pre, color_fill, figsize)
    plt.show()

# https://stackoverflow.com/questions/43620690/matplotlib-creating-a-class-that-can-be-plotted
# https://realpython.com/python-callable-instances/
# https://stackoverflow.com/questions/57150426/what-is-printf
# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter19.05-Root-Finding-in-Python.html
# https://github.com/jonathanrocher/Code-samples/blob/master/scipy/fsolve.py
# https://fossies.org/linux/scipy/scipy/optimize/_root_scalar.py
# https://realpython.com/documenting-python-code/