import api from "../../api/client";



export const getSummary = () => api.get("/analytics/summary/");
export const getFunnel = () => api.get("/analytics/funnel/");
export const getAgents = () => api.get("/analytics/agents/");
export const getSLA = () => api.get("/analytics/sla/");
export const getAIImpact = () => api.get("/analytics/ai-impact/");
