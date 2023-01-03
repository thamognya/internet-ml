<template lang="pug">
div(v-if="loading")
    .flex.items-center.justify-center.h-screen(v-if="loading")
        LoadingWheel
div(v-else)
    .grid.grid-cols-1.place-content-center.align-middle.gap-y-5.h-screen.text-center
        .grid.grid-cols-1.place-self-center
            h1.text-5xl
                a.url(href="/NLP") Internet-NLP
            h1.text-2xl
                a.url(href="/NLP/no-context/question-answering") Question Answering No Context
            h1.text-2xl
                a.url(href="/") Part of Internet-ML
        .container.mx-auto
            form(v-if="!loading", @submit.prevent="submitForm")
                label.block.font-bold.text-lg.mb-2(for="question") Question
                textarea#question.border.rounded.w-full.py-2.px-3(
                    v-model="form.question",
                    rows="5"
                )
                button.bg-gray-500.text-white.font-bold.py-2.px-4.rounded(
                    class="hover:bg-gray-700",
                    type="submit",
                    v-if="form.submitCounter < 600"
                )
                    | Submit
                p.bg-red-500(v-if="form.submitCounter >= 600") Please wait for sometime as you have made 600 requests   within one hour.
            .mt-4.font-bold(v-if="answer !== null")
                p Question: {{ tmpquestion }}
                p.typed-text Answer: {{ typedAnswer }}
                p Urls:
                ul(v-if="typedAnswer.length === answer.length && urls !== null")
                    li(v-for="url in urls", :key="url")
                        span - 
                        a.url(:href="url") {{ url }}
</template>

<script>
import LoadingWheel from '@/components/LoadingWheel.vue'

export default {
    components: { LoadingWheel },
    data() {
        return {
            form: {
                question: '',
                submitCounter: 0
            },
            answer: null,
            loading: false,
            typedAnswer: '',
            urls: null
        }
    },
    created() {
        setInterval(() => {
            this.form.submitCounter = 0
        }, 3600000)
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
            this.form.submitCounter++
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
                const typingInterval = setInterval(() => {
                    this.typedAnswer +=
                        this.answer[this.typedAnswer.length] || ''
                    if (this.typedAnswer.length === this.answer.length) {
                        clearInterval(typingInterval)
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

<style lang="scss">
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
