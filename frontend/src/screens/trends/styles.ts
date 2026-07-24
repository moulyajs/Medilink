import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8FAFC",
  },

  content: {
    width: "100%",
    maxWidth: 900,
    alignSelf: "center",
    padding: 20,
  },

heading: {
  fontSize: 32,
  fontWeight: "700",
  color: "#1E293B",
},

  cardRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 16,
    marginBottom: 16,
  },

  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#0F172A",
    marginBottom: 12,
  },

  loading: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  header: {
  flexDirection: "row",
  alignItems: "center",
  marginBottom: 20,
},

backButton: {
  marginRight: 12,
  padding: 4,
},
});