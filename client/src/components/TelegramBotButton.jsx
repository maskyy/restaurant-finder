import React from 'react';

const TelegramBotButton = () => {
  // Bot URL
  const telegramBotUrl = 'https://t.me/naboka_weather_bot';

  return (
    <button
      onClick={() => window.open(telegramBotUrl, '_blank')}
      style={{
        backgroundColor: '#0088cc',
        color: '#fff',
        border: 'none',
        padding: '10px 20px',
        borderRadius: '5px',
        cursor: 'pointer',
      }}
    >
      Use our bot to find the restaurants!
    </button>
  );
};

export default TelegramBotButton;
