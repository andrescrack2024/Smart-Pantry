// src/screens/ScannerScreen.js
import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ActivityIndicator, Dimensions, Animated } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');
const viewFinderSize = width * 0.7;

export default function ScannerScreen({ onCancel, onScanFinished }) {
  const [permission, requestPermission] = useCameraPermissions();
  const [processing, setProcessing] = useState(false);
  const cameraRef = useRef(null);
  
  // Animación del láser escaneando
  const scanLineAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (!processing) {
      // Bucle de animación del láser
      const startLaserAnimation = () => {
        scanLineAnim.setValue(0);
        Animated.loop(
          Animated.sequence([
            Animated.timing(scanLineAnim, {
              toValue: 1,
              duration: 2000,
              useNativeDriver: true,
            }),
            Animated.timing(scanLineAnim, {
              toValue: 0,
              duration: 2000,
              useNativeDriver: true,
            })
          ])
        ).start();
      };
      startLaserAnimation();
    } else {
      scanLineAnim.stopAnimation();
    }
  }, [processing]);

  if (!permission) return <View style={styles.loadingContainer}><ActivityIndicator size="large" color="#4CAF50" /></View>;
  
  if (!permission.granted) {
    return (
      <View style={styles.permissionContainer}>
        <View style={styles.iconWrapper}>
          <Ionicons name="camera-outline" size={80} color="#666" />
        </View>
        <Text style={styles.permissionTitle}>Permiso de Cámara Requerido</Text>
        <Text style={styles.permissionText}>
          Necesitamos tu permiso para utilizar la cámara y escanear tus alimentos o tickets automáticamente.
        </Text>
        <TouchableOpacity style={styles.permissionButton} onPress={requestPermission}>
          <Text style={styles.permissionButtonText}>Otorgar Permiso</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.permissionCancelButton} onPress={onCancel}>
          <Text style={styles.permissionCancelText}>Cancelar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current && !processing) {
      setProcessing(true);
      console.log("Capturando foto...");
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.15, // Compresión alta para asegurar que quepa en Firestore (<1MB) y suba instantáneamente
          base64: true,
          skipProcessing: false,
        });
        console.log("¡Foto lista! Enviando base64 al HomeScreen...");
        onScanFinished(photo.base64);
      } catch (error) {
        console.error("Error al capturar la imagen:", error);
        setProcessing(false);
      }
    }
  };

  const laserY = scanLineAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0, viewFinderSize - 4]
  });

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} facing="back" ref={cameraRef} />
      
      {/* Capa de diseño del escáner moderno (posicionado de forma absoluta para evitar el warning de children) */}
      <View style={styles.overlayContainer}>
        
        {/* Header superior */}
        <View style={styles.headerContainer}>
          <Text style={styles.headerTitle}>Escáner de Despensa</Text>
          <Text style={styles.headerSubtitle}>Coloca el producto o recibo dentro del cuadro</Text>
        </View>

        {/* Área del Viewfinder con esquinas premium */}
        <View style={styles.middleContainer}>
          <View style={styles.sideOverlay} />
          
          <View style={styles.viewfinder}>
            {/* Esquinas estéticas del escáner */}
            <View style={[styles.corner, styles.topLeft]} />
            <View style={[styles.corner, styles.topRight]} />
            <View style={[styles.corner, styles.bottomLeft]} />
            <View style={[styles.corner, styles.bottomRight]} />
            
            {/* Línea láser animada */}
            {!processing && (
              <Animated.View style={[styles.laser, { transform: [{ translateY: laserY }] }]} />
            )}
          </View>

          <View style={styles.sideOverlay} />
        </View>

        {/* Panel inferior de botones y estado */}
        <View style={styles.bottomContainer}>
          {processing ? (
            <View style={styles.processingCard}>
              <ActivityIndicator size="large" color="#4CAF50" />
              <Text style={styles.processingText}>La IA está analizando...</Text>
              <Text style={styles.processingSubtext}>Extrayendo textos y detectando alimentos</Text>
            </View>
          ) : (
            <View style={styles.controlsRow}>
              {/* Botón Cancelar con Ionicons */}
              <TouchableOpacity style={styles.iconButton} onPress={onCancel}>
                <Ionicons name="close-circle-outline" size={32} color="#ffffff" />
                <Text style={styles.iconButtonText}>Cerrar</Text>
              </TouchableOpacity>

              {/* Botón Capturar Premium */}
              <TouchableOpacity style={styles.captureOuterCircle} onPress={takePicture}>
                <View style={styles.captureInnerCircle} />
              </TouchableOpacity>

              {/* Info o ayuda decorativa */}
              <View style={styles.iconButtonPlaceholder}>
                <Ionicons name="sparkles-outline" size={26} color="rgba(255,255,255,0.7)" />
                <Text style={styles.iconButtonText}>IA Activa</Text>
              </View>
            </View>
          )}
        </View>

      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#000' 
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#121212',
  },
  camera: { 
    flex: 1 
  },
  overlayContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'space-between',
  },
  
  // Header superior
  headerContainer: {
    paddingTop: 50,
    paddingBottom: 20,
    backgroundColor: 'rgba(0,0,0,0.6)',
    alignItems: 'center',
  },
  headerTitle: {
    color: '#ffffff',
    fontSize: 22,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  headerSubtitle: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 13,
    marginTop: 6,
    fontWeight: '500',
  },

  // Viewfinder intermedio
  middleContainer: {
    flexDirection: 'row',
    height: viewFinderSize,
    alignItems: 'center',
  },
  sideOverlay: {
    flex: 1,
    height: '100%',
    backgroundColor: 'rgba(0,0,0,0.6)',
  },
  viewfinder: {
    width: viewFinderSize,
    height: viewFinderSize,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.15)',
    backgroundColor: 'transparent',
    position: 'relative',
    justifyContent: 'center',
  },
  
  // Esquinas del visor
  corner: {
    position: 'absolute',
    width: 20,
    height: 20,
    borderColor: '#4CAF50', // Verde vibrante de SmartPantry
  },
  topLeft: {
    top: -2,
    left: -2,
    borderTopWidth: 4,
    borderLeftWidth: 4,
    borderTopLeftRadius: 8,
  },
  topRight: {
    top: -2,
    right: -2,
    borderTopWidth: 4,
    borderRightWidth: 4,
    borderTopRightRadius: 8,
  },
  bottomLeft: {
    bottom: -2,
    left: -2,
    borderBottomWidth: 4,
    borderLeftWidth: 4,
    borderBottomLeftRadius: 8,
  },
  bottomRight: {
    bottom: -2,
    right: -2,
    borderBottomWidth: 4,
    borderRightWidth: 4,
    borderBottomRightRadius: 8,
  },

  // Láser del escáner
  laser: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 4,
    backgroundColor: '#4CAF50',
    shadowColor: '#4CAF50',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 10,
    elevation: 8,
  },

  // Panel inferior
  bottomContainer: {
    paddingBottom: 40,
    paddingTop: 30,
    backgroundColor: 'rgba(0,0,0,0.6)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  controlsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    width: '100%',
    paddingHorizontal: 20,
  },
  iconButton: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
  },
  iconButtonPlaceholder: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
  },
  iconButtonText: {
    color: '#ffffff',
    fontSize: 12,
    marginTop: 6,
    fontWeight: '600',
  },

  // Botón capturador
  captureOuterCircle: {
    width: 84,
    height: 84,
    borderRadius: 42,
    borderWidth: 4,
    borderColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  captureInnerCircle: {
    width: 66,
    height: 66,
    borderRadius: 33,
    backgroundColor: '#ffffff',
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 3,
  },

  // Tarjeta de procesamiento IA
  processingCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    paddingVertical: 25,
    paddingHorizontal: 35,
    borderRadius: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 10,
    elevation: 10,
    width: width * 0.8,
  },
  processingText: {
    color: '#111111',
    fontSize: 17,
    fontWeight: '800',
    marginTop: 15,
  },
  processingSubtext: {
    color: '#666666',
    fontSize: 12,
    marginTop: 4,
    textAlign: 'center',
  },

  // Permisos e indicaciones de error
  permissionContainer: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
  },
  iconWrapper: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  permissionTitle: {
    color: '#ffffff',
    fontSize: 22,
    fontWeight: '800',
    marginBottom: 12,
    textAlign: 'center',
  },
  permissionText: {
    color: '#aaaaaa',
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 40,
  },
  permissionButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 16,
    paddingHorizontal: 40,
    borderRadius: 14,
    width: '100%',
    alignItems: 'center',
    shadowColor: '#4CAF50',
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  permissionButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  permissionCancelButton: {
    marginTop: 20,
    padding: 10,
  },
  permissionCancelText: {
    color: '#888888',
    fontSize: 15,
    fontWeight: '600',
  }
});