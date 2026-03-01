import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-50 via-slate-50 to-indigo-50 text-slate-900 font-sans selection:bg-indigo-500 selection:text-white relative overflow-hidden">

      {/* Decorative background effects */}
      <div className="absolute top-0 -left-10 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob pointer-events-none"></div>
      <div className="absolute top-0 -right-10 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000 pointer-events-none"></div>
      <div className="absolute -bottom-32 left-32 w-96 h-96 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000 pointer-events-none"></div>

      <nav className="bg-white/60 backdrop-blur-xl border-b border-white/50 sticky top-0 z-50 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20 items-center">
            <div className="flex items-center group cursor-pointer">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg group-hover:shadow-indigo-500/50 transition-shadow duration-300 mr-4">
                <svg className="w-7 h-7 text-white transform group-hover:scale-110 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span className="text-2xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-slate-900 to-indigo-900">
                UniLoan AI
              </span>
            </div>
          </div>
        </div>
      </nav>

      <main className="py-12 relative z-10">
        <Dashboard />
      </main>

      <footer className="relative z-10 mt-12 py-10 border-t border-indigo-100/50 text-center text-sm font-medium text-slate-500 bg-white/40 backdrop-blur-sm">
        <p>Explainable AI for Smarter Lending Decisions &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
