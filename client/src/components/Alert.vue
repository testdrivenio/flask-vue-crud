<template>
  <div>
    <div class="alert alert-success" role="alert">{{ message }}</div>
    <br/>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
