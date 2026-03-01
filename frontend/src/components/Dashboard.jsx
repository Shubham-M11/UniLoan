import React, { useState } from 'react';
import LoanForm from './LoanForm';
import ResultView from './ResultView';

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState('personal');
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [submissionCount, setSubmissionCount] = useState(0);

    const handleSubmit = async (formData) => {
        setIsLoading(true);
        setResult(null);
        try {
            const endpoint = activeTab === 'personal' ? '/predict/personal' : '/predict/business';
            const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
            const response = await fetch(`${apiUrl}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            setSubmissionCount(prev => prev + 1);
            setResult(data);
        } catch (error) {
            console.error('Submission error:', error);
            alert('Failed to get prediction from backend.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto p-4 md:p-8 space-y-12 animate-in fade-in zoom-in-95 duration-1000">
            <div className="text-center space-y-6 mb-16 relative">
                <div className="inline-block px-4 py-1.5 rounded-full bg-blue-100/50 border border-blue-200 text-blue-700 font-semibold text-sm mb-4 shadow-sm backdrop-blur-md">
                    Powered by Machine Learning
                </div>
                <h1 className="text-5xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 drop-shadow-sm tracking-tight">
                    Intelligent Loan Evaluator
                </h1>
                <p className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto leading-relaxed font-medium">
                    Experience explainable, AI-driven lending decisions wrapped in a stunning modern interface.
                </p>
            </div>

            <div className="flex flex-col lg:flex-row gap-8 lg:gap-12">
                {/* Left Side: Form */}
                <div className="w-full lg:w-1/2 bg-white/60 backdrop-blur-2xl rounded-[2rem] p-8 shadow-[0_8px_30px_rgb(0,0,0,0.04)] ring-1 ring-slate-900/5 transition-all duration-500 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] relative overflow-hidden group">

                    {/* Subtle shine effect */}
                    <div className="absolute top-0 -inset-full h-full w-1/2 z-0 block transform -skew-x-12 bg-gradient-to-r from-transparent to-white opacity-20 group-hover:animate-shine"></div>
                    <div className="flex bg-slate-100/80 backdrop-blur-md rounded-2xl p-1.5 mb-10 shadow-inner relative z-10">
                        <button
                            onClick={() => { setActiveTab('personal'); setResult(null); }}
                            className={`flex-1 py-3.5 text-sm font-bold rounded-xl transition-all duration-500 ease-out ${activeTab === 'personal' ? 'bg-white text-blue-600 shadow-md transform scale-[1.02] ring-1 ring-black/5' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-200/50'}`}
                        >
                            Personal Loan
                        </button>
                        <button
                            onClick={() => { setActiveTab('business'); setResult(null); }}
                            className={`flex-1 py-3.5 text-sm font-bold rounded-xl transition-all duration-500 ease-out ${activeTab === 'business' ? 'bg-white text-indigo-600 shadow-md transform scale-[1.02] ring-1 ring-black/5' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-200/50'}`}
                        >
                            Business Loan
                        </button>
                    </div>

                    <LoanForm type={activeTab} onSubmit={handleSubmit} isLoading={isLoading} />
                </div>

                {/* Right Side: Results */}
                <div className="w-full lg:w-1/2 flex flex-col items-center justify-center perspective-1000">
                    {result ? (
                        <ResultView key={submissionCount} result={result} />
                    ) : (
                        <div className="h-full w-full rounded-[2rem] border-2 border-dashed border-indigo-200/60 flex flex-col items-center justify-center p-12 text-center text-slate-400 bg-white/20 backdrop-blur-xl shadow-inner transition-all duration-700 hover:bg-white/40 hover:border-indigo-300 min-h-[500px] group">
                            <div className="w-24 h-24 mb-8 rounded-full bg-indigo-50/50 flex items-center justify-center group-hover:scale-110 group-hover:bg-indigo-100 transition-all duration-700">
                                <svg className="w-12 h-12 text-indigo-300 group-hover:text-indigo-500 transition-colors duration-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <h3 className="text-2xl font-bold text-slate-700 mb-3 group-hover:text-indigo-900 transition-colors">Awaiting Evaluation</h3>
                            <p className="mt-2 text-lg leading-relaxed text-slate-500 max-w-xs">Enter your parameters on the left to generate a visual AI risk analysis.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
