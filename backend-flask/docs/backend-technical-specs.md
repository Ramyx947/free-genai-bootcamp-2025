# Backend Server Technical Specifications

## Business Goal: 
A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a  Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps

You have been tasked with creating the backend API of the application.

## Technical Requirements:
- The backend will be written in Python
- The database will be SQLite3
- The API will be built using Flask
- The API will be JSON only
- There will be no authentication/authorization, 
- Everything will be treated as for a single user


## Database Schema

Our database will be a single user database called 'words.db' that will be created in the root of the project folder of the backend-flask.
We will use the following tables:

- `words`  - stored vocabulary words
    - `id` integer
    - `romanian`  string
    - `english` string
    - `parts` - json

- `words_groups` - joint table for words and groups - many -to -many
    - `id` integer
    - `word_id` integer
    - `group_id` integer
- `groups` - thematic groups of words
    - `id` integer
    - `name` string
- `study_sessions` - records of study sessions grouping `word_review_items`
    - `id` integer
    - `group_id`  integer
    - `created_at` datatime
    - `study_activity_id` integer
- `study_activities` - a specific study activity, linking a study session to group
    - `id` integer
    - `study_session_id` integer
    - `group_id` integer
    - `created_at` datatime
- `word_review_items`  a record of word practice, determining if the word was correct or not.
    - `word_id`  integer
    - `study_session_id` integer
    - `correct` boolean
    - `created_at` datatime



## API Endpoints

### GET /api/dashboard/last_study_session

**Description:**
Returns information about the most recent study session.

**Example JSON Response:**

```json
{
    "id": 15,
    "group_id": 3,
    "created_at": "2023-10-05T16:30:00Z",
    "group_id": 3,
    "group_name": "Common Verbs",
    "study_activity_id": 8,
}
```

### GET /api/dashboard/study_progress

**Description:**  
Returns study progress statistics. 
Please note that the frontend will display the will determine progress bar based on the total words studied and total words available.

**Example JSON Response:**

```json
{
    "total_words_studied": 4,
    "total_available_words": 240,
}
```

---

### GET /api/dashboard/quick_stats

**Description:**  
Returns quick overview statistics.

**Example JSON Response:**
```json
{
    "study_streak_days": 4,
}
```
### GET /api/study_activities
### GET /api/study_activities/:id

Returns the details of a single study activity, as identified by its ID.

**Example JSON Response:**

```json
{
    "id": 1,
    "name": "Vocabulary Quiz",
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "description": "Quiz on vocabulary words"
}
```

---


### GET /api/study_activities/:id/study_sessions
**Description:**  
Fetches all study sessions that are associated with the specified study activity.

**Example JSON Response:**

```json
{
  "items": [
    {
      "id": 5,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Fruits",
      "start_time": "2023-10-01T11:00:00Z",
      "end_time": "2023-10-01T11:30:00Z",
      "review_item_count": 20
    }
  ],
  "pagination": {
    "total_pages": 2,
    "current_page": 1,
    "per_page": 10,
    "total_items": 20
  }
}
```

---

### POST /api/study_activities
Creates a new study activity.

#### Request Params
- group_id integer
- study_activity_id integer

#### Request JSON Payload

```json
{
    "id": 1,
    "group_id": 123,
}
```

#### Response JSON

```json
{
  "study_activity": {
    "id": 3,
    "group_id": 2,
    "study_activity_id": 101,
    "created_at": "2023-10-03T09:00:00Z"
  },
  "message": "Study activity created successfully."
}
```
### GET /api/words

Retrieves a list of all vocabulary words.
Pagination is supported (20 words per page)

**Example Response:**

```json
{
  "items": [
    {
      "id": 1,
      "romanian": "măr",
      "english": "apple",
      "pronunciation": "mur",
      "parts": ["noun"]
    }
  ],
  "pagination": {
    "total_pages": 2,
    "current_page": 1,
    "per_page": 10,
    "total_items": 20
  }
}
```
### GET /api/words/:id

**Example JSON Response:**


```json
{
    "id": 1,
    "romanian": "măr",
    "english": "apple",
    "pronunciation": "mur",
    "parts": ["noun"],
    "stats": {
        "correct_count": 7,
        "wrong_count": 3
    },
    "groups": [
        {
            "id": 1,
            "name": "Fruits"
        }
    ]
}
```

### GET /api/groups


**Description:**  
Lists all thematic groups of words.

**Example Response:**

