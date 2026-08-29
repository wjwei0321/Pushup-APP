const fs = require('fs');

const mockData = {
    "status": "success",
    "data": [
        [
            "2026-08-28T16:00:00.000Z",
            "Push-up",
            10,
            "1899-12-30T02:00:00.000Z",
            363
        ]
    ],
    "username": "atw007wj@gmail.com"
};

// Mocks
global.window = { addEventListener: ()=>{}, scrollY: 0 };
global.localStorage = { getItem: ()=>null, setItem: ()=>{} };
global.navigator = { userAgent: '' };

const document = {
    addEventListener: () => {},
    getElementById: (id) => ({ 
        textContent: '', 
        value: '',
        style: {}, 
        classList: { add: ()=>{}, remove: ()=>{}, toggle: ()=>{} },
        innerHTML: ''
    }),
    createElement: (tag) => ({ 
        className: '', 
        style: {}, 
        appendChild: () => {},
        classList: { add: ()=>{}, remove: ()=>{}, toggle: ()=>{} },
        innerHTML: '',
        textContent: ''
    }),
    querySelector: () => ({ style: {}, classList: { add: ()=>{}, remove: ()=>{} } }),
    querySelectorAll: () => []
};
global.document = document;
global.fetch = async () => ({ json: async () => mockData });

let js = fs.readFileSync('app.js', 'utf8');

try {
    eval(js);
    global.userEmail = "atw007wj@gmail.com";
    
    fetchData().then(() => {
        console.log("fetchData finished. trainingData:", trainingData.length);
        console.log("SUCCESS!");
    }).catch(e => {
        console.error("RUNTIME ERROR:", e);
    });
} catch(e) {
    console.error("EVAL ERROR:", e);
}
