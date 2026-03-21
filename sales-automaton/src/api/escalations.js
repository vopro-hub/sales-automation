import axios from "axios";

export const getEscalations = async () => {
  const response = await axios.get("/api/escalations/");
  return response.data;
};
