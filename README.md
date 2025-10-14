<div align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=FF0000&height=240&text=SKN19-2nd-4Team&animation=&fontColor=ffffff&fontSize=90" />
</div>







# 배그나라 치킨공주/아임그라운드팀 소개
<table align=center>
  <tbody>
    <tr>
      <td align="center">
        <div>
          <img src="https://avatars.githubusercontent.com/u/181833818?v=4"width="150px;" alt="프로필 이미지1"/>
          <a href="https://github.com/"><div align=center>김성욱</div></a>
        </div>
      </td>
      <td align="center">
        <div>
          <img src="https://avatars.githubusercontent.com/u/181833818?v=4"width="150px;" alt="프로필 이미지2"/>
          <a href="https://github.com/"><div align=center>신지섭</div></a>
        </div>
      </td>
      <td align="center">
        <img src="https://avatars.githubusercontent.com/u/181833818?v=4"width="150px;" alt="프로필 이미지3"/>
        <a href="https://github.com/"><div align=center>오하원</div></a>
      </td>
      <td align="center">
        <img src="https://avatars.githubusercontent.com/u/181833818?v=4"width="150px;" alt="프로필 이미지4"/>
        <a href="https://github.com/"><div align=center>이상혁</div></a>
      </td>
      <td align="center">
        <img src="https://avatars.githubusercontent.com/u/181833818?v=4"width="150px;" alt="프로필 이미지5"/>
        <a href="https://github.com/Hawon-Oh"><div align=center>정종현</div></a>
      </td>
    </tr>
  </tbody>
