
import { CustomCard } from "@/components/ui/custom-card";
import { BookOpen, GraduationCap, List, ListCheck } from "lucide-react";
import { WordGroup } from "@/types/group";

const INITIAL_GROUPS: WordGroup[] = [
  {
    id: 1,
    name: "Kitchen",
    wordCount: 15,
    description: "Kitchen-related vocabulary for everyday use"
  },
  {
    id: 2,
    name: "Holiday",
    wordCount: 12,
    description: "Words and phrases for holiday situations"
  },
  {
    id: 3,
    name: "Travel",
    wordCount: 20,
    description: "Essential vocabulary for traveling"
  },
  {
    id: 4,
    name: "Core Verbs",
    wordCount: 8,
    description: "Fundamental Romanian verbs"
  }
];

const Index = () => {
  const totalWords = INITIAL_GROUPS.reduce((sum, group) => sum + group.wordCount, 0);
  const totalGroups = INITIAL_GROUPS.length;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <CustomCard
          title="Words"
          description={`${totalWords} words in your collection`}
          to="/words"
        >
          <div className="flex items-center justify-end">
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </div>
        </CustomCard>

        <CustomCard
          title="Groups"
          description={`${totalGroups} word groups created`}
          to="/groups"
        >
          <div className="flex items-center justify-end">
            <List className="h-4 w-4 text-muted-foreground" />
          </div>
        </CustomCard>

        <CustomCard
          title="Study Activities"
          description="3 available activities"
          to="/study-activities"
        >
          <div className="flex items-center justify-end">
            <GraduationCap className="h-4 w-4 text-muted-foreground" />
          </div>
        </CustomCard>

        <CustomCard
          title="Sessions"
          description="0 learning sessions completed"
          to="/sessions"
        >
          <div className="flex items-center justify-end">
            <ListCheck className="h-4 w-4 text-muted-foreground" />
          </div>
        </CustomCard>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <CustomCard
          title="Recent Activity"
          description="Your learning progress this week"
        >
          <p className="text-sm text-muted-foreground">No recent activity</p>
        </CustomCard>

        <CustomCard
          title="Quick Stats"
          description="Overview of your learning journey"
        >
          <p className="text-sm text-muted-foreground">Start learning to see your stats!</p>
        </CustomCard>
      </div>
    </div>
  );
};

export default Index;
