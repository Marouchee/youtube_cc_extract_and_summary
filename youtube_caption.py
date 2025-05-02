from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    # https://www.youtube.com/watch?v=영상ID 형태에서 ID만 뽑아내기
    # 1) standard URL: v=VIDEO_ID
    qs = urlparse(url).query
    if qs:
        params = parse_qs(qs)
        if 'v' in params and params['v']:
            return params['v'][0]
    # 2) short URL: youtu.be/VIDEO_ID
    m = re.search(r"youtu\.be/([^?&/]+)", url)
    if m:
        return m.group(1)
    return None

def fetch_captions(video_url: str, languages=['ko','en']) -> str:
    video_id = extract_video_id(video_url)
    if not video_id:
        print("[Error] 잘못된 URL입니다.")
        return ""

    try:
        # 수동/자동 자막 모두 시도
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        # 문장 단위 텍스트만 이어붙이기
        return "\n".join(item['text'] for item in transcript)

    except TranscriptsDisabled:
        print("[Error] 이 영상은 자막 사용이 비활성화되어 있습니다.")
    except NoTranscriptFound:
        print(f"[Error] {languages} 언어 자막을 찾을 수 없습니다.")
    except Exception as e:
        print(f"[Error] {e}")
    return ""