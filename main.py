import streamlit as st
import re
import html


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="두근두근 이름궁합 💕",
    page_icon="💕",
    layout="centered"
)


# =========================================================
# 한글 획수
# =========================================================

CHO_STROKES = {
    "ㄱ": 1, "ㄲ": 2, "ㄴ": 1, "ㄷ": 2, "ㄸ": 4,
    "ㄹ": 3, "ㅁ": 4, "ㅂ": 4, "ㅃ": 8, "ㅅ": 2,
    "ㅆ": 4, "ㅇ": 1, "ㅈ": 2, "ㅉ": 4, "ㅊ": 3,
    "ㅋ": 2, "ㅌ": 3, "ㅍ": 4, "ㅎ": 3
}

JUNG_STROKES = {
    "ㅏ": 2, "ㅐ": 3, "ㅑ": 3, "ㅒ": 4, "ㅓ": 2,
    "ㅔ": 3, "ㅕ": 3, "ㅖ": 4, "ㅗ": 2, "ㅘ": 4,
    "ㅙ": 5, "ㅚ": 3, "ㅛ": 3, "ㅜ": 2, "ㅝ": 4,
    "ㅞ": 5, "ㅟ": 3, "ㅠ": 3, "ㅡ": 1, "ㅢ": 2,
    "ㅣ": 1
}

JONG_STROKES = {
    "": 0, "ㄱ": 1, "ㄲ": 2, "ㄳ": 3, "ㄴ": 1,
    "ㄵ": 3, "ㄶ": 4, "ㄷ": 2, "ㄹ": 3, "ㄺ": 4,
    "ㄻ": 7, "ㄼ": 7, "ㄽ": 5, "ㄾ": 6, "ㄿ": 7,
    "ㅀ": 6, "ㅁ": 4, "ㅂ": 4, "ㅄ": 6, "ㅅ": 2,
    "ㅆ": 4, "ㅇ": 1, "ㅈ": 2, "ㅊ": 3, "ㅋ": 2,
    "ㅌ": 3, "ㅍ": 4, "ㅎ": 3
}


# =========================================================
# 한글 분해 목록
# =========================================================

CHO_LIST = [
    "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ",
    "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
    "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ",
    "ㅋ", "ㅌ", "ㅍ", "ㅎ"
]

JUNG_LIST = [
    "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ",
    "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
    "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ",
    "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ",
    "ㅣ"
]

JONG_LIST = [
    "", "ㄱ", "ㄲ", "ㄳ", "ㄴ",
    "ㄵ", "ㄶ", "ㄷ", "ㄹ",
    "ㄺ", "ㄻ", "ㄼ", "ㄽ",
    "ㄾ", "ㄿ", "ㅀ", "ㅁ",
    "ㅂ", "ㅄ", "ㅅ", "ㅆ",
    "ㅇ", "ㅈ", "ㅊ", "ㅋ",
    "ㅌ", "ㅍ", "ㅎ"
]


# =========================================================
# 한글 한 글자의 획수
# =========================================================

def get_korean_stroke(char):

    code = ord(char)

    if 0xAC00 <= code <= 0xD7A3:

        index = code - 0xAC00

        cho_index = index // 588
        jung_index = (index % 588) // 28
        jong_index = index % 28

        cho = CHO_LIST[cho_index]
        jung = JUNG_LIST[jung_index]
        jong = JONG_LIST[jong_index]

        return (
            CHO_STROKES[cho]
            + JUNG_STROKES[jung]
            + JONG_STROKES[jong]
        )

    return 0


# =========================================================
# 이름 → 숫자
# =========================================================

def name_to_numbers(name):

    numbers = []

    for char in name:

        if "가" <= char <= "힣":

            numbers.append(
                get_korean_stroke(char)
            )

    return numbers


# =========================================================
# 궁합 계산
# =========================================================

def calculate_compatibility(name1, name2):

    combined_name = name1 + name2

    numbers = name_to_numbers(
        combined_name
    )

    if len(numbers) < 2:
        return None

    history = [numbers[:]]

    current = numbers[:]

    while len(current) > 2:

        next_numbers = []

        for i in range(len(current) - 1):

            value = (
                current[i] + current[i + 1]
            ) % 10

            next_numbers.append(value)

        current = next_numbers

        history.append(current[:])

    score = (
        current[0] * 10
        + current[1]
    )

    # 100점 특별 처리
    is_perfect = False

    if name1 == name2:
        score = 100
        is_perfect = True

    elif score == 99:
        score = 100
        is_perfect = True

    return {
        "score": score,
        "numbers": numbers,
        "history": history,
        "is_perfect": is_perfect
    }


