import { useState, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CustomCard } from "@/components/ui/custom-card";
import { Button } from "@/components/ui/button";
import { Plus, Volume2, Play, Search } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { 
  Pagination, 
  PaginationContent, 
  PaginationItem, 
  PaginationNext, 
  PaginationPrevious 
} from "@/components/ui/pagination";

type SortField = 'romanian' | 'pronunciation' | 'english' | 'correct' | 'wrong';
type SortOrder = 'asc' | 'desc';

const ITEMS_PER_PAGE = 20;

const commonWords = [
  { 
    id: 1, 
    romanian: "eu", 
    pronunciation: "yeh-oo", 
    english: "I", 
    correct: 0, 
    wrong: 0,
    description: "First-person singular pronoun. Used in both formal and informal contexts.",
    details: "As a subject pronoun, 'eu' is often omitted in Romanian unless emphasis is needed. Unlike English, Romanian verbs contain person information, making the pronoun optional in many cases.",
    groups: ["Pronouns"]
  },
  { 
    id: 2, 
    romanian: "tu", 
    pronunciation: "too", 
    english: "you (singular)", 
    correct: 0, 
    wrong: 0,
    description: "Second-person singular pronoun - informal. Used with friends, family, children, or in casual settings.",
    details: "Using 'tu' implies familiarity or closeness with the person being addressed. In formal situations, use 'dumneavoastră' instead to show respect.",
    groups: ["Pronouns"]
  },
  { 
    id: 3, 
    romanian: "dumneavoastră", 
    pronunciation: "doom-nea-voas-tră", 
    english: "you (formal)", 
    correct: 0, 
    wrong: 0,
    description: "Formal second-person pronoun. Used to show respect to elders, in professional settings, or with strangers.",
    details: "This formal pronoun can be used for both singular and plural. It always requires verb conjugation in the second person plural, regardless of whether addressing one or multiple people.",
    groups: ["Pronouns"]
  },
  { 
    id: 4, 
    romanian: "el", 
    pronunciation: "yehl", 
    english: "he", 
    correct: 0, 
    wrong: 0,
    description: "Third-person singular masculine pronoun.",
    details: "Used for masculine nouns and when referring to male persons. In Romanian, the pronoun can often be omitted when it's clear from context who is being referred to.",
    groups: ["Pronouns"]
  },
  { 
    id: 5, 
    romanian: "ea", 
    pronunciation: "yah", 
    english: "she", 
    correct: 0, 
    wrong: 0,
    description: "Third-person singular feminine pronoun.",
    details: "Used for feminine nouns and when referring to female persons. Like other subject pronouns in Romanian, it can be omitted when the context is clear.",
    groups: ["Pronouns"]
  },
  { 
    id: 6, 
    romanian: "noi", 
    pronunciation: "noy", 
    english: "we", 
    correct: 0, 
    wrong: 0,
    description: "First-person plural pronoun.",
    details: "Used in both formal and informal contexts. The verb endings change to match the first person plural form when using 'noi'.",
    groups: ["Pronouns"]
  },
  { 
    id: 7, 
    romanian: "voi", 
    pronunciation: "voy", 
    english: "you (plural)", 
    correct: 0, 
    wrong: 0,
    description: "Second-person plural pronoun - informal.",
    details: "Used when addressing multiple people in informal situations. For formal situations addressing multiple people, use 'dumneavoastră'.",
    groups: ["Pronouns"]
  },
  { 
    id: 8, 
    romanian: "ei", 
    pronunciation: "yey", 
    english: "they (masculine)", 
    correct: 0, 
    wrong: 0,
    description: "Third-person plural masculine pronoun.",
    details: "Used for groups containing at least one masculine noun/person. In Romanian, masculine plural is used as the default when referring to mixed groups.",
    groups: ["Pronouns"]
  },
  { 
    id: 9, 
    romanian: "ele", 
    pronunciation: "yeh-leh", 
    english: "they (feminine)", 
    correct: 0, 
    wrong: 0,
    description: "Third-person plural feminine pronoun.",
    details: "Used only when referring to groups consisting entirely of feminine nouns/persons.",
    groups: ["Pronouns"]
  },
  { 
    id: 10, 
    romanian: "și", 
    pronunciation: "shee", 
    english: "and", 
    correct: 0, 
    wrong: 0,
    description: "One of the most common connecting words in Romanian language, used to link ideas and sentences.",
    groups: ["Core Verbs", "Travel"]
  },
  { 
    id: 11, 
    romanian: "nu", 
    pronunciation: "noo", 
    english: "no", 
    correct: 3, 
    wrong: 1,
    description: "The primary negative word in Romanian, used in everyday conversations to express disagreement or negation.",
    groups: ["Core Verbs", "Holiday"]
  },
  { 
    id: 12, 
    romanian: "da", 
    pronunciation: "dah", 
    english: "yes", 
    correct: 5, 
    wrong: 0,
    description: "The affirmative word in Romanian, frequently used in daily conversations to express agreement.",
    groups: ["Core Verbs"]
  },
  { id: 13, romanian: "casa", pronunciation: "kah-sah", english: "house", correct: 0, wrong: 0, description: "'Casa' means 'house' in Romanian, representing a place of residence or dwelling.", groups: [] },
  { id: 14, romanian: "apă", pronunciation: "ah-puh", english: "water", correct: 0, wrong: 0, description: "'Apă' is the Romanian word for 'water,' an essential element for life and often used symbolically.", groups: [] },
  { id: 15, romanian: "pâine", pronunciation: "puh-ee-neh", english: "bread", correct: 0, wrong: 0, description: "'Pâine' means 'bread' in Romanian, a staple food and a symbol of nourishment and sustenance.", groups: [] },
  { id: 16, romanian: "familie", pronunciation: "fah-mee-lee-eh", english: "family", correct: 0, wrong: 0, description: "'Familie' is the Romanian word for 'family,' representing a group of people related by blood, marriage, or adoption.", groups: [] },
  { 
    id: 17, 
    romanian: "bucătărie", 
    pronunciation: "boo-kuh-tuh-ree-eh", 
    english: "kitchen", 
    correct: 0, 
    wrong: 0,
    description: "The room where food is prepared and cooked.",
    groups: ["Kitchen"]
  },
  { 
    id: 18, 
    romanian: "farfurie", 
    pronunciation: "far-foo-ree-eh", 
    english: "plate", 
    correct: 0, 
    wrong: 0,
    description: "A flat dish used for serving food.",
    groups: ["Kitchen"]
  },
  { 
    id: 19, 
    romanian: "lingură", 
    pronunciation: "leen-goo-ruh", 
    english: "spoon", 
    correct: 0, 
    wrong: 0,
    description: "A type of eating utensil with a shallow bowl-shaped end.",
    groups: ["Kitchen"]
  },
  { 
    id: 20, 
    romanian: "furculiță", 
    pronunciation: "foor-koo-lee-tsuh", 
    english: "fork", 
    correct: 0, 
    wrong: 0,
    description: "An eating utensil with prongs used for picking up food.",
    groups: ["Kitchen"]
  },
  { 
    id: 21, 
    romanian: "cuțit", 
    pronunciation: "koo-tseet", 
    english: "knife", 
    correct: 0, 
    wrong: 0,
    description: "A cutting utensil with a sharp blade.",
    groups: ["Kitchen"]
  },
  { 
    id: 22, 
    romanian: "frumos", 
    pronunciation: "froo-mos", 
    english: "beautiful", 
    correct: 0, 
    wrong: 0,
    description: "Pleasing to the senses or mind aesthetically.",
    groups: ["Adjectives"]
  },
  { 
    id: 23, 
    romanian: "mare", 
    pronunciation: "mah-reh", 
    english: "big", 
    correct: 0, 
    wrong: 0,
    description: "Of considerable size, extent, or intensity.",
    groups: ["Adjectives"]
  },
  { 
    id: 24, 
    romanian: "mic", 
    pronunciation: "meek", 
    english: "small", 
    correct: 0, 
    wrong: 0,
    description: "Of a size that is less than normal or usual.",
    groups: ["Adjectives"]
  },
  { 
    id: 25, 
    romanian: "bun", 
    pronunciation: "boon", 
    english: "good", 
    correct: 0, 
    wrong: 0,
    description: "To be desired or approved of.",
    groups: ["Adjectives"]
  },
  { 
    id: 26, 
    romanian: "rău", 
    pronunciation: "ruh-oo", 
    english: "bad", 
    correct: 0, 
    wrong: 0,
    description: "Of poor quality or low standard.",
    groups: ["Adjectives"]
  },
  { 
    id: 27, 
    romanian: "a merge", 
    pronunciation: "ah mair-jeh", 
    english: "to go", 
    correct: 0, 
    wrong: 0,
    description: "To move from one place to another.",
    groups: ["Verbs"]
  },
  { 
    id: 28, 
    romanian: "a veni", 
    pronunciation: "ah veh-nee", 
    english: "to come", 
    correct: 0, 
    wrong: 0,
    description: "To move towards or approach someone or something.",
    groups: ["Verbs"]
  },
  { 
    id: 29, 
    romanian: "a mânca", 
    pronunciation: "ah muhn-kah", 
    english: "to eat", 
    correct: 0, 
    wrong: 0,
    description: "To put food into your mouth and swallow it.",
    groups: ["Verbs", "Kitchen"]
  },
  { 
    id: 30, 
    romanian: "a bea", 
    pronunciation: "ah beh-ah", 
    english: "to drink", 
    correct: 0, 
    wrong: 0,
    description: "To take liquid into your mouth and swallow it.",
    groups: ["Verbs", "Kitchen"]
  },
  { 
    id: 31, 
    romanian: "a dormi", 
    pronunciation: "ah dor-mee", 
    english: "to sleep", 
    correct: 0, 
    wrong: 0,
    description: "To be in a state of rest with your eyes closed.",
    groups: ["Verbs"]
  },
  { 
    id: 32, 
    romanian: "mamă", 
    pronunciation: "mah-muh", 
    english: "mother", 
    correct: 0, 
    wrong: 0,
    description: "Female parent.",
    groups: ["Family"]
  },
  { 
    id: 33, 
    romanian: "tată", 
    pronunciation: "tah-tuh", 
    english: "father", 
    correct: 0, 
    wrong: 0,
    description: "Male parent.",
    groups: ["Family"]
  },
  { 
    id: 34, 
    romanian: "soră", 
    pronunciation: "so-ruh", 
    english: "sister", 
    correct: 0, 
    wrong: 0,
    description: "Female sibling.",
    groups: ["Family"]
  },
  { 
    id: 35, 
    romanian: "frate", 
    pronunciation: "frah-teh", 
    english: "brother", 
    correct: 0, 
    wrong: 0,
    description: "Male sibling.",
    groups: ["Family"]
  },
  { 
    id: 36, 
    romanian: "bunic", 
    pronunciation: "boo-neek", 
    english: "grandfather", 
    correct: 0, 
    wrong: 0,
    description: "The father of one's parent.",
    groups: ["Family"]
  },
  { 
    id: 37, 
    romanian: "bunică", 
    pronunciation: "boo-nee-kuh", 
    english: "grandmother", 
    correct: 0, 
    wrong: 0,
    description: "The mother of one's parent.",
    groups: ["Family"]
  },
  { 
    id: 38, 
    romanian: "a găti", 
    pronunciation: "ah guh-tee", 
    english: "to cook", 
    correct: 0, 
    wrong: 0,
    description: "To prepare food by heating it.",
    groups: ["Verbs", "Kitchen"]
  },
  { 
    id: 39, 
    romanian: "ceașcă", 
    pronunciation: "chahs-kuh", 
    english: "cup", 
    correct: 0, 
    wrong: 0,
    description: "A small container used for drinking.",
    groups: ["Kitchen"]
  },
  { 
    id: 40, 
    romanian: "pahar", 
    pronunciation: "pah-har", 
    english: "glass", 
    correct: 0, 
    wrong: 0,
    description: "A container made of glass used for drinking.",
    groups: ["Kitchen"]
  },
  { 
    id: 41, 
    romanian: "înalt", 
    pronunciation: "ee-nalt", 
    english: "tall", 
    correct: 0, 
    wrong: 0,
    description: "Of great vertical extent.",
    groups: ["Adjectives"]
  },
  { 
    id: 42, 
    romanian: "scund", 
    pronunciation: "skoond", 
    english: "short", 
    correct: 0, 
    wrong: 0,
    description: "Of little height.",
    groups: ["Adjectives"]
  },
  { 
    id: 43, 
    romanian: "a spăla", 
    pronunciation: "ah spuh-lah", 
    english: "to wash", 
    correct: 0, 
    wrong: 0,
    description: "To clean with water.",
    groups: ["Verbs", "Kitchen"]
  },
  { 
    id: 44, 
    romanian: "verișoară", 
    pronunciation: "veh-ree-shwa-ruh", 
    english: "female cousin", 
    correct: 0, 
    wrong: 0,
    description: "The daughter of one's aunt or uncle.",
    groups: ["Family"]
  },
  { 
    id: 45, 
    romanian: "văr", 
    pronunciation: "vuhr", 
    english: "male cousin", 
    correct: 0, 
    wrong: 0,
    description: "The son of one's aunt or uncle.",
    groups: ["Family"]
  },
  { 
    id: 46, 
    romanian: "oală", 
    pronunciation: "wa-luh", 
    english: "pot", 
    correct: 0, 
    wrong: 0,
    description: "A deep container used for cooking.",
    groups: ["Kitchen"]
  },
  { 
    id: 47, 
    romanian: "tigaie", 
    pronunciation: "tee-gah-yeh", 
    english: "frying pan", 
    correct: 0, 
    wrong: 0,
    description: "A flat-bottomed pan used for frying food.",
    groups: ["Kitchen"]
  },
  { 
    id: 48, 
    romanian: "vesel", 
    pronunciation: "veh-sel", 
    english: "happy", 
    correct: 0, 
    wrong: 0,
    description: "Feeling or showing pleasure or contentment.",
    groups: ["Adjectives"]
  },
  { 
    id: 49, 
    romanian: "trist", 
    pronunciation: "treest", 
    english: "sad", 
    correct: 0, 
    wrong: 0,
    description: "Feeling or showing sorrow.",
    groups: ["Adjectives"]
  },
  { 
    id: 50, 
    romanian: "nepot", 
    pronunciation: "neh-pot", 
    english: "grandson/nephew", 
    correct: 0, 
    wrong: 0,
    description: "The son of one's child or sibling.",
    groups: ["Family"]
  }
];

