import React from 'react';
import { Link } from 'react-router-dom';

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen py-16 px-4 font-sans bg-rose-50/30 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <div className="max-w-3xl mx-auto bg-white dark:bg-gray-900 border border-rose-200 dark:border-gray-800 rounded-2xl p-8 md:p-12 shadow-sm">
        <h1 className="text-3xl font-bold mb-2">Privacy Policy</h1>
        <p className="text-xs text-gray-500 italic mb-8">Last updated: October 2026</p>
        
        <div className="space-y-6 text-sm leading-relaxed text-gray-700 dark:text-gray-300">
          <div>
            <h2 className="text-rose-600 font-bold text-lg mb-2">1. Information you provide</h2>
            <p>Details such as your name, email address, or family health profiles submitted for application functionality.</p>
          </div>
          <div>
            <h2 className="text-rose-600 font-bold text-lg mb-2">2. How information may be used</h2>
            <p>Used to operate MedLife.ai, run AI consultations, and maintain secure family health dashboards.</p>
          </div>
          <div>
            <h2 className="text-rose-600 font-bold text-lg mb-2">3. Health information</h2>
            <p>Encrypted and processed strictly for authorized family profile queries and AI assistance.</p>
          </div>
          <div>
            <h2 className="text-rose-600 font-bold text-lg mb-2">4. Third-party services</h2>
            <p>Includes Google Gemini API, local Ollama (Qwen 1.8B), and our secure SMTP email provider.</p>
          </div>
          <div>
            <h2 className="text-rose-600 font-bold text-lg mb-2">5. Security and retention</h2>
            <p>Retained until manual profile deletion or full account termination.</p>
          </div>
          <div>
            <h2 className="text-rose-600 font-bold text-lg mb-2">6. Your choices and contact</h2>
            <p>
              For privacy questions or support inquiries, contact us directly at{' '}
              <a href="mailto:support@onesmarter.com" className="text-rose-500 font-semibold underline">
                support@onesmarter.com
              </a>.
            </p>
          </div>
        </div>

        <div className="mt-8">
          <Link to="/" className="text-xs px-4 py-2 bg-rose-100 dark:bg-gray-800 text-rose-700 dark:text-gray-300 rounded-xl font-semibold">
            ← Back to Home / Login
          </Link>
        </div>
      </div>
    </div>
  );
}
