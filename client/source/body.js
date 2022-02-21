import * as d3 from "d3";

const margin = ({top: 0, right: 0, bottom: 20, left: 60});
const height = 133*3.7;
const width = 275*4;

const data = new Array();

const x = d3.scaleLinear().range([margin.left, width - margin.right]);
const y = d3.scaleLinear().range([height - margin.bottom, margin.top]);

const line = d3.line()
	// assign the X function to plot our line as we wish
	.x(function(d,i){
		// return the X coordinate where we want to plot this datapoint
		return x(i);
	})
	.y(function (d) {
		// return the Y coordinate where we want to plot this datapoint
		return y(d);
	});

const xAxis = function (g) {
	return g
	.attr("transform", `translate(0,${height - margin.bottom})`)
	.call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));
};

const yAxis = function (g) {
	const ticks = 8;

	return g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(ticks))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(""));
};

const graph = d3.select("#temperature-graph").append("svg")
	.attr("class", "chart")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom);

// Add the x-axis
graph.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0, 0)")
	.call(xAxis)
	.append("text")
		.attr("class", "x axis label")
		.attr("y", "1.75em")
		.attr("dy", "0.71em")
		.attr("x", (width/2))
		.attr("font-size", "1.4em")
		.attr("fill", "black")
		.attr("font-weight", "bold")
		.style("text-anchor", "middle")
		.text("Time (Seconds)");

const tempAxis = function ( graph, yAxis, height ) {
	// Add the y-axis to the left
	graph.append("g")
		.attr("class", "y axis")
		.attr("transform", "translate(0, 0)")
		.call(yAxis)
		.append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", -48)
			.attr("dy", "0.71em")
			.attr("x", 0-(height/2))
			.attr("font-size", "1.4em")
			.attr("fill", "black")
			.attr("font-weight", "bold")
			.style("text-anchor", "middle")
			.text("Temperature (°F)");
};

const wattsAxis = function ( graph, yAxis, height ) {
	// Add the y-axis to the left
	graph.append("g")
		.attr("class", "y axis")
		.attr("transform", "translate(0, 0)")
		.call(yAxis)
		.append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", -48)
			.attr("dy", "0.71em")
			.attr("x", 0-(height/2))
			.attr("font-size", "1.4em")
			.attr("fill", "black")
			.attr("font-weight", "bold")
			.style("text-anchor", "middle")
			.text("Power (Watts)");
};

if ( location.search.includes("watts") ) {
 	wattsAxis( graph, yAxis, height );
} else if ( location.search.includes("temperature") ) {
	tempAxis( graph, yAxis, height );
} else if ( location.search.includes("refrigerator") ) {
	tempAxis( graph, yAxis, height );
} else {
	// Default to temperature, I guess
	tempAxis( graph, yAxis, height );
}

graph.append("svg:path")
		.attr("class", "line path main")
		.attr("fill", "none")
		.attr("stroke", "steelblue")
		.attr("stroke-width", "1.5")
		.attr("stroke-opacity", "1");

window.chartThings = {
	x: x,
	y: y,
	graph: graph,
	data: data,
	line: line,
	margin: margin,
	height: height,
	width: width,
	yAxis: yAxis,
	xAxis: xAxis,
};