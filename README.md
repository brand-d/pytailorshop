pyTailorshop
============
Repository with a python re-implementation of the [Tailorshop simulation](https://www.psychologie.uni-heidelberg.de/ae/allg/tools/tailorshop/index.html) (Danner et al., 2011).
The implementation was also used for our [work](https://github.com/brand-d/iccm2024-tailorshop) analysing and modeling human behavior in the tailorshop scenario (Brand, Todorovikj & Ragni, 2024).

## Overview

- `main.py`: Contains an examplary run of a few steps in the tailorshop scenario.
- `main_gui.py`: Launches a GUI for the Tailorshop simulation.
- `tailorshop.py`: Contains the main simulator class.
- `ts_types.py`: Contains classes for managing the observable, derived variables (`Tailorshop_State`) and the controllable variables/actions (`Controllable_Variables`).

## Dependencies

The tailorshop simulation needs the following dependencies to run:

- Python 3
    - [numpy](https://numpy.org)

## Run the example

In order to run the main script with the example, use the following commands:

```
cd /path/to/repository/
$> python main.py
```

To open the GUI, use the following command instead:

```
cd /path/to/repository/
$> python main_gui.py
```

## References

Danner, D., Hagemann, D., Holt, D.V., Hager, M., Schankin, A., Wüstenberg. S. & Funke, J. (2011). Measuring Performance in Dynamic Decision Making: Reliability and Validity of the Tailorshop Simulation. *Journal of Individual Differences*, 32, 225-233.

Brand, D., Todorovikj, S., and Ragni, M. (2024). Predicting Complex Problem Solving Performance in the Tailorshop Scenario. In *Proceedings of the 22th International Conference on Cognitive Modeling*.