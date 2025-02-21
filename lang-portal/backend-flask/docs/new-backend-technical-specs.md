

# Backend Server Technical Specifications

## Business Goal
A language learning school wants to build a prototype learning portal that will serve as:
- An inventory of possible vocabulary that can be learned.
- A Learning Record Store (LRS) that records correct and incorrect practice attempts.
- A unified launchpad to start different learning apps.

## Technical Requirements
- **Language & Framework:** Python with Flask  
- **Database:** SQLite3 (database file: `words.db` in the project root)
- **API Format:** JSON-only responses  
- **Security:**  
  - JWT-based authentication with a refresh token mechanism  
  - CSRF protection and rate limiting  
- **User Model:** Initially single-user, but endpoints support authentication for future expansion.
- **Development Tools:** Utilize AI coding assistants (Cursor, Windsurf Codeium, GitHub Copilot, Amazon Q Developer, Google Code Assist)

## Database Schema

### Database File
- **File:** `words.db`

### Tables

#### `words`
Stores individual vocabulary words.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `romanian` TEXT NOT NULL
- `english` TEXT NOT NULL
- `pronunciation` TEXT
- `part_of_speech` TEXT NOT NULL
- `parts` JSON NOT NULL
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
- `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP

#### `groups`
Stores thematic collections of words.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `name` TEXT NOT NULL
- `description` TEXT
- `word_count` INTEGER DEFAULT 0
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
- `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP

#### `words_groups`
Join table for the many-to-many relationship between words and groups.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `word_id` INTEGER NOT NULL  
- `group_id` INTEGER NOT NULL  
- FOREIGN KEY(`word_id`) REFERENCES `words`(`id`)
- FOREIGN KEY(`group_id`) REFERENCES `groups`(`id`)

#### `study_sessions`
Records individual study sessions.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `activity_id` TEXT NOT NULL  
- `group_id` INTEGER  
- `start_time` DATETIME DEFAULT CURRENT_TIMESTAMP
- `end_time` DATETIME  
- `score` REAL DEFAULT 0  
- FOREIGN KEY(`group_id`) REFERENCES `groups`(`id`)

#### `study_activities`
Stores details about each learning activity.
- `id` TEXT PRIMARY KEY  
- `type` TEXT NOT NULL CHECK(`type` IN ('vocabulary', 'reading', 'grammar'))
- `title` TEXT NOT NULL
- `description` TEXT
- `thumbnail_url` TEXT
- `progress` REAL DEFAULT 0
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
- `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP

#### `word_review_items`
Tracks review attempts for words within study sessions.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `word_id` INTEGER NOT NULL  
- `session_id` INTEGER NOT NULL  
- `correct` BOOLEAN NOT NULL
- `user_answer` TEXT  
- `correct_answer` TEXT  
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP  
- FOREIGN KEY(`word_id`) REFERENCES `words`(`id`)
- FOREIGN KEY(`session_id`) REFERENCES `study_sessions`(`id`)

## API Endpoints

### Authentication

#### POST /api/auth/login
Logs in a user.
- **Request:**
  ```json
  { "username": "user", "password": "pass" }
  ```
- **Response:**
  ```json
  { "access_token": "JWT_TOKEN", "refresh_token": "JWT_REFRESH_TOKEN" }
  ```

#### POST /api/auth/refresh
Refreshes the access token.
- **Request:**
  ```json
  { "refresh_token": "JWT_REFRESH_TOKEN" }
  ```
- **Response:**
  ```json
  { "access_token": "NEW_JWT_TOKEN" }
  ```

---

### Dashboard

#### GET /api/dashboard
Returns an overview of the dashboard.
- **Response Example:**
  ```json
  {
    "lastSession": {
      "date": "2023-10-05T16:30:00Z",
      "score": 85,
      "duration": 15,
      "activity": "Vocabulary Quiz"
    },
    "progress": {
      "totalWordsLearned": 120,
      "completionRate": 50,
      "streak": 5
    },
    "stats": {
      "totalWords": 240,
      "totalGroups": 10,
      "completedSessions": 30
    }
  }
  ```

---

### Word Groups

#### GET /api/groups
Retrieve all word groups.
- **Query Params:**  
  - `page`: number (default 1)  
  - `limit`: number (default 10)
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "name": "Fruits",
      "description": "Common fruits in Romanian",
      "wordCount": 15,
      "createdAt": "2023-10-01T10:00:00Z",
      "updatedAt": "2023-10-01T10:00:00Z"
    }
  ]
  ```

