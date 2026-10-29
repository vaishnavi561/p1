import React, { useState } from 'react';

export default function MemberDetail({
  selectedMember,
  getInitials,
  onOpenEdit,
  onRemoveMember,
  modelLabel,
  activeMessages,
  isAnswering,
  chatInput,
  onChatInputChange,
  onSendMessage,
  activeQuestionCount
}) {

  const handleDownloadChat = () => {
    if (!activeMessages || activeMessages.length === 0) {
      alert("No chat history available to download.");
      return;
    }

    const chatContent = activeMessages
      .map(msg => `[${msg.sender.toUpperCase()}] ${msg.text}`)
      .join('\n\n');

    const blob = new Blob([chatContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${selectedMember.name.replace(/\s+/g, '_')}_MedLife_Chat.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900 rounded-2xl border border-rose-200 dark:border-gray-800 shadow-sm overflow-hidden">
      
      {/* Header */}
      <div className="p-6 border-b border-rose-100 dark:border-gray-800 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-rose-500/10 text-rose-600 dark:text-rose-400 font-bold flex items-center justify-center text-lg">
            {getInitials(selectedMember.name)}
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">{selectedMember.name}</h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Model: <span className="font-semibold text-rose-600 dark:text-rose-400">{modelLabel}</span> | Questions: {activeQuestionCount}/100
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* 📥 Download Chat Button (P3-01) */}
          <button
            onClick={handleDownloadChat}
            className="text-xs px-3 py-2 bg-rose-100 dark:bg-gray-800 text-rose-700 dark:text-gray-300 rounded-xl font-semibold hover:bg-rose-200 dark:hover:bg-gray-700 transition flex items-center space-x-1 cursor-pointer"
            title="Download Chat History"
          >
            <span>📥 Download Chat</span>
          </button>

          <button 
            onClick={() => onOpenEdit(selectedMember)}
            className="text-xs px-3 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-xl font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition cursor-pointer"
          >
            Edit Profile
          </button>
          <button 
            onClick={() => onRemoveMember(selectedMember.id)}
            className="text-xs px-3 py-2 bg-red-100 dark:bg-red-950/40 text-red-700 dark:text-red-400 rounded-xl font-semibold hover:bg-red-200 dark:hover:bg-red-900/50 transition cursor-pointer"
          >
            Delete
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-gray-50/50 dark:bg-gray-950/50">
        {activeMessages.length === 0 ? (
          <div className="text-center py-12 text-gray-400 text-xs">
            No consultation history yet. Ask a health or medical question below!
          </div>
        ) : (
          activeMessages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xl p-4 rounded-2xl text-sm leading-relaxed ${
                msg.sender === 'user' 
                  ? 'bg-rose-600 text-white rounded-br-none' 
                  : 'bg-white dark:bg-gray-800 border border-rose-100 dark:border-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-none shadow-sm'
              }`}>
                <p className="whitespace-pre-wrap">{msg.text}</p>
              </div>
            </div>
          ))
        )}
        {isAnswering && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-gray-800 border border-rose-100 dark:border-gray-700 p-4 rounded-2xl text-xs text-gray-500 animate-pulse">
              AI is analyzing medical context...
            </div>
          </div>
        )}
      </div>

      {/* Chat Input Form */}
      <form onSubmit={onSendMessage} className="p-4 bg-white dark:bg-gray-900 border-t border-rose-100 dark:border-gray-800 flex items-center space-x-3">
        <input 
          type="text"
          value={chatInput}
          onChange={onChatInputChange}
          placeholder={`Ask a question for ${selectedMember.name}...`}
          className="flex-1 px-4 py-3 bg-gray-100 dark:bg-gray-800 border border-transparent dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-white focus:outline-none focus:border-rose-500"
          disabled={isAnswering}
        />
        <button 
          type="submit"
          disabled={isAnswering || !chatInput.trim()}
          className="px-6 py-3 bg-rose-600 hover:bg-rose-700 text-white font-semibold text-xs rounded-xl shadow-md transition cursor-pointer disabled:opacity-50"
        >
          Send →
        </button>
      </form>

    </div>
  );
}