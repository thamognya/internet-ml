<template>
    <div class="container mx-auto p-4">
        <form v-if="!loading" @submit.prevent="submitForm">
            <label class="block font-bold text-lg mb-2" for="question"
                >Question</label
            >
            <textarea
                id="question"
                v-model="form.question"
                class="border rounded w-full py-2 px-3"
                rows="5"
            ></textarea>
            <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                type="submit"
            >
                Submit
            </button>
        </form>
        <div v-if="loading" class="flex items-center justify-center h-screen">
            <div class="lds-ring">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
        <div v-if="answer !== null" class="mt-4 font-bold">
            <p>Question: {{ tmpquestion }}</p>
            <p class="typed-text">Answer: {{ typedAnswer }}</p>
            <p>Urls:</p>
            <ul v-if="typedAnswer.length === answer.length && urls !== null">
                <li v-for="url in urls" :key="url">
                    <a :href="url" class="url">- {{ url }}</a>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            form: {
                question: ''
            },
            answer: null,
            loading: false,
            typedAnswer: '',
            urls: null
        }
    },
    methods: {
        resetForm() {
            this.form.question = ''
            this.answer = null
            this.loading = false
            this.typedAnswer = ''
            this.urls = null
        },
        async submitForm() {
            this.loading = true
            try {
                const { data } = await this.$axios.post(
                    'http://localhost:8080/api/nlp/no-context/question-answering/',
                    {
                        question: this.form.question
                    }
                )
                this.tmpquestion = this.form.question
                this.resetForm()
                this.answer = data.response.answer
                this.loading = false
                // console.log(this.answer)
                const interval = setInterval(() => {
                    this.typedAnswer +=
                        this.answer[this.typedAnswer.length] || ''
                    if (this.typedAnswer.length === this.answer.length) {
                        clearInterval(interval)
                    }
                }, 150)
                this.urls = data.resources
            } catch (error) {
                // console.error(error)
            }
        }
    }
}
</script>

<style>
.lds-ring {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;
}

.lds-ring div {
    box-sizing: border-box;
    display: block;
    position: absolute;
    width: 64px;
    height: 64px;
    margin: 8px;
    border: 8px solid #000;
    border-radius: 50%;
    animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    border-color: #000 transparent transparent;
}

.lds-ring div:nth-child(1) {
    animation-delay: -0.45s;
}

.lds-ring div:nth-child(2) {
    animation-delay: -0.3s;
}

.lds-ring div:nth-child(3) {
    animation-delay: -0.15s;
}

@keyframes lds-ring {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.typed-text {
    position: relative;
    display: inline;
}

.typed-text::after {
    content: '|';
    animation: blink 0.7s infinite;
}

@keyframes blink {
    0% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}
</style>
