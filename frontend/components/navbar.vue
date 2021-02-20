<template>
    <a-menu v-model="navbar" mode="horizontal" theme="dark" class="nav">
        <a-menu-item key="home" @click="$router.push({ path: '/' })">
            <a-icon type="home" /> 寻可校园墙
        </a-menu-item>
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
            <a-menu-item-group title="求助">
                <a-menu-item key="help:1" @click="$router.push({ path: '/help' })">求助墙</a-menu-item>
                <a-menu-item key="help:2" @click="navigate('/help/new')">发布求助</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>

        <a-menu-item key="article" @click="$router.push({ path: '/article' })">
            <a-icon type="crown" /> 大佬杂谈
        </a-menu-item>

        <a-sub-menu>
            <span slot="title"><a-icon type="heat-map" />校园动态</span>
            <a-menu-item-group title="热点">
                <a-menu-item key="hot:1" @click="$router.push({ path: '/hot' })">校园热点</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="讲座">
                <a-menu-item key="lecture:1" @click="$router.push({ path: '/lecture' })">讲座动态</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="活动">
                <a-menu-item key="activity:1" @click="$router.push({ path: '/activity/jingui' })">金匮打卡</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>

        <a-sub-menu>
            <span slot="title"><a-icon type="sliders" />校园团体</span>
            <a-menu-item-group title="社团">
                <a-menu-item key="club:1" @click="$router.push({ path: '/club' })">校园社团</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="学生组织">
                <a-menu-item key="organization:1" @click="$router.push({ path: '/organization' })">校团委学生部门</a-menu-item>
                <a-menu-item key="organization:2" @click="$router.push({ path: '/organization/club' })">学生社团联合会</a-menu-item>
                <a-menu-item key="organization:3" @click="$router.push({ path: '/organization/troupe' })">大学生艺术团</a-menu-item>
                <a-menu-item key="organization:4" @click="$router.push({ path: '/organization/science' })">大学生科学技术协会</a-menu-item>
                <a-menu-item key="organization:5" @click="$router.push({ path: '/organization/union' })">校学生会</a-menu-item>
                <a-menu-item key="organization:6" @click="$router.push({ path: '/organization/subunion' })">院级学生会</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>

        <a-sub-menu>
            <span slot="title"><a-icon type="database" />知识库</span>
            <a-menu-item-group title="题库">
                <a-menu-item key="bank:1" @click="$router.push({ path: '/bank/search' })">查题</a-menu-item>
                <a-menu-item key="bank:2" @click="$router.push({ path: '/bank' })">题库</a-menu-item>
                <a-menu-item key="bank:3" @click="$router.push({ path: '/bank/errorBook', query: { id: userBaseInfo.id } })">错题本</a-menu-item>
                <a-menu-item key="bank:4" @click="$router.push({ path: '/bank/statistics' })">答题记录</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="文件">
                <a-menu-item key="file:1" @click="$router.push({ path: '/file' })">学习资料文件</a-menu-item>
            </a-menu-item-group>
            <a-menu-item-group title="中药">
                <a-menu-item key="medicine:1" @click="$router.push({ path: '/medicine' })">中药库</a-menu-item>
                <a-menu-item key="medicine:2" @click="$router.push({ path: '/medicine/search' })">查中药</a-menu-item>
            </a-menu-item-group>
            <!--
            <a-menu-item-group title="方剂">
                <a-menu-item key="prescription:1" @click="$router.push({ path: '/prescription' })">方剂库</a-menu-item>
                <a-menu-item key="prescription:2" @click="$router.push({ path: '/prescription/search' })">查方剂</a-menu-item>
            </a-menu-item-group>
            -->
            <a-menu-item-group title="经络">
                <a-menu-item key="acupuncture:1" @click="$router.push({ path: '/acupuncture' })">经络库</a-menu-item>
                <a-menu-item key="acupuncture:2" @click="$router.push({ path: '/acupuncture/search' })">查穴位</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>

        <a-menu-item key="newStudent" @click="$router.push({ path: '/newStudent' })">
            <a-icon type="sound" /> 新生指南
        </a-menu-item>
        <a-sub-menu>
            <span slot="title"><a-icon type="gateway" />虚拟仿真</span>
            <a-menu-item-group title="虚拟门诊">
                <a-menu-item key="gateway:1" @click="confirm_VirtualDiagnosis">虚拟门诊</a-menu-item>
                <a-menu-item key="gateway:2" @click="$router.push({ path: '/virtualsimulation/virtualdiagnosis/log' })">查看记录</a-menu-item>
            </a-menu-item-group>
        </a-sub-menu>
        <a-sub-menu>
            <span slot="title"><a-icon type="rise" />推广</span>
            <a-menu-item key="extension:1">Survival</a-menu-item>
        </a-sub-menu>
        <a-menu-item key="about" @click="$router.push({ path: '/about' })">
            <a-icon type="rocket" /> 关于
        </a-menu-item>
        <!-- auth -->
        <template v-if="userBaseInfo.id != -1" style="position: absolute; right: 0">
            <a-badge :count="userBaseInfo.unreadCount" class="auth-avatar">
                <a-avatar :src="baseUrl + userBaseInfo.avatar" />
            </a-badge>
            <a-dropdown class="auth-dropdown">
                <a> {{ userBaseInfo.username }} <a-icon type="down" /></a>
                <a-menu slot="overlay">
                    <a-menu-item>
                        <router-link :to="{ path: '/profile/message', query: { id: userBaseInfo.id } }">我的消息</router-link>
                    </a-menu-item>
                    <a-menu-item>
                        <router-link :to="{ path: '/profile', query: { id: userBaseInfo.id } }">个人信息</router-link>
                    </a-menu-item>
                    <a-menu-item @click="logout">注销</a-menu-item>
                    <a-menu-item v-if="userBaseInfo.isAdmin" @click="$router.push({ path: '/admin' })">管理后台</a-menu-item>
                </a-menu>
            </a-dropdown>
        </template>
        <template v-else>
            <router-link to="/login" class="auth-login">
                <a-button type="primary">登录</a-button>
            </router-link>
            <router-link to="/register" class="auth-register">
                <a-button>注册</a-button>
            </router-link>
        </template>
    </a-menu>
