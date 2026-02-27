import discord
from discord.ext import commands
from dotenv import load_dotenv
import subprocess
import os

import zeroclaw
from zeroclaw import Client

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
model = os.getenv('ZEROCLAW_MODEL')
gemini_key = os.getenv('GEMINI_API_KEY')

# ZeroClaw 클라이언트 초기화 (데몬과 통신)
client = ClawClient(api_key=token)
# 1. 디스코드 봇 설정
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 2. ZeroClaw 및 서버 정보 확인 함수
def get_gpu_status():
    try:
        # nvidia-smi를 통해 GPU 상태 추출
        result = subprocess.check_output(
            ['nvidia-smi', 
             '--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total', 
             '--format=csv,noheader,nounits']
        )
        infos = result.decode('utf-8').strip().split(',')
        return {
            "name": infos[0],
            "temp": infos[1],
            "util": infos[2],
            "mem_used": infos[3],
            "mem_total": infos[4]
        }
    except Exception as e:
        return None

# 3. 봇 이벤트: 준비 완료
@bot.event
async def on_ready():
    print(f'✅ ZeroClaw 연동 봇 로그인 성공: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="DGX Spark 모니터링"))

# 4. 명령어: GPU 상태 확인
@bot.command(name="상태")
async def status(ctx):
    gpu = get_gpu_status()
    if gpu:
        embed = discord.Embed(title="🚀 DGX Spark GPU 상태", color=0x7289da)
        embed.add_field(name="모델명", value=gpu['name'], inline=False)
        embed.add_field(name="온도", value=f"{gpu['temp']}°C", inline=True)
        embed.add_field(name="사용률", value=f"{gpu['util']}%", inline=True)
        embed.add_field(name="메모리", value=f"{gpu['mem_used']} / {gpu['mem_total']} MiB", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ GPU 정보를 가져올 수 없습니다. 드라이버를 확인하세요.")

# 5. 명령어: ZeroClaw 분석 실행 (예시: 부산 사업체 데이터)
@bot.command(name="분석")
async def analyze(ctx, region="수영구"):
    await ctx.send(f"📊 ZeroClaw를 통해 **부산 {region}** 사업체 데이터를 분석 중입니다...")
    
    # 여기에 실제 zeroclaw 라이브러리를 활용한 분석 로직을 추가하세요.
    # 예: result = zeroclaw.analyze(data_path, region)
    
    await ctx.send(f"✅ {region} 분석 완료! (결과 시각화 이미지는 곧 업데이트 됩니다.)")

# 6. 봇 실행
# 주의: 토큰은 절대 외부에 노출하지 마세요!

@bot.command(name="질문")
async def ask_gemini(ctx, *, prompt):
    await ctx.send("🤖 Gemini가 서버 자원을 활용해 생각 중입니다...")
    
    # ZeroClaw를 통해 Gemini에게 작업 지시
    # 예: "부산 수영구 사업체 데이터를 분석해서 요약해줘"
    response = client.chat(
        model=gemini_key,
        message=prompt
    )
    
    await ctx.send(f"✅ **답변:**\n{response.text}")
    
    
bot.run(token)