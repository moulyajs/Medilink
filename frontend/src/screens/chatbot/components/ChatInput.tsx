import React, { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

import { Colors } from "../../../theme";

interface Props {
  onSend: (text: string) => void;
  disabled?: boolean;
}
export default function ChatInput({
  onSend,
  disabled = false,
}: Props) {
  const [text, setText] = useState("");

  const send = () => {
  if (disabled) return;

  if (!text.trim()) return;

  onSend(text);

  setText("");
};

  return (
    <View style={styles.wrapper}>
      <View style={styles.container}>
        <TextInput
  value={text}
  onChangeText={setText}
  placeholder="Ask Medilink AI anything..."
  multiline
  editable={!disabled}
  style={styles.input}
/>

        <TouchableOpacity
  style={[
    styles.button,
    disabled && styles.disabledButton,
  ]}
  onPress={send}
  disabled={disabled}
>
          <Ionicons
            name="send"
            size={20}
            color="#fff"
          />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    padding: 16,
    backgroundColor: Colors.background,
    paddingBottom: 28,
  },

  container: {
    flexDirection: "row",
    alignItems: "flex-end",

    borderWidth: 1,

    borderColor: Colors.border,

    borderRadius: 28,

    backgroundColor: Colors.white,

    paddingLeft: 20,

    paddingRight: 8,

    paddingVertical: 8,
  },

  input: {
    flex: 1,
    maxHeight: 120,
    fontSize: 16,
  },
  disabledButton: {
  opacity: 0.5,
},

  button: {
    width: 44,
    height: 44,

    borderRadius: 22,

    justifyContent: "center",

    alignItems: "center",

    backgroundColor: Colors.primary,
  },
});