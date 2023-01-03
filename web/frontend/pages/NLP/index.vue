<template lang="pug">
div
  .grid.grid-cols-1.place-content-center.align-middle.gap-y-10.h-screen.text-center
    .grid.grid-cols-1.place-self-center
      h1.text-5xl
        a.url(href='/') internet-nlp
      h1.text-2xl
        a.url(href='/') part of internet-ml
    .grid.grid-cols-1.gap-y-4.place-items-center(class='md:grid-cols-2')
      h1.text-2xl
        a.url(href='/nlp/no-context') no context
      h1.text-2xl
        a.url(href='/nlp/context') context
</template>

<script>
import Vue from 'vue'
export default Vue.extend({
    name: 'InternetNLP'
})
</script>
