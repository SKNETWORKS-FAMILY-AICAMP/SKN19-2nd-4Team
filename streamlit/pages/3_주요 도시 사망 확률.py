import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import joblib
import xgboost as xgb

# --- 상수 정의 ---
# 모델 입력 인덱스: 0부터 38까지 (총 39개)
NUM_CLUSTERS_MODEL_INPUT = 39
MODEL_PATH = "models/2nd_xgb_model.joblib"
MAP_PATH = "data/erangel_map.jpg"
MODEL_COORD_MAX = 800000.0

# Streamlit 페이지 설정
st.set_page_config(page_title="지도 클러스터 분석", layout="wide")
st.title("🗺️ 주요 도시 사망확률 시각화")

# --- 0. 모델 및 데이터 로딩 ---


@st.cache_resource
def load_xgboost_model():
    """joblib 파일을 이용해 XGBoost 모델을 로드합니다."""
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        st.error(
            f"❌ 오류: '{MODEL_PATH}' 모델 파일을 찾을 수 없습니다. 경로를 확인해주세요."
        )
        st.stop()
    except Exception as e:
        st.error(f"❌ 오류: 모델 로딩 중 문제가 발생했습니다. ({e})")
        st.stop()


# 모델 로드 실행
xgb_model = load_xgboost_model()

# --- 1. 가상의 기존 데이터프레임 생성 및 초기화 (입력 폼 없이 사용) ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        {
            "player_name": ["NormalPlayer"],
            "avg_player_assists": [0.23],
            "avg_player_dbno": [0.58],
            "avg_player_dist_ride": [1090.14],
            "avg_player_dist_walk": [1120.07],
            "avg_player_dmg": [125.61],
            "avg_player_kills": [0.9],
            "avg_player_survive_time": [729.54],
            "avg_team_placement": [26.8],
        }
    )


# --- 2. 클러스터 그룹 및 위치 정보 정의 (수동 입력) ---
manual_cluster_groups = [
    {
        "cluster_id": "Severny",
        "name": "Severny",
        "center_x": 375000,
        "center_y": 125000,
        "width": 50000,
        "height": 50000,
        "angle": -10,
        "cluster_numbers": [39],
    },
    {
        "cluster_id": "Pochinki",
        "name": "Pochinki",
        "center_x": 351719,
        "center_y": 387742,
        "width": 50000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [1],
    },
    {
        "cluster_id": "Military Base",
        "name": "Military Base",
        "center_x": 443277,
        "center_y": 629393,
        "width": 100000,
        "height": 60000,
        "angle": 0,
        "cluster_numbers": [16, 24, 4],
    },
    {
        "cluster_id": "Georgopol",
        "name": "Georgopol",
        "center_x": 160000,
        "center_y": 250000,
        "width": 150000,
        "height": 80000,
        "angle": 0,
        "cluster_numbers": [32, 6],
    },
    {
        "cluster_id": "Stalber",
        "name": "Stalber",
        "center_x": 560000,
        "center_y": 120000,
        "width": 50000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [30],
    },
    {
        "cluster_id": "Roznok",
        "name": "Roznok",
        "center_x": 400000,
        "center_y": 300000,
        "width": 100000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [22, 8, 39],
    },
    {
        "cluster_id": "Yasnaya",
        "name": "Yasnaya Polyana",
        "center_x": 535834,
        "center_y": 228142,
        "width": 80000,
        "height": 80000,
        "angle": 30,
        "cluster_numbers": [18],
    },
    {
        "cluster_id": "Gatka",
        "name": "Gatka",
        "center_x": 213633,
        "center_y": 391744,
        "width": 50000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [13],
    },
    {
        "cluster_id": "Mylta",
        "name": "Mylta",
        "center_x": 591869,
        "center_y": 467273,
        "width": 50000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [3],
    },
    {
        "cluster_id": "Prison",
        "name": "Prison",
        "center_x": 617886,
        "center_y": 367229,
        "width": 20000,
        "height": 20000,
        "angle": 30,
        "cluster_numbers": [10],
    },
    {
        "cluster_id": "Primorsk",
        "name": "Primorsk",
        "center_x": 148592,
        "center_y": 602376,
        "width": 50000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [9],
    },
    {
        "cluster_id": "Mylta Power",
        "name": "Mylta Power",
        "center_x": 715443,
        "center_y": 423771,
        "width": 50000,
        "height": 50000,
        "angle": 30,
        "cluster_numbers": [14],
    },
    {
        "cluster_id": "Novorepnoye",
        "name": "Novorepnoye",
        "center_x": 600375,
        "center_y": 594871,
        "width": 50000,
        "height": 30000,
        "angle": 30,
        "cluster_numbers": [26],
    },
]


# --- 3. 지도 이미지 불러오기 ---
try:
    bg_image_pil = Image.open(MAP_PATH)
    img_width, img_height = bg_image_pil.size
except FileNotFoundError:
    st.error(f"⚠️ 지도 이미지 파일('{MAP_PATH}')을 찾을 수 없습니다.")
    st.stop()

# --- 4. 사용자 닉네임 선택 및 모델 예측 로직 (DF에서 데이터 가져오기) ---

available_nicknames = st.session_state.df["player_name"].unique().tolist()
current_user_nickname = "분석 대기"
player_stats_row_for_prediction = pd.DataFrame()


