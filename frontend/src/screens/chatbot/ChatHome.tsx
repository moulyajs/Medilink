import React, { useMemo, useState } from "react";
import {
  
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useNavigation } from "@react-navigation/native";

import AppHeader from "../../components/AppHeader";
import SearchBar from "../../components/SearchBar";
import PrimaryButton from "../../components/PrimaryButton";

import ChatCard from "./components/ChatCard";
import SuggestedPrompt from "./components/SuggestedPrompt";
import EmptyState from "./components/EmptyState";

import { conversations, prompts } from "./dummyData";
import { CHAT_PADDING, CHAT_WIDTH } from "./constants";

import { Colors, Spacing, Typography } from "../../theme";

export default function ChatHome() {
  const navigation = useNavigation<any>();

  const [search, setSearch] = useState("");

  const filteredConversations = useMemo(() => {
    if (!search.trim()) return conversations;

    return conversations.filter(
      (item) =>
        item.title.toLowerCase().includes(search.toLowerCase()) ||
        item.description.toLowerCase().includes(search.toLowerCase())
    );
  }, [search]);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={[
        styles.content,
        {
        paddingBottom: 60,
         },
        ]}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.wrapper}>
          <AppHeader
            title="Medilink AI"
            subtitle="Your personal AI assistant for understanding reports, trends and medications."
          />

          <SearchBar
            value={search}
            onChangeText={setSearch}
          />

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              Recent Conversations
            </Text>

            {filteredConversations.length === 0 ? (
              <EmptyState />
            ) : (
              filteredConversations.map((item) => (
                <ChatCard
                  key={item.id}
                  title={item.title}
                  description={item.description}
                  date={item.date}
                  onPress={() =>
                    navigation.navigate("ChatScreen")
                  }
                />
              ))
            )}
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              Suggested Prompts
            </Text>

            <View style={styles.chips}>
              {prompts.map((prompt) => (
                <SuggestedPrompt
                  key={prompt}
                  title={prompt}
                  onPress={() =>
                    navigation.navigate("ChatScreen")
                  }
                />
              ))}
            </View>
          </View>

          <PrimaryButton
            title="Start New Chat"
            onPress={() =>
              navigation.navigate("ChatScreen")
            }
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },

  content: {
    alignItems: "center",
    padding: CHAT_PADDING,
  },

  wrapper: {
    width: "100%",
    maxWidth: CHAT_WIDTH,
  },

  section: {
    marginTop: Spacing.xl,
  },

  sectionTitle: {
    ...Typography.sectionTitle,
    color: Colors.text,
    marginBottom: Spacing.md,
  },

  chips: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginBottom: Spacing.xl,
  },
});