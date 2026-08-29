const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(
`            trainingData = json.data.map(row => {
                return {
                    dateStr: row[0],
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: row[3] || '',
                    rowIndex: row[4]
                };
            });`,
`            trainingData = json.data.map(row => {
                // Normalize date string in case backend sends ISO string
                let dStr = row[0];
                if (dStr && dStr.includes('T')) {
                    const d = new Date(dStr);
                    dStr = \`\${d.getFullYear()}/\${String(d.getMonth()+1).padStart(2, '0')}/\${String(d.getDate()).padStart(2, '0')}\`;
                } else if (dStr && dStr.includes('-')) {
                    dStr = dStr.replace(/-/g, '/'); // fallback normalization
                }
                
                // Normalize time string in case backend sends ISO string (e.g. 1899-12-30T10:00:00.000Z)
                let tStr = row[3] || '';
                if (tStr && tStr.includes('T')) {
                    const d = new Date(tStr);
                    tStr = \`\${String(d.getHours()).padStart(2, '0')}:\${String(d.getMinutes()).padStart(2, '0')}\`;
                }
                
                return {
                    dateStr: dStr,
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: tStr,
                    rowIndex: row[4]
                };
            });`
)

fs.writeFileSync('app.js', js, 'utf8');
