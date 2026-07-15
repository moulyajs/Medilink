import api from "./api";

export interface Profile {
  id?: number;
  name: string;
  email: string;
  phone: string;
  gender: string;
  blood_group: string;
  dob: string;
  address: string;
  emergency_contact: string;
  profile_image: string;
}

/* ---------------- Get Profile ---------------- */

export const getProfile = async (
  id: number
): Promise<Profile> => {

  try {

    const response = await api.get<Profile>(
      `/profile/${id}`
    );

    return response.data;

  } catch (error) {

    console.error("Get Profile Error:", error);

    throw error;

  }

};

/* ---------------- Create Profile ---------------- */

export const createProfile = async (
  profile: Profile
): Promise<Profile> => {

  try {

    const response = await api.post<Profile>(
      "/profile/",
      profile
    );

    return response.data;

  } catch (error) {

    console.error("Create Profile Error:", error);

    throw error;

  }

};

/* ---------------- Update Profile ---------------- */

export const updateProfile = async (
  id: number,
  profile: Profile
): Promise<Profile> => {

  try {

    const response = await api.put<Profile>(
      `/profile/${id}`,
      profile
    );

    return response.data;

  } catch (error) {

    console.error("Update Profile Error:", error);

    throw error;

  }

};

/* ---------------- Delete Profile ---------------- */

export const deleteProfile = async (
  id: number
) => {

  try {

    const response = await api.delete(
      `/profile/${id}`
    );

    return response.data;

  } catch (error) {

    console.error("Delete Profile Error:", error);

    throw error;

  }

};