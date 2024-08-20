# Psychrometric Chart Generator

This package generates a configurable psychrometric chart in matplotlib.

## Description

Based on a json file located in a folder called styles (default_chart), all the
visual aspects of the psychrometric chart could be configurated.

## Getting Started

### Dependencies

The dependencies are describer in the pyproject.toml file.
* numpy 1.26.4
* matplotlib 3.8.3
* scipy 1.12.0

### Installing

The package could be downloaded with the pip command as any other package

* pip psychartgen

### Executing program

Once installed, the chart is generated with a simple function call 

```
chart_handler.show_plot()
```

## Authors

Contributors names and contact info

José E. Azzaro  
jose@azzamura.com

## Version History

* 2024.4
    * First version as a python package

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details

## Acknowledgments

The project utilize several sources including 
* ASHRAE RP 1485 - Thermodynamic Properties of Real Moist Air, Dry Air, Steam, Water, and Ice
* ASHRAE RP 216 - Thermodynamic Properties of Dry Air, Moist Air and Water and SI Psychrometic Charts
* ASHRAE RP 1060 - Formulation of Thermodynamic Properties of Moist Air at High Temperature
* D. C. Shallcross - Handbook of Psychrometric Charts Humidity diagrams for engineers
* Donald P. Gatley - Understanding Psychrometrics