# =========================================================
# 일반 결과 문구
# =========================================================

def get_result_text(score):

    if score >= 95:
        return (
            "운명급 궁합! 💍",
            "이 정도면 이름부터 서로를 찾고 있었던 수준이에요."
        )

    elif score >= 85:
        return (
            "천생연분 💕",
            "서로의 텐션이 아주 잘 맞는 조합이에요!"
        )

    elif score >= 75:
        return (
            "찰떡궁합 💗",
            "같이 있으면 은근히 계속 웃게 되는 사이예요."
        )

    elif score >= 65:
        return (
            "꽤 잘 맞는 사이 ✨",
            "서로 다른 점도 있지만 그게 오히려 매력이 될 수 있어요."
        )

    elif score >= 50:
        return (
            "가능성 있음 👀",
            "조금만 더 가까워지면 의외의 케미가 생길지도?"
        )

    elif score >= 35:
        return (
            "묘하게 신경 쓰이는 사이 💭",
            "완전히 안 맞는 것도 아니고… 뭔가 있네요."
        )

    elif score > 20:
        return (
            "조금 애매한 사이 🤔",
            "서로를 조금 더 알아가는 시간이 필요해 보여요."
        )

    else:
        return (
            "관계를 재고해보세요... 😶",
            "이름궁합 결과가 상당히 심각합니다."
        )


# =========================================================
# CSS
# =========================================================

