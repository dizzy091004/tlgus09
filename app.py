import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
from PIL import Image

# ==========================================
# 1. 초기 설정 및 데이터베이스 연결
# ==========================================

# 앱의 페이지 타이틀과 아이콘 설정
st.set_page_config(page_title="에듀매니저: 학업 & 시간 관리", page_icon="🎓", layout="wide")

# 이미지 업로드를 위한 폴더 생성 (없으면 생성)
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 데이터베이스 연결 함수
def get_connection():
    # SQLite DB 파일을 생성하고 연결합니다.
    conn = sqlite3.connect("study_data.db", check_same_thread=False)
    return conn

# 테이블 생성 (최초 실행 시)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    # 1. 수행평가 테이블: 과목, 과제명, 비중, 마감일 저장
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  subject TEXT, title TEXT, weight REAL, deadline DATE)''')
    # 2. 오답노트 테이블: 과목, 태그(유형), 이미지경로 저장
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  subject TEXT, tag TEXT, img_path TEXT, created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 2. 핵심 로직: 우선순위 계산 알고리즘
# ==========================================

def calculate_priority(weight, deadline_str):
    """
    사용자가 요청한 '중요도(비중) × 남은 시간' 개념을 응용한 알고리즘입니다.
    실제로는 마감일이 가까울수록 우선순위가 높아야 하므로 아래 공식을 사용합니다.
    우선순위 점수 = (비중 * 10) / (남은 일수 + 1)
    """
    try:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        days_left = (deadline - today).days
        
        if days_left < 0:
            return 0
        
        # 우선순위 점수 산출 (마감 임박 + 높은 비중 = 높은 점수)
        priority_score = (weight * 10) / (days_left + 1)
        return round(priority_score, 2)
    except:
        return 0

# ==========================================
# 3. 사이드바 메뉴 구성
# ==========================================

st.sidebar.title("🎓 EduManager v1.0")
menu = st.sidebar.radio("메뉴를 선택하세요", ["🏠 홈", "📅 수행평가 관리기", "📑 오답노트 스캔/분류"])

# ==========================================
# 4. 기능 구현: 홈 화면
# ==========================================

if menu == "🏠 홈":
    st.title("반갑습니다! 오늘을 최고의 하루로 만들어보세요. 🌟")
    st.write("단어장 앱의 로직을 응용한 **학업 통합 관리 시스템**입니다.")
    st.info("왼쪽 메뉴를 통해 기능을 선택해 주세요.")
    
    # 요약 정보 로드
    conn = get_connection()
    try:
        task_count = pd.read_sql_query("SELECT COUNT(*) as count FROM tasks", conn)['count'][0]
        note_count = pd.read_sql_query("SELECT COUNT(*) as count FROM notes", conn)['count'][0]
    except:
        task_count, note_count = 0, 0
    conn.close()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("진행 중인 수행평가", f"{task_count}건")
    with col2:
        st.metric("저장된 오답노트", f"{note_count}개")
    
    st.divider()
    st.subheader("💡 사용 팁")
    st.markdown("""
    1. **수행평가 관리기**: 과제 배점과 마감일을 입력하면 '무엇을 먼저 할지' 자동으로 계산해 줍니다.
    2. **오답노트**: 틀린 문제 사진을 찍고 '실수 유형'을 태그로 달아보세요. 나중에 실수만 모아볼 수 있습니다.
    """)

# ==========================================
# 5. 기능 구현: 수행평가 & 일정 통합 관리기
# ==========================================

elif menu == "📅 수행평가 관리기":
    st.title("📅 수행평가 우선순위 관리")
    
    with st.expander("➕ 새 수행평가 추가", expanded=False):
        with st.form("task_form"):
            col1, col2 = st.columns(2)
            with col1:
                subject = st.text_input("과목명", placeholder="예: 수학, 영어")
                title = st.text_input("과제명", placeholder="예: 탐구 보고서")
            with col2:
                weight = st.number_input("반영 비중 (%)", min_value=1.0, max_value=100.0, value=10.0)
                deadline = st.date_input("마감일")
            
            submit = st.form_submit_button("데이터베이스에 저장")
            
            if submit:
                if subject and title:
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute("INSERT INTO tasks (subject, title, weight, deadline) VALUES (?, ?, ?, ?)", 
                              (subject, title, weight, str(deadline)))
                    conn.commit()
                    conn.close()
                    st.success(f"'{title}' 과제가 추가되었습니다!")
                else:
                    st.error("과목명과 과제명을 입력해 주세요.")

    st.divider()
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()

    if not df.empty:
        df['우선순위 점수'] = df.apply(lambda row: calculate_priority(row['weight'], row['deadline']), axis=1)
        df = df.sort_values(by='우선순위 점수', ascending=False)
        
        st.dataframe(df[['subject', 'title', 'weight', 'deadline', '우선순위 점수']], 
                     use_container_width=True,
                     column_config={
                         "subject": "과목",
                         "title": "과제명",
                         "weight": "비중(%)",
                         "deadline": "마감일",
                         "우선순위 점수": st.column_config.ProgressColumn("시급도 (높을수록 먼저!)", min_value=0, max_value=100)
                     })
    else:
        st.info("등록된 과제가 없습니다.")

# ==========================================
# 6. 기능 구현: 오답노트 스캔 & 분류기
# ==========================================

elif menu == "📑 오답노트 스캔/분류":
    st.title("📑 스마트 오답노트")

    with st.expander("📸 새로운 오답 등록", expanded=False):
        uploaded_file = st.file_uploader("문제 사진(JPG, PNG)을 선택하세요", type=['jpg', 'jpeg', 'png'])
        col1, col2 = st.columns(2)
        with col1:
            note_subject = st.selectbox("과목 선택", ["수학", "영어", "국어", "과학", "사회", "기타"])
        with col2:
            note_tag = st.multiselect("유형 태그 선택", ["계산 실수", "개념 부족", "시간 부족", "문제 이해 불가", "단어 암기 미흡"])
        
        if st.button("오답노트에 업로드"):
            if uploaded_file and note_subject:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{uploaded_file.name}"
                file_path = os.path.join(UPLOAD_DIR, file_name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                conn = get_connection()
                c = conn.cursor()
                c.execute("INSERT INTO notes (subject, tag, img_path, created_at) VALUES (?, ?, ?, ?)", 
                          (note_subject, ",".join(note_tag), file_path, datetime.now()))
                conn.commit()
                conn.close()
                st.success("성공적으로 저장되었습니다!")
            else:
                st.warning("사진과 과목을 확인해 주세요.")

    st.divider()
    conn = get_connection()
    notes_df = pd.read_sql_query("SELECT * FROM notes", conn)
    conn.close()

    if not notes_df.empty:
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            search_subject = st.multiselect("과목별로 보기", notes_df['subject'].unique())
        with filter_col2:
            all_tags = set()
            for t in notes_df['tag'].str.split(','):
                all_tags.update(t)
            search_tag = st.multiselect("틀린 이유별로 보기", list(all_tags) if all_tags else [])

        filtered_df = notes_df
        if search_subject:
            filtered_df = filtered_df[filtered_df['subject'].isin(search_subject)]
        if search_tag:
            filtered_df = filtered_df[filtered_df['tag'].apply(lambda x: any(tag in x for tag in search_tag))]

        if not filtered_df.empty:
            cols = st.columns(3)
            for i, (idx, row) in enumerate(filtered_df.iterrows()):
                with cols[i % 3]:
                    st.image(row['img_path'], caption=f"[{row['subject']}] {row['tag']}", use_container_width=True)
        else:
            st.warning("검색 결과가 없습니다.")
    else:
        st.info("기록된 오답이 없습니다.")
