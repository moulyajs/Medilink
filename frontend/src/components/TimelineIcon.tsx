import React, { useEffect, useRef } from "react";
import {
  Animated,
  StyleSheet,
  View,
} from "react-native";

export default function TimelineIcon({
  children,
}: any) {

  const scale = useRef(new Animated.Value(1)).current;

  useEffect(() => {

    Animated.loop(

      Animated.sequence([

        Animated.timing(scale,{
          toValue:1.12,
          duration:700,
          useNativeDriver:true,
        }),

        Animated.timing(scale,{
          toValue:1,
          duration:700,
          useNativeDriver:true,
        }),

      ])

    ).start();

  },[]);

  return(

<Animated.View
style={[
styles.outer,
{
transform:[{scale}]
}
]}
>

<View style={styles.inner}>
{children}
</View>

</Animated.View>

  );

}

const styles=StyleSheet.create({

outer:{
width:54,
height:54,
borderRadius:27,
backgroundColor:"#D9EDF8",
justifyContent:"center",
alignItems:"center",
shadowColor:"#5D97C9",
shadowOpacity:.25,
shadowRadius:12,
elevation:8
},

inner:{
width:42,
height:42,
borderRadius:21,
backgroundColor:"#4E89B9",
justifyContent:"center",
alignItems:"center"
}

});