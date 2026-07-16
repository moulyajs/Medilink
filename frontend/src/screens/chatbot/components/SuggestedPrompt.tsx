import React from "react";
import Chip from "../../../components/Chip";

interface Props {
  title: string;
  onPress: () => void;
}

export default function SuggestedPrompt({
  title,
  onPress,
}: Props) {
  return (
    <Chip
      title={title}
      onPress={onPress}
    />
  );
}