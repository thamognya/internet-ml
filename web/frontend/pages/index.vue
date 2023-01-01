<template lang="pug">
html(lang="en")
  body
    div(class="grid grid-cols-1 place-content-center align-middle gap-y-10 h-screen text-center")
      div(class="grid grid-cols-1 place-self-center")
        h1(class="text-5xl")
          a(href="/" class="url") Internet-ML
        h1(class="text-2xl")
          a(href="https://links.thamognya.com" class="url") by Thamognya Kodi
      div(class="grid sm:grid-cols-3 grid-cols-1 gap-y-4 place-items-center")
        h1(class="text-3xl")
          a(href="/NLP" class="url") NLP
        h1(class="text-3xl")
          a(href="/#" class="url") Image Generation (in-progress)
        h1(class="text-3xl")
          a(href="/#" class="url") Audio (in-progress)
</template>

<script>
import Vue from 'vue'
import '@/assets/css/url.module.scss'
export default Vue.extend({
    name: 'IndexPage'
})
</script>
