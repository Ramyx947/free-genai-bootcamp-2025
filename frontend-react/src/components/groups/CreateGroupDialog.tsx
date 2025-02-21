
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import { WordGroup } from "@/types/group";

interface CreateGroupDialogProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  onGroupCreate: (group: WordGroup) => void;
  groups: WordGroup[];
}

export const CreateGroupDialog = ({
  isOpen,
  onOpenChange,
  onGroupCreate,
  groups,
}: CreateGroupDialogProps) => {
  const [newGroupName, setNewGroupName] = useState("");
  const [description, setDescription] = useState("");
  const { toast } = useToast();

  const handleCreateGroup = () => {
    if (!newGroupName.trim()) {
      toast({
        title: "Error",
        description: "Please enter a group name",
        variant: "destructive",
      });
      return;
    }
    
    const newGroup: WordGroup = {
      id: Math.max(...groups.map(g => g.id)) + 1,
      name: newGroupName.trim(),
      wordCount: 0,
      description: description.trim() || `Vocabulary group for ${newGroupName.trim()}`
    };
    
    onGroupCreate(newGroup);
    toast({
      title: "Success",
      description: "Group created successfully",
    });
    
    setNewGroupName("");
    setDescription("");
    onOpenChange(false);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Group</DialogTitle>
        </DialogHeader>
        <div className="py-4 space-y-4">
          <Input
            placeholder="Enter group name"
            value={newGroupName}
            onChange={(e) => setNewGroupName(e.target.value)}
          />
          <Textarea
            placeholder="Enter group description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
          />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleCreateGroup}>
            Create
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
