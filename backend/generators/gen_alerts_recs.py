import os

FRONTEND_DIR = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages"

def write_alerts():
    code = '''import React, { useState, useEffect } from "react";
import { AlertTriangle, Filter, Wrench, CheckCircle, RefreshCw } from "lucide-react";
import { alertsAPI, anomaliesAPI, hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { StatusBadge } from "../components/common/StatusBadge";
import { Modal } from "../components/common/Modal";

export const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [hostels, setHostels] = useState([]);
  const [selectedHostel, setSelectedHostel] = useState("");
  const [selectedSeverity, setSelectedSeverity] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [ticketModalOpen, setTicketModalOpen] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [ticketData, setTicketData] = useState({ priority: "High", assigned_to: "Vikram Singh", notes: "" });
  const [scanning, setScanning] = useState(false);

  const loadAlerts = () => {
    setLoading(true);
    const params = {
      ...(selectedHostel ? { hostel_id: selectedHostel } : {}),
      ...(selectedSeverity ? { severity: selectedSeverity } : {}),
      ...(selectedStatus ? { status: selectedStatus } : {})
    };

    Promise.all([alertsAPI.list(params), hostelsAPI.list()])
      .then(([aRes, hRes]) => {
        setAlerts(aRes.data);
        setHostels(hRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadAlerts();
  }, [selectedHostel, selectedSeverity, selectedStatus]);

  const handleRunScan = async () => {
    setScanning(true);
    try {
      await anomaliesAPI.detect();
      loadAlerts();
    } catch (err) {
      alert("Scan failed");
    } finally {
      setScanning(false);
    }
  };

  const handleOpenTicketModal = (alertObj) => {
    setSelectedAlert(alertObj);
    setTicketData({
      priority: alertObj.severity,
      assigned_to: "Vikram Singh",
      notes: `Escalated from Alert #${alertObj.id} (${alertObj.difference_percentage}% surge)`
    });
    setTicketModalOpen(true);
  };

  const handleCreateTicket = async (e) => {
    e.preventDefault();
    if (!selectedAlert) return;
    try {
      await alertsAPI.convertToTicket(selectedAlert.id, ticketData);
      setTicketModalOpen(false);
      loadAlerts();
      alert("Maintenance ticket dispatched successfully!");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to convert alert to ticket");
    }
  };

  const handleUpdateStatus = async (id, status) => {
    try {
      await alertsAPI.updateStatus(id, status);
      loadAlerts();
    } catch (err) {
      alert("Update failed");
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Anomaly Detection & Alert Management"
        subtitle="Active consumption surges flagged by Isolation Forest models"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Filters and Scan trigger */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
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
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>

            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="rounded-xl border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white focus:outline-none"
            >
              <option value="">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Reviewed">Reviewed</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>

          <button
            onClick={handleRunScan}
            disabled={scanning}
            className="flex items-center gap-2 rounded-xl bg-amber-500 px-4 py-2 text-xs font-bold text-white hover:bg-amber-400 transition-all cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${scanning ? "animate-spin" : ""}`} />
            <span>{scanning ? "Evaluating Isolation Forest..." : "Trigger Anomaly Scan"}</span>
          </button>
        </div>

        {/* Alerts Grid */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
          <h3 className="text-sm font-bold text-white mb-4">Live Anomaly Alerts Queue ({alerts.length})</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-3 rounded-l-xl">Severity</th>
                  <th className="px-4 py-3">Hostel</th>
                  <th className="px-4 py-3">Resource</th>
                  <th className="px-4 py-3">Actual / Baseline</th>
                  <th className="px-4 py-3">Surge %</th>
                  <th className="px-4 py-3">Description</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 rounded-r-xl">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {alerts.map((a) => (
                  <tr key={a.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3"><StatusBadge status={a.severity} /></td>
                    <td className="px-4 py-3 font-semibold text-white">{a.hostel_name} ({a.hostel_block})</td>
                    <td className="px-4 py-3">{a.resource_type}</td>
                    <td className="px-4 py-3 font-mono">
                      <span className="text-white font-bold">{a.actual_value.toLocaleString()}</span> /{" "}
                      <span className="text-slate-400">{a.expected_value.toLocaleString()}</span>
                    </td>
                    <td className="px-4 py-3 font-bold text-rose-400">+{a.difference_percentage}%</td>
                    <td className="px-4 py-3 text-slate-400 max-w-xs">{a.description}</td>
                    <td className="px-4 py-3"><StatusBadge status={a.status} /></td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        {a.status !== "Resolved" && (
                          <button
                            onClick={() => handleOpenTicketModal(a)}
                            className="flex items-center gap-1 rounded-lg bg-sky-500/20 border border-sky-500/30 px-2 py-1 text-[11px] font-bold text-sky-400 hover:bg-sky-500/30 transition-colors cursor-pointer"
                            title="Convert to Maintenance Work Order"
                          >
                            <Wrench className="h-3 w-3" />
                            <span>Dispatch Ticket</span>
                          </button>
                        )}
                        {a.status === "Active" && (
                          <button
                            onClick={() => handleUpdateStatus(a.id, "Resolved")}
                            className="rounded-lg p-1 text-slate-400 hover:text-emerald-400 transition-colors cursor-pointer"
                            title="Mark Resolved"
                          >
                            <CheckCircle className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Convert to Ticket Modal */}
      <Modal
        isOpen={ticketModalOpen}
        onClose={() => setTicketModalOpen(false)}
        title={selectedAlert ? `Create Maintenance Ticket for Alert #${selectedAlert.id}` : "Dispatch Maintenance"}
      >
        <form onSubmit={handleCreateTicket} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Issue Priority</label>
            <select
              value={ticketData.priority}
              onChange={(e) => setTicketData({ ...ticketData, priority: e.target.value })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            >
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Assign Maintenance Technician</label>
            <input
              type="text"
              required
              value={ticketData.assigned_to}
              onChange={(e) => setTicketData({ ...ticketData, assigned_to: e.target.value })}
              placeholder="e.g. Vikram Singh (Plumbing & Electrical Lead)"
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Investigation Notes & Instructions</label>
            <textarea
              rows={3}
              value={ticketData.notes}
              onChange={(e) => setTicketData({ ...ticketData, notes: e.target.value })}
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={() => setTicketModalOpen(false)}
              className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white hover:bg-sky-400 cursor-pointer"
            >
              Confirm & Dispatch Ticket
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
'''
    with open(os.path.join(FRONTEND_DIR, "Alerts.jsx"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print("Wrote Alerts.jsx")

def write_recommendations():
    code = '''import React, { useState, useEffect } from "react";
import { Lightbulb, IndianRupee, Droplets, Zap, Flame, Users, CheckCircle2, ArrowRight } from "lucide-react";
import { recommendationsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { StatusBadge } from "../components/common/StatusBadge";

export const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    recommendationsAPI.list()
      .then((res) => setRecommendations(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const totalPotentialSavings = recommendations.reduce(
    (acc, curr) => acc + (curr.estimated_monthly_savings || 0), 0
  );

  return (
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Smart Actionable Recommendations Engine"
        subtitle="Explainable rule & ML-driven interventions to eliminate utility wastage"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Banner with Total Savings */}
        <div className="rounded-2xl border border-emerald-500/30 bg-gradient-to-r from-emerald-500/10 via-slate-900 to-sky-500/10 p-6 backdrop-blur-md shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <span className="rounded-full bg-emerald-500/20 border border-emerald-500/30 px-3 py-1 text-xs font-bold text-emerald-400">
              Optimization Potential
            </span>
            <h2 className="mt-2 text-lg font-bold text-white">
              Estimated Monthly Savings: <span className="text-emerald-400 font-extrabold">₹{totalPotentialSavings.toLocaleString()}</span>
            </h2>
            <p className="text-xs text-slate-400">
              Based on historical baseline reduction across {recommendations.length} identified efficiency targets
            </p>
          </div>
          <button
            onClick={() => alert("Recommendations printed for institutional facilities committee review.")}
            className="flex items-center gap-2 rounded-xl bg-emerald-500 px-4 py-2.5 text-xs font-bold text-white shadow-lg shadow-emerald-500/25 hover:bg-emerald-400 transition-all cursor-pointer"
          >
            <Lightbulb className="h-4 w-4" />
            <span>Export Action Plan</span>
          </button>
        </div>

        {/* Recommendation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendations.map((rec) => (
            <div
              key={rec.id}
              className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl backdrop-blur-md flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <div className="flex items-center gap-2">
                    {rec.category === "Water" && <Droplets className="h-4 w-4 text-sky-400" />}
                    {rec.category === "Electricity" && <Zap className="h-4 w-4 text-amber-400" />}
                    {rec.category === "Gas" && <Flame className="h-4 w-4 text-rose-400" />}
                    {rec.category === "Occupancy" && <Users className="h-4 w-4 text-purple-400" />}
                    <span className="text-xs font-bold text-white">{rec.hostel_name}</span>
                  </div>
                  <span className="rounded-full bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 text-xs font-bold text-emerald-400">
                    Save ~₹{rec.estimated_monthly_savings.toLocaleString()} / mo
                  </span>
                </div>

                <h3 className="mt-4 text-sm font-bold text-white leading-snug">{rec.title}</h3>
                <p className="mt-1 text-xs text-slate-400 leading-relaxed">{rec.description}</p>

                <div className="mt-4 rounded-xl bg-slate-800/60 p-3">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                    Recommended Action Checklist:
                  </p>
                  <ul className="space-y-1.5 text-xs text-slate-300">
                    {rec.suggested_actions.map((act, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle2 className="h-3.5 w-3.5 text-sky-400 flex-shrink-0 mt-0.5" />
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mt-5 border-t border-slate-800 pt-3">
                <p className="text-[11px] text-slate-400">
                  🔬 <strong>Rationale:</strong> {rec.reasoning}
                </p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};
'''
    with open(os.path.join(FRONTEND_DIR, "Recommendations.jsx"), "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print("Wrote Recommendations.jsx")

if __name__ == "__main__":
    write_alerts()
    write_recommendations()
