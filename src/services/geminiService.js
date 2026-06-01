// ─────────────────────────────────────────────────────────────
// geminiService.js (Motor de Escaneo Exclusivo con Groq Llama)
// Intenta primero conectarse con los microservicios locales en Python (Gateway).
// Si el servidor local está desconectado, realiza la llamada inteligente
// de Groq Vision directamente desde la aplicación como un fallback.
// ─────────────────────────────────────────────────────────────

import { Platform } from "react-native";
import Constants from "expo-constants";

// Clave API de Groq para la llamada directa (fallback)
const GROQ_API_KEY = process.env.EXPO_PUBLIC_GROQ_API_KEY || "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";

// Retorna la lista de URLs de microservicios resolviendo dinámicamente la IP de la PC local
const getGatewayUrls = () => {
  const urls = [];
  
  if (Platform.OS === 'web') {
    urls.push("http://localhost:5000/api/v1/scan");
    urls.push("http://127.0.0.1:5000/api/v1/scan");
    if (typeof window !== 'undefined' && window.location) {
      const hostname = window.location.hostname;
      if (hostname && hostname !== 'localhost' && hostname !== '127.0.0.1') {
        urls.push(`http://${hostname}:5000/api/v1/scan`);
      }
    }
  }

  const hostUri = Constants.expoConfig?.hostUri || Constants.manifest?.debuggerHost;
  if (hostUri) {
    const ip = hostUri.split(':')[0];
    if (ip && ip !== 'localhost' && ip !== '127.0.0.1') {
      urls.push(`http://${ip}:5000/api/v1/scan`);
    }
  }

  urls.push("http://192.168.101.7:5000/api/v1/scan");  // IP física del Wi-Fi actual
  urls.push("http://192.168.80.13:5000/api/v1/scan");   // IP del Wi-Fi anterior
  urls.push("http://10.0.2.2:5000/api/v1/scan");       // Emulador Android estándar
  urls.push("http://127.0.0.1:5000/api/v1/scan");     // Localhost de desarrollo
  
  return [...new Set(urls)];
};

// Prompt del sistema altamente permisivo para Groq Vision (Llama 3.2)
const SYSTEM_PROMPT = `Eres un asistente experto en identificación de alimentos a partir de imágenes.
Tu tarea es analizar la imagen proporcionada y devolver ÚNICAMENTE un objeto JSON válido en español con los productos alimenticios detectados.

REGLAS ESTRICTAS:
1. Debes determinar de manera inteligente si la imagen contiene alimentos de cualquier tipo (frutas, verduras, carnes, comidas preparadas, lácteos, granos, panes, etc.), empaques de comida, refrigeradores o alacenas con comida, o tickets de compra de supermercado.
2. Devuelve un objeto JSON con tres propiedades obligatorias:
   - "isFoodRelated" (boolean): Debe ser TRUE si la imagen muestra cualquier tipo de alimento o ticket de compra. Solo debe ser FALSE si muestra objetos completamente no alimentarios.
   - "confidenceReason" (string): Explicación amigable en español de por qué se considera comida o no.
   - "detectedItems" (array): Lista de productos alimenticios detectados. Si "isFoodRelated" es false, este arreglo debe estar vacío [].

Para cada alimento identificado en "detectedItems", incluye:
   - "name": nombre del producto en español (string). Ej: "Manzana roja", "Leche entera".
   - "category": una de las siguientes categorías en español (string):
     "Granos", "Lácteos", "Carnes", "Frutas", "Verduras", "Proteínas", "Despensa", "Enlatados", "Pastas", "Bebidas", "Panadería", "Otros"
   - "quantity": cantidad detectada con su unidad (string). Ej: "1 kg", "2 unidades". Si no sabes, usa "1 ud".
   - "daysLeft": número estimado de días que el producto se mantiene fresco (number entero).

Devuelve ÚNICAMENTE el objeto JSON puro, sin explicaciones adicionales y sin delimitadores markdown.`;

/**
 * Realiza una llamada directa en la nube a Groq Llama 3.2 Vision para fallback de escaneo.
 */
const scanWithGroqDirect = async (cleanBase64) => {
  if (!GROQ_API_KEY) {
    throw new Error("Clave API de Groq no configurada.");
  }
  
  console.log("📡 Conectando directamente con Groq Llama 3.2 Vision...");
  
  const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${GROQ_API_KEY}`
    },
    body: JSON.stringify({
      model: "llama-3.2-11b-vision-preview",
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: SYSTEM_PROMPT },
            {
              type: "image_url",
              image_url: {
                url: `data:image/jpeg;base64,${cleanBase64}`
              }
            }
          ]
        }
      ],
      temperature: 0.1,
      response_format: { type: "json_object" }
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error de Groq API: ${response.status} - ${errorText}`);
  }

  const result = await response.json();
  const content = result.choices[0].message.content;
  console.log("📥 Respuesta directa de Groq Vision recibida.");
  return extraerJSON(content);
};