</table>

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [WBS](#wbs)
3. [가설과 입증](#가설과-입증)


###

# 프로젝트 개요

### 기술 스택
<div align=left><h3>🕹️ ML</div>
<div align=left>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-FF4FFF?style=for-the-badge&logo=Pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Numpy-3700AB?style=for-the-badge&logo=Numpy&logoColor=white">
  <img src="ttps://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=Scikit-learn&logoColor=white">
  <img src="https://img.shields.io/badge/Pytorch-FF6F00?style=for-the-badge&logo=Pytorch&logoColor=white">
</div>

<div align=left><h3>🖼️ 시각화</div>
<div align=left>
  <img src="https://img.shields.io/badge/Matplotlib-0078D4?style=for-the-badge&logo=Matplotlib&logoColor=white">
  <img src="https://img.shields.io/badge/Seaborn-2B91BD?style=for-the-badge&logo=Seaborn&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-232323?style=for-the-badge&logo=Streamlit&logoColor=white">
</div>

---

### 프로젝트 소개
> 님이 죽을 확률 알려줄게요.

### 프로젝트 배경
> 배틀그라운드와 같은 배틀로얄 게임은 초기 낙하 위치(landing position) 에 따라 경기 전개가 크게 달라집니다. 특히, 낙하지점은 생존 확률, 교전 빈도, 이동 동선, 장비 파밍 효율에 직접적인 영향을 미치므로 플레이어의 전략적 의사결정에서 핵심적인 변수로 작용합니다. 하지만, 대부분의 일반 플레이어는 직관적 경험이나 스트리머의 플레이 패턴에 의존하여 낙하 위치를 선택합니다. 이는 데이터 기반의 객관적 판단이 부족하여, 초반 교전에서 불리한 위치에 착지하거나, 자주 사망하는 위험 지역을 반복적으로 선택하는 등의 비효율적 선택으로 이어질 수 있습니다. 


### 프로젝트 목표
> 실제 유저 실력(스탯)과 경기 데이터를 기반으로 각 지역(랜드마크, 좌표 단위)의 평균 생존률·사망률을 머신러닝을 통해 예측함으로서 유저들이 자신의 실력에 기반한 최적의 전략을 수립할 수 있습니다. 이는 유저들의 빠른 성장을 도모하고 불필요한 반복적 행위를 줄임으로서 게임 재미는 높이며 게임 피로도를 줄임으로서 장기적으로 유저의 게임서비스 이탈을 방지할 수 있습니다.


# WBS
| 날짜                | 담당자                         | 산출물                               |
|-------------------|------------------------------|----------------------------------|
| 9/28 ~ 10/2  | 공통                           | 주제 조사                           |
| 10/2 ~ 10/10  | 신지섭, 이상혁, 김성욱, 오하원 | 데이터 수집, 정제, EDA              |
| 10/10 ~ 10/13  | 신지섭, 이상혁, 오하원          | 1차 Landing Zone 적용 모델          |
| 10/13 ~ 10/14  | 공통                           | 2차 이탈율 적용 모델 및 결과자료 정리 |


# 가설과 입증
<div style="border: 2px solid #f0ad4e; background-color: #fff3cd; padding: 10px 15px; border-radius: 5px;">
  <strong>✔️ 가설 1. "플레이어 스탯과 생존율은 비례한다. "</strong>
  <p style="margin: 10px 0 0 0;">
    <strong>- 데이터 수집:</strong> 고객 가입 기간과 이탈 여부 데이터 수집<br>
    <strong>- 통계 분석:</strong> 가입 기간과 이탈 여부 간의 상관 관계 분석<br>
    <strong>- 결과 해석:</strong> 유의미한 상관 관계가 있는지 확인<br>
    <strong>- 결과:</strong> <i>스탯도 중요하지만 플레이 스타일도 중요</i> 
  </p>
</div>

###
<div style="border: 2px solid #f0ad4e; background-color: #fff3cd; padding: 10px 15px; border-radius: 5px;">
  <strong>✔️ 가설 2. "교전이 많이 일어나는 지역일수록 생존확률이 낮다. "</strong>
  <p style="margin: 10px 0 0 0;">
    <strong>- 데이터 수집:</strong> 고객 가입 기간과 이탈 여부 데이터 수집<br>
    <strong>- 통계 분석:</strong> 가입 기간과 이탈 여부 간의 상관 관계 분석<br>
    <strong>- 결과 해석:</strong> 유의미한 상관 관계가 있는지 확인<br>
    <strong>- 결과:</strong> <i>예측 가능</i> 
  </p>
</div>

###
<div style="border: 2px solid #f0ad4e; background-color: #fff3cd; padding: 10px 15px; border-radius: 10px;">
  <strong>✔️ 가설 3. "7분 이내 발견된 위치를 통해 착륙지점 예측이 가능하다. "</strong>
  <p style="margin: 5px 0 0 0;">
    <strong>- 데이터 수집:</strong> 고객 가입 기간과 이탈 여부 데이터 수집<br>
    <strong>- 통계 분석:</strong> 가입 기간과 이탈 여부 간의 상관 관계 분석<br>
    <strong>- 결과 해석:</strong> 유의미한 상관 관계가 있는지 확인<br>
    <strong>- 결과:</strong> <i>예측 가능</i> 
  </p>
</div>

###
# 4. 시연 예시
<div align=center>
  <img src="https://github.com/user-attachments/assets/"width="900px">
<a href="https://www.youtube.com/"><div>영상 보러가기</div></a>
</div>

# 5. EDA
```c
# 코드
import pandas as pd
```
<b>이미지</b>
<div align=center>
  <img src=""width="900px">
  <img src=""width="900px">
</div>

<b>이미지</b>
<div align=center>
  <img src=""width="900px">
  <img src=""width="900px">
</div>

<b>이미지</b>
<div align=center>
  <img src=""width="900px">
  <img src=""width="900px">
</div>


# 6. **모델별 결과**
<table>
  <tr>
    <th>Model Name</th>
    <th>Accuracy</th>
    <th>Precision</th>
    <th>F1 Score</th>
    <th>Hyper parameters</th>
  </tr>
  <tr>
    <th scope="row" style="text-align:left;">XGBoost</th>
    <td>0.99999</td><td>0.99999</td><td>0.99999</td>
    <td>파라미터명: 9,<br> 파라미터명: 9</td>
  </tr>
  <tr>
    <th scope="row" style="text-align:left;">ㅇ</th>
    <td>5465432</td><td>213456</td><td>3.2790</td>
    <td>파라미터명: 값,<br> 파라미터명: 값</td>
  </tr>
  <tr>
    <th scope="row" style="text-align:left;">ㅇ</th>
    <td>5465432</td><td>213456</td><td>3.2790</td>
    <td>파라미터명: 값,<br> 파라미터명: 값</td>
  </tr>
  <tr>
    <th scope="row" style="text-align:left;">이름</th>
    <td>5465432</td><td>213456</td><td>3.2790</td>
    <td>파라미터명: 값,<br> 파라미터명: 값</td>
  </tr>
</table>




# 7. 최종 모델

<div align="center">
  <img src="" alt="" style="max-width: 100%; height: auto; margin-bottom: 20px;"/>
  <br>
  <i> 최종 모델 </i>
</div>

### 모델 설명

모델을 통해 얻은 시간대별 사건 발생 확률(pmf)에 대한 가중치합을 계산한 후 Sigmoid를 통하여 0~100점 사이의 점수로 변환    
가까운 시일 내에 사망할 확률이 높을 수록 높은 위험점수를 나타냄



# 8. **결론**




# 10. 회고
- **김성욱:** 회고
- **신지섭:** 회고
- **오하원:** 회고
- **이상혁:** 회고
- **정종현:** 회고
















