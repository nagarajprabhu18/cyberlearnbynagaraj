import { useEffect, useState } from 'react';
import { ArrowRight, ArrowUpRight, BookOpen, Check, ChevronDown, CirclePlay, Code2, Compass, Menu, Network, Shield, Sparkles, Terminal, X, Zap } from 'lucide-react';

const tracks = [
  { icon: Network, tag: 'NETWORKING', title: 'Build your network foundation', text: 'Move from packets and protocols to confident network troubleshooting.', tone: 'cyan', lessons: '32 lessons' },
  { icon: Terminal, tag: 'LINUX & SYSTEMS', title: 'Get fluent in the terminal', text: 'Learn Linux administration, Bash, permissions, and defensive tooling.', tone: 'violet', lessons: '28 lessons' },
  { icon: Shield, tag: 'DEFENSIVE SECURITY', title: 'Think like a defender', text: 'Understand security fundamentals, monitoring, and incident response.', tone: 'blue', lessons: '24 lessons' },
];

const paths = ['Networking & CCNA', 'Linux & Kali Linux', 'Cybersecurity', 'Python Programming', 'Ethical Hacking Education'];
type Course = { id: number; title: string; slug: string; summary: string; difficulty: string; duration_minutes: number; category: string; lessons: { id: number; title: string; duration_minutes: number; position: number }[] };
const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [courses, setCourses] = useState<Course[]>([]);
  const [catalogState, setCatalogState] = useState<'loading' | 'ready' | 'error'>('loading');

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${apiUrl}/api/v1/courses`, { signal: controller.signal })
      .then((response) => { if (!response.ok) throw new Error('Course catalog request failed'); return response.json() as Promise<Course[]>; })
      .then((items) => { setCourses(items); setCatalogState('ready'); })
      .catch((error: unknown) => { if (error instanceof Error && error.name !== 'AbortError') setCatalogState('error'); });
    return () => controller.abort();
  }, []);
  return <main>
    <header className="topbar wrap">
      <a className="brand" href="#top" aria-label="CyberLearn home"><span className="brand-mark"><Shield size={19} /></span><span>cyber<span className="brand-light">learn</span></span></a>
      <nav className={menuOpen ? 'nav open' : 'nav'} aria-label="Main navigation">
        <a href="#paths" onClick={() => setMenuOpen(false)}>Learning paths</a><a href="#courses" onClick={() => setMenuOpen(false)}>Explore courses</a><a href="#about" onClick={() => setMenuOpen(false)}>About</a>
      </nav>
      <div className="nav-actions"><a className="button button-small" href="#paths">Start learning <ArrowRight size={15}/></a></div>
      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label={menuOpen ? 'Close menu' : 'Open menu'}>{menuOpen ? <X/> : <Menu/>}</button>
    </header>

    <section className="hero wrap" id="top">
      <div className="hero-copy"><div className="eyebrow"><span className="live-dot"/> A clearer path into cybersecurity</div>
        <h1>Build skills.<br/><span>Protect what matters.</span></h1>
        <p className="hero-lede">A practical place to learn networking, Linux, Python, and defensive security — one focused lesson at a time.</p>
        <div className="hero-actions"><a className="button" href="#paths">Explore learning paths <ArrowRight size={17}/></a><a className="text-link" href="#courses"><CirclePlay size={18}/> See how it works</a></div>
        <div className="social-proof"><div className="avatar-stack"><span>A</span><span>M</span><span>J</span><span>+</span></div><div><strong>Learn at your own pace</strong><small>Built for curious beginners and career switchers</small></div></div>
      </div>
      <div className="hero-visual" aria-label="Illustration of a protected network dashboard">
        <div className="visual-grid"/><div className="orbit orbit-one"/><div className="orbit orbit-two"/>
        <div className="shield-core"><Shield size={77} strokeWidth={1.2}/><span className="core-check"><Check size={19}/></span></div>
        <div className="float-card node-card"><span className="node-icon"><Network size={17}/></span><span><small>NETWORK STATUS</small><b>Secure connection</b></span><i/></div>
        <div className="float-card skill-card"><span className="skill-icon"><Code2 size={16}/></span><span><small>YOUR NEXT SKILL</small><b>Subnetting basics</b></span><ArrowUpRight size={15}/></div>
        <div className="visual-caption"><span><Sparkles size={15}/> Learn by doing</span><span>01 / 05</span></div>
      </div>
    </section>

    <section className="metrics wrap" aria-label="Platform highlights"><div><strong>5</strong><span>guided learning paths</span></div><div><strong>100%</strong><span>learn at your own pace</span></div><div><strong><span className="metric-icon"><Shield size={19}/></span></strong><span>safe, defensive practice</span></div><div className="metrics-note">Curiosity is your<br/><em>best security tool.</em></div></section>

    <section className="section wrap" id="paths"><div className="section-heading"><div><div className="eyebrow">A path for every next step</div><h2>Learn the skills that <span>move you forward.</span></h2></div><a className="text-link desktop-link" href="#courses">Browse all paths <ArrowRight size={16}/></a></div>
      <div className="track-grid">{tracks.map(({ icon: Icon, ...track }, i) => <article className={`track-card ${track.tone}`} key={track.tag}><div className="card-top"><span className="track-icon"><Icon size={20}/></span><span className="card-index">0{i + 1}</span></div><div className="track-tag">{track.tag}</div><h3>{track.title}</h3><p>{track.text}</p><div className="card-footer"><span><BookOpen size={14}/>{track.lessons}</span><a href="#courses" aria-label={`Explore ${track.title}`}><ArrowUpRight size={17}/></a></div></article>)}</div>
      <div className="path-strip"><div className="path-intro"><Compass size={19}/><span>Explore all learning paths</span></div><div className="path-list">{paths.map((path) => <a key={path} href="#courses">{path}<ArrowUpRight size={13}/></a>)}</div><ChevronDown className="path-chevron" size={18}/></div>
    </section>

    <section className="feature-band" id="about"><div className="wrap feature-inner"><div><div className="eyebrow">Made for real progress</div><h2>Less noise.<br/><span>More hands-on learning.</span></h2><p>Follow clear, structured lessons, practice in safe simulations, and see your progress add up. No prior experience needed.</p><a href="#join" className="text-link">Find your starting point <ArrowRight size={16}/></a></div><div className="feature-list"><div><span><BookOpen size={18}/></span><div><b>Short, focused lessons</b><small>Understand one useful idea at a time.</small></div><Check size={16}/></div><div><span><Zap size={18}/></span><div><b>Practice as you learn</b><small>Try concepts in isolated, guided exercises.</small></div><Check size={16}/></div><div><span><Shield size={18}/></span><div><b>Security with responsibility</b><small>Every lab is designed for safe, authorized learning.</small></div><Check size={16}/></div></div></div></section>

    <section className="section course-section wrap" id="courses"><div className="section-heading"><div><div className="eyebrow">Start somewhere. Keep going.</div><h2>Your next lesson is <span>closer than you think.</span></h2></div><a className="text-link desktop-link" href="#paths">All learning paths <ArrowRight size={16}/></a></div>
      {catalogState === 'loading' && <div className="course-empty" role="status"><div className="empty-icon"><BookOpen size={23}/></div><h3>Loading the course library</h3><p>Connecting to CyberLearn’s course catalog…</p></div>}
      {catalogState === 'error' && <div className="course-empty" role="alert"><div className="empty-icon"><BookOpen size={23}/></div><h3>Course library is unavailable</h3><p>Start the CyberLearn API and refresh this page to load published courses.</p></div>}
      {catalogState === 'ready' && courses.length === 0 && <div className="course-empty"><div className="empty-icon"><BookOpen size={23}/></div><h3>No published courses yet</h3><p>There are no courses available in the catalog at this time.</p></div>}
      {catalogState === 'ready' && courses.length > 0 && <div className="course-list">{courses.map((course) => <article className="course-item" key={course.id}><div><span className="course-category">{course.category}</span><h3>{course.title}</h3><p>{course.summary}</p></div><div className="course-meta"><span>{course.lessons.length} lessons</span><span>{course.duration_minutes} min</span><span>{course.difficulty}</span></div></article>)}</div>}
    </section>

    <section className="join-section wrap" id="join"><div className="join-glow"/><div><div className="eyebrow">Your next chapter starts here</div><h2>Learn something that<br/><span>makes a difference.</span></h2><p>Pick a learning path and take your first step at your own pace.</p></div><a className="button" href="#paths">Choose a learning path <ArrowRight size={16}/></a></section>

    <footer className="footer wrap"><a className="brand" href="#top"><span className="brand-mark"><Shield size={17}/></span><span>cyber<span className="brand-light">learn</span></span></a><span>Learn with purpose. Defend with confidence.</span><div><a href="#about">About</a><a href="#paths">Learning paths</a><a href="#paths">Get started</a></div><small>© 2026 CyberLearn. Educational content for authorized, defensive learning.</small></footer>
  </main>;
}

export default App;
