![logo5v1](https://user-images.githubusercontent.com/20357655/104316876-2be04600-54ee-11eb-93ed-f9835fde1527.jpg)

# Deep Learning for Audio (DLA)

- Lecture and seminar materials for each week are in `./week*` folders, see `README.md` for materials and instructions
- Any technical issues, ideas, bugs in course materials, contribution ideas - add an issue
- The current version of the course is conducted in **autumn 2024** at the [CS Faculty](https://cs.hse.ru/en/) of [HSE](https://www.hse.ru/en/).

For previous years versions, see [Past Versions](#past-versions) section.

# Syllabus

- [**week01**](./week01) Introduction to Course

  - Lecture: Introduction to Course
  - Seminar: Experiment tracking, `Hydra`, `Git`, `VS code`
  - Self-Study: Introduction to `PyTorch`

- [**week02**](./week02) Introduction to Digital Signal Processing

  - Lecture: Signals, Fourier Transform, spectrograms, MelScale, MFCC
  - Seminar: DSP in practice, spectrogram creation, IRF, frequency filtering

- [**week03**](./week03) Speech Recognition I

  - Lecture: Metrics, Datasets, Connectionist Temporal Classification (CTC), Classic Models, Beam Search, Language models
  - Seminar: Audio Augmentations, Beam Search
  - Q&A Session: Homework discussion, R&D coding tips

- [**week04**](./week04) Speech Recognition II

  - Lecture: LAS, RNN-T, Language models for RNN-T and LAS
  - Seminar: Hybrid RNN-T and CTC model training and inference

- [**week05**](./week05) Guest Lecture. Speech Recognition III and Audio SSL

  - Lecture: Self-Supervised Models for Audio, Audio LLMs

- [**week06**](./week06) Source Separation I

  - Lecture: A review of general Source Separation and Denoising, Encoder-Decoder-Separator architectures, Demucs family, DCCRN, FullSubNet+, BandSplitRNN
  - Seminar: Metrics

- [**week07**](./week07) Source Separation II

  - Lecture: Speech separation, Blind and Target Separation, Recurrent(TasNet, DPRNN, VoiceFilter) and CNN(ConvTasNet, SpEx+)
  - Seminar: WienerFilter, SincFilter and DEMUCS; streaming processing and performance metrics

- [**week08**](./week08) Audio-Visual Deep Learning

  - Lecture: Audio-Visual Fusion, Source Separation, Speech Recognition, and Self-Supervised Models. Wav2Lip and SadTalker (talking face)
  - Q&A: Project and Slurm discussion
  - Extra Seminar: Create Your Own Intelligent Voice Assistant

- [**week09**](./week09) Text to Speech (TTS)

  - Lecture: Tacotron, DeepVoice, GST, FastSpeech, AdaSpeech, Attention Tricks
  - Seminar: postponed

- [**week10**](./week10) Neural Vocoders

  - Lecture: WaveNet, Parallel WaveGAN, WaveGlow, MelGAN, HiFiGAN
  - Seminar: FastSpeech I, TTS pipeline: from text to audio

- [**week11**](./week11) Diffusion-based TTS

  - Lecture: Diffusion concept. Diffusion Vocoders and Diffusion acoustic models.

- [**week12**](./week12) Voice Biometry I

  - Lecture: Introduction. Reverberation. CMs for recorded and synthesized speech detection (LCNN, RawNet2, AASIST). GNNs
  - Seminar: ASVspoof, Sinc-layer, GNN

- [**week13**](./week13) Voice Biometry II

  - Guest Lecture: Kolmogorov-Arnold Networks (KANs), AASIST3, ASVspoof5
  - Lecture: ASV systems. SASV systems. Streaming

- [**week14**](./week14) AI for Music

  - Lecture: Tasks overview, Music Information Retrieval, Music Generation

<!--
-->

# Homeworks and Projects

- [**HW_ASR**](./hw1_asr) Training a speech recognition model
- [**Project_AVSS**](./project_avss) Training an audio-visual speech separation model
- [**HW_NV**](./hw3_nv) Implementation of a TTS model (Neural Vocoder)
<!--
  -->

See our [project template](https://github.com/Blinorot/pytorch_project_template).

# Resources

- [Lecture recordings on YouTube (in russian)](https://youtube.com/playlist?list=PLYG3WHDP5CWVRxLjXZbllqIQTWY_QjKmz)

Some of the weeks have English recordings. See the corresponding sub-directories.

# Contributors & course staff

Course materials and teaching (in different years) were delivered by:

- [Maxim Kaledin](https://t.me/XuMuK_MK)
- [Petr Grinberg](https://t.me/Blinorot)
- [Grigory Fedorov](https://t.me/fedorovgv)
- [Aibek Alanov](https://t.me/aibrain)
- [Alexander Markovich (previously)](https://t.me/markovka17)
- [Daniil Ivanov (previously)](https://t.me/the_longest_id_in_the_world)
- [Ilya Lewin (previously)](https://t.me/levensons)
- [Timofey Smirnov (previously)](https://t.me/timothyxp)
- [Alexander Mamaev (previously)](https://t.me/alxmamaev)

# Past Versions

- [2023](https://github.com/markovka17/dla/tree/2023)
- [2022](https://github.com/markovka17/dla/tree/2022)
- [2021](https://github.com/markovka17/dla/tree/2021)
- [2020](https://github.com/markovka17/dla/tree/2020)
