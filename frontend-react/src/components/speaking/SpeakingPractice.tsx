import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

interface SpeakingPrompt {
  id: string;
  name: string;
  description: string;
  image_url: string;
  difficulty: string;
}

export const SpeakingPractice = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [currentPrompt, setCurrentPrompt] = useState<SpeakingPrompt | null>(null);
  const [evaluation, setEvaluation] = useState<string>('');
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const { toast } = useToast();

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      const chunks: BlobPart[] = [];

      mediaRecorder.current.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        await submitRecording(audioBlob);
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      
      // Stop recording after 60 seconds
      setTimeout(() => stopRecording(), 60000);
    } catch (err) {
      toast({
        title: "Error",
        description: "Could not access microphone",
        variant: "destructive",
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current?.state === 'recording') {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  const submitRecording = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      formData.append('audio_file', audioBlob);
      formData.append('context', currentPrompt?.description || '');

      const response = await fetch('/api/evaluate-speaking', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setEvaluation(data.evaluation);
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to evaluate speaking",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Romanian Speaking Practice</h1>
      
      <Card className="p-6">
        {currentPrompt && (
          <div className="mb-4">
            <img 
              src={currentPrompt.image_url} 
              alt={currentPrompt.name}
              className="w-full max-w-md mx-auto mb-4"
            />
            <p className="text-lg mb-2">{currentPrompt.description}</p>
          </div>
        )}

        <div className="flex justify-center gap-4">
          <Button
            onClick={isRecording ? stopRecording : startRecording}
            variant={isRecording ? "destructive" : "default"}
          >
            {isRecording ? "Stop Recording" : "Start Recording"}
          </Button>
        </div>

        {evaluation && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2">Evaluation</h2>
            <p className="text-gray-700 dark:text-gray-300">{evaluation}</p>
          </div>
        )}
      </Card>
    </div>
  );
}; 