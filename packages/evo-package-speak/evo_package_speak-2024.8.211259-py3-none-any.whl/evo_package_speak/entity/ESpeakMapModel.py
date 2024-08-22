#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_speak.entity.ESpeakModel import ESpeakModel
#========================================================================================================================================
"""ESpeakMapModel

    ESpeakMapModel _DOC_
    
"""
class ESpeakMapModel(EObject):

    VERSION:str="b1f40bb771d4fc52c36d308ef4b6651132ba8d7e0ea131a408702b0555eaa9c2"

    def __init__(self):
        super().__init__()
        
        self.mapESpeakModel:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteMap(self.mapESpeakModel, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.mapESpeakModel = self._doReadMap(ESpeakModel, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmapESpeakModel:{self.mapESpeakModel}",
                            ]) 
        return strReturn
    