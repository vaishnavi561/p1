import React from 'react';

export default function AiConfigBar({
  selectedModel,
  onModelChange,
  apiKey,
  onApiKeyChange,
  isAiConnected,
  onConnectAI,
  isDarkMode,
  toggleTheme
}) {
  return (
    <div className="sticky top-0 z-50 border-b px-6 py-4 flex justify-between items-center shadow-lg transition-colors duration-200 bg-white dark:bg-gray-900 border-rose-200 dark:border-gray-800">
      <h1 className="text-lg font-semibold text-gray-800 dark:text-white">Health dashboard</h1>

      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-3 px-3 py-2 rounded-xl shadow-md border transition-colors duration-200 bg-rose-50/50 dark:bg-gray-800 border-rose-200 dark:border-gray-700 text-gray-800 dark:text-white">
          <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">AI CONFIG</span>
          <select 
            value={selectedModel} 
            onChange={onModelChange} 
            className="text-xs px-2.5 py-1.5 rounded-lg border focus:outline-none focus:ring-2 focus:ring-rose-500 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-rose-300 dark:border-gray-600"
          >
            <option value="Ollama">Ollama (Local)</option>
            <option value="Gemini">Gemini</option>
            <option value="Claude">Claude</option>
            <option value="OpenAI">OpenAI</option>
          </select>
          
          {selectedModel === 'Ollama' ? (
            <span className="text-xs text-emerald-400 font-semibold px-2 py-1 bg-emerald-950/50 border border-emerald-800 rounded-lg">qwen:1.8b (Local)</span>
          ) : (
            <input 
              type="password" 
              value={apiKey} 
              onChange={onApiKeyChange} 
              placeholder={`Enter ${selectedModel} Key`} 
              className="text-xs px-2.5 py-1.5 rounded-lg border focus:outline-none w-36 bg-white dark:bg-gray-700 text-gray-800 dark:text-white border-rose-300 dark:border-gray-600" 
            />
          )}
          
          <button 
            onClick={onConnectAI} 
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition cursor-pointer ${
              isAiConnected 
                ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-600/20 shadow-md' 
                : 'bg-rose-600 hover:bg-rose-700 text-white shadow-rose-600/20 shadow-md'
            }`}
          >
            {isAiConnected ? 'Connected' : 'Connect'}
          </button>
        </div>
        
        <button 
          onClick={toggleTheme} 
          className="p-2.5 rounded-xl border transition shadow-md flex items-center justify-center bg-white dark:bg-gray-800 border-rose-200 dark:border-gray-700 text-gray-700 dark:text-yellow-400"
        >
          {isDarkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </div>
  );
}