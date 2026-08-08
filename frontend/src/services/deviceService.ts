import api from "./api";

export interface Device {
  device_id: string;
  session_id: string;      // <-- add this
  device_name: string;
  device_type: string;
  device_os: string;
  last_active: string;
  is_current: boolean;
  created_at: string;
}

export const getDevices = async () => {
  const response = await api.get("/devices");
  return response.data.devices;
};

export const removeDevice = async (
  deviceId: string
) => {
  await api.delete(`/devices/${deviceId}`);
};