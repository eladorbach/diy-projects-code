# Historical source

`multispectral_2019_original.py` preserves the code published in the April 2019 blog post. Blogger whitespace has been normalized so the control flow is readable; names, values and overall behavior are intentionally left historical.

Important historical quirks include the temporary variable name `lux`, a 32-entry LED list even though three PCA9685 boards were configured, and reinitializing the IDS camera for every band. See `../src/` for the cleaned publication version.