st.html("""
<style>

.stApp {

    background:
        radial-gradient(
            circle at 50% 0%,
            #fff0f7 0%,
            #ffe6f0 25%,
            #fff8fb 60%,
            #ffffff 100%
        );

    color: #333333;
}

.block-container {

    max-width: 700px;

    padding-top: 45px;
    padding-bottom: 80px;
}


/* ===============================
   제목
   =============================== */

.title {

    text-align: center;

    color: #ff4f91;

    font-size: 38px;

    font-weight: 900;

    letter-spacing: -2px;

    margin-bottom: 6px;
}

.subtitle {

    text-align: center;

    color: #a47a8b;

    font-size: 14px;

    margin-bottom: 35px;
}


/* ===============================
   입력 카드
   =============================== */

.input-card {

    background:
        rgba(255,255,255,0.92);

    border:
        1px solid #ffd0e1;

    border-radius: 25px;

    padding: 28px;

    box-shadow:
        0 12px 35px rgba(255,100,160,0.12);

    margin-bottom: 20px;
}


/* ===============================
   하트
   =============================== */

.heart {

    text-align: center;

    font-size: 34px;

    color: #ff4f91;

    margin: 2px 0 5px 0;

    animation:
        heartBeat 1.2s infinite;
}

@keyframes heartBeat {

    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.15);
    }

    100% {
        transform: scale(1);
    }
}


/* ===============================
   버튼
   =============================== */

div.stButton > button {

    width: 100%;

    border: none;

    border-radius: 18px;

    padding: 14px;

    background:
        linear-gradient(
            135deg,
            #ff5c9a,
            #ff78ac
        );

    color: white;

    font-size: 17px;

    font-weight: 800;

    box-shadow:
        0 8px 20px rgba(255,82,145,0.25);

    transition:
        transform 0.2s,
        box-shadow 0.2s;
}

div.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 12px 25px rgba(255,82,145,0.35);
}


/* ===============================
   일반 결과 카드
   =============================== */

.result-card {

    background: white;

    border-radius: 28px;

    padding: 30px 24px;

    text-align: center;

    box-shadow:
        0 15px 45px rgba(255,100,160,0.16);

    border:
        1px solid #ffd8e6;

    margin-top: 30px;
}

.result-names {

    color: #777777;

    font-size: 17px;

    margin-bottom: 15px;
}

.score {

    font-size: 72px;

    font-weight: 900;

    color: #ff4f91;

    line-height: 1;

    margin: 15px 0;
}

.result-title {

    font-size: 22px;

    font-weight: 900;

    color: #333333;

    margin-top: 12px;
}

.result-description {

    color: #888888;

    font-size: 14px;

    margin-top: 8px;

    line-height: 1.7;
}


/* ===============================
   100점 카드
   =============================== */

.perfect-card {

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #fff0f7,
            #ffe0ed
        );

    border:
        3px solid #ff6da5;

    border-radius: 30px;

    padding: 40px 24px;

    text-align: center;

    margin-top: 30px;

    box-shadow:
        0 0 0 6px rgba(255,109,165,0.10),
        0 20px 55px rgba(255,80,145,0.30);
}

.perfect-heart {

    font-size: 48px;

    animation:
        heartBeat 0.8s infinite;
}

.perfect-small {

    color: #ff5795;

    font-size: 12px;

    font-weight: 900;

    letter-spacing: 4px;

    margin-top: 10px;
}

.perfect-score {

    color: #ff3f89;

    font-size: 86px;

    font-weight: 1000;

    line-height: 1;

    margin: 12px 0;
}

.perfect-title {

    color: #333333;

    font-size: 25px;

    font-weight: 900;
}

.perfect-description {

    color: #888888;

    font-size: 14px;

    line-height: 1.8;

    margin-top: 10px;
}


/* ===============================
   해골 결과
   =============================== */

.skull-overlay {

    background:
        linear-gradient(
            135deg,
            #202020,
            #090909
        );

    border:
        3px solid #555555;

    border-radius: 30px;

    padding: 38px 22px;

    text-align: center;

    margin-top: 30px;

    box-shadow:
        0 20px 55px rgba(0,0,0,0.35);
}

.skull-icon {

    font-size: 85px;

    line-height: 1;

    animation:
        skullShake 0.5s infinite;
}

@keyframes skullShake {

    0% {
        transform: rotate(0deg);
    }

    25% {
        transform: rotate(-4deg);
    }

    50% {
        transform: rotate(4deg);
    }

    75% {
        transform: rotate(-4deg);
    }

    100% {
        transform: rotate(0deg);
    }
}

.skull-small {

    color: #aaaaaa;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 3px;

    margin-top: 12px;
}

.skull-score {

    color: #ffffff;

    font-size: 70px;

    font-weight: 900;

    line-height: 1;

    margin: 10px 0;
}

.skull-title {

    color: #ffffff;

    font-size: 24px;

    font-weight: 900;

    margin-top: 12px;
}

.skull-description {

    color: #aaaaaa;

    font-size: 14px;

    line-height: 1.8;

    margin-top: 10px;
}


/* ===============================
   20점 이하 경고
   =============================== */

.warning-card {

    background:
        #fff7f9;

    border:
        2px solid #ffb7cb;

    border-radius: 24px;

    padding: 25px;

    text-align: center;

    margin-top: 30px;

    box-shadow:
        0 12px 30px rgba(255,100,150,0.12);
}

.warning-title {

    color: #ff4f91;

    font-size: 22px;

    font-weight: 900;
}

.warning-description {

    color: #888888;

    font-size: 14px;

    margin-top: 8px;
}


/* ===============================
   계산 과정
   =============================== */

.process-card {

    background:
        #fff8fb;

    border:
        1px solid #ffdce9;

    border-radius: 20px;

    padding: 20px;

    margin-top: 20px;

    text-align: center;
}

.process-label {

    color: #ff6b9f;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 2px;

    margin-bottom: 15px;
}

.process-line {

    color: #555555;

    font-size: 18px;

    letter-spacing: 5px;

    margin: 8px 0;
}

.final-line {

    color: #ff4f91;

    font-weight: 900;
}


/* ===============================
   안내 문구
   =============================== */

.notice {

    text-align: center;

    color: #b08b99;

    font-size: 11px;

    margin-top: 28px;
}

</style>
""")


# =========================================================
# 제목
# =========================================================

st.html("""
<div class="title">
    두근두근 이름궁합 💕
</div>

<div class="subtitle">
    이름만 입력하면 우리의 궁합을 알아볼 수 있어요!
</div>
""")


# =========================================================
# 이름 입력
# =========================================================

st.html("""
<div class="input-card">
""")

name1 = st.text_input(
    "💗 첫 번째 이름",
    placeholder="이름을 입력하세요",
    max_chars=10
)

st.html("""
<div class="heart">
    ♥
</div>
""")

name2 = st.text_input(
    "💗 두 번째 이름",
    placeholder="상대방 이름을 입력하세요",
    max_chars=10
)

st.html("""
</div>
""")


# =========================================================
# 버튼
# =========================================================

