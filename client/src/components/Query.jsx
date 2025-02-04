import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import MapComponent from './MapComponent';
import axiosInstance from '../axiosInstance';



const Query = () => {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axiosInstance.get(`/queries/${id}`);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };
    fetchData();
  }, [id]);

  if (!data) {
    return <div>Loading...</div>;
  }

  const { current_location: currentLocation, restaurants } = data;

  return (
    <div>
      <MapComponent currentLocation={currentLocation} restaurants={restaurants} />
    </div>
  );
};

export default Query;
