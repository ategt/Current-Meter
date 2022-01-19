import * as d3 from "d3";

export function detectPeaks(data, accessor, options) {
  const {lookaround, sensitivity, coalesce, full} = Object.assign({
    lookaround: 2,
    sensitivity: 1.4,
    coalesce: 0,
    full: false
  }, options || accessor)
  
  const values = typeof accessor == "function" ? data.map(accessor) : data;

  // Compute a peakiness score for every sample value in `data`
  // We normalize the scale of the scores by mean-centering and dividing by the standard deviation
  // to get a dimensionless quantity such that can be used as a sensitivity parameter
  // across different scales of data (s. t. normalize(x) == normalize(k*x))
  const scores = values.map(
      (value, index) => peakiness(
        values.slice(Math.max(0, index - lookaround), index),
        value,
        values.slice(index + 1, index + lookaround + 1)
      )
    );

  const normed_scores = normalize(scores);

  // Candidate peaks are indices whose score is above the sensitivity threshold
  const candidates = d3.range(normed_scores.length).filter(index => normed_scores[index] > sensitivity);

  // If we have multiple peaks, coalesce those that are close together
  const groups = candidates.length ? [[candidates[0]]] : [];

  d3.pairs(candidates).forEach(([a, b]) => {
    if (b - a < coalesce) {
      groups[groups.length - 1].push(b)
    } else {
      groups.push([b])
    }
  });

  // Represent every group of peaks by the highest peak in the group
  const peaks = groups.map(
    group => group[d3.scan(group, (a, b) => values[b] - values[a])]
  );

  return full ? { data, values, scores, normed_scores, candidates, groups, peaks } : peaks;
}

// Assigns a spikiness score to `value`, based on its left and right neighbors
export const peakiness = (left, value, right) => {
  // assume zero outside the boundary
  return value - d3.max([d3.min(left) || 0, d3.min(right) || 0]) // this can be max or mean.
}

export const normalize = xs => {
  let mean = d3.mean(xs)
  let stdev = d3.deviation(xs)
  return xs.map(x => (x - mean) / stdev)
}