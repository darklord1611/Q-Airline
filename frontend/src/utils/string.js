import { camelCase } from 'lodash';

function keysToCamelCase(obj) {
    if (Array.isArray(obj)) {
        return obj.map((v) => keysToCamelCase(v));
    } else if (obj !== null && typeof obj === 'object') {
        return Object.keys(obj).reduce((acc, key) => {
            const camelKey = camelCase(key); // Convert to camelCase
            acc[camelKey] = keysToCamelCase(obj[key]); // Recursive call
            return acc;
        }, {});
    }
    return obj;
}

// Example usage
const apiResponse = {
    flight_id: 2,
    route_id: 2,
    departure_time: "2024-11-02T10:30:00+00:00",
    arrival_time: "2024-11-02T12:30:00+00:00",
    departure_airport_id: 1,
    departure_iata_code: "SGN",
    departure_city: "Ho Chi Minh",
    arrival_airport_id: 3,
    arrival_iata_code: "DAD",
    arrival_city: "Da Nang",
    distance: 605,
};

const transformedData = keysToCamelCase(apiResponse);
console.log(transformedData);
