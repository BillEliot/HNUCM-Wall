<template>
  <div>
    <!-- navbar -->
    <a-menu v-model="navbar" mode="horizontal" theme="dark" class="nav">
      <a-menu-item key="love">
        <a-icon type="coffee" /> 表白墙
      </a-menu-item>

      <a-menu-item key="whisper">
        <a-icon type="star" /> 悄悄话
      </a-menu-item>
      <!-- login/register -->
      <template v-if="username">
        <a-avatar :src="avatar" />
        <a-dropdown>
          <a> {{ username }} <a-icon type="down" /></a>
          <a-menu slot="overlay">
            <a-menu-item>
              <router-link to="/profile">个人信息</router-link>
            </a-menu-item>
            <a-menu-item @click="logout">注销</a-menu-item>
            <a-menu-item>
              <router-link to="/reserve">立即预约</router-link>
            </a-menu-item>
          </a-menu>
        </a-dropdown>
      </template>
      <template v-else>
        <router-link to="/login">
          <a-button type="primary" style="margin-right: 10px">登录</a-button>
        </router-link>
        <router-link to="/register">
          <a-button>注册</a-button>
        </router-link>
      </template>
    </a-menu>

    <a-carousel autoplay>
      <img src="https://s2.ax1x.com/2019/04/11/AHBlSe.jpg">
      <img src="https://s2.ax1x.com/2019/04/11/AHWuDS.png">
    </a-carousel>
    <!--
    <div class="hero-holder" style="position: relative">
      <div class="hero-message">
        <h1 class="uppercase">优敏思</h1>
        <h2 class="hero-subtitle">竞赛教育领跑者</h2>
      </div>
    </div>
    -->
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      navbar: null,
      username: null
    }
  }
}
</script>

<style>

</style>
