<template>
  <div>
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>查穴位</h1>
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
                      placeholder="输入穴位名"
                      class="auto-complete"
                    />
                    <a-button type="primary" @click="search" size="large" class="search">搜索</a-button>
                    <hr />
                    <!------------------------------------------------------------------>
                    <a-table
                      :columns="columns"
                      :dataSource="searchResult"
                      rowKey="name"
                      class="table"
                    >
                      <span slot="type" slot-scope="text">
                        <a-tag v-for="(type, index) in text.split(';')" :key="index" :color="randomColor()">
                          {{ type }}
                        </a-tag>
                      </span>
                      <router-link
                        slot="action"
                        slot-scope="text, record"
                        target="_blank"
                        :to="{ path: '/acupuncture/detail', query: { name: record.name } }"
                      >
                        详细
                      </router-link>
                  </a-table>
                </a-spin>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs'

export default {
  layout: 'common',
  data() {
    return {
      spinning: false,
      searchKeyword: '',
      completeResult: [],
      searchResult: [],
      columns: [{
        title: '穴位',
        dataIndex: 'name'
      },{
        title: '定位',
        dataIndex: 'location'
      }, {
        title: '类型',
        dataIndex: '_type',
        scopedSlots: { customRender: 'type' }
      }, {
        title: '属于',
        dataIndex: 'channel'
      }, {
        title: '操作',
        scopedSlots: { customRender: 'action' }
      }]
    }
  },
  async asyncData({ $axios }) {
  },
  methods: {
    randomColor() {
      let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
      return color[Math.round(Math.random() * (color.length - 1))]
    },
    search() {
      if (!!this.searchKeyword) {
        this.spinning = true
        this.$axios.get('searchAcupoint', {
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
      this.$axios.get('autoComplete_searchAcupoint', {
        params: {
          keyword: value
        }
      })
      .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
          this.completeResult = response.data.data
        }
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
