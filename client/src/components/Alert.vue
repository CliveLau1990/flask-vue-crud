<template>
  <div>
      <b-alert variant="success" dismissible show>{{ message }}</b-alert>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
