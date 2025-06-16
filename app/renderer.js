const contentEl = document.getElementById('content');
const openBtn = document.getElementById('open');
const playBtn = document.getElementById('play');
const pauseBtn = document.getElementById('pause');
const stopBtn = document.getElementById('stop');
const voicesSel = document.getElementById('voices');
const speedInput = document.getElementById('speed');

let textContent = '';
let currentVoice = null;

window.api.getVoices().then(vs => {
  vs.forEach(v => {
    const opt = document.createElement('option');
    opt.textContent = v;
    opt.value = v;
    voicesSel.appendChild(opt);
  });
  if (vs.length) currentVoice = vs[0];
});

voicesSel.addEventListener('change', () => {
  currentVoice = voicesSel.value;
});

openBtn.addEventListener('click', async () => {
  const { text } = await window.api.openFile();
  if (text) {
    textContent = text;
    contentEl.textContent = textContent;
  }
});

playBtn.addEventListener('click', () => {
  window.api.speak(textContent, { voice: currentVoice, speed: parseFloat(speedInput.value) });
});

pauseBtn.addEventListener('click', () => {
  // say doesn't support pause/resume directly
});

stopBtn.addEventListener('click', () => {
  window.api.stop();
});
