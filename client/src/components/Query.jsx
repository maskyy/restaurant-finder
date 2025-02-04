// Query.js
import React from 'react';
import { useParams, useLocation } from 'react-router-dom';
import MapComponent from './MapComponent';

const Query = () => {
  const { id } = useParams();

  // Example center coordinates and points
  const center = [51.505, -0.09]; // Replace with dynamic coordinates if needed
  const points = [
    { name: 'Point 1', coordinates: [51.505, -0.09] },
    { name: 'Point 2', coordinates: [51.51, -0.1] },
  ];

  return (
    <div>
      <h1>Query Page for ID: {id}</h1>
      <MapComponent center={center} points={points} />
    </div>
  );
};

export default Query;
