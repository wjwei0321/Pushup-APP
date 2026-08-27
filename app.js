// State
let trainingData = [];
let currentDate = new Date(); // Month currently viewed
let selectedDate = new Date(); // Date currently selected
let apiUrl = 'https://script.google.com/macros/s/AKfycbzULLYM8Qow0Ra3ZO3qv6l6aw7kticNlaI0sr3PAkqHDQdKY50e3v8GN5av14V8Q46n/exec';
let selectedExerciseForLog = null;
let activeFilters = []; // empty means "Show All"

// Icons Dictionary — Caly-style bold silhouette figures
const EXERCISES = {
    'Push-up': '<svg width="100%" height="100%" viewBox="0 0 173 68"><mask id="mask_Push-up"><image width="173" height="68" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK0AAABECAYAAADz5LUJAAACQElEQVR4nO3c207DMBBF0Q7i/3/ZKBKVQmkT52LPnJm9HxFqc1k1rhPyeBARERERERERERERERFlzrw3gOrVWmu9v2tm/4yClkJi3cILWgqN9R1e0JIE1nVfI16UqA0CuwRakgK7BFqSC7QkNcougZakwC6BluQCLckFWpKaGiyBluQCLcn17b0BFOtPuglc2g+/geQ/17QOyDPntKBNVhuIZwsvaKm7NnGE28ILWgoHdQ8uaCkc0j24oKWwUCPAZcnLMRWY0WL1YGBVUNrvaDtrf0F7Y1WQek8RQHuxqlA94XLvwYUA6xNoT2IF7OdG378A2oOB1R8uaIuANYe7t0a85/KarNN2BFb/5TCe5VUQbBu8H72j6tHtePe6jLQ3HuCotUD70XOjzd4HgHXa4CdZ5iqVzZsz80XsJcDGj+lBIqyZVgm2YqRNBDb7Pj0rPafNdmJt8jx2/Z4zK4k2G9ZKYEvNaTNC9czz+QjpR9oKWC3x8lapkbYC1pmAvKGmRVsF6qx9jwR1XciNOlpVrDZoWrB3qdUbs+xIWxVq1mcZpEQb9QBmGmVNAGxotJEPWsbMYZ1XGq3CgYqU3TynVALrhlbl4FR69mwTOidTvgUqHZDo2Y3zzitgPVcQhoy0IP18op/H5gwY76WmKN2GFqh9wF5/7gXRhD8Al9ACNQ+E9GjBqo3VxLb38n8uAPbvyVcHcDZPB4fQAjYnVhPbl260gM2DtYkvQYa4Iha5yEhttYRWKdCKQX0EavnAeByrH5E6aFpqVIPOAAAAAElFTkSuQmCC" /></mask><rect width="173" height="68" fill="currentColor" mask="url(#mask_Push-up)" /></svg>',
    'Pull-up': '<svg width="100%" height="100%" viewBox="0 0 220 199"><mask id="mask_Pull-up"><image width="220" height="199" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANwAAADHCAYAAABySz3ZAAAFYUlEQVR4nO3d0XLbOAxA0TDT//9l7XgzStrtJnZiEQTAc547MSXzCrLcpi8vAAAAAAAAAABAIsdxHKvX0PGc3rwUMlYvoLOvNsMYw7nf8Ly+rl5AV/euvNWuzFkcxc+r4CZ49E3PvjmyORqcL8FdrMOmqH5ej8TvQer73Q4nGMZvnytNOAgkOAgkOAgkOAjUIrjsX3bCyUZN8LTUBWOf89piwkEVgiO98cNJlfH7WcEtlvG2h3l+TfzZW8l4Nb1y3S4M1xDcpr57gfj9z4vv59xSbubff7H55DSuOs0zENwmrght5s+bJdsaBbeBmZsu24bOTnA8TXSPE1xzYshFcI3/6lFkbLNfazT5vlJwTa2YbKbpfYKjvSPRgx3B0XZzZyS4hmz6vAT3JJub7xAcBBLcIrMec2eYuLPWMBp8NSA4tnAkuBDdCA4CCa7BVZM6BAeBBNdMhwcLnQmOy4n+c4JbwIZcc+4yfOYWHAQSXOGrZcYJanp/TXALZI41u6P4uRPcIh3/hfTM1zyK/JawewS3UJdNNNvR6BwJrnF4kVNuxmsdDS9IviT9oZkb4erNW+329Si23u8w4RK6+so+c4Nd+bOPhhPtvwSX2JUbcEZ0V8f2sgG3lIU2yFUb/Nm1Vw5tLP67poIreEVeFV7l0E6CK6xDdPeOpdoDkXsEV9jqzZNhAz3KuXpT4s3KLMNGyh5ehnM0kpyfFIuoLsOGyraxMp2XkeicpFlIdVk2F3lju0m1mA6El8NIFtop5aI6EN46I2lsN2kX1oXw4ozEoZ3SL7AL4c1TIbRTmYV2Ibw9QzuVW3AHotsvtFPZhXcgvH1CO5U/gA6E1z+0U5sD6UB4fUM7tTugDnYPbzQM7dT2wDrYMbzROLab1gfXxQ7hjeahnbY4yA66Rjc2Ce201cF20Cm8sVlsN35rVzFdNulochzfJTjCjU1juxFcQTtv2OoEB4EER6ix+XQWHAQSHAQSXFG735pVJTgIJDjCDFNZcBDJhINAgoNAgoNAgivMQ4h6BAeBBEcI0/iN4CCQ4CCQ4CCQ4CCQ4CCQ4Irz9K8WwTGdi8IHwUEgwUEgwUEgwUEgwUEgwUEgwTXgsXsdgmMqF4M/CQ4CCQ4CCQ4CCQ4CCQ4CCQ4CCQ4CCQ4CCQ4CCQ4CCQ4CCY6pjuM4nOIPgoNAgoNAgmvAbVsdgoNAgoNAgoNAgoNAgmM6D3U+CA4CCQ4CCa44t2u1CA4CCQ4CCY4Qbn3fCA4C/Yp8MWr9XwCm0vVMON75jzfmE1xhJlA9guNTJt71BEeYw+83ERxvTLMYJhwEEhwEElxRPg/V9OqN4ys+202YcKLbW2RUx+ZPKt1Sworgdr/yQPiEEx3/x+e467ilLMiFsVFw3sy9mF6xTDjCHRs/LxAcBBIcD3HreQ3BbUxE8QRXzM6ffzoQHAQSHEtuQY9NJ7XgIJDgNuWByRqCK2TX27DWwbnywTwmHKwKznTjHnvkOSYcyxwbfiZ9D86Vax/e68XBeQP2suNkyeJVbHyHWJ/jMxwEEtymMkyqEfj7MLMQXCGrN2iGSKsT3MYEFE9wxayaclfHOTa8nbwR3OYeCckkvI7gCqo+HUbx9T9DcHw5wUy3awmuqKpTYhRd91UEx6eTzHS7nuAKqzYtRrH1ziA43plo8wmuuCpTo8o6ZxMcn045kVxPcEwn3A+Ca+DqDW3KzSM4pjLd/iS4Jky5GgTHNKbb3wTXiCmXn+CayTJVsqwjG8HxJU8sryW4hlZPl9Wvn5nguMuUu47gmlo1ZUy3rwmOh5hy1xBcY9HTxnS7T3A8zJR7nuCai5o6pttjBMfTU05sLw/7B9McRUz1eEKsAAAAAElFTkSuQmCC" /></mask><rect width="220" height="199" fill="currentColor" mask="url(#mask_Pull-up)" /></svg>',
    'Lunge': '<svg width="100%" height="100%" viewBox="0 0 207 131"><mask id="mask_Lunge"><image width="207" height="131" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAM8AAACDCAYAAAAqG09IAAAEZ0lEQVR4nO3d23LbSAxFUSOl//9lpJjYVY5iSiTI7j4A9nqdicxLb4KSJfnjAwAAAAAAAAAAAAAA4B17+38ABbm77/03MzvUBfGgDX8RTCQk4kF5HojmSES/rj4oUD2cvcdh8qAkvymaVxOIyYNyfFA4z49NPEAwIG7bUIoPnDrPmDwowyeGsyEeIIh4UIJPnjob4gGCiAcIIh4giHiQni94vrMhHiDoEf2HwIxJcfSzNSvIbhhq8Yu3Vq8iWnXbRjwYxm9e1HsBEQ/K8MGT4KeIVgTEcx7cwhfdOq3EbRtSBmNP02fFthAP0k4Y+xYQ8UCSUjBK04fJg1TBKE0f3mGAf2wLMEs4K3+huv0sJg/STBmVl62/fibxNJU5mNUBEU8zlWJZ+c6D7z/LpnxFD7eHS1QOZvb73n76GUPi2dtgIhqrSyyRdXXl2Ow9/tR43m0Mxhzv6uzEejp6rI485u2LuMpnNdR1D0ZhHT1UFgAhnTteWM8y/B2UzghGd73IfSSBafTzsYAey/wBqKqI5jgmzwFdJhLh5HHLIlz2GfKkEe1dCAgn1/mXe85TdRq9C4Nw8rkcj8pJVwyJXxbXlnryKL6nLnIxUbkAZWICF8hL8aif9FnTKHIcFE4+rik5eWaEpH7hUGKfx3vkO5xTxZN58Txv++h35a54XDVecD/bTJ6zU6niyV7BRKbECMTzhGi0mVCMoW/PYYEBk7966s/X9QhdOTCWFb8FPn3bFj0Q/3xxAm9JQYDahfexeqcJCS1u20b/MpDbujrs5imhNnWGTp4rO1v9XrkyE/jTH3LxrPhijw4RbfuYff9McCqknDwjDmSHiLKxyV+q/lE9ntE7WSmibR9UF8WebNubJp4VV6IKEam7cl69+PmxCl+jm/Ukqb5Mf9f59OJfRfa4esVX2Dkm0T3HD+eUPGhKV3HV8GcE48UnT8k/q5jxl62ztjfTsTHx7SwZT8aFUo0nmv5RpeP5QkT5WIKLXot4skSkvG34X8tPks5+kk4UNXGl+3Q2pFFBzAh6dMx+cR+yXGxaTh7lE1bhjaJdtHrOA9yJeCBF5Q7gCOIRlGkBdUY8DY18TuWNnq8RD2RYsolLPKKyLaSOiAcIIh5hnaaPJdxX4sFtvNGLBRviaarbQh+BeMRlvJ3pso/EAwQRTwIZrsze8DaQeIAg4mlMYVpYgqm6h3iSyLzIqiIeIIh4ElGdPn7Dn9rMiHiAIOJpTuFFg6yIJ5nstzqV9oN4cIk3nlzEk1CFq3YFxIPprEj8xAMEEQ8QRDxJKdz6eODFAoXtvgvxAEHEAwQRD6axQrdsG+IBgogHId74nQVfiAdTWLFbtg3xAEHE01zFiTAL8WA4Kxoo8eA0Xiz4i3iAIOLBUFb0lm1DPI1FF3blIM4gHgxjxSMjHoRY8TCOIJ6kFF7xshcBdYjrsXoDkJs1iGQPk6epzov+LsQDBBEPEEQ8QBDxAEHEAwQRDxBEPA3xMvU9iAcIIh7gI+Y3QWYBhPQYShwAAAAASUVORK5CYII=" /></mask><rect width="207" height="131" fill="currentColor" mask="url(#mask_Lunge)" /></svg>',
    'Glute Band': '<svg width="100%" height="100%" viewBox="0 0 168 152"><mask id="mask_Glute_Band"><image width="168" height="152" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKgAAACYCAYAAABwMaIZAAADqUlEQVR4nO3b3W4aMRSF0TjK+7/yVFwgtRFtgfhnH3uty7aqPMM3PiaQjw8AAAAAAAB4pD38U8q4ruv619+31kq/xqUXf6rrP1HuFGu5BZ/sejPMypGWWuzJrg5xVgz1c/UCmB/nqP9zBIGGu4qENIpAD3YViF+ghwd0hUcq0FDp4cwiUD6SHwaBEk2ggZJ3tNkESjSBEr1rC5RoAiWaQIkmUKK/3STQQKmxrCBQogmUaAINNXPMt+AjhUCDtQnhJMd5I1CiCTRcG7jDpe+eNwItoA0IqUKcNyUWSb8vdVQJ867UYnk/1Gph3pVcNM+FWjVKqCP1i6pw41080b5WL4D1k60Fn1Xb/UYkL/IUKcetFtSCHTRASpiP1rM6VmfQxSGkxfnd6vUJ9NAXvspaBbpApThXr1mgk1WMc+XaBTpR5ThXXYNAJ9khzhXXIlCifSb8rGt3O+2es6/JDko0O+dgO+6evxs9fe2gRBPoQLvvnjMIlOiHUKBEE+ggxnsfAiX6YRQo0QQ6gPHej0CJfigFSjSBEk2gnZ18/rwGXLtAeSjlK5gCXSwlhFQC7Wi38d7eeHh63wOBEk2gRBNoJ++Mtl3Pn1fHMS9Qoh8igRJNoB0Y7+PGvECJHvMCJZpAf8h4H0ugRH+qJFCiCZRoAv2B086fbcGYFyjRBEo0gb7ptPG+aswLlGgCJZpA33DqeF8x5gUaYKd4exMo0QT6otPH++wxL9AAu/26ck8CJZpAX2C8zx/zAiWaQIk+Fwt08XhPCSF1zAuUaAIlmkCfcOq79+vJ6x55rQJdqPr5c8a1C5RoAh1gh/E++pqf/fcCHXDzd3ItPoYItLOTY24Drl2gHW/+Ky/Q6p1ppVfuk0A73diTd87v96HnfXJTF6m2g7ZFD6AdlGhfqxdwot67Z3uwu1Xbof/GDrqp1nkkrwpeoMW1zd+cCXRjbYN4BTrZLmfDWQRaWJu8Q654uAS6uVZ8zAuUaAKdaIfz5zX5GgR6wOhuhce8QIkmUKLHvEALvqjtjZFdecwD8A7b/uQx/33UVvrRU2ut3dc768gg0EkqhfisGZF6kzTBjnHOIlCiCZRoAh1s5/F+Tbg2gRJNoEQTKABsySdJxT4aTXynPnKNAg3/EUwb+OKv/grgM7xJOlgr8B1RgRJNoER/qiTQQ8+fVca8QIkmUKIJ9ODxXuEcKlCiHwaBEk2gHZ083kcRKF0fit7nUIESTaBhjPc/CbSTHX45rgWO+V+dCKTY9q/U8wAAAABJRU5ErkJggg==" /></mask><rect width="168" height="152" fill="currentColor" mask="url(#mask_Glute_Band)" /></svg>',
    'Polyquin Step-down': '<svg width="100%" height="100%" viewBox="0 0 440 710"><mask id="polyquinMask"><image width="440" height="710" href="data:image/png;base64,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" /></mask><rect width="440" height="710" fill="currentColor" mask="url(#polyquinMask)" /></svg>',
    'Hack Squat': '<svg width="100%" height="100%" viewBox="0 0 133 247"><mask id="mask_Hack_Squat"><image width="133" height="247" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIUAAAD3CAYAAAAzMJf2AAAFVklEQVR4nO3d7W7jOAxG4TCY+79lLoyFgaDOhy3J4kvqPH8W2Jk2meqYchIntUcy7u7bf83MWr5ut3/99v9fv5d/+P5//97o23vn6r8RRfiXKKI8o+8A9BAFDogCB0QBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB+c3d/BLGoG0ZbAGZ2+5oRReJpYDcFQhTJtwa7IQyiKHKuYAPjeI76Rog9eRz5vYmi0KMJH3QbRFH84WULoijGBwRIFAWnhHfeJlHcyJNtGzuiwAFRFOUdU4oobuJJt44NUeCAKHBAFDggChwQBQ6IAgdEgQOiuIlNuJbyLkRRlHVESRQ4IIqCW4h13i5R3MwSnlsQRTE2IEKiKDQtbNDtEMUklmgbSXNHq/AbrrMYHRxRJI/DeNtgLd4Rxp3bEZMiWSCW6NwEbxY563WaVFf0g0d6SN85dS76oSO9JO9UBi7+wSM9pO5MBp7gQ0d68YxmwQ8d6SVTpzKfuGAKE4NJIXYEu8DEIArxBYpAFIJBeHCMRIEDohA8UqPvA1EIBhGNKF4QxP+IQjgID7pPRCEaRCSiwMHyUTAljpaOgiDeWzYKgvhsySgI4rvloiCI35aKIlsQFnRtxVJR4Jxlosg2JSItEQVBXFM+iqxBWOC1mqWjyBpEtLJREES7slGgXckosk8JC37vR7kosgehoFQUBDFGmSiqBGG8bXCMKkGoSD8pCGK81FFUC8IEto70UeAeaaNgStzn3yN4MVtGZrUg1NjMhf+0mFfCqBiEiZxL7IbfmdZFO/ODqRiEYhRPlU+Y/fW1VYNQNCSKuxeschAmNiWGRDFywSovfib/1BewcigmOCWaJwVB1PZUPXIqTwh105+8OjNGVwjCRLcOiUmxYhDqnkq/0mCVIEx4SlyOgiDWcDoKglhHyDnFa2CrbBlZto7QRx+rxZDJpWpZSJ0pMeK6lOmT4tc1FDjn7M/v9e/1BjL8qqd3d4gwvi+W2i+ra/qiliuoCCNGSxjNY6ZlXBFGjjCmPTwiiDxhhL/2AT1TomBKxLuyBkwKaF5PkeHh3UqeGZ/v//b9Mry2EOXsAZNq+9gW/MyiE0afqUdVz2g/e0EO13n2HzApJsWVK7RGvgawqqlRtC7SvtC9b03EOSFH0oyFZRtpPyifkSeMr3eSUa8j/JziNQ7C0BAexV+jwuDco9ALYqMWk6nT/rN4Vg+CiZH0tQ+mw31aJmb4pLjzQ09WnxLWeH5W9n0fqwfRI3xSjMTJ5ZifRfjbBkfh5HLcwRH2jKby91td+u1j1c+4uPMACT3CeheQLeOeiSnxPMVVbBf3/kxCt49f11q++/NPX0Mo48icoO1bSe/iKpxTmJnNvB/DT9wfRc2Ow4JOeO+YkCnPKVSOViv6ULjkP+qdEYGY2Lvr74pymShaFs3Ef5UVUSThyadEiWc0lXiBIDZEgQOiGMSLTIkNUSRikx4CE8UALvAs6khE0ckLbRs7okjAJj9zShQdvNi2sSMKcRbw+gpRJPk4hZmIooEX3TZ2RCHKAl+WJ4qLvPC2sSMKHBDFBb7AlNgQhRATCGJDFCf5Qtd7EsUJXvwh6F9EIcCEpsSGKH7whbaNHVF84YttGzuiCGSCU2JDFB/4gtvGjigCmHAQG6J4wxc9l9gRxWQmPiU2RPGHLz4lNkQxmSf47Ubyo2ymqMUysS2FSSHAxaYHUQhxkTiIQpAHh0EUojwwDKIQ5kFhEIU4DwiDKIQfGkYhigRh+ORpQRRJwpiJKBKEYUL3BQAAAAAAAHhE+g9JstTfG7IL2AAAAABJRU5ErkJggg==" /></mask><rect width="133" height="247" fill="currentColor" mask="url(#mask_Hack_Squat)" /></svg>',
    'Romanian Deadlift': '<svg width="100%" height="100%" viewBox="0 0 186 247"><mask id="mask_Romanian_Deadlift"><image width="186" height="247" href="data:image/png;base64,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" /></mask><rect width="186" height="247" fill="currentColor" mask="url(#mask_Romanian_Deadlift)" /></svg>',
    'Slant Board Squat': '<svg width="100%" height="100%" viewBox="0 0 138 250"><mask id="mask_Slant_Board_Squat"><image width="138" height="250" href="data:image/png;base64,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" /></mask><rect width="138" height="250" fill="currentColor" mask="url(#mask_Slant_Board_Squat)" /></svg>'
};

