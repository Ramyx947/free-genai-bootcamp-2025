import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Headphones, Mic, Pencil } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const StudyActivities = () => {
  const navigate = useNavigate();

  const activities = [
    {
      title: "Listening Practice",
      description: "Practice listening comprehension with YouTube videos",
      icon: <Headphones className="h-6 w-6" />,
      onClick: () => navigate("/study/listening"),
      color: "bg-blue-500"
    },
    {
      title: "Speaking Practice",
      description: "Practice pronunciation and speaking skills",
      icon: <Mic className="h-6 w-6" />,
      onClick: () => navigate("/study/speaking"),
      color: "bg-green-500"
    },
    {
      title: "Writing Practice",
      description: "Practice writing in Romanian",
      icon: <Pencil className="h-6 w-6" />,
      onClick: () => navigate("/study/writing"),
      color: "bg-purple-500"
    }
  ];

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">Study Activities</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {activities.map((activity) => (
          <Card key={activity.title} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className={`${activity.color} w-12 h-12 rounded-full flex items-center justify-center text-white mb-4`}>
                {activity.icon}
              </div>
              <CardTitle>{activity.title}</CardTitle>
              <CardDescription>{activity.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={activity.onClick}
                className="w-full"
                variant="outline"
              >
                Start Practice
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}; 