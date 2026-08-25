import api from "./api";
import { TimelineItem } from "../types/timeline";
import * as FileSystem from "expo-file-system/legacy";
import * as Sharing from "expo-sharing";

export const getTimeline = async (): Promise<TimelineItem[]> => {
  try {
    const response = await api.get("/timeline/");
    return response.data;
  } catch (error) {
    console.error("Timeline API Error:", error);
    return [];
  }
};

// ------------------------------------------------------
// WEB DOCUMENT VIEW
// ------------------------------------------------------

export const viewDocument = async (
  documentId: string
): Promise<string> => {
  try {
    console.log("VIEW DOCUMENT ID:", documentId);

    const response = await api.get(
      `/document/${documentId}`,
      {
        responseType: "blob",
      }
    );

    const blobUrl = URL.createObjectURL(
      response.data
    );

    console.log(
      "DOCUMENT BLOB URL:",
      blobUrl
    );

    return blobUrl;
  } catch (error: any) {
    console.error(
      "Document View Error:",
      error
    );

    console.error(
      "Response:",
      error?.response
    );

    throw error;
  }
};

// ------------------------------------------------------
// MOBILE DOCUMENT VIEW
// ------------------------------------------------------

export const viewDocumentMobile = async (
  documentId: string
): Promise<void> => {
  try {
    console.log(
      "MOBILE VIEW DOCUMENT:",
      documentId
    );

    const response = await api.get(
      `/document/${documentId}`,
      {
        responseType: "arraybuffer",
      }
    );

    const bytes = new Uint8Array(
      response.data
    );

    let binary = "";

    const chunkSize = 8192;

    for (
      let i = 0;
      i < bytes.length;
      i += chunkSize
    ) {
      const chunk = bytes.subarray(
        i,
        Math.min(
          i + chunkSize,
          bytes.length
        )
      );

      binary += String.fromCharCode(
        ...chunk
      );
    }

    const base64 = btoa(binary);

    const fileUri =
      FileSystem.cacheDirectory +
      `medical-document-${documentId}.pdf`;

    await FileSystem.writeAsStringAsync(
      fileUri,
      base64,
      {
        encoding:
          FileSystem.EncodingType.Base64,
      }
    );

    console.log(
      "DOCUMENT SAVED:",
      fileUri
    );

    const sharingAvailable =
      await Sharing.isAvailableAsync();

    if (!sharingAvailable) {
      throw new Error(
        "Document sharing is not available on this device."
      );
    }

    await Sharing.shareAsync(
      fileUri,
      {
        mimeType: "application/pdf",
        dialogTitle:
          "Open Medical Document",
        UTI: "com.adobe.pdf",
      }
    );

  } catch (error: any) {
    console.error(
      "Mobile Document View Error:",
      error
    );

    console.error(
      "Response:",
      error?.response
    );

    throw error;
  }
};