import React, { useState } from 'react';

const InputField = ({ label, name, type = 'number', value, onChange, placeholder }) => (
    <div className="flex flex-col space-y-1.5 transition-all group">
        <label className="text-sm font-bold text-slate-600 group-focus-within:text-indigo-600 transition-colors tracking-wide">{label}</label>
        <input
            required
            type={type}
            name={name}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            className="p-3.5 border border-slate-200 rounded-xl shadow-sm focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none text-slate-800 transition-all duration-300 hover:border-slate-300 hover:shadow-md bg-white/70 focus:bg-white placeholder-slate-400 font-medium"
        />
    </div>
);

export default function LoanForm({ type, onSubmit, isLoading }) {
    const [formData, setFormData] = useState({
        // Shared
        loan_amount: '',
        credit_score: '',
        tenure: '',
        // Personal
        age: '',
        income: '',
        emi: '',
        // Business
        business_age: '',
        annual_revenue: '',
        net_profit: '',
        existing_liabilities: ''
    });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const submitForm = (e) => {
        e.preventDefault();

        // Only send fields relevant to the selected loan type
        const sharedKeys = ['loan_amount', 'credit_score', 'tenure'];
        const personalKeys = ['age', 'income', 'emi'];
        const businessKeys = ['business_age', 'annual_revenue', 'net_profit', 'existing_liabilities'];

        const relevantKeys = [...sharedKeys, ...(type === 'personal' ? personalKeys : businessKeys)];

        const payload = relevantKeys.reduce((acc, key) => {
            acc[key] = formData[key] ? Number(formData[key]) : 0;
            return acc;
        }, {});
        onSubmit(payload);
    };

    return (
        <form onSubmit={submitForm} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* Shared Fields */}
                <InputField label="Loan Amount (₹)" name="loan_amount" value={formData.loan_amount} onChange={handleChange} placeholder="e.g. 500000" />
                <InputField label="Credit Score" name="credit_score" value={formData.credit_score} onChange={handleChange} placeholder="300 - 850" />
                <InputField label="Loan Tenure (Months)" name="tenure" value={formData.tenure} onChange={handleChange} placeholder="e.g. 36" />

                {/* Dynamic Fields */}
                {type === 'personal' ? (
                    <>
                        <InputField label="Age" name="age" value={formData.age} onChange={handleChange} placeholder="e.g. 30" />
                        <InputField label="Monthly Income (₹)" name="income" value={formData.income} onChange={handleChange} placeholder="e.g. 50000" />
                        <InputField label="Existing Monthly EMIs (₹)" name="emi" value={formData.emi} onChange={handleChange} placeholder="e.g. 5000" />
                    </>
                ) : (
                    <>
                        <InputField label="Business Age (Years)" name="business_age" value={formData.business_age} onChange={handleChange} placeholder="e.g. 5" />
                        <InputField label="Annual Revenue (₹)" name="annual_revenue" value={formData.annual_revenue} onChange={handleChange} placeholder="e.g. 2500000" />
                        <InputField label="Net Profit (₹)" name="net_profit" value={formData.net_profit} onChange={handleChange} placeholder="e.g. 500000" />
                        <InputField label="Existing Liabilities (₹)" name="existing_liabilities" value={formData.existing_liabilities} onChange={handleChange} placeholder="e.g. 100000" />
                    </>
                )}
            </div>

            <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-4 px-6 rounded-2xl font-black text-white text-lg tracking-wide transition-all duration-500 transform relative overflow-hidden group
          ${isLoading
                        ? 'bg-slate-400 cursor-not-allowed scale-100 shadow-none'
                        : 'bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:scale-[1.02] hover:shadow-[0_8px_30px_rgb(99,102,241,0.4)] hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500'
                    }`}
            >
                {/* Button shine effect */}
                {!isLoading && (
                    <div className="absolute top-0 -inset-full h-full w-1/2 z-0 block transform -skew-x-12 bg-gradient-to-r from-transparent to-white opacity-20 group-hover:animate-shine"></div>
                )}

                <span className="relative z-10 flex items-center justify-center">
                    {isLoading ? (
                        <>
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Running AI Models...
                        </>
                    ) : 'Evaluate Loan Risk'}
                </span>
            </button>
        </form>
    );
}
