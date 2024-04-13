# Contador. complemento para NVDA.
# Este archivo está cubierto por la Licencia Pública General GNU
# Consulte el archivo COPYING.txt para obtener más detalles.
# Copyright (C) 2024 Marco Leija <marcomolinaleija@hotmail.com>

import scriptHandler
import globalVars
import api
import ui
import tones
import globalPluginHandler
import addonHandler
addonHandler.initTranslation()

def disableInSecureMode(decoratedCls):
    if globalVars.appArgs.secure:
        return globalPluginHandler.GlobalPlugin
    return decoratedCls

@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @scriptHandler.script(
        # Translators: Description of the script: Counts the number of characters in text from the clipboard.
        description=_("Cuenta del portapapeles la cantidad de caracteres de un texto."),
        gesture="kb:NVDA+shift+C",
        # Translators: Category name for the script
        category=_("Contador")
    )
    def script_countCharacters(self, gesture):
        tones.beep(1000, 100)
        text = api.getClipData()
        if text:
            count = len(text)
            # Translators: This message will show the number of characters in the text.
            message = _("El texto tiene {count} caracteres.").format(count=count)
            ui.message(message)
        else:
            # Translators: Indicates that there is no text selected.
            ui.message(_("No hay texto en el portapapeles."))

    @scriptHandler.script(
        # Translators: Description for the script: Counts the number of words in text from the clipboard.
        description=_("Cuenta del portapapeles la cantidad de palabras de un texto."),
        gesture="kb:NVDA+shift+W",
        category=_("Contador")
    )
    def script_countWords(self, gesture):
        tones.beep(1000, 100)
        text = api.getClipData()
        if text:
            words = text.split()
            count = len(words)
            message = _("El texto tiene {count} palabras.").format(count=count)
            # Translators: This message announces the number of words of the text contained in the clipboard.
            ui.message(message)
        else:
            # Translators: Indicates that there is no text selected.
            ui.message(_("No hay texto en el portapapeles."))

    @scriptHandler.script(
        # Translators: Description for the script: Displays clipboard text in an NVDA browseable message window.
        description=_("Muestra el texto del portapapeles en una ventana navegable de NVDA."),
        gesture="kb:NVDA+ctrl+E",
        category=_("Contador")
    )
    def script_readText(self, gesture):
        text = api.getClipData()
        if text:
        # Translators: The next line shows the message, with the window title called text on the clipboard
            ui.browseableMessage(text, _("Texto en el portapapeles"), isHtml=True)
        else:
            # Translators: Indicates that there is no text on the clipboard.
            ui.message(_("No hay texto en el portapapeles."))

    def __init__(self):
        super(GlobalPlugin, self).__init__()