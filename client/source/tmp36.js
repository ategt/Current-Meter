/**
 * Convert temperature from degrees Celcius
 * into degrees Farenheit.
 */
export const celciusToFarenheit = function (c) {
	return (c * 1.8) + 32;
};

/**
 * Converts an analog Arduino input from an integer
 * between 0 and 1023 into a temperature reading
 * in Celcius.  The TMP36 formula is T = 100 * (V - 0.5)
 * where T is the temperature Celsius and V is volts.
 * The Arduino analog input returns a reading between
 * 0 and 1023 so this function converts the analog reading
 * into a decimal, then finds that decimal of five volts,
 * which is then plugged into the TMP36 formula.
 */
export const readingToCelcius = function ( reading ) {
	return 100 * (((reading/1023)*5) - 0.5);
};

/**
 * Combines two functions into one.
 * Converts an Arduino analog reading into
 * degrees Farenheit.
 */
export const readingToFarenheit = function ( reading ) {
	return celciusToFarenheit( readingToCelcius( reading ) );
};
