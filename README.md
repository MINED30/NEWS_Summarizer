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

## 알고리즘 설명

 **가설 : Pretraining이 Down Stream Task와 비슷할 수록 더 좋은 성능을 낼 것이다.**

구글에서 발표한 *PEGASUS : Pre-training with Extracted Gap-sentences for Abastractive Summarization* 논문에서는 기존 Transformer에 Gap-sentences을 활용한 Pretraining 방법만으로 Abstractive Summarization에서 SOTA를 달성하였다. Gap-sentence generation 방법론을 한국어 요약 task에도 적용해보고자 하는 것이 이번 프로젝트의 목표이다.

### Pretraining
1. ROUGE SCORE를 통해 가장 중요한 문장을 뽑아 <GSG>로 마스킹한다
    - 각 문장별로 해당 문단에서의 나머지 문장과 Rouge Score를 구한다
    - Rouge Score가 가장 높은 문장이 중요한 문장이라고 가정한다
    - 마스킹하는 비율은 30%로 설정하였다
2. 제한된 자원으로 이미 훈련된 모델을 사용하였다
    - 기존에 요약 TASK에 성능이 좋은 것으로 알려져있는 BART를 고려하였다
    - SKT에서 배포한 KoBART를 사용하여 사전학습을 하였다
    - <GSG> 마스킹이 된 문단 전체가 입력되고, 모델은 <GSG>모형을 맞추도록 훈련된다
  
### Finetuning
1. AIHUB에서 제공하는 데이터로 finetuning하였다
    - 입력은 문단이 들어가고, GOLD LABEL을 타겟으로 훈련을 진행하였다
  
### PEGASUS 방법론에대한 추가설명
본인이 2021.10.22에 PEGASUS 논문을 발표한 영상입니다.
https://www.youtube.com/watch?v=14DYRVWFZTs
  
## Reference

- [https://github.com/SKT-AI/KoBART](https://github.com/SKT-AI/KoBART)

- [https://github.com/SKT-AI/KoGPT2](https://github.com/SKT-AI/KoGPT2)

- [https://dacon.io/competitions/official/235813/overview/description](https://dacon.io/competitions/official/235813/overview/description)

- [https://dacon.io/competitions/official/235829/overview/description](https://dacon.io/competitions/official/235829/overview/description)

- Gururangan, S., Marasović, A., Swayamdipta, S., Lo, K., Beltagy, I., Downey, D., & Smith, N. A. (2020). *Don’t Stop Pretraining: Adapt Language Models to Domains and Tasks*. http://arxiv.org/abs/2004.10964

- Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O., Stoyanov, V., Zettlemoyer, L., & Ai, F. (n.d.). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension*. https://huggingface.co/transformers

- Zhang, J., Zhao, Y., Saleh, M., & Liu, P. J. (2019). *PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization*. http://arxiv.org/abs/1912.08777