with st.sidebar:
    st.header("👤 플레이어 정보 선택")

    if available_nicknames:
        user_nickname = st.selectbox(
            "분석할 플레이어를 선택하세요.",
            options=available_nicknames,
            index=len(available_nicknames) - 1,
        )

        player_stats_row_for_prediction = st.session_state.df[
            st.session_state.df["player_name"] == user_nickname
        ].iloc[[-1]]

        current_user_nickname = user_nickname

        st.success(f"선택된 닉네임: **{current_user_nickname}**")
    else:
        st.warning("세션에 플레이어 데이터가 없습니다. 기본 데이터가 로드됩니다.")

# 클러스터별 확률 계산
PROB_DICT = {}
if not player_stats_row_for_prediction.empty:
    try:
        player_features = player_stats_row_for_prediction.drop(columns=["player_name"])

        # 1. 모델 입력 데이터 생성: 플레이어 스탯 행을 NUM_CLUSTERS (39)번 복사
        model_input_df = pd.concat(
            [player_features] * NUM_CLUSTERS_MODEL_INPUT, ignore_index=True
        )

        # 2. 'cluster_id' 특성 추가 (모델이 요구하는 0 ~ 38 인덱스)
        model_input_df["cluster_id"] = range(NUM_CLUSTERS_MODEL_INPUT)

        # 3. 예측 수행:
        feature_order = xgb_model.get_booster().feature_names
        model_input_df = model_input_df[feature_order]

        probabilities = xgb_model.predict_proba(model_input_df)[:, 1]

        # 4. 확률을 PROB_DICT에 매핑 (모델 인덱스 i를 실제 클러스터 ID i+1에 매핑)
        # PROB_DICT[i+1] = probabilities[i]
        PROB_DICT = {i + 1: probabilities[i] for i in range(NUM_CLUSTERS_MODEL_INPUT)}

    except Exception as e:
        st.error(
            f"❌ 예측 오류 발생: 모델 예측에 실패했습니다. (모델 입력 피처/순서 확인 필요: {e})"
        )
        PROB_DICT = {i: 0.5 for i in range(1, NUM_CLUSTERS_MODEL_INPUT + 1)}

# --- 5. 클러스터 영역 시각화 (메인 화면) ---

st.subheader(f"{current_user_nickname}님의 예상 생존 확률 분석 결과입니다.")
st.caption(
    "생존 확률이 낮으면 초록색(안전), 높으면 빨간색(위험)으로 표시됩니다. 지도 위의 백분율은 해당 지역에 매핑된 클러스터들의 평균 확률입니다."
)

# 스크롤 방지를 위해 컬럼으로 공간 제한
col_map, col_spacer = st.columns([2, 1])

with col_map:
    # 좌표 스케일링
    scale_x = img_width / MODEL_COORD_MAX
    scale_y = img_height / MODEL_COORD_MAX

    # Matplotlib Colormap 생성 (0% = 초록색, 100% = 빨간색)
    # 생존 확률이므로, 낮으면 초록(안전), 높으면 빨강(위험)
    cm = plt.cm.get_cmap("RdYlGn_r", 100)

    # Matplotlib figure 및 axes 생성 (크기: 5x5)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(bg_image_pil, extent=[0, img_width, img_height, 0])

    # 수동으로 정의된 위치 그룹을 기반으로 타원을 그립니다.
    for group in manual_cluster_groups:
        cluster_nums = group["cluster_numbers"]

        # 픽셀 좌표로 변환
        scaled_mean = (group["center_x"] * scale_x, group["center_y"] * scale_y)
        scaled_width = group["width"] * scale_x
        scaled_height = group["height"] * scale_y

        # 해당 지역의 최종 평균 확률 계산 로직
        if cluster_nums:
            probabilities = [
                PROB_DICT.get(num, 0.5) for num in cluster_nums if num in PROB_DICT
            ]
            prob_value = np.mean(probabilities) if probabilities else 0.5
        else:
            prob_value = 0.5

        # 확률 값에 따라 색상 가져오기
        ellipse_color = cm(prob_value)

        # 표시할 텍스트 형식 지정 (확률만 표시)
        prob_text = f"{prob_value:.0%}"

        # 타원(Ellipse) 생성 및 추가
        ellipse = Ellipse(
            xy=scaled_mean,
            width=scaled_width,
            height=scaled_height,
            angle=group["angle"],
            edgecolor=ellipse_color,
            facecolor=ellipse_color,
            alpha=0.6,
            linewidth=2,
        )
        ax.add_patch(ellipse)

        # 평균 확률 텍스트 추가
        ax.text(
            scaled_mean[0],
            scaled_mean[1],
            prob_text,
            color="white",
            fontsize=8,
            fontweight="bold",
            ha="center",
            va="center",
            bbox=dict(
                facecolor="black", alpha=0.5, edgecolor="none", boxstyle="round,pad=0.3"
            ),
        )

    # 축 범위 설정 및 축 숨기기
    ax.set_xlim(0, img_width)
    ax.set_ylim(img_height, 0)
    ax.axis("off")

    # Streamlit에 Matplotlib 그림 표시
    st.pyplot(fig)


# --- UI: 사용된 데이터 확인 (하단) ---
st.subheader("모델 예측에 사용된 플레이어 데이터")
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

if not player_stats_row_for_prediction.empty:
    st.dataframe(
        player_stats_row_for_prediction.rename(columns=column_labels).set_index(
            "플레이어"
        ),
        use_container_width=True,
    )
else:
    st.info("현재 모델 예측에 사용된 데이터가 없습니다.")
