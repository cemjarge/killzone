document.addEventListener('DOMContentLoaded', function () {
    const svg = d3.select('#graph');
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const xScale = d3.scaleLinear().domain([0, 7]).range([margin.left, innerWidth]);
    const yScale = d3.scaleLinear().domain([0, 10]).range([innerHeight, margin.top]);

    const stablePointsData = Array.from({ length: 8 }, (_, i) => ({ x: i, y: 5 }));
    const draggablePointsData = Array.from({ length: 8 }, (_, i) => ({ x: i, y: 5 }));

    // Create stable points
    svg.selectAll('.stable-point')
        .data(stablePointsData)
        .enter()
        .append('circle')
        .attr('class', 'stable-point')
        .attr('cx', d => xScale(d.x))
        .attr('cy', d => yScale(d.y))
        .attr('r', 5);

    // Create draggable points
    const draggablePoints = svg.selectAll('.point')
        .data(draggablePointsData)
        .enter()
        .append('circle')
        .attr('class', 'point')
        .attr('cx', d => xScale(d.x))
        .attr('cy', d => yScale(d.y))
        .attr('r', 5)
        .call(d3.drag()
            .on('drag', function (event, d) {
                d.y = yScale.invert(event.y);
                d3.select(this)
                    .attr('cy', yScale(d.y));
            })
            .on('end', function () {
                // Output the updated Y values
                const yValues = draggablePointsData.map(d => d.y.toFixed(2));
                console.log('Y-axis values:', yValues);
            })
        );

    // Add X and Y axes (optional)
    const xAxis = d3.axisBottom(xScale).ticks(8).tickFormat(i => `P${i+1}`);
    const yAxis = d3.axisLeft(yScale);

    svg.append('g')
        .attr('transform', `translate(0, ${innerHeight})`)
        .call(xAxis);

    svg.append('g')
        .attr('transform', `translate(${margin.left}, 0)`)
        .call(yAxis);
});
