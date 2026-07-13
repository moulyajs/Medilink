import React from "react";
import {
TouchableOpacity,
Text,
StyleSheet
} from "react-native";

export default function SkipButton(){

return(

<TouchableOpacity style={styles.button}>

<Text style={styles.text}>
Skip
</Text>

</TouchableOpacity>

);

}

const styles=StyleSheet.create({

button:{

paddingHorizontal:18,

paddingVertical:10,

borderRadius:30,

borderWidth:1,

borderColor:"#CFE5F6",

backgroundColor:"#FFFFFF"

},

text:{

fontWeight:"700",

color:"#4E89B9"

}

});