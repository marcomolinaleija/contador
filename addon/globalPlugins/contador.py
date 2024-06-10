# Contador. complemento para NVDA.
# Este archivo está cubierto por la Licencia Pública General GNU
# Consulte el archivo COPYING.txt para obtener más detalles.
# Copyright (C) 2024 Marco Leija <marcomolinaleija@hotmail.com>

import scriptHandler
import globalVars
import api
import ui
import tones
import textInfos
import globalPluginHandler
from languageHandler import getLanguage
import os
import webbrowser
import addonHandler
addonHandler.initTranslation()

def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls

@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.toggling = False

	def getScript(self, gesture):
		if not self.toggling:
			return super().getScript(gesture)
		script = super().getScript(gesture)
		if not script:
			script = self.script_error
		return self.finish(script)

	def finish(self, script):
		def wrapper(*args, **kwargs):
			try:
				script(*args, **kwargs)
			finally:
				self.deactivateLayer()
		return wrapper

	def deactivateLayer(self):
		self.toggling = False
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)

	def script_error(self, gesture):
		# Translators: Error message when no function is assigned to the pressed key
		ui.message(_("No se ha asignado alguna función para la tecla presionada"))
		tones.beep(277.18, 110)

	@scriptHandler.script(
		# Translators: Description of the script to activate the counter command layer
		description=_("Activa la capa de comandos para el contador"),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_counterLayer(self, gesture):
		if self.toggling:
			self.script_error(gesture)
			return
		self.bindGestures(self.__counterGestures)
		self.toggling = True
		# Translators: Message indicating that the command layer has been activated
		ui.message(_("Capa de comandos activada. presiona f1 para obtener ayuda."))
		tones.beep(349.23, 110)

	def countCharacters(self, text):
		return len(text)

	def countWords(self, text):
		return len(text.split())

	@scriptHandler.script(
		# Translators: Description of the script to count characters in the selected text
		description=_("Cuenta los caracteres del texto seleccionado."),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_countCharactersSelection(self, gesture):
		text = self.getSelectedText()
		if not text:
			# Translators: Message indicating that no text is selected
			ui.message(_("No hay texto seleccionado"))
		else:
			count = self.countCharacters(text)
			# Translators: Message showing the number of characters in the selected text
			ui.message(_(f"El texto seleccionado tiene {count} caracteres"))

	@scriptHandler.script(
		# Translators: Description of the script to count characters from the clipboard text
		description=_("Cuenta los caracteres en el texto desde el portapapeles."),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_countCharactersClipboard(self, gesture):
		text = api.getClipData()
		if not text or not isinstance(text, str) or text.isspace():
			# Translators: Message indicating that there is no text on the clipboard
			ui.message(_("No hay texto en el portapapeles"))
		else:
			count = self.countCharacters(text)
			# Translators: Message showing the number of characters in the clipboard text
			ui.message(_(f"El texto del portapapeles tiene {count} caracteres"))

	@scriptHandler.script(
		# Translators: Description of the script to count words in the selected text
		description=_("Cuenta palabras desde el texto seleccionado."),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_countWordsSelection(self, gesture):
		text = self.getSelectedText()
		if not text:
			# Translators: Message indicating that no text is selected
			ui.message(_("No hay texto seleccionado"))
		else:
			count = self.countWords(text)
			# Translators: Message showing the number of words in the selected text
			ui.message(_(f"El texto seleccionado tiene {count} palabras"))

	@scriptHandler.script(
		# Translators: Description of the script to count words from the clipboard text
		description=_("Cuenta las palabras del texto desde el portapapeles."),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_countWordsClipboard(self, gesture):
		text = api.getClipData()
		if not text or not isinstance(text, str) or text.isspace():
			# Translators: Message indicating that there is no text on the clipboard
			ui.message(_("No hay texto en el portapapeles"))
		else:
			count = self.countWords(text)
			# Translators: Message showing the number of words in the clipboard text
			ui.message(_(f"El texto del portapapeles tiene {count} palabras"))

	@scriptHandler.script(
		# Translators: Description of the script to show clipboard text in a browseable NVDA window
		description=_("Muestra el texto del portapapeles en una ventana navegable de NVDA"),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_readText(self, gesture):
		text = api.getClipData()
		if text:
			# Translators: Window title showing the clipboard text
			ui.browseableMessage(text, _("Texto en el portapapeles"), isHtml=False)
		else:
			# Translators: Message indicating that there is no text on the clipboard
			ui.message(_("No hay texto en el portapapeles."))

	@scriptHandler.script(
		# Translators: Description of the script to open the addon's documentation
		description=_("Abre la documentación del complemento")
	)
	def script_open_doc(self, gesture):
		# Obtiene el idioma actual configurado en NVDA
		currentLanguage = getLanguage()
		# Mapea el idioma a las rutas correspondientes
		docPath = os.path.join(globalVars.appArgs.configPath, "addons", "contador", "doc", currentLanguage, "readme.html")

		if os.path.exists(docPath):
			webbrowser.open(docPath)
			# Translators: Message indicating that the documentation has been opened in the current language
			ui.message(_(f"Documentación abierta en {currentLanguage}."))
		else:
			# Translators: Message indicating that documentation for the current language was not found
			ui.message(_(f"No se encontró la documentación para el idioma {currentLanguage}."))

	@scriptHandler.script(
		# Translators: Description of the script to count lines from the clipboard text
		description=_("Cuenta la cantidad de líneas desde el texto en el portapapeles"),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_count_lines(self, gesture):
		text = api.getClipData()
		if text:
			text_lines = len(text.splitlines())
			# Translators: Message showing the number of lines in the clipboard text
			ui.message(_(f"El texto del portapapeles tiene {text_lines} líneas"))
		else:
			# Translators: Message indicating that there is no text on the clipboard
			ui.message(_("No hay texto en el portapapeles"))

	@scriptHandler.script(
		# Translators: Description of the script to count lines in the selected text
		description=_("Cuenta la cantidad de líneas desde el texto seleccionado"),
		# Translators: Category under which the script falls
		category=_("Contador")
	)
	def script_count_lines_selection(self, gesture):
		text = self.getSelectedText()
		if not text:
			# Translators: Message indicating that no text is selected
			ui.message(_("No hay texto seleccionado"))
		else:
			text_lines = len(text.splitlines())
			# Translators: Message showing the number of lines in the selected text
			ui.message(_(f"El texto seleccionado tiene {text_lines} líneas"))

	def getSelectedText(self):
		obj = api.getFocusObject()
		try:
			info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
			if info and not info.isCollapsed:
				return info.text
		except (RuntimeError, NotImplementedError):
			return None

	__counterGestures = {
		"kb:alt+c": "countCharactersSelection",
		"kb:c": "countCharactersClipboard",
		"kb:alt+p": "countWordsSelection",
		"kb:p": "countWordsClipboard",
		"kb:M": "readText",
		"kb:L": "count_lines",
		"kb:alt+L": "count_lines_selection",
		"kb:f1": "open_doc",
	}

	__gestures = {
		"kb:NVDA+shift+c": "counterLayer",
	}
