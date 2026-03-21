import api from "./client";

export const fetchOverview = async () => {
  const res = await api.get("dashboard/overview/");
  return res.data;
};

export const fetchLeads = async () => {
  const res = await api.get("dashboard/leads/");
  return res.data;
};

export const fetchEscalations = async () => {
  const res = await api.get("dashboard/escalations/");
  return res.data;
};
