
import { CustomCard } from "@/components/ui/custom-card";
import { GraduationCap } from "lucide-react";

const StudyActivities = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Study Activities</h1>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <CustomCard
          title="Vocabulary Practice"
          description="Practice new vocabulary with interactive exercises"
          to="/study-activities/vocabulary"
        >
          <div className="flex items-center justify-end">
            <GraduationCap className="h-5 w-5 text-muted-foreground" />
          </div>
        </CustomCard>

        <CustomCard
          title="Reading Comprehension"
          description="Improve your reading skills with Romanian texts"
          to="/study-activities/reading"
        >
          <div className="flex items-center justify-end">
            <GraduationCap className="h-5 w-5 text-muted-foreground" />
          </div>
        </CustomCard>

        <CustomCard
          title="Grammar Exercises"
          description="Practice Romanian grammar with structured exercises"
          to="/study-activities/grammar"
        >
          <div className="flex items-center justify-end">
            <GraduationCap className="h-5 w-5 text-muted-foreground" />
          </div>
        </CustomCard>
      </div>
    </div>
  );
};

export default StudyActivities;
