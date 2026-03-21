import axios from "axios";

export const getLeads = async () => {
  const response = await axios.get("/api/leads/");
  return response.data;
};
