const plot = document.getElementById('plot');

function plotlyPlot(J1, J2, J3, J6) {
    Plotly.newPlot( plot,
        [{
            type: 'scatter3d',
            mode: 'lines',
            x: [ 0, J1[0], J2[0], J3[0], J6[0] ],
            y: [ 0, J1[1], J2[1], J3[1], J6[1] ],
            z: [ 0, J1[2], J2[2], J3[2], J6[2] ],
            opacity: 1,
            line: {
                width: 6,
                color: '#0000ff',
                reversescale: false
            }
        }], {
            height: 512,
            width: 512,
            scene:{
                aspectmode: "manual",
                aspectratio: {
                    x: 1, y: 1, z: 1,
                },
                xaxis: {
                    nticks: 9,
                    range: [-200, 200],
                },
                yaxis: {
                    nticks: 7,
                    range: [-200, 200],
                },
                zaxis: {
                    nticks: 10,
                    range: [0, 400],
                }
            },

        }
    );
}


function visPlot(J1, J2, J3, J6) {
    let data = new vis.DataSet();
    data.add({
        x: 0, y: 0, z: 0,
    });
    data.add({
        x: J1[0], y: J1[1], z: J1[2],
    });
    data.add({
        x: J2[0], y: J2[1], z: J2[2],
    });
    data.add({
        x: J3[0], y: J3[1], z: J3[2],
    });
    data.add({
        x: J6[0], y: J6[1], z: J6[2],
    });

    // specify options
    let options = {
        width:  '512px',
        height: '512px',
        style: 'line',
        showPerspective: true,
        showGrid: true,
        showShadow: false,
        keepAspectRatio: true,
        verticalRatio: 0.5
    };

    // create a graph3d
    let graph3d = new vis.Graph3d(plot, data, options);
}


function plotArm(joints, callback) {
    let J1 = joints[0];
    let J2 = joints[1];
    let J3 = joints[2];
    let J6 = joints[3];
    //plotlyPlot(J1, J2, J3, J6);
    visPlot(J1, J2, J3, J6);

    callback();
}

let plotInterval = setInterval(() => {
    let joints = serverStatus.joints;
    plotArm(joints, () => {
        console.log('Plot loaded');
    });
}, 3000);

// Server Timeout
setTimeout(() => {
    clearInterval(plotInterval);
}, SERVER_TIMEOUT);