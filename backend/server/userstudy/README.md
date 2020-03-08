# User Study
This directory contains functions and classes that are specifically used for the User Study conducted on February 4th and 5th, 2020.

## Classes and Functions
File `manager.py` contains `UserStudyDialogManager` and `UserStudyAdvancedDialogManager` which are special `DialogManager`s for the user study.

File `scenarios.py` contains functions to generate scenarios for all stages and a check function for advanced stage scenarios. The scenario-generating functions are `create_practice_scenarios`, `create_novice_scenarios` and `create_advanced_scenarios`. The file also includes a check function `advanced_scenario_check` for checking procedures created in advanced-stage scenarios.