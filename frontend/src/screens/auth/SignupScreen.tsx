import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from "react-native";
import { signup } from "../../services/authService";
import { useNavigation } from "@react-navigation/native";
import CustomDropdown from "../../components/profile/CustomDropdown";
export default function SignupScreen() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("");
  const [loading, setLoading] = useState(false);
  const [showGenderMenu, setShowGenderMenu] = useState(false);

  const navigation = useNavigation<any>();
  const handleSignup = async () => {
  try {
    setLoading(true);

    await signup({
      name,
      email,
      password,
      phone,
      dob,
      gender,
    });

    alert("Account created successfully!");

    navigation.navigate("Login");
  } catch (error: any) {
  console.log("Signup Error:", error);
  console.log("Response:", error?.response);
  console.log("Response Data:", error?.response?.data);

  alert(
    error?.response?.data?.detail ||
    error?.message ||
    "Signup failed."
  );
  } finally {
    setLoading(false);
  }
};
  return (
    <ScrollView
      contentContainerStyle={styles.container}
      keyboardShouldPersistTaps="handled"
    >
      <Text style={styles.title}>Create Account</Text>

      <TextInput
        placeholder="Full Name"
        style={styles.input}
        value={name}
        onChangeText={setName}
      />

      <TextInput
        placeholder="Email"
        style={styles.input}
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />

      <TextInput
        placeholder="Phone"
        style={styles.input}
        value={phone}
        onChangeText={setPhone}
        keyboardType="phone-pad"
      />

      <TextInput
        placeholder="Password"
        style={styles.input}
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TextInput
        placeholder="DOB (YYYY-MM-DD)"
        style={styles.input}
        value={dob}
        onChangeText={setDob}
      />

      <CustomDropdown
  label="Gender"
  value={gender}
  placeholder="Select Gender"
  onPress={() => setShowGenderMenu(true)}
/>

{showGenderMenu && (
  <View style={styles.menu}>
    {["Male", "Female", "Other"].map((item) => (
      <TouchableOpacity
        key={item}
        style={styles.menuItem}
        onPress={() => {
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

      <TouchableOpacity
  style={styles.button}
  onPress={handleSignup}
  disabled={loading}
>
<Text style={styles.buttonText}>
    {loading ? "Creating..." : "Sign Up"}
</Text>
      </TouchableOpacity>

      <TouchableOpacity>
        <Text style={styles.loginText}>
          Already have an account? Login
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 24,
    justifyContent: "center",
    backgroundColor: "#FFFFFF",
  },

  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 32,
    textAlign: "center",
  },

  input: {
    height: 52,
    borderWidth: 1,
    borderColor: "#E2E8F0",
    borderRadius: 12,
    paddingHorizontal: 16,
    marginBottom: 16,
  },

  button: {
    height: 52,
    backgroundColor: "#2563EB",
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 12,
    marginTop: 8,
  },

  buttonText: {
    color: "#FFFFFF",
    fontWeight: "600",
    fontSize: 16,
  },

  loginText: {
    marginTop: 24,
    textAlign: "center",
    color: "#2563EB",
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
