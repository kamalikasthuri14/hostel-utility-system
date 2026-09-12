import os

target = r"C:\Users\kamal\.gemini\antigravity\scratch\hostel-utility-optimization\frontend\src\pages\Hostels.jsx"
code = '''import React, { useState, useEffect } from "react";
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
    <div className="flex-1 min-h-screen bg-slate-950 pb-16">
      <Header
        title="Hostel Blocks & Infrastructure Management"
        subtitle="Manage residential wings, bed capacities, and active block assignments"
      />

      <main className="p-8 max-w-7xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Configured Hostels ({hostels.length})</h2>
            <p className="text-xs text-slate-400">Real-time capacity and occupancy metrics</p>
          </div>
          {role === "admin" && (
            <button
              onClick={handleOpenAdd}
              className="flex items-center gap-2 rounded-xl bg-sky-500 px-4 py-2 text-xs font-bold text-white shadow-lg shadow-sky-500/20 hover:bg-sky-400 transition-all cursor-pointer"
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
                className="relative flex flex-col justify-between rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg backdrop-blur-md transition-all hover:border-slate-700"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="rounded-lg bg-sky-500/10 border border-sky-500/20 px-2.5 py-0.5 text-xs font-bold text-sky-400">
                      {h.block}
                    </span>
                    <StatusBadge status={h.status} />
                  </div>

                  <h3 className="mt-3 text-sm font-bold text-white leading-snug">{h.name}</h3>
                  <p className="mt-1 flex items-center gap-1 text-xs text-slate-400">
                    <MapPin className="h-3 w-3 text-slate-500" />
                    {h.location}
                  </p>

                  <div className="mt-5 space-y-2">
                    <div className="flex justify-between text-xs font-semibold text-slate-300">
                      <span>Occupancy:</span>
                      <span className="text-white font-bold">{h.current_occupancy} / {h.capacity} Beds</span>
                    </div>
                    <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${occPct > 95 ? "bg-amber-500" : "bg-sky-500"}`}
                        style={{ width: `${Math.min(100, occPct)}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-[11px] text-slate-400">
                      <span>Occupancy Rate</span>
                      <span className="font-bold text-sky-400">{occPct}%</span>
                    </div>
                  </div>
                </div>

                {role === "admin" && (
                  <div className="mt-6 flex items-center justify-end gap-2 border-t border-slate-800/80 pt-3">
                    <button
                      onClick={() => handleOpenEdit(h)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer"
                      title="Edit Hostel"
                    >
                      <Edit2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(h.id, h.name)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-500/10 hover:text-rose-400 transition-colors cursor-pointer"
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
            <label className="block text-xs font-semibold text-slate-300 mb-1">Hostel Name</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. Himalaya Boys Hostel"
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-sky-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Block Identifier</label>
              <input
                type="text"
                required
                value={formData.block}
                onChange={(e) => setFormData({ ...formData, block: e.target.value })}
                placeholder="e.g. Block A"
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-sky-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-sky-500 focus:outline-none"
              >
                <option value="Active">Active</option>
                <option value="Maintenance">Maintenance</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Bed Capacity</label>
              <input
                type="number"
                required
                value={formData.capacity}
                onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-sky-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Current Occupancy</label>
              <input
                type="number"
                required
                value={formData.current_occupancy}
                onChange={(e) => setFormData({ ...formData, current_occupancy: parseInt(e.target.value) || 0 })}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-sky-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Campus Location</label>
            <input
              type="text"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              placeholder="e.g. North Campus - Wing A"
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-sky-500 focus:outline-none"
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
              {editingHostel ? "Save Changes" : "Create Hostel"}
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
print("Hostels.jsx generated.")