</template>

<script>
import { mapState } from 'vuex'
import { mapMutations } from 'vuex'

export default {
  data() {
    return {
        navbar: null
    }
  },
  async fetch() {
      await this.$axios.get('getUserBaseInfo')
      .then((response) => {
          this.setUserBaseInfo(response.data.data)
      })
  },
  methods: {
      ...mapMutations({
          setUserBaseInfo: 'setUserBaseInfo',
          clearUserBaseInfo: 'clearUserBaseInfo'
      }),

      logout() {
        this.$axios.get('logout')
        this.clearUserBaseInfo()
      },
      navigate(path) {
        if (this.userBaseInfo.id == -1) {
            this.$message.warning('先登录吧～')
        }
        else {
            this.$router.push({ path: path })
        }
      },
      confirm_VirtualDiagnosis() {
          this.$confirm({
            title: '下载【虚拟门诊】',
            content: '虚拟门诊利用虚拟现实技术，提供真实的门诊接诊环境，您之后可以在【查看记录】里查看您的接诊记录，是否要下载？(提取码: 7mrx)',
            onOk() {
                window.open('https://pan.baidu.com/s/1cgM0tvrYj9eENRspyxuZmg', '_blank')
            }
        })
      }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl,
      userBaseInfo: state => state.userBaseInfo
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.nav {
    position: fixed;
    width: 100%;
    top: 0;
    min-height: 36px;
    z-index: 99;
}

.auth-login {
    position: relative;
}
.auth-register {
    position: relative;
}

.auth-avatar {
    position: relative;
}
.auth-dropdown {
    position: relative;
}

@media screen and (min-width: 992px) {
    .auth-login {
        position: absolute;
        right: 10px;
    }
    .auth-register {
        position: absolute;
        right: 80px;
    }

    .auth-avatar {
        float: right;
        right: 1%;
        top: 5px;
    }
    .auth-dropdown {
        float: right;
        right: 2%;
    }
}
</style>
