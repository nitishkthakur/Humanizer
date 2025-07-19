function app() {
    return {
        currentPage: 'humanize',
        prompt: '',
        mode: 'humanize',
        aiResponse: '',
        humanizedOutput: '',
        loading: false,
        chatInput: '',
        chatMessages: [],
        chatLoading: false,
        messageId: 1,

        async humanizeText() {
            if (!this.prompt.trim()) return;
            
            this.loading = true;
            this.aiResponse = '';
            this.humanizedOutput = '';

            try {
                const formData = new FormData();
                formData.append('prompt', this.prompt);
                formData.append('mode', this.mode);

                const response = await fetch('/humanize', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    if (this.mode === 'humanize') {
                        this.aiResponse = this.prompt;
                        this.humanizedOutput = data.result;
                    } else {
                        this.aiResponse = data.result;
                        this.humanizedOutput = 'Using LLM mode - response generated above';
                    }
                } else {
                    this.aiResponse = `Error: ${data.error}`;
                    this.humanizedOutput = 'An error occurred while processing your request.';
                }
            } catch (error) {
                console.error('Error:', error);
                this.aiResponse = 'Network error occurred';
                this.humanizedOutput = 'Failed to connect to the server. Please try again.';
            } finally {
                this.loading = false;
            }
        },

        async sendMessage() {
            if (!this.chatInput.trim()) return;

            const userMessage = {
                id: this.messageId++,
                type: 'user',
                content: this.chatInput,
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };

            this.chatMessages.push(userMessage);
            const messageToSend = this.chatInput;
            this.chatInput = '';
            this.chatLoading = true;

            this.scrollToBottom();

            try {
                const formData = new FormData();
                formData.append('message', messageToSend);

                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                const assistantMessage = {
                    id: this.messageId++,
                    type: 'assistant',
                    content: data.success ? data.result : `Error: ${data.error}`,
                    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                };

                this.chatMessages.push(assistantMessage);
            } catch (error) {
                console.error('Error:', error);
                const errorMessage = {
                    id: this.messageId++,
                    type: 'assistant',
                    content: 'Sorry, I encountered an error. Please try again.',
                    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                };
                this.chatMessages.push(errorMessage);
            } finally {
                this.chatLoading = false;
                this.$nextTick(() => this.scrollToBottom());
            }
        },

        scrollToBottom() {
            this.$nextTick(() => {
                const chatMessages = document.getElementById('chat-messages');
                if (chatMessages) {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            });
        },

        init() {
            this.$watch('currentPage', () => {
                if (this.currentPage === 'chat' && this.chatMessages.length === 0) {
                    this.chatMessages.push({
                        id: this.messageId++,
                        type: 'assistant',
                        content: 'Hello! I\'m here to help. How can I assist you today?',
                        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    });
                    this.$nextTick(() => this.scrollToBottom());
                }
            });
        }
    }
}