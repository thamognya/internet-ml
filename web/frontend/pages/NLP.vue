<template lang="pug">
html(lang="en")
  body
    div(class="grid grid-cols-1 place-content-center align-middle gap-y-10 h-screen text-center")
      div(class="grid grid-cols-1 place-self-center")
        h1(class="text-5xl")
          a(href="/" class="url") Internet-NLP
        h1(class="text-2xl")
          a(href="https://links.thamognya.com" class="url") by Thamognya Kodi
</template>

<script>
import Vue from 'vue'
import '@/assets/css/url.module.scss'
export default Vue.extend({
    name: 'InternetNLP'
})
</script>
