import React, { useState, useEffect } from "react";
import { FileSpreadsheet, Printer, Download, Calendar, DollarSign, ArrowDownRight } from "lucide-react";
import { reportsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { MetricCard } from "../components/common/MetricCard";

export const Reports = () => {
  const [reportType, setReportType] = useState("monthly");
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadReport = () => {
    setLoading(true);
    let promise;
    if (reportType === "daily") promise = reportsAPI.getDaily();
    else if (reportType === "weekly") promise = reportsAPI.getWeekly();
    else promise = reportsAPI.getMonthly();

    promise
      .then((res) => setReportData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadReport();
  }, [reportType]);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Institutional Utility & Financial Audit Reports"
        subtitle="Automated daily, weekly, and monthly resource accountability summaries with estimated savings"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Controls */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setReportType("daily")}
              className={`rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                reportType === "daily" ? "bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/20" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              Daily Operational Report
            </button>
            <button
              onClick={() => setReportType("weekly")}
              className={`rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                reportType === "weekly" ? "bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/20" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              Weekly Resource Audit
            </button>
            <button
              onClick={() => setReportType("monthly")}
              className={`rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                reportType === "monthly" ? "bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/20" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              Monthly Executive Summary
            </button>
          </div>

          <button
            onClick={handlePrint}
            className="flex items-center gap-2 rounded-xl bg-white border border-slate-200 px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 transition-all shadow-xs cursor-pointer"
          >
            <Printer className="h-4 w-4 text-sky-600" />
            <span>Print / PDF Export</span>
          </button>
        </div>

        {reportData && (
          <div className="space-y-6">
            {/* Savings & Financial Banner */}
            {reportType === "monthly" && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
                  <span className="text-xs font-bold text-slate-500 uppercase">Current Total Utility Bill</span>
                  <p className="mt-2 text-2xl font-extrabold text-slate-900">₹{reportData.current_total_cost?.toLocaleString()}</p>
                  <p className="text-[11px] text-slate-400 mt-1 font-medium">Period: {reportData.period}</p>
                </div>
                <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
                  <span className="text-xs font-bold text-slate-500 uppercase">Potential Optimized Bill</span>
                  <p className="mt-2 text-2xl font-extrabold text-sky-700">₹{reportData.potential_optimized_cost?.toLocaleString()}</p>
                  <p className="text-[11px] text-slate-400 mt-1 font-medium">Toward historical baseline</p>
                </div>
                <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5 shadow-sm">
                  <span className="text-xs font-bold text-emerald-800 uppercase">Estimated Possible Savings</span>
                  <p className="mt-2 text-2xl font-black text-emerald-700">₹{reportData.estimated_possible_savings?.toLocaleString()}</p>
                  <p className="text-[11px] text-emerald-600 mt-1 font-semibold">~14% achievable reduction</p>
                </div>
              </div>
            )}

            {/* Block Breakdown Table */}
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
              <h3 className="text-sm font-extrabold text-slate-900 mb-1">{reportData.report_type}</h3>
              <p className="text-xs text-slate-500 mb-4 font-medium">Institutional disaggregated accounting matrix</p>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-700">
                  <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-b border-slate-100">
                    <tr>
                      <th className="px-4 py-3 rounded-l-xl">Hostel Block</th>
                      <th className="px-4 py-3">Water (Litres)</th>
                      <th className="px-4 py-3">Electricity (kWh)</th>
                      <th className="px-4 py-3">Gas (kg)</th>
                      <th className="px-4 py-3 rounded-r-xl">Total Cost (₹)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {reportData.blocks?.map((b, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                        <td className="px-4 py-3 font-bold text-slate-900">{b.hostel_name} ({b.block})</td>
                        <td className="px-4 py-3 font-semibold text-slate-800">{b.water_litres?.toLocaleString()} L</td>
                        <td className="px-4 py-3 font-semibold text-slate-800">{b.electricity_kwh?.toLocaleString()} kWh</td>
                        <td className="px-4 py-3 font-semibold text-slate-800">{b.gas_kg?.toLocaleString()} kg</td>
                        <td className="px-4 py-3 font-extrabold text-emerald-600">₹{b.total_cost?.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
