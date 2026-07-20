import React,{useEffect,useRef} from "react";
import {Animated} from "react-native";

export default function AnimatedPill({children}:any){

const opacity=useRef(new Animated.Value(0.4)).current;

useEffect(()=>{

Animated.loop(

Animated.sequence([

Animated.timing(opacity,{
toValue:1,
duration:1200,
useNativeDriver:true
}),

Animated.timing(opacity,{
toValue:0.4,
duration:1200,
useNativeDriver:true
})

])

).start();

},[])

return(

<Animated.View style={{opacity}}>
{children}
</Animated.View>

)

}