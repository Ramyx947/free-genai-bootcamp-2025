
import { useParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Volume2 } from "lucide-react";
import { CustomBreadcrumb } from "@/components/ui/custom-breadcrumb";

const WordDetails = () => {
  const { id } = useParams();
  
  // Find the word from commonWords array (you'll need to import or fetch this)
  const word = {
    romanian: "dumneavoastră",
    english: "you (formal)",
    pronunciation: "doom-nea-voas-tră",
    description: "Formal second-person pronoun. Used to show respect to elders, in professional settings, or with strangers.",
    details: "This formal pronoun can be used for both singular and plural. It always requires verb conjugation in the second person plural, regardless of whether addressing one or multiple people. In written communication, it's often capitalized (Dumneavoastră) to show additional respect. The pronoun comes from 'domnia voastră' meaning 'your lordship' and its formal nature reflects this historic origin."
  };

  const breadcrumbItems = [
    { label: "Words", path: "/words" },
    { label: "Word Details", path: `/words/${id}` },
  ];

  return (
    <div className="space-y-6">
      <CustomBreadcrumb items={breadcrumbItems} />
      
      <h1 className="text-3xl font-bold tracking-tight">Word Details</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Word Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold">{word.romanian}</h2>
                <p className="text-muted-foreground">{word.english}</p>
              </div>
              <Button variant="outline" size="icon">
                <Volume2 className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-2">
              <h3 className="font-medium">Pronunciation</h3>
              <p className="text-purple-600 dark:text-purple-400 italic">
                {word.pronunciation}
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-medium">Description</h3>
              <p className="text-muted-foreground">{word.description}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Additional Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-muted-foreground leading-relaxed">
                {word.details}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default WordDetails;
