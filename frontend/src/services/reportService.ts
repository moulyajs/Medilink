import { Platform } from "react-native";
import api from "./api";

export async function uploadReport(file: any) {
  const formData = new FormData();

  if (Platform.OS === "web" && file.file) {
    formData.append("file", file.file);
  } else {
    formData.append("file", {
      uri: file.uri,
      name: file.fileName || file.name || "upload.jpg",
      type: file.mimeType || file.type || "image/jpeg",
    } as any);
  }

  const response = await api.post(
    "/reports/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}