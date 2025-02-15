# Backend Technical Specifications

## Overview

The backend system is built using:
- Python with Flask framework
- SQLite3 database
- JSON-only responses
- Single user system (no auth required)

## Database Schema

### Core Tables

```sql
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    romanian TEXT NOT NULL,
    english TEXT NOT NULL,
    parts JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE words_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER,
    group_id INTEGER,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    study_activity_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);

CREATE TABLE word_review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER,
    study_session_id INTEGER,
    correct BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
);
```

## API Endpoints

### Dashboard

```typescript
// Get last study session
GET /api/dashboard/last_study_session
Response: {
    id: number
    activityName: string
    groupName: string
    date: string
    score: number
    duration: number
}

// Get study progress
GET /api/dashboard/study_progress
Response: {
    totalWordsLearned: number
    completionRate: number
    streak: number
}

// Get quick stats
GET /api/dashboard/quick_stats
Response: {
    totalWords: number
    totalGroups: number
    completedSessions: number
}
```

### Words Management

```typescript
// Get paginated words list
GET /api/words
Query params: {
    page?: number        // default: 1
    limit?: number       // default: 100
    search?: string
    group_id?: number
}
Response: {
    words: {
        id: number
        romanian: string
        english: string
        parts: {
            partOfSpeech: string
            pronunciation?: string
        }
    }[]
    total: number
}

// Get single word
GET /api/words/:id
Response: {
    id: number
    romanian: string
    english: string
    parts: {
        partOfSpeech: string
        pronunciation?: string
    }
    groupIds: number[]
}
```

### Groups Management

```typescript
// Get groups list
GET /api/groups
Query params: {
    page?: number    // default: 1
    limit?: number   // default: 100
}
Response: {
    groups: {
        id: number
        name: string
        description: string
        wordCount: number
    }[]
    total: number
}

// Get group details
GET /api/groups/:id
Response: {
    id: number
    name: string
    description: string
    wordCount: number
}

// Get words in group
GET /api/groups/:id/words
Response: {
    words: {
        id: number
        romanian: string
        english: string
        parts: object
    }[]
}

// Get group study sessions
GET /api/groups/:id/study_sessions
Response: {
    sessions: {
        id: number
        activityName: string
        created_at: string
        score: number
    }[]
}
```

### Study Activities

```typescript
// Get available activities
GET /api/study_activities
Response: {
    activities: {
        id: number
        type: string
        name: string
        description: string
    }[]
}

// Create study activity session
POST /api/study_activities
Body: {
    group_id: number
    study_activity_id: number
}
Response: {
    session_id: number
    words: {
        id: number
        romanian: string
        english: string
    }[]
}
```

### Study Sessions

```typescript
// Get sessions list
GET /api/study_sessions
Query params: {
    page?: number
    limit?: number
    sortBy?: string
    sortOrder?: 'asc' | 'desc'
}
Response: {
    sessions: {
        id: number
        activityName: string
        groupName: string
        startTime: string
        endTime: string
        reviewItemsCount: number
        score: number
    }[]
    total: number
    currentPage: number
    totalPages: number
}

// Get session details
GET /api/study_sessions/:id
Response: {
    id: number
    activityName: string
    groupName: string
    startTime: string
    endTime: string
    score: number
    details: {
        correctAnswers: number
        totalQuestions: number
        timeSpent: number
        reviewItems: {
            id: number
            word: string
            correct: boolean
            userAnswer: string
            correctAnswer: string
        }[]
    }
}

// Record word review
POST /api/study_sessions/:id/words/:word_id/review
Body: {
    correct: boolean
}
Response: {
    success: boolean
}
```

### System Management

```typescript
// Reset study history
POST /api/reset_history
Response: {
    success: boolean
}

// Full system reset
POST /api/full_reset
Response: {
    success: boolean
}
```

## Implementation Notes

1. Database Indexes
```sql
CREATE INDEX idx_words_romanian ON words(romanian);
CREATE INDEX idx_words_english ON words(english);
CREATE INDEX idx_word_review_items_session ON word_review_items(study_session_id);
CREATE INDEX idx_study_sessions_created ON study_sessions(created_at);
```

2. Response Format
```typescript
// Success Response
{
    status: 'success',
    data: object | array
}

// Error Response
{
    status: 'error',
    error: {
        code: string
        message: string
        details?: object
    }
}
```

3. Pagination
- Default page size: 100 items
- Page numbers start at 1
- Include total count and page info in responses

4. Performance Considerations
- Use JOIN operations for related data
- Index frequently queried fields
- Cache common dashboard queries
