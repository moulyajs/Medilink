import React, {
  useEffect,
  useState,
} from "react";

import {
  SafeAreaView,
  FlatList,
  View,
  Text,
  TouchableOpacity,
  Alert,
  StyleSheet,
} from "react-native";

import {
  getDevices,
  removeDevice,
  Device,
} from "../../services/deviceService";

export default function ConnectedDevicesScreen() {

  const [devices, setDevices] = useState<Device[]>([]);

  const loadDevices = async () => {
    try {
      const data = await getDevices();
      setDevices(data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    loadDevices();
  }, []);

  const deleteDevice = (id: string) => {
    Alert.alert(
      "Remove Device",
      "Remove this trusted device?",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Remove",
          style: "destructive",
          onPress: async () => {
            await removeDevice(id);
            loadDevices();
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>

      <FlatList
        data={devices}
        keyExtractor={(item) => item.device_id}
        ListEmptyComponent={
          <Text style={styles.empty}>
            No connected devices.
          </Text>
        }
        renderItem={({ item }) => (
          <View style={styles.card}>

            <View style={{ flex: 1 }}>

              <Text style={styles.title}>
                {item.device_name}
              </Text>

              <Text style={styles.subtitle}>
                {item.device_os}
              </Text>

              <Text style={styles.subtitle}>
                {item.device_type}
              </Text>

              <Text style={styles.subtitle}>
                Last Active:
              </Text>

              <Text style={styles.date}>
                {new Date(
                  item.last_active
                ).toLocaleString()}
              </Text>

              {item.is_current && (
                <Text style={styles.current}>
                  Current Device
                </Text>
              )}

            </View>

            {!item.is_current && (
              <TouchableOpacity
                style={styles.button}
                onPress={() =>
                  deleteDevice(item.device_id)
                }
              >
                <Text style={styles.buttonText}>
                  Remove
                </Text>
              </TouchableOpacity>
            )}

          </View>
        )}
      />

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: "#F8FAFC",
    padding: 16,
  },

  card: {
    backgroundColor: "#fff",
    borderRadius: 14,
    padding: 18,
    marginBottom: 15,
    flexDirection: "row",
    alignItems: "center",

    elevation: 3,
  },

  title: {
    fontSize: 17,
    fontWeight: "700",
    color: "#111827",
  },

  subtitle: {
    color: "#6B7280",
    marginTop: 2,
  },

  date: {
    color: "#9CA3AF",
    fontSize: 12,
    marginTop: 2,
  },

  current: {
    marginTop: 8,
    color: "#16A34A",
    fontWeight: "700",
  },

  button: {
    backgroundColor: "#EF4444",
    paddingHorizontal: 18,
    paddingVertical: 10,
    borderRadius: 8,
  },

  buttonText: {
    color: "#fff",
    fontWeight: "700",
  },

  empty: {
    textAlign: "center",
    marginTop: 60,
    color: "#6B7280",
  },

});