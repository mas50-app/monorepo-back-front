

export function formatDate(date) {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString();
    return `${day}-${month}-${year}`;
}


export function formatDate1(date){
    const partes = date.split('-');
    const day = parseInt(partes[0]);
    const month = parseInt(partes[1]);
    const year = parseInt(partes[2]);

    const nombreMes = new Intl.DateTimeFormat('es-ES', { month: 'long' }).format(new Date(year, month - 1, day)); // Obtenemos el nombre del mes en español
    return `${day} ${nombreMes} ${year}`
}