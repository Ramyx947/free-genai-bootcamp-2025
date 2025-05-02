import { RouteObject } from "react-router-dom";
import Index from "@/pages/Index";
import StudyActivities from "@/pages/StudyActivities";
import StudyActivityDetails from "@/pages/StudyActivityDetails";
import VocabularyPractice from "@/pages/study-activities/vocabulary";
import VocabularyGame from "@/pages/study-activities/vocabulary-game";
import Words from "@/pages/Words";
import WordDetails from "@/pages/WordDetails";
import Groups from "@/pages/Groups";
import GroupDetails from "@/pages/GroupDetails";
import Sessions from "@/pages/Sessions";
import Settings from "@/pages/Settings";
import Terms from "@/pages/Terms";
import Privacy from "@/pages/Privacy";
import Support from "@/pages/Support";
import Feedback from "@/pages/Feedback";
import About from "@/pages/About";
import NotFound from "@/pages/NotFound";
import { ListeningPractice } from "@/components/study/ListeningPractice";
import { SpeakingPractice } from '@/components/speaking/SpeakingPractice';
import { WritingPractice } from "@/pages/WritingPractice";
import { StudyActivities as StudyActivitiesComponent } from "@/components/study/StudyActivities";

export const routes: RouteObject[] = [
  {
    path: "/",
    element: <Index />,
  },
  {
    path: "/dashboard",
    element: <Index />,
  },
  {
    path: "/study",
    element: <StudyActivitiesComponent />,
  },
  {
    path: "/study-activities/:id",
    element: <StudyActivityDetails />,
  },
  {
    path: "/study-activities/vocabulary",
    element: <VocabularyPractice />,
  },
  {
    path: "/study-activities/vocabulary/:groupId",
    element: <VocabularyGame />,
  },
  {
    path: "/words",
    element: <Words />,
  },
  {
    path: "/words/:id",
    element: <WordDetails />,
  },
  {
    path: "/groups",
    element: <Groups />,
  },
  {
    path: "/groups/:id",
    element: <GroupDetails />,
  },
  {
    path: "/sessions",
    element: <Sessions />,
  },
  {
    path: "/settings",
    element: <Settings />,
  },
  {
    path: "/terms",
    element: <Terms />,
  },
  {
    path: "/privacy",
    element: <Privacy />,
  },
  {
    path: "/support",
    element: <Support />,
  },
  {
    path: "/feedback",
    element: <Feedback />,
  },
  {
    path: "/about",
    element: <About />,
  },
  {
    path: "/study/listening",
    element: <ListeningPractice />,
  },
  {
    path: "/study/speaking",
    element: <SpeakingPractice />,
  },
  {
    path: "/study/writing",
    element: <WritingPractice />,
  },
  {
    path: "*",
    element: <NotFound />,
  },
];
