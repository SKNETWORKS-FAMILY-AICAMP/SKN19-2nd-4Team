import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import joblib
import xgboost as xgb
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from streamlit_image_coordinates import streamlit_image_coordinates
from io import BytesIO

# --- 상수 및 경로 정의 ---
NUM_CLUSTERS_MODEL_INPUT = 39
MODEL_PATH_XGB = "models/2nd_xgb_model.joblib"
MODEL_PATH_GMM = "models/gmm_model.joblib"
SCALER_PATH = "models/scaler.joblib"
MAP_PATH = "data/erangel_map.jpg"
MODEL_COORD_MAX = 800000.0
DISPLAY_WIDTH = 800  # ⭐ 지도 표시 너비를 600 -> 800으로 확대

# Streamlit 페이지 설정
st.set_page_config(page_title="지도 클릭 분석", layout="wide")
st.title("🗺️ 특정지역 사망확률 예측")

# --- 0. 모델 및 데이터 로딩 (캐싱 적용) ---


@st.cache_resource
def load_models_and_scaler():
    """XGBoost, GMM 모델 및 Scaler를 로드합니다."""
    try:
        xgb_model = joblib.load(MODEL_PATH_XGB)
        gmm_model = joblib.load(MODEL_PATH_GMM)
        scaler = joblib.load(SCALER_PATH)
        return xgb_model, gmm_model, scaler
    except FileNotFoundError as e:
        st.error(
            f"❌ 오류: 모델/스케일러 파일 '{e.filename}'을(를) 찾을 수 없습니다. 경로를 확인해주세요."
        )
        st.stop()
    except Exception as e:
        st.error(f"❌ 오류: 모델/스케일러 로딩 중 문제가 발생했습니다. ({e})")
        st.stop()


xgb_model, gmm_model, scaler = load_models_and_scaler()

# --- 1. 가상의 기존 데이터프레임 생성 및 초기화 ---
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

available_nicknames = st.session_state.df["player_name"].unique().tolist()
current_user_nickname = "분석 대기"
player_stats_row = pd.DataFrame()


# --- 예측 및 이미지 생성 함수 ---
def generate_prediction_image(
    input_image_pil,
    clicked_x,
    clicked_y,
    player_stats,
    xgb_model,
    gmm_model,
    scaler,
    img_width,
    img_height,
    display_width,
    display_height,
):
    """
    클릭된 좌표와 플레이어 스탯을 기반으로 예측을 수행하고,
    점이 찍힌 새로운 이미지를 Matplotlib으로 생성하여 반환합니다.
    """
    if player_stats.empty:
        return input_image_pil, "플레이어 데이터를 선택하세요."

    # 픽셀 좌표를 모델 좌표 (0~800000)로 스케일링 및 보정
    original_x_on_full_map = clicked_x * (img_width / display_width)
    original_y_on_full_map = clicked_y * (img_height / display_height)

    model_coord_x = original_x_on_full_map * (MODEL_COORD_MAX / img_width)
    model_coord_y = original_y_on_full_map * (MODEL_COORD_MAX / img_height)

    xgb_cluster_input_index = None
    death_prob = None

    try:
        gmm_input = pd.DataFrame([[model_coord_x, model_coord_y]], columns=["x", "y"])
        scaled_gmm_input = scaler.transform(gmm_input)

        predicted_cluster_index = gmm_model.predict(scaled_gmm_input)[0]

        # ⭐ GMM 인덱스 0과 2~39 매핑 로직 (0부터 39까지 반환한다고 가정)
        if predicted_cluster_index == 0:
            xgb_cluster_input_index = 0  # 0은 0으로 매핑
        elif 2 <= predicted_cluster_index <= 39:
            xgb_cluster_input_index = (
                predicted_cluster_index - 1
            )  # 2->1, 39->38 (XGBoost 인덱스)
        else:
            # GMM이 1을 반환하거나, 범위를 벗어난 값을 반환할 경우 에러 처리
            st.warning(
                f"GMM이 유효하지 않은 클러스터 인덱스({predicted_cluster_index})를 반환했습니다. (1은 제외)"
            )
            return input_image_pil, "GMM 예측 오류 (유효하지 않은 클러스터 ID)"

        player_features = player_stats.drop(columns=["player_name"])
        xgb_input = player_features.copy()
        xgb_input["cluster_id"] = xgb_cluster_input_index

        feature_order = xgb_model.get_booster().feature_names
        xgb_input = xgb_input[feature_order]

        survival_prob = xgb_model.predict_proba(xgb_input)[:, 1][0]
        death_prob = 1.0 - survival_prob

    except Exception as e:
        st.error(f"❌ 모델 예측 중 오류 발생: {e}")
        return input_image_pil, f"예측 오류: {e}"

    # Matplotlib으로 이미지 생성
    # figsize와 dpi를 조정하여 DISPLAY_WIDTH/HEIGHT에 맞춤
    fig, ax = plt.subplots(figsize=(display_width / 100, display_height / 100), dpi=100)
    ax.imshow(input_image_pil, extent=[0, img_width, img_height, 0])

    # 클릭 지점에 점 찍기
    ax.plot(
        original_x_on_full_map,
        original_y_on_full_map,
        "o",
        color="red",
        markersize=8,
        markeredgecolor="white",
        markeredgewidth=1.5,
    )

    # 확률 텍스트 표시
    if death_prob is not None:
        prob_text = f"Death_proba : {death_prob:.1%}"
        ax.text(
            original_x_on_full_map,
            original_y_on_full_map - 20,
            prob_text,
            color="red" if death_prob > 0.5 else "green",
            fontsize=9,
            fontweight="bold",
            ha="center",
            va="bottom",
            bbox=dict(
                facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.3"
            ),
        )

    ax.set_xlim(0, img_width)
    ax.set_ylim(img_height, 0)
    ax.axis("off")
    fig.tight_layout(pad=0)

    # Figure를 BytesIO로 저장 후 PIL Image로 로드
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, dpi=100)
    buf.seek(0)
    pil_img = Image.open(buf).convert("RGB")
    plt.close(fig)

    return (
        pil_img,
        f"✅ 예측 결과: 사망 확률 **{death_prob:.2%}** (클러스터 ID: {xgb_cluster_input_index})",
    )


