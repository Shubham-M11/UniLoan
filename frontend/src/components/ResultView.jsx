import React from 'react';

export default function ResultView({ result }) {
    if (!result) return null;

    const { approval_probability, risk_level, suggested_loan_amount, key_factors, advisory } = result;

    const probPercentage = Math.round(approval_probability * 100);

    // Determine colors based on risk level
    let riskColor = "text-green-500";
    let riskBg = "bg-green-100/50";
    let ringColor = "text-green-500";

    if (risk_level === "Medium") {
        riskColor = "text-yellow-500";
        riskBg = "bg-yellow-100/50";
        ringColor = "text-yellow-400";
    } else if (risk_level === "High") {
        riskColor = "text-red-500";
        riskBg = "bg-red-100/50";
        ringColor = "text-red-500";
    }

    // Circle Gauge Math
    const radius = 60;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (probPercentage / 100) * circumference;

    return (
        <div className="w-full bg-white/70 backdrop-blur-3xl rounded-[2rem] p-10 shadow-[0_8px_30px_rgb(0,0,0,0.06)] ring-1 ring-slate-900/5 animate-in slide-in-from-right-8 duration-700 relative overflow-hidden">

            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 pointer-events-none"></div>

            <div className="flex flex-col items-center justify-center space-y-4 mb-10 relative z-10">
                <h2 className="text-3xl font-black text-slate-800 tracking-tight">AI Evaluation Complete</h2>

                {/* Probability Gauge */}
                <div className="relative flex items-center justify-center mt-6 mb-2">
                    <svg className="transform -rotate-90 w-40 h-40">
                        {/* Background Circle */}
                        <circle
                            cx="80"
                            cy="80"
                            r={radius}
                            stroke="currentColor"
                            strokeWidth="12"
                            fill="transparent"
                            className="text-gray-100"
                        />
                        {/* Progress Circle */}
                        <circle
                            cx="80"
                            cy="80"
                            r={radius}
                            stroke="currentColor"
                            strokeWidth="12"
                            fill="transparent"
                            strokeDasharray={circumference}
                            strokeDashoffset={strokeDashoffset}
                            className={`${ringColor} transition-all duration-1000 ease-out`}
                            strokeLinecap="round"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-4xl font-extrabold text-gray-800">{probPercentage}%</span>
                        <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider mt-1">Approval</span>
                    </div>
                </div>

                {/* Risk Badge */}
                <div className={`mt-2 px-8 py-2.5 rounded-2xl font-black text-sm tracking-widest shadow-md ring-1 ring-inset ${riskBg} ${riskColor} hover:scale-105 transition-transform duration-300 cursor-default inline-flex items-center backdrop-blur-sm`}>
                    <span className="relative flex h-3 w-3 mr-3">
                        <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${riskColor.replace('text-', 'bg-')}`}></span>
                        <span className={`relative inline-flex rounded-full h-3 w-3 ${riskColor.replace('text-', 'bg-')}`}></span>
                    </span>
                    {risk_level.toUpperCase()} RISK
                </div>
            </div>

            <div className="bg-slate-50/80 backdrop-blur-md rounded-[1.5rem] p-8 space-y-8 shadow-inner border border-slate-100/50 relative z-10">

                {/* Suggested Amount */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-200/60 pb-6 hover:bg-slate-100/50 p-4 rounded-2xl transition-all duration-300 cursor-default group">
                    <div className="text-slate-500 font-semibold group-hover:text-slate-800 transition-colors flex items-center mb-2 sm:mb-0">
                        <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center mr-3 group-hover:scale-110 transition-transform">
                            <svg className="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        Suggested Safe Amount
                    </div>
                    <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500 sm:text-right">
                        {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(suggested_loan_amount)}
                    </div>
                </div>

                {/* Key Factors */}
                <div>
                    <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest mb-4 flex items-center">
                        <svg className="w-5 h-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Why Did The AI Decide This?
                    </h3>
                    <ul className="space-y-3">
                        {key_factors.map((factor, idx) => (
                            <li key={idx} className="flex items-start bg-white p-3 rounded-xl shadow-sm hover:shadow-md transition-all duration-300 border border-gray-100 group cursor-default hover:-translate-y-0.5">
                                <div className={`p-2 rounded-lg mr-3 shadow-inner ${risk_level === 'High' ? 'bg-red-50 text-red-500' : 'bg-blue-50 text-blue-500'} group-hover:scale-110 transition-transform`}>
                                    <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        {risk_level === 'High' ? (
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                        ) : (
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                        )}
                                    </svg>
                                </div>
                                <div className="flex flex-col pt-1">
                                    <span className="text-gray-800 font-semibold">{factor}</span>
                                    <span className="text-xs text-gray-500 mt-0.5">This influenced your {probPercentage}% approval odds.</span>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Advisory */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-start bg-blue-50 text-blue-800 p-4 rounded-xl">
                        <svg className="w-6 h-6 mr-3 flex-shrink-0 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-sm font-medium leading-relaxed">{advisory}</p>
                    </div>
                </div>

            </div>

        </div>
    );
}
