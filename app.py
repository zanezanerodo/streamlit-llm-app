from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from langchain_openai import ChatOpenAI 
from langchain.schema import HumanMessage, SystemMessage 

# ページ設定
st.set_page_config(
    page_title="プログラミングアシスター",
    layout="wide"
)

def get_system_message(expert_mode):
    """専門家モードに応じたシステムメッセージを返す"""
    if expert_mode == "VSCode Expert":
        return """あなたはVSCodeの専門家です。以下の役割で回答してください：
        
        - VSCodeの機能、拡張機能、設定、ショートカット、デバッグ方法に精通
        - VSCode特有の開発ワークフローやベストプラクティスを提案
        - VSCodeの環境設定やカスタマイズ方法を具体的に説明
        - 複数言語でのVSCode活用法を理解
        - 常に実践的で具体的なアドバイスを提供
        - 必要に応じてVSCode固有のJSON設定例やコマンド例を示す
        
        回答は分かりやすく、実際にVSCodeで試せる形で提供してください。"""
        
    else:  # Google Colab Expert
        return """あなたはGoogle Colabの専門家です。以下の役割で回答してください：
        
        - Google Colabの機能、制限、最適化手法に精通
        - Colabでのライブラリインストール、GPU/TPU活用法を理解
        - Colabノートブックの共有、保存、バージョン管理に詳しい
        - Colab特有の環境での機械学習、データ分析のベストプラクティスを提案
        - ColabとGoogleドライブ、BigQueryなどとの連携方法を理解
        - メモリ制限やセッション切断への対処法を提案
        
        回答は実際にColabで実行可能なコード例を含め、Colab環境の特性を考慮した実践的なアドバイスを提供してください。"""
    

def call_llm_with_expert_mode(input_text,expert_mode):
    """
    入力テキストと専門家モードを受け取り、LLMの応答を返す
    
    Args:
        input_text (str): ユーザーの入力テキスト
        expert_mode (str): 選択された専門家モード
    
    Returns:
        str: LLMからの回答
    """
    try:
        # OpenAI APIキーの確認
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key: 
            return "⚠️ OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYを設定してください。"
        
        # LLMモデルの初期化
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.4,
            openai_api_key=api_key
        )
        
        # システムメッセージの取得
        system_message = get_system_message(expert_mode)
        
        # メッセージの作成
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=input_text)
        ]
        
        # LLMへの問い合わせ
        response = llm(messages)
        
        return response.content
    
    except Exception as e:
        return f"⚠️ エラーが発生しました: {str(e)}"
    
def main():
    """メインアプリケーション"""

    # アプリケーションタイトル
    st.title("プログラムアシスター")

    #アプリケーションの概要と説明
    with st.expander("アプリについて・説明", expanded=True):
        st.markdown("""
        ### 📋 概要
        このアプリは、プログラミングに関する質問に特化したAIアシスタントです。
        LangChain経由でLLMを呼び出し、選択した専門家モードに応じて最適な回答を提供します。
        
        ### 🚀 使い方
        1. **専門家モードを選択**: VSCodeまたはGoogle Colabの専門家を選択
        2. **質問を入力**: 下のテキストエリアに質問や相談内容を入力
        3. **送信**: 「質問する」ボタンをクリック
        4. **回答を確認**: AI専門家からの回答が表示されます
        
        ### 💡 質問例
        - **VSCode**: 「Pythonのデバッグ設定を教えて」「便利な拡張機能は？」
        - **Colab**: 「GPUを使った機械学習の始め方は？」「大容量データの処理方法は？」
        """)
    

    # 専門家モード選択
    st.subheader("専門家モード選択")
    expert_mode= st.radio(
        "どちらの専門家に質問しますか？",
        options=["VSCode Expert", "Google Colab Expert"],
        help="選択した専門家の知識に基づいて回答します"
        )
    # 選択されたモードの説明
    if expert_mode == "VSCode Expert":
        st.info("🔧 VSCodeの機能、拡張機能、設定、開発ワークフローについて専門的にサポートします")
    else:
        st.info("💻 Google Colabの機能、ライブラリ、データ処理について専門的にサポートします"   )

    #　質問入力フォーム
    st.subheader("質問を入力")
    input_text = st.text_area(
        "質問内容",
        placeholder=f"{'VScode' if expert_mode == 'VSCode Expert' else 'Googole Colab'}について質問してください...",
        height=120
    )

    # 実行ボタン
    if st.button("質問する"):
        if not input_text.strip():
            st.warning("質問内容を入力してください")
        else:
            with st.spinner("専門家が回答を考えています..."):
                # LLM呼び出し
                answer = call_llm_with_expert_mode(input_text, expert_mode)

                # 回答表示
                st.subheader("専門家からの回答")
                st.markdown(answer)


if __name__ == "__main__":
    main()
    