import React, { useState } from 'react';
import api from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    try {
      // Calls the backend registration endpoint
      await api.post('/api/register/', { username, email, password });
      
      // Successfully registered -> redirect user to login
      navigate('/login');
    } catch (err) {
      const errData = err.response?.data;
      if (typeof errData === 'object') {
        setError(Object.values(errData).flat().join(' '));
      } else {
        setError("Registration failed. Please try again.");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white p-4">
      <div className="max-w-md w-full bg-gray-900 border border-gray-800 p-8 rounded-3xl shadow-2xl">
        <h2 className="text-2xl font-bold mb-1">Create an Account</h2>
        <p className="text-xs text-gray-400 mb-6">Join MedLife.ai to manage your family health.</p>

        {error && <div className="mb-4 p-3 bg-red-950/50 border border-red-800 text-red-400 text-xs rounded-xl">{error}</div>}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase text-gray-400 mb-1">Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              className="w-full px-3 py-2.5 bg-gray-800 border border-gray-700 rounded-xl text-sm text-white focus:outline-none focus:border-rose-500" 
              required 
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-gray-400 mb-1">Email</label>
            <input 
              type="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              className="w-full px-3 py-2.5 bg-gray-800 border border-gray-700 rounded-xl text-sm text-white focus:outline-none focus:border-rose-500" 
              required 
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-gray-400 mb-1">Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              className="w-full px-3 py-2.5 bg-gray-800 border border-gray-700 rounded-xl text-sm text-white focus:outline-none focus:border-rose-500" 
              required 
            />
          </div>

          <button 
            type="submit" 
            className="w-full py-3 bg-rose-600 hover:bg-rose-700 text-white font-semibold text-sm rounded-xl shadow-lg transition cursor-pointer mt-2"
          >
            Sign Up →
          </button>
        </form>

        <div className="text-center mt-6 text-xs text-gray-400">
          Already have an account? <span onClick={() => navigate('/login')} className="text-rose-500 hover:underline cursor-pointer font-semibold">Sign in</span>
        </div>
      </div>
    </div>
  );
}