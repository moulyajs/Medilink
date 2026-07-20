import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Colors, Spacing } from "../../../theme";

interface Props {
  message: string;
  isUser: boolean;
}

export default function MessageBubble({
  message,
  isUser,
}: Props) {
  return (
    <View
      style={[
        styles.wrapper,
        isUser
          ? styles.userWrapper
          : styles.botWrapper,
      ]}
    >
      <View
        style={[
          styles.bubble,
          isUser
            ? styles.userBubble
            : styles.botBubble,
        ]}
      >
        <Text
          style={[
            styles.text,
            isUser && styles.userText,
          ]}
        >
          {message}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    width: "100%",
    marginVertical: 6,
  },

  userWrapper: {
    alignItems: "flex-end",
  },

  botWrapper: {
    alignItems: "flex-start",
  },

  bubble: {
    maxWidth: "78%",
    padding: Spacing.md,
    borderRadius: 18,
  },

  userBubble: {
    backgroundColor: Colors.primary,
    borderBottomRightRadius: 6,
  },

  botBubble: {
    backgroundColor: Colors.botBubble,
    borderBottomLeftRadius: 6,
  },

  text: {
    color: Colors.text,
    fontSize: 16,
    lineHeight: 24,
  },

  userText: {
    color: Colors.white,
  },
});