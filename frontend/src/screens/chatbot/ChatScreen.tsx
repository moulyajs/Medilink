import React, { useRef, useState } from "react";
import {
  StyleSheet,
  View,
  Text,
  FlatList,
  TouchableOpacity,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";

import ChatInput from "./components/ChatInput";
import MessageBubble from "./components/MessageBubble";
import TypingIndicator from "./components/TypingIndicator";

import { CHAT_WIDTH, CHAT_PADDING } from "./constants";
import { Colors, Typography } from "../../theme";
import { sendMessage } from "../../services/chatService";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
}

export default function ChatScreen() {
  const navigation = useNavigation<any>();

  const flatListRef = useRef<FlatList>(null);

  const [typing, setTyping] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      sender: "bot",
      text:
        "Hello 👋 I'm Medilink AI.\n\nI can help explain your reports, compare trends and answer questions about your medical history.",
    },
  ]);

  const handleSend = async (text: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      sender: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);

    setTyping(true);

    try {
      const response = await sendMessage(text);

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: response.response,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: "bot",
          text: "Sorry, something went wrong.",
        },
      ]);
    } finally {
      setTyping(false);

      setTimeout(() => {
        flatListRef.current?.scrollToEnd({
          animated: true,
        });
      }, 100);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.wrapper}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Ionicons
              name="arrow-back"
              size={24}
              color={Colors.primary}
            />
          </TouchableOpacity>

          <View style={styles.headerCenter}>
            <Text style={styles.title}>Medilink AI</Text>
            <Text style={styles.subtitle}>
              Personal Health Assistant
            </Text>
          </View>

          {/* Spacer to balance the back button */}
          <View style={styles.headerSpacer} />
        </View>

        {/* Messages */}
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(item) => item.id}
          style={styles.list}
          contentContainerStyle={styles.listContent}
          renderItem={({ item }) => (
            <MessageBubble
              message={item.text}
              isUser={item.sender === "user"}
            />
          )}
          ListFooterComponent={
            typing ? <TypingIndicator /> : null
          }
        />

        {/* Input */}
        <ChatInput onSend={handleSend} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },

  wrapper: {
    flex: 1,
    width: "100%",
    maxWidth: CHAT_WIDTH,
    alignSelf: "center",
  },

  header: {
    height: 75,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: CHAT_PADDING,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
    backgroundColor: Colors.white,
  },

  headerCenter: {
    alignItems: "center",
  },

  headerSpacer: {
    width: 24,
  },

  title: {
    ...Typography.cardTitle,
    color: Colors.text,
    textAlign: "center",
  },

  subtitle: {
    color: Colors.textSecondary,
    marginTop: 2,
    fontSize: 13,
    textAlign: "center",
  },

  list: {
    flex: 1,
    width: "100%",
  },

  listContent: {
    padding: CHAT_PADDING,
  },
});