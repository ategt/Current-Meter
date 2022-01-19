import * as d3 from "d3";
import { calculatePeaks, calculateTrouffs } from './header';

const ampPartsPerAnalogUnit = 20 / 509;
const correctiveFactor = 12.5 / 13.732809430255402;

export const calculateAmps = function () {
	const amps = new Array();

	const mergedWavePoints = [...calculateTrouffs(), ...calculatePeaks()];
	mergedWavePoints.sort((a,b) => a.idx - b.idx);

	for ( let i = 0; i < mergedWavePoints.length - 1; i++ ) {
	    const magnitude = Math.abs(mergedWavePoints[i].value - mergedWavePoints[i+1].value) / 2;
	    amps.push(magnitude * ampPartsPerAnalogUnit * correctiveFactor);
	}

	//amps.map(x => Math.round(x*100)/100);

	return amps;
};

export const useAmpereData = function () {
	const data = window.chartThings.data;
	const width = window.chartThings.width;
	const height = window.chartThings.height;
	const margin = window.chartThings.margin;

	const ampData = calculateAmps();

	// update axis domains
	window.chartThings.x.domain([0, ampData.length]).range([margin.left, width - margin.right]);
	//window.chartThings.y.domain([d3.min(ampData, function(d) { return d; }), d3.max(ampData, function(d) { return d; })]);
	window.chartThings.y.domain([0, d3.max(ampData, function(d) { return d; })]);

	const graph = window.chartThings.graph;
	const line = window.chartThings.line;

	// update axis labels
	graph.selectAll("g.y.axis").call(window.chartThings.yAxis);
	graph.selectAll("g.x.axis").call(window.chartThings.xAxis);

	// re-draw data
	graph.selectAll("path").attr("d", line(ampData));
};

window.useAmpereData = useAmpereData;