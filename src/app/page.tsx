'use client';

import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function HomePage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [token, setToken] = useState('');
    const [resumeText, setResumeText] = useState('');
    const [updateText, setUpdateText] = useState('');
    const [response, setResponse] = useState<any>(null);
    const [error, setError] = useState('');

    const handleSignup = async () => {
        try {
            const res = await fetch(`${API_URL}/api/v1/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, full_name: 'Test User' })
            });
            const data = await res.json();
            setResponse(data);
            setError('');
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleLogin = async () => {
        try {
            const res = await fetch(`${API_URL}/api/v1/login/access-token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
            });
            const data = await res.json();
            setToken(data.access_token);
            setResponse(data);
            setError('');
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleParseResume = async () => {
        try {
            const res = await fetch(`${API_URL}/api/v1/resumes/parse`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ resume_text: resumeText })
            });
            const data = await res.json();
            setResponse(data);
            setError('');
        } catch (err: any) {
            setError(err.message);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-8 text-indigo-900">
                    AI Resume Agent
                </h1>

                {/* Auth Section */}
                <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <h2 className="text-2xl font-semibold mb-4 text-gray-800">Authentication</h2>
                    <div className="space-y-4">
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        />
                        <div className="flex gap-4">
                            <button
                                onClick={handleSignup}
                                className="flex-1 bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition"
                            >
                                Sign Up
                            </button>
                            <button
                                onClick={handleLogin}
                                className="flex-1 bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 transition"
                            >
                                Login
                            </button>
                        </div>
                        {token && (
                            <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                                <strong>Token:</strong> {token.substring(0, 20)}...
                            </div>
                        )}
                    </div>
                </div>

                {/* Resume Parsing Section */}
                {token && (
                    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                        <h2 className="text-2xl font-semibold mb-4 text-gray-800">Parse Resume</h2>
                        <textarea
                            placeholder="Paste your resume text here..."
                            value={resumeText}
                            onChange={(e) => setResumeText(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md h-32 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        />
                        <button
                            onClick={handleParseResume}
                            className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition"
                        >
                            Parse Resume
                        </button>
                    </div>
                )}

                {/* Response Display */}
                {(response || error) && (
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-2xl font-semibold mb-4 text-gray-800">Response</h2>
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                                <strong>Error:</strong> {error}
                            </div>
                        )}
                        {response && (
                            <pre className="bg-gray-50 p-4 rounded overflow-auto text-sm">
                                {JSON.stringify(response, null, 2)}
                            </pre>
                        )}
                    </div>
                )}

                {/* API Status */}
                <div className="mt-6 text-center text-sm text-gray-600">
                    Connected to: <span className="font-mono bg-gray-100 px-2 py-1 rounded">{API_URL}</span>
                </div>
            </div>
        </div>
    );
}
