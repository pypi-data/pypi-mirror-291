
def f_dib_point(ax, style, *args):
    for arg in args:
        ax.scatter(arg[1], arg[2], color=style["line_color"], marker=style["marker"])
        for i, txt in enumerate(arg[0]):
            ax.annotate(txt, (arg[1][i] + 1.0, arg[2][i] + 1.0), **style["text_props"], picker=True, gid=id)


def f_dib_line(ax, style, *args):
    for arg in args:
        f_dib_point(ax, style, *args)
        ax.plot(arg[1], arg[2], linestyle=style["line_style"], linewidth=style["line_width"],
                color=style["line_color"])