// DOM Elements
const calendarDaysEl = document.getElementById('calendarDays');
const currentMonthYearEl = document.getElementById('currentMonthYear');
const selectedDateDisplay = document.getElementById('selectedDateDisplay');
const dailyLogList = document.getElementById('dailyLogList');
const addWorkoutModal = document.getElementById('addWorkoutModal');
const settingsModal = document.getElementById('settingsModal');
const exerciseDropdown = document.getElementById('exerciseDropdown');
const filterModal = document.getElementById('filterModal');
const headerFilterBtn = document.getElementById('headerFilterBtn');

// Init
document.addEventListener('DOMContentLoaded', () => {
    initExerciseListGrid();
    initFilterModal();
    renderCalendar();
    fetchData();
    initPullToRefresh();
    initScrollNav();

    // Close modals when clicking outside (using direct listeners for mobile compatibility)
    document.querySelectorAll('.modal').forEach(modal => {
        const dismissHandler = (e) => {
            if (e.target === modal) {
                if (modal.id === 'addWorkoutModal') closeAddWorkoutModal();
                if (modal.id === 'filterModal') closeFilterModal();
                if (modal.id === 'settingsModal') {
                    modal.classList.remove('show');
                    setTimeout(() => modal.style.display = 'none', 300);
                }
            }
        };
        modal.addEventListener('mousedown', dismissHandler);
        modal.addEventListener('touchstart', dismissHandler, {passive: true});
        
        // Swipe down to dismiss
        const content = modal.querySelector('.modal-content');
        if (content) {
            let startY = 0;
            let currentY = 0;
            
            content.addEventListener('touchstart', (e) => {
                const scroller = e.target.closest('[style*="overflow-y"]');
                if (scroller && scroller.scrollTop > 0) return; // Don't drag if scrolling inner content
                startY = e.touches[0].clientY;
                currentY = 0;
                content.style.transition = 'none';
            }, {passive: true});
            
            content.addEventListener('touchmove', (e) => {
                if (startY === 0) return;
                const deltaY = e.touches[0].clientY - startY;
                if (deltaY > 0) {
                    if (e.cancelable) e.preventDefault();
                    currentY = deltaY;
                    content.style.transform = `translateY(${deltaY}px)`;
                }
            }, {passive: false});
            
            content.addEventListener('touchend', () => {
                if (startY === 0) return;
                content.style.transition = 'transform 0.3s ease-out';
                if (currentY > 100) {
                    // Dismiss by driving the sheet down
                    content.style.transform = 'translateY(100%)';
                    
                    if (modal.id === 'addWorkoutModal') closeAddWorkoutModal();
                    if (modal.id === 'filterModal') closeFilterModal();
                    if (modal.id === 'settingsModal') {
                        modal.classList.remove('show');
                        setTimeout(() => modal.style.display = 'none', 300);
                    }
                    setTimeout(() => { content.style.transform = ''; }, 300);
                } else {
                    // Snap back
                    content.style.transform = '';
                }
                startY = 0;
            });
        }
    });
});

