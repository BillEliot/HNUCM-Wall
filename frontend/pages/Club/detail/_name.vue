<template>
    <div>
        <!-- navbar -->
        <navbar :userBaseInfo="userBaseInfo" />
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ clubInfo.name }}</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12 text-center">
                    <a-card title="社团介绍">
                    </a-card>
                    <hr />
                    <a-card title="社团组织">
                        <div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="red">会长</a-tag>
                            </div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="red">副会长</a-tag>
                            </div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="green">会长助理</a-tag>
                            </div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="green">策划理事</a-tag>
                            </div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="green">财务理事</a-tag>
                            </div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="green">网络理事</a-tag>
                            </div>
                            <div class="memeber">
                                <a-avatar :size="64" icon="user" />
                                <h4></h4>
                                <a-tag color="green">宣传理事</a-tag>
                            </div>
                        </div>
                    </a-card>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer'
import navbar from '~/components/navbar'

export default {
  components: {
      navbar,
      Footer
  },
  data() {
    return {
    }
  },
  async asyncData({ $axios, query }) {
    let userBaseInfo = null
    let clubInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    await $axios.post('getClubDetail', qs.stringify({
        name: query.name
    }))
    .then((res) => {
        clubInfo = res.data
    })

    return {
        userBaseInfo: userBaseInfo,
        clubInfo: clubInfo
    }
  },
  methods: {
  },
}
</script>

<style scoped>
.memeber {
    float: left;
    margin-right: 15px;
}
</style>
