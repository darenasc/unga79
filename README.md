# UN General Assermbly 79 Speeches

The app analyses the speech of each country at the #UNGA79 in 2024. It presents:
- A summary of the speech
- A list of risks identied in the the speech
- Other coutries mentioned and the sentiment towards them 
- A haiku 
- An audio with Yoda's advice in Carl Sagan's voice

The process is the following:

```mermaid
flowchart LR
    data_collection(Download URLs) --> transcripts(Get transcripts)
    transcripts --> summary(LLM summary)
    transcripts --> haiku(LLM haiku)
    transcripts --> risks(LLM risks)
    transcripts --> other_countries(LLM countries mentioned)
    transcripts --> yoda(LLM yoda's advice)
    summary --> streamlit(Streamlit App)
    haiku --> streamlit(Streamlit App)
    risks --> streamlit(Streamlit App)
    other_countries --> streamlit(Streamlit App)
    yoda --> TTS(TTS audio)
    TTS --> streamlit(Streamlit App)
```
<img src="figures/streamlit-mark-color.png" alt="drawing" width="25"/>[ See the app](https://unga79.streamlit.app)

![](figures/screenshot.png)

## LLM application

* [x] Summary of the speech
* [x] List of countries mentioned and sentiment
* [x] Risks mentioned in the speech
* [x] Top 3 most important ideas mentioned
* [x] Advice in Yoda style
* [ ] Emotion detection: speech, such as happiness, sadness, anger, or excitement
* [ ] **Inference Generation**: Use LLMs to generate inferences based on the speech content, such as predicting potential consequences of policy decisions oranticipating international reactions.
* [ ] **Speech Emotional Arc Analysis**: Analyze the emotional tone of the speech over time to identify potential shifts or arcs in sentiment. This can provide insight into the leader's communication strategy or audience engagement.

## Usage locally

```bash
# Clone this repository
git clone https://github.com/darenasc/unga79.git
# Change directory to repository
cd unga79
# Install dependencies
pip install pipenv
python3 -m pipenv install Pipfile
python3 -m pipenv install -d Pipfile
# Activate Python environment
pipenv shell
# Run the streamlit app
streamlit run app/app.py
```

### TTS

> Note: Installing the TTS model is not needed to interact with the app as the 
    audio files are included in the repository in [app/audio/](app/audio/).

For the voice generation I'm using [F5-TTS](https://github.com/SWivid/F5-TTS).
Generated a sample of 10 seconds with the voice of Carl Sagan and passed the 
texts generate from the LLM.

The following is the process to install and run the script to generate the 
audios.

```bash
# Clone the repository
git clone https://github.com/SWivid/F5-TTS.git
cd F5-TTS

# Run the following two brew lines only if you are using an Apple Silicon chip
brew update
brew install ffmpeg

# Install torch in a second environment
pipenv install torch torchaudio
pipenv install -e .

# Launch the gradio GUI
f5-tts_infer-gradio

# Or run shell commands replacing the arguments between "<>" to generate an audio
f5-tts_infer-cli \
--model "F5-TTS" \
--ref_audio "</YOUR/REFERENCE/AUDIO.wav>" \
--ref_text "<The text in the reference audio to create the voice.>" \
--gen_file "</THE/FILE/WITH/THE/CONTENT/TO/VOICED.txt>" \
--output_dir "</OUTPUT/DIR>" \
--output_file "<OUTPUT_FILE.wav>" 
```

## Resources
- [#UNGA79 Youtube](https://www.youtube.com/watch?v=pH19ivsC62E&list=PLwoDFQJEq_0YukP-06eOEinhpM2GeG3hY)
- [UNGA79](https://docs.google.com/spreadsheets/d/1qtqfnRSW24j-XLN7SRKywDCuFatARCH8pUg1Rr6I2vI/edit?gid=1290530125#gid=1290530125)