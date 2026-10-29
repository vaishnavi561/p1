import React, { useEffect } from 'react';

export default function Toast({ message, type = 'error', onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 4000); // Auto-dismiss after 4 seconds
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  const bgStyles = type === 'success' 
    ? 'bg-emerald-600 text-white' 
    : 'bg-rose-600 text-white shadow-lg shadow-rose-600/30';

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-bounce">
      <div className={`px-5 py-3 rounded-2xl text-xs font-semibold flex items-center space-x-3 ${bgStyles}`}>
        <span>{type === 'success' ? '✅' : '⚠️'}</span>
        <span>{message}</span>
        <button onClick={onClose} className="ml-2 opacity-80 hover:opacity-100 font-bold">×</button>
      </div>
    </div>
  );
}