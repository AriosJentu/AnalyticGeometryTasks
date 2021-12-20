def text_replacer(text):
	
	if text.find("\\left[") >= 0:
		text = text.replace("#R#", ", заданной точками")
		text = text.replace("#RS#",
			", где одна из них задана точками"
			if text.count("\\left[") == 1 else
			", заданных точками"
		)

		if text.rfind("\\left[") > text.rfind(";") and text.find("#RG#") >= 0:
			text = text.replace("#RG#", 
				", заданной точками"
				if text.count("\\left[") == 1 else
				", заданных точками"
			)
		elif text.rfind("\\left[") < text.rfind(";") and text.find("#RG#") >= 0:
			text = text.replace("#RH#",
				", заданной точками"
				if text.count("\\left[") == 1 else
				""
			)

	text = text.replace("#R#", "")
	text = text.replace("#RS#", "")
	text = text.replace("#RG#", "")
	text = text.replace("#RH#", "")

	return text