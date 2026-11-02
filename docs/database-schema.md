# Database schema plan

The SQLAlchemy model layer will implement these normalized entities and constraints. IDs are UUIDs, timestamps are UTC, and content records use `created_at`/`updated_at`.

| Table | Key relationships and constraints |
|---|---|
| users | Unique normalized email, password hash, verified/active flags |
| roles | Unique role name; seed `student` and `admin` |
| user_roles | Unique `(user_id, role_id)` |
| categories | Unique slug, publication metadata |
| courses | Category FK, unique slug, difficulty/duration/published fields |
| lessons | Course FK, unique `(course_id, position)`, safe content and duration |
| enrollments | Unique `(user_id, course_id)`, enrolled/completed timestamps |
| lesson_progress | Unique `(user_id, lesson_id)`, completion and last position |
| quizzes | Optional course/lesson FK, time limit and difficulty |
| questions | Quiz FK, prompt/type/difficulty/position |
| question_options | Question FK, option body and correctness (never returned before submission) |
| quiz_attempts | User/quiz FKs, score, start/submit timestamps |
| quiz_answers | Attempt/question FKs, selected option IDs and correctness snapshot |
| achievements | Unique code, criteria metadata |
| user_achievements | Unique `(user_id, achievement_id)`, earned timestamp |
| certificates | User/course FKs, unique public verification ID, issue timestamp |
| bookmarks | Unique `(user_id, lesson_id)` |
| notes | User/lesson FKs, indexed owner and lesson |
| notifications | User FK, read timestamp, bounded message and type |

Additional indexes target course publication/category, lesson course order, quiz question order, user activity chronology, and search slugs. Ownership checks are performed in queries and service methods. Deletions use deliberate cascade/restrict behavior; learner history is not silently removed when content is archived.
