# AI 모델 파일 위치

이 디렉토리에 다음 AI 모델 파일들을 배치해주세요:

## 필요한 파일:

1. **sky3000.h5** - 천간 궁합 분석 모델 (TensorFlow/Keras 모델)
2. **earth3000.h5** - 지지 궁합 분석 모델 (TensorFlow/Keras 모델)  
3. **cal.csv** - 만세력 데이터 파일

## 파일 위치:
```
backend/models/
├── sky3000.h5
├── earth3000.h5
└── cal.csv
```

## 참고:
- 이 파일들은 `app/ai/saju_engine.py`의 `SajuEngine` 클래스에서 사용됩니다
- 파일이 없으면 궁합 분석 API(`/api/analysis/calculate`)가 동작하지 않습니다
- `.env` 파일의 `MODEL_PATH` 설정에서 경로를 변경할 수 있습니다
