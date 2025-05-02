import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/hooks/use-toast";
import { LoadingSpinner } from "@/components/ui/loading-spinner";

interface Question {
  id: string;
  text: string;
  options: string[];
  correctAnswer: string;
}

export const ListeningPractice = () => {
  const [videoUrl, setVideoUrl] = useState("");
  const [transcript, setTranscript] = useState("");
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleVideoSubmit = async () => {
    try {
      setLoading(true);
      const serviceUrl = import.meta.env.VITE_LISTENING_SERVICE_URL;
      
      if (!serviceUrl) {
        throw new Error('Listening service URL not configured');
      }

      const response = await fetch(`${serviceUrl}/api/process-video`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ url: videoUrl })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to process video');
      }

      const data = await response.json();
      setTranscript(data.transcript);
      setQuestions(data.questions);
      
      toast({
        title: "Success",
        description: "Video processed successfully",
      });
    } catch (error) {
      console.error('Video processing error:', error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : 'Failed to process video',
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">Listening Practice</h1>
      
      <Card className="p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Add YouTube Video</h2>
        <div className="flex gap-4">
          <Input
            placeholder="Enter YouTube URL"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            disabled={loading}
          />
          <Button 
            onClick={handleVideoSubmit}
            disabled={loading || !videoUrl}
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <LoadingSpinner size={16} />
                <span>Processing...</span>
              </div>
            ) : (
              'Process Video'
            )}
          </Button>
        </div>
      </Card>

      {transcript && (
        <Card className="p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Transcript</h2>
          <p className="whitespace-pre-wrap">{transcript}</p>
        </Card>
      )}

      {questions.length > 0 && (
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Comprehension Questions</h2>
          <div className="space-y-6">
            {questions.map((question) => (
              <div key={question.id} className="space-y-4">
                <p className="font-medium">{question.text}</p>
                <div className="space-y-2">
                  {question.options.map((option) => (
                    <div key={option} className="flex items-center space-x-2">
                      <Checkbox id={`${question.id}-${option}`} />
                      <label htmlFor={`${question.id}-${option}`}>{option}</label>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}; 