import React, { useEffect, useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Dimensions,
  Alert,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import * as ImagePicker from "expo-image-picker";

import ProfileImagePicker from "../../components/profile/ProfileImagePicker";
import CustomInput from "../../components/profile/CustomInput";
import CustomDropdown from "../../components/profile/CustomDropdown";
import PrimaryButton from "../../components/profile/PrimaryButton";
import DateTimePicker from "@react-native-community/datetimepicker";
import { getProfile, updateProfile } from "../../services/profileService";
import { useFocusEffect } from "@react-navigation/native";
import { useCallback } from "react";
import { useTheme } from "../../theme/ThemeContext";
const { width } = Dimensions.get("window");

export default function EditProfileScreen() {

  const navigation = useNavigation<any>();
  const { colors, darkMode } = useTheme();

  const [image, setImage] = useState("");

  const [name, setName] = useState("");
const [email, setEmail] = useState("");
const [phone, setPhone] = useState("");
const [dob, setDob] = useState("");
const [gender, setGender] = useState("");
const [blood, setBlood] = useState("");
const [address, setAddress] = useState("");
const [emergency, setEmergency] = useState("");

const [showGenderMenu, setShowGenderMenu] = useState(false);

const [showBloodMenu, setShowBloodMenu] = useState(false);
const [showDatePicker, setShowDatePicker] = useState(false);

const loadProfile = async () => {
  try {
    const profile = await getProfile();

    setName(profile.name ?? "");
    setEmail(profile.email ?? "");
    setPhone(profile.phone ?? "");
    setDob(profile.dob ?? "");
    setGender(profile.gender ?? "");
    setBlood(profile.blood_group ?? "");
    setAddress(profile.address ?? "");
    setEmergency(profile.emergency_contact ?? "");
    setImage(profile.profile_image ?? "");

  } catch (error) {
    console.log(error);
  }
};
useFocusEffect(
  useCallback(() => {
    loadProfile();
  }, [])
);

  async function pickImage() {

    const permission =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permission.granted) {

      Alert.alert(
        "Permission Required",
        "Gallery permission is needed."
      );

      return;
    }

    const result =
      await ImagePicker.launchImageLibraryAsync({

        mediaTypes:
          ImagePicker.MediaTypeOptions.Images,

        allowsEditing: true,

        aspect: [1, 1],

        quality: 1,

      });

    if (!result.canceled) {

      setImage(result.assets[0].uri);

    }

  }

 const saveProfile = async () => {

  try {

    await updateProfile({
  name,
  phone,
  gender,
  blood_group: blood,
  dob,
  address,
  emergency_contact: emergency,
  profile_image: image,
});

    Alert.alert(
      "Success",
      "Profile Updated Successfully!"
    );

    navigation.goBack();

  } catch (error) {

    console.log(error);

    Alert.alert(
      "Error",
      "Unable to update profile."
    );

  }

};

  return (<SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>

  <ScrollView
    showsVerticalScrollIndicator={false}
    contentContainerStyle={styles.scroll}
  >

    {/* Header */}

    <LinearGradient
      colors={
        darkMode
          ? ["#1F2A3D", "#22314A", "#1A2740"]
          : ["#5D9DFF", "#4E89B9", "#3B73C5"]
      }
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.header}
    >

      {/* Top Row */}

      <View style={styles.headerRow}>

        <TouchableOpacity
          onPress={() => navigation.goBack()}
        >

          <Ionicons
            name="arrow-back"
            size={24}
            color="#FFFFFF"
          />

        </TouchableOpacity>

        <Text style={styles.headerTitle}>
          Edit Profile
        </Text>

        <TouchableOpacity>

          <Ionicons
            name="settings-outline"
            size={22}
            color="#FFFFFF"
          />

        </TouchableOpacity>

      </View>

      {/* Subtitle */}

      <Text style={styles.headerSubtitle}>
        Manage your personal medical identity
      </Text>

      {/* Avatar */}

      <View style={styles.avatarContainer}>

        <ProfileImagePicker
          image={image}
          onPress={pickImage}
        />

      </View>

    </LinearGradient>

    {/* Personal Information */}

    <View
      style={[
        styles.card,
        {
          backgroundColor: colors.card,
          borderColor: colors.border,
          shadowColor: colors.shadow,
        },
      ]}
    >

      <View style={styles.cardHeader}>

        <Ionicons
          name="person-circle-outline"
          size={24}
          color={colors.primary}
        />

        <Text style={[styles.sectionTitle, { color: colors.text }]}>
          Personal Information
        </Text>

      </View>

      <CustomInput
        label="Full Name"
        value={name}
        onChangeText={setName}
        placeholder="Full Name"
        icon="person-outline"
      />

      <CustomInput
  label="Email"
  value={email}
  placeholder="Email Address"
  keyboardType="email-address"
  icon="mail-outline"
  editable={false}
/>

      <CustomInput
        label="Phone Number"
        value={phone}
        onChangeText={setPhone}
        placeholder="Phone Number"
        keyboardType="phone-pad"
        icon="call-outline"
      />

     <Text style={[styles.label, { color: colors.text }]}>
    Date of Birth
    </Text>

    <TouchableOpacity
    style={[
      styles.dropdown,
      {
        backgroundColor: colors.card,
        borderColor: colors.border,
      },
    ]}
    onPress={() => setShowDatePicker(true)}
    >

    <Ionicons
        name="calendar-outline"
        size={20}
        color={colors.primary}
    />

    <Text style={[styles.dropdownText, { color: colors.text }]}>
        {dob}
    </Text>

    </TouchableOpacity>

      <CustomDropdown
        label="Gender"
        value={gender}
        placeholder="Select Gender"
        onPress={() => setShowGenderMenu(true)}
      />
      {showGenderMenu && (

<View
  style={[
    styles.menu,
    {
      backgroundColor: colors.card,
      borderColor: colors.border,
    },
  ]}
>

  {["Male","Female","Other"].map(item=>(

    <TouchableOpacity

      key={item}

      style={[styles.menuItem, { borderBottomColor: colors.border }]}

      onPress={()=>{
        setGender(item);
        setShowGenderMenu(false);
      }}

    >

      <Text style={[styles.menuText, { color: colors.text }]}>
        {item}
      </Text>

    </TouchableOpacity>

  ))}

</View>

)}

      <CustomDropdown
        label="Blood Group"
        value={blood}
        placeholder="Select Blood Group"
        onPress={() => setShowBloodMenu(true)}
      />
      {showBloodMenu && (

<View
  style={[
    styles.menu,
    {
      backgroundColor: colors.card,
      borderColor: colors.border,
    },
  ]}
>

  {["A+","A-","B+","B-","AB+","AB-","O+","O-"].map(item=>(

    <TouchableOpacity

      key={item}

      style={[styles.menuItem, { borderBottomColor: colors.border }]}

      onPress={()=>{
        setBlood(item);
        setShowBloodMenu(false);
      }}

    >

      <Text style={[styles.menuText, { color: colors.text }]}>
        {item}
      </Text>

    </TouchableOpacity>

  ))}

</View>

)}
            <CustomInput
        label="Address"
        value={address}
        onChangeText={setAddress}
        placeholder="Enter your address"
        icon="location-outline"
        multiline
      />

      <CustomInput
        label="Emergency Contact"
        value={emergency}
        onChangeText={setEmergency}
        placeholder="Emergency phone number"
        keyboardType="phone-pad"
        icon="medkit-outline"
      />

    </View>

    {/* Health Summary */}

    <View
      style={[
        styles.healthCard,
        {
          backgroundColor: colors.card,
          shadowColor: colors.shadow,
        },
      ]}
    >

      <View style={styles.healthHeader}>

        <View style={styles.healthIcon}>

          <Ionicons
            name="heart"
            size={22}
            color="#FFFFFF"
          />

        </View>

        <View>

          <Text style={[styles.healthTitle, { color: colors.text }]}>
            Health Summary
          </Text>

          <Text style={[styles.healthSubtitle, { color: colors.subText }]}>
            Your medical profile overview
          </Text>

        </View>

      </View>

      {/* Stats */}

      <View style={styles.statsRow}>

        <View
          style={[
            styles.statCard,
            {
              backgroundColor: darkMode ? "#1F2733" : "#F4FAFF",
              borderColor: colors.border,
            },
          ]}
        >

          <Ionicons
            name="document-text-outline"
            size={26}
            color={colors.primary}
          />

          <Text style={[styles.statNumber, { color: colors.primary }]}>
            24
          </Text>

          <Text style={[styles.statLabel, { color: colors.subText }]}>
            Reports
          </Text>

        </View>

        <View
          style={[
            styles.statCard,
            {
              backgroundColor: darkMode ? "#1F2733" : "#F4FAFF",
              borderColor: colors.border,
            },
          ]}
        >

          <Ionicons
            name="pulse-outline"
            size={26}
            color={colors.primary}
          />

          <Text style={[styles.statNumber, { color: colors.primary }]}>
            18
          </Text>

          <Text style={[styles.statLabel, { color: colors.subText }]}>
            Timeline
          </Text>

        </View>

        <View
          style={[
            styles.statCard,
            {
              backgroundColor: darkMode ? "#1F2733" : "#F4FAFF",
              borderColor: colors.border,
            },
          ]}
        >

          <Ionicons
            name="sparkles-outline"
            size={26}
            color={colors.primary}
          />

          <Text style={[styles.statNumber, { color: colors.primary }]}>
            12
          </Text>

          <Text style={[styles.statLabel, { color: colors.subText }]}>
            AI Insights
          </Text>

        </View>

      </View>

      {/* Medical Details */}

      <View style={styles.infoRow}>

        <Text style={[styles.infoLabel, { color: colors.subText }]}>
          Blood Group
        </Text>

        <Text style={[styles.infoValue, { color: colors.text }]}>
          {blood}
        </Text>

      </View>

      <View style={styles.infoRow}>

        <Text style={[styles.infoLabel, { color: colors.subText }]}>
          Medical Profile
        </Text>

        <Text style={styles.activeStatus}>
          Active
        </Text>

      </View>

      <View style={styles.infoRow}>

        <Text style={[styles.infoLabel, { color: colors.subText }]}>
          Last Updated
        </Text>

        <Text style={[styles.infoValue, { color: colors.text }]}>
          Today
        </Text>

      </View>

    </View>
        {/* Bottom Buttons */}

    <View style={styles.buttonContainer}>

      <PrimaryButton
        title="Save Changes"
        icon="save-outline"
        onPress={saveProfile}
      />

      <TouchableOpacity
        activeOpacity={0.8}
        style={[
          styles.cancelButton,
          {
            backgroundColor: colors.card,
            borderColor: colors.border,
          },
        ]}
        onPress={() => navigation.goBack()}
      >

        <Ionicons
          name="close-outline"
          size={22}
          color={colors.primary}
        />

        <Text style={[styles.cancelText, { color: colors.primary }]}>
          Cancel
        </Text>

      </TouchableOpacity>

    </View>

    {/* Footer */}

    <View style={styles.footer}>

      <Ionicons
        name="shield-checkmark"
        size={18}
        color={colors.primary}
      />

      <Text style={[styles.footerText, { color: colors.subText }]}>
        Your profile is securely encrypted and protected.
      </Text>

    </View>

  </ScrollView>
{showDatePicker && (

<DateTimePicker

value={dob ? new Date(dob) : new Date()}

mode="date"

display="default"

onChange={(event, selectedDate) => {

  setShowDatePicker(false);

  if (selectedDate) {
    setDob(selectedDate.toDateString());
  }

}}

/>

)}
</SafeAreaView>

);

}
const styles = StyleSheet.create({

  container: {
    flex: 1,
  },

  scroll: {
    paddingBottom: 40,
  },

  /* ================= HEADER ================= */

  header: {
    paddingTop: 24,
    paddingHorizontal: width > 900 ? 60 : 24,
    paddingBottom: 45,

    borderBottomLeftRadius: 35,
    borderBottomRightRadius: 35,

    elevation: 8,
  },

  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  headerTitle: {
    color: "#FFFFFF",
    fontSize: width > 900 ? 30 : 24,
    fontWeight: "800",
  },

  headerSubtitle: {
    color: "#E8F3FF",
    fontSize: 15,
    marginTop: 14,
    textAlign: "center",
    lineHeight: 22,
  },

  avatarContainer: {
    alignItems: "center",
    marginTop: 28,
  },
    /* ================= CARD ================= */

  card: {

    marginTop: 25,

    marginHorizontal: width > 900 ? 80 : 18,

    borderRadius: 28,

    padding: 22,

    shadowOpacity: 0.06,

    shadowRadius: 18,

    shadowOffset: {
      width: 0,
      height: 10,
    },

    elevation: 7,
  },

  cardHeader: {

    flexDirection: "row",

    alignItems: "center",

    marginBottom: 22,

  },

  sectionTitle: {

    marginLeft: 12,

    fontSize: 22,

    fontWeight: "700",

  },
    /* ================= HEALTH CARD ================= */

  healthCard: {

    marginHorizontal: width > 900 ? 80 : 18,

    marginTop: 28,

    borderRadius: 28,

    padding: 24,

    shadowOpacity: 0.06,

    shadowRadius: 18,

    shadowOffset: {
      width: 0,
      height: 8,
    },

    elevation: 7,
  },

  healthHeader: {

    flexDirection: "row",

    alignItems: "center",

    marginBottom: 25,

  },

  healthIcon: {

    width: 54,

    height: 54,

    borderRadius: 27,

    backgroundColor: "#EF4444",

    justifyContent: "center",

    alignItems: "center",

    marginRight: 16,

  },

  healthTitle: {

    fontSize: 22,

    fontWeight: "700",

  },

  healthSubtitle: {

    marginTop: 4,

    fontSize: 14,

  },
    /* ================= STATS ================= */

  statsRow: {

    flexDirection: "row",

    justifyContent: "space-between",

    marginBottom: 25,

  },

  statCard: {

    width: "31%",

    paddingVertical: 22,

    borderRadius: 20,

    alignItems: "center",

    borderWidth: 1,

  },

  statNumber: {

    marginTop: 12,

    fontSize: 24,

    fontWeight: "800",

  },

  statLabel: {

    marginTop: 5,

    fontSize: 13,

  },

  infoRow: {

    flexDirection: "row",

    justifyContent: "space-between",

    marginTop: 16,

  },

  infoLabel: {

    fontSize: 15,

  },

  infoValue: {

    fontWeight: "700",

  },

  activeStatus: {

    color: "#16A34A",

    fontWeight: "700",

  },
    /* ================= BUTTONS ================= */

  buttonContainer: {

    marginHorizontal: width > 900 ? 120 : 22,

    marginTop: 35,

  },

  cancelButton: {

    marginTop: 18,

    height: 56,

    borderRadius: 30,

    borderWidth: 1,

    flexDirection: "row",

    justifyContent: "center",

    alignItems: "center",

  },

  cancelText: {

    marginLeft: 8,

    fontWeight: "700",

    fontSize: 16,

  },

  /* ================= FOOTER ================= */

  footer: {

    flexDirection: "row",

    justifyContent: "center",

    alignItems: "center",

    marginTop: 30,

    marginBottom: 30,

    paddingHorizontal: 25,

  },

  footerText: {

    marginLeft: 8,

    fontSize: 13,

    textAlign: "center",

  },
  label:{
  fontSize:15,
  fontWeight:"600",
  marginBottom:8,
},

dropdown:{
  height:56,
  borderRadius:16,
  borderWidth:1,
  flexDirection:"row",
  alignItems:"center",
  paddingHorizontal:18,
  marginBottom:18,
},

dropdownText:{
  marginLeft:12,
  fontSize:16,
},

menu:{
  borderRadius:18,
  borderWidth:1,
  marginBottom:18,
  overflow:"hidden",
  elevation:6,
},

menuItem:{
  padding:16,
  borderBottomWidth:1,
},

menuText:{
  fontSize:16,
},

});