check = st.button(
    "💘 우리 궁합 확인하기"
)


# =========================================================
# 결과
# =========================================================

if check:

    name1 = re.sub(
        r"\s+",
        "",
        name1
    )

    name2 = re.sub(
        r"\s+",
        "",
        name2
    )


    # -----------------------------------------------------
    # 이름 미입력
    # -----------------------------------------------------

    if not name1 or not name2:

        st.warning(
            "두 사람의 이름을 모두 입력해주세요! 💕"
        )


    # -----------------------------------------------------
    # 한글 확인
    # -----------------------------------------------------

    elif (
        not re.search("[가-힣]", name1)
        or
        not re.search("[가-힣]", name2)
    ):

        st.warning(
            "한글 이름을 입력해주세요! 🥰"
        )


    else:

        result = calculate_compatibility(
            name1,
            name2
        )


        if result is None:

            st.warning(
                "계산할 수 있는 한글 이름을 입력해주세요!"
            )


        else:

            score = result["score"]


            # =================================================
            # 100점
            # =================================================

            if result["is_perfect"]:

                st.html(
                    f"""
                    <div class="perfect-card">

                        <div class="perfect-heart">
                            💕
                        </div>

                        <div class="perfect-small">
                            PERFECT MATCH
                        </div>

                        <div class="perfect-score">
                            100%
                        </div>

                        <div class="perfect-title">
                            💍 운명의 상대 발견!
                        </div>

                        <div class="perfect-description">
                            {html.escape(name1)}
                            ❤️
                            {html.escape(name2)}
                            <br><br>
                            두 이름이 완벽하게 맞아떨어졌어요!
                            <br>
                            이 조합은 오늘의 주인공입니다 ✨
                        </div>

                    </div>
                    """
                )


            # =================================================
            # 15점 이하
            # =================================================

            elif score <= 15:

                st.html(
                    f"""
                    <div class="skull-overlay">

                        <div class="skull-icon">
                            💀
                        </div>

                        <div class="skull-small">
                            DANGER LEVEL
                        </div>

                        <div class="skull-score">
                            {score}%
                        </div>

                        <div class="skull-title">
                            전생에 원수졌나요?
                        </div>

                        <div class="skull-description">
                            {html.escape(name1)}
                            ×
                            {html.escape(name2)}
                            <br><br>
                            이 정도면 우주가 둘 사이를
                            말리고 있는 수준이에요... 💀
                        </div>

                    </div>
                    """
                )


            # =================================================
            # 16~20점
            # =================================================

            elif score <= 20:

                st.html(
                    f"""
                    <div class="warning-card">

                        <div class="warning-title">
                            ⚠️ 관계를 재고해보세요...
                        </div>

                        <div class="warning-description">
                            {html.escape(name1)}
                            ×
                            {html.escape(name2)}
                            <br><br>
                            궁합 점수는
                            <b>{score}%</b>입니다.
                            <br>
                            신중한 접근이 필요해 보여요... 🤔
                        </div>

                    </div>
                    """
                )


            # =================================================
            # 일반 결과
            # =================================================

            else:

                title, description = get_result_text(
                    score
                )

                st.html(
                    f"""
                    <div class="result-card">

                        <div class="result-names">
                            {html.escape(name1)}
                            💕
                            {html.escape(name2)}
                        </div>

                        <div class="score">
                            {score}%
                        </div>

                        <div class="result-title">
                            {html.escape(title)}
                        </div>

                        <div class="result-description">
                            {html.escape(description)}
                        </div>

                    </div>
                    """
                )


            # =================================================
            # 계산 과정
            # =================================================

            st.html("""
            <div class="process-card">

                <div class="process-label">
                    💕 NAME MATCHING PROCESS
                </div>
            """)

            for index, row in enumerate(
                result["history"]
            ):

                number_text = "   ".join(
                    str(x)
                    for x in row
                )

                if index == len(
                    result["history"]
                ) - 1:

                    st.html(
                        f"""
                        <div class="process-line final-line">
                            {number_text}
                        </div>
                        """
                    )

                else:

                    st.html(
                        f"""
                        <div class="process-line">
                            {number_text}
                        </div>
                        """
                    )

            st.html("""
            </div>
            """)


            # =================================================
            # 안내
            # =================================================

            st.html("""
            <div class="notice">
                ※ 재미로 보는 이름궁합 테스트예요 💗
            </div>
            """)
