import React, { useEffect, useState } from "react";
import {
  SafeAreaView,
  FlatList,
  Alert,
  TouchableOpacity,
  Text,
} from "react-native";

import SessionCard from "../../components/settings/SessionCard";

import {
  getSessions,
  logoutSession,
  logoutAllSessions,
  Session,
} from "../../services/sessionService";

export default function SessionManagementScreen() {

  const [sessions, setSessions] = useState<Session[]>([]);

  const load = async () => {
    const data = await getSessions();
    setSessions(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <SafeAreaView style={{ flex: 1 }}>

      <FlatList
        data={sessions}
        keyExtractor={(item: any) => item.session_id}
        renderItem={({ item }: any) => (
          <SessionCard
            device={item.device_name}
            platform={item.platform}
            lastActive={item.last_active}
            current={item.current}
            onLogout={async () => {
              await logoutSession(item.session_id);
              load();
            }}
          />
        )}
      />

      <TouchableOpacity
        style={{
          margin:20,
          backgroundColor:"#EF4444",
          padding:18,
          borderRadius:12
        }}
        onPress={async()=>{
          Alert.alert(
            "Logout All",
            "Logout from all devices?",
            [
              {text:"Cancel"},
              {
                text:"Logout",
                onPress:async()=>{
                  await logoutAllSessions();
                  load();
                }
              }
            ]
          );
        }}
      >
        <Text
          style={{
            color:"#fff",
            textAlign:"center",
            fontWeight:"700"
          }}
        >
          Logout All Sessions
        </Text>
      </TouchableOpacity>

    </SafeAreaView>
  );
}