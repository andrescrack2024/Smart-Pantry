// ─────────────────────────────────────────────────────────────
// geminiService.js
// Servicio híbrido inteligente de escaneo de alimentos.
// Intenta primero conectarse con los microservicios locales en Python (Gateway).
// Si el servidor local está desconectado, realiza la llamada inteligente
// de Gemini Vision directamente desde la aplicación como un fallback transparente.
// ─────────────────────────────────────────────────────────────

import { GoogleGenerativeAI } from "@google/generative-ai";
import { Platform } from "react-native";
import Constants from "expo-constants";

// Clave API de Gemini para la llamada directa (fallback)
const API_KEY = process.env.EXPO_PUBLIC_GEMINI_API_KEY;

let genAI = null;
let model = null;

if (API_KEY) {
  genAI = new GoogleGenerativeAI(API_KEY);
  model = genAI.getGenerativeModel({ 
    model: "gemini-1.5-flash",
    generationConfig: {
      responseMimeType: "application/json",
      responseSchema: {
        type: "object",
        properties: {
          isFoodRelated: {
            type: "boolean",
            description: "TRUE si la imagen contiene algún tipo de alimento, despensa, nevera con comida o ticket de compra de supermercado. FALSE si la imagen muestra de forma evidente objetos no comestibles como computadoras, laptops, sillas, celulares, etc."
          },
          confidenceReason: {
            type: "string",
            description: "Explicación breve en español del porqué es o no alimento."
          },
          detectedItems: {
            type: "array",
            items: {
              type: "object",
              properties: {
                name: {
                  type: "string",
                  description: "Nombre del alimento en español."
                },
                category: {
                  type: "string",
                  enum: ["Granos", "Lácteos", "Carnes", "Frutas", "Verduras", "Proteínas", "Despensa", "Enlatados", "Pastas", "Bebidas", "Panadería", "Otros"],
                  description: "Categoría del alimento."
                },
                quantity: {
                  type: "string",
                  description: "Cantidad con unidad, ej: '1 bolsa', '2 unidades'. Usa '1 ud' si no sabes."
                },
                daysLeft: {
                  type: "integer",
                  description: "Días estimados de frescura restante."
                }
              },
              required: ["name", "category", "quantity", "daysLeft"]
            }
          }
        },
        required: ["isFoodRelated", "confidenceReason", "detectedItems"]
      }
    }
  });
} else {
  console.warn("🚨 Advertencia: EXPO_PUBLIC_GEMINI_API_KEY no configurada. El fallback directo móvil no estará disponible.");
}

// Retorna la lista de URLs de microservicios resolviendo dinámicamente la IP de la PC local (cambiados a rango 5000 para evitar bloqueos de puerto inseguro en Chrome)
const getGatewayUrls = () => {
  const urls = [];
  
  // 1. Si estamos en Web, priorizar localhost, 127.0.0.1 y el hostname activo del navegador
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

  // 2. Obtener la IP dinámica desde Expo Metro Bundler (Súper robusto en celular real)
  const hostUri = Constants.expoConfig?.hostUri || Constants.manifest?.debuggerHost;
  if (hostUri) {
    const ip = hostUri.split(':')[0];
    if (ip && ip !== 'localhost' && ip !== '127.0.0.1') {
      urls.push(`http://${ip}:5000/api/v1/scan`);
    }
  }

  // 3. Fallbacks estáticos (incluyendo tu dirección IP física real 192.168.101.7)
  urls.push("http://192.168.101.7:5000/api/v1/scan");  // IP física del Wi-Fi actual
  urls.push("http://192.168.80.13:5000/api/v1/scan");   // IP del Wi-Fi anterior
  urls.push("http://10.0.2.2:5000/api/v1/scan");       // Emulador Android estándar
  urls.push("http://127.0.0.1:5000/api/v1/scan");     // Localhost de desarrollo
  
  // Filtrar duplicados manteniendo orden
  const uniqueUrls = [...new Set(urls)];
  console.log("🔍 URLs dinámicas auto-detectadas para Microservicios locales:", uniqueUrls);
  return uniqueUrls;
};

