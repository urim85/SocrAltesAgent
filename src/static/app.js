document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const currentPlan = document.getElementById('current-plan');
    const depthBtns = document.querySelectorAll('.depth-btn');

    let messages = [];
    let socraticDepth = 1;
    let sessionId = null;
    let isThinking = false;

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Depth Selection
    depthBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            depthBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            socraticDepth = parseInt(btn.dataset.depth);
        });
    });

    // Send Message
    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text || isThinking) return;

        // Add User Message to UI
        addMessage(text, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';
        
        isThinking = true;
        const loadingId = addLoadingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: [...messages, { role: 'user', content: text }],
                    socratic_depth: socraticDepth,
                    session_id: sessionId
                })
            });

            if (!response.ok) throw new Error('API request failed');

            const data = await response.json();
            
            // Update State
            sessionId = data.session_id;
            messages.push({ role: 'user', content: text });
            messages.push({ role: 'assistant', content: data.answer });

            // Remove Loading & Add AI Response
            removeLoadingIndicator(loadingId);
            addMessage(data.answer, 'ai');

            // Update Plan if available
            if (data.plan) {
                currentPlan.innerText = data.plan;
                currentPlan.classList.add('updated');
                setTimeout(() => currentPlan.classList.remove('updated'), 1000);
            }

        } catch (error) {
            console.error(error);
            removeLoadingIndicator(loadingId);
            addMessage('죄송합니다. 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.', 'ai');
        } finally {
            isThinking = false;
        }
    }

    function addMessage(text, role) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        msgDiv.innerHTML = `
            <div class="message-content">
                ${text.replace(/\n/g, '<br>')}
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function addLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ai';
        msgDiv.id = id;
        msgDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function removeLoadingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    newChatBtn.addEventListener('click', () => {
        chatMessages.innerHTML = `
            <div class="message ai">
                <div class="message-content">
                    새로운 대화를 시작합니다. 무엇을 도와드릴까요?
                </div>
            </div>
        `;
        messages = [];
        sessionId = null;
        currentPlan.innerText = '질문을 입력하면 AI가 학습 계획을 세웁니다.';
    });
});
