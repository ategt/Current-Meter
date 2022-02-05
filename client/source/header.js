import * as d3 from "d3";
import io from 'socket.io-client';
import { detectPeaks } from './peak-detection';
import { readingToFarenheit } from './tmp36';

const NUMBER_REGEX = new RegExp("b\\'([\\d]+)");
const socket = io();

const mv_to_f = function (mv) {
	return (mv - 202.4) / 3.7;
};

const format_power = function (data) {
	return `Amps: ${data.amps} \tWatts: ${data.watts}`;
};

const format_temperature = function (data) {
	const freezerTemp = Math.round(mv_to_f(parseInt(data.denoised_temperature_reading)));
	const counterTemp = Math.round(readingToFarenheit(parseInt(data.denoised_exterior_temperature_reading)));

	return `Freezer: ${freezerTemp}°F \tCounter: ${counterTemp}°F`;
};

const format_response = function (line_item) {
	try {
		if ( location.search.includes("watts") ) {
		 	return format_power(line_item);
		} else if ( location.search.includes("temperature") ) {
			return format_temperature(line_item);
		} else {
			// Default to temperature, I guess
			return format_temperature(line_item);
		}
	} catch (ex) {
		return JSON.stringify(line_item);
	}
};

const update_temperature_data = function (line_item) {
	const data_item = line_item;
	const reading = {watts: parseFloat(data_item.watts), temp_reading: parseInt(data_item.denoised_temperature_reading)};
	//const temperature = mv_to_f(datum);
		// adjustedReading: "-0.05"
		// amps: "-0.00"
		// denoised_temperature_reading: "447"
		// instant_temperature: "449"
		// reading: "1.32"
		// watts: "-0.34"

	const data = window.chartThings.data;
	const width = window.chartThings.width;
	const height = window.chartThings.height;
	const margin = window.chartThings.margin;

	if ( location.search.includes("watts") ) {
	 	data.push(reading.watts);
	} else if ( location.search.includes("temperature") ) {
		data.push(mv_to_f(reading.temp_reading));
	} else {
		// Default to temperature, I guess
		data.push(mv_to_f(reading.temp_reading));
	}

	//data.splice(0, Math.max(data.length-250, 0));

	// update axis domains
	window.chartThings.x.domain([0, data.length]).range([margin.left, width - margin.right]);
	window.chartThings.y.domain([d3.min(data, function(d) { return d; }), d3.max(data, function(d) { return d; })]);

	const graph = window.chartThings.graph;
	const line = window.chartThings.line;

	// update axis labels
	graph.selectAll("g.y.axis").call(window.chartThings.yAxis);
	graph.selectAll("g.x.axis").call(window.chartThings.xAxis);

	// re-draw data
	graph.selectAll("path.line.path.main").attr("d", line(data));
};

export const calculatePeaks = function (data, options) {
	const peaksIndexes = detectPeaks(data, d => d, options);
	const peakSet = new Set(peaksIndexes);
	const peaks = data.map((itm, idx) => ({idx:idx, value:itm})).filter((itm, idx) => peakSet.has(idx));

	return peaks;
};

window.calculatePeaks = calculatePeaks;

export const calculateTrouffs = function (data, options) {
	const peaksIndexes = detectPeaks(data, d => -d, options);
	const peakSet = new Set(peaksIndexes);
	const peaks = data.map((itm, idx) => ({idx:idx, value:itm})).filter((itm, idx) => peakSet.has(idx));

	return peaks;
};

window.calculateTrouffs = calculateTrouffs;

const calculateVariance = function () {
	return d3.variance(window.chartThings.data);
};

window.calcVar = calculateVariance;

socket.on('board response broadcast', function(msg) {
	const el = document.getElementById("reading-banner");
	const headingElement = document.createElement("h2");

	headingElement.innerText = format_response(msg.data);
	//headingElement.innerText = JSON.stringify(msg.data);
	el.replaceChildren(headingElement);

	if (window.chartThings) {
		update_temperature_data(msg.data);
	}
});
