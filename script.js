function updateClock() {
    const now = new Date();
    
    // Získanie hodín, minút a sekúnd a pridanie nuly na začiatok, ak sú menšie ako 10
    let hours = now.getHours().toString().padStart(2, '0');
    let minutes = now.getMinutes().toString().padStart(2, '0');
    let seconds = now.getSeconds().toString().padStart(2, '0');
    
    // Spojenie do formátu HH:MM:SS
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // Zapísanie času do HTML
    document.getElementById('clock').textContent = timeString;
}

// Spustíme funkciu hneď po načítaní stránky
updateClock();

// Nastavíme opakované spúšťanie funkcie každých 1000 milisekúnd (1 sekunda)
setInterval(updateClock, 1000);
