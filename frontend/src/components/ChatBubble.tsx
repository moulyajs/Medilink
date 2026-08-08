import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

interface Props {
  sender: string;
  message: string;
  ai?: boolean;
}

export default function ChatBubble({
  sender,
  message,
  ai = false,
}: Props) {

  return (

    <View
      style={[
        styles.card,
        ai && styles.aiCard,
      ]}
    >

      <Text
        style={[
          styles.sender,
          ai && styles.aiSender,
        ]}
      >
        {sender}
      </Text>

      <Text
        style={[
          styles.message,
          ai && styles.aiMessage,
        ]}
      >
        {message}
      </Text>

    </View>

  );

}

const styles = StyleSheet.create({

  card: {

    width: 190,

    backgroundColor: "#FFFFFF",

    borderRadius: 22,

    padding: 16,

    shadowColor: "#000",

    shadowOpacity: 0.08,

    shadowRadius: 12,

    elevation: 6,

  },

  aiCard: {

    backgroundColor: "#4E89F9",

  },

  sender: {

    fontSize: 13,

    fontWeight: "700",

    color: "#8094A8",

    marginBottom: 8,

  },

  aiSender: {

    color: "#DCE8FF",

  },

  message: {

    fontSize: 15,

    lineHeight: 22,

    color: "#3A5268",

    fontWeight: "600",

  },

  aiMessage: {

    color: "#FFFFFF",

  },

});