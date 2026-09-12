import os

FRONTEND_DIR = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages"

def write_maintenance():
    code = '''import React, { useState, useEffect } from "react";
import { Wrench, Plus, Filter, CheckCircle2, Clock, AlertCircle } from "lucide-react";
import { maintenanceAPI, hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { StatusBadge } from "../components/common/StatusBadge";
import { Modal } from "../components/common/Modal";

export const Maintenance = () => {
  const [tickets, setTickets] = useState([]);
  const [hostels, setHostels] = useState([]);
  const [selectedHostel, setSelectedHostel] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [selectedPriority, setSelectedPriority] = useState("");
  const [loading, setLoading] = useState(true);
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [activeTicket, setActiveTicket] = useState(null);

  const [formData, setFormData] = useState({
    hostel_id: "",
    resource_type: "Water",
    issue_type: "Pipe Rupture / Flow Leak",
    description: "",
    priority: "Medium",
    assigned_to: "Vikram Singh",
    notes: ""
  });

  const [updateData, setUpdateData] = useState({
    status: "",
    priority: "",
    assigned_to: "",
    notes: ""
  });

  const loadTickets = () => {
    setLoading(true);
    const params = {
      ...(selectedHostel ? { hostel_id: selectedHostel } : {}),
      ...(selectedStatus ? { status: selectedStatus } : {}),
      ...(selectedPriority ? { priority: selectedPriority } : {})
    };

    Promise.all([maintenanceAPI.list(params), hostelsAPI.list()])
      .then(([mRes, hRes]) => {
        setTickets(mRes.data);
        setHostels(hRes.data);
        if (hRes.data.length > 0 && !formData.hostel_id) {
          setFormData((prev) => ({ ...prev, hostel_id: hRes.data[0].id }));
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadTickets();
  }, [selectedHostel, selectedStatus, selectedPriority]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await maintenanceAPI.create(formData);
      setCreateModalOpen(false);
      loadTickets();
    } catch (err) {
      alert("Failed to create ticket");
    }
  };

  const handleOpenEdit = (t) => {
    setActiveTicket(t);
    setUpdateData({
      status: t.status,
      priority: t.priority,
      assigned_to: t.assigned_to || "",
      notes: ""
    });
    setEditModalOpen(true);
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!activeTicket) return;
    try {
      await maintenanceAPI.update(activeTicket.id, updateData);
      setEditModalOpen(false);
      loadTickets();
    } catch (err) {
      alert("Update failed");
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Maintenance Management & Work Order Dispatch"
        subtitle="Track utility leaks, power surge repairs, and technician work order lifecycles"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Controls */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex flex-wrap items-center gap-3">
            <Filter className="h-4 w-4 text-sky-400" />
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Hostels</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.block}</option>
              ))}
            </select>

            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Statuses</option>
              <option value="Open">Open</option>
              <option value="Assigned">Assigned</option>
              <option value="In Progress">In Progress</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
          </div>

          <button
            onClick={() => setCreateModalOpen(true)}
            className="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white shadow-lg shadow-sky-500/20 hover:bg-sky-400 transition-all cursor-pointer"
          >
            <Plus className="h-4 w-4" />
            <span>Create Work Order</span>
          </button>
        </div>

        {/* Tickets Table */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
          <h3 className="text-sm font-bold text-white mb-4">Active Work Orders ({tickets.length})</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-3 rounded-l-xl">Ticket #</th>
                  <th className="px-4 py-3">Hostel</th>
                  <th className="px-4 py-3">Resource</th>
                  <th className="px-4 py-3">Issue Type</th>
                  <th className="px-4 py-3">Priority</th>
                  <th className="px-4 py-3">Technician</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 rounded-r-xl">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {tickets.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-sky-400">#{t.id}</td>
                    <td className="px-4 py-3 font-semibold text-white">{t.hostel_name} ({t.hostel_block})</td>
                    <td className="px-4 py-3">{t.resource_type}</td>
                    <td className="px-4 py-3 text-slate-200">{t.issue_type}</td>
                    <td className="px-4 py-3"><StatusBadge status={t.priority} /></td>
                    <td className="px-4 py-3 text-slate-300">{t.assigned_to || "Unassigned"}</td>
                    <td className="px-4 py-3"><StatusBadge status={t.status} /></td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => handleOpenEdit(t)}
                        className="rounded-lg border border-slate-700 bg-slate-800 px-2.5 py-1 text-[11px] font-semibold text-sky-400 hover:bg-slate-700 hover:text-white transition-colors cursor-pointer"
                      >
                        Update / Notes
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Create Ticket Modal */}
      <Modal isOpen={createModalOpen} onClose={() => setCreateModalOpen(false)} title="Create New Maintenance Work Order">
        <form onSubmit={handleCreate} className="space-y-4">
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

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Resource</label>
              <select
                value={formData.resource_type}
                onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              >
                <option value="Water">Water</option>
                <option value="Electricity">Electricity</option>
                <option value="Gas">Gas</option>
                <option value="General">General</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Issue Headline</label>
            <input
              type="text"
              required
              value={formData.issue_type}
              onChange={(e) => setFormData({ ...formData, issue_type: e.target.value })}
              placeholder="e.g. Tank float valve malfunction"
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Detailed Description</label>
            <textarea
              rows={3}
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Describe symptoms, location on floor, observed leakage..."
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={() => setCreateModalOpen(false)}
              className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white hover:bg-sky-400 cursor-pointer"
            >
              Submit Ticket
            </button>
          </div>
        </form>
      </Modal>

      {/* Update Modal */}
      <Modal isOpen={editModalOpen} onClose={() => setEditModalOpen(false)} title={`Update Work Order #${activeTicket?.id}`}>
        <form onSubmit={handleUpdate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Status</label>
              <select
                value={updateData.status}
                onChange={(e) => setUpdateData({ ...updateData, status: e.target.value })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              >
                <option value="Open">Open</option>
                <option value="Assigned">Assigned</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Priority</label>
              <select
                value={updateData.priority}
                onChange={(e) => setUpdateData({ ...updateData, priority: e.target.value })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Assigned Technician</label>
            <input
              type="text"
              value={updateData.assigned_to}
              onChange={(e) => setUpdateData({ ...updateData, assigned_to: e.target.value })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Add Maintenance Note / Progress Update</label>
            <textarea
              rows={3}
              value={updateData.notes}
              onChange={(e) => setUpdateData({ ...updateData, notes: e.target.value })}
              placeholder="e.g. Replaced 2-inch copper valve on riser pipe. Tested water pressure."
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          {activeTicket?.notes && (
            <div className="rounded-xl bg-slate-800/80 p-3 text-xs text-slate-300 whitespace-pre-wrap font-mono">
              <p className="font-bold text-slate-400 mb-1 font-sans">Activity Log History:</p>
              {activeTicket.notes}
            </div>
          )}

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={() => setEditModalOpen(false)}
              className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white hover:bg-sky-400 cursor-pointer"
            >
              Update Work Order
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
'''
    with open(os.path.join(FRONTEND_DIR, "Maintenance.jsx"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print("Wrote Maintenance.jsx")

def write_reports():
    code = '''import React, { useState, useEffect } from "react";
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
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Institutional Utility & Financial Audit Reports"
        subtitle="Automated daily, weekly, and monthly resource accountability summaries with estimated savings"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Controls */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setReportType("daily")}
              className={`rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                reportType === "daily" ? "bg-sky-500 text-white shadow" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              Daily Operational Report
            </button>
            <button
              onClick={() => setReportType("weekly")}
              className={`rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                reportType === "weekly" ? "bg-sky-500 text-white shadow" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              Weekly Resource Audit
            </button>
            <button
              onClick={() => setReportType("monthly")}
              className={`rounded-xl px-4 py-2 text-xs font-bold transition-all cursor-pointer ${
                reportType === "monthly" ? "bg-sky-500 text-white shadow" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              Monthly Executive Summary
            </button>
          </div>

          <button
            onClick={handlePrint}
            className="flex items-center gap-2 rounded-xl bg-slate-800 border border-slate-700 px-4 py-2 text-xs font-bold text-white hover:bg-slate-700 transition-all cursor-pointer"
          >
            <Printer className="h-4 w-4 text-sky-400" />
            <span>Print / PDF Export</span>
          </button>
        </div>

        {reportData && (
          <div className="space-y-6">
            {/* Savings & Financial Banner */}
            {reportType === "monthly" && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg">
                  <span className="text-xs font-semibold text-slate-400 uppercase">Current Total Utility Bill</span>
                  <p className="mt-2 text-2xl font-bold text-white">₹{reportData.current_total_cost?.toLocaleString()}</p>
                  <p className="text-[11px] text-slate-500 mt-1">Period: {reportData.period}</p>
                </div>
                <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg">
                  <span className="text-xs font-semibold text-slate-400 uppercase">Potential Optimized Bill</span>
                  <p className="mt-2 text-2xl font-bold text-sky-400">₹{reportData.potential_optimized_cost?.toLocaleString()}</p>
                  <p className="text-[11px] text-slate-500 mt-1">Toward historical baseline</p>
                </div>
                <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-5 shadow-lg">
                  <span className="text-xs font-bold text-emerald-400 uppercase">Estimated Possible Savings</span>
                  <p className="mt-2 text-2xl font-extrabold text-emerald-400">₹{reportData.estimated_possible_savings?.toLocaleString()}</p>
                  <p className="text-[11px] text-slate-400 mt-1">~14% achievable reduction</p>
                </div>
              </div>
            )}

            {/* Block Breakdown Table */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-1">{reportData.report_type}</h3>
              <p className="text-xs text-slate-400 mb-4">Institutional disaggregated accounting matrix</p>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                    <tr>
                      <th className="px-4 py-3 rounded-l-xl">Hostel Block</th>
                      <th className="px-4 py-3">Water (Litres)</th>
                      <th className="px-4 py-3">Electricity (kWh)</th>
                      <th className="px-4 py-3">Gas (kg)</th>
                      <th className="px-4 py-3 rounded-r-xl">Total Cost (₹)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {reportData.blocks?.map((b, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                        <td className="px-4 py-3 font-bold text-white">{b.hostel_name} ({b.block})</td>
                        <td className="px-4 py-3 text-slate-200">{b.water_litres?.toLocaleString()} L</td>
                        <td className="px-4 py-3 text-slate-200">{b.electricity_kwh?.toLocaleString()} kWh</td>
                        <td className="px-4 py-3 text-slate-200">{b.gas_kg?.toLocaleString()} kg</td>
                        <td className="px-4 py-3 font-bold text-emerald-400">₹{b.total_cost?.toLocaleString()}</td>
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
'''
    with open(os.path.join(FRONTEND_DIR, "Reports.jsx"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print("Wrote Reports.jsx")

def write_settings():
    code = '''import React, { useState, useEffect } from "react";
import { Settings as SettingsIcon, IndianRupee, RefreshCw, CheckCircle2, ShieldAlert } from "lucide-react";
import { settingsAPI } from "../services/api";
import { Header } from "../components/common/Header";

export const Settings = () => {
  const [rates, setRates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reseedLoading, setReseedLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState("");

  const loadRates = () => {
    setLoading(true);
    settingsAPI.getRates()
      .then((res) => setRates(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadRates();
  }, []);

  const handleUpdateRate = async (id, newRate) => {
    try {
      await settingsAPI.updateRate(id, parseFloat(newRate));
      setStatusMsg("Utility tariff rate updated successfully.");
      loadRates();
      setTimeout(() => setStatusMsg(""), 3000);
    } catch (err) {
      alert("Rate update failed");
    }
  };

  const handleReseed = async () => {
    if (window.confirm("Re-seeding will recreate 8 blocks, 2,450 students, and 6 months of utility records. Proceed?")) {
      setReseedLoading(true);
      try {
        await settingsAPI.reseed();
        setStatusMsg("Database re-seeded successfully with fresh demo records!");
        loadRates();
      } catch (err) {
        alert("Reseed failed");
      } finally {
        setReseedLoading(false);
      }
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Institutional Settings & Tariff Configuration"
        subtitle="Configure commercial billing unit rates, database state, and system diagnostics"
      />

      <main className="p-8 max-w-4xl mx-auto space-y-6">
        {statusMsg && (
          <div className="rounded-xl bg-emerald-500/10 border border-emerald-500/30 p-3 text-xs font-semibold text-emerald-400">
            {statusMsg}
          </div>
        )}

        {/* Utility Tariff Rates */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md">
          <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
            <IndianRupee className="h-4 w-4 text-emerald-400" />
            Commercial Utility Tariff Rates
          </h3>
          <p className="text-xs text-slate-400 mb-6">
            Rates applied across all consumption logs to calculate operational costs in INR (₹)
          </p>

          <div className="space-y-4">
            {rates.map((r) => (
              <div key={r.id} className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-800/40 p-4">
                <div>
                  <p className="text-sm font-bold text-white">{r.resource_type}</p>
                  <p className="text-xs text-slate-400">Billing Unit: {r.unit}</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5">
                    <span className="text-xs text-slate-400 mr-1">₹</span>
                    <input
                      type="number"
                      step="0.01"
                      defaultValue={r.rate}
                      onBlur={(e) => handleUpdateRate(r.id, e.target.value)}
                      className="w-20 bg-transparent text-sm font-bold text-white focus:outline-none"
                    />
                    <span className="text-xs text-slate-400 ml-1">/ {r.unit}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Demo Database Re-seed */}
        <div className="rounded-2xl border border-rose-500/30 bg-rose-500/5 p-6 shadow-xl">
          <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
            <ShieldAlert className="h-4 w-4 text-rose-400" />
            Demo Data & Environment Reset
          </h3>
          <p className="text-xs text-slate-400 mb-4">
            Re-populates all 8 blocks, 1,440+ historical consumption rows, pre-trains Random Forest models, and generates initial anomaly alerts.
          </p>
          <button
            onClick={handleReseed}
            disabled={reseedLoading}
            className="flex items-center gap-2 rounded-xl bg-rose-500 px-4 py-2.5 text-xs font-bold text-white hover:bg-rose-600 transition-all cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${reseedLoading ? "animate-spin" : ""}`} />
            <span>{reseedLoading ? "Re-seeding Database & Training ML..." : "Re-Seed Complete Demo Database"}</span>
          </button>
        </div>
      </main>
    </div>
  );
};
'''
    with open(os.path.join(FRONTEND_DIR, "Settings.jsx"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print("Wrote Settings.jsx")

if __name__ == "__main__":
    write_maintenance()
    write_reports()
    write_settings()
