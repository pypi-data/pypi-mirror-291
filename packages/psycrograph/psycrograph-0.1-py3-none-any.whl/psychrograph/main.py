""" A package to make psychrometric charts """

import gc
import json
import psychrograph.psychro_aux as psy
import psychrograph.psychro_aux_diag as psy_d
import psychrograph.psy_verify_lim as psy_f
import psychrograph.psy_curve_fun as psy_c
import psychrograph.psy_system_fun as psy_s
from matplotlib import backend_bases
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)
from psychrograph.drag import DragHandler

backend_bases.NavigationToolbar2.toolitems = (
    ('Home', 'Reset original view', 'home', 'home'),
    ('Back', 'Back to  previous view', 'back', 'back'),
    ('Forward', 'Forward to next view', 'forward', 'forward'),
    (None, None, None, None),
    ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    (None, None, None, None),
    ('Save', 'Save the figure', 'filesave', 'save_figure'),
)


# path = str('styles/default_chart.json')
class ChartPlotHandler:
    def __init__(self, path):
        self.f = None
        self.ax = None
        self.path = path
        # Read the configuration file
        self.style = self.open_json(self.path)
        # Set the chart style
        self.set_style(self.style)
        # Calculate the barometric pressure
        self.patm = psy.patm_ICAO(self.style["altitude_m"])
        # Calculate the chart limits
        self.limits_ext = self.set_limits(self.style, self.patm)
        # Draw an empty chart with limits
        self.draw_chart_base(self.style, self.limits_ext, self.patm)
        # Draw the chart curves
        self.draw_chart_curves(self.style, self.limits_ext, self.patm)
        # Set titles in the chart
        self.set_title(self.style, self.patm)
        # Create the event handler
        self.dragh = DragHandler()
        # Draw lines
        # self.draw_line(self.hvac, self.patm)
        # self.show_plot()
        gc.collect()
        # collected = gc.collect()
        # print("Garbage collector: collected", "%d objects." % collected)

    # Customize style based on the JSON configuration
    @staticmethod
    def open_json(json_str):
        """ Load configuration file from a JSON string """
        with open(json_str, 'r', encoding='utf8') as json_file:
            config_file = json.load(json_file)
        return config_file

    # Function to set the chart style
    def set_style(self, style):
        # https: // www.geeksforgeeks.org / extract - nested - data - from -complex - json /
        self.f = plt.figure(style["figure"]["title"], figsize=style["figure"]["figsize"], dpi=100)
        self.ax = self.f.add_subplot(111)
        # Avoid resizing the figure
        mng = plt.get_current_fig_manager()
        mng.window.resizable(False, False)
        # Axes titles
        self.ax.set_xlabel(**style["figure"]["x_label"])
        self.ax.set_ylabel(**style["figure"]["y_label"])
        # Locators
        self.ax.xaxis.set_major_locator(MultipleLocator(style["figure"]["locators"]["x_major_locator"]))
        self.ax.xaxis.set_minor_locator(MultipleLocator(style["figure"]["locators"]["x_minor_locator"]))
        self.ax.yaxis.set_major_locator(MultipleLocator(style["figure"]["locators"]["y_major_locator"]))
        self.ax.yaxis.set_minor_locator(MultipleLocator(style["figure"]["locators"]["y_minor_locator"]))
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        # Positions and properties of ticks and labels
        self.ax.tick_params(**style["figure"]["x_axis_ticks"])
        self.ax.tick_params(**style["figure"]["y_axis_ticks"])
        # Default style (out of the user scope)
        self.ax.grid(False)
        self.ax.yaxis.set_label_position('right')
        # Axes colors
        self.ax.spines['right'].set_color(style["figure"]["color_pre"])
        self.ax.spines['left'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['bottom'].set_color(style["figure"]["color_pre"])

    # Function to define the limits of the chart
    def set_limits(self, style, patm):
        self.limits_ext = psy_f.check_lim(style["limits"], patm)
        return self.limits_ext

    # Function to Draw the base of the chart
    def draw_chart_base(self, style, limits_ext, patm):
        psy_c.f_dib_sat(limits_ext, style["chart_curves"]["color_fill"], style["chart_curves"]["prop_sat"], patm,
                        self.ax)
        self.ax.axis([limits_ext[0], limits_ext[1], limits_ext[2], limits_ext[3]])
        if limits_ext[4] < limits_ext[1]:
            self.ax.plot([limits_ext[4], limits_ext[1]], [limits_ext[3], limits_ext[3]], linewidth=0.5,
                         color=style["figure"]["color_pre"])
        yt = psy_d.Calc_T_RH(limits_ext[0], 100.0, patm)
        self.ax.plot([limits_ext[0], limits_ext[0]], [limits_ext[2], yt], linewidth=0.5,
                     color=style["figure"]["color_pre"])

    # Function to Draw the chart curves
    def draw_chart_curves(self, style, limits_ext, patm):
        # Draw the Tdb lines
        if style["chart_curves"]["curve_tdb"]:
            psy_c.f_dib_tdb(limits_ext, style["chart_curves"]["step_tdb"], style["chart_curves"]["prop_tdb"], patm,
                            self.ax)
        # Draw the W lines
        if style["chart_curves"]["curve_W"]:
            psy_c.f_dib_w(limits_ext, style["chart_curves"]["step_W"], style["chart_curves"]["prop_W"], patm, self.ax)
        # Draw the RH lines
        if style["chart_curves"]["curve_RH"]:
            psy_c.f_dib_rh(limits_ext, style["chart_curves"]["step_RH"], style["chart_curves"]["text_step_RH"],
                           style["chart_curves"]["prop_RH"], patm, self.ax, style["figure"]["figsize"],
                           style["chart_curves"]["text_prop_RH"])
        # Draw the v lines
        if style["chart_curves"]["curve_v"]:
            psy_c.f_dib_v(limits_ext, style["chart_curves"]["step_v"], style["chart_curves"]["text_step_v"],
                          style["chart_curves"]["prop_v"], patm, self.ax, style["figure"]["figsize"],
                          style["chart_curves"]["text_prop_v"], style["chart_curves"]["text_v"])

        if style["chart_curves"]["curve_h"]:
            psy_c.f_dib_h(limits_ext, style["chart_curves"]["step_h"], style["chart_curves"]["text_step_h"],
                          style["chart_curves"]["prop_h"], patm, self.ax, style["figure"]["figsize"],
                          style["chart_curves"]["text_prop_h"], style["chart_curves"]["text_h"])

        if style["chart_curves"]["curve_twb"]:
            psy_c.f_dib_twb(limits_ext, style["chart_curves"]["step_twb"], style["chart_curves"]["text_step_twb"],
                            style["chart_curves"]["prop_twb"], patm, self.ax, style["figure"]["figsize"],
                            style["chart_curves"]["text_prop_twb"], style["chart_curves"]["text_twb"])

    def set_title(self, style, patm):
        self.ax.text(0.0, 1.0, style["figure"]["title"], **style["figure"]["title_prop"], transform=self.ax.transAxes)
        self.ax.text(0.0, 0.97, style["figure"]["sub_title1"] + r'{:.2f}'.format(float(style["altitude_m"])) + " m",
                     **style["figure"]["title_prop"], transform=self.ax.transAxes)
        self.ax.text(0.0, 0.94, style["figure"]["sub_title2"] + r'{:.2f}'.format(float(patm)) + " kPa",
                     **style["figure"]["title_prop"], transform=self.ax.transAxes)

    def draw_line(self, *args):
        style = self.open_json(self.path)
        psy_s.f_dib_line(self.ax, style, *args)

    def draw_point(self, *args):
        style = self.open_json(self.path)
        psy_s.f_dib_point(self.ax, style, *args)

    @staticmethod
    def show_plot():
        # Show the matplotlib plot
        plt.show()


