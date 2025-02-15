import { useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CustomBreadcrumb } from "@/components/ui/custom-breadcrumb";
import { useToast } from "@/hooks/use-toast";
import { GameState } from "@/types/vocabulary-game";
import { Play, Gamepad2, RotateCcw, Clock, Star } from "lucide-react";
import { WordGroup, Word } from "@/types/group";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { getSuccessToast, getErrorToast } from "@/config/toast";
import { format } from "date-fns";

const INITIAL_GROUPS: WordGroup[] = [
  {
    id: 1,
    name: "Kitchen",
    wordCount: 15,
    description: "Kitchen-related vocabulary for everyday use",
    words: [
      { romanian: "farfurie", english: "plate" },
      { romanian: "lingură", english: "spoon" },
      { romanian: "furculiță", english: "fork" },
      { romanian: "cuțit", english: "knife" },
      { romanian: "pahar", english: "glass" }
    ]
  },
  {
    id: 2,
    name: "Holiday",
    wordCount: 12,
    description: "Holiday and vacation terms",
    words: [
      { romanian: "plajă", english: "beach" },
      { romanian: "vacanță", english: "vacation" },
      { romanian: "hotel", english: "hotel" }
    ]
  },
  {
    id: 3,
    name: "Travel",
    wordCount: 20,
    description: "Essential travel vocabulary",
    words: [
      { romanian: "avion", english: "airplane" },
      { romanian: "tren", english: "train" },
      { romanian: "autobuz", english: "bus" }
    ]
  },
  {
    id: 4,
    name: "Core Verbs",
    wordCount: 8,
    description: "Fundamental Romanian verbs",
    words: [
      { romanian: "sunt", english: "am" },
      { romanian: "este", english: "to be" },
      { romanian: "nu", english: "not" },
      { romanian: "da", english: "yes" }
    ]
  }
];

