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
            <a-sub-menu key="bank">
                <span slot="title"><a-icon type="database" /><span>题库</span></span>
                <a-menu-item key="bank:1" @click="index = 4">上传题库</a-menu-item>
            </a-sub-menu>
            <a-sub-menu key="file">
                <span slot="title"><a-icon type="database" /><span>文件</span></span>
                <a-menu-item key="file:1" @click="index = 5">上传文件</a-menu-item>
            </a-sub-menu>
        </a-menu>
      </a-layout-sider>
      <a-layout class="layout">
        <a-layout-content>
            <adminHot v-show="index == 1" />
            <adminLecture v-show="index == 2" />
            <!--<adminClub v-show="index == 3" />-->
            <!--<adminUploadBank :userBaseInfo="userBaseInfo" :zySubjects="zySubjects" :xySubjects="xySubjects" :bankUploadHistory="bankUploadHistory" v-show="index == 4" />
            <adminUploadFile :userBaseInfo="userBaseInfo" :zySubjects="zySubjects_f" :xySubjects="xySubjects_f" :fileUploadHistory="fileUploadHistory" v-show="index == 5" />
            -->
        </a-layout-content>
      </a-layout>
    </a-layout>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

import adminUser from '~/components/admin/admin_user'
import adminHot from '~/components/admin/admin_hot'
import adminLecture from '~/components/admin/admin_lecture'
//import adminClub from '~/components/admin/admin_club'
import adminUploadBank from '~/components/admin/admin_uploadBank'
import adminUploadFile from '~/components/admin/admin_uploadFile'

export default {
  middleware: 'LoginRequired',
  components: {
      adminUser,
      adminHot,
      adminLecture,
      //adminClub,
      adminUploadBank,
      adminUploadFile
  },
  data() {
    return {
        index: 1
    }
  },
  async asyncData({ $axios, redirect }) {
    let zySubjects = []
    let xySubjects = []
    let zySubjects_f = []
    let xySubjects_f = []
    let bankUploadHistory = []
    let fileUploadHistory = []

    // admin upload bank
    // get subjects and chapters
    /*
    await $axios.get('getBankSubjects')
    .then((response) => {
        response.data.info.forEach(subject => {
            if (subject.subjectType == 'zy') {
                zySubjects.push(subject.key)
            }
            else if (subject.subjectType == 'xy') {
                xySubjects.push(subject.key)
            }
        })
    })
    // get history
    await $axios.get('getBankUploadHistory')
    .then((response) => {
        bankUploadHistory = response.data.info
    })
    // admin upload file
     // get subjects and chapters
    await $axios.get('getFileSubjects')
    .then((response) => {
        response.data.info.forEach(subject => {
            if (subject.subjectType == 'zy') {
                zySubjects_f.push(subject.key)
            }
            else if (subject.subjectType == 'xy') {
                xySubjects_f.push(subject.key)
            }
        })
    })
    // get history
    await $axios.get('getFileUploadHistory')
    .then((response) => {
        fileUploadHistory = response.data.info
    })

    return {
        zySubjects: zySubjects,
        xySubjects: xySubjects,
        zySubjects_f: zySubjects_f,
        xySubjects_f: xySubjects_f,
        bankUploadHistory: bankUploadHistory,
        fileUploadHistory: fileUploadHistory
    }
    */
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
