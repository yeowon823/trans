import streamlit as st
from deep_translator import GoogleTranslator

# 페이지 기본 설정
st.set_page_config(page_title="다국어 번역기", page_icon="🌐")

st.title("한글 다국어 번역기 🌐")
st.write("한국어를 🇺🇸영어, 🇨🇳중국어, 🇯🇵일본어로 동시에 번역해 줍니다.")

# 사용자 입력 받기
text_to_translate = st.text_area("번역할 한국어 텍스트를 입력하세요:", placeholder="여기에 입력...")

# 번역 버튼
if st.button("번역하기"):
    if text_to_translate.strip():
        with st.spinner("번역 중... 잠시만 기다려주세요!"):
            try:
                # 번역 실행
                eng_translation = GoogleTranslator(source='ko', target='en').translate(text_to_translate)
                zh_translation = GoogleTranslator(source='ko', target='zh-CN').translate(text_to_translate)
                ja_translation = GoogleTranslator(source='ko', target='ja').translate(text_to_translate)

                st.success("번역 완료!")
                
                # 결과 출력
                st.subheader("🇺🇸 영어 (English)")
                st.info(eng_translation)
                
                st.subheader("🇨🇳 중국어 (Chinese)")
                st.info(zh_translation)
                
                st.subheader("🇯🇵 일본어 (Japanese)")
                st.info(ja_translation)
                
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
    else:
        st.warning("먼저 번역할 텍스트를 입력해 줘!")
