: Launch Option 1 - Specific version of ANSYS EM Suite
: 	step1. Create an environment variable [ANSYSEM_INSTALL_DIR]
:	step2. Set its value to the	Specific version of ANSYS EM Suite install folder.
: 			ex)C:\Program Files\AnsysEM\AnsysEM20.2\Win64

: Launch Option 2 - Latest version of ANSYS EM Suite
:	You don't have to do anything because ADEA will automatically find the ANSYS EM Suite of the latest version on your PC.

set PATH=%SIWAVE_INSTALL_DIR%\common\IronPython"

ipyw64 ".\ANSYS_EYE_Analyzer_v0.py"