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
                        <h1>查方剂</h1>
                        <p class="subheading"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <div class="container">
        <div class="row">
            <div class="col-md-12 col-sm-12 text-center">
              <a-spin :spinning="spinning">
                  <a-auto-complete
                    v-model="searchKeyword"
                    :dataSource="completeResult"
                    size="large"
                    @search="autoComplete"
                    placeholder="输入方剂名"
                    class="auto-complete"
                  />
                  <a-button type="primary" @click="search" size="large" class="search">搜索</a-button>
                  <hr />
                  <!-------------------------------------------------------------------------------->
                  <a-table
                    :columns="columns"
                    :dataSource="searchResult"
                    :rowKey="record => record.name"
                    :bordered="true"
                    :pagination="false"
                    class="table"
                  >
                    <router-link
                      slot="action"
                      slot-scope="text, record"
                      target="_blank"
                      :to="{ path: '/prescription/detail', query: { name: record.name } }"
                    >
                      详细
                    </router-link>
                  </a-table>
                </a-spin>
            </div>
        </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
    Footer,
    navbar
  },
  data() {
    return {
      spinning: false,
      searchKeyword: '',
      completeResult: [],
      columns: [{
        title: '方剂',
        dataIndex: 'name',
      }, {
        title: '功效',
        dataIndex: 'function'
      }, {
        title: '类型',
        dataIndex: 'type',
      }, {
        title: '操作',
        scopedSlots: { customRender: 'action' }
      }],
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    return {
        userBaseInfo: userBaseInfo
    }
  },
  methods: {
    search() {
      if (!!this.searchKeyword) {
        this.spinning = true
        this.$axios.get('searchPrescription', {
          params: {
            keyword: this.searchKeyword
          }
        })
        .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
            this.spinning = false
            this.searchResult = response.data.data
          }
        })
      }
      else {
        this.$message.warning('输入些关键字吧～')
      }
    },
    autoComplete(value) {
      this.$axios.post('autoComplete_searchPrescription', qs.stringify({
        keyword: value
      }))
      .then((res) => {
        this.completeResult = res.data.info
      })
    }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
.submit {
  margin-top: 10px;
  margin-right: 10px;
}
.auto-complete {
  width: 600px;
  height: 40px;
  margin-left: 10px;
}
.search {
  margin-left: 10px;
}

@media screen and (max-width: 768px) {
  .auto-complete {
    width: 100px;
  }
}
@media screen and (max-width: 970px) {
  .auto-complete {
    width: 250px;
  }
}
</style>
