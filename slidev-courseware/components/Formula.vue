<script setup lang="ts">
import { computed } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const props = defineProps<{
  tex: string
  display?: boolean
}>()

const rendered = computed(() =>
  katex.renderToString(props.tex, {
    displayMode: props.display ?? false,
    throwOnError: false,
    strict: false,
  }),
)
</script>

<template>
  <span
    :class="display ? 'formula-display' : 'formula-inline'"
    v-html="rendered"
  />
</template>
