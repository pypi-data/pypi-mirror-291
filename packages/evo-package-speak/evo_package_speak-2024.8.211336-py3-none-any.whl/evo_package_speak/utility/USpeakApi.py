#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_speak.entity import *

#<
#OTHER IMPORTS ...
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# USpeakApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""USpeakApi
"""
class USpeakApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if USpeakApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            USpeakApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: USpeakApi instance
    """
    @staticmethod
    def getInstance():
        if USpeakApi.__instance is None:
            uObject = USpeakApi()  
            uObject.doInit()  
        return USpeakApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doInit

    Raises:
        Exception: api exception

    Returns:

    """   
    def doInit(self):   
        try:
#<
            #INIT ...
            pass
#>   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnTts(self, eAction:EAction) -> EAction:
        """doOnTts utility callback
            input: ESpeakInput
            output: ESpeakOutput

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eSpeakInput:ESpeakInput = eAction.doGetInput(ESpeakInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eSpeakInput is None:
                raise Exception("ERROR_REQUIRED|eSpeakInput|")

#<        
            #Add other check

            if eSpeakInput.eApiText is None:
                raise Exception("ERROR_REQUIRED|eSpeakInput.eApiText|")
            
            if IuText.StringEmpty(eSpeakInput.eApiText.text) :
                raise Exception("ERROR_REQUIRED|eSpeakInput.eApiText.text|")
                 
            eSpeakOutput = ESpeakOutput()
            eSpeakOutput.doGenerateID()
            
            textSanatize = str(eSpeakInput.eApiText.text).replace("\"", "'")
            
            os_name = platform.system()

            fileID = IuKey.toString(eSpeakOutput.id)
            fileExt= ".wav"
            
            # Perform actions based on the OS
            if os_name == "Darwin":
                filePath = f"/tmp/cyborgai/{fileID}{fileExt}"
                command=f"say --data-format LEI16@22050  --file-format WAVE  -o {filePath} \"{textSanatize}\""
 
                await IuSystem.do_exec_async(command)
                
                eApiFileAudio = EApiFile()
                eApiFileAudio.id = eSpeakOutput.id
                eApiFileAudio.enumEApiFileType = EnumEApiFileType.AUDIO
                await eApiFileAudio.fromFile(filePath)
                
                eSpeakOutput.eApiFileAudio = eApiFileAudio
 
            elif os_name == "Linux":
               pass
               
            else:
                raise Exception(f"ERROR_UNSUPOORTED|{os_name}|")
            
            os.remove(filePath)
            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eSpeakOutput)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnStt(self, eAction:EAction) -> EAction:
        """doOnStt utility callback
            input: EApiFile
            output: EApiFile

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eApiFile:EApiFile = eAction.doGetInput(EApiFile)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eApiFile is None:
                raise Exception("ERROR_REQUIRED|eApiFile|")

#<        
            #Add other check
            '''
            if eApiFile. is None:
                raise Exception("ERROR_REQUIRED|eApiFile.|")
            '''
   
            eApiFile = EApiFile()
            eApiFile.doGenerateID()
            eApiFile.doGenerateTime()

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eApiFile)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetModel(self, eAction:EAction) -> EAction:
        """doOnGetModel utility callback
            input: EApiQuery
            output: ESpeakModel

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eApiQuery:EApiQuery = eAction.doGetInput(EApiQuery)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eApiQuery is None:
                raise Exception("ERROR_REQUIRED|eApiQuery|")

#<        
            #Add other check
            '''
            if eApiQuery. is None:
                raise Exception("ERROR_REQUIRED|eApiQuery.|")
            '''
   
            eSpeakModel = ESpeakModel()
            eSpeakModel.doGenerateID()
            eSpeakModel.doGenerateTime()

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eSpeakModel)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnQueryModel(self, eAction:EAction) -> EAction:
        """doOnQueryModel utility callback
            input: EApiQuery
            output: ESpeakMapModel

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eApiQuery:EApiQuery = eAction.doGetInput(EApiQuery)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eApiQuery is None:
                raise Exception("ERROR_REQUIRED|eApiQuery|")

#<        
            #Add other check
            '''
            if eApiQuery. is None:
                raise Exception("ERROR_REQUIRED|eApiQuery.|")
            '''
   
            eSpeakMapModel = ESpeakMapModel()
            eSpeakMapModel.doGenerateID()
            eSpeakMapModel.doGenerateTime()

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eSpeakMapModel)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<
#OTHER METHODS ...
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
