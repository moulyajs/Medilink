import React from "react";
import {
View,
Text,
StyleSheet
} from "react-native";

export default function OnboardingHeader(){

return(

<>

<View style={styles.badge}>

<Text style={styles.badgeText}>
MEDICAL JOURNEY
</Text>

</View>

<Text style={styles.title}>
Every step of your{"\n"}care, captured
</Text>

<Text style={styles.subtitle}>
Your complete medical timeline—
consultations, tests & prescriptions—
beautifully organized.
</Text>

</>

);

}

const styles=StyleSheet.create({

badge:{

alignSelf:"center",

backgroundColor:"#F0F8FE",

paddingHorizontal:18,

paddingVertical:8,

borderRadius:30,

marginTop:15

},

badgeText:{

letterSpacing:2,

fontSize:11,

fontWeight:"700",

color:"#4E89B9"

},

title:{

fontSize:38,

fontWeight:"800",

textAlign:"center",

marginTop:25,

color:"#284B68"

},

subtitle:{

marginTop:18,

fontSize:17,

lineHeight:28,

textAlign:"center",

color:"#7092AA"

}

});