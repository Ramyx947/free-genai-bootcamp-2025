import { useParams, Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Volume2 } from "lucide-react";
import { CustomBreadcrumb } from "@/components/ui/custom-breadcrumb";

const groups = {
  1: {
    id: 1,
    name: "Kitchen",
    words: [
      { id: 1, romanian: "bucătărie", pronunciation: "boo-kuh-tuh-ree-eh", english: "kitchen", correct: 0, wrong: 0 },
      { id: 2, romanian: "masă", pronunciation: "mah-suh", english: "table", correct: 0, wrong: 0 },
      { id: 3, romanian: "scaun", pronunciation: "skown", english: "chair", correct: 0, wrong: 0 }
    ]
  },
  2: {
    id: 2,
    name: "Holiday",
    words: [
      { id: 1, romanian: "vacanță", pronunciation: "vah-kahn-tsuh", english: "holiday/vacation", correct: 0, wrong: 0 },
      { id: 2, romanian: "plajă", pronunciation: "plah-zhuh", english: "beach", correct: 0, wrong: 0 },
      { id: 3, romanian: "soare", pronunciation: "swa-reh", english: "sun", correct: 0, wrong: 0 }
    ]
  },
  3: {
    id: 3,
    name: "Travel",
    words: [
      { id: 1, romanian: "tren", pronunciation: "trehn", english: "train", correct: 0, wrong: 0 },
      { id: 2, romanian: "avion", pronunciation: "ah-vee-on", english: "airplane", correct: 0, wrong: 0 },
      { id: 3, romanian: "hotel", pronunciation: "ho-tehl", english: "hotel", correct: 0, wrong: 0 }
    ]
  },
  4: {
    id: 4,
    name: "Core Verbs",
    words: [
      { id: 1, romanian: "a fi", pronunciation: "ah fee", english: "to be", correct: 0, wrong: 0 },
      { id: 2, romanian: "a avea", pronunciation: "ah ah-veh-ah", english: "to have", correct: 0, wrong: 0 },
      { id: 3, romanian: "a merge", pronunciation: "ah mehr-geh", english: "to go/walk", correct: 0, wrong: 0 },
      { id: 4, romanian: "a face", pronunciation: "ah fah-cheh", english: "to do/make", correct: 0, wrong: 0 },
      { id: 5, romanian: "a vrea", pronunciation: "ah vreh-ah", english: "to want", correct: 0, wrong: 0 }
    ]
  }
} as const;

const GroupDetails = () => {
  const { id } = useParams();
  const groupId = id ? parseInt(id) : null;
  const group = groupId ? groups[groupId as keyof typeof groups] : null;

  const breadcrumbItems = [
    { label: "Groups", path: "/groups" },
    { label: group?.name || "Group Details" },
  ];

  if (!group) {
    return <div>Group not found</div>;
  }

  return (
    <div className="space-y-6">
      <CustomBreadcrumb items={breadcrumbItems} />
      
      <h1 className="text-3xl font-bold tracking-tight">Group Details</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>{group.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Romanian</TableHead>
                <TableHead>Pronunciation</TableHead>
                <TableHead>English</TableHead>
                <TableHead className="text-right">Correct</TableHead>
                <TableHead className="text-right">Wrong</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {group.words.map((word) => (
                <TableRow key={word.id}>
                  <TableCell data-label="Romanian">{word.romanian}</TableCell>
                  <TableCell data-label="Pronunciation">{word.pronunciation}</TableCell>
                  <TableCell data-label="English">{word.english}</TableCell>
                  <TableCell data-label="Correct" className="text-right">{word.correct}</TableCell>
                  <TableCell data-label="Wrong" className="text-right">{word.wrong}</TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon">
                      <Volume2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default GroupDetails;