const Words = () => {
  const [sortField, setSortField] = useState<SortField>('romanian');
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedGroup, setSelectedGroup] = useState<string>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const navigate = useNavigate();

  // Extract unique groups from commonWords
  const uniqueGroups = useMemo(() => {
    const groups = new Set<string>();
    commonWords.forEach(word => {
      word.groups.forEach(group => groups.add(group));
    });
    return Array.from(groups).sort();
  }, []);

  // Filter words based on search term and selected group
  const filteredWords = useMemo(() => {
    return commonWords.filter(word => {
      const matchesSearch = searchTerm === '' || 
        word.romanian.toLowerCase().includes(searchTerm.toLowerCase()) ||
        word.english.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesGroup = selectedGroup === 'all' || 
        word.groups.includes(selectedGroup);

      return matchesSearch && matchesGroup;
    });
  }, [searchTerm, selectedGroup]);

  // Calculate pagination
  const totalPages = Math.ceil(filteredWords.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedWords = filteredWords.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  const handlePractice = (e: React.MouseEvent, groups: string[]) => {
    e.preventDefault();
    navigate('/study-activities/vocabulary', { 
      state: { 
        wordGroups: groups,
        source: 'words'
      }
    });
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-3">
            Word Collection
            <div className="flex h-5">
              <div className="w-2 h-full bg-[#ea384c]"></div>
              <div className="w-2 h-full bg-[#ffd700]"></div>
              <div className="w-2 h-full bg-[#0057b8]"></div>
            </div>
          </h1>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Word
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search in English or Romanian..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select
          value={selectedGroup}
          onValueChange={setSelectedGroup}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select group" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Groups</SelectItem>
            {uniqueGroups.map((group) => (
              <SelectItem key={group} value={group}>
                {group}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      
      <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-4">
        {paginatedWords.map((word) => (
          <CustomCard
            key={word.id}
            title={
              <div className="flex flex-col gap-1">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="break-words">{word.romanian}</span>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-6 w-6 shrink-0 self-center"
                    >
                      <Volume2 className="h-3 w-3" />
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-1 justify-end">
                    {word.groups.slice(0, 2).map((group, index) => (
                      <Badge 
                        key={index}
                        variant="outline" 
                        className="text-[10px] bg-sky-50 text-sky-700 border-sky-200 whitespace-nowrap hover:bg-sky-100 dark:bg-sky-900/30 dark:text-sky-300 dark:border-sky-800"
                      >
                        {group}
                      </Badge>
                    ))}
                    {word.groups.length > 2 && (
                      <Badge 
                        variant="outline" 
                        className="text-[10px] bg-sky-50 text-sky-700 border-sky-200 whitespace-nowrap hover:bg-sky-100 dark:bg-sky-900/30 dark:text-sky-300 dark:border-sky-800"
                      >
                        +{word.groups.length - 2} more
                      </Badge>
                    )}
                  </div>
                </div>
                <div className="text-xs italic text-purple-600 dark:text-purple-400">
                  {word.pronunciation}
                </div>
              </div>
            }
            description={word.english}
            to={`/words/${word.id}`}
            className="flex flex-col"
            footer={
              <div className="flex items-center justify-start w-full gap-1">
                <Badge variant="secondary" className="text-xs bg-purple-100 text-purple-800 hover:bg-purple-100">
                  Correct: {word.correct}
                </Badge>
                <Badge variant="secondary" className="text-xs bg-orange-100 text-orange-800 hover:bg-orange-100">
                  Wrong: {word.wrong}
                </Badge>
              </div>
            }
          >
            <div className="flex flex-col">
              <div>
                <div className="text-sm text-gray-600 dark:text-gray-300 mb-2 line-clamp-2">
                  {word.description}
                </div>
              </div>
              {word.groups.length > 0 && (
                <Button
                  onClick={(e) => handlePractice(e, word.groups)}
                  className="bg-purple-600 hover:bg-purple-700 text-white dark:bg-purple-500 dark:hover:bg-purple-600 w-fit"
                  size="sm"
                >
                  <Play className="h-3 w-3 mr-1" />
                  Practice
                </Button>
              )}
            </div>
          </CustomCard>
        ))}
      </div>
      
      {filteredWords.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          No words found matching your search criteria
        </div>
      ) : (
        <Pagination className="mt-8">
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                onClick={() => handlePageChange(currentPage - 1)}
                className={`${
                  currentPage === 1 || filteredWords.length === 0
                    ? 'pointer-events-none opacity-50'
                    : 'hover:shadow-sm'
                }`}
              />
            </PaginationItem>
            <PaginationItem>
              <span className="flex h-9 items-center px-4 text-sm font-medium">
                {currentPage} of {totalPages}
              </span>
            </PaginationItem>
            <PaginationItem>
              <PaginationNext
                onClick={() => handlePageChange(currentPage + 1)}
                className={`${
                  currentPage === totalPages || filteredWords.length === 0
                    ? 'pointer-events-none opacity-50'
                    : 'hover:shadow-sm'
                }`}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}
    </div>
  );
};

export default Words;
