def _remove_trailing_comma(string: str):
	if string[-1] == ',':
		return string.rstrip(string[-1])
	return string

def parse_string(string: str):
	string = _remove_trailing_comma(string)
	return (str(string)
				.replace('\t', '')
				.replace('\n', '')
				.replace('\\', '')
				.strip()
				.split(','))