// Prompt del sistema altamente permisivo para Gemini Vision
const SYSTEM_PROMPT = `Eres un asistente experto en identificación de alimentos a partir de imágenes.
Tu tarea es analizar la imagen proporcionada y devolver ÚNICAMENTE un objeto JSON válido en español con los productos alimenticios detectados.

REGLAS ESTRICTAS:
1. Debes determinar de manera inteligente si la imagen contiene alimentos de cualquier tipo (frutas, verduras, carnes, comidas preparadas, lácteos, granos, panes, etc.), empaques de comida, refrigeradores o alacenas con comida, o tickets de compra de supermercado.
2. Devuelve un objeto JSON con tres propiedades obligatorias:
   - "isFoodRelated" (boolean): Debe ser TRUE si la imagen muestra cualquier tipo de alimento (crudo, cocinado, fresco, enlatado), empaques de alimentos, alacenas/refrigeradores con comida, o tickets/recibos de compra. Solo debe ser FALSE si la imagen muestra de forma evidente objetos completamente no alimentarios (como electrodomésticos, muebles, vehículos, herramientas, computadoras) o personas/animales sin ningún alimento visible. Ante la menor duda o si hay algún elemento comestible o ticket de compra, devuelve TRUE.
   - "confidenceReason" (string): Explicación amigable en español de por qué se considera comida o no (ej: "Se detectó una manzana roja", "La imagen muestra un zapato y ningún tipo de comida", "Se identificaron múltiples ingredientes en el plato de comida").
   - "detectedItems" (array): Lista de productos alimenticios detectados. Si "isFoodRelated" es false, este arreglo debe estar vacío [].

Para cada alimento identificado en "detectedItems", incluye:
   - "name": nombre del producto en español (string). Usa nombres comunes y claros. Ejemplo: "Manzana roja", "Leche entera", "Arroz blanco".
   - "category": una de las siguientes categorías en español (string):
     "Granos", "Lácteos", "Carnes", "Frutas", "Verduras", "Proteínas", "Despensa", "Enlatados", "Pastas", "Bebidas", "Panadería", "Otros"
   - "quantity": cantidad detectada con su unidad (string). Ejemplos: "1 kg", "2 unidades", "500 ml", "1 paquete", "3 piezas". Si no puedes determinar la cantidad, usa "1 ud".
   - "daysLeft": número estimado de días que el producto se mantiene fresco/apto para consumo (number entero). Guíate por la categoría: Frutas/Verduras (5-10 días), Lácteos (7-14 días), Carnes/Pollos frescos (2-4 días), Enlatados/Secos (180-365 días).

Devuelve ÚNICAMENTE el objeto JSON puro, sin explicaciones adicionales y sin delimitadores de código markdown como \`\`\`json ni \`\`\`.`;


/**
 * Realiza una llamada directa en la nube a Groq Llama 3.2 Vision para fallback de escaneo.
 * 
 * @param {string} cleanBase64 - Imagen en Base64 limpia.
 * @returns {Promise<Object>} Resultado JSON parseado de alimentos.
 */
