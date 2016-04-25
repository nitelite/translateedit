import sublime, sublime_plugin, json

settings_filename = "translate_commands.sublime-settings"

class InputTranslationKeyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.Window.show_input_panel(sublime.active_window(), "Specify key", "", self.onKeySpecified, None, None)
		
	def onKeySpecified(self, new_key):
		self.view.run_command("create_translation_key", { "new_key": new_key })


class SetJsonTranslateFileCommand(sublime_plugin.WindowCommand):
	def run(self):
		settings = sublime.load_settings(settings_filename)

		view = sublime.active_window().active_view()
		path = view.file_name() if view else None
		if path != None:
			jsonfiles = settings.get("json_files", [])
			jsonfiles.append(path)
			settings.set("json_files", jsonfiles)

			print("Current JSON files: " + ", ".join(jsonfiles))


class ClearJsonTranslateFileCommand(sublime_plugin.WindowCommand):		
	def run(self):
		view = sublime.active_window().active_view()
		settings = sublime.load_settings(settings_filename)
		settings.set("json_files", [])
		print("Current JSON files cleared")


class CreateTranslationKeyCommand(sublime_plugin.TextCommand):
	#path_root = "Skolemelk2016"
	#translation_file = "frontend/assets/lang/nb.json"

	def run(self, edit, new_key):
		settings = sublime.load_settings(settings_filename)

		jsonfiles = settings.get("json_files")

		selection = self.view.sel()
		#filename = self.view.file_name()

		#path = filename[0:filename.find(self.path_root) + len(self.path_root) + 1] + self.translation_file
		#print("Updating " + path)

		for region in selection:
			new_html = '<Translate component="p" content="' + new_key + '" />'
			translation = self.view.substr(region)
			self.view.replace(edit, region, new_html)

			for file in jsonfiles:
				self.updateFile(file, new_key, translation)

	def updateFile(self, path, new_key, translation):
		parts = new_key.split(".")
		data = None

		with open(path) as infile:
			data = json.load(infile)

		pointer = data
		for part in parts[:-1]:
			if not part in pointer:
				pointer[part] = {}
			pointer = pointer[part]

		pointer[parts[-1]] = translation

		with open(path, 'w') as outfile:
			json.dump(data, outfile, indent=4, separators=(',', ': '))

