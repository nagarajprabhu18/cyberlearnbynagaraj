from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.limits import limiter
from app.models import Course, Enrollment, Lesson, LessonProgress, Role, User
from app.schemas import CourseOut, LoginIn, RegisterIn, TokenOut, UserOut
from app.security import decode_access_token, hash_password, make_access_token, verify_password

router = APIRouter(prefix="/api/v1")
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    user = db.get(User, decode_access_token(token))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


async def admin_user(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Administrator access required")
    return user


@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, payload: RegisterIn, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User.id).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Unable to create account with those details")
    student_role = db.scalar(select(Role).where(Role.name == "student"))
    if student_role is None:
        student_role = Role(name="student")
        db.add(student_role)
        db.flush()
    user = User(email=email, display_name=payload.display_name.strip(), password_hash=hash_password(payload.password), roles=[student_role])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=TokenOut)
@limiter.limit("5/minute")
async def login(request: Request, payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenOut(access_token=make_access_token(user.id))


@router.get("/auth/me", response_model=UserOut)
async def me(user: User = Depends(current_user)):
    return user


@router.get("/courses", response_model=list[CourseOut])
async def list_courses(q: str | None = Query(default=None, max_length=100), difficulty: str | None = None,
                 limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0), db: Session = Depends(get_db)):
    stmt = select(Course).options(joinedload(Course.category), joinedload(Course.lessons)).where(Course.is_published.is_(True))
    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(or_(Course.title.ilike(pattern), Course.summary.ilike(pattern)))
    if difficulty:
        stmt = stmt.where(Course.difficulty == difficulty.lower())
    courses = db.scalars(stmt.order_by(Course.id).limit(limit).offset(offset)).unique().all()
    return [CourseOut(id=c.id, title=c.title, slug=c.slug, summary=c.summary, difficulty=c.difficulty,
                      duration_minutes=c.duration_minutes, category=c.category.name, lessons=c.lessons) for c in courses]


@router.post("/courses/{course_id}/enroll", status_code=status.HTTP_201_CREATED)
async def enroll(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    course = db.scalar(select(Course).where(Course.id == course_id, Course.is_published.is_(True)))
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrollment = db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course.id))
    if not enrollment:
        db.add(Enrollment(user_id=user.id, course_id=course.id))
        db.commit()
    return {"course_id": course.id, "enrolled": True}


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(lesson_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    enrolled = db.scalar(select(Enrollment.id).where(Enrollment.user_id == user.id, Enrollment.course_id == lesson.course_id))
    if not enrolled:
        raise HTTPException(status_code=403, detail="Enroll in this course to track lesson progress")
    progress = db.scalar(select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id))
    if progress is None:
        db.add(LessonProgress(user_id=user.id, lesson_id=lesson.id, completed=True))
    else:
        progress.completed = True
    db.commit()
    return {"lesson_id": lesson.id, "completed": True}


@router.get("/dashboard")
async def dashboard(user: User = Depends(current_user), db: Session = Depends(get_db)):
    enrolled_count = db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.user_id == user.id)) or 0
    completed_count = db.scalar(select(func.count()).select_from(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.completed.is_(True))) or 0
    return {"enrolled_courses": enrolled_count, "completed_lessons": completed_count}


@router.get("/admin/overview")
async def admin_overview(_admin: User = Depends(admin_user), db: Session = Depends(get_db)):
    return {"registered_users": db.scalar(select(func.count()).select_from(User)) or 0,
            "published_courses": db.scalar(select(func.count()).select_from(Course).where(Course.is_published.is_(True))) or 0}
