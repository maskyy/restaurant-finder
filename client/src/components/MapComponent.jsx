// MapComponent.js
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const blueIcon = new L.Icon({
  iconUrl: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
});

const greenIcon = new L.Icon({
  iconUrl: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
});

const MapComponent = ({ currentLocation, restaurants }) => {
  const center = { lat: currentLocation.latitude, lng: currentLocation.longitude };
  return (
    <MapContainer center={center} zoom={15} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      <Marker position={center} icon={blueIcon}>
        <Popup>Current location</Popup>
      </Marker>

      {restaurants.map((place, index) => {
        return (
          <Marker key={index} position={{ lat: place.latitude, lng: place.longitude }} icon={greenIcon}>
            <Popup>
              <a href={place.url} target="_blank" rel="noopener noreferrer">
                <strong>{place.name}</strong>
              </a>
              <br />
              Rating: {place.rating || 'N/A'} ⭐
              <br />
              Price: {place.price || 'N/A'}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
};

export default MapComponent;
