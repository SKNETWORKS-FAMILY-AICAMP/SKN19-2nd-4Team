import streamlit as st
import pandas as pd

# --- 1. 가상의 기존 데이터프레임 생성 ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        [
            {
                "player_name": "NormalPlayer",
                "avg_player_assists": 0.23,
                "avg_player_dbno": 0.58,
                "avg_player_dist_ride": 1090.14,
                "avg_player_dist_walk": 1120.07,
                "avg_player_dmg": 125.61,
                "avg_player_kills": 0.9,
                "avg_player_survive_time": 729.54,
                "avg_team_placement": 26.8,
            },
            {
                "player_name": "이상혁",
                "avg_player_assists": 0.1,
                "avg_player_dbno": 1.3,
                "avg_player_dist_ride": 500.0,
                "avg_player_dist_walk": 200.0,
                "avg_player_dmg": 400.0,
                "avg_player_kills": 3.1,
                "avg_player_survive_time": 500.0,
                "avg_team_placement": 13.0,
            },
            {
                "player_name": "김성욱",
                "avg_player_assists": 0.23,
                "avg_player_dbno": 0.4,
                "avg_player_dist_ride": 1500.0,
                "avg_player_dist_walk": 1000.0,
                "avg_player_dmg": 100.0,
                "avg_player_kills": 0.7,
                "avg_player_survive_time": 1400.0,
                "avg_team_placement": 10.0,
            },
            {
                "player_name": "신지섭",
                "avg_player_assists": 0.12,
                "avg_player_dbno": 0.8,
                "avg_player_dist_ride": 1200.0,
                "avg_player_dist_walk": 800.0,
                "avg_player_dmg": 145.0,
                "avg_player_kills": 1.2,
                "avg_player_survive_time": 900.0,
                "avg_team_placement": 17.0,
            },
        ]
    )


# 페이지 제목 설정
st.title("📊 PUBG 플레이어 데이터 입력 페이지")
st.header("당신의 플레이 스타일 데이터를 입력해주세요.")

# --- 페이지 상단 레이아웃 컬럼 생성 ---
col_name, _, col_method = st.columns([4, 4, 2])

# --- 라디오 버튼을 오른쪽 컬럼에 배치 (form 바깥) ---
with col_method:
    input_method = st.radio(
        "데이터 입력 방식을 선택하세요.",
        ("숫자", "바"),
        horizontal=True,
        label_visibility="collapsed",
    )

# --- form 생성 및 이름 입력창을 왼쪽 컬럼에 배치 ---
with st.form("player_data_form"):
    with col_name:
        player_name = st.text_input(
            "플레이어 이름 (Player Name)",
            label_visibility="collapsed",
            placeholder="플레이어 이름 (Player Name)",
        )

    # 폼 내부에서 별도의 컬럼으로 스탯 입력 부분 구성
    col_stat1, col_stat2 = st.columns(2)

    if input_method == "숫자":
        with col_stat1:
            avg_player_assists = st.number_input(
                "평균 어시스트", min_value=0.0, format="%.4f"
            )
            avg_player_dbno = st.number_input(
                "평균 DBNO",
                min_value=0.0,
                format="%.4f",
                help="DBNO는 킬하지 못하고 기절만 시킨 횟수입니다.",
            )
            avg_player_dist_ride = st.number_input(
                "평균 이동 거리 (차량)", min_value=0.0, format="%.4f"
            )
            avg_player_dmg = st.number_input(
                "평균 데미지", min_value=0.0, format="%.4f"
            )
            avg_team_placement = st.number_input(
                "평균 팀 순위", min_value=1.0, max_value=100.0, format="%.4f"
            )
        with col_stat2:
            avg_player_dist_walk = st.number_input(
                "평균 이동 거리 (도보)", min_value=0.0, format="%.4f"
            )
            avg_player_kills = st.number_input("평균 킬", min_value=0.0, format="%.4f")
            avg_player_survive_time = st.number_input(
                "평균 생존 시간(초)", min_value=0.0, format="%.4f"
            )

    else:  # "바" 선택 시 (슬라이더)
        with col_stat1:
            avg_player_assists = st.slider("평균 어시스트", 0.0, 3.0, 1.0, 0.01)
            avg_player_dbno = st.slider(
                "평균 DBNO",
                0.0,
                11.0,
                1.0,
                0.01,
                help="DBNO는 킬하지 못하고 기절만 시킨 횟수입니다.",
            )
            avg_player_dist_ride = st.slider("평균 이동 거리 (차량)", 0, 8000, 1000, 10)
            avg_player_dmg = st.slider("평균 데미지", 0, 1500, 150, 1)
            avg_team_placement = st.slider("평균 팀 순위", 1.0, 100.0, 50.0, 0.1)
        with col_stat2:
            avg_player_dist_walk = st.slider("평균 이동 거리 (도보)", 0, 3500, 500, 10)
            avg_player_kills = st.slider("평균 킬", 0.0, 16.0, 1.0, 0.1)
            avg_player_survive_time = st.slider("평균 생존 시간(초)", 0, 3600, 1500, 10)

    # --- 폼 제출 버튼 위치 변경 ---
    _, col_button = st.columns([4, 1])
    with col_button:
        submitted = st.form_submit_button("데이터 제출")

# --- 제출 후 처리 로직 ---
if submitted:
    # 플레이어 이름이 비어있는지 확인
    if not player_name:
        st.error("⚠️ 플레이어 이름을 반드시 입력해야 합니다.")
    else:  # 이름이 입력되었을 경우에만 아래 로직 실행
        new_data = {
            "player_name": [player_name],
            "avg_player_assists": [avg_player_assists],
            "avg_player_dbno": [avg_player_dbno],
            "avg_player_dist_ride": [avg_player_dist_ride],
            "avg_player_dist_walk": [avg_player_dist_walk],
            "avg_player_dmg": [avg_player_dmg],
            "avg_player_kills": [avg_player_kills],
            "avg_player_survive_time": [avg_player_survive_time],
            "avg_team_placement": [avg_team_placement],
        }
        new_df = pd.DataFrame(new_data)
        st.session_state.df = pd.concat(
            [st.session_state.df, new_df], ignore_index=True
        )
        st.success(f"'{player_name}'님의 데이터가 성공적으로 추가되었습니다!")

# --- 4. 항상 전체 데이터프레임을 화면에 표시합니다 ---
st.subheader("전체 데이터 확인 (누적)")
column_labels = {
    "player_name": "플레이어",
    "avg_player_assists": "평균 어시스트",
    "avg_player_dbno": "평균 DBNO",
    "avg_player_dist_ride": "평균 이동(차량)",
    "avg_player_dist_walk": "평균 이동(도보)",
    "avg_player_dmg": "평균 데미지",
    "avg_player_kills": "평균 킬",
    "avg_player_survive_time": "평균 생존 시간(초)",
    "avg_team_placement": "평균 팀 순위",
}
st.dataframe(st.session_state.df.rename(columns=column_labels))
