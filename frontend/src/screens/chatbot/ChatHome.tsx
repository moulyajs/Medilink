import React, {
  useMemo,
  useState,
  useCallback,
} from "react";
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  ActivityIndicator,
  RefreshControl,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useNavigation,useFocusEffect } from "@react-navigation/native";

import AppHeader from "../../components/AppHeader";
import SearchBar from "../../components/SearchBar";
import PrimaryButton from "../../components/PrimaryButton";

import ChatCard from "./components/ChatCard";
import SuggestedPrompt from "./components/SuggestedPrompt";
import EmptyState from "./components/EmptyState";

import { prompts } from "./dummyData";


import { CHAT_PADDING, CHAT_WIDTH } from "./constants";

import { Colors, Spacing, Typography } from "../../theme";
import {
  getSessions,
  createSession,
  deleteSession,
} from "../../services/chatService";


import Ionicons from "@expo/vector-icons/build/Ionicons";

interface Conversation {
  session_id: string;
  title: string | null;
  updated_at: string;
}

export default function ChatHome() {
  const navigation = useNavigation<any>();

  const [search, setSearch] = useState("");

  const [conversations, setConversations] = useState<
    Conversation[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useFocusEffect(
  useCallback(() => {
    loadSessions();
  }, [])
);

  const loadSessions = useCallback(async () => {
  try {
    setLoading(true);

    const data = await getSessions();
    setConversations(data);
  } catch (err) {
    console.log(err);
  } finally {
    setLoading(false);
  }
}, []);
const onRefresh = async () => {
  setRefreshing(true);

  await loadSessions();

  setRefreshing(false);
};

  const handleNewChat = async () => {
    try {
      const session = await createSession();

      navigation.navigate("ChatScreen", {
        sessionId: session.session_id,
      });
    } catch (err) {
      console.log(err);
    }
  };

  const handlePrompt = async (prompt: string) => {
    try {
      const session = await createSession();

      navigation.navigate("ChatScreen", {
        sessionId: session.session_id,
        autoPrompt: prompt,
      });
    } catch (err) {
      console.log(err);
    }
  };
  const handleDelete = (sessionId: string) => {
  Alert.alert(
    "Delete Conversation",
    "Are you sure you want to delete this conversation?",
    [
      {
        text: "Cancel",
        style: "cancel",
      },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          try {
            await deleteSession(sessionId);

            setConversations((prev) =>
              prev.filter(
                (item) => item.session_id !== sessionId
              )
            );
          } catch (err) {
            console.log(err);

            Alert.alert(
              "Error",
              "Failed to delete conversation."
            );
          }
        },
      },
    ]
  );
};

  const filteredConversations = useMemo(() => {
    if (!search.trim()) return conversations;

    return conversations.filter((item) =>
      item.title
        ?.toLowerCase()
        .includes(search.toLowerCase())
    );
  }, [search, conversations]);

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
  refreshControl={
    <RefreshControl
      refreshing={refreshing}
      onRefresh={onRefresh}
    />
  }
>
        <View style={styles.wrapper}>
          <View style={styles.topRow}>
            <TouchableOpacity onPress={() => navigation.goBack()}>
              <Ionicons
                name="arrow-back"
                size={24}
                color={Colors.text}
              />
            </TouchableOpacity>
          </View>

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

            {loading ? (
  <ActivityIndicator
    size="large"
    color={Colors.primary}
    style={{ marginTop: 20 }}
  />
) : filteredConversations.length === 0 ? (
  <EmptyState />
) : (
  filteredConversations.map((item) => (
    <ChatCard
  key={item.session_id}
  title={item.title ?? "New Chat"}
  description=""
  date={new Date(item.updated_at).toLocaleDateString()}
  onPress={() =>
    navigation.navigate("ChatScreen", {
      sessionId: item.session_id,
    })
  }
  onDelete={() =>
    handleDelete(item.session_id)
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
                  onPress={() => handlePrompt(prompt)}
                />
              ))}
            </View>
          </View>

          <PrimaryButton
            title="Start New Chat"
            onPress={handleNewChat}
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

  topRow: {
    marginBottom: 16,
  },

  chips: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginBottom: Spacing.xl,
  },
});