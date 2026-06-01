import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';

// 1. Configuración de comportamiento
// Le decimos al celular: "Aún si tengo la app abierta y la estoy mirando, muéstrame la alerta y hazla sonar"
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

// 2. Función para pedirle permiso al usuario
export async function requestNotificationPermission() {
  if (Device.isDevice) {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    
    // Si no tenemos permiso, le sale el cuadrito en la pantalla preguntando
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    
    if (finalStatus !== 'granted') {
      console.log('Permiso de notificaciones denegado.');
      return false;
    }

    // Configuración especial obligatoria para que Android permita vibrar y sonar duro
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'Alertas de Despensa',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }
    
    return true;
  } else {
    console.log('Debes usar un celular físico para las notificaciones Push.');
    return false;
  }
}

// 3. Función mágica para programar la alarma
export async function scheduleExpirationNotification(itemName, daysLeft) {
  
  // ⚠️ MODO DE PRUEBA (ACTUAL): 
  // Sin importar cuándo se venza, la alarma sonará en exactamente 5 SEGUNDOS.
  const triggerSeconds = 5; 

  // 🚀 MODO PRODUCCIÓN (PARA CUANDO TERMINES LA APP):
  // Borra el "5" de arriba y quítale las dos barras (//) a la línea de abajo. 
  // Esto hará la matemática para que suene exactamente 1 día antes de vencerse.
  // const triggerSeconds = (daysLeft - 1) * 24 * 60 * 60; 

  // Si el alimento ya está vencido (días negativos), no programamos nada
  if (triggerSeconds <= 0) return;

  await Notifications.scheduleNotificationAsync({
    content: {
      title: "¡Ojo con la despensa! 🚨",
      body: `El/La ${itemName} se vence pronto. ¡A cocinar se dijo!`,
      sound: true,
      priority: Notifications.AndroidNotificationPriority.HIGH, // Prioridad máxima en Android
    },
    trigger: { 
      seconds: triggerSeconds 
    },
  });
}