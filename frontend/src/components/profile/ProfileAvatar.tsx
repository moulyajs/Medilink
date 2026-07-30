import React from "react";
import {
  View,
  Text,
  Image,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { useTheme } from "../../theme/ThemeContext";
import { Ionicons } from "@expo/vector-icons";

type Props = {
  name: string;
  role?: string;
  image?: any;
  onEdit?: () => void;
};

export default function ProfileAvatar({
  name,
  role,
  image,
  onEdit,
}: Props) {
   const { colors } = useTheme();
  return (
    <View style={styles.container}>

      <View style={styles.avatarWrapper}>

        {image ? (
  <Image
    source={
      typeof image === "string"
        ? { uri: image }
        : image
    }
    style={styles.avatar}
  />
) : (
          <View
  style={[
    styles.placeholder,
    { backgroundColor: colors.primary },
  ]}
>

            <Ionicons
              name="person"
              size={52}
              color="#FFFFFF"
            />

          </View>
        )}

       <TouchableOpacity
  style={[
    styles.editButton,
    {
      borderColor: colors.card,
    },
  ]}
  onPress={onEdit}
>
  <Ionicons
    name="camera"
    size={16}
    color="#FFFFFF"
  />
</TouchableOpacity>

      </View>

      <Text
  style={[
    styles.name,
    { color: colors.text },
  ]}
>
        {name}
      </Text>

      {role && (
        <Text
  style={[
    styles.role,
    { color: colors.text },
  ]}
>
          {role}
        </Text>
      )}

    </View>
  );
}

const styles = StyleSheet.create({

  container: {
    alignItems: "center",
    marginVertical: 24,
  },

  avatarWrapper: {
    position: "relative",
  },

  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
  },

  placeholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: "#2563EB",
    justifyContent: "center",
    alignItems: "center",
  },

  editButton: {
  position: "absolute",
  bottom: 0,
  right: 0,

  width: 36,
  height: 36,

  borderRadius: 18,

  backgroundColor: "#14B8A6",

  justifyContent: "center",
  alignItems: "center",

  borderWidth: 3,
},

  name: {
    marginTop: 18,
    fontSize: 24,
    fontWeight: "700",
    color: "#0F172A",
  },

  role: {
    marginTop: 6,
    fontSize: 15,
    color: "#64748B",
  },

});