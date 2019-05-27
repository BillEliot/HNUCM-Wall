<template>
    <a-menu v-model="navbar" mode="horizontal" theme="dark" class="nav">
        <a-sub-menu>
            <span slot="title"><a-icon type="coffee" />表白墙</span>
            <a-menu-item-group title="I Love U">
            <a-menu-item key="love:1" @click="$router.push({ path: '/' })">表白墙</a-menu-item>
            <a-menu-item key="love:2" @click="$router.push({ path: '/love/new' })">我要表白</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>

        <a-menu-item key="whisper">
            <a-icon type="star" /> 悄悄话
        </a-menu-item>
        <!-- auth -->
        <template v-if="userBaseInfo.uid != -1">
            <a-avatar :src="baseUrl + userBaseInfo.avatar" class="auth-avatar" />
            <a-dropdown class="auth-dropdown">
                <a> {{ userBaseInfo.nickname }} <a-icon type="down" /></a>
                <a-menu slot="overlay">
                    <a-menu-item>
                    <router-link :to="{ path: '/profile', query: { uid: userBaseInfo.uid } }">个人信息</router-link>
                    </a-menu-item>
                    <a-menu-item @click="logout">注销</a-menu-item>
                </a-menu>
            </a-dropdown>
        </template>
        <template v-else>
            <router-link to="/login">
                <a-button type="primary" class="auth-login">登录</a-button>
            </router-link>
            <router-link to="/register">
                <a-button class="auth-register">注册</a-button>
            </router-link>
        </template>
    </a-menu>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: ['userBaseInfo'],
  data() {
    return {
        navbar: null
    }
  },
  methods: {
      logout() {
        this.$axios.get('logout')
        this.userBaseInfo.nickname = ''
        this.userBaseInfo.avatar = ''
      },
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.auth-avatar {
    position: absolute;
    right: 10px;
    top: 10%
}
.auth-dropdown {
    position: absolute;
    right: 50px
}

@media (min-width: 375px) {
    .auth-login {
        position: absolute;
        right: 10px;
        top: 10%
    }
    .auth-register {
        position: absolute;
        right: 80px;
        top: 10%
    }
}
</style>
