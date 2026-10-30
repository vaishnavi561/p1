import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { QRCodeSVG } from 'qrcode.react';
import { useNavigate } from 'react-router-dom';

export default function TwoFactorSetup() {
  const [otpauthUrl, setOtpauthUrl] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    api.post('/api/auth/2fa/setup/')
      .then(response => {
        setOtpauthUrl(response.data.totp_uri);
        setLoading(false);
      })
      .catch(err => {
        console.error("2FA load error:", err);
        setError("Failed to load 2FA setup. Please ensure you are logged in.");
        setLoading(false);
      });
  }, []);

  const handleVerify = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await api.post('/api/auth/2fa/verify-enable/', { 
        totp_code: otpCode 
      });
      setSuccessMessage(response.data.message || "2FA enabled successfully!");
      
      // ✅ FIXED: Send them directly to the dashboard instead of throwing them back to login!
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500);
    } catch (err) {
      console.error("Verification error:", err);
      setError(err.response?.data?.error || "Invalid 6-digit code. Please try again.");
    }
  };

  if (loading) {
    return <div className="text-center p-8 text-white">Loading 2FA Setup...</div>;
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md text-gray-800">
        <h2 className="text-2xl font-bold text-center mb-1">Secure Your Account</h2>
        <p className="text-sm text-gray-500 text-center mb-6">Enable Two-Factor Authentication (2FA)</p>

        <ol className="text-sm text-gray-700 space-y-2 mb-6">
          <li>1. Open <b>Google Authenticator</b> or <b>Microsoft Authenticator</b>.</li>
          <li>2. Tap <b>+</b> to add an account and scan the QR code below:</li>
        </ol>

        <div className="flex flex-col items-center justify-center border border-gray-200 rounded-xl p-4 bg-gray-50 mb-6">
          <div className="bg-white p-3 rounded-lg shadow-sm mb-3">
            {otpauthUrl ? <QRCodeSVG value={otpauthUrl} size={180} /> : <p>Loading QR...</p>}
          </div>
        </div>

        {error && <p className="text-red-500 text-sm text-center mb-4">{error}</p>}
        {successMessage && <p className="text-green-600 text-sm text-center font-semibold mb-4">{successMessage}</p>}

        <form onSubmit={handleVerify} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-600 uppercase mb-2">
              3. Enter 6-digit code from app
            </label>
            <input 
              type="text" 
              maxLength="6"
              value={otpCode}
              onChange={(e) => setOtpCode(e.target.value)}
              placeholder="123456"
              className="w-full text-center tracking-widest text-lg py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>

          <button 
            type="submit"
            className="w-full py-3 bg-rose-600 hover:bg-rose-700 text-white font-semibold rounded-lg transition duration-200"
          >
            Verify and Enable 2FA →
          </button>
        </form>
      </div>
    </div>
  );
}