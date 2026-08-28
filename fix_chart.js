const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

const lines = js.split('\n');
let yStartIndex = -1;
let yEndIndex = -1;

for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('y: {') && lines[i].includes('position')) {
        yStartIndex = i;
        for (let j = i + 1; j < i + 15; j++) {
            if (lines[j].includes('}')) {
                // Check if it's the closing brace for y: {
                if (lines[j].trim() === '}' || lines[j].trim() === '},') {
                    yEndIndex = j;
                    break;
                }
            }
        }
        break;
    }
}

if (yStartIndex !== -1 && yEndIndex !== -1) {
    const newYConfig = [
        "                y: {",
        "                    position: 'left',",
        "                    stacked: currentStatsChartType === 'bar',",
        "                    beginAtZero: true,",
        "                    border: { display: false },",
        "                    grid: { display: false, drawBorder: false, drawTicks: false },",
        "                    ticks: {",
        "                        display: false,",
        "                        maxTicksLimit: 5",
        "                    }",
        "                }"
    ].join('\n');
    
    lines.splice(yStartIndex, yEndIndex - yStartIndex + 1, newYConfig);
    fs.writeFileSync('app.js', lines.join('\n'));
    console.log("Successfully replaced Y-axis config.");
} else {
    console.log("Could not find Y-axis config.");
}
