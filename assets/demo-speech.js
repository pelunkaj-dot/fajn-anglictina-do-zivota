// Deliberately no speech service, media access, Audio, speechSynthesis or network calls.
export function stopSpeech(){}
export function speak(text,accent,slow=false,onStatus=()=>{}){onStatus('Zkus spojení přečíst nahlas. Poslech je v plné verzi.')}
export function voicePanel(target,accent,onResult,translation=''){
 const box=document.createElement('section');box.className='demo-speaking voice-panel';
 box.innerHTML='<div class="speaking-invitation"><span class="eyebrow">TEĎ TO ŘEKNI NAHLAS</span><h3>Přečti svou odpověď nahlas.</h3></div><p class="voice-reference" lang="en"></p><button class="text-button" data-voice="meaning">Zobrazit český význam</button><p class="voice-meaning requested-translation" hidden></p><p>Zkus větu říct druhému člověku. Kontrolu výslovnosti nabízí plná verze.</p>';
 box.querySelector('.voice-reference').textContent=target;const button=box.querySelector('[data-voice="meaning"]');button.hidden=!translation;button.onclick=()=>{const meaning=box.querySelector('.voice-meaning');meaning.textContent=translation;meaning.hidden=!meaning.hidden};return box;
}
