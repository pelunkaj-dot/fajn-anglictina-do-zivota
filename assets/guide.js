// Guidance follows the learner; decorative previews never alter answers or scores.
let dispose=()=>{};
export function stopGuide(){dispose();dispose=()=>{}}
export function guideStatus(message){const task=document.querySelector('.task[data-guide]');if(!task)return;task.classList.toggle('guide-playing',message.startsWith('Přehrávám'));if(message.startsWith('Teď zopakuj'))task.classList.remove('guide-playing')}
export function startGuide(task,{spoken=false,mode='teach'}={}){
 stopGuide();if(!task)return;const timers=new Set(),listeners=[];let touched=false;
 const later=(fn,ms)=>{const id=setTimeout(()=>{timers.delete(id);if(task.isConnected)fn()},ms);timers.add(id);return id};
 const on=(element,type,fn)=>{if(element){element.addEventListener(type,fn);listeners.push(()=>element.removeEventListener(type,fn))}};
 const rail=document.createElement('ol');rail.className='learning-path';rail.setAttribute('aria-label','Postup cvičení');rail.innerHTML=['Poslechni',mode==='practice'?'Vyber odpověď':mode==='conversation'?'Napiš odpověď':'Sestav odpověď','Ověř','Vyslov'].map((label,i)=>`<li data-guide-step="${i+1}"><span>${i+1}</span>${label}</li>`).join('');task.querySelector('.learning-guide').after(rail);
 const set=step=>{task.dataset.guide=String(step);rail.querySelectorAll('li').forEach(li=>{if(Number(li.dataset.guideStep)===step)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current')})};
 const compose=()=>{touched=true;task.classList.remove('guide-preview');set(2)};
 if(spoken){set(4);task.querySelector('.prompt-speaking').hidden=true;task.querySelector('.voice-panel')?.classList.add('guide-voice');}
 else{
 set(1);const next=document.createElement('button');next.type='button';next.className='text-button guide-next';next.textContent='Teď sestavit odpověď →';task.querySelector('.prompt-speaking').append(next);on(next,'click',()=>{compose();task.querySelector('#response-area').scrollIntoView({block:'nearest',behavior:document.body.classList.contains('no-motion')?'instant':'smooth'})});
 // A short neutral gesture shows the mechanics, never a word from the answer.
 if(mode==='teach'){const preview=document.createElement('div');preview.className='gesture-preview';preview.setAttribute('aria-hidden','true');preview.innerHTML='<span class="gesture-slot"></span><span class="gesture-word">slovo</span><svg class="gesture-hand" viewBox="0 0 32 40"><path d="M11 22V7a3 3 0 016 0v11l3-1 7 5c3 2 3 5 2 8l-3 7H12L5 26c-3-4 1-7 4-4l2 2" fill="currentColor" stroke="var(--surface)" stroke-width="2"/></svg>';task.querySelector('#response-area').prepend(preview);later(()=>{if(!touched&&task.dataset.guide==='1'){set(2);task.classList.add('guide-preview');later(()=>task.classList.remove('guide-preview'),4800)}},6500)}
 let checkTimer;const response=task.querySelector('#response-area');on(response,'pointerdown',()=>{if(task.dataset.guide==='1')compose();task.classList.remove('guide-preview')});
 const working=()=>{compose();clearTimeout(checkTimer);const hasAnswer=mode==='teach'?task.querySelectorAll('[data-remove]').length>0:mode==='conversation'?!!task.querySelector('#written-answer')?.value.trim():false;if(hasAnswer)checkTimer=later(()=>set(3),2400)};
 on(response,'click',e=>{if(e.target.closest('[data-token],[data-remove],[data-move]'))working()});on(response,'input',working);on(response,'drop',working);on(task.querySelector('#check-answer'),'click',()=>set(2));
 on(task.querySelector('#listen-prompt'),'click',()=>{touched=true;set(1);task.classList.remove('guide-preview')});
 listeners.push(()=>clearTimeout(checkTimer));
 }
 dispose=()=>{for(const id of timers)clearTimeout(id);for(const off of listeners)off();task.classList.remove('guide-playing','guide-preview')};
}
