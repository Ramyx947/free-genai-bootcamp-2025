
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CustomBreadcrumb } from "@/components/ui/custom-breadcrumb";
import { useToast } from "@/hooks/use-toast";
import { GameState, WordItem } from "@/types/vocabulary-game";
import { Play, Gamepad2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { WordGroup } from "@/types/group";

const INITIAL_GROUPS: WordGroup[] = [
  {
    id: 1,
    name: "Kitchen",
    wordCount: 15,
    description: "Practice kitchen-related vocabulary with interactive exercises",
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
    description: "Learn holiday and vacation terms through engaging activities",
    words: [
      { romanian: "plajă", english: "beach" },
      { romanian: "vacanță", english: "vacation" },
      { romanian: "hotel", english: "hotel" },
      { romanian: "mare", english: "sea" }
    ]
  },
  {
    id: 3,
    name: "Travel",
    wordCount: 20,
    description: "Master essential travel vocabulary with fun exercises",
    words: [
      { romanian: "avion", english: "airplane" },
      { romanian: "tren", english: "train" },
      { romanian: "autobuz", english: "bus" },
      { romanian: "stație", english: "station" }
    ]
  },
  {
    id: 4,
    name: "Core Verbs",
    wordCount: 8,
    description: "Practice fundamental Romanian verbs through interactive games",
    words: [
      { romanian: "sunt", english: "am" },
      { romanian: "este", english: "is" },
      { romanian: "nu", english: "no" },
      { romanian: "da", english: "yes" }
    ]
  }
];

const VocabularyPractice = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [filteredGroups, setFilteredGroups] = useState<WordGroup[]>(INITIAL_GROUPS);
  
  const breadcrumbItems = [
    ...(location.state?.source === 'words' 
      ? [{ 
          label: "Words", 
          path: "/words",
          state: { source: 'words' }
        }]
      : location.state?.source === 'groups'
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
      state: location.state 
    }
  ];

  useEffect(() => {
    const { wordGroups } = location.state || {};
    if (wordGroups && Array.isArray(wordGroups)) {
      const filtered = INITIAL_GROUPS.filter(group => 
        wordGroups.includes(group.name)
      );
      setFilteredGroups(filtered);
    }
  }, [location]);

  const handleGroupSelect = (groupId: number) => {
    const selectedGroup = filteredGroups.find(g => g.id === groupId);
    navigate(`/study-activities/vocabulary/${groupId}`, {
      state: { 
        ...location.state,
        selectedGroup: selectedGroup?.name 
      }
    });
  };

  return (
    <div className="space-y-6">
      <CustomBreadcrumb items={breadcrumbItems} />
      
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Vocabulary Practice</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredGroups.map((group) => (
          <Card key={group.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                <span>{group.name}</span>
                <Gamepad2 className="h-5 w-5 text-muted-foreground" />
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">{group.description}</p>
              <p className="text-sm">Words: {group.wordCount}</p>
              <Button 
                onClick={() => handleGroupSelect(group.id)}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white dark:bg-purple-500 dark:hover:bg-purple-600"
              >
                <Play className="mr-2 h-4 w-4" />
                Practice Now
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default VocabularyPractice;
