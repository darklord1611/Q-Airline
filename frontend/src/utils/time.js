const formatHour = function (isoString) {
    const date = new Date(isoString);
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    return `${hours}:${minutes}`;
}

// Format ISO date to "YYYY-MM-DD" for input[type="date"]
const formatDate = function (isoString) {
    if (!isoString) return "";
    const date = new Date(isoString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

// Helper function to combine checkin and time into ISO format
const assembleDateTime = function (date, time) {
    return `${date}T${time}:00.000Z`;
}

export default { formatHour, formatDate, assembleDateTime };