// Scroll to hide/show navigation
function initScrollNav() {
    let lastScrollY = window.scrollY;
    const nav = document.querySelector('.floating-nav');
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        // Hide when scrolling down, show when scrolling up
        if (currentScrollY > lastScrollY && currentScrollY > 50) {
            nav.classList.add('hidden');
        } else {
            nav.classList.remove('hidden');
        }
        
        lastScrollY = currentScrollY;
    }, { passive: true });
}

// Pull to refresh logic
function initPullToRefresh() {
    let touchStartY = 0;
    let isRefreshing = false;
    const ptr = document.getElementById('ptrIndicator');
    const homeView = document.getElementById('homeView');

    document.addEventListener('touchstart', e => {
        if (document.querySelector('.modal.show')) return;
        if (window.scrollY <= 0) {
            touchStartY = e.touches[0].clientY;
        }
    }, {passive: true});

    document.addEventListener('touchmove', e => {
        if (touchStartY === 0 || isRefreshing || document.querySelector('.modal.show')) return;
        const touchY = e.touches[0].clientY;
        const delta = touchY - touchStartY;
        
        // If we are at the top and pulling down
        if (delta > 0 && window.scrollY <= 0) {
            if (e.cancelable) {
                e.preventDefault(); // Stop native iOS rubber banding!
            }
            ptr.style.opacity = Math.min(delta / 100, 1);
            homeView.style.transform = `translateY(${Math.min(delta / 2, 80)}px)`;
            ptr.style.transform = `rotate(${delta}deg)`;
        }
    }, {passive: false});

    document.addEventListener('touchend', e => {
        if (touchStartY === 0 || isRefreshing) return;
        const touchY = e.changedTouches[0].clientY;
        const delta = touchY - touchStartY;
        
        if (delta > 100 && window.scrollY <= 0) {
            isRefreshing = true;
            ptr.classList.add('spinning');
            homeView.style.transform = `translateY(60px)`;
            
            fetchData().then(() => {
                isRefreshing = false;
                ptr.classList.remove('spinning');
                homeView.style.transform = `translateY(0)`;
                ptr.style.opacity = 0;
            });
        } else {
            homeView.style.transform = `translateY(0)`;
            ptr.style.opacity = 0;
        }
        touchStartY = 0;
    });
}

