import * as d3 from "d3";
import io from 'socket.io-client';
import { detectPeaks } from './peak-detection';

const NUMBER_REGEX = new RegExp("b\\'([\\d]+)");
const socket = io();

const mv_to_f = function (mv) {
	return (mv - 202.4) / 3.7;
};

const format_response = function (line_item) {
	try {
		const datum = +NUMBER_REGEX.exec(line_item).pop();
		const temperature = mv_to_f(datum);

		return `${Math.round(temperature)}°F - ${datum} - ${line_item}`;
	} catch (ex) {
		return line_item;
	}
};

const update_temperature_data = function (line_item) {
	const data_item = line_item;
	const reading = {millis: parseInt(data_item.millis), reading: parseInt(data_item.reading)};
	//const temperature = mv_to_f(datum);

	const data = window.chartThings.data;
	const width = window.chartThings.width;
	const height = window.chartThings.height;
	const margin = window.chartThings.margin;

	data.push(reading.reading);

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
	graph.selectAll("path").attr("d", line(data));
};

export const calculatePeaks = function () {
	const peaksIndexes = detectPeaks(window.chartThings.data, d => d,
								{ 
								  lookaround: 15,  // the number of neighbors to compare to on each side
								  sensitivity: 0.5, // sensitivity, in terms of standard deviations above the mean
								  coalesce: 5     // coalesce together peaks within this distance of each other
								});

	const peakSet = new Set(peaksIndexes);
	const peaks = window.chartThings.data.map((itm, idx) => ({idx:idx, value:itm})).filter((itm, idx) => peakSet.has(idx));

	return peaks;
};

window.calculatePeaks = calculatePeaks;

export const calculateTrouffs = function () {
	const peaksIndexes = detectPeaks(window.chartThings.data, d => -d,
								{ 
								  lookaround: 15,  // the number of neighbors to compare to on each side
								  sensitivity: 0.5, // sensitivity, in terms of standard deviations above the mean
								  coalesce: 5     // coalesce together peaks within this distance of each other
								});

	const peakSet = new Set(peaksIndexes);
	const peaks = window.chartThings.data.map((itm, idx) => ({idx:idx, value:itm})).filter((itm, idx) => peakSet.has(idx));

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

	//headingElement.innerText = format_response(msg.data);
	headingElement.innerText = JSON.stringify(msg.data);
	el.replaceChildren(headingElement);

	if (window.chartThings) {
		update_temperature_data(msg.data);
	}
});
