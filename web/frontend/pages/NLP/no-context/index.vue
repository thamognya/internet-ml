<script>
import Vue from 'vue'
export default Vue.extend({
    name: 'InternetNLP'
})
</script>

<template lang="pug">
html(lang="en")
  body
    div(class="grid grid-cols-1 place-content-center align-middle gap-y-10 h-screen text-center")
      div(class="grid grid-cols-1 place-self-center")
        h1(class="text-5xl")
          a(href="/NLP" class="url") Internet-NLP
        h1(class="text-2xl")
          a(href="/NLP/no-context" class="url") No context tools
        h1(class="text-2xl")
          a(href="/" class="url") Part of Internet-ML
      div(class="grid md:grid-cols-2 grid-cols-1 gap-y-4 place-items-center")
        h1(class="text-2xl")
          a(href="/NLP/no-context/question-answer" class="url") Question Answering
        h1(class="text-2xl")
          a(href="/NLP/context/NLI" class="url") NLI
</template>