function initExerciseListGrid() {
    const grid = document.getElementById('exerciseListGrid');
    grid.innerHTML = '';
    Object.keys(EXERCISES).forEach(ex => {
        const btn = document.createElement('div');
        btn.style.cssText = 'border: 1.5px solid var(--text-primary); border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 20px; cursor: pointer; background: var(--card-bg); font-weight: 700; font-size: 1.2rem; transition: transform 0.1s;';
        btn.innerHTML = `<div style="width:32px; height:32px; display:flex; align-items:center; justify-content:center;">${EXERCISES[ex]}</div> <span>${ex}</span>`;
        btn.onclick = () => selectExercise(ex);
        btn.onmousedown = () => btn.style.transform = 'scale(0.97)';
        btn.onmouseup = () => btn.style.transform = 'scale(1)';
        btn.ontouchstart = () => btn.style.transform = 'scale(0.97)';
        btn.ontouchend = () => btn.style.transform = 'scale(1)';
        grid.appendChild(btn);
    });
}

// Filter Logic
function initFilterModal() {
    const list = document.getElementById('filterList');
    list.innerHTML = '';
    
    // Add "Show All"
    const allDiv = document.createElement('div');
    allDiv.className = 'filter-item selected';
    allDiv.id = 'filterItem_ALL';
    allDiv.innerHTML = `<span>Show All</span> <div class="filter-checkbox"></div>`;
    allDiv.onclick = () => toggleFilter('ALL');
    list.appendChild(allDiv);

    // Add Exercises
    Object.keys(EXERCISES).forEach(ex => {
        const exDiv = document.createElement('div');
        exDiv.className = 'filter-item';
        exDiv.id = `filterItem_${ex.replace(/\s+/g, '_')}`;
        exDiv.innerHTML = `
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:24px; height:24px;">${EXERCISES[ex]}</div>
                <span>${ex}</span>
            </div>
            <div class="filter-checkbox"></div>
        `;
        exDiv.onclick = () => toggleFilter(ex);
        list.appendChild(exDiv);
    });
}

