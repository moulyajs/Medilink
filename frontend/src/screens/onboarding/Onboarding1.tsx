import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";

import { useNavigation } from "@react-navigation/native";


export default function Onboarding1(){

const navigation = useNavigation<any>();


return(

<SafeAreaView style={styles.container}>


{/* Skip */}

<TouchableOpacity 
style={styles.skip}
onPress={()=>navigation.replace("Login")}
>

<Text style={styles.skipText}>
Skip
</Text>

</TouchableOpacity>



{/* Illustration */}

<View style={styles.imageContainer}>

<Text style={styles.emoji}>
🩺
</Text>

</View>



{/* Text */}

<Text style={styles.title}>
Your Health,
{"\n"}
All in One Place
</Text>


<Text style={styles.description}>
Securely store and access
your medical records
anytime, anywhere.
</Text>



{/* Dots */}

<View style={styles.dots}>

<View style={[styles.dot,styles.active]}/>
<View style={styles.dot}/>
<View style={styles.dot}/>

</View>



{/* Button */}

<TouchableOpacity
style={styles.button}
onPress={()=>navigation.navigate("Onboarding2")}
>

<Text style={styles.buttonText}>
Next →
</Text>

</TouchableOpacity>



</SafeAreaView>

)

}


const styles=StyleSheet.create({

container:{
flex:1,
backgroundColor:"#F8FBFD",
alignItems:"center",
paddingHorizontal:25
},


skip:{
alignSelf:"flex-end",
marginTop:20
},


skipText:{
fontSize:16,
color:"#6F90A8"
},



imageContainer:{
marginTop:60,
width:260,
height:260,
borderRadius:130,
backgroundColor:"#EAF6FD",
alignItems:"center",
justifyContent:"center"
},


emoji:{
fontSize:100
},



title:{
marginTop:50,
fontSize:34,
fontWeight:"800",
textAlign:"center",
color:"#244C69"
},


description:{
marginTop:20,
fontSize:17,
lineHeight:26,
textAlign:"center",
color:"#6F90A8"
},



dots:{
flexDirection:"row",
marginTop:50,
gap:8
},


dot:{
height:8,
width:8,
borderRadius:10,
backgroundColor:"#D0E3F1"
},


active:{
width:25,
backgroundColor:"#4E89B9"
},



button:{
position:"absolute",
bottom:40,
width:"100%",
height:55,
borderRadius:30,
backgroundColor:"#4E89B9",
alignItems:"center",
justifyContent:"center"
},


buttonText:{
color:"#fff",
fontSize:18,
fontWeight:"700"
}


});