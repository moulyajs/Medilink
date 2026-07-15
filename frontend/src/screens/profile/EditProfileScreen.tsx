import React, { useState } from "react";
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
import { updateProfile } from "../../services/profileService";
const { width } = Dimensions.get("window");

export default function EditProfileScreen() {

  const navigation = useNavigation<any>();

  const [image, setImage] = useState("");

  const [name, setName] = useState("Zara Khatun");
  const [email, setEmail] = useState("zara@gmail.com");
  const [phone, setPhone] = useState("+91 9876543210");
  const [dob, setDob] = useState("10 Aug 2004");
  const [gender, setGender] = useState("Female");
  const [blood, setBlood] = useState("O+");
  const [address, setAddress] = useState("Kolkata, India");
  const [emergency, setEmergency] = useState("+91 9123456780");
  const [showDatePicker, setShowDatePicker] = useState(false);

const [showGenderMenu, setShowGenderMenu] = useState(false);

const [showBloodMenu, setShowBloodMenu] = useState(false);

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

    await updateProfile(1, {
      name,
      email,
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

  return (<SafeAreaView style={styles.container}>

  <ScrollView
    showsVerticalScrollIndicator={false}
    contentContainerStyle={styles.scroll}
  >

    {/* Header */}

    <LinearGradient
      colors={["#5D9DFF", "#4E89B9", "#3B73C5"]}
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

    <View style={styles.card}>

      <View style={styles.cardHeader}>

        <Ionicons
          name="person-circle-outline"
          size={24}
          color="#4E89B9"
        />

        <Text style={styles.sectionTitle}>
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
        onChangeText={setEmail}
        placeholder="Email Address"
        keyboardType="email-address"
        icon="mail-outline"
      />

      <CustomInput
        label="Phone Number"
        value={phone}
        onChangeText={setPhone}
        placeholder="Phone Number"
        keyboardType="phone-pad"
        icon="call-outline"
      />

     <Text style={styles.label}>
    Date of Birth
    </Text>

    <TouchableOpacity
    style={styles.dropdown}
    onPress={() => setShowDatePicker(true)}
    >

    <Ionicons
        name="calendar-outline"
        size={20}
        color="#4E89B9"
    />

    <Text style={styles.dropdownText}>
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

<View style={styles.menu}>

  {["Male","Female","Other"].map(item=>(

    <TouchableOpacity

      key={item}

      style={styles.menuItem}

      onPress={()=>{
        setGender(item);
        setShowGenderMenu(false);
      }}

    >

      <Text style={styles.menuText}>
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

<View style={styles.menu}>

  {["A+","A-","B+","B-","AB+","AB-","O+","O-"].map(item=>(

    <TouchableOpacity

      key={item}

      style={styles.menuItem}

      onPress={()=>{
        setBlood(item);
        setShowBloodMenu(false);
      }}

    >

      <Text style={styles.menuText}>
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

    <View style={styles.healthCard}>

      <View style={styles.healthHeader}>

        <View style={styles.healthIcon}>

          <Ionicons
            name="heart"
            size={22}
            color="#FFFFFF"
          />

        </View>

        <View>

          <Text style={styles.healthTitle}>
            Health Summary
          </Text>

          <Text style={styles.healthSubtitle}>
            Your medical profile overview
          </Text>

        </View>

      </View>

      {/* Stats */}

      <View style={styles.statsRow}>

        <View style={styles.statCard}>

          <Ionicons
            name="document-text-outline"
            size={26}
            color="#4E89B9"
          />

          <Text style={styles.statNumber}>
            24
          </Text>

          <Text style={styles.statLabel}>
            Reports
          </Text>

        </View>

        <View style={styles.statCard}>

          <Ionicons
            name="pulse-outline"
            size={26}
            color="#4E89B9"
          />

          <Text style={styles.statNumber}>
            18
          </Text>

          <Text style={styles.statLabel}>
            Timeline
          </Text>

        </View>

        <View style={styles.statCard}>

          <Ionicons
            name="sparkles-outline"
            size={26}
            color="#4E89B9"
          />

          <Text style={styles.statNumber}>
            12
          </Text>

          <Text style={styles.statLabel}>
            AI Insights
          </Text>

        </View>

      </View>

      {/* Medical Details */}

      <View style={styles.infoRow}>

        <Text style={styles.infoLabel}>
          Blood Group
        </Text>

        <Text style={styles.infoValue}>
          {blood}
        </Text>

      </View>

      <View style={styles.infoRow}>

        <Text style={styles.infoLabel}>
          Medical Profile
        </Text>

        <Text style={styles.activeStatus}>
          Active
        </Text>

      </View>

      <View style={styles.infoRow}>

        <Text style={styles.infoLabel}>
          Last Updated
        </Text>

        <Text style={styles.infoValue}>
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
        style={styles.cancelButton}
        onPress={() => navigation.goBack()}
      >

        <Ionicons
          name="close-outline"
          size={22}
          color="#4E89B9"
        />

        <Text style={styles.cancelText}>
          Cancel
        </Text>

      </TouchableOpacity>

    </View>

    {/* Footer */}

    <View style={styles.footer}>

      <Ionicons
        name="shield-checkmark"
        size={18}
        color="#4E89B9"
      />

      <Text style={styles.footerText}>
        Your profile is securely encrypted and protected.
      </Text>

    </View>

  </ScrollView>
{showDatePicker && (

<DateTimePicker

value={new Date()}

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
    backgroundColor: "#F4F8FC",
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

    backgroundColor: "#FFFFFF",

    borderRadius: 28,

    padding: 22,

    shadowColor: "#000",

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

    color: "#23384D",

  },
    /* ================= HEALTH CARD ================= */

  healthCard: {

    marginHorizontal: width > 900 ? 80 : 18,

    marginTop: 28,

    backgroundColor: "#FFFFFF",

    borderRadius: 28,

    padding: 24,

    shadowColor: "#000",

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

    color: "#23384D",

  },

  healthSubtitle: {

    marginTop: 4,

    color: "#7A93AA",

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

    backgroundColor: "#F4FAFF",

    alignItems: "center",

    borderWidth: 1,

    borderColor: "#E2EDF7",

  },

  statNumber: {

    marginTop: 12,

    fontSize: 24,

    fontWeight: "800",

    color: "#2563EB",

  },

  statLabel: {

    marginTop: 5,

    color: "#71869C",

    fontSize: 13,

  },

  infoRow: {

    flexDirection: "row",

    justifyContent: "space-between",

    marginTop: 16,

  },

  infoLabel: {

    color: "#71869C",

    fontSize: 15,

  },

  infoValue: {

    fontWeight: "700",

    color: "#23384D",

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

    backgroundColor: "#FFFFFF",

    borderWidth: 1,

    borderColor: "#D7E7F6",

    flexDirection: "row",

    justifyContent: "center",

    alignItems: "center",

  },

  cancelText: {

    marginLeft: 8,

    color: "#4E89B9",

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

    color: "#7A93AA",

    fontSize: 13,

    textAlign: "center",

  },
  label:{
  fontSize:15,
  fontWeight:"600",
  color:"#23384D",
  marginBottom:8,
},

dropdown:{
  height:56,
  borderRadius:16,
  borderWidth:1,
  borderColor:"#DCEAF5",
  backgroundColor:"#F8FBFE",
  flexDirection:"row",
  alignItems:"center",
  paddingHorizontal:18,
  marginBottom:18,
},

dropdownText:{
  marginLeft:12,
  fontSize:16,
  color:"#23384D",
},

menu:{
  backgroundColor:"#FFF",
  borderRadius:18,
  marginBottom:18,
  overflow:"hidden",
  elevation:6,
},

menuItem:{
  padding:16,
  borderBottomWidth:1,
  borderBottomColor:"#EEF3F8",
},

menuText:{
  fontSize:16,
  color:"#23384D",
},

});