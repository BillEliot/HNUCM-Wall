<template>
    <a-layout class="wapper">
      <!-- sider -->
      <a-layout-sider>
          <a-menu
            mode="inline"
            theme="dark"
            style="height: 100%"
        >
            <a-sub-menu key="database">
                <span slot="title"><a-icon type="database" /><span>数据库</span></span>
                <a-menu-item key="database:1" @click="index = 0">用户</a-menu-item>
                <a-menu-item key="database:2" @click="index = 1">校园热点</a-menu-item>
                <a-menu-item key="database:3" @click="index = 2">讲座动态</a-menu-item>
                <a-menu-item key="database:4" @click="index = 3">社团信息</a-menu-item>
            </a-sub-menu>
        </a-menu>
      </a-layout-sider>
      <a-layout>
        <!-- header -->
        <a-layout-header class="header">
            <navbar :userBaseInfo="userBaseInfo" />
        </a-layout-header>
        <!-- content -->
        <a-layout-content>
            <adminUser v-show="index == 0" />
            <adminHot v-show="index == 1" :uid="userBaseInfo.uid" />
            <adminLecture v-show="index == 2" />
            <!--<adminClub v-show="index == 3" />-->
        </a-layout-content>
        <!-- footer -->
        <a-layout-footer style="padding: 0">
            <Footer />
        </a-layout-footer>
      </a-layout>
    </a-layout>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'
import { mapState } from 'vuex'

import adminUser from '~/components/admin/admin_user'
import adminHot from '~/components/admin/admin_hot'
import adminLecture from '~/components/admin/admin_lecture'
//import adminClub from '~/components/admin/admin_club'

export default {
  components: {
      Footer,
      navbar,
      adminUser,
      adminHot,
      adminLecture,
      //adminClub
  },
  data() {
    return {
        index: 1
    }
  },
  async asyncData({ $axios, redirect }) {
    let userBaseInfo = null

    // user base info
    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
        if (!userBaseInfo.isAdmin) {
            redirect({ path: '/' })
        }
    })
    // admin hot
    await $axios.get('getHotList')
    .then((response) => {
        
    })

    return {
        userBaseInfo: userBaseInfo,
    }
  },
  methods: {
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.wapper {
    position: absolute;
    height: 100%;
    width: 100%;
}

.header {
    padding: 0;
    height: 50px;
}
</style>
