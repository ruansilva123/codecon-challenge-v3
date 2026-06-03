<template>
  <UContainer class="pt-5">
    <h2>Bloqueie seu ip com 5 requisições</h2>
    <div class="flex flex-col items-center my-12">
      <p class="text-lg font-semibold mb-3">IP: {{ myIp }}</p>
      <UButton label="Chamar a API" size="xl" @click="ChamarApi" />
      <!-- <p class="text-center text-red-500" v-if="requestRealizadas">Restam apenas {{ 5 - requestRealizadas }} requisições</p> -->
    </div>
    <h6>Solicitar Vários</h6>
    <div class="flex flex-col items-center gap-1">
      <UInputNumber v-model="solicitarVariosQtd" />
      <UButton @click="enviarVarios" :label="`Enviar ${solicitarVariosQtd}`" />
    </div>
  </UContainer>
</template>
<script setup lang="ts">
const deuErro = ref(false)
const myIp = ref()
const requestRealizadas = ref(0)
const solicitarVariosQtd = ref(5)
onMounted(() => {
  verificarIp()
})
const verificarIp = async () => {
  const response = await $fetch('https://api.ipify.org?format=json')
  myIp.value = (response as any).ip
}
const ChamarApi = async () => {
  await $fetch('http://localhost:8080/', {
    method: 'get'
  })
}
const enviarVarios = () => {
  for (let i = 0; i <= solicitarVariosQtd.value; i++) {
    ChamarApi()
  }
}
</script>