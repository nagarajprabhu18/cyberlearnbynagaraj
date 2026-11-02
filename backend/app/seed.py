from sqlalchemy import select

from app.db import SessionLocal
from app.models import Category, Course, Lesson, Role

CATALOG = [
    ("Networking & CCNA", "networking-ccna", "Network Fundamentals", "Learn how devices communicate across local networks.", [
        ("How data moves across a network", "A network connects devices so they can exchange data. Switches forward traffic within a local network, while routers move traffic between networks. This course uses diagrams and simulated scenarios only.", 8),
        ("The OSI model", "The OSI model is a seven-layer reference for discussing network functions: physical, data link, network, transport, session, presentation, and application. Use the layer names to organize troubleshooting observations.", 10),
        ("IPv4 addresses and subnets", "An IPv4 address identifies an interface. A prefix length describes how many leading bits identify the network. Practice calculating ranges with the platform's simulated subnet exercises; no network scanning is required.", 12),
    ]),
    ("Linux & Kali Linux", "linux-kali", "Linux Command Line Essentials", "Build confidence with everyday Linux commands and permissions.", [
        ("Navigating files safely", "Use pwd to print the current directory, ls to inspect files, and cd to change directories. Begin in a disposable local practice folder. Avoid running unfamiliar scripts with elevated privileges.", 7),
        ("Understanding file permissions", "Linux permissions describe read, write, and execute rights for the owner, group, and others. Use ls -l to inspect permissions in your own practice environment.", 9),
    ]),
    ("Cybersecurity", "cybersecurity", "Defensive Security Foundations", "Learn core principles for protecting systems and responding to events.", [
        ("The CIA triad", "Confidentiality limits access to authorized people, integrity protects accuracy, and availability keeps services usable. Defensive decisions often balance all three.", 6),
        ("Reading a security event timeline", "A timeline organizes recorded events by time, source, and observed action. In this simulated lesson, preserve relevant context, record uncertainty, and follow your organization's response process.", 8),
    ]),
    ("Python Programming", "python-programming", "Python for Helpful Automation", "Start with Python basics and build safe local productivity scripts.", [
        ("Values and variables", "Python variables give readable names to values. Start with strings, integers, and booleans, then use print() to inspect results in a local interpreter.", 8),
    ]),
    ("Ethical Hacking Education", "ethical-hacking", "Authorized Security Testing Principles", "Understand permission, scope, evidence, and responsible reporting.", [
        ("Permission and scope come first", "Security testing requires explicit written authorization and a defined scope. This learning path uses simulated targets or isolated local labs only. Never test systems you do not own or have permission to assess.", 7),
    ]),
]


def seed():
    with SessionLocal.begin() as db:
        for role_name in ("student", "admin"):
            if not db.scalar(select(Role).where(Role.name == role_name)):
                db.add(Role(name=role_name))
        for name, slug, title, summary, lessons in CATALOG:
            category = db.scalar(select(Category).where(Category.slug == slug))
            if category is None:
                category = Category(name=name, slug=slug)
                db.add(category)
                db.flush()
            course = db.scalar(select(Course).where(Course.slug == slug))
            if course is None:
                course = Course(category_id=category.id, title=title, slug=slug, summary=summary,
                                difficulty="beginner", duration_minutes=sum(item[2] for item in lessons), is_published=True)
                db.add(course)
                db.flush()
                for position, (lesson_title, content, duration) in enumerate(lessons, 1):
                    db.add(Lesson(course_id=course.id, title=lesson_title, content=content,
                                  duration_minutes=duration, position=position))


if __name__ == "__main__":
    seed()
