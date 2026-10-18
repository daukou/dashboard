function updateDashboard() {
    const now = new Date();
    
    // Čas (HH:MM)
    let hours = now.getHours().toString().padStart(2, '0');
    let minutes = now.getMinutes().toString().padStart(2, '0');
    document.getElementById('clock').textContent = `${hours}:${minutes}`;
    
    // Zoznamy pre anglické názvy dní a mesiacov
    const days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    
    // Dátum
    document.getElementById('day').textContent = days[now.getDay()];
    
    let dayNum = now.getDate();
    let month = months[now.getMonth()];
    let year = now.getFullYear();
    
    document.getElementById('date').textContent = `${dayNum} ${month} ${year}`;
}

updateDashboard();
setInterval(updateDashboard, 1000);
