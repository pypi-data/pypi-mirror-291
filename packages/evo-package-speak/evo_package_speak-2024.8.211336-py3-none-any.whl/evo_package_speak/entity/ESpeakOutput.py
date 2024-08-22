#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""ESpeakOutput

    ESpeakOutput _DOC_
    
"""
class ESpeakOutput(EObject):

    VERSION:str="9a9cd44d1e60d18eb8a723359e14081381404ebeca201b004eb6e359959f2dd7"

    def __init__(self):
        super().__init__()
        
        self.language:str = None
        self.eApiFileAudio:EApiFile = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.language, stream)
        self._doWriteEObject(self.eApiFileAudio, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.language = self._doReadStr(stream)
        self.eApiFileAudio = self._doReadEObject(EApiFile, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tlanguage:{self.language}",
                f"\teApiFileAudio:{self.eApiFileAudio}",
                            ]) 
        return strReturn
    