#### POST /api/groups
Create a new word group.
- **Request Body:**
  ```json
  {
    "name": "New Group",
    "description": "Description of the group"
  }
  ```
- **Response:** Newly created group object.

#### PUT /api/groups/:id
Update an existing group.
- **Request Body:**
  ```json
  {
    "name": "Updated Group Name",
    "description": "Updated description"
  }
  ```
- **Response:** Updated group object.

#### DELETE /api/groups/:id
Delete a group.
- **Response Example:**
  ```json
  {
    "success": true,
    "message": "Group deleted successfully."
  }
  ```

#### GET /api/groups/:id/words
Retrieve all words in a specific group.
- **Query Params:**  
  - `page`: number  
  - `limit`: number
- **Response Example:**
  ```json
  {
    "words": [
      {
        "id": 1,
        "romanian": "măr",
        "english": "apple",
        "pronunciation": "mur",
        "partOfSpeech": "noun",
        "parts": ["noun"],
        "stats": {
          "correctCount": 7,
          "wrongCount": 3
        }
      }
    ],
    "total": 15
  }
  ```

---

### Word Collection

#### GET /api/words
Retrieve all words.
- **Query Params:**
  - `search` (optional)
  - `group` (optional)
  - `page`: number
  - `limit`: number
- **Response Example:**
  ```json
  {
    "words": [
      {
        "id": 1,
        "romanian": "măr",
        "english": "apple",
        "pronunciation": "mur",
        "partOfSpeech": "noun",
        "createdAt": "2023-10-01T10:00:00Z",
        "updatedAt": "2023-10-01T10:00:00Z",
        "groupIds": [1, 2]
      }
    ],
    "total": 240
  }
  ```

#### POST /api/words
Add a new word.
- **Request Body:**
  ```json
  {
    "romanian": "măr",
    "english": "apple",
    "pronunciation": "mur",
    "partOfSpeech": "noun",
    "groupIds": [1]
  }
  ```
- **Response:** Newly created word object.

#### PUT /api/words/:id
Update an existing word.
- **Request Body:** (any combination of)
  ```json
  {
    "romanian": "updated",
    "english": "updated",
    "pronunciation": "updated",
    "partOfSpeech": "noun",
    "groupIds": [1, 3]
  }
  ```
- **Response:** Updated word object.

#### DELETE /api/words/:id
Delete a word.
- **Response Example:**
  ```json
  {
    "success": true,
    "message": "Word deleted successfully."
  }
  ```

---

### Study Activities

#### GET /api/activities
Retrieve available study activities.
- **Response Example:**
  ```json
  [
    {
      "id": "act1",
      "type": "vocabulary",
      "title": "Vocabulary Quiz",
      "description": "Test your vocabulary skills",
      "thumbnail_url": "https://example.com/thumbnail.jpg",
      "progress": 70
    }
  ]
  ```

#### POST /api/activities/:id/start
Start an activity session.
- **Response Example:**
  ```json
  {
    "sessionId": "sess123",
    "questions": [ /* array of questions */ ]
  }
  ```

#### POST /api/activities/:id/submit
Submit activity results.
- **Request Body:**
  ```json
  {
    "sessionId": "sess123",
    "answers": [
      { "questionId": 1, "answer": "response" }
    ]
  }
  ```
- **Response Example:**
  ```json
  {
    "success": true,
    "score": 85,
    "message": "Results submitted successfully."
  }
  ```

