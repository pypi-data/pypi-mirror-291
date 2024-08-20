from psychrograph import main

path = str('C:/Users/Jose/OneDrive - SRL AZZAMURA/FLASK/psychroplan/psychrograph/styles/basic_chart.json')

chart_handler = main.ChartPlotHandler(path)
# Draw lines
linea = [["OA", "MX"], [35.0, 23.0], [14.0, 10.0]]
# main.ChartPlotHandler.draw_point(chart_handler, linea)
main.ChartPlotHandler.draw_line(chart_handler, linea)

# Draw chart
main.ChartPlotHandler.show_plot()
