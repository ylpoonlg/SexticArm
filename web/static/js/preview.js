const plot = document.getElementById('plot');

function plotArm(callback) {
    // request joint coordinates

    Plotly.newPlot( plot,
        [{
            type: 'scatter3d',
            mode: 'lines',
            x: [   0,   0,  10,  80,  90],
            y: [   0,   0,  50, 100,  90],
            z: [   0, 150, 200, 200, 180],
            opacity: 1,
            line: {
                width: 6,
                color: '#0000ff',
                reversescale: false
            }
        }], {
            height: 512,
            width: 512,
            margin: 'auto'
        }
    );
    callback();
}

setTimeout(() => {
    plotArm(() => {
        console.log('Plot loaded');
    });
}, 0);