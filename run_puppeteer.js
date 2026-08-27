const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.error('BROWSER ERROR:', err.message));
  
  await page.goto('file://' + __dirname + '/index.html', { waitUntil: 'load' });
  
  const bodySize = await page.evaluate(() => {
      const container = document.querySelector('.container');
      const homeView = document.getElementById('homeView');
      return {
          bodyW: document.body.clientWidth,
          bodyH: document.body.clientHeight,
          containerW: container ? container.clientWidth : 0,
          containerH: container ? container.clientHeight : 0,
          containerDisplay: container ? window.getComputedStyle(container).display : 'N/A',
          homeDisplay: homeView ? window.getComputedStyle(homeView).display : 'N/A',
          homeH: homeView ? homeView.clientHeight : 0
      };
  });
  console.log('Metrics:', bodySize);
  
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
