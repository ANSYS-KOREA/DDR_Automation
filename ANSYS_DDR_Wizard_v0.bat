: Launch Option 1 - Specific version of ANSYS EM Suite
: 	step1. Create an environment variable [ANSYSEM_INSTALL_DIR]
:	step2. Set its value to the	Specific version of ANSYS EM Suite install folder.
: 			ex)C:\Program Files\AnsysEM\AnsysEM20.2\Win64

: Launch Option 2 - Latest version of ANSYS EM Suite
:	You don't have to do anything because SerDes 3D Model Wizard will automatically find the ANSYS EM Suite of the latest version on your PC.

set PATH="C:\AnsysEM\AnsysEM21.2\Win64\common\IronPython"

ipy64 "D:\1_Work\20220106_DDR_Compliance\1_Work\Code\ANSYS_DDR_Wizard_v0\ANSYS_DDR_Wizard_v0.py"