```json
{
  "items": [
    {
      "id": 1,
      "name": "Fruits",
      "words_count": 10
    }
  ],
  "pagination": {
    "total_pages": 2,
    "current_page": 1,
    "per_page": 10,
    "total_items": 20
  }
}
```
### GET /api/groups/:id
**Description:**  
Returns details for a single group identified by its ID.

**Example Response:**

```json
{
    "id": 1,
    "name": "Fruits",
    "stats": {
        "total_word_count": 10,
    }
}
```

### GET /api/groups/:id/words
**Description:**  
Retrieves all vocabulary words associated with a specific group.

**Example Response:**

```json
{
    "items": [
      {
        "romanian": "măr",
        "english": "apple",
        "pronunciation": "mur",
        "correct_count": 7,
        "wrong_count": 3,
      }
    ],
    "pagination": {
        "total_pages": 2,
        "current_page": 1,
        "per_page": 10,
        "total_items": 20
    }

}
```

### GET /api/groups/:id/study_sessions

**Description:**  
Returns the study sessions logged for a given group.

**Example Response:**

```json
{
    "items": [
      {
        "id": 12,
        "activity_name": "Vocabulary Quiz",
        "group_name": "Fruits",
        "start_time": "2023-10-02T14:00:00Z",
        "end_time": "2023-10-02T14:30:00Z",
        "review_item_count": 15,
      } 
    ],
    "pagination": {
        "total_pages": 2,
        "current_page": 1,
        "per_page": 10,
        "total_items": 20
    }
}
```

### GET /api/study_sessions
Description:
Retrieves a list of all study sessions, including their basic statistics.
Example Response:

```json
{
  "items": [
    {
      "id": 15,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Fruits",
      "start_time": "2023-10-05T16:30:00Z",
      "end_time": "2023-10-05T16:45:00Z",
      "review_item_count": 20,
    }
  ],
  "pagination": {
    "total_pages": 2,
    "current_page": 1,
    "per_page": 10,
    "total_items": 20
  }
}
```

### GET /api/study_sessions/:id
**Description:**
Returns detailed information about a specific study session, identified by its ID.
**Example JSON Response:**

```json
{
    "id": 15,
    "activity_name": "Vocabulary Quiz",
    "group_name": "Fruits",
    "start_time": "2023-10-05T16:30:00Z",
    "end_time": "2023-10-05T16:45:00Z",
    "review_item_count": 20,
}
```

### GET /api/study_sessions/:id/words
Description:
Retrieves all words that were reviewed in a specific study session, including their review results.
Example Response:

```json
{
  "items": [
    {
      "id": 15,
      "activity_name": "Vocabulary Quiz",
      "words": [
      {
        "romanian": "carte",
        "english": "book",
        "pronunciation": "car-te",
        "parts": ["noun"],
        "correct_count": 10,
        "wrong_count": 5
      }
    ],
    "pagination": {
        "total_pages": 2,
        "current_page": 1,
        "per_page": 10,
        "total_items": 20
    }
  }
} 
```

### POST /api/reset_history

**Description:**  
Resets all study history (e.g., deletes or archives study sessions and review items). This is a destructive operation that resets progress data.

**Example JSON Request:**

```json
{
  "success": true,
  "message": "Study history has been reset."
}
```

---

### POST /api/full_reset

**Description:**  
Performs a full reset of the system state including words, groups, study sessions, and study activities. Use with caution!

**Example JSON Request:**

```json
{
  "success": true,
  "message": "Full system reset completed."
}
```

### POST /api/study_sessions/:id/words/:word_id/review

**Description:**  
Records the result of a word review for a specific study session.  
**Request Params**  
- `id` (study_session_id) integer
- `word_id` integer 
- `correct` boolean

**Example Request Payload:**

```json
{
  "correct": true
}
```

**Example Response:**

```json
{
    "success": true,
    "word_id": 1,
    "study_session_id": 12,
    "correct": true,
    "created_at": "2023-10-03T16:00:00Z"
}
```

## Scripts (Tasks)

Invoke is the task runner for Python
### Initialize the database
This task will initialize the sqlite database called 'words.db'.

###  Migrate the database
This task will run a series of migrations sql files on the database.

Migrations live in the `migration` folder.
THe migration files will be run in order of their file name.
The file names should look like this:

```sql
001_init.sql
002_create_words_table.sql
```

###  Seed the database
This task will import JSON files and transform them into target data into the database.

All seed files live in the `seeds` folder
All seed files should be loaded.

In our task we should have a DSL to specify each seed files and its expected group word name.

```json
{
    "id": 1,
    "romanian": "măr",
    "english": "apple",
    "pronunciation": "mur",
},
```
