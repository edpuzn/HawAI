<template>
  <div class="chat-grid">
    <aside class="card sidebar">
      <button class="btn btn-success btn-sm w-100" @click="createThread">+ Yeni sohbet</button>
      <ul class="mt-3 list-unstyled threads">
        <li
          v-for="t in threads"
          :key="t.id"
          :class="['thread-item', t.id===threadId ? 'active' : '']"
        >
          <button class="btn btn-sm btn-link flex-1 text-start title" type="button" @click="openThread(t.id)">{{ t.title }}</button>
          <button class="btn btn-sm btn-outline-danger" type="button" title="Sil" aria-label="Sil" @click="removeThread(t.id)">Sil</button>
        </li>
      </ul>
    </aside>
    <main class="main">
      <div ref="messagesEl" class="messages">
        <div v-for="m in messages" :key="m.id" class="msg-row" :class="m.role==='user' ? 'to-right' : 'to-left'">
          <div v-if="editId===m.id && m.role==='user'" class="card edit-wrap">
            <textarea v-model="editText" class="form-control" rows="3" />
            <div class="d-flex gap-2 mt-2">
              <button class="btn btn-success btn-sm" @click="saveEdit">Kaydet</button>
              <button class="btn btn-secondary btn-sm" @click="cancelEdit">Vazgeç</button>
            </div>
          </div>
          <template v-else>
            <MessageBubble
              :text="m.content"
              :from="m.role"
              :image_preview_src="firstImage(m)"
            />
            <div v-if="m.images?.length > 1" class="img-grid">
              <img v-for="(im,i) in m.images.slice(1)" :key="i" :src="previewSrc(im)" class="thumb" />
            </div>
            <div v-if="m.role==='user'" class="meta">
              <button class="btn btn-link btn-sm text-muted" @click="startEdit(m)">✎ Düzenle</button>
            </div>
          </template>
        </div>
        <div v-if="isThinking" class="thinking">
          <div class="dots"><span></span><span></span><span></span></div>
          <div class="thinking-text">Düşünüyor…</div>
        </div>
      </div>

      <div class="composer">
        <ChatBox :thinking="isThinking" :placeholder="'Mesajınızı yazın…'" @send="handleSendWithImage" />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axios'
import MessageBubble from '@/components/MessageBubble.vue'
import ChatBox from '@/components/ChatBox.vue'

const router = useRouter()
const threads = ref<any[]>([])
const messages = ref<any[]>([])
const threadId = ref<string>('')
const isThinking = ref(false)
const messagesEl = ref<HTMLDivElement|null>(null)

const editId = ref<string>('')
const editText = ref('')

function previewSrc(im: string){
  if(im?.startsWith('data:image')) return im
  return im
}
function firstImage(m: any){
  const im = (m?.images || [])[0]
  return im ? previewSrc(im) : undefined
}
async function ensureAuth(){
  try{ await axios.get('/auth/me') }catch{ router.push('/login') }
}
async function loadThreads(){
  threads.value = (await axios.get('/chat/threads')).data
  if(!threads.value.length) await createThread()
}
async function createThread(){
  const res = await axios.post('/chat/threads', { title: 'Yeni Sohbet' })
  threadId.value = res.data.id
  await openThread(threadId.value)
}
async function openThread(id: string){
  threadId.value = id
  messages.value = (await axios.get(`/chat/messages/${id}`)).data
  await nextTick(); scrollToBottom(false)
}
async function removeThread(id: string){
  try{
    await axios.delete(`/chat/threads/${id}`)
    // listeden çıkar
    threads.value = threads.value.filter(t => t.id !== id)
    if(threadId.value === id){
      // mevcut silindiyse: varsa ilkine geç, yoksa sıfırla
      if(threads.value.length){
        await openThread(threads.value[0].id)
      } else {
        threadId.value = ''
        messages.value = []
      }
    }
  }catch(e){ /* sessizce geç */ }
}
function scrollToBottom(smooth = true){
  const el = messagesEl.value
  if(!el) return
  el.scrollTo({ top: el.scrollHeight, behavior: smooth ? 'smooth' : 'auto' })
}
async function handleSendWithImage(text: string, image_base64?: string, image_preview_src?: string){
  if(!text && !image_preview_src) return
  if(!threadId.value){ await createThread() }
  isThinking.value = true
  try{
    const images = image_preview_src ? [image_preview_src] : []
    await axios.post('/chat/send', { thread_id: threadId.value, content: text, images })
    await openThread(threadId.value)
  } finally {
    isThinking.value = false
    await nextTick(); scrollToBottom(true)
  }
}
function startEdit(m:any){ editId.value = m.id; editText.value = m.content }
async function saveEdit(){ await axios.post(`/chat/edit/${editId.value}`, { content: editText.value }); editId.value=''; await openThread(threadId.value) }
function cancelEdit(){ editId.value='' }

onMounted(async ()=>{ await ensureAuth(); await loadThreads(); await nextTick(); scrollToBottom(false) })
</script>

<style scoped>
.chat-grid{
  display:grid;grid-template-columns:260px 1fr;height:calc(100vh - 64px);gap:0;
}
.sidebar{ border-right:0;overflow:auto;margin:0;border-top-left-radius:0;border-top-right-radius:12px; }
.threads{ margin: 8px 0 0 0; }
.thread-item{ cursor:pointer; margin:6px 0; padding:8px 10px; border-radius:10px; color:#e5e7eb; }
.thread-item:hover{ background:#0f172a; }
.thread-item.active{ color:#22c55e; background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25); }

.main{ display:grid;grid-template-rows:1fr auto; }
.messages{ padding:12px; overflow:auto; display:flex; flex-direction:column; gap:10px; }
.msg-row{ display:flex; }
.msg-row.to-right{ justify-content:flex-end; }
.msg-row.to-left{ justify-content:flex-start; }
.img-grid{ display:flex; gap:6px; margin-top:6px; flex-wrap:wrap; }
.thumb{ max-width:160px; border-radius:8px; border:1px solid #1f2937; }
.meta{ margin-top:4px; text-align:right; }
.edit-wrap{ max-width:820px; }

.composer{ position:sticky; bottom:8px; padding:0 12px 12px; }

.thinking{ position:sticky; bottom:0; display:flex; flex-direction:column; align-items:center; gap:6px; padding:8px 0 2px; }
.thinking-text{ color:#9ca3af; font-size:.92rem; }
.dots{ display:inline-flex; gap:6px; }
.dots span{ width:8px; height:8px; border-radius:50%; background:#22c55e; animation: bounce 1s infinite ease-in-out; }
.dots span:nth-child(2){ animation-delay:.12s; }
.dots span:nth-child(3){ animation-delay:.24s; }
@keyframes bounce { 0%,80%,100%{ transform:translateY(0); opacity:.7 } 40%{ transform:translateY(-5px); opacity:1 } }
</style>


