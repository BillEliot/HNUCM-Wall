<template>
    <a-menu v-model="navbar" mode="horizontal" theme="dark" class="nav">
        <a-sub-menu>
            <span slot="title"><a-icon type="coffee" />墙墙们</span>
            <a-menu-item-group title="表白">
                <a-menu-item key="love:1" @click="$router.push({ path: '/love' })">表白墙</a-menu-item>
                <a-menu-item key="love:2" @click="navigate('/love/new')">我要表白</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="失物招领">
                <a-menu-item key="lose:1" @click="$router.push({ path: '/lose' })">失物墙</a-menu-item>
                <a-menu-item key="lose:2" @click="navigate('/lose/new')">发布失物</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="二手交易">
                <a-menu-item key="deal:1" @click="$router.push({ path: '/deal' })">二手墙</a-menu-item>
                <a-menu-item key="deal:2" @click="navigate('/deal/new')">发布物品</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>

        <a-menu-item key="bank" @click="$router.push({ path: '/bank' })">
            <a-icon type="star" /> 题库
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
        this.userBaseInfo.uid = -1
        this.userBaseInfo.nickname = '赶快登录吧～'
        this.userBaseInfo.avatar = '/media/img/avatar/anony.jpg'
      },
      navigate(path) {
          if (this.userBaseInfo.uid == -1) {
              this.$message.warning('先登录吧～')
          }
          else {
              this.$router.push({ path: path })
          }
      }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
.nav {
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 99;
}

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
