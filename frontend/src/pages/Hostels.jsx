import React, { useState, useEffect } from "react";
import { Building2, Users, Plus, Edit2, Trash2, ShieldCheck, MapPin } from "lucide-react";
import { hostelsAPI } from "../services/api";
import { Header } from "../components/common/Header";
import { Modal } from "../components/common/Modal";
import { StatusBadge } from "../components/common/StatusBadge";
import { useAuth } from "../contexts/AuthContext";

export const Hostels = () => {
  const { role } = useAuth();
  const [hostels, setHostels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingHostel, setEditingHostel] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    block: "",
    capacity: 300,
    current_occupancy: 280,
    location: "North Campus",
    status: "Active"
  });

  const loadHostels = () => {
    setLoading(true);
    hostelsAPI.list()
      .then((res) => setHostels(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadHostels();
  }, []);

  const handleOpenAdd = () => {
    setEditingHostel(null);
    setFormData({
      name: "",
      block: "",
      capacity: 300,
      current_occupancy: 280,
      location: "North Campus",
      status: "Active"
    });
    setModalOpen(true);
  };

  const handleOpenEdit = (h) => {
    setEditingHostel(h);
    setFormData({
      name: h.name,
      block: h.block,
      capacity: h.capacity,
      current_occupancy: h.current_occupancy,
      location: h.location,
      status: h.status
    });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingHostel) {
        await hostelsAPI.update(editingHostel.id, formData);
      } else {
        await hostelsAPI.create(formData);
      }
      setModalOpen(false);
      loadHostels();
    } catch (err) {
      alert(err.response?.data?.detail || "Operation failed");
    }
  };

  const handleDelete = async (id, name) => {
    if (window.confirm(`Are you sure you want to delete ${name}?`)) {
      try {
        await hostelsAPI.delete(id);
        loadHostels();
      } catch (err) {
        alert(err.response?.data?.detail || "Delete failed");
      }
    }
  };

  return (
    <div className="flex-1 min-h-screen bg-slate-50/60 pb-16">
      <Header
        title="Hostel Blocks & Infrastructure Management"
        subtitle="Manage residential wings, bed capacities, and active block assignments"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-extrabold text-slate-900">Configured Hostels ({hostels.length})</h2>
            <p className="text-xs text-slate-500 font-medium">Real-time capacity and occupancy metrics</p>
          </div>
          {role === "admin" && (
            <button
              onClick={handleOpenAdd}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 transition-all cursor-pointer"
            >
              <Plus className="h-4 w-4" />
              <span>Add Hostel Block</span>
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {hostels.map((h) => {
            const occPct = h.occupancy_rate || Math.round((h.current_occupancy / h.capacity) * 100);
            return (
              <div
                key={h.id}
                className="relative flex flex-col justify-between rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm transition-all hover:shadow-md hover:border-sky-200"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="rounded-lg bg-sky-50 border border-sky-200 px-2.5 py-0.5 text-xs font-extrabold text-sky-700">
                      {h.block}
                    </span>
                    <StatusBadge status={h.status} />
                  </div>

                  <h3 className="mt-3 text-sm font-bold text-slate-900 leading-snug">{h.name}</h3>
                  <p className="mt-1 flex items-center gap-1 text-xs text-slate-500 font-medium">
                    <MapPin className="h-3.5 w-3.5 text-slate-400" />
                    {h.location}
                  </p>

                  <div className="mt-5 space-y-2">
                    <div className="flex justify-between text-xs font-semibold text-slate-700">
                      <span>Occupancy:</span>
                      <span className="text-slate-900 font-extrabold">{h.current_occupancy} / {h.capacity} Beds</span>
                    </div>
                    <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${occPct > 95 ? "bg-amber-500" : "bg-sky-500"}`}
                        style={{ width: `${Math.min(100, occPct)}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-[11px] text-slate-500">
                      <span>Occupancy Rate</span>
                      <span className="font-extrabold text-sky-600">{occPct}%</span>
                    </div>
                  </div>
                </div>

                {role === "admin" && (
                  <div className="mt-6 flex items-center justify-end gap-2 border-t border-slate-100 pt-3">
                    <button
                      onClick={() => handleOpenEdit(h)}
                      className="rounded-lg p-1.5 text-slate-500 hover:bg-slate-100 hover:text-slate-800 transition-colors cursor-pointer"
                      title="Edit Hostel"
                    >
                      <Edit2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(h.id, h.name)}
                      className="rounded-lg p-1.5 text-slate-500 hover:bg-rose-50 hover:text-rose-600 transition-colors cursor-pointer"
                      title="Delete Hostel"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </main>

      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingHostel ? `Edit ${editingHostel.name}` : "Add New Hostel Block"}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Hostel Name</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. Himalaya Boys Hostel"
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Block Identifier</label>
              <input
                type="text"
                required
                value={formData.block}
                onChange={(e) => setFormData({ ...formData, block: e.target.value })}
                placeholder="e.g. Block A"
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              >
                <option value="Active">Active</option>
                <option value="Maintenance">Maintenance</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Bed Capacity</label>
              <input
                type="number"
                required
                value={formData.capacity}
                onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Current Occupancy</label>
              <input
                type="number"
                required
                value={formData.current_occupancy}
                onChange={(e) => setFormData({ ...formData, current_occupancy: parseInt(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Campus Location</label>
            <input
              type="text"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              placeholder="e.g. North Campus - Wing A"
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setModalOpen(false)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-md shadow-sky-500/20 hover:from-sky-600 hover:to-indigo-700 cursor-pointer"
            >
              {editingHostel ? "Save Changes" : "Create Hostel"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