const VocabularyGame = () => {
  const { groupId } = useParams();
  const { state } = useLocation();
  const { toast } = useToast();
  const [gameState, setGameState] = useState<GameState>("ready");
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [answer, setAnswer] = useState("");
  const [isRomanianToEnglish, setIsRomanianToEnglish] = useState(true);
  const [gameHistory, setGameHistory] = useState<{
    date: Date;
    score: number;
    totalWords: number;
  }[]>(() => {
    const saved = localStorage.getItem("vocabularyGameHistory");
    return saved ? JSON.parse(saved) : [];
  });

  const group = INITIAL_GROUPS.find(g => g.id === Number(groupId));
  const groupName = group?.name || "Unknown Group";
  const words = group?.words || [];

  const source = state?.source;
  const selectedGroup = state?.selectedGroup;

  const breadcrumbItems = [
    ...(source === 'words'
      ? [{ 
          label: "Words", 
          path: "/words",
          state: { source: 'words', wordGroups: state?.wordGroups }
        }]
      : source === 'groups'
      ? [{ 
          label: "Word Groups", 
          path: "/groups",
          state: { source: 'groups' }
        }]
      : [{ 
          label: "Study Activities", 
          path: "/study-activities",
          state: { source: 'study-activities' }
        }]
    ),
    { 
      label: "Vocabulary Practice", 
      path: "/study-activities/vocabulary",
      state
    },
    { 
      label: `${selectedGroup || groupName} Practice`, 
      path: undefined 
    }
  ];

  const saveGameResult = (finalScore: number, totalWords: number) => {
    const newHistory = [
      ...gameHistory,
      { date: new Date(), score: finalScore, totalWords }
    ];
    setGameHistory(newHistory);
    localStorage.setItem("vocabularyGameHistory", JSON.stringify(newHistory));
  };

  const startGame = () => {
    if (words.length === 0) {
      toast({
        title: "No words available",
        description: "This group doesn't have any words to practice with.",
        variant: "destructive"
      });
      return;
    }
    setGameState("playing");
    setCurrentWordIndex(0);
    setScore(0);
    setAnswer("");
  };

  const checkAnswer = () => {
    const currentWord = words[currentWordIndex];
    const correctAnswer = isRomanianToEnglish 
      ? currentWord.english.toLowerCase().trim()
      : currentWord.romanian.toLowerCase().trim();
    const isCorrect = answer.toLowerCase().trim() === correctAnswer;

    if (isCorrect) {
      setScore(prev => prev + 1);
      toast(getSuccessToast(
        "Correct!",
        `Great job! The answer is "${correctAnswer}"`
      ));
    } else {
      toast(getErrorToast(
        "Incorrect",
        `The correct answer was "${correctAnswer}"`
      ));
    }

    if (currentWordIndex < words.length - 1) {
      setCurrentWordIndex(prev => prev + 1);
      setAnswer("");
    } else {
      setGameState("finished");
      saveGameResult(score + (isCorrect ? 1 : 0), words.length);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && answer.trim() !== "") {
      checkAnswer();
    }
  };

  const formatDate = (date: Date) => {
    return format(new Date(date), 'MMM dd, yyyy HH:mm');
  };

  return (
    <div className="space-y-6">
      <CustomBreadcrumb items={breadcrumbItems} />
      
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">
          {groupName} Practice
        </h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            <span>Vocabulary Game</span>
            <div className="flex items-center gap-4">
              <div className="flex items-center space-x-2">
                <Switch
                  id="language-toggle"
                  checked={isRomanianToEnglish}
                  onCheckedChange={setIsRomanianToEnglish}
                />
                <Label htmlFor="language-toggle">
                  {isRomanianToEnglish ? "Romanian → English" : "English → Romanian"}
                </Label>
              </div>
              <Gamepad2 className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {gameState === "ready" && (
            <div className="text-center space-y-4">
              <p>Practice {words.length} words from {groupName}</p>
              <Button 
                onClick={startGame}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white"
              >
                <Play className="mr-2 h-4 w-4" />
                Start Practice
              </Button>
            </div>
          )}
          
          {gameState === "playing" && (
            <div className="text-center space-y-4">
              <p className="text-xl font-semibold">
                Translate: {isRomanianToEnglish 
                  ? words[currentWordIndex]?.romanian 
                  : words[currentWordIndex]?.english}
              </p>
              <div className="flex gap-4 justify-center">
                <Input
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={`Type the ${isRomanianToEnglish ? "English" : "Romanian"} translation`}
                  className="max-w-md"
                  autoFocus
                />
              </div>
              <Button 
                onClick={() => answer.trim() && checkAnswer()}
                disabled={!answer.trim()}
              >
                Check Answer
              </Button>
              <p>Progress: {currentWordIndex + 1}/{words.length}</p>
              <p>Score: {score}/{currentWordIndex}</p>
            </div>
          )}
          
          {gameState === "finished" && (
            <div className="text-center space-y-4">
              <p className="text-xl font-bold">Final Score: {score}/{words.length}</p>
              <p className="text-muted-foreground">
                {score === words.length 
                  ? "Perfect score! Amazing job! 🎉" 
                  : score >= words.length * 0.7 
                  ? "Great work! Keep practicing! 👏" 
                  : "Keep practicing to improve! 💪"}
              </p>
              <Button onClick={startGame}>
                <RotateCcw className="mr-2 h-4 w-4" />
                Play Again
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-muted-foreground" />
            Recent Practice Sessions
          </CardTitle>
        </CardHeader>
        <CardContent>
          {gameHistory.length > 0 ? (
            <div className="space-y-4">
              {gameHistory.slice(-5).reverse().map((session, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between border-b pb-2 last:border-0"
                >
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">
                      {formatDate(session.date)}
                    </p>
                    <div className="flex items-center gap-2">
                      <Star
                        className={`h-4 w-4 ${
                          session.score === session.totalWords
                            ? "text-yellow-500 fill-yellow-500"
                            : "text-muted-foreground"
                        }`}
                      />
                      <p className="font-medium">
                        Score: {session.score}/{session.totalWords}
                      </p>
                    </div>
                  </div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {Math.round((session.score / session.totalWords) * 100)}%
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-muted-foreground">
              No practice sessions completed yet. Start practicing to see your progress!
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default VocabularyGame;
