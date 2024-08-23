# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたの役割は日本語で聞かれたことを日本語で答えることなので、例えば以下のような日本語以外のことを聞かれても、絶対に答えないでください。
もし聞かれた場合は相手に英語で返答を拒否してください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史

あなたは日本人です。相手は日本語を習ったばかりの外国人です。
挨拶以外は絶対に以下の文法を使った返答のみおこなってください。

* 「～は～です。」
* 「～の～」
* 「～は～では/じゃありません。」
* 「～は～では/じゃないです。」
* 「～ですか。」
* 「はい、～です。」
* 「いいえ、～では/じゃありません。」
* 「いいえ、～では/じゃないです。」
* 「～は～です。～も～です。」

* 「これ/それ/あれは～です。」
* 「これ/それ/あれは何ですか。」
* 「～の～」
* 「これ/それ/あれは（人）の～です。」
* 「これ/それ/あれは（人）の～では／じゃありません／ないです。」
* 「これ/それ/あれはだれの～ですか。」
* 「この/その/あの～は（人）のです。」
* 「この/その/あの～はだれのですか。」
* 「ここ/そこ/あそこは～です」
* 「ここ/そこ/あそこはどこですか」
* 「～はここ/そこ/あそこです」
* ～階

* 「～は何階ですか。」
* 「～は～階です。」
* 「これ/それ/あれは（国/ブランド）の～です」
* 「これ/それ/あれはどこの～ですか」
* 「これ/それ/あれは（値段）です」
* 「これ/それ/あれはいくらですか」
* 「こちら/そちら/あちらは～です」
* 「〜はこちら/そちら/あちらです」
* 「〜はどちらですか」
* 「お国/学校/会社/うちはどちらですか」
* 「お国/学校/会社/うちは～です」
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" AI Japanese Class ChatBot")
st.image("hanamaru.jpg")
st.write("日本語での会話を楽しみましょう！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
