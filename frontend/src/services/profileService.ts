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
export interface UpdateProfileRequest {
  name?: string;
  phone?: string;
  gender?: string;
  blood_group?: string;
  dob?: string;
  address?: string;
  emergency_contact?: string;
  profile_image?: string;
}
/* ---------------- Get Profile ---------------- */

export const getProfile = async (): Promise<Profile> => {
  const response = await api.get<Profile>("/profile/me");
  return response.data;
};



/* ---------------- Update Profile ---------------- */

export const updateProfile = async (
  profile: UpdateProfileRequest
): Promise<Profile> => {

  const response = await api.put<Profile>(
    "/profile/me",
    profile
  );

  return response.data;
};