# --- 2. 지도 이미지 로드 및 초기 설정 ---
try:
    bg_image_pil = Image.open(MAP_PATH).convert("RGB")
    img_width, img_height = bg_image_pil.size
    display_height = int(DISPLAY_WIDTH * (img_height / img_width))
except FileNotFoundError:
    st.error(f"⚠️ 지도 이미지 파일('{MAP_PATH}')을 찾을 수 없습니다.")
    st.stop()

# 세션 상태에 원본 이미지 PIL 객체와 현재 표시할 이미지 저장
if "original_map_image" not in st.session_state:
    st.session_state.original_map_image = bg_image_pil
    st.session_state.current_display_image = bg_image_pil
if "prediction_result_text" not in st.session_state:
    st.session_state.prediction_result_text = (
        "👆 지도 위를 클릭하여 사망 확률을 예측해보세요."
    )


# --- 3. 메인 화면 로직: 플레이어 선택 및 이미지 표시 ---

# 3.1 [사이드바: 플레이어 선택 및 데이터 가져오기]
with st.sidebar:
    st.header("👤 플레이어 정보 선택")
    if available_nicknames:
        user_nickname = st.selectbox(
            "분석할 플레이어를 선택하세요.",
            options=available_nicknames,
            index=len(available_nicknames) - 1,
        )
        player_stats_row = (
            st.session_state.df[st.session_state.df["player_name"] == user_nickname]
            .iloc[[-1]]
            .reset_index(drop=True)
        )
        current_user_nickname = user_nickname
        st.success(f"선택: **{current_user_nickname}**")
    else:
        st.warning("세션에 플레이어 데이터가 없습니다.")


# 3.2 [메인 화면 UI]
st.subheader(f"{current_user_nickname}님의 예상 사망 확률 분석")

st.markdown("##### 1. 분석할 지점을 지도 위에서 클릭하세요.")

# streamlit_image_coordinates를 사용하여 좌표만 얻고, 그 위에 점이 찍힌 이미지 표시
clicked_value = streamlit_image_coordinates(
    st.session_state.current_display_image,
    key="map_click_input",
    width=DISPLAY_WIDTH,
    height=display_height,
)

# 클릭이 발생하면 이미지 업데이트 로직을 실행하고 재실행
if clicked_value and not player_stats_row.empty:
    clicked_x = clicked_value["x"]
    clicked_y = clicked_value["y"]

    updated_image, result_message = generate_prediction_image(
        st.session_state.original_map_image,
        clicked_x,
        clicked_y,
        player_stats_row,
        xgb_model,
        gmm_model,
        scaler,
        img_width,
        img_height,
        DISPLAY_WIDTH,
        display_height,
    )
    st.session_state.current_display_image = updated_image
    st.session_state.prediction_result_text = result_message
    st.rerun()


# --- 4. 하단 사용 데이터 표시 ---
st.markdown("---")
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

if not player_stats_row.empty:
    st.dataframe(
        player_stats_row.rename(columns=column_labels).set_index("플레이어"),
        use_container_width=True,
    )
else:
    st.info("사이드바에서 플레이어를 선택하고 지도 위를 클릭하여 분석을 시작하세요.")
