def text_replacer(text):
	
	if text.find("\\left[") >= 0:
		text = text.replace("#R#", ", заданной точками")
		text = text.replace("#RE#", " (given by points)")

		text = text.replace("#RS#",
			", где одна из них задана точками"
			if text.count("\\left[") == 1 else
			", заданных точками"
		)

		text = text.replace("#RSE#",
			" (one of them given by points)"
			if text.count("\\left[") == 1 else
			" (given by points)"
		)

		if text.rfind("\\left[") > text.rfind(";") and text.find("#RG#") >= 0:
			text = text.replace("#RG#", 
				", заданной точками"
				if text.count("\\left[") == 1 else
				", заданных точками"
			)

		elif text.rfind("\\left[") < text.rfind(";") and (text.find("#RH#") or text.find("#RHE#")) >= 0:
			text = text.replace("#RH#",
				", заданной точками"
				if text.count("\\left[") == 1 else
				""
			)
			text = text.replace("#RHE#",
				" (given by points)"
				if text.count("\\left[") == 1 else
				""
			)

	text = text.replace("#R#", "")
	text = text.replace("#RS#", "")
	text = text.replace("#RG#", "")
	text = text.replace("#RH#", "")

	text = text.replace("#RE#", "")
	text = text.replace("#RSE#", "")
	text = text.replace("#RHE#", "")

	return text