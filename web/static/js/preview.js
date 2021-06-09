const plot = document.getElementById('plot');

var lastJoints = []; // to store last joint positions. If unchanged, graph will not be plotted again
var lastCamPos = {}; // to reset to the same camera position when refreshing the plot

function resizePlot() {
    let cw = $('#plot').width();
    $('#plot').css({'height':cw+'px'});
    lastJoints = [];
    plotRefresh();
}

// wait for serverStatus to load then resize plot
// refresh every one second
var resizePlotInterval = setInterval(() => {
    if (serverStatus) {
        resizePlot();
        clearInterval(resizePlotInterval);
    }
}, 1000);
window.addEventListener("resize", resizePlot);

// Use vis.js to plot 3dgraph
function visPlot(J1, J2, J3, J6) {
    let data = new vis.DataSet();
    data.add({ x: 0, y: 0, z: 0, });
    data.add({ x: J1[0], y: J1[1], z: J1[2], });
    data.add({ x: J2[0], y: J2[1], z: J2[2], });
    data.add({ x: J3[0], y: J3[1], z: J3[2], });
    data.add({ x: J6[0], y: J6[1], z: J6[2], });

    // specify options
    let options = {
        width:  '100%',
        height: '100%',
        xCenter: '50%',
        yCenter: '50%',

        xMin: -200, xMax: 200,
        yMin: -200, yMax: 200,
        zMin: 0, zMax: 410,

        style: 'line',
        tooltip: true,
        keepAspectRatio: true,
        verticalRatio: 1.0,
        cameraPosition: lastCamPos
    };

    // create a graph3d
    let graph3d = new vis.Graph3d(plot, data, options);

    function onCameraPositionChange(newPos) {
        lastCamPos = newPos;
    }
    graph3d.on('cameraPositionChange', onCameraPositionChange);
}

function plotRefresh(e) {
    let joints = serverStatus.joints;

    if (JSON.stringify(joints) == JSON.stringify(lastJoints)) return;
    lastJoints = joints;
    let J1 = joints[0];
    let J2 = joints[1];
    let J3 = joints[2];
    let J6 = joints[3];

    visPlot(J1, J2, J3, J6);

    console.log('Plot loaded');
}

let plotInterval = setInterval(() => {
    plotRefresh();
}, 1000);

// Server Timeout
setTimeout(() => {
    clearInterval(plotInterval);
}, SERVER_TIMEOUT);