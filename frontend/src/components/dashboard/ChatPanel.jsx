import React from 'react';

export default function ChatPanel({
  selectedMember,
  modelLabel,
  activeMessages,
  isAnswering,
  chatInput,
  onChatInputChange,
  onSendMessage,
  activeQuestionCount
}) {
  return (
    <div className="p-6 rounded-2xl border shadow-lg bg-white dark:bg-gray-900 border-rose-200 dark:border-gray-800">
      <div className="flex justify-between items-center mb-6 border-b pb-4 border-gray-200 dark:border-gray-800">
        <div className="flex items-center space-x-2">
          <span className="w-8 h-8 rounded-full bg-rose-500/10 text-rose-600 flex items-center justify-center font-bold">✨</span>
          <div className="text-left">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white">Ask medlife.ai ({modelLabel})</h3>
          </div>
        </div>
      </div>

      <div className="space-y-4 mb-6 max-h-96 overflow-y-auto pr-2">
        {activeMessages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-lg p-3.5 rounded-2xl text-sm ${msg.sender === 'user' ? 'bg-rose-600 text-white rounded-br-none' : 'bg-rose-50 dark:bg-gray-800 text-gray-800 dark:text-gray-100 rounded-bl-none border border-rose-200 dark:border-gray-700'}`}>
              <div className="text-[10px] font-semibold opacity-70 mb-1">{msg.sender === 'user' ? 'You' : `MedlifeAI Database + ${modelLabel}`}</div>
              {msg.text}
            </div>
          </div>
        ))}
        {isAnswering && (
          <div className="flex justify-start">
            <div className="p-3 rounded-2xl text-xs italic bg-rose-100 dark:bg-gray-800 text-rose-700 dark:text-gray-400">
              Querying database & {modelLabel}...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={onSendMessage} className="flex items-center space-x-2 pt-2">
        <input 
          type="text" 
          value={chatInput} 
          onChange={onChatInputChange} 
          placeholder={`Ask a question about ${selectedMember.name}...`} 
          className="flex-1 px-4 py-3 rounded-xl border text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 bg-white dark:bg-gray-800 border-rose-200 dark:border-gray-700 text-gray-900 dark:text-white" 
          disabled={activeQuestionCount >= 100} 
        />
        <button type="submit" disabled={isAnswering} className="px-5 py-3 bg-rose-600 hover:bg-rose-700 text-white font-semibold text-sm rounded-xl cursor-pointer">Send →</button>
      </form>
    </div>
  );
}