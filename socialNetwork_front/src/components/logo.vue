<template>
  <div class="logo">
    <div class="text-wrappe text-l r">
      <p>sport</p>
      <p>movie</p>
      <p>society</p>
      <p>fashion</p>
      <p>social</p>
      <p>business</p>
      <p>serial</p>
      <p>game</p>
      <p>nature</p>
      <p>finance</p>
      <p>food</p>
      <p>job</p>
      <p>info</p>
      <p>science</p>
      <p>travel</p>
    </div>
    <h1 class="text-sky-500 text-2xl font-semibold pl-1">network.</h1>
  </div>
</template>

<script setup>
import { gsap } from "gsap";
import SplitType from "split-type";
import { onMounted } from "vue";

onMounted(() => {
  const titles = gsap.utils.toArray("p");

  const tl = gsap.timeline({ repeat: -1, repeatDelay: 0 });

  titles.forEach((title) => {
    const splitTitle = new SplitType(title);
    tl.from(
      splitTitle.chars,
      {
        duration: 1,
        opacity: 0,
        y: 10,
        rotateX: -90,
        stagger: 0.05,
      },
      "<"
    ).to(
      splitTitle.chars,
      {
        duration: 1.3,
        opacity: 0,
        y: -10,
        rotateX: -90,
        stagger: 0.05,
      },
      "<1"
    );
  });
});
</script>

<style scoped>
.logo {
  display: flex;
  align-items: baseline;
}

.text-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

p {
  margin: 0;
  line-height: 0;
  text-align: right;
}
</style>
