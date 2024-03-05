import scriptHandler
import api
import ui
import tones
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @scriptHandler.script(
        description="Cuenta del portapapeles la cantidad de caracteres de un texto.",
        gesture="kb:NVDA+shift+C",
        category="Contador"
    )
    def script_countCharacters(self, gesture):
        tones.beep(1000, 100)
        text = api.getClipData()
        if text:
            count = len(text)
            message = f"El texto tiene {count} caracteres."
            ui.message(message)
        else:
            ui.message("No hay texto seleccionado.")
    @scriptHandler.script(
        description="Cuenta del portapapeles la cantidad de palabras de un texto.",
        gesture="kb:NVDA+shift+W",
        category="Contador"
    )
    def script_countWords(self, gesture):
        tones.beep(1000, 100)
        text = api.getClipData()
        if text:
            words = text.split()
            count = len(words)
            message = f"El texto tiene {count} palabras."
            ui.message(message)
        else:
            ui.message("No hay texto seleccionado.")
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.bindGesture("kb:NVDA+shift+c", "countCharacters")
        self.bindGesture("kb:NVDA+shift+w", "countWords")
