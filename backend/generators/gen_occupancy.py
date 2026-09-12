import os

target = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages\Occupancy.jsx"
code = '''import React, { useState, useEffect } from "react";
import { Users, Plus, Calendar, Filter } from "lucide-react";
import { occupancyAPI, hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { Modal } from "../components/common/Modal";

export const Occupancy = () => {
  const [records, setRecords] = useState([]);
  const [hostels, setHostels] = useState([]);
  const [selectedHostel, setSelectedHostel] = useState("");
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    hostel_id: "",
    date: new Date().toISOString().split("T")[0],
    student_count: 280
  });

  const loadData = () => {
    setLoading(true);
    const params = selectedHostel ? { hostel_id: selectedHostel } : {};
    Promise.all([occupancyAPI.list(params), hostelsAPI.list()])
      .then(([occRes, hostRes]) => {
        setRecords(occRes.data);
        setHostels(hostRes.data);
        if (hostRes.data.length > 0 && !formData.hostel_id) {
          setFormData((prev) => ({ ...prev, hostel_id: hostRes.data[0].id }));
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [selectedHostel]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await occupancyAPI.log(formData);
      setModalOpen(false);
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || "Log failed");
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Student Occupancy & Capacity Tracking"
        subtitle="Track daily resident attendance, leave variances, and capacity loading"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-3">
            <Filter className="h-4 w-4 text-sky-400" />
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Hostels ({hostels.length} Blocks)</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>
          </div>

          <button
            onClick={() => setModalOpen(true)}
            className="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white shadow-lg shadow-sky-500/20 hover:bg-sky-400 transition-all cursor-pointer"
          >
            <Plus className="h-4 w-4" />
            <span>Log Daily Occupancy</span>
          </button>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md">
          <h3 className="text-sm font-bold text-white mb-4">Historical Daily Occupancy Log</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-3 rounded-l-xl">Date</th>
                  <th className="px-4 py-3">Hostel Block</th>
                  <th className="px-4 py-3">Residents Present</th>
                  <th className="px-4 py-3">Occupancy Rate</th>
                  <th className="px-4 py-3 rounded-r-xl">Status Indicator</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {records.slice(0, 50).map((r) => (
                  <tr key={r.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 font-semibold text-white">{r.date}</td>
                    <td className="px-4 py-3 text-sky-400">{r.hostel_name} ({r.hostel_block})</td>
                    <td className="px-4 py-3 font-bold text-white">{r.student_count}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-20 h-2 rounded-full bg-slate-800 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${r.occupancy_percentage > 95 ? "bg-amber-500" : "bg-sky-500"}`}
                            style={{ width: `${r.occupancy_percentage}%` }}
                          />
                        </div>
                        <span className="font-semibold">{r.occupancy_percentage}%</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      {r.occupancy_percentage >= 95 ? (
                        <span className="text-amber-400 font-medium">Peak Density</span>
                      ) : r.occupancy_percentage <= 50 ? (
                        <span className="text-slate-400 font-medium">Vacation Low</span>
                      ) : (
                        <span className="text-emerald-400 font-medium">Nominal</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Log Daily Student Occupancy">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Hostel Block</label>
            <select
              value={formData.hostel_id}
              onChange={(e) => setFormData({ ...formData, hostel_id: parseInt(e.target.value) })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            >
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Date</label>
            <input
              type="date"
              required
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Resident Student Count</label>
            <input
              type="number"
              required
              value={formData.student_count}
              onChange={(e) => setFormData({ ...formData, student_count: parseInt(e.target.value) || 0 })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={() => setModalOpen(false)}
              className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white hover:bg-sky-400"
            >
              Save Occupancy Log
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
'''

with open(target, "w", encoding="utf-8") as f:
    f.write(code.strip() + "\n")
print("Occupancy.jsx generated.")
