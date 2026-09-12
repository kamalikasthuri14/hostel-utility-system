import React, { useState, useEffect } from "react";
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
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Anomaly Detection & Alert Management"
        subtitle="Active consumption surges flagged by Isolation Forest models"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Filters and Scan trigger */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
          <div className="flex flex-wrap items-center gap-3">
            <Filter className="h-4 w-4 text-sky-600" />
            <select
              value={selectedHostel}
              onChange={(e) => setSelectedHostel(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:bg-white transition-all"
            >
              <option value="">All Hostels</option>
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.block}</option>
              ))}
            </select>

            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:bg-white transition-all"
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
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:bg-white transition-all"
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
            className="flex items-center gap-2 rounded-xl bg-amber-500 px-4 py-2 text-xs font-bold text-white hover:bg-amber-600 transition-all shadow-md shadow-amber-500/20 cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${scanning ? "animate-spin" : ""}`} />
            <span>{scanning ? "Evaluating Isolation Forest..." : "Trigger Anomaly Scan"}</span>
          </button>
        </div>

        {/* Alerts Grid */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
          <h3 className="text-sm font-extrabold text-slate-900 mb-4">Live Anomaly Alerts Queue ({alerts.length})</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-b border-slate-100">
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
              <tbody className="divide-y divide-slate-100">
                {alerts.map((a) => (
                  <tr key={a.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-4 py-3"><StatusBadge status={a.severity} /></td>
                    <td className="px-4 py-3 font-bold text-slate-900">{a.hostel_name} ({a.hostel_block})</td>
                    <td className="px-4 py-3 font-semibold">{a.resource_type}</td>
                    <td className="px-4 py-3 font-mono">
                      <span className="text-slate-900 font-bold">{a.actual_value.toLocaleString()}</span> /{" "}
                      <span className="text-slate-500">{a.expected_value.toLocaleString()}</span>
                    </td>
                    <td className="px-4 py-3 font-extrabold text-rose-600">+{a.difference_percentage}%</td>
                    <td className="px-4 py-3 text-slate-600 max-w-xs">{a.description}</td>
                    <td className="px-4 py-3"><StatusBadge status={a.status} /></td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        {a.status !== "Resolved" && (
                          <button
                            onClick={() => handleOpenTicketModal(a)}
                            className="flex items-center gap-1 rounded-lg bg-sky-50 border border-sky-200 px-2 py-1 text-[11px] font-bold text-sky-700 hover:bg-sky-100 transition-colors cursor-pointer shadow-xs"
                            title="Convert to Maintenance Work Order"
                          >
                            <Wrench className="h-3 w-3 text-sky-600" />
                            <span>Dispatch Ticket</span>
                          </button>
                        )}
                        {a.status === "Active" && (
                          <button
                            onClick={() => handleUpdateStatus(a.id, "Resolved")}
                            className="rounded-lg p-1 text-slate-400 hover:text-emerald-600 transition-colors cursor-pointer"
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
            <label className="block text-xs font-bold text-slate-700 mb-1">Issue Priority</label>
            <select
              value={ticketData.priority}
              onChange={(e) => setTicketData({ ...ticketData, priority: e.target.value })}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            >
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Assign Maintenance Technician</label>
            <input
              type="text"
              required
              value={ticketData.assigned_to}
              onChange={(e) => setTicketData({ ...ticketData, assigned_to: e.target.value })}
              placeholder="e.g. Vikram Singh (Plumbing & Electrical Lead)"
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Investigation Notes & Instructions</label>
            <textarea
              rows={3}
              value={ticketData.notes}
              onChange={(e) => setTicketData({ ...ticketData, notes: e.target.value })}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setTicketModalOpen(false)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 cursor-pointer"
            >
              Confirm & Dispatch Ticket
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
