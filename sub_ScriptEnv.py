import sys
import os 
import warnings
import __main__
import platform
import System
import sub_AEDT

#check 64 bits platform
def CheckPlatform():
    bits = platform.architecture()[0]
    if bits.find("64") == -1: #not a 64 bit platform
       raise Exception("Python shell must run in 64 bit mode")

def CheckWindowsOnly():
    if System.Environment.OSVersion.Platform == System.PlatformID.Unix:
        raise Exception("Not supported on Unix Platforms")

# Check if paths are the same for this script file and launched com
# server
def CheckPaths(oDesktop):
    # Use the new API if available based on introspection
    if oDesktop.match('GetExeDir').Count >= 1:
        appPath =  os.path.normcase(os.path.normpath(oDesktop.GetExeDir()))
    else:
        # Has issues with developer builds but works ok for installations
        sysLibPath = oDesktop.GetSysLibDirectory()
        appPath =  os.path.normcase(os.path.normpath(os.path.split(sysLibPath)[0] + "/.."))

    filePath =  os.path.normcase(os.path.normpath(os.path.split(__file__)[0]))
    return filePath.startswith(appPath)

#---------------------------------------------------------------------------------------
# Always launches a new instance of the application: the variables related to these
# 'oDesktop', 'oAnsoftApplication' etc, are loaded into the supplied domain (or __main__)
#
# If needed create the module using..
#
# import imp, sys
# mod = imp.new_module('myModule')
# sys.modules[mod.__name__] = mod
#
# IntializeNew(NonGraphical=True, Module=mod)
#---------------------------------------------------------------------------------------
def InitializeNew(NonGraphical=False, Module = None):
    # Till we can test and verify
    CheckWindowsOnly()
    _doInitialize("", Module, AlwaysNew=True, NG=NonGraphical)

#---------------------------------------------------------------------------------------
# Launches the COM server associated with the supplied ProgID. Can connect to
# an existing instance. Because of this and because an existing COM server may be
# NG or not, we do not allows this to specify NG mode.
#
# The variables created are stored in the __main__ module.
#
# Note that unlike InitializeNew, Initialize does not take a module since COM bojects
# created by ProgID tend to be reused (if the server is already up). Multiple Initializes
# can hit the same existing com server. So within a script, we treat progID COM servers
# like globals
#---------------------------------------------------------------------------------------
def Initialize_NG(name):
    #_doInitialize(name, Module=None, AlwaysNew=False, NG=False)
    oApp, oDesktop = _doInitialize(name, Module=None, AlwaysNew=True, NG=True)
    return oApp, oDesktop

def Initialize(name):
    #_doInitialize(name, Module=None, AlwaysNew=False, NG=False)
    oApp, oDesktop = _doInitialize(name, Module=None, AlwaysNew=False, NG=False)
    return oApp, oDesktop

def _doInitialize(name, Module, AlwaysNew, NG):

  # default module is __main__
  if Module is None:
    Module = sys.modules['__main__']

  # We assume that for a given module, user calls Shutdown before 
  # reiniting. Previously we used to warn if oAnsoftApplication was found
  # to be defined here. However, ScriptEnv.Initialize is called multiple times
  # in script playbackscenarios under ARM and we don't want these warnings all
  # the time.
  if not "oAnsoftApplication" in dir(Module):
    # throws exception if not 64 bits
    CheckPlatform()

    import clr    
    File = sub_AEDT.Get_AEDT_Dir() + "\\Ansys.Ansoft.CoreCOMScripting.dll"
    clr.AddReferenceToFileAndPath(File)
    #clr.AddReference("Ansys.Ansoft.CoreCOMScripting")
    from Ansys.Ansoft.CoreCOMScripting.COM import StandalonePyScriptWrapper

    oApp = None
    if AlwaysNew:
      oApp = StandalonePyScriptWrapper.CreateObjectNew(NG)
    else:
      oApp = StandalonePyScriptWrapper.CreateObject(name)

    if oApp:
      # check that the COM server was created from the right directory
      oDesktop = oApp.GetAppDesktop()
      #if not CheckPaths(oDesktop):
      #  warnings.warn("Application was launched from different directory")

      #adding oAnsoftApplication and oDesktop to the module
      setattr(Module, "oAnsoftApplication", oApp)
      setattr(Module, "oDesktop", oDesktop)
      
    else:
      raise Exception("Failed to launch application")

  return oApp, oDesktop

# For use in cleaning up a scripting environment created via
# Initialize. Assumes a single ElectronicsDesktop launch
# All created COM objects are unusable after this even if they
# are not set to None
# If Initialize/InitializeNew inited a supplied module, send that in here
def Shutdown(Module=None):
    # default Module is __main__
    if Module is None:
        Module = sys.modules['__main__']

    # Shutdown
    scopeID = None
    if "oAnsoftApplication" in dir(Module) and "oDesktop" in dir(Module):
        if Module.oDesktop is not None:
            try:
                scopeID = Module.oDesktop.ScopeID
                Module.oDesktop.QuitApplication()
                #import sub_functions
                #sub_funcitons.ReleaseObject(Module.oDesktop)
                
            except:
                pass
        else:
            warnings.warn("Supplied module does not have oDesktop and oAnsoftApplication objects.")

        # Clear out the COMScope and module
        try:
            from Ansys.Ansoft.CoreCOMScripting.Util import COMUtil
            
            # clear the scope out
            if scopeID is not None:
                COMUtil.ReleaseCOMObjectScope(COMUtil.PInvokeProxyAPI, scopeID)

            # reset the variables
            delattr(Module, "oAnsoftApplication")
            delattr(Module, "oDesktop")
        except:
            pass

def Release(Module=None):
    # default Module is __main__
    if Module is None:
        Module = sys.modules['__main__']

    # Shutdown
    scopeID = None
    if "oAnsoftApplication" in dir(Module) and "oDesktop" in dir(Module):
        if Module.oDesktop is not None:
            try:
                scopeID = Module.oDesktop.ScopeID
                Module.oDesktop = None
                #import sub_functions
                #sub_funcitons.ReleaseObject(Module.oDesktop)
                
            except:
                pass
        else:
            warnings.warn("Supplied module does not have oDesktop and oAnsoftApplication objects.")

        # Clear out the COMScope and module
        try:
            from Ansys.Ansoft.CoreCOMScripting.Util import COMUtil
            
            # clear the scope out
            if scopeID is not None:
                COMUtil.ReleaseCOMObjectScope(COMUtil.PInvokeProxyAPI, scopeID)

            # reset the variables
            delattr(Module, "oAnsoftApplication")
            delattr(Module, "oDesktop")
        except:
            pass
