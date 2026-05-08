import streamlit as st
import pandas as pd
import os
import math
import streamlit.components.v1 as components

# ==========================================
# 1. 초기 설정 및 테마 적용
# ==========================================

st.set_page_config(page_title="EduScience: 통합 과학 실험실", page_icon="🔬", layout="wide")

# 프리미엄 디자인을 위한 커스텀 CSS 주입
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    div.stMetric, .stDataFrame, .stCodeBlock {
        background-color: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    h1, h2, h3, p, span {
        color: #f8fafc !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 사이드바 메뉴 (통합 과학)
# ==========================================

st.sidebar.title("🔬 EduScience Lab")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "실험실 메뉴", 
    [
        "🏠 과학 실험실 홈", 
        "🔭 물리학: 3D 포물선 운동", 
        "🧪 화학: 원자 구조 시각화", 
        "🧬 생명과학: DNA 3D 구조",
        "🤖 AI 과학 튜터"
    ]
)

# ==========================================
# 3. 기능 구현: 홈 화면
# ==========================================

if menu == "🏠 과학 실험실 홈":
    st.title("🔬 EduScience: 통합 과학 학습 플랫폼")
    st.markdown("""
    ### 물리, 화학, 생명과학을 하나로!
    이 앱은 고등학교 과학 교육과정의 핵심 개념들을 3D 시뮬레이션과 AI를 통해 탐구할 수 있도록 돕습니다.
    
    #### 🚀 탐구 분야:
    1. **🔭 물리학**: 3D 공간에서의 역학적 운동 분석.
    2. **🧪 화학**: 눈에 보이지 않는 미시적 원자 세계 탐험.
    3. **🧬 생명과학**: 생명의 설계도, DNA의 입체 구조 이해.
    4. **🤖 AI 과학 튜터**: 질문을 통해 스스로 답을 찾아가는 과학적 사고 훈련.
    """)
    st.image("https://images.unsplash.com/photo-1532094349884-543bc11b234d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", use_container_width=True)

# ==========================================
# 4. 기능 구현: 🔭 물리학 (포물선 운동)
# ==========================================

elif menu == "🔭 물리학: 3D 포물선 운동":
    st.title("🔭 물리학 실험실: 3D 포물선 운동")
    col1, col2, col3 = st.columns(3)
    with col1: velocity = st.slider("초기 속도 (m/s)", 5, 50, 25)
    with col2: angle = st.slider("발사 각도 (°)", 10, 80, 45)
    with col3: gravity = st.slider("중력 가속도 (m/s²)", 1.0, 20.0, 9.8)

    rad = math.radians(angle)
    vx, vy = velocity * math.cos(rad), velocity * math.sin(rad)

    three_js_physics = f"""
    <div id="container" style="width: 100%; height: 500px; border-radius: 15px; background: #0f172a;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias:true}});
        renderer.setSize(window.innerWidth, 500);
        document.getElementById('container').appendChild(renderer.domElement);
        scene.add(new THREE.GridHelper(100, 20, 0x334155, 0x1e293b));
        const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 32), new THREE.MeshPhongMaterial({{color:0x3b82f6}}));
        scene.add(sphere);
        scene.add(new THREE.PointLight(0xffffff, 1, 100).clone().position.set(10, 10, 10));
        scene.add(new THREE.AmbientLight(0x404040));
        camera.position.set(20, 15, 40); camera.lookAt(0, 5, 0);
        let t = 0;
        function animate() {{
            requestAnimationFrame(animate);
            t += 0.05; const x = {vx}*t, y = {vy}*t - 0.5*{gravity}*t*t;
            if (y >= 0) sphere.position.set(x, y, 0); else t = 0;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """
    components.html(three_js_physics, height=520)

# ==========================================
# 5. 기능 구현: 🧪 화학 (원자 구조)
# ==========================================

elif menu == "🧪 화학: 원자 구조 시각화":
    st.title("🧪 화학 실험실: 원자 구조 & 전자 배치")
    element = st.selectbox("원소 선택", ["수소 (H)", "헬륨 (He)", "리튬 (Li)", "탄소 (C)", "산소 (O)"])
    
    # 원자 번호에 따른 전자 수 설정
    atomic_data = {"수소 (H)": 1, "헬륨 (He)": 2, "리튬 (Li)": 3, "탄소 (C)": 6, "산소 (O)": 8}
    electrons = atomic_data[element]
    
    st.write(f"**{element}** 원자의 3D 모델입니다. 중심의 원자핵과 주위를 도는 전자를 관찰해 보세요.")

    three_js_chem = f"""
    <div id="container" style="width: 100%; height: 500px; border-radius: 15px; background: #0f172a;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias:true}});
        renderer.setSize(window.innerWidth, 500);
        document.getElementById('container').appendChild(renderer.domElement);

        // 원자핵
        const nucleus = new THREE.Mesh(new THREE.SphereGeometry(1.5, 32, 32), new THREE.MeshPhongMaterial({{color:0xef4444}}));
        scene.add(nucleus);

        // 전자들 생성
        const electronGroup = new THREE.Group();
        for(let i=0; i<{electrons}; i++) {{
            const e = new THREE.Mesh(new THREE.SphereGeometry(0.3, 16, 16), new THREE.MeshPhongMaterial({{color:0xfde047}}));
            const orbitSize = i < 2 ? 5 : 8; // 전자 껍질 레이어
            e.position.x = orbitSize;
            const pivot = new THREE.Group();
            pivot.rotation.y = (Math.PI * 2 / {electrons}) * i;
            pivot.rotation.x = Math.random() * Math.PI;
            pivot.add(e);
            electronGroup.add(pivot);
        }}
        scene.add(electronGroup);

        scene.add(new THREE.PointLight(0xffffff, 1, 100).clone().position.set(10, 10, 10));
        scene.add(new THREE.AmbientLight(0x404040));
        camera.position.z = 15;

        function animate() {{
            requestAnimationFrame(animate);
            electronGroup.children.forEach((pivot, idx) => {{
                pivot.rotation.y += 0.02 + (idx * 0.005);
                pivot.rotation.z += 0.01;
            }});
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """
    components.html(three_js_chem, height=520)

# ==========================================
# 6. 기능 구현: 🧬 생명과학 (DNA)
# ==========================================

elif menu == "🧬 생명과학: DNA 3D 구조":
    st.title("🧬 생명과학 실험실: DNA 이중 나선")
    st.write("생명체의 설계도인 DNA의 이중 나선 구조를 3D로 탐사합니다.")
    
    three_js_bio = f"""
    <div id="container" style="width: 100%; height: 500px; border-radius: 15px; background: #0f172a;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias:true}});
        renderer.setSize(window.innerWidth, 500);
        document.getElementById('container').appendChild(renderer.domElement);

        const dnaGroup = new THREE.Group();
        for(let i=0; i<40; i++) {{
            const y = (i - 20) * 0.8;
            const angle = i * 0.4;
            
            // 두 가닥의 인산-당 골격
            const s1 = new THREE.Mesh(new THREE.SphereGeometry(0.4, 16, 16), new THREE.MeshPhongMaterial({{color:0x10b981}}));
            s1.position.set(Math.cos(angle)*4, y, Math.sin(angle)*4);
            
            const s2 = new THREE.Mesh(new THREE.SphereGeometry(0.4, 16, 16), new THREE.MeshPhongMaterial({{color:0x10b981}}));
            s2.position.set(Math.cos(angle + Math.PI)*4, y, Math.sin(angle + Math.PI)*4);
            
            // 염기 쌍 (연결선)
            const lineGeom = new THREE.BufferGeometry().setFromPoints([s1.position, s2.position]);
            const line = new THREE.Line(lineGeom, new THREE.LineBasicMaterial({{color:0x64748b}}));
            
            dnaGroup.add(s1); dnaGroup.add(s2); dnaGroup.add(line);
        }}
        scene.add(dnaGroup);

        scene.add(new THREE.PointLight(0xffffff, 1, 100).clone().position.set(10, 10, 10));
        scene.add(new THREE.AmbientLight(0x404040));
        camera.position.set(0, 0, 25);

        function animate() {{
            requestAnimationFrame(animate);
            dnaGroup.rotation.y += 0.01;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """
    components.html(three_js_bio, height=520)

# ==========================================
# 7. 기능 구현: 🤖 AI 과학 튜터
# ==========================================

elif menu == "🤖 AI 과학 튜터":
    st.title("🤖 AI 통합 과학 튜터")
    st.info("💡 물리, 화학, 생명과학에 대한 질문을 남겨주세요. 원리를 깨우칠 수 있도록 돕겠습니다.")
    
    if "sci_messages" not in st.session_state: st.session_state.sci_messages = []
    for msg in st.session_state.sci_messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("질문을 입력하세요 (예: 미토콘드리아의 역할은 무엇인가요?)"):
        st.session_state.sci_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = f"'{prompt}'에 대해 함께 알아봅시다. "
            if "세포" in prompt or "DNA" in prompt: response += "생명체의 기본 단위인 세포 내에서 해당 구조가 어떤 기능을 수행하는지 떠올려 볼까요?"
            elif "원자" in prompt or "반응" in prompt: response += "화학적 결합과 전자 배치의 관점에서 접근해 보는 것은 어떨까요?"
            else: response += "이 현상의 핵심적인 과학적 원리가 무엇인지 먼저 정의해 보는 것이 좋겠네요."
            st.markdown(response)
            st.session_state.sci_messages.append({"role": "assistant", "content": response})