function openFilterModal() {
    filterModal.style.display = 'flex';
    setTimeout(() => filterModal.classList.add('show'), 10);
}

function closeFilterModal() {
    filterModal.classList.remove('show');
    setTimeout(() => filterModal.style.display = 'none', 300);
}

function toggleFilter(type) {
    if (type === 'ALL') {
        activeFilters = [];
    } else {
        if (activeFilters.includes(type)) {
            activeFilters = activeFilters.filter(f => f !== type);
        } else {
            activeFilters.push(type);
        }
    }
    
    // Update UI checkmarks
    document.getElementById('filterItem_ALL').classList.toggle('selected', activeFilters.length === 0);
    Object.keys(EXERCISES).forEach(ex => {
        const item = document.getElementById(`filterItem_${ex.replace(/\s+/g, '_')}`);
        if (item) {
            item.classList.toggle('selected', activeFilters.includes(ex));
        }
    });

    // Update Header Button
    if (activeFilters.length === 0) {
        headerFilterBtn.classList.remove('active');
        headerFilterBtn.innerHTML = 'A';
    } else if (activeFilters.length === 1) {
        headerFilterBtn.classList.add('active');
        headerFilterBtn.innerHTML = `<div style="width:20px;height:20px;display:flex;">${EXERCISES[activeFilters[0]]}</div>`;
    } else {
        headerFilterBtn.classList.add('active');
        headerFilterBtn.innerHTML = activeFilters.length;
    }

    renderCalendar();
    renderDailyLog();
}

// Data Fetching
async function fetchData() {
    try {
        // 加入時間戳記避免瀏覽器快取 (Cache-busting)
        const timestamp = new Date().getTime();
        const res = await fetch(`${apiUrl}?action=get&t=${timestamp}`);
        const json = await res.json();
        if (json.status === 'success') {
            // Data is [Date, Type, Set1, Set2, Set3, Set4, Set5, Set6]
            trainingData = json.data.filter(row => row[0]).map((row, index) => {
                const dateObj = new Date(row[0]);
                const dateStr = `${dateObj.getFullYear()}/${String(dateObj.getMonth()+1).padStart(2, '0')}/${String(dateObj.getDate()).padStart(2, '0')}`;
                
                // Parse sets
                let sets = [];
                for(let i = 2; i <= 7; i++) {
                    if (row[i] && !isNaN(parseInt(row[i]))) {
                        sets.push(parseInt(row[i]));
                    }
                }
                
                return {
                    rowIndex: index + 2, // Sheet row
                    dateStr: dateStr,
                    type: row[1],
                    sets: sets
                };
            });


            renderCalendar(); // Re-render to show indicators
            renderDailyLog(); // Re-render list
        }
    } catch (e) {
        console.error(e);
    }
}

// Calendar Logic
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    currentMonthYearEl.textContent = `${MONTH_NAMES[month]} ${year}`;
    
    calendarDaysEl.innerHTML = '';
    
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // Empty cells before month
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement('div');
        cell.className = 'day-cell empty';
        calendarDaysEl.appendChild(cell);
    }
    
    // Days
    const today = new Date();
    for (let i = 1; i <= daysInMonth; i++) {
        const cell = document.createElement('div');
        cell.className = 'day-cell';
        
        const numSpan = document.createElement('span');
        numSpan.className = 'day-number';
        numSpan.textContent = i;
        
        if (year === today.getFullYear() && month === today.getMonth() && i === today.getDate()) {
            numSpan.classList.add('today');
        }
        cell.appendChild(numSpan);
        
        // Check if selected
        if (year === selectedDate.getFullYear() && month === selectedDate.getMonth() && i === selectedDate.getDate()) {
            cell.classList.add('selected');
        }
        
        // Check for data
        const dateStr = `${year}/${String(month+1).padStart(2, '0')}/${String(i).padStart(2, '0')}`;
        let dayData = trainingData.filter(d => d.dateStr === dateStr);
        
        if (activeFilters.length > 0) {
            dayData = dayData.filter(d => activeFilters.includes(d.type));
        }
        
        if (dayData.length > 0) {
            const container = document.createElement('div');
            container.className = 'day-icons-container';
            
            // Group by exercise type
            const exerciseSets = {};
            dayData.forEach(d => {
                if (!exerciseSets[d.type]) exerciseSets[d.type] = 0;
                exerciseSets[d.type] += d.sets.length;
            });

            const distinctCount = Object.keys(exerciseSets).length;
            Object.keys(exerciseSets).forEach(exType => {
                const sets = exerciseSets[exType];
                
                // Scale proportion according to quantity
                let size = 16 + (sets * 3); 
                if (size > 28) size = 28; // Max size to prevent overflow
                
                if (distinctCount > 2) size = Math.min(size, 16);
                else if (distinctCount > 1) size = Math.min(size, 20);
                
                const ind = document.createElement('div');
                ind.className = 'day-indicator';
                ind.style.width = `${size}px`;
                ind.style.height = `${size}px`;
                ind.innerHTML = EXERCISES[exType];
                container.appendChild(ind);
            });
            cell.appendChild(container);
        }
        
        cell.onclick = () => {
            selectedDate = new Date(year, month, i);
            renderCalendar();
            renderDailyLog();
        };
        
        calendarDaysEl.appendChild(cell);
    }
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
}
function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
}