---

### Learning Sessions

#### GET /api/study_sessions
Retrieve a paginated list of study sessions.
- **Query Params:**
  - `page`: number
  - `limit`: number
  - `sortBy`: one of `startTime`, `endTime`, `activityName`, `groupName`
  - `sortOrder`: `asc` or `desc`
- **Response Example:**
  ```json
  {
    "sessions": [
      {
        "id": "sess123",
        "activityName": "Vocabulary Quiz",
        "groupName": "Fruits",
        "startTime": "2023-10-05T16:30:00Z",
        "endTime": "2023-10-05T16:45:00Z",
        "reviewItemsCount": 20,
        "score": 85
      }
    ],
    "total": 30,
    "currentPage": 1,
    "totalPages": 3
  }
  ```

#### GET /api/study_sessions/:id
Retrieve detailed information about a specific study session.
- **Response Example:**
  ```json
  {
    "id": "sess123",
    "activityName": "Vocabulary Quiz",
    "groupName": "Fruits",
    "startTime": "2023-10-05T16:30:00Z",
    "endTime": "2023-10-05T16:45:00Z",
    "score": 85,
    "details": {
      "correctAnswers": 15,
      "totalQuestions": 20,
      "timeSpent": 15,
      "reviewItems": [
        {
          "id": 1,
          "word": "măr",
          "correct": true,
          "userAnswer": "măr",
          "correctAnswer": "măr"
        }
      ]
    }
  }
  ```

---

### Word Review

#### POST /api/study_sessions/:session_id/words/:word_id/review
Record the result of a word review during a study session.
- **Request Body:**
  ```json
  {
    "correct": true,
    "userAnswer": "măr",
    "correctAnswer": "măr"
  }
  ```
- **Response Example:**
  ```json
  {
    "success": true,
    "wordId": 1,
    "sessionId": "sess123",
    "correct": true,
    "createdAt": "2023-10-05T16:50:00Z"
  }
  ```

---

### Reset Endpoints

#### POST /api/reset_history
Reset all study history (e.g., delete or archive study sessions and review items).
- **Response Example:**
  ```json
  {
    "success": true,
    "message": "Study history has been reset."
  }
  ```

#### POST /api/full_reset
Perform a full system reset (clear words, groups, sessions, activities, and review items).
- **Response Example:**
  ```json
  {
    "success": true,
    "message": "Full system reset completed."
  }
  ```

---

### Footer

#### GET /api/footer
Retrieve dynamic footer content.
- **Response Example:**
  ```json
  {
    "links": [
      { "href": "/terms", "label": "Terms & Conditions" },
      { "href": "/privacy", "label": "Privacy Policy" },
      { "href": "/support", "label": "Help & Support" },
      { "href": "/feedback", "label": "Feedback" },
      { "href": "/about", "label": "About" }
    ],
    "copyright": "© 2025 Romanian Language School",
    "socialLinks": [
      {
        "platform": "Twitter",
        "url": "https://twitter.com/romanian_school",
        "icon": "twitter-icon-url"
      }
    ]
  }
  ```

---

## Error Handling

All error responses should follow this structure:
```json
{
  "code": "ERROR_CODE",
  "message": "User-friendly error message.",
  "details": { "field": "error details if applicable" }
}
```

---

## Scripts (Tasks)

Use Invoke as the task runner for the following tasks:

### Initialize the Database
Creates the `words.db` SQLite database in the project root.

### Migrate the Database
Run SQL migration files from the `migrations/` folder (e.g., `001_init.sql`, `002_create_tables.sql`).

### Seed the Database
Load JSON seed files from the `seeds/` folder to populate initial data. Each seed file follows a DSL specifying seed data and associated groups.  
Example seed entry:
```json
{
  "id": 1,
  "romanian": "măr",
  "english": "apple",
  "pronunciation": "mur",
  "partOfSpeech": "noun"
}
```