/**
 * Voice Recognition Service
 * Provides Web Speech API integration for voice input with fallback functionality
 */

export interface VoiceRecognitionOptions {
  lang?: string;
  continuous?: boolean;
  interimResults?: boolean;
  maxAlternatives?: number;
}

export interface VoiceRecognitionResult {
  transcript: string;
  isFinal: boolean;
  confidence?: number;
}

class VoiceRecognitionService {
  private recognition: any;
  private isSupported: boolean;

  constructor() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.isSupported = !!SpeechRecognition;

    if (this.isSupported) {
      this.recognition = new SpeechRecognition();
    }
  }

  isVoiceRecognitionSupported(): boolean {
    return this.isSupported;
  }

  async startListening(
    options: VoiceRecognitionOptions = {},
    onResult: (result: VoiceRecognitionResult) => void,
    onError: (error: any) => void
  ): Promise<void> {
    if (!this.isSupported) {
      // Fallback to text input when Web Speech API is not supported
      console.warn('Web Speech API is not supported in this browser. Falling back to text input.');
      onError('Voice recognition not supported. Please use text input.');
      return;
    }

    // Set options
    this.recognition.lang = options.lang || 'en-US';
    this.recognition.continuous = options.continuous || false;
    this.recognition.interimResults = options.interimResults || false;
    this.recognition.maxAlternatives = options.maxAlternatives || 1;

    // Set up event handlers
    this.recognition.onresult = (event: any) => {
      const result = event.results[event.resultIndex];
      const transcript = result[0].transcript;
      const isFinal = result.isFinal;
      const confidence = result[0].confidence;

      onResult({
        transcript,
        isFinal,
        confidence
      });
    };

    this.recognition.onerror = (event: any) => {
      // Handle specific error types with appropriate fallbacks
      const errorType = event.error;
      let errorMessage = `Voice recognition error: ${errorType}`;

      switch(errorType) {
        case 'no-speech':
          errorMessage = 'No speech detected. Try speaking more clearly.';
          break;
        case 'audio-capture':
          errorMessage = 'Could not access microphone. Please check permissions.';
          break;
        case 'not-allowed':
          errorMessage = 'Microphone access denied. Please enable microphone permissions.';
          break;
        case 'network':
          errorMessage = 'Network error occurred. Please check your connection.';
          break;
        default:
          errorMessage = `Voice recognition error: ${errorType}`;
      }

      onError(errorMessage);
    };

    this.recognition.onend = () => {
      // Recognition automatically stops after result, which is expected behavior
    };

    try {
      this.recognition.start();
    } catch (error: any) {
      if (error.message.includes('recognition already started')) {
        // Already started, ignore
      } else {
        throw error;
      }
    }
  }

  stopListening(): void {
    if (!this.isSupported) {
      return;
    }
    this.recognition.stop();
  }

  abortListening(): void {
    if (!this.isSupported) {
      return;
    }
    this.recognition.abort();
  }
}

// Singleton instance
const voiceRecognitionService = new VoiceRecognitionService();

export default voiceRecognitionService;

// Convenience functions
export const startVoiceRecognition = (
  options: VoiceRecognitionOptions = {},
  onResult: (result: VoiceRecognitionResult) => void,
  onError: (error: any) => void
): Promise<void> => {
  return voiceRecognitionService.startListening(options, onResult, onError);
};

export const stopVoiceRecognition = (): void => {
  voiceRecognitionService.stopListening();
};

export const abortVoiceRecognition = (): void => {
  voiceRecognitionService.abortListening();
};

export const isVoiceRecognitionSupported = (): boolean => {
  return voiceRecognitionService.isVoiceRecognitionSupported();
};

// Fallback mechanism for unsupported browsers
export const showVoiceInputFallback = (): string => {
  return "Voice input is not supported in your browser. Please use text input instead.";
};