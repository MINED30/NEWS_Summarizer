# NEWS_Summarizer
KoBART domain-adaptive pretraining with Extracted Gap-sentences (PEGASUS) for Abstractive Summarization



１)            외부 데이터 사용 시, 해당 데이터 및 전처리 코드(출처 표기, 크롤링시 크롤링 코드 추가)
- 외부데이터
  -  `./NAVER_NEWS_LINK/` 에 출처 링크 수록  
  - 파일명은 `./NAVER_NEWS_LINK/LinkList_<year>_<keyword>_<num_of_links>.txt`을 따름
- 크롤링코드
  - 링크수집코드 : A_Link_collector.py
  - 크롤링코드 : B_Crawling.py

２)            모델 생성 및 학습 코드
- Rouge Score활용한 Gapsentence Generation : D_Gapsentence_generation.ipynb
- GSG기반 Pretraining  : E_Pretraining_step.ipynb
- Finetuning  : F_Finetuning_step.ipynb

３)            추론(예측) 코드
- Prediction  : G_Prediction.ipynb

４)            리더보드 점수 복원이 가능한 모델
- Demonstration  : H_Demo_Summarizer.ipynb

５)            개발 환경
- colab환경
- 추가된 라이브러리 : transformers, hanja, wandb