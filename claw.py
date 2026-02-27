import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
# zeroclaw에서 제공하는 도구들을 그대로 가져옵니다.
from zeroclaw_tools import create_agent, shell, file_read, file_write


load_dotenv()


async def main():
    # 1. 환경 변수 확인
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("에러: GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        return

    # 2. OpenAI 호환 주소 대신, 전용 라이브러리를 직접 사용 (에러 원인 원천 차단)
    # create_agent 내부의 llm을 우리가 직접 만든 Gemini 모델로 교체합니다.
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    # 3. zeroclaw_tools의 에이전트 생성 (llm 인자를 직접 전달할 수 있다면 베스트)
    # 만약 create_agent가 llm 객체를 직접 받지 못한다면 아래와 같이 구성합니다.
    agent = create_agent(
        tools=[shell, file_read, file_write],
        model=llm, # 문자열 대신 llm 객체를 직접 전달해 보세요
    )
    
    # 4. 작업 실행
    try:
        result = await agent.ainvoke({
            "messages": [HumanMessage(content="/tmp 디렉토리의 파일 목록을 알려줘")]
        })
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"실행 중 에러 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())