// Daily Log Logic
function renderDailyLog() {
    const month = MONTH_NAMES[selectedDate.getMonth()].substring(0, 3);
    selectedDateDisplay.textContent = `${month} ${selectedDate.getDate()}`;
    
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    let dayData = trainingData.filter(d => d.dateStr === dateStr);
    
    if (activeFilters.length > 0) {
        dayData = dayData.filter(d => activeFilters.includes(d.type));
    }
    
    dailyLogList.innerHTML = '';
    openSwipeCard = null; // Clear any open swipe state
    
    if (dayData.length === 0) {
        dailyLogList.innerHTML = '<div style="text-align:center; padding: 20px; color: #aaa;">No workouts logged today.</div>';
        return;
    }
    
    dayData.forEach(entry => {
        entry.sets.forEach((repCount, setIndex) => {
            const card = document.createElement('div');
            card.className = 'log-card';
            
            const iconSvg = EXERCISES[entry.type] || EXERCISES['Push-up'];
            
            card.innerHTML = `
                <div class="log-card-actions" style="position: absolute; top: 0; right: 0; height: 100%; display: flex; z-index: 1;">
                    <button class="edit-swipe-btn" onclick="enableEditMode(this, ${entry.rowIndex}, ${setIndex})" style="background: var(--text-secondary); color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    </button>
                    <button class="delete-swipe-btn" onclick="confirmDeleteSet(${entry.rowIndex}, ${setIndex})" style="background: #e74c3c; color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer; border-radius: 0 16px 16px 0;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    </button>
                </div>
                <div class="log-card-content" style="position: relative; z-index: 2; background: white; padding: 12px 16px; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03); transition: transform 0.2s ease-out; transform: translateX(0);">
                    <div class="log-card-left" style="display: flex; align-items: center; gap: 12px;">
                        <div class="log-icon">${iconSvg}</div>
                        <div class="log-details" style="display: flex; flex-direction: column;">
                            <span class="log-title" style="font-weight: 700; font-size: 1rem;">${entry.type}</span>
                            <span class="log-time" style="font-size: 0.8rem; color: var(--text-secondary);">Set ${setIndex + 1}</span>
                        </div>
                    </div>
                    <input type="number" class="inline-edit-input" data-row="${entry.rowIndex}" data-set="${setIndex}" value="${repCount}" readonly onblur="saveInlineEdit(this)" onkeydown="if(event.key==='Enter') this.blur();" style="font-size: 1.5rem; font-weight: 800; border: none; background: transparent; width: 70px; text-align: right; color: var(--text-primary); font-family: inherit; outline: none; padding: 0;">
                </div>
            `;
            
            initSwipeActions(card);
            
            dailyLogList.appendChild(card);
        });
    });
}

// Inline Edit & Swipe Logic
let openSwipeCard = null;

function closeOpenSwipeCard() {
    if (openSwipeCard) {
        openSwipeCard.style.transition = 'transform 0.2s ease-out';
        openSwipeCard.style.transform = 'translateX(0px)';
        // Reset local state if possible, though touchstart will reset startX anyway
        openSwipeCard = null;
    }
}

// Global listener to close open swipe actions when tapping outside
document.addEventListener('touchstart', e => {
    if (openSwipeCard && !openSwipeCard.parentElement.contains(e.target)) {
        closeOpenSwipeCard();
    }
});
document.addEventListener('mousedown', e => {
    if (openSwipeCard && !openSwipeCard.parentElement.contains(e.target)) {
        closeOpenSwipeCard();
    }
});

function initSwipeActions(card) {
    const content = card.querySelector('.log-card-content');
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    // Total width of actions on the right is 140px (70 + 70)
    const actionWidth = -140;

    content.addEventListener('touchstart', e => {
        if (e.target.tagName.toLowerCase() === 'input') return; // Don't drag if focusing input
        
        // If another card is open, close it
        if (openSwipeCard && openSwipeCard !== content) {
            closeOpenSwipeCard();
        }
        
        // If this card is already open and we touch it again, don't necessarily close it here,
        // we let touchmove/touchend handle the swipe back, or if it's a tap, it might just stay open
        // Wait, if it's open, currentX should reflect that.
        // We can parse the current transform to get currentX, or just assume it from state
        const matrix = new WebKitCSSMatrix(window.getComputedStyle(content).transform);
        currentX = matrix.m41; // get actual translateX
        
        startX = e.touches[0].clientX - currentX; 
        isDragging = true;
        content.style.transition = 'none';
    }, {passive: true});
    
    content.addEventListener('touchmove', e => {
        if (!isDragging) return;
        const x = e.touches[0].clientX;
        const diff = x - startX;
        
        // If swiping left, allow up to actionWidth, with some rubber-banding
        if (diff < 0) {
            currentX = Math.max(diff, actionWidth - 20);
        } else {
            // Swiping right (closing)
            currentX = Math.min(diff, 20); // Rubber band right
        }
        
        content.style.transform = `translateX(${currentX}px)`;
    }, {passive: true});
    
    content.addEventListener('touchend', () => {
        if (!isDragging) return;
        isDragging = false;
        content.style.transition = 'transform 0.2s ease-out';
        
        // Snap open or close
        if (currentX < actionWidth / 2) {
            currentX = actionWidth;
            openSwipeCard = content;
        } else {
            currentX = 0;
            if (openSwipeCard === content) openSwipeCard = null;
        }
        content.style.transform = `translateX(${currentX}px)`;
    });
}

function enableEditMode(btn, rowIndex, setIndex) {
    // Snap card back
    closeOpenSwipeCard();
    const card = btn.closest('.log-card');
    const content = card.querySelector('.log-card-content');
    
    // Focus input
    const input = content.querySelector('.inline-edit-input');
    input.removeAttribute('readonly');
    input.style.borderBottom = '2px solid var(--accent-color)';
    input.style.borderRadius = '0';
    input.focus();
    
    // Move cursor to end
    const val = input.value;
    input.value = '';
    input.value = val;
}

