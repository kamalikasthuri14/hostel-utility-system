import React, { useState, useEffect } from "react";
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
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Maintenance Management & Work Order Dispatch"
        subtitle="Track utility leaks, power surge repairs, and technician work order lifecycles"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Controls */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
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
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:bg-white transition-all"
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
            className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 transition-all cursor-pointer"
          >
            <Plus className="h-4 w-4" />
            <span>Create Work Order</span>
          </button>
        </div>

        {/* Tickets Table */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm">
          <h3 className="text-sm font-extrabold text-slate-900 mb-4">Active Work Orders ({tickets.length})</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-b border-slate-100">
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
              <tbody className="divide-y divide-slate-100">
                {tickets.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-sky-700">#{t.id}</td>
                    <td className="px-4 py-3 font-bold text-slate-900">{t.hostel_name} ({t.hostel_block})</td>
                    <td className="px-4 py-3 font-semibold">{t.resource_type}</td>
                    <td className="px-4 py-3 text-slate-800 font-medium">{t.issue_type}</td>
                    <td className="px-4 py-3"><StatusBadge status={t.priority} /></td>
                    <td className="px-4 py-3 text-slate-700">{t.assigned_to || "Unassigned"}</td>
                    <td className="px-4 py-3"><StatusBadge status={t.status} /></td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => handleOpenEdit(t)}
                        className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-[11px] font-bold text-sky-700 hover:bg-sky-50 hover:text-sky-800 hover:border-sky-300 transition-colors cursor-pointer shadow-xs"
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
            <label className="block text-xs font-bold text-slate-700 mb-1">Hostel Block</label>
            <select
              value={formData.hostel_id}
              onChange={(e) => setFormData({ ...formData, hostel_id: parseInt(e.target.value) })}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            >
              {hostels.map((h) => (
                <option key={h.id} value={h.id}>{h.name} ({h.block})</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Resource</label>
              <select
                value={formData.resource_type}
                onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              >
                <option value="Water">Water</option>
                <option value="Electricity">Electricity</option>
                <option value="Gas">Gas</option>
                <option value="General">General</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Issue Headline</label>
            <input
              type="text"
              required
              value={formData.issue_type}
              onChange={(e) => setFormData({ ...formData, issue_type: e.target.value })}
              placeholder="e.g. Tank float valve malfunction"
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Detailed Description</label>
            <textarea
              rows={3}
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Describe symptoms, location on floor, observed leakage..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setCreateModalOpen(false)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 cursor-pointer"
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
              <label className="block text-xs font-bold text-slate-700 mb-1">Status</label>
              <select
                value={updateData.status}
                onChange={(e) => setUpdateData({ ...updateData, status: e.target.value })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              >
                <option value="Open">Open</option>
                <option value="Assigned">Assigned</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Priority</label>
              <select
                value={updateData.priority}
                onChange={(e) => setUpdateData({ ...updateData, priority: e.target.value })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Assigned Technician</label>
            <input
              type="text"
              value={updateData.assigned_to}
              onChange={(e) => setUpdateData({ ...updateData, assigned_to: e.target.value })}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Add Maintenance Note / Progress Update</label>
            <textarea
              rows={3}
              value={updateData.notes}
              onChange={(e) => setUpdateData({ ...updateData, notes: e.target.value })}
              placeholder="e.g. Replaced 2-inch copper valve on riser pipe. Tested water pressure."
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          {activeTicket?.notes && (
            <div className="rounded-xl bg-slate-50 border border-slate-200 p-3 text-xs text-slate-700 whitespace-pre-wrap font-mono">
              <p className="font-bold text-slate-500 mb-1 font-sans">Activity Log History:</p>
              {activeTicket.notes}
            </div>
          )}

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setEditModalOpen(false)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 cursor-pointer"
            >
              Update Work Order
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
