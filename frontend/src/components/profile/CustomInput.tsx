import React from "react";
import {
  View,
  Text,
  TextInput,
  StyleSheet,
} from "react-native";

type Props = {
  label: string;
  placeholder: string;
  value: string;
  onChangeText: (text: string) => void;
};

export default function CustomInput({

  label,

  placeholder,

  value,

  onChangeText,

}:Props){

  return(

    <View style={styles.container}>

      <Text style={styles.label}>
        {label}
      </Text>

      <TextInput

        style={styles.input}

        placeholder={placeholder}

        value={value}

        onChangeText={onChangeText}

      />

    </View>

  );

}

const styles=StyleSheet.create({

container:{

marginBottom:18

},

label:{

marginBottom:8,

fontWeight:"600",

fontSize:15,

color:"#334155"

},

input:{

height:54,

borderWidth:1,

borderColor:"#CBD5E1",

borderRadius:14,

paddingHorizontal:16,

fontSize:16,

backgroundColor:"#FFFFFF"

}

});