function saveInlineEdit(input) {
    input.setAttribute('readonly', 'true');
    input.style.borderBottom = 'none';
    
    const rowIndex = parseInt(input.getAttribute('data-row'));
    const setIndex = parseInt(input.getAttribute('data-set'));
    const newVal = parseInt(input.value);
    
    if (isNaN(newVal) || newVal <= 0) {
        showToast('Invalid number. Reverting...');
        renderDailyLog(); // Revert UI to old state
        return;
    }
    
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    // Only update if changed
    if (entry.sets[setIndex] !== newVal) {
        entry.sets[setIndex] = newVal;
        updateSetOnBackend(entry);
    }
}

function confirmDeleteSet(rowIndex, setIndex) {
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    if (confirm(`Delete Set ${setIndex + 1}?`)) {
        entry.sets.splice(setIndex, 1);
        updateSetOnBackend(entry);
    } else {
        // Snap back
        renderDailyLog();
    }
}

async function updateSetOnBackend(entry) {
    // Optimistic UI Update
    renderDailyLog();
    showToast('Updating...');
    
    // If no sets left, delete the entire row
    const payload = {
        action: entry.sets.length === 0 ? 'delete' : 'edit',
        rowIndex: entry.rowIndex - 2, // Backend expects 0-index based on row 2
        reps: entry.sets
    };
    
    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        
        if (result.status === 'success') {
            showToast('Updated successfully!');
            fetchData();
        } else {
            showToast('Error: ' + result.message);
        }
    } catch (e) {
        console.error(e);
        showToast('Error updating record');
    }
}

// Modal Logic
function openAddWorkoutModal() {
    selectedExerciseForLog = null;
    document.getElementById('stepSelectExercise').style.display = 'flex';
    document.getElementById('stepInputReps').style.display = 'none';
    document.getElementById('workoutRepsDisplay').textContent = '0';
    
    addWorkoutModal.style.display = 'flex';
    setTimeout(() => addWorkoutModal.classList.add('show'), 10);
}

function closeAddWorkoutModal() {
    addWorkoutModal.classList.remove('show');
    setTimeout(() => addWorkoutModal.style.display = 'none', 300);
}

function selectExercise(type) {
    selectedExerciseForLog = type;
    document.getElementById('selectedExerciseTitle').textContent = type;
    
    const dateOptions = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
    document.getElementById('selectedExerciseDate').textContent = selectedDate.toLocaleDateString('en-US', dateOptions);
    
    document.getElementById('selectedExerciseIconLarge').innerHTML = `<div style="width: 140px; height: 140px; background: var(--accent-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; padding: 28px; box-sizing: border-box;">${EXERCISES[type]}</div>`;
    
    updateModalStats();

    document.getElementById('stepSelectExercise').style.display = 'none';
    document.getElementById('stepInputReps').style.display = 'flex';
}

function addReps(amount) {
    const display = document.getElementById('workoutRepsDisplay');
    let current = parseInt(display.textContent) || 0;
    display.textContent = current + amount;
}

function clearReps() {
    document.getElementById('workoutRepsDisplay').textContent = '0';
}

function backToExerciseSelection() {
    document.getElementById('stepInputReps').style.display = 'none';
    document.getElementById('stepSelectExercise').style.display = 'flex';
}