const scanWithGroqDirect = async (cleanBase64) => {
  const apiKey = process.env.EXPO_PUBLIC_GROQ_API_KEY;
  if (!apiKey) {
    throw new Error("Clave API de Groq no configurada.");
  }
  
  console.log("📡 Conectando directamente con Groq Llama 3.2 Vision...");
  
  const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`
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
 * Si falla, usa Gemini API directamente desde el teléfono de forma automática.
 * 
 * @param {string} base64Image - Imagen codificada en Base64.
 * @returns {Promise<{isFoodRelated: boolean, confidenceReason: string, data: Array}>}
 */
export const scanReceipt = async (base64Image) => {
  if (!base64Image || typeof base64Image !== "string") {
    console.error("🚨 Error: No se proporcionó una imagen válida en Base64.");
    return { isFoodRelated: false, confidenceReason: "No se proporcionó una imagen válida.", data: [] };
  }

  // Limpiar el base64 eliminando encabezados URI
  const cleanBase64 = base64Image.includes(",") ? base64Image.split(",")[1] : base64Image;

  // 1. INTENTAR CONECTAR CON LOS MICROSERVICIOS LOCALES (GATEWAY)
  console.log("📡 Intentando conectar con los microservicios locales...");
  
  // Lista de URLs locales autodetectadas dinámicamente
  const localUrls = getGatewayUrls();
  
  for (const url of localUrls) {
    try {
      console.log(`🔗 Enviando imagen al Gateway local en: ${url}`);
      
      // Implementamos un AbortController de 45s para dar tiempo al procesamiento de OCR + IA en local
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
        
        // Si el backend local determinó que es comida, nos aseguramos de que devuelva algo
        const isFood = result.isFoodRelated ?? true;
        let detected = result.data ?? [];
        if (isFood && detected.length === 0) {
          // Si es un ticket reconocido pero sin items, retornamos tal cual (el modal maneja la advertencia de corte)
          detected = [];
        }

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

  // 2. FALLBACK: EJECUTAR CLOUD VISION DIRECTAMENTE EN LA APP MÓVIL/WEB
  console.log("⚡ Servidor local inaccesible. Activando fallback directo...");
  
  let parsedResult = null;
  let usedService = "";
  
  // A. Intentar Groq Primero (prioritario a petición del usuario)
  if (process.env.EXPO_PUBLIC_GROQ_API_KEY) {
    try {
      parsedResult = await scanWithGroqDirect(cleanBase64);
      usedService = "Groq Llama Vision";
    } catch (groqErr) {
      console.warn("⚠️ Falló fallback directo de Groq:", groqErr.message);
    }
  }
  
  // B. Si Groq falló o no estaba configurado, intentar Gemini
  if (!parsedResult && model) {
    try {
      console.log("📡 Conectando directamente con Gemini Vision...");
      const imagePart = {
        inlineData: {
          data: cleanBase64,
          mimeType: "image/jpeg",
        },
      };
      const result = await model.generateContent([SYSTEM_PROMPT, imagePart]);
      const responseText = result.response.text();
      parsedResult = extraerJSON(responseText);
      usedService = "Gemini Vision";
    } catch (geminiErr) {
      console.warn("⚠️ Falló fallback directo de Gemini:", geminiErr.message);
    }
  }
  
  if (!parsedResult) {
    throw new Error("🚨 El servidor de microservicios está apagado y los fallbacks de IA en la nube (Groq/Gemini) fallaron o no están configurados.");
  }
  
  try {
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
      confidenceReason: parsedResult.confidenceReason ?? `Análisis IA en la nube (${usedService}) completado.`,
      data: detected
    };
  } catch (error) {
    console.error("🚨 Error crítico al procesar la imagen con fallback directo:", error);
    let friendlyMessage = error.message;
    if (friendlyMessage && (friendlyMessage.includes("leaked") || friendlyMessage.includes("403") || friendlyMessage.includes("404") || friendlyMessage.includes("API key") || friendlyMessage.includes("not found"))) {
      friendlyMessage = "La clave API directa de la app móvil ha caducado o está deshabilitada. Asegúrate de iniciar los microservicios locales en tu PC ejecutando el script 'start_services.ps1' o configurar una clave válida en Render.";
    }
    throw new Error(friendlyMessage || "Fallo de conexión con la IA de respaldo.");
  }
};

/**
 * Limpia y extrae JSON de la respuesta de texto.
 */
function extraerJSON(text) {
  if (!text || typeof text !== "string") return {};

  let textoLimpio = text.trim();

  // Quitar triple backticks
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
    console.error("🚨 Error al parsear JSON directo de Gemini:", parseError.message);
    return {};
  }
}

export default {
  scanReceipt,
};