/**
 * Escanea una imagen en Base64 e identifica los alimentos contenidos de forma inteligente.
 * Intenta llamar al servidor local de microservicios primero.
 * Si falla, usa Groq Llama Vision directamente en el móvil de forma automática.
 */
export const scanReceipt = async (base64Image) => {
  if (!base64Image || typeof base64Image !== "string") {
    console.error("🚨 Error: No se proporcionó una imagen válida en Base64.");
    return { isFoodRelated: false, confidenceReason: "No se proporcionó una imagen válida.", data: [] };
  }

  const cleanBase64 = base64Image.includes(",") ? base64Image.split(",")[1] : base64Image;

  // 1. INTENTAR CONECTAR CON LOS MICROSERVICIOS LOCALES (GATEWAY)
  console.log("📡 Intentando conectar con los microservicios locales...");
  const localUrls = getGatewayUrls();
  
  for (const url of localUrls) {
    try {
      console.log(`🔗 Enviando imagen al Gateway local en: ${url}`);
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 45000);
      
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ base64_image: cleanBase64 }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      if (response.ok) {
        const result = await response.json();
        console.log("🎉 ¡Microservicios locales respondieron exitosamente!");
        
        const isFood = result.isFoodRelated ?? true;
        let detected = result.data ?? [];

        return {
          isFoodRelated: isFood,
          confidenceReason: result.confidenceReason ?? "Escaneo local de microservicios exitoso.",
          data: detected
        };
      } else {
        console.warn(`⚠️ Gateway local devolvió código de error en la URL: ${url}`);
      }
    } catch (e) {
      console.log(`🔌 No se pudo conectar con el microservicio en ${url}: ${e.message}`);
    }
  }

  // 2. FALLBACK: EJECUTAR GROQ VISION DIRECTAMENTE EN LA APP MÓVIL/WEB
  console.log("⚡ Servidor local inaccesible. Activando fallback directo con Groq Vision...");
  
  try {
    const parsedResult = await scanWithGroqDirect(cleanBase64);
    const isFood = parsedResult.isFoodRelated ?? true;
    let detected = parsedResult.detectedItems ?? [];
    
    if (isFood && detected.length === 0) {
      detected = [{
        name: "Alimento Escaneado",
        category: "Otros",
        daysLeft: 7,
        quantity: "1 ud"
      }];
    }
    
    return {
      isFoodRelated: isFood,
      confidenceReason: parsedResult.confidenceReason ?? "Análisis IA en la nube (Groq Llama Vision) completado.",
      data: detected
    };
  } catch (error) {
    console.error("🚨 Error crítico al procesar la imagen con Groq directo:", error);
    let friendlyMessage = error.message;
    if (friendlyMessage && (friendlyMessage.includes("leaked") || friendlyMessage.includes("403") || friendlyMessage.includes("404") || friendlyMessage.includes("API key") || friendlyMessage.includes("not found"))) {
      friendlyMessage = "La clave API directa de Groq ha caducado o está deshabilitada. Asegúrate de iniciar los microservicios locales en tu PC ejecutando el script 'start_services.ps1' o configurar una clave válida.";
    }
    throw new Error(friendlyMessage || "Fallo de conexión con la IA de respaldo Groq.");
  }
};

/**
 * Limpia y extrae JSON de la respuesta de texto.
 */
function extraerJSON(text) {
  if (!text || typeof text !== "string") return {};

  let textoLimpio = text.trim();

  const regexBloqueCodigo = /```(?:json)?\s*([\s\S]*?)```/;
  const coincidencia = textoLimpio.match(regexBloqueCodigo);
  if (coincidencia) {
    textoLimpio = coincidencia[1].trim();
  }

  const inicioObj = textoLimpio.indexOf("{");
  const finObj = textoLimpio.lastIndexOf("}");

  if (inicioObj !== -1 && finObj !== -1 && finObj > inicioObj) {
    textoLimpio = textoLimpio.substring(inicioObj, finObj + 1);
  }

  try {
    return JSON.parse(textoLimpio);
  } catch (parseError) {
    console.error("🚨 Error al parsear JSON directo de Groq:", parseError.message);
    return {};
  }
}

export default {
  scanReceipt,
};
