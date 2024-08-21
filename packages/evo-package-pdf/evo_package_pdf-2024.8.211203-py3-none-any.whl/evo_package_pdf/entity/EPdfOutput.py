#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_pdf.entity.EPdfPage import EPdfPage
#========================================================================================================================================
"""EPdfOutput

    this is EPdfOutput DESCRIPTION
    
"""
class EPdfOutput(EObject):

    VERSION:str="416e199190f29762a510f1e0b9554fc0350ff58a6dca8bfde901ab2d531e331a"

    def __init__(self):
        super().__init__()
        
        self.mapEPdfPage:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteMap(self.mapEPdfPage, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.mapEPdfPage = self._doReadMap(EPdfPage, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmapEPdfPage:{self.mapEPdfPage}",
                            ]) 
        return strReturn
    