import { StyleSheet } from "react-native";

export default StyleSheet.create({

  /* =========================
     Timeline Container
  ========================= */

  timelineContainer: {
    backgroundColor: "#FFFFFF",

    borderRadius: 16,

    paddingVertical: 24,
    paddingHorizontal: 20,

    shadowColor: "#000",

    shadowOpacity: 0.08,

    shadowRadius: 8,

    shadowOffset: {
      width: 0,
      height: 2,
    },

    elevation: 4,
  },

  timelineTitle: {
    fontSize: 20,
    fontWeight: "600",

    color: "#0F172A",

    textAlign: "center",

    marginBottom: 28,
  },

  scrollContent: {
    alignItems: "flex-start",

    paddingRight: 24,
  },

  /* =========================
     Timeline Event
  ========================= */

  eventItem: {
    width: 110,

    alignItems: "center",
  },

  circle: {
    width: 56,
    height: 56,

    borderRadius: 28,

    justifyContent: "center",
    alignItems: "center",

    shadowColor: "#000",

    shadowOpacity: 0.12,

    shadowRadius: 4,

    shadowOffset: {
      width: 0,
      height: 2,
    },

    elevation: 3,
  },

  line: {
    width: 70,

    height: 3,

    marginTop: 28,

    backgroundColor: "#CBD5E1",
  },

  eventLabel: {
    marginTop: 12,

    fontSize: 15,

    fontWeight: "600",

    color: "#0F172A",

    textAlign: "center",
  },

  eventDate: {
    marginTop: 6,

    fontSize: 13,

    color: "#64748B",

    textAlign: "center",
  },

  /* =========================
     View Button
  ========================= */

  viewButton: {
    marginTop: 12,

    borderWidth: 1,

    borderColor: "#2563EB",

    borderRadius: 12,

    paddingHorizontal: 16,

    paddingVertical: 6,

    backgroundColor: "#FFFFFF",
  },

  viewText: {
    color: "#2563EB",

    fontSize: 13,

    fontWeight: "600",
  },

  /* =========================
     Load More
  ========================= */

  loadMore: {
    width: 120,

    alignItems: "center",

    justifyContent: "center",

    marginLeft: 12,
  },

  loadMoreButton: {
    marginTop: 12,

    borderWidth: 1,

    borderColor: "#2563EB",

    borderRadius: 12,

    paddingHorizontal: 16,

    paddingVertical: 6,
  },

  loadMoreText: {
    color: "#2563EB",

    fontSize: 13,

    fontWeight: "700",
  },

});