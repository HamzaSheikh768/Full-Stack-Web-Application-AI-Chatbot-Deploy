'use client';

import { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Mic, MicOff } from 'lucide-react';
import { toast } from 'sonner';

interface VoiceInputWidgetProps {
  onTranscript: (text: string) => void;
  onError?: (error: string) => void;
  supportedLanguages?: string[];
  defaultLanguage?: string;
}

declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

export default function VoiceInputWidget({
  onTranscript,
  onError,
  supportedLanguages = ['en-US', 'ur-PK'],
  defaultLanguage = 'en-US'
}: VoiceInputWidgetProps) {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const [isSupported, setIsSupported] = useState(true);

  // Check for Web Speech API support
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
      if (onError) {
        onError('Web Speech API is not supported in this browser');
      }
      return;
    }

    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = false;
    recognitionInstance.lang = defaultLanguage;

    recognitionInstance.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript);
      setIsListening(false);
    };

    recognitionInstance.onerror = (event: any) => {
      const errorMsg = `Speech recognition error: ${event.error}`;
      if (onError) {
        onError(errorMsg);
      }
      toast.error(`Voice input error: ${event.error}`);
      setIsListening(false);
    };

    recognitionInstance.onend = () => {
      if (isListening) {
        // Recognition stopped unexpectedly, restart if still supposed to be listening
        try {
          recognitionInstance.start();
        } catch (e) {
          // Ignore if already started
        }
      }
    };

    setRecognition(recognitionInstance);

    return () => {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
    };
  }, [onTranscript, onError, defaultLanguage]);

  const toggleListening = useCallback(() => {
    if (!recognition) return;

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      try {
        recognition.start();
        setIsListening(true);
      } catch (error: any) {
        if (error.message.includes('already started')) {
          // Ignore if already started
          setIsListening(true);
        } else {
          console.error('Error starting speech recognition:', error);
          if (onError) {
            onError(error.message);
          }
          toast.error('Failed to start voice input');
        }
      }
    }
  }, [isListening, recognition, onError]);

  if (!isSupported) {
    return (
      <div className="text-sm text-red-500 p-2">
        Voice input is not supported in your browser. Please use text input instead.
      </div>
    );
  }

  return (
    <Button
      type="button"
      variant={isListening ? "destructive" : "secondary"}
      size="icon"
      onClick={toggleListening}
      aria-label={isListening ? "Stop listening" : "Start voice input"}
      className={isListening ? "animate-pulse" : ""}
    >
      {isListening ? (
        <MicOff className="h-4 w-4" />
      ) : (
        <Mic className="h-4 w-4" />
      )}
    </Button>
  );
}