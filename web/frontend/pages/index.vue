<template lang="pug">
div
    .grid.grid-cols-1.place-content-center.align-middle.gap-y-10.h-screen.text-center
        .grid.grid-cols-1.place-self-center
            h1.text-5xl
                a.url(href='/') Internet-ML
            h1.text-xl
                a.url(href='https://links.thamognya.com') by Thamognya Kodi
        .grid.grid-cols-1.gap-y-4.place-items-center(class='md:grid-cols-3')
            h1.text-2xl
                a.url(href='/NLP') NLP
            h1.text-2xl
                a.url(href='/#') Image Generation (in-progress)
            h1.text-2xl
                a.url(href='/#') Audio (in-progress)
</template>

<script lang="typescript">
import Vue from 'vue'
export default Vue.extend({
    name: 'IndexPage'
})
</script>
