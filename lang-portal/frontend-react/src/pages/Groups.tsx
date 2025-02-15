
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, List } from "lucide-react";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { CreateGroupDialog } from "@/components/groups/CreateGroupDialog";
import { GroupsTable } from "@/components/groups/GroupsTable";
import { WordGroup, SortField, SortOrder } from "@/types/group";
import { useNavigate } from "react-router-dom";

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

const Groups = () => {
  const [sortField, setSortField] = useState<SortField>('name');
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [groups, setGroups] = useState<WordGroup[]>(INITIAL_GROUPS);
  const navigate = useNavigate();

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  const sortedGroups = [...groups].sort((a, b) => {
    const modifier = sortOrder === 'asc' ? 1 : -1;
    if (sortField === 'name') {
      return a.name.localeCompare(b.name) * modifier;
    }
    return (a.wordCount - b.wordCount) * modifier;
  });

  const handleCreateGroup = (newGroup: WordGroup) => {
    setGroups(prevGroups => [...prevGroups, newGroup]);
  };

  const handlePractice = (groupId: number) => {
    navigate(`/study-activities/vocabulary/${groupId}`, { 
      state: { source: 'groups' }
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Word Groups</h1>
        <Button onClick={() => setIsCreateOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Group
        </Button>
      </div>
      
      <Card className="hover:shadow-lg transition-shadow hover:bg-gradient-to-br from-gray-50 to-gray-200 backdrop-blur-sm">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-lg font-medium">My Groups</CardTitle>
          <List className="h-5 w-5 text-muted-foreground" />
        </CardHeader>
        <CardContent className="text-black">
          <GroupsTable 
            groups={sortedGroups}
            sortField={sortField}
            sortOrder={sortOrder}
            onSort={handleSort}
            onPractice={handlePractice}
          />
        </CardContent>
      </Card>

      <div className="px-6">
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious 
                href="#"
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                className={`${
                  currentPage === 1 || groups.length === 0
                    ? 'pointer-events-none opacity-50'
                    : ''
                }`}
              />
            </PaginationItem>
            <PaginationItem>
              <span className="px-4 py-2">
                {currentPage} of {Math.max(1, Math.ceil(groups.length / 10))}
              </span>
            </PaginationItem>
            <PaginationItem>
              <PaginationNext 
                href="#"
                onClick={() => setCurrentPage(p => p + 1)}
                className={`${
                  currentPage >= Math.ceil(groups.length / 10) || groups.length === 0
                    ? 'pointer-events-none opacity-50'
                    : ''
                }`}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>

      <CreateGroupDialog 
        isOpen={isCreateOpen}
        onOpenChange={setIsCreateOpen}
        onGroupCreate={handleCreateGroup}
        groups={groups}
      />
    </div>
  );
};

export default Groups;
