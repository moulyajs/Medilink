import React from "react";
import { View, StyleSheet } from "react-native";

import TimelineCard from "./TimelineCard";

export default function TimelineSection() {
  return (
    <View style={styles.container}>

      <TimelineCard
        icon="medkit"
        title="Doc Consulting"
        subtitle="General Practitioner"
        date="12 OCT"
      />

      <TimelineCard
        icon="flask"
        title="Blood Analysis"
        subtitle="Complete Blood Panel"
        date="15 OCT"
      />

      <TimelineCard
        icon="medical"
        title="Medication"
        subtitle="Active Prescription"
        date="18 OCT"
      />

    </View>
  );
}

const styles = StyleSheet.create({

container:{

marginTop:15

}

});