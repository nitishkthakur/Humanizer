function app() {
    return {
        currentPage: 'humanize',
        prompt: '',
        mode: 'llm_approach',
        selectedModel: 'llama-3.3-70b-versatile',
        chatSelectedModel: 'llama-3.3-70b-versatile',
        aiResponse: '',
        humanizedOutput: '',
        loading: false,
        generating: false,
        chatInput: '',
        chatMessages: [],
        chatLoading: false,
        clearingChat: false,
        sessionId: 'default',
        messageId: 1,

        get aiResponseMarkdown() {
            if (!this.aiResponse) return 'AI response will appear here...';
            return marked.parse(this.aiResponse);
        },

        get humanizedOutputFormatted() {
            if (!this.humanizedOutput) return 'Humanized text will appear here...';
            return marked.parse(this.humanizedOutput);
        },

        get humanizedSectionLabel() {
            if (this.mode === 'llm_approach') {
                return 'HUMANIZED OUTPUT (LLM Approach)';
            } else {
                return 'HUMANIZED OUTPUT';
            }
        },

        async humanizeText() {
            if (!this.prompt.trim()) return;
            
            // Check if "Work in Progress" is selected
            if (this.mode === 'work_in_progress') {
                alert('This feature is work in progress. Please try the LLM Approach instead.');
                return;
            }
            
            // Only proceed if LLM Approach is selected
            if (this.mode !== 'llm_approach') {
                return;
            }
            
            this.loading = true;
            this.humanizedOutput = '';

            try {
                const formData = new FormData();
                formData.append('prompt', this.prompt);
                formData.append('mode', this.mode);
                formData.append('model', this.selectedModel);
                
                // Always send the AI response if available for humanization
                if (this.aiResponse) {
                    formData.append('ai_response', this.aiResponse);
                }

                const response = await fetch('/humanize', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // Always put the humanized result on the right side
                    this.humanizedOutput = data.result;
                } else {
                    this.humanizedOutput = `Error: ${data.error}`;
                }
            } catch (error) {
                console.error('Error:', error);
                this.humanizedOutput = 'Failed to connect to the server. Please try again.';
            } finally {
                this.loading = false;
            }
        },

        async generateResponse() {
            if (!this.prompt.trim()) return;
            
            this.generating = true;
            this.aiResponse = '';

            try {
                const formData = new FormData();
                formData.append('message', this.prompt);
                formData.append('model', this.selectedModel);

                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    this.aiResponse = data.result;
                } else {
                    this.aiResponse = `Error: ${data.error}`;
                }
            } catch (error) {
                console.error('Error:', error);
                this.aiResponse = 'Network error occurred. Please try again.';
            } finally {
                this.generating = false;
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
                formData.append('model', this.chatSelectedModel);
                formData.append('session_id', this.sessionId);

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

        async clearChat() {
            this.clearingChat = true;
            
            try {
                const formData = new FormData();
                formData.append('session_id', this.sessionId);

                const response = await fetch('/clear-chat', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // Clear the frontend chat messages
                    this.chatMessages = [];
                    this.messageId = 1;
                    
                    // Add welcome message back
                    this.chatMessages.push({
                        id: this.messageId++,
                        type: 'assistant',
                        content: 'Hello! I\'m here to help. How can I assist you today?',
                        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    });
                } else {
                    console.error('Failed to clear chat:', data.error);
                }
            } catch (error) {
                console.error('Error clearing chat:', error);
            } finally {
                this.clearingChat = false;
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