function updateModalStats() {
    if (!selectedExerciseForLog) return;
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    const dayRow = trainingData.find(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    
    let sets = 0;
    let totalReps = 0;
    if (dayRow) {
        sets = dayRow.sets.length;
        totalReps = dayRow.sets.reduce((sum, val) => sum + val, 0);
    }
    
    document.getElementById('modalSetsToday').textContent = sets;
    document.getElementById('modalTotalRepsToday').textContent = totalReps;
}

async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsDisplay').textContent;
    if (!reps || isNaN(reps) || parseInt(reps) <= 0) return alert('Please enter valid reps.');
    
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    
    const payload = {
        action: 'log',
        date: dateStr,
        type: selectedExerciseForLog,
        exerciseType: selectedExerciseForLog,
        count: parseInt(reps)
    };
    
    // Optimistic UI Update
    let dayRow = trainingData.find(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    if (dayRow) {
        if(dayRow.sets.length >= 6) {
            alert('Max 6 sets allowed per day per exercise.');
            return;
        }
        dayRow.sets.push(parseInt(reps));
    } else {
        trainingData.push({
            rowIndex: -1,
            dateStr: dateStr,
            type: selectedExerciseForLog,
            sets: [parseInt(reps)]
        });
    }
    
    // Update UI and keep modal open for continuous input
    clearReps();
    updateModalStats();
    renderCalendar();
    renderDailyLog();
    showToast("Logged!");
    
    try {
        await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        fetchData(); // Sync exact state
    } catch (e) {
        console.error(e);
    }
}

// Settings
function saveSettings() {
    const val = document.getElementById('apiUrl').value.trim();
    if (val) {
        apiUrl = val;
        localStorage.setItem('pushup_apiUrl', apiUrl);
        settingsModal.classList.remove('show');
        setTimeout(() => settingsModal.style.display = 'none', 300);
        fetchData();
    }
}

// Utils
// Stats State
let currentStatsTimeFilter = '3M';
let currentStatsChartType = 'line';
let currentStatsExercise = 'All';
let statsChartInstance = null;

function switchView(view) {
    document.getElementById('homeView').style.display = view === 'home' ? 'block' : 'none';
    document.getElementById('statsView').style.display = view === 'stats' ? 'block' : 'none';
    
    const navItems = document.querySelectorAll('.floating-nav .nav-item:not(.add-btn)');
    navItems[0].classList.toggle('active', view === 'home');
    navItems[1].classList.toggle('active', view === 'stats');
    
    if (view === 'stats') {
        renderStats();
    }
}

function showToast(msg = "Logged successfully!") {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}

// --- Statistics Logic ---

function setTimeFilter(filter) {
    currentStatsTimeFilter = filter;
    renderStats();
}

function toggleChartType(type) {
    currentStatsChartType = type;
    renderStats();
}

function setStatsExercise(ex) {
    currentStatsExercise = ex;
    renderStats();
}

function renderStats() {
    // 1. Update UI active states
    document.querySelectorAll('.stats-time-filter .time-filter-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tf-' + currentStatsTimeFilter)?.classList.add('active');
    
    document.getElementById('btnLineChart').classList.toggle('active', currentStatsChartType === 'line');
    document.getElementById('btnBarChart').classList.toggle('active', currentStatsChartType === 'bar');
    
    // 2. Render Exercise Filter Pills
    const filterContainer = document.getElementById('statsExerciseFilter');
    const allEx = [...new Set(trainingData.map(d => d.type))];
    const exList = ['All', ...allEx];
    
    if (!exList.includes(currentStatsExercise)) {
        currentStatsExercise = 'All';
    }
    
    filterContainer.innerHTML = '';
    exList.forEach(ex => {
        const pill = document.createElement('div');
        pill.className = 'stats-exercise-pill' + (currentStatsExercise === ex ? ' active' : '');
        pill.textContent = ex === 'All' ? '全部' : ex;
        pill.onclick = () => setStatsExercise(ex);
        filterContainer.appendChild(pill);
    });
    
    // 3. Filter data by date and exercise
    const now = new Date();
    let cutoffDate = new Date(0);
    if (currentStatsTimeFilter === '3M') {
        cutoffDate = new Date(now.getFullYear(), now.getMonth() - 3, now.getDate());
    } else if (currentStatsTimeFilter === '6M') {
        cutoffDate = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate());
    } else if (currentStatsTimeFilter === '1Y') {
        cutoffDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
    }
    
    let filteredData = trainingData.filter(d => new Date(d.dateStr) >= cutoffDate);
    
    if (currentStatsExercise !== 'All') {
        filteredData = filteredData.filter(d => d.type === currentStatsExercise);
    }
    
    // 4. Aggregate Data by Date
    const dailyTotals = {};
    let grandTotal = 0;
    
    filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = {};
        const sum = d.sets.reduce((a, b) => a + b, 0);
        dailyTotals[d.dateStr][d.type] = (dailyTotals[d.dateStr][d.type] || 0) + sum;
        grandTotal += sum;
    });
    
    document.getElementById('statsTotalNumber').textContent = grandTotal.toLocaleString();
    
    // 5. Prepare Chart.js datasets
    const sortedDates = Object.keys(dailyTotals).sort((a, b) => new Date(a) - new Date(b));
    const labels = sortedDates.map(dateStr => {
        const d = new Date(dateStr);
        return d.getDate() + '/' + (d.getMonth() + 1);
    });
    
    const datasets = [];
    const CHART_COLORS = [
        { line: '#f39c12', fill: 'rgba(243, 156, 18, 0.15)' },
        { line: '#3498db', fill: 'rgba(52, 152, 219, 0.15)' },
        { line: '#e74c3c', fill: 'rgba(231, 76, 60, 0.15)' },
        { line: '#2ecc71', fill: 'rgba(46, 204, 113, 0.15)' },
        { line: '#9b59b6', fill: 'rgba(155, 89, 182, 0.15)' },
    ];
    
    if (currentStatsExercise !== 'All') {
        const data = sortedDates.map(dateStr => dailyTotals[dateStr][currentStatsExercise] || 0);
        datasets.push({
            label: currentStatsExercise,
            data: data,
            borderColor: '#f39c12',
            backgroundColor: 'USE_GRADIENT',
            fill: currentStatsChartType === 'line',
            tension: 0.45,
            borderWidth: currentStatsChartType === 'line' ? 2.5 : 0,
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: '#f39c12',
            pointHoverBorderColor: '#fff',
            pointHoverBorderWidth: 2,
            borderRadius: currentStatsChartType === 'bar' ? 6 : 0,
            barPercentage: 0.6,
        });
    } else {
        allEx.forEach((ex, i) => {
            const c = CHART_COLORS[i % CHART_COLORS.length];
            const data = sortedDates.map(dateStr => dailyTotals[dateStr][ex] || 0);
            datasets.push({
                label: ex,
                data: data,
                borderColor: c.line,
                backgroundColor: currentStatsChartType === 'line' ? 'transparent' : c.line,
                fill: false,
                tension: 0.45,
                borderWidth: currentStatsChartType === 'line' ? 2 : 0,
                pointRadius: 0,
                pointHoverRadius: 4,
                pointHoverBackgroundColor: c.line,
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                borderRadius: currentStatsChartType === 'bar' ? 6 : 0,
                barPercentage: 0.6,
            });
        });
    }
    
    // 6. Render Chart
    const ctx = document.getElementById('statsChart').getContext('2d');
    if (statsChartInstance) {
        statsChartInstance.destroy();
    }
    
    // Create gradient for single exercise line chart
    if (currentStatsExercise !== 'All' && currentStatsChartType === 'line' && datasets.length > 0) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 260);
        gradient.addColorStop(0, 'rgba(243, 156, 18, 0.3)');
        gradient.addColorStop(0.5, 'rgba(243, 156, 18, 0.08)');
        gradient.addColorStop(1, 'rgba(243, 156, 18, 0)');
        datasets[0].backgroundColor = gradient;
    } else if (currentStatsExercise !== 'All' && currentStatsChartType === 'bar' && datasets.length > 0) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 260);
        gradient.addColorStop(0, 'rgba(243, 156, 18, 0.9)');
        gradient.addColorStop(1, 'rgba(243, 156, 18, 0.5)');
        datasets[0].backgroundColor = gradient;
    }
    
    statsChartInstance = new Chart(ctx, {
        type: currentStatsChartType,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 600,
                easing: 'easeOutQuart'
            },
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: currentStatsExercise === 'All' && allEx.length > 1,
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 6,
                        padding: 16,
                        font: { family: 'Outfit', size: 12, weight: '600' },
                        color: '#999'
                    }
                },
                tooltip: {
                    backgroundColor: '#1a1a2e',
                    titleFont: { size: 12, family: 'Outfit', weight: '500' },
                    bodyFont: { size: 14, family: 'Outfit', weight: '700' },
                    titleColor: 'rgba(255,255,255,0.6)',
                    bodyColor: '#fff',
                    padding: { top: 10, bottom: 10, left: 14, right: 14 },
                    cornerRadius: 10,
                    displayColors: currentStatsExercise === 'All',
                    boxPadding: 4,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' reps';
                        }
                    }
                }
            },
            scales: {
                x: {
                    stacked: currentStatsChartType === 'bar',
                    grid: { display: false },
                    border: { display: false },
                    ticks: {
                        maxTicksLimit: 6,
                        font: { family: 'Outfit', size: 11, weight: '500' },
                        color: '#bbb',
                        padding: 8
                    }
                },
                y: {
                    stacked: currentStatsChartType === 'bar',
                    beginAtZero: true,
                    border: { display: false },
                    grid: {
                        color: 'rgba(0,0,0,0.04)',
                        drawBorder: false,
                    },
                    ticks: {
                        maxTicksLimit: 5,
                        font: { family: 'Outfit', size: 11, weight: '500' },
                        color: '#bbb',
                        padding: 8
                    }
                }
            }
        }
    });
}
