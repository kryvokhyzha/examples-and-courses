# Homework 3 (Neural Vocoder)

As always, your code **must** be based on the provided [Project Template](https://github.com/Blinorot/pytorch_project_template). Feel free to choose any of the code branches as a starting point (maybe you will find the `main` branch easier than the `ASR` one).

## Task

In this homework, you need to implement [HiFiGAN](https://arxiv.org/pdf/2010.05646.pdf) vocoder. **You are not allowed to use any implementation from the web**. The penalty for doing this will be severe.

Use [LJSpeech](https://keithito.com/LJ-Speech-Dataset/) Dataset.

To avoid a mismatch of training and test features you should use the same code for obtaining MelSpectrograms from audio. An example is given below.

<details>
<summary>Click me</summary>

```python
from dataclasses import dataclass

import torch
from torch import nn

import torchaudio

import librosa


@dataclass
class MelSpectrogramConfig:
    sr: int = 22050
    win_length: int = 1024
    hop_length: int = 256
    n_fft: int = 1024
    f_min: int = 0
    f_max: int = 8000
    n_mels: int = 80
    power: float = 1.0

    # value of melspectrograms if we fed a silence into `MelSpectrogram`
    pad_value: float = -11.5129251


class MelSpectrogram(nn.Module):

    def __init__(self, config: MelSpectrogramConfig):
        super(MelSpectrogram, self).__init__()

        self.config = config

        self.mel_spectrogram = torchaudio.transforms.MelSpectrogram(
            sample_rate=config.sr,
            win_length=config.win_length,
            hop_length=config.hop_length,
            n_fft=config.n_fft,
            f_min=config.f_min,
            f_max=config.f_max,
            n_mels=config.n_mels
        )

        # The is no way to set power in constructor in 0.5.0 version.
        self.mel_spectrogram.spectrogram.power = config.power

        # Default `torchaudio` mel basis uses HTK formula. In order to be compatible with WaveGlow
        # we decided to use Slaney one instead (as well as `librosa` does by default).
        mel_basis = librosa.filters.mel(
            sr=config.sr,
            n_fft=config.n_fft,
            n_mels=config.n_mels,
            fmin=config.f_min,
            fmax=config.f_max
        ).T
        self.mel_spectrogram.mel_scale.fb.copy_(torch.tensor(mel_basis))

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        """
        :param audio: Expected shape is [B, T]
        :return: Shape is [B, n_mels, T']
        """

        mel = self.mel_spectrogram(audio) \
            .clamp_(min=1e-5) \
            .log_()

        return mel
```

</details>

---

## Mandatory requirements

In general, the format of the current homework follows that of the first homework assignment (ASR). You must organize the repository as in the first homework assignment, which is to break up the code into modules and follow the code style.

So, we don't accept homework if any of the following requirements are not satisfied:

- The code should be stored in a public github (or gitlab) repository and based on the provided template. (Before the deadline, use a private repo. Make it public after the deadline.)
- All the necessary packages should be mentioned in `./requirements.txt` or be installed in a dockerfile.
- All necessary resources (such as model checkpoints, LMs, and logs) should be downloadable with a script. Mention the script (or lines of code) in the `README.md`.
- You should implement all functions in `synthesize.py` (for evaluation) so that we can check your assignment (see [Testing](#testing) section).
- Basically, your `synthesize.py` and `train.py` scripts should run without issues after running all commands in your installation guide. Create a clean env and deploy your lib into a separate directory to check if everything works fine given that you follow your stated installation steps.
- You must provide the logs for the training of your final model from the start of the training. We heavily recommend you to use W&B (CometML) Reports feature.
- Attach a report that includes:
  - Description and result of each experiment.
  - How to reproduce your model?
  - Attach training logs showing the rate of convergence.
  - What worked and what didn't work?
  - What were the major challenges?
  - Special tasks from the [Report](#report) section.

## Testing

You **must** add `synthesize.py` script and a `CustomDirDataset` Dataset class in `src/datasets/` with a proper config in `src/configs/`. Add additional option to provide a text query to the model via command-line instead of a dataset.

The `CustomDirDataset` should be able to parse any directory of the following format:

```bash
NameOfTheDirectoryWithUtterances
└── transcriptions
    ├── UtteranceID1.txt
    ├── UtteranceID2.txt
    .
    .
    .
    └── UtteranceIDn.txt
```

It should has an argument for the path to this custom directory that can be changed via `Hydra`-options.

The `synthesize.py` script must apply the model on the given dataset and save generated utterances in the requested directory. The generated utterance id should be the same as the utterance id in transcription (so they can be matched together).

Mention the lines on how to run inference on your final model in the `README`. Include the lines for the script too.

> [!NOTE]
> Vocoder needs spectrograms to operate on. You can generate them using one of the acoustic models from huggingface, espnet, or NVIDIA NeMo. Pass the text transcription as input. Note that the MelSpectrogram settings used for training your Vocoder should be the same as for the acoustic models to avoid extra artifacts.

> [!TIP]
> For the [Report](#report) section, it will be useful to also add a "resynthesize" option where ground-truth audio is taken as input to extract melspectrogram.

## Report

To supplement your report, conduct the following analysis.

**Inner-Analysis**:

1. Take several utterances from LJSpeech dataset you were training the vocoder on.
2. Calculate the MelSpectrograms (using original audio) and generate synthesized versions of the audio using your vocoder.
3. Compare the generated samples with the corresponding original ones. Do this in time and time-frequency domains. What differences do you see? Can you understand that the audio is synthesized by listening to them? Can you do it by looking at the waveform or spectrogram? Explain the results and do some conclusions.

**External Dataset Analysis**:

1. Take some other utterances, for example, the ones in the [Grade](#grade) Section.
2. Calculate the MelSpectrograms and generate synthesized versions.
3. Conduct the comparison again. Does the conclusions from the _Inner Analysis_ hold here too? What differences do you see between using external and training datasets?

**Full-TTS system Analysis**:

1. Finally, take some text transcriptions and generate utterances using your vocoder and one of the acoustic models as mentioned in the [Testing](#testing) section. Note that you will need a ground truth audio to do a comparison with:
   - For the first part, take the text transcription from the LJspeech dataset.
   - For the second part, take the text transcription from the external dataset.
2. Conduct the comparison of generated utterances with their original versions. What new artifacts do you see and hear?

Add some final thoughts about the quality of generated samples and the ease of their detection. What limitations of TTS systems have you found?

> [!TIP]
> To improve your grade, try to calculate some statistics on a big-enough set of utterances to supplement your thoughts.

---

## Grade

```
grade = MOS + 0.5 * (quality of code and report)
```

> [!IMPORTANT]
> Keep in mind that this is an individual homework and that the report is of ASR-HW style, not an article-style as in AVSS.

To evaluate the MOS (between 0 and 5), you must add a synthesis of the following sentences to the report:

- Deep Learning in Audio course at HSE University offers an exciting and challenging exploration of cutting-edge techniques in audio processing, from speech recognition to music analysis. With complex homeworks that push students to apply theory to real-world problems, it provides a hands-on, rigorous learning experience that is both demanding and rewarding.
- Dmitri Shostakovich was a Soviet-era Russian composer and pianist who became internationally known after the premiere of his First Symphony in 1926 and thereafter was regarded as a major composer.
- Lev Termen, better known as Leon Theremin was a Russian inventor, most famous for his invention of the theremin, one of the first electronic musical instruments and the first to be mass-produced.
- Mihajlo Pupin was a founding member of National Advisory Committee for Aeronautics (NACA) on 3 March 1915, which later became NASA, and he participated in the founding of American Mathematical Society and American Physical Society.
- Leonard Bernstein was an American conductor, composer, pianist, music educator, author, and humanitarian. Considered to be one of the most important conductors of his time, he was the first American-born conductor to receive international acclaim.

The corresponding original audio for calculating `MelSpectogram` will be provided in the course channel.

Add a neural-MOS estimate of your model performance using [WVMOS](https://github.com/AndreevP/wvmos) or [NORESQA-MOS](https://github.com/facebookresearch/Noresqa).

To give you a rough idea of how we are going to evaluate, the scale is _approximately_ as follows:

    5. Words can be heard perfectly
    4. There is some obvious noise, but all the words are clear and you do not have to listen to them to understand
    3. Most words are understandable, but some words are indistinguishable
    2. Very noisy audio, but some words are understandable
    1. At least it squeaks
    0. Vacuum cleaner

**There are no bonuses for this homework.**
