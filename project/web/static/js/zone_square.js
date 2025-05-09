const videoWrapper = document.getElementById('video-wrapper');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const dcanvas = document.getElementById('canvas-display');
const ctx = canvas.getContext('2d');
const dctx = dcanvas.getContext('2d');
const parameter = document.getElementById('zone_number');

let current = 0;
let points = [{x: 0, y: 0}, {x: 0, y: 0}, {x: 0, y: 0}, {x: 0, y: 0}];
let check = false;


function updatePointsFromInputs() {
    for (let i = 1; i <= 4; i++) {
        const x = document.getElementById(`x${i}`).value;
        const y = document.getElementById(`y${i}`).value;
        points[i - 1] = { x: parseInt(x, 10), y: parseInt(y, 10) };
    }
    drawPoints();
}

for (let i = 1; i <= 4; i++) {
    document.getElementById(`x${i}`).addEventListener('change', updatePointsFromInputs);
    document.getElementById(`y${i}`).addEventListener('change', updatePointsFromInputs);
}

videoWrapper.addEventListener('click', function(event) {
    const rect = video.getBoundingClientRect(); // Use video instead of videoWrapper to get the correct scaling factor
    
    // make point it smaller than real
    // const scaleX = rect.width / video.videoWidth;
    // const scaleY = rect.height / video.videoHeight;

    // make point bigger than real
    // const scaleX = video.videoWidth / rect.width;
    // const scaleY = video.videoHeight / rect.height;

    // use this 2 code
    const x = (event.clientX - rect.left);
    const y = (event.clientY - rect.top);

    document.getElementById(`x${current + 1}`).value = Math.ceil(x);
    document.getElementById(`y${current + 1}`).value = Math.ceil(y);

    points[current] = { x: Math.round(x), y: Math.round(y) };

    if (current < 3) {
        current++;
        check = false;
    } else {
        current = 0;
        check = true;
    }
    drawPoints();
});

// function that will appear the point when create zone
function drawPoints() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    points.forEach(point => {
        ctx.fillStyle = '#FF0000';
        ctx.beginPath();
        ctx.arc(point.x*0.6, point.y*0.5, 2, 0, 2 * Math.PI);
        ctx.fill();
    });

    const firstPoint = points[0];
    const lastPoint = points[points.length - 1];

    // Ensure both points have coordinates (not zero)
    // if (firstPoint.x !== 0 || firstPoint.y !== 0 || lastPoint.x !== 0 || lastPoint.y !== 0) {
    if (check) {
        ctx.strokeStyle = '#00FF00'; // Green color for the line
        ctx.lineWidth = 2; // Adjust line width if needed
        ctx.beginPath();
        ctx.moveTo(firstPoint.x*0.6, firstPoint.y*0.5);
        ctx.lineTo(lastPoint.x*0.6, lastPoint.y*0.5);
        ctx.stroke();
    }
}

// function that will create set of zone and will fetch the zone that have created
function createAndDisplayPoints() {

    const taskId = window.taskId;
    const jsonUrl = `/static/detection/zone_data/${taskId}.json`;

    fetch(jsonUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            data.zones.forEach(zone => {
                let before_x = zone.points[3].x;
                let before_y = zone.points[3].y;

                let TextPoint_x = zone.points[0].x;
                let TextPoint_y = zone.points[0].y;

                zone.points.forEach(point => {
                    dctx.fillStyle = '#00FF00';
                    dctx.strokeStyle = '#00FF00';
                    dctx.beginPath();
                    dctx.arc(point.x * 0.6, point.y * 0.5, 2, 0, 2 * Math.PI);
                    dctx.fill();

                    // line
                    dctx.moveTo(before_x*0.6, before_y*0.5);
                    dctx.lineTo(point.x * 0.6, point.y * 0.5, 2, 0, 2 * Math.PI);
                    dctx.stroke();

                    before_x = point.x;
                    before_y = point.y;

                    if(TextPoint_x>point.x){
                        if(TextPoint_y<point.y){
                            TextPoint_x = point.x;
                            TextPoint_y = point.y;
                        }
                    }
                });
                
                const rectX = TextPoint_x * 0.6;
                const rectY = TextPoint_y * 0.5;

                // Display text within the rectangle
                dctx.fillStyle = '#0000FF';
                dctx.font = '10px Arial';
                dctx.fillText(`zone${zone.id}`, rectX, rectY);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Initialize points from existing input values
updatePointsFromInputs();

// console.log(window.zonesData);
createAndDisplayPoints();

document.addEventListener('keypress', function(event) {
    if (event.key === '1') {
        current = 0;
    } else if (event.key === '2') {
        current = 1;
    } else if (event.key === '3') {
        current = 2;
    } else if (event.key === '4') {
        current = 3;
    } else if (event.key = 'q') {
        current = 0;
        points = [{x: null, y: null}, {x: null, y: null}, {x: null, y: null}, {x: null, y: null}];
        for (let i = 1; i <= 4; i++) {
            document.getElementById(`x${i}`).value = null;
            document.getElementById(`y${i}`).value = null;
        }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        createAndDisplayPoints();
    }  
});