import React, { useState, useEffect } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc, collection, onSnapshot, query, updateDoc, arrayUnion } from 'firebase/firestore';
import { 
  User, Clock, Award, CheckCircle, Play, Square, 
  Download, Trophy, MapPin, Calendar, Star, Zap,
  X, Send, ClipboardList, Loader2, Newspaper, ChevronRight, Heart, Home, Users, Globe,
  Mail, Instagram, MessageCircle, PlusCircle, AlertCircle, ExternalLink, Info, Share2, 
  Lock, Check, FileText, Medal, Search, ChevronDown, ChevronUp, LogIn, MessageCircle as MessageIcon
} from 'lucide-react';

// Конфигурация Firebase (подставляется средой исполнения)
const firebaseConfig = JSON.parse(__firebase_config);
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

const App = () => {
  const [lang, setLang] = useState('ru'); // 'ru', 'uz'
  const [view, setView] = useState('home');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Состояния для облачных данных
  const [news, setNews] = useState([]);
  const [events, setEvents] = useState([]);
  const [allVolunteers, setAllVolunteers] = useState([]);

  // UI Состояния
  const [selectedNews, setSelectedNews] = useState(null); 
  const [showEventInfo, setShowEventInfo] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeSession, setActiveSession] = useState(null);
  const [timer, setTimer] = useState(0);

  // Лимиты для списков (показывать только 3)
  const [showAllAchievements, setShowAllAchievements] = useState(false);
  const [showAllCertificates, setShowAllCertificates] = useState(false);
  const [showAllVolunteers, setShowAllVolunteers] = useState(false);

  const translations = {
    ru: {
      appName: "Olympic Volunteers",
      subtitle: "Независимое волонтерское движение",
      home: "Главная",
      news: "Новости",
      events: "Ивенты",
      volunteers: "Волонтеры",
      profile: "Профиль",
      welcome: "Добро пожаловать!",
      registerInBot: "Пожалуйста, сначала пройдите регистрацию в нашем боте!",
      enterApp: "Войти в кабинет",
      noEvents: "На данный момент активных мероприятий нет.",
      noVolunteers: "Список волонтеров пуст",
      whoWeAre: "Кто мы такие?",
      mission: "Мы — крупнейшее волонтерское движение. Наша миссия: обеспечить безупречную организацию мероприятий и продвигать олимпийские ценности.",
      ourFamily: "Наша семья",
      responsibility: "Зона ответственности",
      totalHours: "Всего часов",
      nextLevel: "До уровня",
      hoursLeft: "Осталось",
      achievements: "Достижения",
      certificates: "Мои сертификаты",
      searchPlaceholder: "Поиск волонтера...",
      findVolunteers: "Найти единомышленников",
      apply: "Подать заявку",
      checkIn: "Начать смену",
      checkOut: "Завершить смену",
      onPost: "На посту",
      verified: "Проверено ✓",
      readMore: "Подробнее",
      joinUs: "Присоединяйтесь к нам",
      send: "Отправить",
      showAll: "Показать все",
      hide: "Свернуть",
      loading: "Загрузка профиля...",
      ranks: {
        r1: "Зеленый Авокадик",
        r2: "Бодрый Авокадик",
        r3: "Авокадо-Профи",
        r4: "Мастер Авокадо",
        r5: "Золотой Авокадо"
      }
    },
    uz: {
      appName: "Olympic Volunteers",
      subtitle: "Mustaqil volontyorlar harakati",
      home: "Asosiy",
      news: "Yangiliklar",
      events: "Iventlar",
      volunteers: "Ko'ngillilar",
      profile: "Profil",
      welcome: "Xush kelibsiz!",
      registerInBot: "Iltimos, avval botda ro'yxatdan o'ting!",
      enterApp: "Kirish",
      noEvents: "Hozircha faol iventlar yo'q.",
      noVolunteers: "Ro'yxat bo'sh",
      whoWeAre: "Biz kimmiz?",
      mission: "Biz eng yirik ko'ngillilar harakatimiz. Tadbirlarni mukammal tashkil etish bizning asosiy vazifamizdir.",
      ourFamily: "Bizning oilamiz",
      responsibility: "Mas'uliyat",
      totalHours: "Jami soatlar",
      nextLevel: "Darajagacha",
      hoursLeft: "Qoldi",
      achievements: "Yutuqlar",
      certificates: "Sertifikatlarim",
      searchPlaceholder: "Qidiruv...",
      findVolunteers: "Maslakdoshlarni topish",
      apply: "Ariza berish",
      checkIn: "Boshlash",
      checkOut: "Tugatish",
      onPost: "Postda",
      verified: "Tasdiqlandi ✓",
      readMore: "Batafsil",
      joinUs: "Bizga qo'shiling",
      send: "Yuborish",
      showAll: "Hammasini ko'rsatish",
      hide: "Yopish",
      loading: "Profil yuklanmoqda...",
      ranks: {
        r1: "Yashil Avokadik",
        r2: "Chaqqon Avokadik",
        r3: "Avokado-Profi",
        r4: "Avokado Ustasi",
        r5: "Oltin Avokado"
      }
    }
  };

  const t = (key) => translations[lang]?.[key] || translations['ru'][key] || key;

  const family = [
    { 
      name: "Бегижонов Пахлавон Махмуд", 
      role: { ru: "Координатор IT и Аэропорта", uz: "IT va Aeroport kordinatori" }, 
      responsibility: { ru: "IT-департамент и логистика в аэропорту", uz: "IT-departamenti va aeroport logistikasi" },
      email: "pahlovon222@gmail.com",
      tg: "pahlavonmahmud222",
      ig: "pahlovonmahmud222",
      photo: "👨‍💻"
    }
  ];

  const ACHIEVEMENTS_GUIDE = [
    { id: 'a1', icon: '🥋', req: 10, title: { ru: 'Помощник Дзюдоиста', uz: 'Dzyudo yordamchisi' } },
    { id: 'a2', icon: '🏃', req: 20, title: { ru: 'Мастер Марафона', uz: 'Marafon ustasi' } },
    { id: 'a3', icon: '⚽', req: 15, title: { ru: 'Футбольный Гид', uz: 'Futbol gidi' } },
    { id: 'a4', icon: '💻', req: 30, title: { ru: 'IT Авокадо', uz: 'IT Avokado' } }
  ];

  // RULE 3 - Инициализация Firebase Auth
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
          await signInWithCustomToken(auth, __initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (err) { console.error("Firebase auth error:", err); }
    };
    initAuth();

    const unsubscribe = onAuthStateChanged(auth, async (fbUser) => {
      if (fbUser) {
        // RULE 1 - Путь к профилю пользователя
        const docRef = doc(db, 'artifacts', appId, 'users', fbUser.uid, 'profile', 'data');
        const docSnap = await getDoc(docRef);
        if (docSnap.exists()) {
          setUser({ uid: fbUser.uid, ...docSnap.data() });
        } else {
          setUser({ uid: fbUser.uid, unregistered: true });
        }
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  // RULE 2 - Загрузка данных из Firestore
  useEffect(() => {
    if (!auth.currentUser) return;
    
    const unsubNews = onSnapshot(collection(db, 'artifacts', appId, 'public', 'data', 'news'), (snap) => {
      setNews(snap.docs.map(d => ({ id: d.id, ...d.data() })));
    });
    const unsubEvents = onSnapshot(collection(db, 'artifacts', appId, 'public', 'data', 'events'), (snap) => {
      setEvents(snap.docs.map(d => ({ id: d.id, ...d.data() })));
    });
    const unsubVols = onSnapshot(collection(db, 'artifacts', appId, 'public', 'data', 'volunteers'), (snap) => {
      setAllVolunteers(snap.docs.map(d => ({ id: d.id, ...d.data() })));
    });

    return () => { unsubNews(); unsubEvents(); unsubVols(); };
  }, [auth.currentUser]);

  // Таймер рабочей смены
  useEffect(() => {
    let interval;
    if (activeSession) {
      interval = setInterval(() => setTimer(prev => prev + 1), 1000);
    } else {
      setTimer(0);
    }
    return () => clearInterval(interval);
  }, [activeSession]);

  const getRankData = (hours = 0) => {
    const ranks = translations[lang]?.ranks || translations['ru'].ranks;
    if (hours < 20) return { title: ranks.r1, min: 0, max: 20, color: "bg-green-400" };
    if (hours < 50) return { title: ranks.r2, min: 20, max: 50, color: "bg-[#7DFF00]" };
    if (hours < 150) return { title: ranks.r3, min: 50, max: 150, color: "bg-[#0081C8]" };
    if (hours < 300) return { title: ranks.r4, min: 150, max: 300, color: "bg-[#FF2B85]" };
    return { title: ranks.r5, min: 300, max: 1000, color: "bg-yellow-400" };
  };

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  if (loading) return (
    <div className="max-w-md mx-auto min-h-screen bg-black flex flex-col items-center justify-center gap-4">
      <Loader2 className="animate-spin text-[#7DFF00]" size={40} />
      <span className="text-white/50 font-black uppercase tracking-widest text-xs">{t('loading')}</span>
    </div>
  );

  // Экран-заглушка для незарегистрированных через бот пользователей
  if (user?.unregistered) {
    return (
      <div className="max-w-md mx-auto min-h-screen bg-black flex flex-col items-center justify-center p-8 text-center text-white">
        <div className="w-24 h-24 bg-[#7DFF00] rounded-[30px] flex items-center justify-center text-5xl mb-8 animate-bounce shadow-[0_0_50px_rgba(125,255,0,0.3)]">🥑</div>
        <h1 className="text-2xl font-black uppercase mb-4 italic tracking-tighter">Olympic Hub</h1>
        <p className="text-gray-400 font-bold mb-10 leading-relaxed text-sm uppercase tracking-widest">{t('registerInBot')}</p>
        <button className="w-full bg-[#7DFF00] text-black font-black py-5 rounded-2xl uppercase shadow-xl flex items-center justify-center gap-3 active:scale-95 transition-all">
          <MessageIcon size={20} /> Перейти в Бот
        </button>
      </div>
    );
  }

  const currentRank = getRankData(user?.totalHours || 0);

  return (
    <div className="max-w-md mx-auto min-h-screen pb-28 bg-gray-50 font-sans selection:bg-[#7DFF00]/30 relative text-left">
      {/* Шапка приложения */}
      <div className="bg-white px-8 py-6 flex justify-between items-center border-b-2 border-gray-100 sticky top-0 z-50">
        <div className="flex items-center gap-4">
           <div className="w-12 h-12 bg-black rounded-2xl flex items-center justify-center text-2xl shadow-lg border-b-4 border-[#7DFF00]">🥑</div>
           <div className="flex flex-col">
                <span className="font-black text-base leading-none tracking-tighter uppercase">Olympic</span>
                <span className="font-black text-[10px] leading-none text-[#0081C8] tracking-widest uppercase mt-1">Volunteers</span>
           </div>
        </div>
        <button 
          onClick={() => setLang(lang === 'ru' ? 'uz' : 'ru')} 
          className="text-[10px] font-black border-2 border-gray-100 px-3 py-1 rounded-lg uppercase bg-gray-50 active:bg-gray-200 transition-colors"
        >
          {lang}
        </button>
      </div>

      <div className="p-6">
        {/* Вкладка ГЛАВНАЯ */}
        {view === 'home' && (
          <div className="space-y-8 animate-in fade-in duration-500">
             <div className="bg-white rounded-[40px] p-8 shadow-sm border-2 border-gray-50">
               <h3 className="text-xl font-black text-gray-900 uppercase mb-4">{t('whoWeAre')}</h3>
               <p className="text-gray-600 font-bold text-sm leading-relaxed italic">{t('mission')}</p>
             </div>

             <div className="px-2">
                <h3 className="text-xl font-black text-gray-900 uppercase mb-6 ml-4 flex items-center gap-2">
                  <Heart className="text-[#FF2B85] fill-[#FF2B85]" size={18} /> {t('ourFamily')}
                </h3>
                {family.map((f, i) => (
                  <div key={i} className="bg-white p-6 rounded-[35px] border-2 border-gray-50 shadow-sm mb-4">
                    <div className="flex gap-4">
                        <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center text-3xl shrink-0">{f.photo}</div>
                        <div>
                            <h4 className="text-lg font-black text-gray-900 uppercase leading-none">{f.name}</h4>
                            <p className="text-[10px] text-blue-600 font-black uppercase mt-1 tracking-widest">{f.role[lang]}</p>
                            <p className="text-[11px] text-gray-400 font-bold mt-2 leading-tight">{f.responsibility[lang]}</p>
                        </div>
                    </div>
                    <div className="grid grid-cols-2 gap-2 mt-4">
                        <a href={`https://t.me/${f.tg}`} target="_blank" className="bg-sky-50 text-sky-600 text-[10px] font-black py-2 rounded-xl text-center uppercase active:scale-95 transition-all">Telegram</a>
                        <a href={`https://instagram.com/${f.ig}`} target="_blank" className="bg-pink-50 text-pink-600 text-[10px] font-black py-2 rounded-xl text-center uppercase active:scale-95 transition-all">Instagram</a>
                    </div>
                  </div>
                ))}
             </div>

             {/* Контакты сообщества */}
             <div className="px-2 pb-6">
                <div className="bg-black rounded-[40px] p-8 shadow-2xl relative overflow-hidden">
                    <h3 className="text-xl font-black text-[#7DFF00] uppercase mb-4 flex items-center gap-2 relative z-10">
                      <Share2 size={20} /> {t('joinUs')}
                    </h3>
                    <div className="space-y-3 relative z-10">
                        <a href="https://t.me/olympic_volunteers_uz" target="_blank" className="flex items-center justify-between bg-white/10 p-4 rounded-2xl group transition-all">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-[#0081C8] rounded-xl flex items-center justify-center text-white"><MessageIcon size={20} /></div>
                                <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Telegram</p><p className="text-xs font-bold text-white">@olympic_volunteers_uz</p></div>
                            </div>
                            <ChevronRight size={18} className="text-white/30" />
                        </a>
                        <a href="https://instagram.com/olympic_volunteers_uz_" target="_blank" className="flex items-center justify-between bg-white/10 p-4 rounded-2xl group transition-all">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-[#FF2B85] rounded-xl flex items-center justify-center text-white"><Instagram size={20} /></div>
                                <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Instagram</p><p className="text-xs font-bold text-white">@olympic_volunteers_uz_</p></div>
                            </div>
                            <ChevronRight size={18} className="text-white/30" />
                        </a>
                        <a href="mailto:olympicvolunteersuz@gmail.com" className="flex items-center justify-between bg-white/10 p-4 rounded-2xl group transition-all">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center text-white"><Mail size={20} /></div>
                                <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Email</p><p className="text-xs font-bold text-white">olympicvolunteersuz@gmail.com</p></div>
                            </div>
                            <ChevronRight size={18} className="text-white/30" />
                        </a>
                    </div>
                    <div className="absolute top-0 right-0 w-32 h-32 bg-[#7DFF00]/10 rounded-full blur-3xl -mr-10 -mt-10"></div>
                </div>
             </div>
          </div>
        )}

        {/* Вкладка НОВОСТИ */}
        {view === 'news' && (
           <div className="space-y-6 animate-in fade-in pb-10">
              <h2 className="text-3xl font-black text-gray-900 uppercase tracking-tighter px-2">{t('news')}</h2>
              {news.length === 0 ? (
                <div className="bg-white rounded-[40px] p-10 text-center border-2 border-dashed border-gray-100 text-gray-300 font-black uppercase text-xs tracking-widest">Нет новостей</div>
              ) : (
                news.map(n => (
                  <div key={n.id} className="bg-white rounded-[40px] overflow-hidden shadow-sm border-2 border-gray-50 active:scale-[0.98] transition-all">
                    <img src={n.image} className="w-full h-48 object-cover" />
                    <div className="p-6">
                       <h3 className="text-xl font-black text-gray-900 uppercase leading-tight">{n.title?.[lang]}</h3>
                       <p className="text-sm text-gray-500 mt-2 line-clamp-2 font-bold italic">{n.content?.[lang]}</p>
                       <button onClick={() => setSelectedNews(n)} className="mt-4 text-[#0081C8] font-black text-xs uppercase flex items-center gap-1">
                         {t('readMore')} <ChevronRight size={14}/>
                       </button>
                    </div>
                  </div>
                ))
              )}
           </div>
        )}

        {/* Вкладка ИВЕНТЫ */}
        {view === 'events' && (
           <div className="space-y-4 animate-in slide-in-from-bottom duration-500 pb-10">
              <h2 className="text-3xl font-black text-gray-900 uppercase tracking-tighter px-2">{t('events')}</h2>
              {events.length === 0 ? (
                <div className="bg-white rounded-[40px] p-12 text-center border-2 border-dashed border-gray-100">
                  <Calendar size={48} className="mx-auto text-gray-200 mb-4" />
                  <p className="text-gray-400 font-bold uppercase text-xs tracking-widest leading-relaxed">{t('noEvents')}</p>
                </div>
              ) : (
                events.map(event => (
                  <div key={event.id} className="bg-white rounded-[35px] p-6 shadow-sm border-2 border-gray-50 relative overflow-hidden active:border-[#7DFF00] transition-colors">
                    <div className="flex gap-4">
                      <div className={`w-14 h-14 ${event.color || 'bg-blue-500'} rounded-[22px] flex items-center justify-center text-white shadow-xl`}>
                         <Medal size={24} />
                      </div>
                      <div className="flex-1">
                         <h4 className="font-black text-gray-900 text-lg leading-tight uppercase">{event.title?.[lang]}</h4>
                         <p className="text-[11px] text-gray-400 font-bold uppercase mt-1 flex items-center gap-1 tracking-tighter">
                            <MapPin size={12} className="text-[#FF2B85]" /> {event.location}
                         </p>
                      </div>
                      <button onClick={() => setShowEventInfo(event)} className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center text-gray-400 active:text-blue-600 transition-colors">
                        <Info size={20} />
                      </button>
                    </div>
                  </div>
                ))
              )}
           </div>
        )}

        {/* Вкладка ВОЛОНТЕРЫ */}
        {view === 'volunteers' && (
          <div className="space-y-6 animate-in fade-in pb-10">
            <h2 className="text-3xl font-black text-gray-900 uppercase tracking-tighter px-2">{t('volunteers')}</h2>
            <div className="px-2 relative">
              <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
              <input 
                type="text" 
                placeholder={t('searchPlaceholder')}
                className="w-full bg-white border-2 border-gray-100 rounded-3xl py-4 pl-12 pr-6 text-sm font-bold shadow-sm outline-none focus:border-[#7DFF00] transition-all"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="space-y-4 px-2">
              {allVolunteers.filter(v => v.name?.toLowerCase().includes(searchTerm.toLowerCase())).slice(0, showAllVolunteers ? undefined : 3).map(v => (
                <div key={v.id} className="bg-white rounded-[35px] p-5 shadow-sm border-2 border-gray-50 flex items-center justify-between active:scale-[0.98] transition-all">
                   <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-100 rounded-2xl flex items-center justify-center text-2xl border-2 border-gray-50 shadow-sm">🥑</div>
                      <div>
                         <p className="font-black text-gray-900 text-sm uppercase leading-none tracking-tighter">{v.name}</p>
                         <p className="text-[10px] text-blue-500 font-black uppercase mt-1 italic tracking-widest">{getRankData(v.hours).title}</p>
                      </div>
                   </div>
                   <div className="text-right">
                      <p className="text-[8px] font-black text-gray-300 uppercase tracking-widest mb-1">Часов</p>
                      <p className="text-lg font-black italic text-gray-900 leading-none">{v.hours?.toFixed(1) || '0.0'}</p>
                   </div>
                </div>
              ))}
              {allVolunteers.length > 3 && (
                <button 
                  onClick={() => setShowAllVolunteers(!showAllVolunteers)} 
                  className="text-gray-400 font-black text-[10px] uppercase w-full py-3 flex items-center justify-center gap-2 hover:text-black transition-colors"
                >
                  {showAllVolunteers ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
                  {showAllVolunteers ? t('hide') : t('showAll')}
                </button>
              )}
            </div>
          </div>
        )}

        {/* Вкладка ПРОФИЛЬ */}
        {view === 'profile' && user && (
          <div className="space-y-6 animate-in fade-in pb-10">
             <div className="bg-[#1a1a1a] rounded-[45px] p-8 shadow-2xl relative overflow-hidden border-b-8 border-[#7DFF00]">
                <div className="relative z-10 flex flex-col items-center text-center">
                    <div className="w-28 h-28 bg-white rounded-[40px] flex items-center justify-center text-5xl mb-5 shadow-2xl border-4 border-[#7DFF00]">{user.avatar || '🥑'}</div>
                    <h2 className="text-3xl font-black text-white uppercase tracking-tighter leading-none">{user.name}</h2>
                    <div className={`mt-4 px-4 py-1.5 rounded-full text-black text-[11px] font-black uppercase tracking-widest ${currentRank.color}`}>
                        {currentRank.title}
                    </div>

                    <div className="w-full mt-8 space-y-2">
                       <div className="flex justify-between items-center px-1">
                           <span className="text-[9px] font-black text-gray-500 uppercase tracking-widest">{t('nextLevel')}</span>
                           <span className="text-[9px] font-black text-[#7DFF00] uppercase tracking-widest">
                               {t('hoursLeft')}: {(currentRank.max - (user.totalHours || 0)).toFixed(1)} h
                           </span>
                       </div>
                       <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden border border-white/5">
                           <div 
                             className={`h-full transition-all duration-1000 ${currentRank.color}`} 
                             style={{ width: `${Math.min(100, (((user.totalHours || 0) - currentRank.min) / (currentRank.max - currentRank.min)) * 100)}%` }}
                           ></div>
                       </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 w-full mt-8">
                       <div className="bg-white/5 backdrop-blur-md p-5 rounded-3xl border border-white/10 text-left">
                           <p className="text-[10px] font-black text-gray-500 uppercase tracking-widest">{t('totalHours')}</p>
                           <p className="text-3xl font-black text-[#7DFF00] italic mt-1">{user.totalHours?.toFixed(1) || '0.0'}</p>
                       </div>
                       <div className="bg-white/5 backdrop-blur-md p-5 rounded-3xl border border-white/10 text-left">
                           <p className="text-[10px] font-black text-gray-500 uppercase tracking-widest">ID</p>
                           <p className="text-lg font-black text-white mt-1 italic tracking-widest">{user.id || '000000'}</p>
                       </div>
                    </div>
                </div>
                <div className="absolute top-0 right-0 w-32 h-32 bg-[#7DFF00]/10 rounded-full blur-3xl -mr-10 -mt-10"></div>
             </div>

             {/* Блок ДОСТИЖЕНИЙ (лимит 3) */}
             <div className="bg-white rounded-[40px] p-8 shadow-sm border-2 border-gray-50">
               <h3 className="text-xl font-black text-gray-900 uppercase mb-6 flex items-center gap-2">
                 <Medal className="text-[#FF2B85]"/> {t('achievements')}
               </h3>
               <div className="grid grid-cols-3 gap-4 mb-6">
                 {ACHIEVEMENTS_GUIDE.slice(0, showAllAchievements ? undefined : 3).map(a => {
                    const isEarned = (user.totalHours || 0) >= a.req;
                    return (
                      <div key={a.id} className={`aspect-square rounded-[30px] flex flex-col items-center justify-center gap-2 border-2 transition-all ${isEarned ? 'bg-green-50 border-[#7DFF00] shadow-sm' : 'bg-gray-50 border-gray-100 grayscale opacity-40'}`}>
                        <span className="text-3xl">{a.icon}</span>
                        <p className="text-[8px] font-black uppercase text-center px-1 leading-tight tracking-tighter">{a.title[lang]}</p>
                      </div>
                    );
                 })}
               </div>
               {ACHIEVEMENTS_GUIDE.length > 3 && (
                 <button onClick={() => setShowAllAchievements(!showAllAchievements)} className="text-gray-400 font-black text-[10px] uppercase w-full pt-4 flex items-center justify-center gap-1">
                   {showAllAchievements ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
                   {showAllAchievements ? t('hide') : t('showAll')}
                 </button>
               )}
             </div>

             {/* Блок СЕРТИФИКАТОВ (лимит 3) */}
             <div className="bg-white rounded-[40px] p-8 shadow-sm border-2 border-gray-50">
               <h3 className="text-xl font-black text-gray-900 uppercase mb-6 flex items-center gap-2">
                 <FileText className="text-[#0081C8]"/> {t('certificates')}
               </h3>
               <div className="space-y-4 mb-6 text-left">
                  {(user.certificates || []).slice(0, showAllCertificates ? undefined : 3).map((cert, idx) => (
                    <div key={idx} className="flex justify-between items-center p-4 bg-gray-50 rounded-2xl border border-gray-100 active:scale-[0.98] transition-all">
                       <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center text-xl"><FileText size={20}/></div>
                          <div>
                            <p className="text-xs font-black text-gray-900 uppercase leading-none tracking-tighter">{cert.title}</p>
                            <p className="text-[10px] text-gray-400 font-bold mt-1 uppercase">{cert.date}</p>
                          </div>
                       </div>
                       <button className="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center active:scale-90 transition-all"><Download size={14}/></button>
                    </div>
                  ))}
                  {(!user.certificates || user.certificates.length === 0) && (
                    <p className="text-center text-[10px] font-black text-gray-300 uppercase py-4 tracking-widest italic">Пока нет сертификатов</p>
                  )}
               </div>
               {(user.certificates || []).length > 3 && (
                 <button onClick={() => setShowAllCertificates(!showAllCertificates)} className="text-gray-400 font-black text-[10px] uppercase w-full pt-2 flex items-center justify-center gap-1">
                    {showAllCertificates ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
                    {showAllCertificates ? t('hide') : t('showAll')}
                 </button>
               )}
             </div>
          </div>
        )}
      </div>

      {/* МОДАЛЬНЫЕ ОКНА */}
      {selectedNews && (
        <div className="fixed inset-0 z-[200] bg-black/80 backdrop-blur-sm flex items-end justify-center animate-in fade-in duration-300">
           <div className="bg-white w-full max-w-md h-[85vh] rounded-t-[50px] overflow-hidden flex flex-col relative text-left shadow-2xl animate-in slide-in-from-bottom-20 duration-500">
              <img src={selectedNews.image} className="w-full h-64 object-cover" alt="News" />
              <button 
                onClick={() => setSelectedNews(null)} 
                className="absolute top-6 right-6 bg-black/50 text-white p-2 rounded-full backdrop-blur-md active:scale-90 transition-all"
              >
                <X size={24}/>
              </button>
              <div className="p-8 overflow-y-auto">
                 <span className="text-[10px] font-black text-[#FF2B85] uppercase tracking-[0.2em] mb-2 block">{selectedNews.date}</span>
                 <h2 className="text-2xl font-black text-gray-900 uppercase leading-tight tracking-tighter mb-4">{selectedNews.title[lang]}</h2>
                 <div className="w-16 h-1.5 bg-[#7DFF00] rounded-full mb-6"></div>
                 <p className="text-gray-600 font-bold leading-relaxed italic pb-10">{selectedNews.content[lang]}</p>
              </div>
           </div>
        </div>
      )}

      {/* НИЖНЯЯ ПАНЕЛЬ НАВИГАЦИИ */}
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-[calc(100%-2rem)] max-w-md bg-black rounded-[35px] py-4 px-4 flex justify-between items-center shadow-2xl z-50 border border-white/10 backdrop-blur-md">
        <button onClick={() => setView('home')} className={`flex flex-col items-center gap-1 transition-all ${view === 'home' ? 'text-[#7DFF00] scale-110 shadow-[0_0_20px_rgba(125,255,0,0.2)]' : 'text-white/40 active:text-white/60'}`}>
          <Home size={20} /><span className="text-[6px] font-black uppercase tracking-widest">{t('home')}</span>
        </button>
        <button onClick={() => setView('news')} className={`flex flex-col items-center gap-1 transition-all ${view === 'news' ? 'text-[#7DFF00] scale-110 shadow-[0_0_20px_rgba(125,255,0,0.2)]' : 'text-white/40 active:text-white/60'}`}>
          <Newspaper size={20} /><span className="text-[6px] font-black uppercase tracking-widest">{t('news')}</span>
        </button>
        <button onClick={() => setView('events')} className={`flex flex-col items-center gap-1 transition-all ${view === 'events' ? 'text-[#7DFF00] scale-110 shadow-[0_0_20px_rgba(125,255,0,0.2)]' : 'text-white/40 active:text-white/60'}`}>
          <Zap size={20} /><span className="text-[6px] font-black uppercase tracking-widest">{t('events')}</span>
        </button>
        <button onClick={() => setView('volunteers')} className={`flex flex-col items-center gap-1 transition-all ${view === 'volunteers' ? 'text-[#7DFF00] scale-110 shadow-[0_0_20px_rgba(125,255,0,0.2)]' : 'text-white/40 active:text-white/60'}`}>
          <Users size={20} /><span className="text-[6px] font-black uppercase tracking-widest">{t('volunteers')}</span>
        </button>
        <button onClick={() => setView('profile')} className={`flex flex-col items-center gap-1 transition-all ${view === 'profile' ? 'text-[#7DFF00] scale-110 shadow-[0_0_20px_rgba(125,255,0,0.2)]' : 'text-white/40 active:text-white/60'}`}>
          <User size={20} /><span className="text-[6px] font-black uppercase tracking-widest">{t('profile')}</span>
        </button>
      </div>
    </div>
  );
};

export default App;