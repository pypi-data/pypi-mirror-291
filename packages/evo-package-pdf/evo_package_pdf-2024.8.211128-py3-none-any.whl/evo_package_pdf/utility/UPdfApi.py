#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_pdf.entity import *

#<
from pymupdf import pymupdf, Document, Page
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# UPdfApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""UPdfApi
"""
class UPdfApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if UPdfApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            UPdfApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: UPdfApi instance
    """
    @staticmethod
    def getInstance():
        if UPdfApi.__instance is None:
            uObject = UPdfApi()  
            uObject.doInit()  
        return UPdfApi.__instance
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
    async def doOnParser(self, eAction:EAction) -> EAction:
        """doOnParser utility callback
            input: EPdfInput
            output: EPdfOutput

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            ePdfInput:EPdfInput = eAction.doGetInput(EPdfInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if ePdfInput is None:
                raise Exception("ERROR_REQUIRED|ePdfInput|")

#<        
            eAction.enumApiAction = EnumApiAction.PROGRESS
            example_float = 123.456

            # Convert float to bytes
            float_bytes = struct.pack('f', example_float)
            eAction.output = float_bytes
            yield eAction    
               
            
            IuLog.doDebug(__name__, f"doParser:{ePdfInput} ")
           
#<
            
            ePdfOutput = await self.__doParserPdf(ePdfInput)
            
           
            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(ePdfOutput)
                    
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
#<
    async def __doParserPdf(self, ePdfInput) ->EPdfOutput:
        try:
            input_pdf = await ePdfInput.pdf.toFile()
            print(input_pdf)
            
            ePdfOutput = EPdfOutput()
            ePdfOutput.doGenerateID(input_pdf)
            ePdfOutput.doGenerateTime()
            
            doc = pymupdf.open(input_pdf)
            page = doc.load_page
            pageIndex = 1
            for page in doc:
                
                ePdfPage = EPdfPage()
                ePdfPage.doGenerateID(str(pageIndex)) #.rjust(3,"0")
                
                links = page.get_links()
                for link in links:
                    print("link", link)
                    if "uri" in link:
                        uri=link["uri"]
                        eApiText = EApiText()
                        eApiText.doGenerateID(uri)
                        eApiText.text = uri
                        ePdfPage.mapEApiTextUri.doSet(eApiText)
                    
            
                textPage = page.get_textpage()
                textFullTmp = textPage.extractText()
                page_lines = textFullTmp.split('\n')
                title = page_lines[0] if page_lines else ''
                text = '\n'.join(page_lines[1:]) if len(page_lines) > 1 else ''
                
                ePdfPage.number = pageIndex
                ePdfPage.title = title
                ePdfPage.text = text
                
                image_list = page.get_images(full=True)
                for image_index, img in enumerate(image_list, start=1):  

                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    eApiImage = EApiFile()
                    eApiImage.doGenerateID(f"image_{page.number +1}_{image_index}")
                    eApiImage.data = image_bytes
                    eApiImage.name = f"image_{page.number +1}_{image_index}"
                    eApiImage.ext = ".png" #image_ext   
                    eApiImage.enumEApiFileType = EnumEApiFileType.IMAGE
                    ePdfPage.mapEApiImage.doSet(eApiImage)
                
                ePdfOutput.mapEPdfPage.doSet(ePdfPage)  
                pageIndex+=1
                
            return ePdfOutput
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise     
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
