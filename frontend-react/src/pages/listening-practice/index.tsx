import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { fetchWithTimeout } from '@/api';

interface Dialogue {
  dialog: string[];
  question: string;
  options: Record<string, string>;
  correct_answer: string;
}

export const ListeningPractice = () => {
  const [selectedTopic, setSelectedTopic] = useState<string>('');
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const { toast } = useToast();

  const { data: dialogues } = useQuery({
    queryKey: ['dialogues'],
    queryFn: async () => {
      const response = await fetchWithTimeout('/api/dialogues');
      return response.dialogues;
    }
  });

  const { data: audioUrl } = useQuery({
    queryKey: ['audio', selectedTopic],
    queryFn: async () => {
      if (!selectedTopic) return null;
      const response = await fetchWithTimeout(`/api/audio/${selectedTopic}`);
      return response.audio_url;
    },
    enabled: !!selectedTopic
  });

  const handleSubmit = () => {
    if (!selectedAnswer) {
      toast({
        title: "Error",
        description: "Please select an answer",
        variant: "destructive"
      });
      return;
    }

    const isCorrect = selectedAnswer === dialogues[selectedTopic]?.correct_answer;
    toast({
      title: isCorrect ? "Correct!" : "Incorrect",
      description: isCorrect 
        ? "Great job!" 
        : `The correct answer was: ${dialogues[selectedTopic]?.options[dialogues[selectedTopic]?.correct_answer]}`,
      variant: isCorrect ? "default" : "destructive"
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Romanian Listening Practice</h1>

      <div className="grid gap-8 md:grid-cols-2">
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Select a Topic</h2>
          <div className="space-y-4">
            {dialogues && Object.keys(dialogues).map((topic) => (
              <Button
                key={topic}
                variant={selectedTopic === topic ? "default" : "outline"}
                onClick={() => setSelectedTopic(topic)}
                className="w-full"
              >
                {topic.replace(/_/g, ' ').toUpperCase()}
              </Button>
            ))}
          </div>
        </Card>

        {selectedTopic && (
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Listen and Answer</h2>
            {audioUrl && (
              <audio controls className="w-full mb-4">
                <source src={audioUrl} type="audio/mp3" />
              </audio>
            )}

            <div className="space-y-4">
              <p className="font-medium">{dialogues[selectedTopic].question}</p>
              <RadioGroup onValueChange={setSelectedAnswer} value={selectedAnswer}>
                {Object.entries(dialogues[selectedTopic].options).map(([key, value]) => (
                  <div key={key} className="flex items-center space-x-2">
                    <RadioGroupItem value={key} id={key} />
                    <Label htmlFor={key}>{value}</Label>
                  </div>
                ))}
              </RadioGroup>

              <Button onClick={handleSubmit} className="w-full">
                Check Answer
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}; 